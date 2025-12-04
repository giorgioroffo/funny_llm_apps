"""
JSON parsing module for AI Consensus Engine.

Handles extraction and parsing of JSON from LLM responses, including fallback strategies.

Author: Dr Giorgio Roffo
Year: 2025-2026
Reference: Roffo, G., 2024. Exploring advanced large language models with llmsuite. 
           arXiv preprint arXiv:2407.12036.
"""

import json
import re


def extract_json_scores(text):
    """Extract JSON from Chief's response - handles code fences, plain JSON, nested braces, incomplete JSON."""
    if not text:
        return None
    
    text = text.strip()
    
    # Method 1: Try parsing entire text as JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Method 2: Extract JSON from code fences
    json_pattern = re.compile(r'```(?:json)?\s*(\{.*?\})\s*```', re.IGNORECASE | re.DOTALL)
    matches = json_pattern.findall(text)
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue
    
    # Method 3: Find first { ... } block with proper brace matching
    start = text.find("{")
    if start != -1:
        json_str = _extract_balanced_braces(text, start)
        if json_str:
            try:
                return json.loads(json_str.strip())
            except json.JSONDecodeError:
                pass
    
    return None


def _extract_balanced_braces(text, start):
    """Extract balanced brace block starting at given position."""
    brace_count = 0
    end = start
    in_string = False
    escape_next = False
    
    for i in range(start, len(text)):
        char = text[i]
        
        if escape_next:
            escape_next = False
            continue
        
        if char == '\\':
            escape_next = True
            continue
        
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
        
        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i
                    break
    
    if end > start:
        return text[start:end + 1]
    return None


def extract_json_fallback(text):
    """Fallback: Extract key-value pairs using regex even from incomplete JSON."""
    if not text:
        return None
    
    result = {}
    
    # Extract score_agent_1_percent
    match = re.search(r'"score_agent_1_percent"\s*:\s*(\d+)', text)
    if match:
        try:
            result["score_agent_1_percent"] = int(match.group(1))
        except (ValueError, IndexError):
            pass
    
    # Extract score_agent_2_percent
    match = re.search(r'"score_agent_2_percent"\s*:\s*(\d+)', text)
    if match:
        try:
            result["score_agent_2_percent"] = int(match.group(1))
        except (ValueError, IndexError):
            pass
    
    # Extract ranking array
    match = re.search(r'"ranking"\s*:\s*\[(.*?)\]', text)
    if match:
        try:
            ranking_str = match.group(1)
            ranking_items = re.findall(r'"([^"]+)"', ranking_str)
            if ranking_items:
                result["ranking"] = ranking_items
        except (ValueError, IndexError):
            pass
    
    # Extract string fields (handle multi-line and incomplete strings)
    string_fields = [
        "agent_1_reasoning",
        "agent_2_reasoning",
        "best_solution_summary",
        "evaluation_notes"
    ]
    
    for field in string_fields:
        match = re.search(rf'"{field}"\s*:\s*"([^"]*(?:\\.[^"]*)*)"', text, re.DOTALL)
        if not match:
            match = re.search(rf'"{field}"\s*:\s*"([^"]*)', text)
        if match:
            result[field] = match.group(1).replace('\\"', '"').replace('\\n', '\n')
    
    # Only return if we got at least the scores
    if result.get("score_agent_1_percent") is not None or result.get("score_agent_2_percent") is not None:
        return result
    
    return None


def parse_evaluation_json(raw_json):
    """Parse Chief's evaluation JSON using multiple fallback strategies."""
    json_data = None
    
    # Method 1: Try direct JSON parse
    try:
        json_data = json.loads(raw_json.strip())
    except json.JSONDecodeError:
        pass
    
    # Method 2: Extract JSON from text
    if not json_data:
        json_data = extract_json_scores(raw_json)
    
    # Method 3: Fallback regex extraction
    if not json_data:
        json_data = extract_json_fallback(raw_json)
    
    return json_data


def coerce_score_to_int(score):
    """Coerce various score formats to integer."""
    if score is None:
        return None
    
    try:
        if isinstance(score, (int, float)):
            return int(round(score))
        if isinstance(score, str):
            # Remove % and extract number
            cleaned = score.replace("%", "").strip()
            match = re.search(r'-?\d+', cleaned)
            if match:
                return int(match.group())
    except (ValueError, TypeError):
        pass
    
    return None

