import json
from agents.core import BaseAgent, BaseBehaviour
from models.clustering import get_clustering_model

class ClusterAgent(BaseAgent):
    class ClusterCycle(BaseBehaviour):
        async def on_start(self):
            self.model = get_clustering_model()
            print("ClusterAgent: Incremental KMeans initialized.")

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                data = json.loads(msg.body)
                # Filter features for clustering
                x = {k: v for k, v in data.items() if isinstance(v, (int, float))}
                
                # Cluster
                cluster_label = self.model.predict_one(x)
                self.model.learn_one(x)

    async def setup(self):
        behav = self.ClusterCycle()
        self.add_behaviour(behav)
