import asyncio
import json
import pandas as pd
import os
import requests
from aiokafka import AIOKafkaProducer
try:
    from kafka.config import KAFKA_BROKER, TOPIC_NAME
except ImportError:
    from config import KAFKA_BROKER, TOPIC_NAME

# NSL-KDD column names
COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", 
    "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised", 
    "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells", 
    "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count", 
    "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate", 
    "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", 
    "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate", 
    "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate", 
    "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate", 
    "label", "difficulty_level"
]

TRAIN_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain+.txt"
TEST_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest+.txt"

DATA_DIR = os.path.join(os.getcwd(), "data", "raw")

def download_file(url, filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Downloading {url}...")
        response = requests.get(url)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded to {filepath}")
    return filepath

async def stream_nsl_kdd():
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Download files
    train_path = download_file(TRAIN_URL, "KDDTrain+.txt")
    test_path = download_file(TEST_URL, "KDDTest+.txt")

    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        request_timeout_ms=10000, # Give it more time to establish
        retry_backoff_ms=500      # Retry connecting if failed
    )

    await producer.start()
    
    try:
        print(f"Starting NSL-KDD producer on topic: {TOPIC_NAME}")
        
        # Load and stream Train data first, then Test data
        while True:
            for path in [train_path, test_path]:
                print(f"Streaming from {path}...")
                # Use chunksize for large files if needed, but NSL-KDD is manageable
                df = pd.read_csv(path, names=COLUMNS)
                
                count = 0
                for _, row in df.iterrows():
                    data = row.to_dict()
                    await producer.send_and_wait(TOPIC_NAME, data)
                    count += 1
                    if count % 100 == 0:
                        print(f"Sent {count} rows...")
                    # Sleep briefly to simulate real-time stream
                    await asyncio.sleep(0.1) # Reduced sleep for faster testing
            print("Finished dataset. Restarting loop...")

    finally:
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(stream_nsl_kdd())
