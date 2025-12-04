"""
UI module for AI Consensus Engine.

Contains Gradio interface definition and event handlers.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

import gradio as gr
from .simulation import initialize_simulation
from .evaluation import final_evaluation
from .state import reset_state


def create_ui():
    """Create the Gradio interface."""
    with gr.Blocks(title="AI Consensus Engine") as demo:
        
        # Header
        gr.Markdown("""
        # 🧠 AI Reasoning Engine 🧠
        #### *Dr Giorgio Roffo*
        
        ### ⚡ Advanced Multi-Model Problem Solving Simulator ⚡
        
        **A hierarchical collaboration system** with 1 👑 Chief Architect orchestrating 2 Expert Agents:
        - 📐 **Logic Strategist** (strategic thinking & algorithms)
        - ⚔️ **Pragmatic Critic** (skeptical validation & edge cases)
        
        🚀 **3 automatic iterations** → Chief asks questions → Experts respond → Chief evaluates & scores!
        """)
        
        # Disclaimer
        gr.Markdown("""
        <div style='background-color: #ffe4cc; color: #7c2d12; padding: 10px; border-radius: 5px; border-left: 4px solid #ea580c;'>
        <strong style='color: #7c2d12;'>⚠️ DISCLAIMER:</strong> This content is AI-generated for demo/research purposes. 
        All outputs are simulated AI responses, not real statements from actual systems.
        </div>
        """)
        
        # Input Section
        with gr.Row():
            with gr.Column():
                problem_input = gr.Textbox(
                    label="📋 Problem Description",
                    placeholder="Describe the problem you want the AI Consensus Engine to solve...",
                    lines=5
                )
                ground_truth_input = gr.Textbox(
                    label="🎯 Expected Solution / Ground Truth (Optional: For Scoring)",
                    placeholder="Optional: Provide the expected solution for evaluation scoring...",
                    lines=3
                )
                with gr.Row():
                    start_btn = gr.Button("🚀 Start Simulation", variant="primary")
                    reset_btn = gr.Button("🔄 Reset", variant="secondary")
        
        # Status & Token Info
        gr.Markdown("### 📊 Status & Token Usage")
        status_output = gr.Markdown(value="")
        
        # Visualization Area - The "Boardroom"
        gr.Markdown("---")
        gr.Markdown("""
        ## 🎭 The Boardroom - Multi-Agent Collaboration
        
        <div style='text-align: center; color: #666; margin-bottom: 20px;'>
        👑 Chief orchestrates the conversation • 📐 Logic provides strategy • ⚔️ Critic challenges & validates
        </div>
        """)
        
        with gr.Row():
            # Column 1: Logic Strategist (Left)
            with gr.Column():
                logic_label = gr.Markdown("""
                ### 📐 Logic Strategist
                <div style='color: #2563eb; font-size: 0.9em;'>Strategic Thinking & Algorithms</div>
                """)
                logic_output = gr.Markdown(label="", value="", elem_classes=["agent-output"])
            
            # Column 2: Chief Architect (Center)
            with gr.Column():
                chief_label = gr.Markdown("""
                ### 👑 Chief Architect
                <div style='color: #dc2626; font-size: 0.9em;'>Orchestrator & Evaluator</div>
                """)
                chief_output = gr.Markdown(label="", value="", elem_classes=["agent-output"])
            
            # Column 3: Pragmatic Critic (Right)
            with gr.Column():
                critic_label = gr.Markdown("""
                ### ⚔️ Pragmatic Critic
                <div style='color: #ea580c; font-size: 0.9em;'>Skeptical Validation & Edge Cases</div>
                """)
                critic_output = gr.Markdown(label="", value="", elem_classes=["agent-output"])
        
        # Controls
        gr.Markdown("---")
        with gr.Row():
            final_eval_btn = gr.Button("🏁 Show Final Evaluation & Scores", variant="primary", size="lg")
            gr.Markdown("""
            <div style='background-color: #d1fae5; color: #065f46; padding: 10px; border-radius: 5px;'>
            <strong style='color: #065f46;'>💡 Note:</strong> All <strong style='color: #065f46;'>3 iterations</strong> run automatically when you start the simulation.
            The Chief will ask questions, experts respond, and at the end the Chief evaluates and assigns scores!
            </div>
            """)
        
        # Final Solution & Scores
        gr.Markdown("---")
        gr.Markdown("## 🏆 Final Results")
        final_solution_output = gr.Markdown(label="### ✅ Final Synthesized Solution", value="")
        scores_output = gr.Markdown(label="### 📊 Chief's Evaluation & Scores", value="")
        
        # Event handlers
        start_btn.click(
            fn=initialize_simulation,
            inputs=[problem_input, ground_truth_input],
            outputs=[status_output, chief_output, logic_output, critic_output]
        )
        
        final_eval_btn.click(
            fn=final_evaluation,
            inputs=[],
            outputs=[status_output, final_solution_output, scores_output, chief_output, logic_output, critic_output]
        )
        
        def reset_handler():
            """Handle reset button click."""
            reset_state()
            return "🔄 Simulation reset!", "", "", "", "", ""
        
        reset_btn.click(
            fn=reset_handler,
            inputs=[],
            outputs=[status_output, chief_output, logic_output, critic_output, final_solution_output, scores_output]
        )
        
        # Footer
        gr.Markdown("---")
        gr.Markdown("""
        *© 2025-2026 Dr Giorgio Roffo - AI Consensus Engine*
        
        **Citation:** Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
        arXiv preprint arXiv:2407.12036.
        """)
    
    return demo

