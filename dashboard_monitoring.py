import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

# Styling
st.set_page_config(page_title="🤖 Model Monitoring Dashboard", layout="wide", page_icon="📈")

API_URL = "http://localhost:8000"

st.title("🤖 Model Performance & Monitoring")
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
    metrics = fetch_data("metrics")
    status_data = fetch_data("status")
    
    with placeholder.container():
        if metrics and status_data:
            # Row 1: Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Accuracy", f"{metrics.get('Accuracy', 0):.4f}")
            col2.metric("F1-Score", f"{metrics.get('F1', 0):.4f}")
            col3.metric("Precision", f"{metrics.get('Precision', 0):.4f}")
            col4.metric("Recall", f"{metrics.get('Recall', 0):.4f}")

            st.markdown("---")
            
            # Row 2: Performance Curve & Drift
            col_a, col_b = st.columns([2, 1])
            
            with col_a:
                st.subheader("Performance Evolution")
                history = fetch_data("history")
                if history:
                    df_hist = pd.DataFrame(history)
                    fig = px.line(df_hist, x="timestamp", y="accuracy", title="Real-time Accuracy Curve")
                    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Visualizing trend data...")
                
            with col_b:
                st.subheader("Concept Drift Alerts")
                drift_count = status_data.get("drift_count", 0)
                if drift_count > 0:
                    st.error(f"⚠️ {drift_count} Global Concept Drifts Detected!")
                else:
                    st.success("✅ No Concept Drift detected")
        else:
            st.error("⚠️ API Not responding. Make sure `backend/main.py` is running.")
            
    time.sleep(2)
