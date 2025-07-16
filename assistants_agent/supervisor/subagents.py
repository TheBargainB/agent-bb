"""Create all subagents using individual agent files and configs."""
from assistants_agent.supervisor.supervisor_configuration import Configuration
from assistants_agent.agents.promotions_agent.agent import create_promotions_agent
from assistants_agent.agents.grocery_agent.agent import create_grocery_agent
from assistants_agent.user_config import UserConfig

# Load supervisor configuration
supervisor_config = Configuration()

async def create_subagents(configurable: dict = None):
    """Create all subagents using individual agent files."""
    
    # Use configurable values if provided, otherwise fall back to defaults
    if configurable is None:
        configurable = {}
    
    # Build user_config from individual fields if not provided
    user_config_data = configurable.get("user_config")
    if user_config_data is None:
        user_config = UserConfig(
            country_code=supervisor_config.country_code,
            language_code=supervisor_config.language_code,
            dietary_restrictions=supervisor_config.dietary_restrictions,
            budget_level=supervisor_config.budget_level,
            household_size=supervisor_config.household_size,
            store_preference=supervisor_config.store_preference,
            store_websites=supervisor_config.store_websites
        )
    elif isinstance(user_config_data, dict):
        # Convert dict to UserConfig instance
        user_config = UserConfig(**user_config_data)
    elif isinstance(user_config_data, UserConfig):
        # Already a UserConfig instance
        user_config = user_config_data
    else:
        # Fallback to building from individual fields
        user_config = UserConfig(
            country_code=supervisor_config.country_code,
            language_code=supervisor_config.language_code,
            dietary_restrictions=supervisor_config.dietary_restrictions,
            budget_level=supervisor_config.budget_level,
            household_size=supervisor_config.household_size,
            store_preference=supervisor_config.store_preference,
            store_websites=supervisor_config.store_websites
        )

    # Create promotions research agent
    promotions_agent_config = {
        "model": configurable.get("promotions_model", supervisor_config.promotions_model),
        "system_prompt": configurable.get("promotions_system_prompt", supervisor_config.promotions_system_prompt),
        "tools": configurable.get("promotions_tools", supervisor_config.promotions_tools),
        "user_config": user_config
    }
    promotions_research_agent = await create_promotions_agent(promotions_agent_config)

    # Create grocery search agent
    grocery_agent_config = {
        "model": configurable.get("grocery_model", supervisor_config.grocery_model),
        "system_prompt": configurable.get("grocery_system_prompt", supervisor_config.grocery_system_prompt),
        "tools": configurable.get("grocery_tools", supervisor_config.grocery_tools),
        "user_config": user_config
    }
    grocery_search_agent = await create_grocery_agent(grocery_agent_config)
    
    return [promotions_research_agent, grocery_search_agent]
