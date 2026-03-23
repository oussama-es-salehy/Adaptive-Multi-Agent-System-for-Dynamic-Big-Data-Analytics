import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
import time
import os
import subprocess

# Config
st.set_page_config(page_title="🛡️ MAS Advanced Dashboard", layout="wide", page_icon="🛡️")

API_URL = "http://127.0.0.1:8080"

# Auto-start Backend if not running
try:
    requests.get(API_URL, timeout=1)
except:
    import sys
    st.sidebar.warning("📡 Starting Backend API...")
    # Use the same python executable as the dashboard
    subprocess.Popen([sys.executable, "backend/main.py"], 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)

# Sidebar Navigation
st.sidebar.title("🛡️ IDS Control Center")
page = st.sidebar.radio("Navigate", ["📊 Global Analytics", "🤖 Model Monitoring"])

def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", timeout=3)
        if response.status_code == 200:
            return response.json()
        else:
            st.sidebar.error(f"Error {response.status_code} on {endpoint}")
    except Exception as e:
        st.sidebar.error(f"Connection Error: {str(e)}")
        return None
    return None

# --- SHARED AREA ---
if page == "📊 Global Analytics":
    st.title("📊 Network Traffic Analytics")
    st.markdown("---")
    
    distribution = fetch_data("distribution")
    status_data = fetch_data("status")
    
    if status_data and distribution:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("System Status")
            st.info(f"Status: {status_data.get('status', 'offline').upper()}")
            st.metric("Total Flows", sum(distribution.values()))
            
            last_update = status_data.get("last_update", {})
            if last_update:
                st.write("**Last Sample:**")
                st.caption(f"Service: {last_update.get('service')}, Label: {last_update.get('label')}")

        with col2:
            st.subheader("Class Distribution")
            df = pd.DataFrame(list(distribution.items()), columns=["Type", "Count"])
            fig = px.bar(df, x="Type", y="Count", color="Type", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("⚠️ API Not responding. (Run `backend/main.py`) ")

elif page == "🤖 Model Monitoring":
    st.title("🤖 Online Model Monitoring")
    st.markdown("---")
    
    metrics = fetch_data("metrics")
    status_data = fetch_data("status")
    history = fetch_data("history")
    
    if metrics and status_data:
        # Metrics Row
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Accuracy", f"{metrics.get('Accuracy', 0):.4f}")
        c2.metric("F1-Score", f"{metrics.get('F1', 0):.4f}")
        c3.metric("Precision", f"{metrics.get('Precision', 0):.4f}")
        c4.metric("Recall", f"{metrics.get('Recall', 0):.4f}")

        st.markdown("---")
        
        # History & Drift
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.subheader("Accuracy Trend")
            if history:
                df_hist = pd.DataFrame(history)
                fig = px.line(df_hist, x="timestamp", y="accuracy", title="Performance Evolution")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Waiting for history data...")

        with col_b:
            st.subheader("Concept Drift Alerts")
            drift_count = status_data.get("drift_count", 0)
            if drift_count > 0:
                st.error(f"⚠️ {drift_count} Global Drifts Detected!")
            else:
                st.success("✅ Model is stable")
    else:
        st.error("⚠️ API Not responding.")

# Auto-refresh logic (optional in UI)
if st.sidebar.button("Force Refresh"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("MAS Real-time Analytics v2.0")
