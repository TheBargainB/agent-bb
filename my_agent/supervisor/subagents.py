"""Create all subagents using individual agent files and configs."""
from my_agent.supervisor.supervisor_configuration import Configuration
from my_agent.agents.promotions_agent.agent import create_promotions_agent
from my_agent.agents.grocery_agent.agent import create_grocery_agent
from my_agent.user_config import UserConfig, DietaryRestriction, BudgetLevel

# Load supervisor configuration
supervisor_config = Configuration()

async def create_subagents(configurable: dict = None):
    """Create all subagents using individual agent files."""
    
    # Use configurable values if provided, otherwise fall back to defaults
    if configurable is None:
        configurable = {}
    
    # Build user_config from individual fields if not provided - FIXED: Consistent with agent.py logic
    user_config_data = configurable.get("user_config")
    if user_config_data is None:
        # Use the same logic as agent.py for consistency
        country_code = configurable.get("country_code", "US")
        language_code = configurable.get("language_code", "en")
        dietary_restrictions_str = configurable.get("dietary_restrictions", "none")
        budget_level_str = configurable.get("budget_level", "medium")
        household_size = configurable.get("household_size", 1)
        store_preference = configurable.get("store_preference", "any")
        
        # Auto-generate store websites based on country
        store_websites = configurable.get("store_websites")
        if not store_websites:
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
                store_websites = "amazon.com, walmart.com, tesco.com"
        
        # Create UserConfig with proper enum conversion
        user_config = UserConfig(
            user_id=configurable.get("user_id", ""),
            country_code=country_code,
            language_code=language_code,
            dietary_restrictions=[DietaryRestriction.NONE],  # Default
            budget_level=BudgetLevel.MEDIUM,  # Default
            household_size=household_size,
            store_preference=store_preference,
            store_websites=store_websites
        )
        
        # Apply user preferences with proper enum conversion
        if dietary_restrictions_str != "none":
            try:
                user_config.dietary_restrictions = [DietaryRestriction(dietary_restrictions_str)]
            except ValueError:
                user_config.dietary_restrictions = [DietaryRestriction.NONE]
        
        try:
            user_config.budget_level = BudgetLevel(budget_level_str)
        except ValueError:
            user_config.budget_level = BudgetLevel.MEDIUM
            
    elif isinstance(user_config_data, dict):
        # Convert dict to UserConfig instance
        user_config = UserConfig(**user_config_data)
    elif isinstance(user_config_data, UserConfig):
        # Already a UserConfig instance
        user_config = user_config_data
    else:
        # Fallback to building from individual fields (same as above)
        country_code = configurable.get("country_code", "US")
        language_code = configurable.get("language_code", "en")
        dietary_restrictions_str = configurable.get("dietary_restrictions", "none")
        budget_level_str = configurable.get("budget_level", "medium")
        household_size = configurable.get("household_size", 1)
        store_preference = configurable.get("store_preference", "any")
        
        # Auto-generate store websites based on country
        store_websites = configurable.get("store_websites")
        if not store_websites:
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
                store_websites = "amazon.com, walmart.com, tesco.com"
        
        user_config = UserConfig(
            user_id=configurable.get("user_id", ""),
            country_code=country_code,
            language_code=language_code,
            dietary_restrictions=[DietaryRestriction.NONE],
            budget_level=BudgetLevel.MEDIUM,
            household_size=household_size,
            store_preference=store_preference,
            store_websites=store_websites
        )
        
        # Apply user preferences
        if dietary_restrictions_str != "none":
            try:
                user_config.dietary_restrictions = [DietaryRestriction(dietary_restrictions_str)]
            except ValueError:
                user_config.dietary_restrictions = [DietaryRestriction.NONE]
        
        try:
            user_config.budget_level = BudgetLevel(budget_level_str)
        except ValueError:
            user_config.budget_level = BudgetLevel.MEDIUM

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
