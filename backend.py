from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

# -----------------------------
# Agent State Definition
# -----------------------------
class AgentState(TypedDict):
    messages: List[str]
    vehicle_id: str
    sensor_data: Dict
    vehicle_profile: Dict
    service_history: Dict
    risk_score: str
    risk_explanation: str
    service_slots: List[str]
    chosen_slot: str
    notification_text: str
    notification_status: str
    next_agent: str


# -----------------------------
# Agent 1: Risk Analysis
# -----------------------------
def risk_agent(state: AgentState):

    temp = state["sensor_data"].get("engine_temp", 0)
    oil = state["sensor_data"].get("oil_pressure", 0)

    if temp > 110:
        state["risk_score"] = "HIGH"
        state["risk_explanation"] = "Engine temperature extremely high"
    elif temp > 95:
        state["risk_score"] = "MEDIUM"
        state["risk_explanation"] = "Engine temperature above normal"
    else:
        state["risk_score"] = "LOW"
        state["risk_explanation"] = "Vehicle operating normally"

    return state


# -----------------------------
# Agent 2: Service Scheduler
# -----------------------------
def service_agent(state: AgentState):

    slots = [
        "Tomorrow 10 AM",
        "Tomorrow 3 PM",
        "Day after Tomorrow 11 AM"
    ]

    state["service_slots"] = slots
    state["chosen_slot"] = slots[0]

    return state


# -----------------------------
# Agent 3: Notification Agent
# -----------------------------
def notification_agent(state: AgentState):

    state["notification_text"] = (
        f"Vehicle {state['vehicle_id']} requires maintenance. "
        f"Recommended slot: {state['chosen_slot']}"
    )

    state["notification_status"] = "Sent"

    return state


# -----------------------------
# Build LangGraph Workflow
# -----------------------------
builder = StateGraph(AgentState)

builder.add_node("risk_agent", risk_agent)
builder.add_node("service_agent", service_agent)
builder.add_node("notification_agent", notification_agent)

builder.set_entry_point("risk_agent")

builder.add_edge("risk_agent", "service_agent")
builder.add_edge("service_agent", "notification_agent")
builder.add_edge("notification_agent", END)

graph_app = builder.compile()