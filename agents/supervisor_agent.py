import json
import os
import time
from agents.core import BaseAgent, BaseBehaviour, MockMessage
from evaluation.metrics import PerformanceMetrics

class SupervisorAgent(BaseAgent):
    class MonitoringCycle(BaseBehaviour):
        async def on_start(self):
            self.drift_count = 0
            self.metrics = PerformanceMetrics()
            self.class_distribution = {}
            self.metrics_history = []
            self.save_path = "data/metrics.json"
            # Ensure data directory exists
            os.makedirs("data", exist_ok=True)
            print("SupervisorAgent: Ready to coordinate.")

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                data = json.loads(msg.body)
                event = data.get("event")
                
                # Handle drift events
                if event == "concept_drift_detected":
                    self.drift_count += 1
                    print(f"SupervisorAgent ALERT: Global Concept Drift #{self.drift_count} has been reported.")
                
                # Handle performance updates for dashboard
                y_true = data.get("y_true")
                y_pred = data.get("y_pred")
                if y_true is not None and y_pred is not None:
                    # Update metrics
                    self.metrics.update(y_true, y_pred)
                    
                    # Update class distribution
                    label_str = str(y_true)
                    self.class_distribution[label_str] = self.class_distribution.get(label_str, 0) + 1
                    
                    # Store historical metrics
                    report = self.metrics.get_report()
                    self.metrics_history.append({
                        "timestamp": time.time(),
                        "accuracy": report.get("Accuracy", 0),
                        "f1": report.get("F1", 0)
                    })
                    
                    if len(self.metrics_history) > 100:
                        self.metrics_history.pop(0)

                    # Save to file for dashboard
                    dashboard_data = {
                        "metrics": report,
                        "metrics_history": self.metrics_history,
                        "drift_count": self.drift_count,
                        "class_distribution": self.class_distribution,
                        "last_update": data 
                    }
                    with open(self.save_path, "w") as f:
                        json.dump(dashboard_data, f)

    async def setup(self):
        behav = self.MonitoringCycle()
        self.add_behaviour(behav)
