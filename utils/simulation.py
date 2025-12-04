"""
Simulation module for AI Consensus Engine.

Handles the multi-iteration simulation workflow and agent interactions.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

from .config import CHIEF_MODEL, LOGIC_MODEL, CRITIC_MODEL, NUM_ITERATIONS
from .state import consensus_state, initialize_state
from .llm_client import query_model
from .prompts import build_chief_prompt, build_logic_prompt, build_critic_prompt, build_final_evaluation_context
from .formatters import format_conversation_history, format_token_usage
from .json_parser import parse_evaluation_json


def validate_input(problem):
    """Validate that problem input is not empty."""
    return problem and problem.strip()


def build_conversation_context():
    """Build context string with full conversation history."""
    context = f"Problem: {consensus_state['problem_statement']}\n\n"
    context += "CONVERSATION HISTORY:\n\n"
    
    max_len = max(
        len(consensus_state["chief_history"]),
        len(consensus_state["logic_expert_history"]),
        len(consensus_state["critic_expert_history"])
    )
    
    for i in range(max_len):
        if i < len(consensus_state["chief_history"]):
            context += f"👑 Chief: {consensus_state['chief_history'][i]}\n\n"
        if i < len(consensus_state["logic_expert_history"]):
            context += f"📐 Logic Strategist: {consensus_state['logic_expert_history'][i]}\n\n"
        if i < len(consensus_state["critic_expert_history"]):
            context += f"⚔️ Pragmatic Critic: {consensus_state['critic_expert_history'][i]}\n\n"
    
    if consensus_state["chief_history"]:
        context += f"\n👑 Chief's latest question/directive: {consensus_state['chief_history'][-1]}\n\n"
    
    return context


def get_chief_initial_message(problem):
    """Get Chief's initial analysis and question."""
    chief_messages = [
        {"role": "system", "content": consensus_state["chief_system"]},
        {"role": "user", "content": f"Problem: {problem}\n\nAnalyze this problem and ask your first targeted question to guide the Logic Strategist and Pragmatic Critic toward a solution."}
    ]
    
    chief_response, _, _, _ = query_model(chief_messages, CHIEF_MODEL)
    consensus_state["chief_history"].append(chief_response)
    return chief_response


def get_logic_response(context):
    """Get Logic Strategist's response to Chief's question."""
    logic_messages = [
        {"role": "system", "content": consensus_state["logic_system"]},
        {"role": "user", "content": context + "Respond to the Chief's question with your strategic analysis and approach."}
    ]
    
    # Add recent history for context
    if consensus_state["logic_expert_history"]:
        for msg in consensus_state["logic_expert_history"][-2:]:
            logic_messages.append({"role": "assistant", "content": msg})
    
    logic_response, _, _, _ = query_model(logic_messages, LOGIC_MODEL)
    consensus_state["logic_expert_history"].append(logic_response)
    return logic_response


def get_critic_response(context, logic_response):
    """Get Pragmatic Critic's response analyzing Logic's proposal."""
    critic_context = context + f"📐 Logic Strategist just said: {logic_response}\n\n"
    critic_context += "Respond to the Chief's question AND analyze Logic Strategist's proposal. Find flaws, demand specifics, check feasibility."
    
    critic_messages = [
        {"role": "system", "content": consensus_state["critic_system"]},
        {"role": "user", "content": critic_context}
    ]
    
    # Add recent history for context
    if consensus_state["critic_expert_history"]:
        for msg in consensus_state["critic_expert_history"][-2:]:
            critic_messages.append({"role": "assistant", "content": msg})
    
    critic_response, _, _, _ = query_model(critic_messages, CRITIC_MODEL)
    consensus_state["critic_expert_history"].append(critic_response)
    return critic_response


