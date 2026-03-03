import os
import json
from typing import TypedDict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

from langfuse import Langfuse
from langfuse.callback import CallbackHandler

load_dotenv()

langfuse = Langfuse()
langfuse_handler = CallbackHandler()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

class FraudState(TypedDict):
    transaction: dict
    features: dict
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    risk_reasoning: str
    investigation_notes: str
    final_action: str
    trace_id: str

def extract_features(state: FraudState) -> dict:
    """
    Parse raw transaction into structured features.
    In production this would hit a feature store.
    """
    txn = state["transaction"]
    
    features = {
        "amount_usd": txn.get("amount"),
        "is_new_account": txn.get("account_age_days", 999) < 30,
        "is_foreign_ip": txn.get("ip_country") != txn.get("billing_country"),
        "is_high_velocity": txn.get("txns_last_hour", 0) > 5,
        "device_fingerprint_match": txn.get("device_seen_before", True),
    }
    
    print(f"[extract_features] Extracted: {features}")
    return {"features": features}


def classify_risk(state: FraudState) -> dict:
    """
    LLM-based risk classification. In production this would
    also call a trained model; the LLM provides reasoning.
    This call is automatically traced by Langfuse via the callback.
    """
    features = state["features"]
    txn = state["transaction"]
    
    risk_flags = [k for k, v in features.items() if v is True]
    
    messages = [
        SystemMessage(content="""You are a fraud risk classifier for a travel booking platform.
Analyze transaction features and classify risk as HIGH, MEDIUM, or LOW.
Respond in JSON: {"risk_level": "HIGH|MEDIUM|LOW", "reasoning": "brief explanation"}"""),
        HumanMessage(content=f"""
Transaction amount: ${txn.get('amount')}
Destination: {txn.get('destination')}
Risk flags present: {risk_flags}
Account age (days): {txn.get('account_age_days')}
Previous bookings: {txn.get('previous_bookings', 0)}

Classify this transaction's fraud risk.""")
    ]
    
    response = llm.invoke(messages)
    
    try:
        result = json.loads(response.content)
        risk_level = result["risk_level"]
        reasoning = result["reasoning"]
    except (json.JSONDecodeError, KeyError):
        # LLMs sometimes don't follow JSON instructions perfectly
        risk_level = "MEDIUM"
        reasoning = response.content
    
    print(f"[classify_risk] Risk: {risk_level} — {reasoning}")
    return {"risk_level": risk_level, "risk_reasoning": reasoning}


def investigate(state: FraudState) -> dict:
    """
    Deep investigation node — only reached for HIGH risk.
    In production this would query entity graphs, device history, etc.
    """
    features = state["features"]
    reasoning = state["risk_reasoning"]
    
    messages = [
        SystemMessage(content="""You are a fraud investigator. 
Given risk signals, produce a concise investigation summary and specific recommended checks.
Format: {"investigation_notes": "...", "recommended_checks": ["check1", "check2"]}"""),
        HumanMessage(content=f"""
Initial risk assessment: {reasoning}
Feature signals: {json.dumps(features, indent=2)}

What additional investigation steps should be taken?""")
    ]
    
    response = llm.invoke(messages)
    
    try:
        result = json.loads(response.content)
        notes = result.get("investigation_notes", response.content)
    except json.JSONDecodeError:
        notes = response.content
    
    print(f"[investigate] Notes: {notes}")
    return {"investigation_notes": notes}


def recommend_action(state: FraudState) -> dict:
    """Terminal node after investigation — produce final decision."""
    action = "BLOCK_AND_REVIEW" if state["risk_level"] == "HIGH" else "FLAG_FOR_REVIEW"
    print(f"[recommend_action] Final action: {action}")
    return {"final_action": action}


def approve(state: FraudState) -> dict:
    """Terminal node for low-risk transactions."""
    print("[approve] Transaction approved.")
    return {"final_action": "APPROVE"}


# ─────────────────────────────────────────────
# Routing logic — this is the "edge" condition
# Like a Temporal workflow's if/else branching
# ─────────────────────────────────────────────

def route_on_risk(state: FraudState) -> str:
    """Returns the name of the next node based on risk level."""
    risk = state.get("risk_level", "LOW")
    if risk == "HIGH":
        return "investigate"
    else:
        return "approve"


# ─────────────────────────────────────────────
# Graph assembly — wire nodes and edges together
# ─────────────────────────────────────────────

def build_fraud_graph() -> StateGraph:
    graph = StateGraph(FraudState)
    
    # Register nodes
    graph.add_node("extract_features", extract_features)
    graph.add_node("classify_risk", classify_risk)
    graph.add_node("investigate", investigate)
    graph.add_node("recommend_action", recommend_action)
    graph.add_node("approve", approve)
    
    # Entry point
    graph.set_entry_point("extract_features")
    
    # Edges: extract → classify always
    graph.add_edge("extract_features", "classify_risk")
    
    # Conditional edge: classify → investigate OR approve
    graph.add_conditional_edges(
        "classify_risk",          # source node
        route_on_risk,            # routing function
        {
            "investigate": "investigate",
            "approve": "approve",
        }
    )
    
    # investigate always leads to recommend_action
    graph.add_edge("investigate", "recommend_action")
    
    # Terminal nodes
    graph.add_edge("recommend_action", END)
    graph.add_edge("approve", END)
    
    return graph.compile()


# ─────────────────────────────────────────────
# Run it
# ─────────────────────────────────────────────

def run_fraud_check(transaction: dict) -> FraudState:
    app = build_fraud_graph()
    
    # Create a Langfuse trace for the entire run — 
    # this is your "parent span" equivalent
    trace = langfuse.trace(
        name="fraud-check",
        input=transaction,
        metadata={"transaction_id": transaction.get("id")}
    )
    
    initial_state: FraudState = {
        "transaction": transaction,
        "features": {},
        "risk_level": "LOW",
        "risk_reasoning": "",
        "investigation_notes": "",
        "final_action": "",
        "trace_id": trace.id,
    }
    
    # config passes the Langfuse handler into every LLM call in the graph
    config = {"callbacks": [langfuse_handler]}
    final_state = app.invoke(initial_state, config=config)
    
    # Update the Langfuse trace with the outcome
    trace.update(output={"action": final_state["final_action"], "risk": final_state["risk_level"]})
    langfuse.flush()  # ensure spans are sent before process exits
    
    return final_state


# ─────────────────────────────────────────────
# Test transactions
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Suspicious transaction
    suspicious_txn = {
        "id": "TXN-001",
        "amount": 4200,
        "destination": "Cancun, Mexico",
        "account_age_days": 2,
        "ip_country": "Russia",
        "billing_country": "USA",
        "txns_last_hour": 8,
        "device_seen_before": False,
        "previous_bookings": 0,
    }
    
    # Legitimate transaction
    legit_txn = {
        "id": "TXN-002",
        "amount": 350,
        "destination": "Seattle, WA",
        "account_age_days": 730,
        "ip_country": "USA",
        "billing_country": "USA",
        "txns_last_hour": 1,
        "device_seen_before": True,
        "previous_bookings": 12,
    }
    
    print("=" * 50)
    print("SUSPICIOUS TRANSACTION")
    print("=" * 50)
    result1 = run_fraud_check(suspicious_txn)
    print(f"Final: {result1['final_action']}\n")
    
    print("=" * 50)
    print("LEGITIMATE TRANSACTION")
    print("=" * 50)
    result2 = run_fraud_check(legit_txn)
    print(f"Final: {result2['final_action']}")
    
    print("\nCheck your Langfuse dashboard at https://cloud.langfuse.com")