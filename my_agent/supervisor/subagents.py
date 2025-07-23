"""
Subagents creation for the supervisor system.
This module handles the creation and configuration of specialized agents.
"""

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import ToolMessage
from my_agent.utils.utils import load_chat_model

async def create_search_research_agent(model_name: str, system_prompt: str):
    """Create a search research agent graph."""
    from my_agent.utils.graph import make_graph
    from my_agent.supervisor.supervisor_configuration import Configuration
    
    # Load supervisor configuration for defaults
    supervisor_config = Configuration()
    
    # Create configuration for the search agent
    search_config = RunnableConfig(
        configurable={
            "model": model_name,
            "system_prompt": system_prompt,
            "selected_tools": supervisor_config.search_tools,
            "name": "search_research_agent",
            "country_code": supervisor_config.country_code,
            "language_code": supervisor_config.language_code,
            "store_preference": supervisor_config.store_preference
        }
    )
    
    # Create and return the graph (awaited since make_graph is async)
    return await make_graph(search_config)

async def create_subagents(configurable: dict) -> list:
    """Create and return a list of specialized subagents."""
    print("🔨 Creating subagents with Phase 3 sophisticated memory...")
    
    # Extract agent configurations from configurable
    search_model = configurable.get("search_model", "openai/gpt-4o-mini")
    search_prompt = configurable.get(
        "search_prompt", 
        "You are a grocery product search specialist. Help users find specific food products, "
        "compare prices, and discover new items that match their dietary preferences."
    )
    
    # Create the search/research agent graph
    search_research_agent_graph = await create_search_research_agent(
        model_name=search_model,
        system_prompt=search_prompt
    )
    
    # Add name attribute to the graph so langgraph_supervisor can access it
    search_research_agent_graph.name = "search_research_agent"
    
    # Define the function schema for the supervisor
    search_function = {
        "name": "search_research_agent",
        "description": "Search for grocery products, research pricing, and find items matching dietary preferences",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for grocery products or research"
                }
            },
            "required": ["query"]
        }
    }
    
    # Add function attribute to the graph as well
    search_research_agent_graph.function = search_function
    
    return [search_research_agent_graph]
