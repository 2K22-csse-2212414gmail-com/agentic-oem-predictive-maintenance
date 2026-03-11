from typing_extensions import TypedDict
from typing import Annotated, List, Dict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "add_messages"]
    vehicle_id: str

    sensor_data: Dict[str, float]
    vehicle_profile: Dict[str, str]
    service_history: Dict[str, list]

    risk_score: str
    risk_explanation: str

    service_slots: List[str]
    chosen_slot: str

    notification_text: str
    notification_status: str

    next_agent: str  # "sensor" | "data" | "predict" | "scheduler" | "notify" | "FINISH"
def sensor_node(state: AgentState) -> dict:
    print("SensorAgent running for", state["vehicle_id"])
    # Example: enrich sensor_data (you can replace with real logic)
    new_data = dict(state.get("sensor_data", {}))
    new_data.setdefault("engine_temp", 90.0)
    new_data.setdefault("oil_pressure", 30.0)
    new_data.setdefault("odometer_km", 42000.0)
    return {"sensor_data": new_data}
def data_node(state: AgentState) -> dict:
    print("DataAgent running for", state["vehicle_id"])
    # Example: enrich service history
    history = dict(state.get("service_history", {}))
    history.setdefault("last_service_date", "2025-11-15")
    history.setdefault("previous_issues", ["brake wear"])
    return {"service_history": history}
def predict_node(state: AgentState) -> dict:
    print("PredictAgent running for", state["vehicle_id"])
    km = state["sensor_data"].get("odometer_km", 0)
    risk = "HIGH" if km >= 40000 else "MEDIUM"
    explanation = f"Risk {risk} based on {km} km and previous issues {state['service_history'].get('previous_issues', [])}"
    return {
        "risk_score": risk,
        "risk_explanation": explanation,
    }
def scheduler_node(state: AgentState) -> dict:
    print("SchedulerAgent running for", state["vehicle_id"])
    # Simple mocked slots
    slots = [
        "2026-03-10 10:00 @ Kanpur SC1",
        "2026-03-11 14:00 @ Kanpur SC2",
    ]
    chosen = slots[0]
    return {
        "service_slots": slots,
        "chosen_slot": chosen,
    }
def notify_node(state: AgentState) -> dict:
    print("NotificationAgent running for", state["vehicle_id"])
    text = f"Dear customer, your vehicle {state['vehicle_id']} is booked for {state['chosen_slot']}."
    return {
        "notification_text": text,
        "notification_status": "SENT",
    }
def supervisor_node(state: AgentState) -> dict:
    """
    Router/master: decides which agent to run next.
    It NEVER calls tools directly and ONLY sets next_agent.
    """

    # First-time default if next_agent missing/empty
    if not state.get("next_agent"):
        # Start with sensor check
        return {"next_agent": "sensor"}

    # 1) If sensor_data missing → go to sensor
    if not state.get("sensor_data"):
        return {"next_agent": "sensor"}

    # 2) If service_history missing → go to data
    if not state.get("service_history"):
        return {"next_agent": "data"}

    # 3) If no risk_score yet → go to predict
    if not state.get("risk_score"):
        return {"next_agent": "predict"}

    # 4) If risk exists but no slots yet → go to scheduler
    if state["risk_score"] in ("HIGH", "MEDIUM", "LOW") and not state.get("service_slots"):
        return {"next_agent": "scheduler"}

    # 5) If slot chosen but notification not sent → go to notify
    if state.get("chosen_slot") and state.get("notification_status") != "SENT":
        return {"next_agent": "notify"}

    # 6) If notification is sent, we are done
    if state.get("notification_status") == "SENT":
        return {"next_agent": "FINISH"}

    # Fallback safety: if nothing matched, finish to avoid infinite loop
    return {"next_agent": "FINISH"}
workflow = StateGraph(AgentState)

workflow.add_node("supervisor", supervisor_node)
workflow.add_node("sensor", sensor_node)
workflow.add_node("data", data_node)
workflow.add_node("predict", predict_node)
workflow.add_node("scheduler", scheduler_node)
workflow.add_node("notify", notify_node)

workflow.set_entry_point("supervisor")

workflow.add_conditional_edges(
    "supervisor",
    lambda s: s["next_agent"],
    {
        "sensor": "sensor",
        "data": "data",
        "predict": "predict",
        "scheduler": "scheduler",
        "notify": "notify",
        "FINISH": END,
    },
)

for worker in ["sensor", "data", "predict", "scheduler", "notify"]:
    workflow.add_edge(worker, "supervisor")

graph_app = workflow.compile()
initial_state: AgentState = {
    "messages": [],
    "vehicle_id": "DL12AB1234",
    "sensor_data": {"engine_temp": 90.0, "oil_pressure": 30.0, "odometer_km": 42000.0},
    "vehicle_profile": {"model": "Hatchback X", "fuel_type": "Petrol", "city": "Kanpur"},
    "service_history": {"last_service_date": "2025-11-15", "previous_issues": ["brake wear"]},
    "risk_score": "",
    "risk_explanation": "",
    "service_slots": [],
    "chosen_slot": "",
    "notification_text": "",
    "notification_status": "",
    "next_agent": "",  # let supervisor decide first step
}

result = graph_app.invoke(initial_state)
print("Final risk:", result["risk_score"])
print("Chosen slot:", result["chosen_slot"])
print("Notification:", result["notification_text"])
print("Notification status:", result["notification_status"])
