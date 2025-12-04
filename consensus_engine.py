"""
AI CONSENSUS ENGINE - Problem Solving Unit
==========================================

A hierarchical multi-agent problem-solving system with:
- 1 Chief Architect (orchestrator)
- 1 Logic Strategist (high-level strategy)
- 1 Pragmatic Critic (skeptical validator)

All content is AI-generated simulation.

Main entry point for the application.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

from utils.ui import create_ui


def main():
    """Main entry point for the AI Consensus Engine."""
    demo = create_ui()
    demo.launch(share=False)


if __name__ == "__main__":
    main()
