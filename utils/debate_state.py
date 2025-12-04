"""
State management module for AI Alterego Debate Simulator.

Manages global conversation state.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""


def create_initial_state():
    """Create and return a fresh state dictionary."""
    return {
        "agent1_messages": [],
        "agent2_messages": [],
        "agent1_system": "",
        "agent2_system": "",
        "agent1_name": "",
        "agent2_name": "",
        "is_running": False
    }


# Global state instance
conversation_state = create_initial_state()


def reset_state():
    """Reset the global state to initial values."""
    global conversation_state
    conversation_state = create_initial_state()


def initialize_state(agent1_system, agent2_system, agent1_name, agent2_name):
    """Initialize state with agent systems and names."""
    global conversation_state
    conversation_state["agent1_system"] = agent1_system
    conversation_state["agent2_system"] = agent2_system
    conversation_state["agent1_name"] = agent1_name
    conversation_state["agent2_name"] = agent2_name
    conversation_state["agent1_messages"] = []
    conversation_state["agent2_messages"] = []
    conversation_state["is_running"] = True

