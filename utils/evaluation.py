"""
Evaluation module for AI Consensus Engine.

Handles final evaluation parsing and result formatting.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

from .state import consensus_state
from .json_parser import parse_evaluation_json, coerce_score_to_int
from .formatters import (
    format_token_usage,
    format_conversation_history,
    summarize_expert_contribution,
    create_ranking_table,
    format_final_solution_display
)


def validate_simulation_complete():
    """Validate that simulation has been completed."""
    if not consensus_state["is_started"]:
        return False, "❌ Please start the simulation first!"
    
    if consensus_state["iteration_count"] < 3:
        return False, "⚠️ Complete all 3 iterations first!"
    
    return True, None


def extract_evaluation_data(json_data):
    """Extract evaluation data from parsed JSON."""
    logic_score = coerce_score_to_int(json_data.get("score_agent_1_percent"))
    critic_score = coerce_score_to_int(json_data.get("score_agent_2_percent"))
    ranking = json_data.get("ranking", [])
    best_solution_summary = json_data.get("best_solution_summary", "")
    evaluation_notes = json_data.get("evaluation_notes", "")
    agent_reasonings = {
        "📐 Logic Strategist": json_data.get("agent_1_reasoning", ""),
        "⚔️ Pragmatic Critic": json_data.get("agent_2_reasoning", "")
    }
    
    return logic_score, critic_score, ranking, best_solution_summary, evaluation_notes, agent_reasonings


def final_evaluation():
    """Extract scores from Chief's final evaluation JSON and display results."""
    try:
        # Validate simulation is complete
        is_valid, error_msg = validate_simulation_complete()
        if not is_valid:
            return error_msg, "", "", "", "", ""
        
        # Get raw JSON response
        raw_json = consensus_state.get("final_chief_raw", "")
        if not raw_json:
            return "❌ No Chief evaluation found!", "", "", "", "", ""
        
        # Parse JSON
        json_data = parse_evaluation_json(raw_json)
        if not json_data:
            error_preview = raw_json[:1000].replace("\n", "\\n").replace("`", "'")
            error_msg = f"❌ Could not parse Chief's JSON response.\n\nFull response (first 1000 chars):\n```\n{error_preview}\n```\n\nPlease check if the JSON is complete and valid."
            return error_msg, "", "", "", "", ""
        
        # Extract data
        logic_score, critic_score, ranking, best_solution_summary, evaluation_notes, agent_reasonings = \
            extract_evaluation_data(json_data)
        
        # Get expert solutions
        logic_solution = summarize_expert_contribution(
            consensus_state["logic_expert_history"], "Logic Strategist"
        )
        critic_solution = summarize_expert_contribution(
            consensus_state["critic_expert_history"], "Pragmatic Critic"
        )
        
        # Format displays
        final_solution = format_final_solution_display(
            best_solution_summary, agent_reasonings, evaluation_notes
        )
        
        scores_table = create_ranking_table(
            logic_score,
            critic_score,
            logic_solution,
            critic_solution,
            ranking=ranking,
            best_solution=best_solution_summary,
            evaluation_notes=evaluation_notes,
            agent_reasonings=agent_reasonings
        )
        
        token_info = format_token_usage() + f"✅ Final evaluation completed!"
        
        # Format conversation displays
        chief_display = format_conversation_history("Chief", consensus_state["chief_history"])
        logic_display = format_conversation_history("Logic Strategist", consensus_state["logic_expert_history"])
        critic_display = format_conversation_history("Pragmatic Critic", consensus_state["critic_expert_history"])
        
        return token_info, final_solution, scores_table, chief_display, logic_display, critic_display
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        error_msg = f"❌ **Error in final evaluation:**\n\n{str(e)}\n\n**Details:**\n```\n{error_details}\n```"
        return error_msg, "", "", "", "", ""

