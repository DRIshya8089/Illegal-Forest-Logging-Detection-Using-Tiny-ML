import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Node metadata (static)
NODES_INFO = [
    {"Node ID": "Node-01", "Latitude": 10.0765, "Longitude": 76.3472, "Node Status": "Active"},
    {"Node ID": "Node-02", "Latitude": 10.0783, "Longitude": 76.3481, "Node Status": "Active"},
    {"Node ID": "Node-03", "Latitude": 10.0791, "Longitude": 76.3500, "Node Status": "Active"},
    {"Node ID": "Node-04", "Latitude": 10.0801, "Longitude": 76.3490, "Node Status": "Active"},
    {"Node ID": "Node-05", "Latitude": 10.0810, "Longitude": 76.3510, "Node Status": "Maintenance"},
    {"Node ID": "Node-06", "Latitude": 10.0820, "Longitude": 76.3520, "Node Status": "Maintenance"},
]

# Temperature status label
def label_temp(t):
    if t >= 50:
        return f"High ({t:.1f}°C)"
    elif t <= 20:
        return f"Low ({t:.1f}°C)"
    return f"Normal ({t:.1f}°C)"

# Weighted event simulation
def simulate_event():
    events = ['Safe', 'Chainsaw', 'Tree Fall', 'Wildfire', 'Battery Low', 'Human Intrusion']
    weights = [40, 10, 7, 5, 3, 15]
    return random.choices(events, weights=weights, k=1)[0]

# Create initial DataFrame with random data
def initialize_nodes():
    rows = []
    for node in NODES_INFO:
        pct = random.randint(10, 95)
        temp = round(random.uniform(15.0, 60.0), 1)
        timestamp = ""  # no timestamp initially
        rows.append({
            **node,
            "Activity Status": "Safe",
            "Battery Percentage": f"{pct}%",
            "Temperature (°C)": temp,
            "Temperature Status": label_temp(temp),
            "Occurred at": timestamp,
        })
    return pd.DataFrame(rows)

# Page configuration
st.set_page_config(page_title="Forest Safety Detection", layout="wide")
st.title("Illegal Forest Logging and Trespassing Detection")
st.markdown("---")

# Initialize state
if 'nodes_df' not in st.session_state:
    st.session_state.nodes_df = initialize_nodes()

# Update on refresh
if st.sidebar.button("🔄 Refresh Data"):
    df = st.session_state.nodes_df.copy()
    for idx, row in df.iterrows():
        if row['Node Status'] == 'Active':
            event = simulate_event()
            voltage = round(random.uniform(3.0, 4.0), 2)
            pct = random.randint(10, 95)
            temp = round(random.uniform(15.0, 60.0), 1)
            timestamp = datetime.now().strftime("%I:%M:%S %p") if event != 'Safe' else ""
            df.at[idx, 'Activity Status'] = event
            df.at[idx, 'Battery Percentage'] = f"{pct}%"
            df.at[idx, 'Temperature (°C)'] = temp
            df.at[idx, 'Temperature Status'] = label_temp(temp)
            df.at[idx, 'Occurred at'] = timestamp
    st.session_state.nodes_df = df

df = st.session_state.nodes_df

# Display table without horizontal scroll
st.subheader("📡 Node Status Overview")
st.table(df[[
    'Node ID', 'Node Status', 'Latitude', 'Longitude',
    'Battery Percentage',
    'Temperature Status', 'Activity Status', 'Occurred at'
]])

# Sidebar summary metrics
total_nodes = len(df)
active_nodes = (df['Node Status'] == 'Active').sum()
maint_nodes = (df['Node Status'] == 'Maintenance').sum()
alerts_today = (df['Activity Status'] != 'Safe').sum()
fire_alerts = (df['Activity Status'] == 'Wildfire').sum()
battery_critical = df['Battery Percentage'].apply(
    lambda x: int(x.rstrip('%')) < 20 if x else False
).sum()

with st.sidebar:
    st.subheader("📊 Summary")
    st.markdown(f"- **Total Nodes:** {total_nodes}  ")
    st.markdown(f"- **Active Nodes:** {active_nodes}  ")
    st.markdown(f"- **Maintenance Nodes:** {maint_nodes}  ")
    st.markdown("---")
    col1, col2 = st.columns(2)
    col1.metric("Active Nodes", active_nodes)
    col2.metric("Unusual Activity", alerts_today)
    col3, col4 = st.columns(2)
    col3.metric("🔥 Fire Alerts", fire_alerts)
    col4.metric("🔋 Critical Batteries", battery_critical)

st.markdown("---")
st.caption("Built for iCDAC Internship – Illegal Tree Logging Detection Project")
