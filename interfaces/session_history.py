import streamlit as st
from datetime import datetime

def initialize_history():
    """Initialize session history if it doesn't exist"""
    if 'session_history' not in st.session_state:
        st.session_state.session_history = []
    if 'show_history' not in st.session_state:
        st.session_state.show_history = False

def add_to_history(query, response, agent_type=None):
    """
    Add a query-response pair to session history
    
    Args:
        query (str): User's query
        response (str): Agent's response
        agent_type (str): Type of agent that provided the response
    """
    initialize_history()
    
    history_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "response": response,
        "agent_type": agent_type,
        "id": len(st.session_state.session_history) + 1
    }
    
    st.session_state.session_history.append(history_entry)

def get_history():
    """Get all session history"""
    initialize_history()
    return st.session_state.session_history

def clear_history():
    """Clear all session history"""
    st.session_state.session_history = []

def get_history_count():
    """Get total number of history entries"""
    initialize_history()
    return len(st.session_state.session_history)

def export_history_as_text():
    """Export history as formatted text for copying"""
    history = get_history()
    if not history:
        return "No conversation history available."
    
    exported_text = "AutoMarketer.AI - Conversation History\n"
    exported_text += "=" * 50 + "\n\n"
    
    for entry in history:
        exported_text += f"📅 {entry['timestamp']}\n"
        if entry['agent_type']:
            exported_text += f"🤖 Agent: {entry['agent_type']}\n"
        exported_text += f"❓ Query: {entry['query']}\n"
        exported_text += f"💬 Response: {entry['response']}\n"
        exported_text += "-" * 30 + "\n\n"
    
    return exported_text

def get_recent_history(limit=5):
    """Get recent history entries"""
    history = get_history()
    return history[-limit:] if history else [] 