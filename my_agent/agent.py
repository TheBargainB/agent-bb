"""
Main agent definition for the international assistants agent system.
This file exposes the compiled supervisor graph for LangGraph deployment.
"""

from langchain_core.runnables import RunnableConfig
from my_agent.supervisor.supervisor_configuration import Configuration, create_supervisor_system_prompt
from my_agent.supervisor.subagents import create_subagents
from my_agent.utils.utils import load_chat_model
from my_agent.user_config import UserConfig, DietaryRestriction, BudgetLevel

from langgraph_supervisor import create_supervisor

# Main graph construction function
async def make_supervisor_graph(config: RunnableConfig):
    """Create the international supervisor graph with all specialized agents."""
    # Extract configuration values directly from the config
    configurable = config.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "openai/gpt-4.1")
    
    # Get configuration fields with proper defaults
    country_code = configurable.get("country_code", "US")  # Changed from NL to US as more neutral default
    language_code = configurable.get("language_code", "en")  # Changed from nl to en as more neutral default
    dietary_restrictions_str = configurable.get("dietary_restrictions", "none")
    budget_level_str = configurable.get("budget_level", "medium") 
    household_size = configurable.get("household_size", 1)
    store_preference = configurable.get("store_preference", "any")  # ADDED: Missing store_preference extraction
    
    # Get store websites from user config or auto-generate based on country
    store_websites = configurable.get("store_websites")
    if not store_websites:
        # Auto-generate country-specific store websites
        if country_code == "US":
            store_websites = "walmart.com, target.com, kroger.com, safeway.com, albertsons.com"
        elif country_code == "UK":
            store_websites = "tesco.com, sainsburys.co.uk, asda.com, morrisons.com, waitrose.com"
        elif country_code == "DE":
            store_websites = "edeka.de, rewe.de, aldi.de, lidl.de, netto-online.de"
        elif country_code == "NL":
            store_websites = "ah.nl, jumbo.com, lidl.nl, dirk.nl, hoogevliet.com"
        elif country_code == "FR":
            store_websites = "carrefour.fr, auchan.fr, leclerc.fr, monoprix.fr, franprix.fr"
        elif country_code == "CA":
            store_websites = "loblaw.ca, sobeys.com, metro.ca, walmart.ca, costco.ca"
        elif country_code == "AU":
            store_websites = "woolworths.com.au, coles.com.au, aldi.com.au, iga.com.au"
        else:
            # Generic international defaults for other countries
            store_websites = "amazon.com, walmart.com, tesco.com"
    
    # Build user config from region defaults
    user_config = UserConfig(
        user_id=configurable.get("user_id", ""),
        country_code=country_code,
        language_code=language_code,
        dietary_restrictions=[DietaryRestriction.NONE], # Default to none
        budget_level=BudgetLevel.MEDIUM, # Default to medium
        household_size=household_size,
        store_preference=store_preference,  # Use extracted store_preference
        store_websites=store_websites  # Use user's store websites or auto-generated defaults
    )
    

    
    # Allow override with full user_config if provided - MOVED TO TOP for proper priority
    user_config_data = configurable.get("user_config")
    if isinstance(user_config_data, dict):
        # Use provided user_config dict as highest priority
        user_config = UserConfig(**user_config_data)
    elif isinstance(user_config_data, UserConfig):
        # Use provided UserConfig instance as highest priority
        user_config = user_config_data
    else:
        # Only process individual fields if no user_config provided
        # Override with specific user preferences - FIXED: Proper enum conversion
        if dietary_restrictions_str != "none":
            try:
                # Convert string to enum list properly
                user_config.dietary_restrictions = [DietaryRestriction(dietary_restrictions_str)]
            except ValueError:
                # If invalid dietary restriction, keep default
                user_config.dietary_restrictions = [DietaryRestriction.NONE]
        else:
            # Explicitly set to none
            user_config.dietary_restrictions = [DietaryRestriction.NONE]
        
        # Convert budget level string to enum
        try:
            user_config.budget_level = BudgetLevel(budget_level_str)
        except ValueError:
            # If invalid budget level, keep default
            user_config.budget_level = BudgetLevel.MEDIUM
            
        user_config.household_size = household_size
    
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