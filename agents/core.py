import asyncio
import json
import uuid

# A simple event-based bridge to replace XMPP for local execution
class MessageBridge:
    def __init__(self):
        self.queues = {}

    def register(self, jid):
        self.queues[str(jid)] = asyncio.Queue()
        with open("agents_debug.log", "a") as f:
            f.write(f"REGISTER: {jid}\n")

    async def send(self, msg):
        to_jid = str(msg.to)
        with open("agents_debug.log", "a") as f:
            f.write(f"SEND: from unknown to {to_jid} body={msg.body[:30]}...\n")
        if to_jid in self.queues:
            await self.queues[to_jid].put(msg)
        else:
            print(f"BRIDGE ERROR: Destination {to_jid} not found!")

    async def receive(self, jid, timeout=None):
        try:
            if timeout:
                return await asyncio.wait_for(self.queues[str(jid)].get(), timeout=timeout)
            return await self.queues[str(jid)].get()
        except asyncio.TimeoutError:
            return None

class MockMessage:
    def __init__(self, to, body=None, metadata=None):
        self.to = to
        self.body = body
        self.metadata = metadata or {}

    def set_metadata(self, key, value):
        self.metadata[key] = value

    def get_metadata(self, key):
        return self.metadata.get(key)

# Global bridge for the system
bridge = MessageBridge()

class BaseAgent:
    def __init__(self, jid, password):
        self.jid = jid
        self.config = {}
        bridge.register(str(jid))

    def set(self, key, value):
        self.config[key] = value

    def get(self, key):
        return self.config.get(key)

    async def start(self):
        await self.setup()
        for behav in self.behaviours:
            asyncio.create_task(behav._run())

    async def stop(self):
        for behav in self.behaviours:
            behav.kill()

    async def setup(self):
        pass

    def add_behaviour(self, behav):
        behav.agent = self
        if not hasattr(self, 'behaviours'):
            self.behaviours = []
        self.behaviours.append(behav)

class BaseBehaviour:
    def __init__(self):
        self.agent = None
        self._killed = False

    async def on_start(self):
        pass

    async def run(self):
        pass

    async def on_stop(self):
        pass

    async def _run(self):
        await self.on_start()
        while not self._killed:
            try:
                await self.run()
            except Exception as e:
                print(f"BEHAVIOUR ERROR in {self.agent.jid}: {e}")
            await asyncio.sleep(0.01)
        await self.on_stop()

    def kill(self):
        self._killed = True

    async def send(self, msg):
        await bridge.send(msg)

    async def receive(self, timeout=None):
        return await bridge.receive(self.agent.jid, timeout=timeout)
