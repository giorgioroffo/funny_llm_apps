"""
UI module for AI Alterego Debate Simulator.

Contains Gradio interface definition and event handlers.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

import gradio as gr
from .debate_config import get_default_profiles
from .debate_conversation import save_profiles, start_conversation, next_exchange, reset_conversation


def create_ui():
    """Create the Gradio interface."""
    alice_default, bob_default = get_default_profiles()
    
    with gr.Blocks(title="AI Alterego - Debate Simulator") as demo:
        
        # Header
        gr.Markdown("""
        <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
            <h1 style='color: #ffffff; font-size: 3.5em; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-weight: 700; letter-spacing: 2px;'>
                🤖 AI ALTEREGO - Debate Simulator 🤖
            </h1>
            <p style='color: #f0f0f0; font-size: 1.2em; margin: 15px 0 10px 0; font-weight: 300; letter-spacing: 1px;'>
                Conversational Simulation Between Two AI Agents
            </p>
            <div style='background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 800px;'>
                <p style='color: #ffffff; font-size: 1.05em; margin: 0; line-height: 1.6;'>
                    Configure the profiles of two AI agents with <strong style='color: #ffd700;'>customizable personalities</strong>, 
                    <strong style='color: #60a5fa;'>interests</strong>, and <strong style='color: #34d399;'>backgrounds</strong>, 
                    and watch them debate on any topic!
                </p>
            </div>
            <div style='margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2);'>
                <p style='color: #e0e0e0; font-size: 0.95em; margin: 5px 0; font-style: italic;'>
                    Dr Giorgio Roffo • 2025-2026
                </p>
                <p style='color: #d0d0d0; font-size: 0.85em; margin: 5px 0;'>
                    Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
                    arXiv preprint arXiv:2407.12036.
                </p>
            </div>
        </div>
        """)
        
        # Disclaimer
        gr.Markdown("""
        <div style='background-color: #ffe4cc; color: #7c2d12; padding: 15px; border-radius: 5px; border-left: 4px solid #ea580c; margin-bottom: 20px;'>
        <strong style='color: #7c2d12;'>⚠️ DISCLAIMER:</strong> This content is AI-generated for demo/satire/research purposes. 
        These are <strong>NOT</strong> real statements nor quotes from real people. 
        The "personas" are simulated alter egos. All messages are prefixed with <strong>"(AI SIMULATION)"</strong> to indicate they are AI-generated simulations.
        </div>
        """)
        
        # Main Topic
        with gr.Row():
            topic_input = gr.Textbox(
                label="🎯 Debate Topic",
                placeholder="E.g.: Economic policy, climate change, education reform, healthcare systems...",
                value="What policies should governments prioritize in 2025?",
                lines=2
            )
        
        # Two columns for profiles
        with gr.Row():
            # Profile 1
            with gr.Column():
                gr.Markdown("## 👤 Agent 1 Profile")
                name1 = gr.Textbox(label="Name", value=alice_default["name"])
                gender1 = gr.Dropdown(label="Gender", choices=["female", "male"], value=alice_default["gender"])
                characteristics1 = gr.Textbox(label="Personal Characteristics", value=alice_default["characteristics"], lines=2)
                attitudes1 = gr.Textbox(label="Attitudes", value=alice_default["attitudes"], lines=2)
                hobbies1 = gr.Textbox(label="Hobbies", value=alice_default["hobbies"], lines=2)
                personality1 = gr.Textbox(label="General Personality", value=alice_default["personality"], lines=2)
                interests1 = gr.Textbox(label="Specific Interests", value=alice_default["interests"], lines=2)
                background1 = gr.Textbox(label="Professional Background", value=alice_default["background"], lines=2)
            
            # Profile 2
            with gr.Column():
                gr.Markdown("## 👤 Agent 2 Profile")
                name2 = gr.Textbox(label="Name", value=bob_default["name"])
                gender2 = gr.Dropdown(label="Gender", choices=["female", "male"], value=bob_default["gender"])
                characteristics2 = gr.Textbox(label="Personal Characteristics", value=bob_default["characteristics"], lines=2)
                attitudes2 = gr.Textbox(label="Attitudes", value=bob_default["attitudes"], lines=2)
                hobbies2 = gr.Textbox(label="Hobbies", value=bob_default["hobbies"], lines=2)
                personality2 = gr.Textbox(label="General Personality", value=bob_default["personality"], lines=2)
                interests2 = gr.Textbox(label="Specific Interests", value=bob_default["interests"], lines=2)
                background2 = gr.Textbox(label="Professional Background", value=bob_default["background"], lines=2)
        
        # Buttons
        with gr.Row():
            save_btn = gr.Button("💾 Save Profiles", variant="secondary")
            start_btn = gr.Button("🚀 Start Conversation", variant="primary")
            next_btn = gr.Button("➡️ Next Exchange", variant="primary")
            reset_btn = gr.Button("🔄 Reset", variant="secondary")
        
        # Status
        status_output = gr.Textbox(label="📊 Status", interactive=False, lines=3)
        
        # Conversation display
        gr.Markdown("---")
        
        # Dynamic title for conversation
        conversation_title = gr.Markdown("## 🎭 Debate simulation between two AI agents (AI-generated, not real quotes)")
        
        with gr.Row():
            with gr.Column():
                chat1_label = gr.Markdown(f"### 🔴 [AI SIMULATION] Alterego inspired by {alice_default['name']}")
                chat1_output = gr.Textbox(label="", interactive=False, lines=15, show_label=False)
            
            with gr.Column():
                chat2_label = gr.Markdown(f"### 🔵 [AI SIMULATION] Alterego inspired by {bob_default['name']}")
                chat2_output = gr.Textbox(label="", interactive=False, lines=15, show_label=False)
        
        # Event handlers
        save_btn.click(
            fn=save_profiles,
            inputs=[topic_input, 
                    name1, gender1, characteristics1, attitudes1, hobbies1, personality1, interests1, background1,
                    name2, gender2, characteristics2, attitudes2, hobbies2, personality2, interests2, background2],
            outputs=[status_output, conversation_title, chat1_label, chat2_label]
        )
        
        start_btn.click(
            fn=start_conversation,
            inputs=[],
            outputs=[status_output, chat1_output, chat2_output]
        )
        
        next_btn.click(
            fn=next_exchange,
            inputs=[],
            outputs=[status_output, chat1_output, chat2_output]
        )
        
        reset_btn.click(
            fn=reset_conversation,
            inputs=[],
            outputs=[status_output, chat1_output, chat2_output]
        )
        
        # Footer
        gr.Markdown("---")
        gr.Markdown("""
        *© 2025-2026 Dr Giorgio Roffo - AI Alterego Debate Simulator*
        
        **Citation:** Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
        arXiv preprint arXiv:2407.12036.
        """)
    
    return demo

