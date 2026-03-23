import asyncio
import aiokafka
import json

async def test_kafka():
    print("Connecting to Kafka...")
    consumer = aiokafka.AIOKafkaConsumer(
        'network_topic',
        bootstrap_servers='127.0.0.1:9092',
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        print("Waiting for messages...")
        msg = await asyncio.wait_for(consumer.getone(), timeout=10)
        print(f"SUCCESS: Got message at offset {msg.offset}")
        print(f"Content snippet: {str(msg.value)[:100]}")
    except asyncio.TimeoutError:
        print("TIMEOUT: No messages in topic 'network_topic'")
    except Exception as e:
        print(f"ERROR: {str(e)}")
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(test_kafka())
