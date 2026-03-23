import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import time

# Styling
st.set_page_config(page_title="📊 Data Analytics Dashboard", layout="wide", page_icon="🛡️")

API_URL = "http://localhost:8000"

st.title("📊 Real-time Data Analytics")
st.markdown("---")

def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return None
    return None

placeholder = st.empty()

while True:
    distribution = fetch_data("distribution")
    status_data = fetch_data("status")
    
    with placeholder.container():
        # Performance Summary
        if status_data and distribution:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("System Status")
                st.info(f"Status: {status_data.get('status', 'offline').upper()}")
                st.metric("Total Flows", sum(distribution.values()))
                
                last_update = status_data.get("last_update", {})
                if last_update:
                    st.write("**Last Event Sample:**")
                    st.json({k: v for k, v in last_update.items() if k in ["protocol_type", "service", "label"]})

            with col2:
                st.subheader("Traffic Class Distribution")
                if distribution:
                    df = pd.DataFrame(list(distribution.items()), columns=["Type", "Count"])
                    fig = go.Figure(data=[go.Bar(x=df["Type"], y=df["Count"], marker_color="#3366cc")])
                    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Waiting for data distribution...")
            
            # Additional Analytics (e.g., protocol_type)
            # This would require SupervisorAgent to track more data, coming soon!
        else:
            st.error("⚠️ API Not responding. Make sure `backend/main.py` is running.")
            
    time.sleep(2)
