"""
Utility functions for grocery assistant evaluation.
"""

import re
from typing import List, Dict, Any

def extract_tool_calls(messages: List[Dict[str, Any]]) -> List[str]:
    """
    Extract tool calls from assistant messages.
    
    Args:
        messages: List of message dictionaries from the assistant
        
    Returns:
        List of tool names that were called
    """
    tool_calls = []
    
    for message in messages:
        if message.get("role") == "assistant":
            content = message.get("content", "")
            
            # Look for tool calls in the content
            # This is a simplified extraction - in practice you might need more sophisticated parsing
            if "google_serpapi_product_search" in content.lower():
                tool_calls.append("google_serpapi_product_search")
            if "tavily_product_search" in content.lower():
                tool_calls.append("tavily_product_search")
            if "get_todays_date" in content.lower() or "today's date" in content.lower():
                tool_calls.append("get_todays_date")
    
    return list(set(tool_calls))  # Remove duplicates

def format_messages_string(messages: List[Dict[str, Any]]) -> str:
    """
    Format messages into a readable string for logging.
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Formatted string representation of messages
    """
    formatted = []
    
    for i, message in enumerate(messages):
        role = message.get("role", "unknown")
        content = message.get("content", "")
        formatted.append(f"[{i}] {role}: {content}")
    
    return "\n".join(formatted)

def check_response_quality(response: str, criteria: str) -> Dict[str, Any]:
    """
    Check if the response meets the quality criteria.
    
    Args:
        response: The assistant's response
        criteria: The expected criteria for the response
        
    Returns:
        Dictionary with quality metrics
    """
    response_lower = response.lower()
    criteria_lower = criteria.lower()
    
    # Simple keyword matching - in practice you might use more sophisticated NLP
    keywords = criteria_lower.split()
    matched_keywords = [kw for kw in keywords if kw in response_lower]
    
    # Calculate match percentage
    match_percentage = len(matched_keywords) / len(keywords) if keywords else 0
    
    return {
        "match_percentage": match_percentage,
        "matched_keywords": matched_keywords,
        "total_keywords": len(keywords),
        "response_length": len(response),
        "meets_criteria": match_percentage > 0.3  # Threshold for passing
    }

def check_config_usage(response: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if the response properly uses the user configuration.
    
    Args:
        response: The assistant's response
        config: The user configuration
        
    Returns:
        Dictionary with configuration usage metrics
    """
    response_lower = response.lower()
    
    usage_metrics = {}
    
    # Check country usage
    country_code = config.get("country_code", "").lower()
    usage_metrics["country_mentioned"] = country_code in response_lower
    
    # Check store preference usage
    store_preference = config.get("store_preference", "").lower()
    usage_metrics["store_preference_mentioned"] = store_preference in response_lower
    
    # Check store websites usage
    store_websites = config.get("store_websites", "")
    if store_websites:
        websites = [site.strip().lower() for site in store_websites.split(",")]
        mentioned_websites = [site for site in websites if site in response_lower]
        usage_metrics["store_websites_mentioned"] = len(mentioned_websites) > 0
        usage_metrics["mentioned_websites"] = mentioned_websites
    else:
        usage_metrics["store_websites_mentioned"] = False
        usage_metrics["mentioned_websites"] = []
    
    # Check budget level usage
    budget_level = config.get("budget_level", "").lower()
    usage_metrics["budget_level_mentioned"] = budget_level in response_lower
    
    # Check dietary restrictions usage
    dietary_restrictions = config.get("dietary_restrictions", "").lower()
    usage_metrics["dietary_restrictions_mentioned"] = dietary_restrictions in response_lower
    
    return usage_metrics 