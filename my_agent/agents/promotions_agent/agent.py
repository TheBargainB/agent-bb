"""Promotions research agent implementation."""
from langchain_core.runnables import RunnableConfig
from my_agent.utils.graph import make_graph
from my_agent.agents.promotions_agent.config import DEFAULT_PROMOTIONS_CONFIG
from my_agent.user_config import UserConfig

async def create_promotions_agent(agent_config: dict = None) -> object:
    """
    Create a promotions research agent.
    
    Args:
        agent_config: Override configuration for the agent
        
    Returns:
        Configured promotions research agent
    """
    
    # Get configuration values with defaults
    config = agent_config or {}
    user_config = config.get("user_config", UserConfig())
    
    # Create personalized system prompt if user_config is provided
    if "system_prompt" in config and isinstance(user_config, UserConfig):
        base_prompt = config["system_prompt"]
        store_info = f"Store preference: {user_config.store_preference}" if user_config.store_preference != "any" else "Store preference: any store"
        user_context = f"""
USER PREFERENCES:
- Country: {user_config.country_code}
- Language: {user_config.language_code}
- Budget: {user_config.budget_level.value}
- Dietary needs: {', '.join([dr.value for dr in user_config.dietary_restrictions]) if user_config.dietary_restrictions[0].value != "none" else "No restrictions"}
- Household size: {user_config.household_size}
- {store_info}
- Store websites: {user_config.store_websites}

When searching for promotions, prioritize the user's preferred store if specified and use the store websites for targeted searches."""
        personalized_prompt = f"{base_prompt}\n{user_context}"
    else:
        personalized_prompt = config.get("system_prompt", DEFAULT_PROMOTIONS_CONFIG.system_prompt)
    
    # Create agent configuration
    promotions_config = RunnableConfig(
        configurable={
            "model": config.get("model", DEFAULT_PROMOTIONS_CONFIG.model),
            "system_prompt": personalized_prompt,
            "selected_tools": config.get("tools", DEFAULT_PROMOTIONS_CONFIG.tools),
            "name": DEFAULT_PROMOTIONS_CONFIG.name
        }
    )
    
    # Create and return the agent
    return await make_graph(promotions_config) 