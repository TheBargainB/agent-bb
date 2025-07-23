"""Configuration utilities for the grocery shopping assistant."""

from typing import Literal
from pydantic import BaseModel, Field

class Configuration(BaseModel):
    """Base configuration for the grocery shopping assistant.
    
    This configuration allows users to select which tools are available
    to the assistant during operation.
    """
    
    # Tool selection
    selected_tools: list[Literal["google_search", "get_todays_date"]] = Field(
        default=["google_search", "get_todays_date"],
        description="List of tools available to the assistant"
    )
    
    # Agent configuration  
    agent_model: str = Field(
        default="openai/gpt-4o-mini",
        description="Language model to use for the assistant"
    )
    
    # Search configuration
    max_results_per_tool: int = Field(
        default=5,
        description="Maximum number of results per search tool"
    )
    
    # Performance configuration
    enable_parallel_search: bool = Field(
        default=True,
        description="Enable parallel execution of search tools"
    )

# Default configuration instance
DEFAULT_CONFIG = Configuration() 