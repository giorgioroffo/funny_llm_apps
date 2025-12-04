"""
Formatting module for AI Consensus Engine.

Contains functions for formatting conversation history, HTML tables, and display content.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

from .state import consensus_state


def format_conversation_history(agent_name, history):
    """Format conversation history with clear markers."""
    if not history:
        return ""
    
    formatted = []
    for i, msg in enumerate(history, 1):
        formatted.append(f"### {agent_name} - Step {i}\n\n{msg}")
    
    return "\n\n---\n\n".join(formatted)


def html_escape(text):
    """Escape HTML special characters."""
    if not text:
        return ""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#x27;"))


def format_token_usage():
    """Format token usage information for display."""
    token_info = f"📊 **Token Usage:**\n"
    token_info += f"- Input tokens: {consensus_state['total_tokens_in']:,}\n"
    token_info += f"- Output tokens: {consensus_state['total_tokens_out']:,}\n"
    token_info += f"- Total tokens: {consensus_state['total_tokens_in'] + consensus_state['total_tokens_out']:,}\n"
    token_info += f"- **Estimated cost: ${consensus_state['total_cost']:.4f}**\n\n"
    return token_info


def summarize_expert_contribution(history, expert_name):
    """Summarize an expert's contribution from their conversation history."""
    if not history:
        return "No contributions recorded."
    
    # Take the last 2 messages and create a brief summary
    recent_messages = history[-2:] if len(history) >= 2 else history
    summary = " ".join(recent_messages)
    
    # Truncate if too long (max 200 chars)
    if len(summary) > 200:
        summary = summary[:197] + "..."
    
    return summary


def normalize_agent_label(label):
    """Map ranking labels to canonical agent names."""
    if not label:
        return None
    normalized = label.lower().strip()
    if "agent 1" in normalized or "logic" in normalized or "strategist" in normalized:
        return "📐 Logic Strategist"
    if "agent 2" in normalized or "critic" in normalized:
        return "⚔️ Pragmatic Critic"
    return label


def create_ranking_table(logic_score, critic_score, logic_solution, critic_solution,
                        ranking=None, best_solution=None, evaluation_notes=None, agent_reasonings=None):
    """Create a ranking table with scores and markdown snapshots."""
    agent_reasonings = agent_reasonings or {}
    
    # Prepare canonical agent dictionary
    agent_data = {
        "📐 Logic Strategist": {
            "score": logic_score,
            "solution": logic_solution or "_No solution snapshot provided._",
            "reasoning": agent_reasonings.get("📐 Logic Strategist")
        },
        "⚔️ Pragmatic Critic": {
            "score": critic_score,
            "solution": critic_solution or "_No solution snapshot provided._",
            "reasoning": agent_reasonings.get("⚔️ Pragmatic Critic")
        }
    }
    
    # Build ordered list
    experts = [{"name": name, **payload} for name, payload in agent_data.items()]
    
    if ranking:
        ordered = []
        used = set()
        for label in ranking:
            canonical = normalize_agent_label(label)
            for expert in experts:
                if expert["name"] == canonical and canonical not in used:
                    ordered.append(expert)
                    used.add(canonical)
                    break
        for expert in experts:
            if expert["name"] not in used:
                ordered.append(expert)
        experts = ordered
    else:
        experts.sort(key=lambda x: (x["score"] is not None, x["score"]), reverse=True)
    
    table_html = """<style>
.scoreboard-table table {width: 100%; border-collapse: collapse; font-family: "IBM Plex Sans", Arial;}
.scoreboard-table th, .scoreboard-table td {border: 1px solid #1f2937; padding: 12px;}
</style>
<div class='scoreboard-table' style='margin: 20px 0; background-color: #000000; color: #f8fafc; border-radius: 8px; border: 1px solid #1f2937; padding: 12px;'>
<h2 style='color: #facc15; margin-bottom: 12px;'>🏆 Professor's Final Evaluation - Student Rankings</h2>
<table>
<thead>
    <tr style='background-color: #050505; color: #facc15;'>
        <th>Rank</th>
        <th>Agent</th>
        <th>Score</th>
        <th>Chief Thought</th>
    </tr>
</thead>
<tbody>
"""
    
    for idx, expert in enumerate(experts, 1):
        rank_labels = {1: "🥇 1st", 2: "🥈 2nd"}
        rank_text = rank_labels.get(idx, f"{idx}th")
        row_style = "background-color: #111111; font-weight: bold;" if idx == 1 else ""
        score = expert["score"]
        score_text = f"{score}%" if isinstance(score, (int, float)) else "N/A"
        if isinstance(score, (int, float)):
            score_color = "#10b981" if score >= 70 else "#ef4444" if score < 50 else "#f59e0b"
        else:
            score_color = "#f1f5f9"
        reasoning = expert.get("reasoning") or "No chief note provided."
        
        table_html += f"""<tr style='{row_style}'>
    <td style='text-align:center; font-weight:600;'>{rank_text}</td>
    <td>{expert['name']}</td>
    <td style='text-align:center; color:{score_color}; font-weight:600;'>{score_text}</td>
    <td>{html_escape(reasoning)}</td>
</tr>
"""
    
    table_html += "</tbody></table></div>"
    
    # Append markdown-based snapshots
    snapshot_blocks = []
    for name, payload in agent_data.items():
        snapshot_blocks.append(f"#### {name} — Solution Snapshot\n\n{payload['solution']}")
    
    table_html += "\n\n" + "\n\n".join(snapshot_blocks)
    
    return table_html


def format_final_solution_display(best_solution_summary, agent_reasonings, evaluation_notes):
    """Format the final solution display with HTML styling."""
    summary_blocks = []
    
    if best_solution_summary:
        summary_blocks.append(
            f"<div style='margin-bottom: 12px; color: #f8fafc;'>"
            f"<strong>🥇 Best Solution Summary:</strong><br>{html_escape(best_solution_summary)}</div>"
        )
    
    if agent_reasonings:
        perf_items = "".join(
            f"<li><strong>{label}:</strong> {html_escape(note)}</li>"
            for label, note in agent_reasonings.items() if note
        )
        if perf_items:
            summary_blocks.append(
                f"<div style='background-color: #050505; color: #f8fafc; padding: 15px; border-radius: 6px; border-left: 4px solid #6366f1; margin-bottom: 12px;'>"
                f"<strong>📋 Agent Performance Highlights:</strong><ul style='margin: 8px 0 0 18px;'>{perf_items}</ul></div>"
            )
    
    if evaluation_notes:
        summary_blocks.append(
            f"<div style='background-color: #050505; color: #f8fafc; padding: 15px; border-radius: 6px; border-left: 4px solid #f97316;'>"
            f"<strong>📝 Evaluation Notes:</strong> {html_escape(evaluation_notes)}</div>"
        )
    
    if not summary_blocks:
        summary_blocks.append(
            "<div style='background-color: #050505; color: #f8fafc; padding: 15px; border-radius: 6px;'>"
            "Chief provided structured scores but no narrative summary.</div>"
        )
    
    final_solution = (
        "<div style='background-color: #000000; color: #f8fafc; padding: 18px; border-radius: 10px; "
        "border: 1px solid #262626; box-shadow: 0 10px 25px rgba(0,0,0,0.6);'>"
        + "".join(summary_blocks)
        + "</div>"
    )
    
    return final_solution