def get_chief_response(iteration, logic_response, critic_response):
    """Get Chief's response (question or final evaluation)."""
    if iteration == NUM_ITERATIONS:
        chief_context = build_final_evaluation_context(
            consensus_state["problem_statement"],
            consensus_state["ground_truth_solution"],
            consensus_state["logic_expert_history"],
            consensus_state["critic_expert_history"],
            logic_response,
            critic_response
        )
    else:
        chief_context = f"## Problem Statement\n{consensus_state['problem_statement']}\n\n"
        if consensus_state["ground_truth_solution"]:
            chief_context += f"## Expected / Reference Solution\n{consensus_state['ground_truth_solution']}\n\n"
        else:
            chief_context += "## Expected / Reference Solution\n(Not provided)\n\n"
        chief_context += f"📐 Logic Strategist said: {logic_response}\n\n"
        chief_context += f"⚔️ Pragmatic Critic said: {critic_response}\n\n"
        chief_context += f"Analyze their responses. You can ask clarifying questions or guide them further. Ask your next targeted question to refine the solution. (Iteration {iteration}/{NUM_ITERATIONS})"
    
    chief_messages = [{"role": "system", "content": consensus_state["chief_system"]}]
    for msg in consensus_state["chief_history"]:
        chief_messages.append({"role": "assistant", "content": msg})
    chief_messages.append({"role": "user", "content": chief_context})
    
    chief_response, _, _, _ = query_model(chief_messages, CHIEF_MODEL)
    
    # Handle final evaluation JSON
    display_message = chief_response
    if iteration == NUM_ITERATIONS:
        consensus_state["final_chief_raw"] = chief_response
        parsed_json = parse_evaluation_json(chief_response)
        consensus_state["final_chief_json"] = parsed_json
        display_message = "🧾 Chief submitted the final evaluation JSON. See Final Results for the breakdown."
    
    consensus_state["chief_history"].append(display_message)
    return display_message


def run_iteration(iteration):
    """Run a single iteration of the simulation."""
    consensus_state["iteration_count"] = iteration
    
    context = build_conversation_context()
    
    # Step 1: Logic responds
    logic_response = get_logic_response(context)
    logic_display = format_conversation_history("Logic Strategist", consensus_state["logic_expert_history"])
    
    # Step 2: Critic responds
    critic_response = get_critic_response(context, logic_response)
    critic_display = format_conversation_history("Pragmatic Critic", consensus_state["critic_expert_history"])
    
    # Step 3: Chief responds
    chief_response = get_chief_response(iteration, logic_response, critic_response)
    chief_display = format_conversation_history("Chief", consensus_state["chief_history"])
    
    return chief_display, logic_display, critic_display


def initialize_simulation(problem, ground_truth):
    """Initialize the consensus engine and automatically run all iterations."""
    try:
        # Validate input
        if not validate_input(problem):
            yield "❌ Error: Problem description cannot be empty!", "", "", ""
            return
        
        # Initialize state
        chief_system = build_chief_prompt(problem)
        logic_system = build_logic_prompt(problem)
        critic_system = build_critic_prompt(problem)
        initialize_state(problem, ground_truth, chief_system, logic_system, critic_system)
        
        yield "⏳ Starting simulation... Chief Architect is analyzing the problem.", "", "", ""
        
        # Chief starts with initial analysis
        get_chief_initial_message(problem)
        chief_display = format_conversation_history("Chief", consensus_state["chief_history"])
        yield f"👑 Chief Architect has started the discussion (Iteration 1/{NUM_ITERATIONS})", chief_display, "", ""
        
        # Run all iterations
        for iteration in range(1, NUM_ITERATIONS + 1):
            yield f"🔄 Iteration {iteration}: Waiting for Logic Strategist...", \
                  chief_display, \
                  format_conversation_history("Logic Strategist", consensus_state["logic_expert_history"]), \
                  format_conversation_history("Pragmatic Critic", consensus_state["critic_expert_history"])
            
            chief_display, logic_display, critic_display = run_iteration(iteration)
            
            if iteration < NUM_ITERATIONS:
                yield f"🔄 Iteration {iteration}: Chief Architect is analyzing responses...", \
                      chief_display, logic_display, critic_display
        
        # Final status
        token_info = format_token_usage() + f"✅ All {NUM_ITERATIONS} iterations completed automatically!"
        yield token_info, chief_display, logic_display, critic_display
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        error_msg = f"❌ **Error during simulation:**\n\n{str(e)}\n\n"
        error_msg += f"**Details:**\n```\n{error_details}\n```\n\n"
        error_msg += "Please check:\n"
        error_msg += "- OpenAI API key is set in .env file\n"
        error_msg += "- Internet connection is active\n"
        error_msg += "- API quota/limits are not exceeded"
        
        yield error_msg, "", "", ""

