# frontend.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agentic_oem import graph_app, AgentState

st.set_page_config(page_title="OEM Predictive Maintenance", layout="wide")
st.title("🚗 OEM Predictive Maintenance Orchestrator")

# --- SIDEBAR: vehicle context + Agentic AI toggle ---
with st.sidebar:
    st.header("Vehicle Context")

    vehicle_id = st.text_input("Vehicle ID", "DL12AB1234")

    km = st.number_input("Odometer (km)", value=42000)
    engine_temp = st.number_input("Engine temp (°C)", value=90)
    oil_pressure = st.number_input("Oil pressure", value=30)

    model = st.text_input("Model", "Hatchback X")
    fuel_type = st.selectbox("Fuel type", ["Petrol", "Diesel", "EV"], index=0)
    city = st.text_input("City", "Kanpur")

    last_service = st.text_input("Last service date", "2025-11-15")
    previous_issues = st.text_area(
        "Previous issues (comma separated)",
        "brake wear"
    )

    st.markdown("### Agentic AI Enrollment")
    agentic_enabled = st.checkbox(
        "Enable Agentic AI (auto-enroll, schedule, notify)",
        value=True
    )

# helper to build base state from sidebar
def build_base_state() -> AgentState:
    issues_list = [x.strip() for x in previous_issues.split(",") if x.strip()]
    return {
        "messages": [],
        "vehicle_id": vehicle_id,
        "sensor_data": {
            "engine_temp": float(engine_temp),
            "oil_pressure": float(oil_pressure),
            "odometer_km": float(km),
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
        "next_agent": "",
    }

# --- MAIN: two tabs ---
tab_form, tab_chat = st.tabs(["📋 Form Run", "💬 Chat"])

# ========== TAB 1: FORM RUN ==========
with tab_form:
    st.subheader("One-shot workflow run")

    run_clicked = st.button("Run Workflow (uses sidebar data)")

    if run_clicked:
        state = build_base_state()

        if agentic_enabled:
            with st.spinner("Running Agentic AI (auto enrollment + notification)..."):
                result = graph_app.invoke(state)

            st.success("Agentic AI enrollment completed.")

            st.markdown("#### 🔎 Risk & Explanation")
            st.write("**Vehicle ID:**", result["vehicle_id"])
            st.write("**Risk score:**", result["risk_score"])
            st.write("**Risk explanation:**", result["risk_explanation"])

            st.markdown("#### 🗓️ Scheduled Slot")
            st.write("**Available slots:**", result["service_slots"])
            st.write("**Chosen slot:**", result["chosen_slot"])

            st.markdown("#### 📨 Enrollment Notification")
            st.write("**Message:**", result["notification_text"])
            st.write("**Status:**", result["notification_status"])

        else:
            with st.spinner("Running basic analysis (no auto enrollment)..."):
                result = graph_app.invoke(state)

            st.info("Agentic AI disabled: showing only analysis.")
            st.markdown("#### 🔎 Risk & Explanation")
            st.write("**Vehicle ID:**", result["vehicle_id"])
            st.write("**Risk score:**", result["risk_score"])
            st.write("**Risk explanation:**", result["risk_explanation"])

# ========== TAB 2: CHAT ==========
with tab_chat:
    st.subheader("Chat with Agentic OEM AI")

    # init chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # render history
    for msg in st.session_state.chat_messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.write(msg.content)

    # chat input
    if prompt := st.chat_input("Ask about this vehicle's maintenance..."):
        user_msg = HumanMessage(content=prompt)
        st.session_state.chat_messages.append(user_msg)

        with st.chat_message("assistant"):
            state = build_base_state()

            with st.spinner(
                "Thinking with multi-agent workflow (Agentic AI: "
                + ("ON" if agentic_enabled else "OFF")
                + ")..."
            ):
                result = graph_app.invoke(state)

            # you can branch on agentic_enabled if you want different behavior;
            # here we just answer differently in text
            if agentic_enabled:
                reply_text = (
                    f"Based on the current data for {result['vehicle_id']}, "
                    f"your risk is **{result['risk_score']}**.\n\n"
                    f"Reason: {result['risk_explanation']}\n\n"
                    f"I have also scheduled a service slot: {result['chosen_slot']}.\n\n"
                    f"Notification message would be:\n\n{result['notification_text']}"
                )
            else:
                reply_text = (
                    f"Based on the current data for {result['vehicle_id']}, "
                    f"your risk is **{result['risk_score']}**.\n\n"
                    f"Reason: {result['risk_explanation']}\n\n"
                    f"(Agentic AI is OFF, so I am not auto-enrolling or scheduling.)"
                )

            st.write(reply_text)
            ai_msg = AIMessage(content=reply_text)
            st.session_state.chat_messages.append(ai_msg)
