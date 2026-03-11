import streamlit as st
from backend import graph_app, AgentState
from langchain_core.messages import HumanMessage, AIMessage

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="LangGraph Multi-Agent Chatbot", layout="centered")

st.title("🤖 Multi-Agent Chatbot (LangGraph + Streamlit)")
st.write("This chatbot uses a multi-agent workflow to process vehicle maintenance queries.")

# -----------------------------
# Session State Initialization
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar (Vehicle Context)
# -----------------------------
with st.sidebar:
    st.header("Vehicle Context")

    vehicle_id = st.text_input("Vehicle ID", "V123")
    odometer = st.number_input("Odometer (km)", value=42000)
    engine_temp = st.number_input("Engine Temperature (°C)", value=90)
    oil_pressure = st.number_input("Oil Pressure", value=30)

    model = st.text_input("Vehicle Model", "Hatchback X")
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "EV"])
    city = st.text_input("City", "Kanpur")

    last_service = st.text_input("Last Service Date", "2025-11-15")
    previous_issues = st.text_area("Previous Issues (comma separated)", "brake wear")

# -----------------------------
# Display Chat History
# -----------------------------
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"

    with st.chat_message(role):
        st.write(msg.content)

# -----------------------------
# Chat Input
# -----------------------------
if prompt := st.chat_input("Ask about vehicle maintenance..."):

    # Save user message
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)

    with st.chat_message("user"):
        st.write(prompt)

    # Convert issues string → list
    issues_list = [i.strip() for i in previous_issues.split(",") if i.strip()]

    # -----------------------------
    # LangGraph Agent State
    # -----------------------------
    state: AgentState = {
        "messages": [],
        "vehicle_id": vehicle_id,
        "sensor_data": {
            "engine_temp": float(engine_temp),
            "oil_pressure": float(oil_pressure),
            "odometer_km": float(odometer),
        },
        "vehicle_profile": {
            "model": model,
            "fuel_type": fuel_type,
            "city": city,
        },
        "service_history": {
            "last_service_date": last_service,
            "previous_issues": issues_list,
        },
        "risk_score": "",
        "risk_explanation": "",
        "service_slots": [],
        "chosen_slot": "",
        "notification_text": "",
        "notification_status": "",
        "next_agent": "supervisor",
    }

    # -----------------------------
    # Run LangGraph Workflow
    # -----------------------------
    with st.chat_message("assistant"):
        with st.spinner("Agents analyzing vehicle data..."):

            result = graph_app.invoke(state)

        # Create readable response
        response = f"""
### Vehicle Analysis Report

**Vehicle ID:** {result['vehicle_id']}

**Risk Score:** {result['risk_score']}

**Explanation:**  
{result['risk_explanation']}

**Recommended Service Slot:**  
{result['chosen_slot']}

**Notification:**  
{result['notification_text']}
"""

        st.write(response)

        # Save AI message
        ai_msg = AIMessage(content=response)
        st.session_state.messages.append(ai_msg)