"""
State management module for AI Consensus Engine.

Manages global simulation state and provides state initialization/reset functions.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""


def create_initial_state():
    """Create and return a fresh state dictionary."""
    return {
        "problem_statement": "",
        "ground_truth_solution": "",
        "iteration_count": 0,
        "chief_history": [],
        "logic_expert_history": [],
        "critic_expert_history": [],
        "chief_system": "",
        "logic_system": "",
        "critic_system": "",
        "is_started": False,
        "total_tokens_in": 0,
        "total_tokens_out": 0,
        "total_cost": 0.0,
        "token_details": [],
        "final_chief_raw": "",
        "final_chief_json": None
    }


# Global state instance
consensus_state = create_initial_state()


def reset_state():
    """Reset the global state to initial values."""
    global consensus_state
    consensus_state = create_initial_state()


def initialize_state(problem, ground_truth, chief_system, logic_system, critic_system):
    """Initialize state with problem and system prompts."""
    global consensus_state
    consensus_state["problem_statement"] = problem
    consensus_state["ground_truth_solution"] = ground_truth if ground_truth else ""
    consensus_state["iteration_count"] = 0
    consensus_state["chief_history"] = []
    consensus_state["logic_expert_history"] = []
    consensus_state["critic_expert_history"] = []
    consensus_state["chief_system"] = chief_system
    consensus_state["logic_system"] = logic_system
    consensus_state["critic_system"] = critic_system
    consensus_state["is_started"] = True
    consensus_state["total_tokens_in"] = 0
    consensus_state["total_tokens_out"] = 0
    consensus_state["total_cost"] = 0.0
    consensus_state["token_details"] = []
    consensus_state["final_chief_raw"] = ""
    consensus_state["final_chief_json"] = None

