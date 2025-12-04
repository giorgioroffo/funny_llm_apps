"""
LLM Client module for AI Consensus Engine.

Handles all LLM API interactions with fallback logic and token tracking.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

import os
from openai import OpenAI
from litellm import completion
import litellm
from dotenv import load_dotenv
from .config import MODEL_FALLBACKS, MAX_TOKENS, COST_PER_1M_INPUT, COST_PER_1M_OUTPUT
from .state import consensus_state

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI()


def _derive_fallback_chain(model_id):
    """Return model + applicable fallback list."""
    for key in MODEL_FALLBACKS.keys():
        if model_id == key or model_id.startswith(f"{key}-"):
            return [model_id] + MODEL_FALLBACKS[key]
    return [model_id]


def _is_recoverable_error(error_text):
    """Check if an error is recoverable (model not found, empty response, etc.)."""
    recoverable_phrases = (
        "model_not_found",
        "does not exist",
        "not find model",
        "empty response",
        "no content returned"
    )
    error_lower = str(error_text).lower()
    return any(phrase in error_lower for phrase in recoverable_phrases)


def _extract_response_content(response):
    """Extract content and usage from LiteLLM or OpenAI response."""
    if isinstance(response, dict):
        content = response["choices"][0]["message"]["content"]
        usage = response.get("usage", {})
        tokens_in = usage.get("prompt_tokens", 0)
        tokens_out = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", tokens_in + tokens_out)
    else:
        content = response.choices[0].message.content
        usage = getattr(response, "usage", None)
        if usage:
            tokens_in = getattr(usage, "prompt_tokens", 0)
            tokens_out = getattr(usage, "completion_tokens", 0)
            total_tokens = getattr(usage, "total_tokens", tokens_in + tokens_out)
        else:
            tokens_in = tokens_out = total_tokens = 0
    
    return content, tokens_in, tokens_out, total_tokens


def _calculate_cost(tokens_in, tokens_out):
    """Calculate cost based on token usage."""
    return (tokens_in / 1_000_000 * COST_PER_1M_INPUT) + (tokens_out / 1_000_000 * COST_PER_1M_OUTPUT)


def _update_token_tracking(model, tokens_in, tokens_out, total_tokens, cost):
    """Update global state with token usage and cost."""
    consensus_state["total_tokens_in"] += tokens_in
    consensus_state["total_tokens_out"] += tokens_out
    consensus_state["total_cost"] += cost
    consensus_state["token_details"].append({
        "model": model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "total_tokens": total_tokens,
        "cost": cost
    })


def _invoke_litellm(messages, model):
    """Invoke model via LiteLLM."""
    model_name = f"openai/{model}"
    response = completion(
        model=model_name,
        messages=messages,
        api_key=openai_api_key,
        max_tokens=MAX_TOKENS
    )
    
    content, tokens_in, tokens_out, total_tokens = _extract_response_content(response)
    
    try:
        cost = litellm.completion_cost(completion_response=response, model=model_name)
    except Exception:
        cost = _calculate_cost(tokens_in, tokens_out)
    
    if not content or not content.strip():
        raise ValueError(f"Empty response from model '{model}'")
    
    _update_token_tracking(model, tokens_in, tokens_out, total_tokens, cost)
    return content, tokens_in, tokens_out, cost


def _invoke_openai_direct(messages, model):
    """Invoke model via direct OpenAI client (fallback)."""
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=MAX_TOKENS
    )
    
    content = response.choices[0].message.content
    if hasattr(response, "usage") and response.usage:
        usage = response.usage
        tokens_in = getattr(usage, "prompt_tokens", 0)
        tokens_out = getattr(usage, "completion_tokens", 0)
        cost = _calculate_cost(tokens_in, tokens_out)
    else:
        tokens_in = tokens_out = 0
        cost = 0.0
    
    total_tokens = tokens_in + tokens_out
    _update_token_tracking(model, tokens_in, tokens_out, total_tokens, cost)
    
    if not content or not content.strip():
        raise ValueError(f"Empty response from model '{model}' (direct OpenAI fallback)")
    
    return content, tokens_in, tokens_out, cost


def _invoke_model(messages, model):
    """Single attempt to call a specific model (LiteLLM + OpenAI fallback)."""
    try:
        return _invoke_litellm(messages, model)
    except Exception as e:
        import traceback
        print(f"LiteLLM error for model '{model}': {e}")
        print("Attempting direct OpenAI client fallback...")
        
        try:
            return _invoke_openai_direct(messages, model)
        except Exception as fallback_error:
            raise Exception(
                f"Both LiteLLM and OpenAI client failed for model '{model}'. "
                f"LiteLLM error: {e}; OpenAI error: {fallback_error}"
            )


def query_model(messages, model_id):
    """Query OpenAI via LiteLLM with automatic fallbacks if a model is missing."""
    attempted = set()
    chain = _derive_fallback_chain(model_id)
    last_error = None
    
    for candidate in chain:
        if candidate in attempted:
            continue
        attempted.add(candidate)
        try:
            return _invoke_model(messages, candidate)
        except Exception as exc:
            if _is_recoverable_error(str(exc)):
                print(f"[Consensus Engine] Model '{candidate}' unavailable or empty. Trying fallback...")
                last_error = exc
                continue
            raise exc
    
    raise last_error or Exception("All model fallbacks failed for query_model")

