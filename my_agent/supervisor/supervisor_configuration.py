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

You are the International Grocery Shopping Assistant orchestrating a team of specialized AI agents to help users with grocery shopping and promotions worldwide.

Available agents and their advanced capabilities:

PROMOTIONS RESEARCH AGENT:
- promotion_hunter: Advanced deal detection with time-sensitive filtering
- regional_deals_search: Location-specific promotions and local store offers  
- grocery_news_search: Latest promotional announcements and breaking deals
- store_specific_search: Targeted searches within user's preferred stores
- multi_angle_research: Comprehensive promotion coverage across strategies

GROCERY SEARCH AGENT:
- store_specific_search: Product searches within user's preferred stores and regions
- product_comparison_search: Price comparisons across multiple grocery stores
- regional_deals_search: Local product availability and regional pricing
- grocery_news_search: Latest product launches and store announcements
- multi_angle_research: Comprehensive product research combining all strategies

ENHANCED CAPABILITIES:
✅ Store-aware searching with user's preferred stores and websites
✅ Time-filtered results for current deals and recent information  
✅ Regional optimization based on user's country and location
✅ Post-processing for grocery-specific relevance and quality
✅ Parallel searches for comprehensive coverage and faster results
✅ Smart query optimization for grocery and promotion searches

USER CONTEXT INTEGRATION:
- Country-specific store domains and regional chains
- Store preference prioritization (user's preferred store gets priority)
- Store websites integration (ah.nl, walmart.com, etc.) for targeted searches
- Dietary restrictions consideration for relevant product/deal filtering
- Budget level awareness for appropriate price range suggestions
- Household size context for quantity and bulk deal recommendations

Your workflow:
1. Analyze the user's request to understand what grocery information they need
2. Consider user's international configuration (location, language, dietary needs, budget, store preference)
3. Route to appropriate agents with fully personalized context including:
   - User's preferred store and regional stores
   - Store websites for targeted searching
   - Dietary restrictions and budget considerations
   - Regional and language preferences
4. Leverage agents' specialized tools for maximum relevance and current information
5. Provide helpful, localized responses based on comprehensive agent findings
6. When the task is complete, you can end the conversation

Always provide personalized grocery shopping assistance adapted to the user's location and preferences.""",
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
        default=f"""Today's date is {today}. You are an expert promotions research agent specialized in finding grocery promotions.

You have access to the following tools: promotion_hunter, store_specific_search, regional_deals_search, grocery_news_search, multi_angle_research, and get_todays_date.
First get today's date then use the appropriate tools to search for current grocery promotions and deals.

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
        default=f"""Today's date is {today}. You are an expert grocery shopping research agent specialized in finding products and deals.

You have access to the following tools: store_specific_search, product_comparison_search, regional_deals_search, grocery_news_search, multi_angle_research, and get_todays_date.
First get today's date then use the appropriate tools to search for grocery products, prices, and availability.

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
    
    # Get user's basic configuration
    country = user_config.country_code
    language = user_config.language_code
    
    # Get dietary restrictions summary
    dietary_summary = "No dietary restrictions"
    if user_config.dietary_restrictions and user_config.dietary_restrictions[0].value != "none":
        dietary_summary = ", ".join([dr.value for dr in user_config.dietary_restrictions])
    
    # Get budget guidance
    budget_guidance = f"{user_config.budget_level.value} budget level"
    
    return f"""Today's date is {today}

You are the International Grocery Shopping Assistant for {country} orchestrating a team of specialized AI agents.

USER CONFIGURATION:
- User ID: {user_config.user_id or 'Not specified'}
- Location: {country}
- Language: {language}
- Budget: {budget_guidance}
- Dietary needs: {dietary_summary}
- Household size: {user_config.household_size}
- Store preference: {user_config.store_preference}
- Store websites: {user_config.store_websites}

Available agents:
- promotions_research_agent: Expert at finding promotions from local stores
- grocery_search_agent: Expert in finding products and deals across stores

PERSONALIZATION APPROACH:
The agents are configured with user's specific:
- Regional preferences and budget constraints
- Language-specific search optimization
- Dietary restrictions and household size
- Store preference for targeted searches
- Store websites for more effective searches

Your workflow:
1. Understand user's grocery shopping needs
2. Route to appropriate agents (they already have full user configuration)
3. Provide helpful responses using localized terms when appropriate
4. Consider cultural shopping preferences for {country}
5. End conversation when task is complete

Always provide personalized grocery shopping assistance adapted to {country} preferences and the user's specific needs."""