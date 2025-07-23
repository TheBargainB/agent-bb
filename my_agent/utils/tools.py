"""This module provides tools for grocery shopping research and product search.

It includes tools for Google Shopping search using the official SerpAPI wrapper
and date retrieval.

These tools are designed for grocery shopping assistance with worldwide support
and country-specific localization.
"""

import json
import os
from datetime import datetime
from typing import Any, Callable, List

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_community.utilities import SerpAPIWrapper
from pydantic import BaseModel, Field


@tool
async def google_search(query: str, config: RunnableConfig) -> str:
    """Google Shopping search for grocery products using official SerpAPI wrapper.
    
    Args:
        query: Search query for products
        config: LangGraph configuration containing user preferences
    """
    try:
        if not query:
            return "No search query provided. Please provide a search term."
        
        # Access the configurable values from RunnableConfig
        configurable = config.get("configurable", {}) if config else {}
        
        # Get runtime configuration values
        country_code = configurable.get("country_code", "US")
        language_code = configurable.get("language_code", "en")
        
        # Create SerpAPI wrapper with shopping-specific parameters
        serpapi = SerpAPIWrapper(
            params={
                "engine": "google_shopping",
                "gl": country_code.lower(),
                "hl": language_code,
                "device": "desktop"
            }
        )
        
        # Get raw results instead of processed string
        raw_result = await serpapi.aresults(query)
        
        # Return raw JSON as string for the agent to process
        import json
        return json.dumps(raw_result, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return f"Search Error: {str(e)}. Please try again."

@tool
async def get_todays_date() -> str:
    """Get the current date."""
    return datetime.now().strftime("%Y-%m-%d")

def get_tools(selected_tools: List[str]) -> List[Callable[..., Any]]:
    """Convert a list of tool names to actual tool functions."""
    tools = []
    for tool in selected_tools:
        if tool == "google_search":
            tools.append(google_search)
        elif tool == "get_todays_date":
            tools.append(get_todays_date)
    
    return tools 