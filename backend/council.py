"""
Council orchestration for the 3-stage multi-LLM consultation process.
"""
import logging
import time
from typing import Dict, List, Any, Optional
from openrouter import query_models_parallel
from config import COUNCIL_MODELS
from rate_limiter import get_rate_limiter
from performance import get_performance_monitor

logger = logging.getLogger(__name__)


import asyncio as asyncio_module


async def stage1_collect_responses(
    user_query: str,
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Stage 1: Collect individual responses from all council models in parallel.
    
    Args:
        user_query: The user's question/query
        api_key: OpenRouter API key (uses config default if not provided)
    
    Returns:
        List of dictionaries with 'model' and 'response' keys.
        Only includes successful responses (filters out None values).
    
    Requirements: 3.1, 3.2, 3.3, 3.5
    """
    # Start performance monitoring
    perf_monitor = get_performance_monitor()
    timer_id = perf_monitor.start_stage(1, {"query_length": len(user_query)})
    
    logger.info(f"Stage 1: Collecting responses from {len(COUNCIL_MODELS)} models")
    
    # Use adaptive rate limiter instead of fixed delay
    rate_limiter = get_rate_limiter()
    await rate_limiter.wait_if_needed("openrouter")
    
    # Build messages list with user query
    messages = [
        {"role": "user", "content": user_query}
    ]
    
    # Track individual model response times
    model_start_times = {model: time.time() for model in COUNCIL_MODELS}
    
    # Query all council models in parallel
    responses = await query_models_parallel(
        models=COUNCIL_MODELS,
        messages=messages,
        api_key=api_key
    )
    
    # Filter out None responses and format results
    results = []
    for model, response in responses.items():
        # Log individual model response time
        if model in model_start_times:
            duration = time.time() - model_start_times[model]
            perf_monitor.log_model_response(model, duration)
        
        if response is not None and response.get("content"):
            results.append({
                "model": model,
                "response": response["content"]
            })
        else:
            logger.warning(f"Stage 1: No response from model {model}")
    
    logger.info(f"Stage 1: Collected {len(results)}/{len(COUNCIL_MODELS)} responses")
    
    if not results:
        logger.error("Stage 1: All models failed to respond")
    
    # End performance monitoring
    stage_duration = perf_monitor.end_stage(timer_id)
    
    return results



def _anonymize_responses(stage1_results: List[Dict[str, Any]]) -> tuple[str, Dict[str, str]]:
    """
    Anonymize Stage 1 responses for unbiased peer review.
    
    Args:
        stage1_results: List of dicts with 'model' and 'response' keys
    
    Returns:
        Tuple of (anonymized_text, label_to_model_mapping)
        - anonymized_text: Formatted string with "Response A:", "Response B:", etc.
        - label_to_model_mapping: Dict mapping "Response A" -> model name
    
    Requirements: 4.1, 4.5
    """
    labels = [chr(65 + i) for i in range(len(stage1_results))]  # A, B, C, ...
    
    # Create label to model mapping
    label_to_model = {}
    anonymized_parts = []
    
    for label, result in zip(labels, stage1_results):
        response_label = f"Response {label}"
        label_to_model[response_label] = result["model"]
        
        anonymized_parts.append(f"{response_label}:\n{result['response']}\n")
    
    anonymized_text = "\n".join(anonymized_parts)
    
    logger.info(f"Anonymized {len(stage1_results)} responses with labels {labels}")
    
    return anonymized_text, label_to_model



def _build_ranking_prompt(user_query: str, anonymized_responses: str) -> str:
    """
    Build the ranking prompt for Stage 2 peer review.
    
    Args:
        user_query: The original user question
        anonymized_responses: Formatted anonymized responses
    
    Returns:
        Complete prompt string for ranking
    
    Requirements: 4.2
    """
    prompt = f"""You are evaluating different responses to the following question:

{user_query}

Here are the responses (anonymized):

{anonymized_responses}

Your task:
1. Evaluate each response based on accuracy, completeness, clarity, and usefulness
2. Consider the strengths and weaknesses of each response
3. Provide a final ranking from best to worst

IMPORTANT: You MUST format your final ranking EXACTLY as shown below:

FINAL RANKING:
1. Response X
2. Response Y
3. Response Z

(Replace X, Y, Z with the actual response letters)

Now provide your evaluation and ranking:"""
    
    return prompt



import re


def parse_ranking_from_text(ranking_text: str) -> List[str]:
    """
    Parse ranking from model's response text using regex with fallbacks.
    
    Args:
        ranking_text: The full text response from the ranking model
    
    Returns:
        Ordered list of response labels (e.g., ["Response C", "Response A", "Response B"])
        Returns empty list if parsing fails completely.
    
    Requirements: 4.4
    """
    # Strategy 1: Look for "FINAL RANKING:" section with numbered list
    final_ranking_pattern = r'FINAL RANKING:\s*\n((?:\d+\.\s*Response\s+[A-Z]\s*\n?)+)'
    match = re.search(final_ranking_pattern, ranking_text, re.IGNORECASE | re.MULTILINE)
    
    if match:
        ranking_section = match.group(1)
        # Extract "Response X" patterns in order
        response_pattern = r'Response\s+([A-Z])'
        matches = re.findall(response_pattern, ranking_section, re.IGNORECASE)
        if matches:
            result = [f"Response {letter.upper()}" for letter in matches]
            logger.info(f"Parsed ranking (strategy 1): {result}")
            return result
    
    # Strategy 2: Fallback - find all "Response X" patterns in order of appearance
    response_pattern = r'Response\s+([A-Z])'
    matches = re.findall(response_pattern, ranking_text, re.IGNORECASE)
    
    if matches:
        # Remove duplicates while preserving order
        seen = set()
        result = []
        for letter in matches:
            letter_upper = letter.upper()
            response_label = f"Response {letter_upper}"
            if response_label not in seen:
                seen.add(response_label)
                result.append(response_label)
        
        logger.info(f"Parsed ranking (strategy 2 - fallback): {result}")
        return result
    
    logger.warning("Failed to parse any ranking from text")
    return []



from typing import Tuple


async def stage2_collect_rankings(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
    api_key: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """
    Stage 2: Each model ranks anonymized responses from Stage 1.
    
    Args:
        user_query: The original user question
        stage1_results: Results from Stage 1 with 'model' and 'response' keys
        api_key: OpenRouter API key (uses config default if not provided)
    
    Returns:
        Tuple of (stage2_results, label_to_model_mapping)
        - stage2_results: List of dicts with 'model', 'ranking', and 'parsed_ranking' keys
        - label_to_model_mapping: Dict mapping "Response A" -> model name
    
    Requirements: 4.3, 4.4
    """
    # Start performance monitoring
    perf_monitor = get_performance_monitor()
    timer_id = perf_monitor.start_stage(2, {"responses_to_rank": len(stage1_results)})
    
    logger.info(f"Stage 2: Collecting rankings from {len(COUNCIL_MODELS)} models")
    
    # Use adaptive rate limiter instead of fixed delay
    rate_limiter = get_rate_limiter()
    await rate_limiter.wait_if_needed("openrouter")
    
    if not stage1_results:
        logger.error("Stage 2: No Stage 1 results to rank")
        return [], {}
    
    # Anonymize responses
    anonymized_text, label_to_model = _anonymize_responses(stage1_results)
    
    # Build ranking prompt
    ranking_prompt = _build_ranking_prompt(user_query, anonymized_text)
    
    # Create messages for ranking
    messages = [
        {"role": "user", "content": ranking_prompt}
    ]
    
    # Track individual model response times
    model_start_times = {model: time.time() for model in COUNCIL_MODELS}
    
    # Query all council models in parallel
    responses = await query_models_parallel(
        models=COUNCIL_MODELS,
        messages=messages,
        api_key=api_key
    )
    
    # Process rankings
    results = []
    for model, response in responses.items():
        # Log individual model response time
        if model in model_start_times:
            duration = time.time() - model_start_times[model]
            perf_monitor.log_model_response(model, duration)
        
        if response is not None and response.get("content"):
            ranking_text = response["content"]
            parsed_ranking = parse_ranking_from_text(ranking_text)
            
            results.append({
                "model": model,
                "ranking": ranking_text,
                "parsed_ranking": parsed_ranking
            })
        else:
            logger.warning(f"Stage 2: No ranking from model {model}")
    
    logger.info(f"Stage 2: Collected {len(results)}/{len(COUNCIL_MODELS)} rankings")
    
    # End performance monitoring
    stage_duration = perf_monitor.end_stage(timer_id)
    
    return results, label_to_model



from collections import defaultdict


def calculate_aggregate_rankings(
    stage2_results: List[Dict[str, Any]],
    label_to_model: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Calculate aggregate rankings across all peer reviews.
    
    Args:
        stage2_results: Results from Stage 2 with 'parsed_ranking' lists
        label_to_model: Mapping from "Response X" labels to model names
    
    Returns:
        List of dicts sorted by average rank (best first) with keys:
        - model: Model name
        - average_rank: Average position (lower is better)
        - rankings_count: Number of times this model was ranked
    
    Requirements: 5.1, 5.2, 5.3, 5.4, 5.5
    """
    logger.info("Calculating aggregate rankings")
    
    # Track positions for each response label
    positions = defaultdict(list)
    
    for result in stage2_results:
        parsed_ranking = result.get("parsed_ranking", [])
        
        # Record position (1-indexed) for each response in this ranking
        for position, response_label in enumerate(parsed_ranking, start=1):
            positions[response_label].append(position)
    
    # Calculate average rank for each model
    aggregate = []
    for response_label, model_name in label_to_model.items():
        if response_label in positions:
            position_list = positions[response_label]
            average_rank = sum(position_list) / len(position_list)
            
            aggregate.append({
                "model": model_name,
                "average_rank": average_rank,
                "rankings_count": len(position_list)
            })
        else:
            # Model wasn't ranked by anyone
            logger.warning(f"Model {model_name} ({response_label}) received no rankings")
            aggregate.append({
                "model": model_name,
                "average_rank": float('inf'),  # Worst possible rank
                "rankings_count": 0
            })
    
    # Sort by average rank (lower is better)
    aggregate.sort(key=lambda x: x["average_rank"])
    
    logger.info(f"Aggregate rankings calculated for {len(aggregate)} models")
    
    return aggregate



def _build_chairman_prompt(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
    stage2_results: List[Dict[str, Any]]
) -> str:
    """
    Build the chairman prompt with full context from all stages.
    
    Args:
        user_query: The original user question
        stage1_results: Individual responses from Stage 1
        stage2_results: Rankings from Stage 2
    
    Returns:
        Complete prompt string for chairman synthesis
    
    Requirements: 6.1, 6.3
    """
    # Format Stage 1 responses
    stage1_text = "STAGE 1 - Individual Responses:\n\n"
    for i, result in enumerate(stage1_results, 1):
        model_name = result["model"].split("/")[-1] if "/" in result["model"] else result["model"]
        stage1_text += f"{i}. {model_name}:\n{result['response']}\n\n"
    
    # Format Stage 2 rankings
    stage2_text = "STAGE 2 - Peer Rankings:\n\n"
    for i, result in enumerate(stage2_results, 1):
        model_name = result["model"].split("/")[-1] if "/" in result["model"] else result["model"]
        stage2_text += f"{i}. {model_name}'s Ranking:\n{result['ranking']}\n\n"
    
    # Build complete chairman prompt
    prompt = f"""You are the Chairman of an LLM Council. Multiple AI models have provided responses to a question and then ranked each other's answers.

Original Question: {user_query}

{stage1_text}

{stage2_text}

Your task as Chairman is to synthesize all of this information into a single, comprehensive answer. This is NOT a summary - you should:

1. Consider the insights from all individual responses
2. Take into account the peer rankings and what they reveal about response quality
3. Note patterns of agreement or disagreement among the models
4. Integrate the collective wisdom into a cohesive, well-reasoned answer
5. Provide additional context or nuance where the council's responses complement each other

Synthesize the council's collective wisdom into your final answer:"""
    
    return prompt



from openrouter import query_model
from config import CHAIRMAN_MODEL


async def stage3_synthesize_final(
    user_query: str,
    stage1_results: List[Dict[str, Any]],
    stage2_results: List[Dict[str, Any]],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Stage 3: Chairman synthesizes final response with full context.
    
    Args:
        user_query: The original user question
        stage1_results: Individual responses from Stage 1
        stage2_results: Rankings from Stage 2
        api_key: OpenRouter API key (uses config default if not provided)
    
    Returns:
        Dictionary with 'model' and 'response' keys.
        Returns error message if chairman query fails.
    
    Requirements: 6.2, 6.4, 6.5
    """
    # Start performance monitoring
    perf_monitor = get_performance_monitor()
    timer_id = perf_monitor.start_stage(3, {
        "stage1_responses": len(stage1_results),
        "stage2_rankings": len(stage2_results)
    })
    
    logger.info(f"Stage 3: Chairman ({CHAIRMAN_MODEL}) synthesizing final answer")
    
    # Use adaptive rate limiter instead of fixed delay
    rate_limiter = get_rate_limiter()
    await rate_limiter.wait_if_needed("openrouter")
    
    # Build comprehensive chairman prompt
    chairman_prompt = _build_chairman_prompt(user_query, stage1_results, stage2_results)
    
    # Create messages
    messages = [
        {"role": "user", "content": chairman_prompt}
    ]
    
    # Track chairman response time
    chairman_start_time = time.time()
    
    # Query chairman model
    response = await query_model(
        model=CHAIRMAN_MODEL,
        messages=messages,
        api_key=api_key
    )
    
    # Log chairman response time
    chairman_duration = time.time() - chairman_start_time
    perf_monitor.log_model_response(CHAIRMAN_MODEL, chairman_duration)
    
    if response is None or not response.get("content"):
        logger.error("Stage 3: Chairman failed to generate response")
        # End monitoring even on failure
        perf_monitor.end_stage(timer_id)
        return {
            "model": CHAIRMAN_MODEL,
            "response": "Error: The chairman was unable to synthesize a final answer. Please try again."
        }
    
    logger.info("Stage 3: Chairman synthesis complete")
    
    # End performance monitoring
    stage_duration = perf_monitor.end_stage(timer_id)
    
    return {
        "model": CHAIRMAN_MODEL,
        "response": response["content"]
    }
