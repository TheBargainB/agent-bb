"""
Subagents creation for the supervisor system (tutorial pattern).
Create all subagents using the make_graph pattern from react_agent.
"""

from langchain_core.runnables import RunnableConfig

async def create_subagents(configurable: dict = None) -> list:
    """Create all subagents using the make_graph pattern (EXACT tutorial pattern)."""
    
    # Use configurable values if provided, otherwise fall back to defaults (tutorial pattern)
    if configurable is None:
        configurable = {}
    
    print("🔨 Creating subagents using exact tutorial pattern...")
    
    # Load supervisor configuration
    from my_agent.supervisor.supervisor_configuration import Configuration
    supervisor_config = Configuration()
    
    # Create search research agent using make_graph (EXACT tutorial pattern)
    search_config = RunnableConfig(
        configurable={
            "model": configurable.get("search_model", supervisor_config.search_model),
            "system_prompt": configurable.get("search_prompt", supervisor_config.search_system_prompt),
            "selected_tools": configurable.get("search_tools", supervisor_config.search_tools),
            "name": "search_research_agent"
        }
    )
    
    # Import make_graph from utils (tutorial pattern)
    from my_agent.utils.graph import make_graph
    search_research_agent = await make_graph(search_config)
    
    print("✅ Subagents created using tutorial pattern!")
    return [search_research_agent]
