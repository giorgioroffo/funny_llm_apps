"""
AI ALTEREGO - DEBATE SIMULATOR
==============================

A simulation tool for conversations between two AI agents with customizable 
personalities, interests, and backgrounds. Uses Gradio for a web interface.

Main entry point for the application.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

from utils.debate_ui import create_ui


def main():
    """Main entry point for the AI Alterego Debate Simulator."""
    demo = create_ui()
    demo.launch(share=False)


if __name__ == "__main__":
    main()
