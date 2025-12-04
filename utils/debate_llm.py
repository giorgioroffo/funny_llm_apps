"""
LLM Client module for AI Alterego Debate Simulator.

Handles OpenAI API calls for agent conversations.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from .debate_config import GPT_MODEL
from .debate_prompts import stamp_sim
from .debate_state import conversation_state

load_dotenv(override=True)
openai_client = OpenAI()


def call_agent1():
    """Agent 1 responds to Agent 2's last message (adversarial)."""
    messages = [{"role": "system", "content": conversation_state["agent1_system"]}]
    
    # Build conversation history
    for i in range(len(conversation_state["agent2_messages"])):
        messages.append({"role": "user", "content": conversation_state["agent2_messages"][i]})
        if i < len(conversation_state["agent1_messages"]):
            messages.append({"role": "assistant", "content": conversation_state["agent1_messages"][i]})
    
    # Add latest message if needed
    if len(conversation_state["agent2_messages"]) > len(conversation_state["agent1_messages"]):
        messages.append({"role": "user", "content": conversation_state["agent2_messages"][-1]})
    
    response = openai_client.chat.completions.create(model=GPT_MODEL, messages=messages)
    return stamp_sim(response.choices[0].message.content)


def call_agent2():
    """Agent 2 responds to Agent 1's last message (polite)."""
    messages = [{"role": "system", "content": conversation_state["agent2_system"]}]
    
    # Build conversation history
    for i in range(len(conversation_state["agent2_messages"])):
        if i == 0:
            messages.append({"role": "assistant", "content": conversation_state["agent2_messages"][i]})
        else:
            if i - 1 < len(conversation_state["agent1_messages"]):
                messages.append({"role": "user", "content": conversation_state["agent1_messages"][i - 1]})
            messages.append({"role": "assistant", "content": conversation_state["agent2_messages"][i]})
    
    # Add latest message if needed
    if len(conversation_state["agent1_messages"]) > 0 and len(conversation_state["agent1_messages"]) >= len(conversation_state["agent2_messages"]):
        messages.append({"role": "user", "content": conversation_state["agent1_messages"][-1]})
    
    response = openai_client.chat.completions.create(model=GPT_MODEL, messages=messages)
    return stamp_sim(response.choices[0].message.content)

