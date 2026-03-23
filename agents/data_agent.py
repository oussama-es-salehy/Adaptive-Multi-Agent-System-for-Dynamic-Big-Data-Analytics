import asyncio
import json
from agents.core import BaseAgent, BaseBehaviour, MockMessage
try:
    from kafka.config import KAFKA_BROKER, TOPIC_NAME
except ImportError:
    from ..kafka.config import KAFKA_BROKER, TOPIC_NAME

class DataAgent(BaseAgent):
    class ConsumeKafka(BaseBehaviour):
        async def on_start(self):
            import aiokafka
            print(f"DataAgent: Starting Kafka consumer on {KAFKA_BROKER} for topic {TOPIC_NAME}...")
            try:
                self.consumer = aiokafka.AIOKafkaConsumer(
                    TOPIC_NAME,
                    bootstrap_servers=KAFKA_BROKER,
                    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                    auto_offset_reset='earliest'
                )
                await self.consumer.start()
                print("DataAgent: Consumer connected and started.")
            except Exception as e:
                print(f"DataAgent ERROR: Failed to start Kafka consumer: {e}")

        async def run(self):
            # Consume message from Kafka
            async for msg in self.consumer:
                learning_agent_jid = self.agent.get("learning_agent_jid")
                
                if learning_agent_jid:
                    msg_to_learning = MockMessage(to=learning_agent_jid)
                    msg_to_learning.set_metadata("ontology", "intrusion-detection")
                    msg_to_learning.set_metadata("performative", "inform")
                    msg_to_learning.body = json.dumps(msg.value)
                    await self.send(msg_to_learning)
                else:
                    print("DataAgent: LearningAgent JID not configured!")
                
                # Small delay to prevent tight loop if Kafka is fast
                await asyncio.sleep(0.01)

        async def on_stop(self):
            await self.consumer.stop()

    async def setup(self):
        behav = self.ConsumeKafka()
        self.add_behaviour(behav)
