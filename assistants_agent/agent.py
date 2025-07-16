"""
Main agent definition for the international assistants agent system.
This file exposes the compiled supervisor graph for LangGraph deployment.
"""

from langchain_core.runnables import RunnableConfig
from assistants_agent.supervisor.supervisor_configuration import Configuration, create_supervisor_system_prompt
from assistants_agent.supervisor.subagents import create_subagents
from assistants_agent.utils.utils import load_chat_model
from assistants_agent.user_config import UserConfig, DietaryRestriction, BudgetLevel

from langgraph_supervisor import create_supervisor

# Main graph construction function
async def make_supervisor_graph(config: RunnableConfig):
    """Create the international supervisor graph with all specialized agents."""
    # Extract configuration values directly from the config
    configurable = config.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "openai/gpt-4.1")
    
    # Get configuration fields
    country_code = configurable.get("country_code", "NL")
    language_code = configurable.get("language_code", "nl")
    dietary_restrictions_str = configurable.get("dietary_restrictions", "none")
    budget_level_str = configurable.get("budget_level", "medium") 
    household_size = configurable.get("household_size", 1)
    
    # Build user config from region defaults
    user_config = UserConfig(
        country_code=country_code,
        language_code=language_code,
        dietary_restrictions=[DietaryRestriction.NONE], # Default to none
        budget_level=BudgetLevel.MEDIUM, # Default to medium
        household_size=household_size,
        store_preference="any",  # Default to any store
        store_websites="ah.nl, jumbo.com, lidl.nl"  # Default websites
    )
    
    # Override with specific user preferences
    if dietary_restrictions_str != "none":
        try:
            user_config.dietary_restrictions = [DietaryRestriction(dietary_restrictions_str)]
        except ValueError:
            # If invalid dietary restriction, keep default
            pass
    else:
        # Explicitly set to none
        user_config.dietary_restrictions = [DietaryRestriction.NONE]
    
    try:
        user_config.budget_level = BudgetLevel(budget_level_str)
    except ValueError:
        # If invalid budget level, keep default
        pass
        
    user_config.household_size = household_size
    
    # Allow override with full user_config if provided
    user_config_data = configurable.get("user_config")
    if isinstance(user_config_data, dict):
        user_config = UserConfig(**user_config_data)
    elif isinstance(user_config_data, UserConfig):
        user_config = user_config_data
    
    # Create dynamic supervisor system prompt based on user configuration
    if "supervisor_system_prompt" in configurable:
        # Use explicitly provided prompt
        supervisor_system_prompt = configurable["supervisor_system_prompt"]
    else:
        # Generate dynamic international prompt
        supervisor_system_prompt = create_supervisor_system_prompt(user_config)
    
    # Update configurable to ensure user_config is available to subagents
    configurable_with_user = configurable.copy()
    configurable_with_user["user_config"] = user_config
    
    # Create subagents using the async function, passing configurable values with user config
    subagents = await create_subagents(configurable_with_user)

    # Create supervisor graph
    supervisor_graph = create_supervisor(
        agents=subagents,
        model=load_chat_model(supervisor_model),
        prompt=supervisor_system_prompt,
        config_schema=Configuration
    )

    compiled_graph = supervisor_graph.compile()
    return compiled_graph

# Export the graph for LangGraph configuration
graph = make_supervisor_graph 