"""
Conversation logic module for AI Alterego Debate Simulator.

Handles conversation flow and agent interactions.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

from .debate_state import conversation_state, initialize_state, reset_state
from .debate_prompts import build_profile_string, build_system_prompt
from .debate_llm import call_agent1, call_agent2


def save_profiles(topic, name1, gender1, characteristics1, attitudes1, hobbies1, personality1, interests1, background1,
                  name2, gender2, characteristics2, attitudes2, hobbies2, personality2, interests2, background2):
    """Save profiles and prepare for conversation."""
    # Build profiles
    profile1 = build_profile_string(gender1, characteristics1, attitudes1, hobbies1, personality1, interests1, background1)
    profile2 = build_profile_string(gender2, characteristics2, attitudes2, hobbies2, personality2, interests2, background2)
    
    # Build system prompts
    agent1_system = build_system_prompt(name1, gender1, profile1, topic, "adversarial")
    agent2_system = build_system_prompt(name2, gender2, profile2, topic, "polite")
    
    # Initialize state
    initialize_state(agent1_system, agent2_system, name1, name2)
    
    status = f"✅ Profiles saved!\n\nTopic: {topic}\n\nPress 'Start Conversation' to begin!"
    title = f"## 🎭 Debate simulation between two AI agents (AI-generated, not real quotes)"
    label1 = f"### 🔴 [AI SIMULATION] Alterego inspired by {name1}"
    label2 = f"### 🔵 [AI SIMULATION] Alterego inspired by {name2}"
    
    return status, title, label1, label2


def start_conversation():
    """Start the conversation between two agents."""
    if not conversation_state["agent1_system"] or not conversation_state["agent2_system"]:
        return "❌ Please save profiles first!", "", ""
    
    conversation_state["agent1_messages"] = []
    conversation_state["agent2_messages"] = []
    
    # Agent 2 starts the conversation
    agent2_response = call_agent2()
    conversation_state["agent2_messages"].append(agent2_response)
    
    # Agent 2 started, Agent 1 box is empty
    chat1 = ""
    chat2 = agent2_response
    
    name2 = conversation_state["agent2_name"]
    return f"🎬 {name2} started the conversation!", chat1, chat2


def next_exchange():
    """Generate next exchange in the conversation."""
    if not conversation_state["agent2_messages"]:
        return "❌ Please start the conversation first!", "", ""
    
    name1 = conversation_state["agent1_name"]
    name2 = conversation_state["agent2_name"]
    
    # Agent 1 responds to Agent 2's last message
    agent1_response = call_agent1()
    conversation_state["agent1_messages"].append(agent1_response)
    
    # Agent 2 responds to Agent 1's message
    agent2_response = call_agent2()
    conversation_state["agent2_messages"].append(agent2_response)
    
    # Show only the latest message from each agent
    chat1 = agent1_response
    chat2 = agent2_response
    
    exchange_num = len(conversation_state["agent1_messages"])
    return f"✅ Exchange {exchange_num}: {name1} and {name2} have responded!", chat1, chat2


def reset_conversation():
    """Reset the conversation."""
    reset_state()
    return "🔄 Conversation reset!", "", ""

