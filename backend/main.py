import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

app = FastAPI(title="🛡️ MAS Intrusion Detection API")

# Enable CORS for Streamlit dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

METRICS_FILE = "data/metrics.json"

@app.get("/")
async def root():
    return {"message": "MAS Intrusion Detection API is running", "endpoints": ["/metrics", "/distribution", "/status"]}

@app.get("/metrics")
async def get_metrics():
    if not os.path.exists(METRICS_FILE):
        return {"error": "No metrics available yet"}
    
    try:
        with open(METRICS_FILE, "r") as f:
            data = json.load(f)
        return data.get("metrics", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/distribution")
async def get_distribution():
    if not os.path.exists(METRICS_FILE):
        return {}
    
    try:
        with open(METRICS_FILE, "r") as f:
            data = json.load(f)
        return data.get("class_distribution", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    if not os.path.exists(METRICS_FILE):
        return {"status": "waiting_for_data", "drift_count": 0}
    
    try:
        with open(METRICS_FILE, "r") as f:
            data = json.load(f)
        return {
            "status": "running",
            "drift_count": data.get("drift_count", 0),
            "last_update": data.get("last_update", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history():
    if not os.path.exists(METRICS_FILE):
        return []
    
    try:
        with open(METRICS_FILE, "r") as f:
            data = json.load(f)
        return data.get("metrics_history", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
