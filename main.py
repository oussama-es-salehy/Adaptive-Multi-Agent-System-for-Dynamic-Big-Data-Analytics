import asyncio
from agents.data_agent import DataAgent
from agents.learning_agent import LearningAgent
from agents.drift_agent import DriftAgent
from agents.cluster_agent import ClusterAgent
from agents.supervisor_agent import SupervisorAgent

async def main():
    print("Starting Serverless Multi-Agent System (No XMPP Required)...")
    
    # Initializing agents
    supervisor = SupervisorAgent("supervisor", "password")
    drift = DriftAgent("drift", "password")
    learning = LearningAgent("learning", "password")
    cluster = ClusterAgent("cluster", "password")
    data_collector = DataAgent("data", "password")
    
    # Set up contacts
    data_collector.set("learning_agent_jid", str(learning.jid))
    learning.set("drift_agent_jid", str(drift.jid))
    learning.set("supervisor_agent_jid", str(supervisor.jid))
    drift.set("supervisor_agent_jid", str(supervisor.jid))

    # Start all agents
    await supervisor.start()
    await drift.start()
    await learning.start()
    await cluster.start()
    await data_collector.start()

    print("MAS is running. Press CTRL+C to stop.")
    
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        # Stop all agents
        await supervisor.stop()
        await drift.stop()
        await learning.stop()
        await cluster.stop()
        await data_collector.stop()
        print("MAS stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
