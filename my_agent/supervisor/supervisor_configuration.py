"""Define the configurable parameters for the international supervisor agent."""
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from my_agent.user_config import UserConfig

today = datetime.now().strftime("%Y-%m-%d")

class Configuration(BaseModel):
    """Unified configuration for the international supervisor and all sub-agents."""

    # User identification
    user_id: str = Field(
        default="",
        description="Unique identifier for the user session",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )

    # User preference fields (exposed in UI)
    country_code: str = Field(
        default="US",
        description="Country code (US, UK, DE, NL, FR, etc.) - determines default stores and language",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )
    
    language_code: str = Field(
        default="en",
        description="Language code (en, nl, de, fr, etc.) for search terms and responses",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )
    
    dietary_restrictions: str = Field(
        default="none",
        description="Dietary restrictions: none, vegetarian, vegan, gluten_free, halal, kosher, etc.",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )
    
    budget_level: str = Field(
        default="medium",
        description="Budget level: low, medium, high, no_limit",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )
    
    household_size: int = Field(
        default=1,
        description="Number of people in household (affects quantity recommendations)",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )
    
    store_preference: str = Field(
        default="any",
        description="Preferred store for shopping (e.g., 'Albert Heijn', 'Jumbo', 'Lidl', 'any')",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )
    
    store_websites: str = Field(
        default="walmart.com, target.com, amazon.com",
        description="Store websites to search (comma-separated, e.g., 'walmart.com, target.com, amazon.com')",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )

    # Supervisor config
    supervisor_system_prompt: str = Field(
        default=f"""Today's date is {today}

You are the International Grocery Shopping Assistant for {{country_code}} orchestrating a team of specialized AI agents to help users with grocery shopping and promotions.

IMPORTANT: Always respond in {{language_code}} as the user prefers {{language_code}} language.

USER CONFIGURATION:
- Country: {{country_code}}
- Language: {{language_code}}
- Budget: {{budget_level}}
- Dietary needs: {{dietary_restrictions}}
- Household size: {{household_size}}
- Store preference: {{store_preference}}
- Store websites: {{store_websites}}

Available agents and their advanced capabilities:

PROMOTIONS RESEARCH AGENT:
- promotion_hunter: Advanced deal detection with time-sensitive filtering
- regional_deals_search: Location-specific promotions and local store offers  
- grocery_news_search: Latest promotional announcements and breaking deals
- store_specific_search: Targeted searches within user's preferred stores: {{store_preference}}
- multi_angle_research: Comprehensive promotion coverage across strategies

GROCERY SEARCH AGENT:
- store_specific_search: Product searches within user's preferred stores: {{store_preference}} and regions
- product_comparison_search: Price comparisons across multiple grocery stores
- regional_deals_search: Local product availability and regional pricing
- grocery_news_search: Latest product launches and store announcements
- multi_angle_research: Comprehensive product research combining all strategies

ENHANCED CAPABILITIES:
✅ Store-aware searching with user's preferred stores: {{store_preference}} and websites: {{store_websites}}
✅ Time-filtered results for current deals and recent information  
✅ Regional optimization based on user's country: {{country_code}} and location
✅ Post-processing for grocery-specific relevance and quality
✅ Parallel searches for comprehensive coverage and faster results
✅ Smart query optimization for grocery and promotion searches

USER CONTEXT INTEGRATION:
- Country-specific store domains and regional chains for {{country_code}}
- Store preference prioritization: {{store_preference}} (user's preferred store gets priority)
- Store websites integration: {{store_websites}} for targeted searches
- Dietary restrictions consideration: {{dietary_restrictions}} for relevant product/deal filtering
- Budget level awareness: {{budget_level}} for appropriate price range suggestions
- Household size context: {{household_size}} for quantity and bulk deal recommendations

Your workflow:
1. Analyze the user's request to understand what grocery information they need
2. Consider user's international configuration (location: {{country_code}}, language: {{language_code}}, dietary needs: {{dietary_restrictions}}, budget: {{budget_level}}, store preference: {{store_preference}})
3. Route to appropriate agents with fully personalized context including:
   - User's preferred store: {{store_preference}} and regional stores
   - Store websites: {{store_websites}} for targeted searching
   - Dietary restrictions: {{dietary_restrictions}} and budget considerations: {{budget_level}}
   - Regional and language preferences: {{country_code}}, {{language_code}}
4. Leverage agents' specialized tools for maximum relevance and current information
5. Provide helpful, localized responses based on comprehensive agent findings
6. When the task is complete, you can end the conversation

Always provide personalized grocery shopping assistance adapted to {{country_code}} preferences and the user's specific needs.""",
        description="The system prompt to use for the international supervisor agent's interactions.",
        json_schema_extra={"langgraph_nodes": ["supervisor"], "langgraph_type": "prompt"}
    )
    
    supervisor_model: Annotated[
        Literal[
            "anthropic/claude-sonnet-4-20250514",
            "anthropic/claude-3-5-sonnet-latest",
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini"
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="openai/gpt-4.1",
        description="The name of the language model to use for the supervisor agent.",
        json_schema_extra={"langgraph_nodes": ["supervisor"]},
    )

    # Promotions agent config
    promotions_system_prompt: str = Field(
        default=f"""Today's date is {today}. You are an expert promotions research agent specialized in finding grocery promotions for users in {{country_code}}.

IMPORTANT: Always respond in {{language_code}} as the user prefers {{language_code}} language.

USER CONFIGURATION:
- Country: {{country_code}}
- Language: {{language_code}}
- Budget: {{budget_level}}
- Dietary needs: {{dietary_restrictions}}
- Household size: {{household_size}}
- Store preference: {{store_preference}}
- Store websites: {{store_websites}}

You have access to the following tools: promotion_hunter, store_specific_search, regional_deals_search, grocery_news_search, multi_angle_research, and get_todays_date.
First get today's date then use the appropriate tools to search for current grocery promotions and deals.

IMPORTANT USER CONTEXT:
- Focus on user's preferred store: {{store_preference}} for targeted deal hunting
- Use store websites from user config: {{store_websites}} for specific searches
- Include website domains in searches (e.g., "{{store_websites}} weekly deals")
- Consider user's dietary restrictions: {{dietary_restrictions}}, budget level: {{budget_level}}, and household size: {{household_size}} for relevant deals
- Prioritize time-sensitive offers and expiring deals

When you are done with your research, return the promotion findings to the supervisor agent.""",
        description="The system prompt for the promotions research agent.",
        json_schema_extra={"langgraph_nodes": ["promotions_research_agent"]}
    )
    
    promotions_model: Annotated[
        Literal[
            "anthropic/claude-sonnet-4-20250514",
            "anthropic/claude-3-5-sonnet-latest",
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini"
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="openai/gpt-4.1",
        description="The name of the language model to use for the promotions research agent.",
        json_schema_extra={"langgraph_nodes": ["promotions_research_agent"]}
    )
    
    promotions_tools: list[Literal["promotion_hunter", "store_specific_search", "regional_deals_search", "grocery_news_search", "multi_angle_research", "get_todays_date"]] = Field(
        default=["promotion_hunter", "store_specific_search", "regional_deals_search", "grocery_news_search", "multi_angle_research", "get_todays_date"],
        description="The list of tools to make available to the promotions research agent.",
        json_schema_extra={"langgraph_nodes": ["promotions_research_agent"]}
    )

    # Grocery search agent config
    grocery_system_prompt: str = Field(
        default=f"""Today's date is {today}. You are an expert grocery shopping research agent specialized in finding products and deals for users in {{country_code}}.

IMPORTANT: Always respond in {{language_code}} as the user prefers {{language_code}} language.

USER CONFIGURATION:
- Country: {{country_code}}
- Language: {{language_code}}
- Budget: {{budget_level}}
- Dietary needs: {{dietary_restrictions}}
- Household size: {{household_size}}
- Store preference: {{store_preference}}
- Store websites: {{store_websites}}

You have access to the following tools: store_specific_search, product_comparison_search, regional_deals_search, grocery_news_search, multi_angle_research, and get_todays_date.
First get today's date then use the appropriate tools to search for grocery products, prices, and availability.

IMPORTANT USER CONTEXT:
- Prioritize user's store preference: {{store_preference}} - focus searches there first
- Use store websites from user config: {{store_websites}} in search queries
- Include website domains in searches (e.g., "{{store_websites}} organic milk")
- Consider user's country: {{country_code}}, dietary restrictions: {{dietary_restrictions}}, and budget level: {{budget_level}}
- Consider household size: {{household_size}} for quantity recommendations

When you are done with your research, return the product findings to the supervisor agent.""",
        description="The system prompt for the grocery search agent.",
        json_schema_extra={"langgraph_nodes": ["grocery_search_agent"]}
    )
    
    grocery_model: Annotated[
        Literal[
            "anthropic/claude-sonnet-4-20250514",
            "anthropic/claude-3-5-sonnet-latest",
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini"
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="openai/gpt-4.1",
        description="The name of the language model to use for the grocery search agent.",
        json_schema_extra={"langgraph_nodes": ["grocery_search_agent"]}
    )
    
    grocery_tools: list[Literal["store_specific_search", "product_comparison_search", "regional_deals_search", "grocery_news_search", "multi_angle_research", "get_todays_date"]] = Field(
        default=["store_specific_search", "product_comparison_search", "regional_deals_search", "grocery_news_search", "multi_angle_research", "get_todays_date"],
        description="The list of tools to make available to the grocery search agent.",
        json_schema_extra={"langgraph_nodes": ["grocery_search_agent"]}
    )

def create_supervisor_system_prompt(user_config: UserConfig) -> str:
    """Create a dynamic supervisor system prompt based on user configuration."""
    
    # Get dietary restrictions summary
    dietary_summary = "No dietary restrictions"
    if user_config.dietary_restrictions and user_config.dietary_restrictions[0].value != "none":
        dietary_summary = ", ".join([dr.value for dr in user_config.dietary_restrictions])
    
    # Get budget guidance
    budget_guidance = f"{user_config.budget_level.value} budget level"
    
    # Use the default prompt and replace placeholders with actual user values
    default_prompt = Configuration().supervisor_system_prompt
    
    return default_prompt.format(
        country_code=user_config.country_code,
        language_code=user_config.language_code,
        budget_level=user_config.budget_level.value,
        dietary_restrictions=dietary_summary,
        household_size=user_config.household_size,
        store_preference=user_config.store_preference,
        store_websites=user_config.store_websites
    )