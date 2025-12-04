"""
Configuration module for AI Consensus Engine.

Contains all constants, model definitions, and configuration settings.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

# Model definitions (pick distinct models tuned for each role)
# - Chief: best reasoning horsepower (we attempt the newest tier, then fall back automatically)
# - Logic: math-heavy but still efficient
# - Critic: lightweight + fast for punchy rebuttals
CHIEF_MODEL = "gpt-4.1"
LOGIC_MODEL = "gpt-4o"
CRITIC_MODEL = "gpt-4.1-nano-2025-04-14"

# Fallback chains so the sim keeps running even if a model is unavailable in the org
MODEL_FALLBACKS = {
    "gpt-4.1": ["gpt-4.1", "gpt-4o", "gpt-4o-mini"],
    "gpt-4o": ["gpt-4o-mini", "gpt-3.5-turbo"],
    "gpt-4.1-nano-2025-04-14": ["gpt-4o-mini", "gpt-3.5-turbo"],
    "gpt-4o-mini": ["gpt-3.5-turbo"]
}

# Required final evaluation JSON schema so the Chief always follows it
FINAL_EVAL_JSON_SCHEMA = """{
  "score_agent_1_percent": <integer 0-100>,
  "score_agent_2_percent": <integer 0-100>,
  "ranking": ["Agent 1", "Agent 2"],
  "agent_1_reasoning": "<concise chief judgement about Agent 1>",
  "agent_2_reasoning": "<concise chief judgement about Agent 2>",
  "best_solution_summary": "<short paragraph explaining the winning approach>",
  "evaluation_notes": "<optional chief notes or tie-breaker comments>"
}"""

# LLM API settings
MAX_TOKENS = 200
COST_PER_1M_INPUT = 2.50
COST_PER_1M_OUTPUT = 10.00

# Simulation settings
NUM_ITERATIONS = 3

