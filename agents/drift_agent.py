import json
from agents.core import BaseAgent, BaseBehaviour, MockMessage
from drift.adwin_detector import DriftDetector

class DriftAgent(BaseAgent):
    class CheckDrift(BaseBehaviour):
        async def on_start(self):
            self.detector = DriftDetector()
            print("DriftAgent: ADWIN detector initialized.")

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                data = json.loads(msg.body)
                error = data.get("error", 0)
                
                # ADWIN expects a value representing the current model error (0 or 1 usually)
                drift_detected = self.detector.update(error)
                
                if drift_detected:
                    print(f"DriftAgent: DRIFT DETECTED!")
                    # Notify Supervisor
                    supervisor_agent_jid = self.agent.get("supervisor_agent_jid")
                    
                    if supervisor_agent_jid:
                        msg_to_supervisor = MockMessage(to=supervisor_agent_jid)
                        msg_to_supervisor.set_metadata("ontology", "supervisor-notify")
                        msg_to_supervisor.body = json.dumps({"event": "concept_drift_detected"})
                        await self.send(msg_to_supervisor)

    async def setup(self):
        behav = self.CheckDrift()
        self.add_behaviour(behav)
