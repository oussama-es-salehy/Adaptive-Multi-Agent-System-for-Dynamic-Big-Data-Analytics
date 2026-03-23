import json
from agents.core import BaseAgent, BaseBehaviour, MockMessage
from models.online_model import get_online_model
from river import compose

class LearningAgent(BaseAgent):
    class LearnCycle(BaseBehaviour):
        async def on_start(self):
            # We use a pipeline that handles categorical variables
            self.model = get_online_model()
            self.pending_feedback = {} # Cache for delayed learning
            print("LearningAgent: Model initialized with Delayed Learning support.")

        async def run(self):
            try:
                msg = await self.receive(timeout=10)
                if msg:
                    data = json.loads(msg.body)
                    label_raw = data.pop('label', None)
                    flow_id = data.get('flow_id', str(hash(json.dumps(data))))

                    # Pre-processing: convert all numeric strings to floats
                    x = {}
                    for k, v in data.items():
                        if k == 'flow_id': continue
                        try:
                            x[k] = float(v)
                        except (ValueError, TypeError):
                            x[k] = v # String/Categorical
                    
                    if label_raw is None:
                        y_pred_raw = self.model.predict_one(x)
                        self.pending_feedback[flow_id] = (x, y_pred_raw)
                        return

                    # Map label to binary (0: normal, 1: attack)
                    label = 0 if str(label_raw).lower() == 'normal' else 1
                    
                    # CASE 2: Label arrived
                    if not x and flow_id in self.pending_feedback:
                        x, y_pred_binary = self.pending_feedback.pop(flow_id)
                    else:
                        y_pred_binary = self.model.predict_one(x) # 0 or 1
                    
                    # Learn
                    self.model.learn_one(x, label)
                    
                    if y_pred_binary is not None:
                        error = 1 if y_pred_binary != label else 0
                        drift_agent_jid = self.agent.get("drift_agent_jid")
                        if drift_agent_jid:
                            msg_to_drift = MockMessage(to=drift_agent_jid)
                            msg_to_drift.body = json.dumps({"error": error})
                            await self.send(msg_to_drift)
                        
                        supervisor_agent_jid = self.agent.get("supervisor_agent_jid")
                        if supervisor_agent_jid:
                            msg_to_supervisor = MockMessage(to=supervisor_agent_jid)
                            msg_to_supervisor.set_metadata("ontology", "performance-monitoring")
                            # Send mapped binary values for metrics
                            msg_to_supervisor.body = json.dumps({"y_true": label, "y_pred": y_pred_binary})
                            await self.send(msg_to_supervisor)
            except Exception as e:
                import traceback
                with open("agents_debug.log", "a") as f:
                    f.write(f"LEARNING ERROR: {str(e)}\n{traceback.format_exc()}\n")

    async def setup(self):
        behav = self.LearnCycle()
        self.add_behaviour(behav)
