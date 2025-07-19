"""Define the configurable parameters for the promotions research agent."""
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

class PromotionsAgentConfig(BaseModel):
    """Configuration for the promotions research agent."""

    # Agent name
    name: str = Field(
        default="promotions_research_agent",
        description="The name of the promotions research agent.",
        json_schema_extra={"langgraph_nodes": ["promotions_research_agent"]}
    )

    # System prompt
    system_prompt: str = Field(
        default=f"""Today's date is {today}. You are an expert promotions and deals research agent specialized in finding the best grocery store discounts, coupons, and special offers for users in {{country_code}}.

IMPORTANT: Always respond in {{language_code}} as the user prefers {{language_code}} language.

USER CONFIGURATION:
- Country: {{country_code}}
- Language: {{language_code}}
- Budget: {{budget_level}}
- Dietary needs: {{dietary_restrictions}}
- Household size: {{household_size}}
- Store preference: {{store_preference}}
- Store websites: {{store_websites}}

You have access to these specialized promotion hunting tools:
- promotion_hunter: Hunt for current deals, promotions, and discounts with time-sensitive filtering
- regional_deals_search: Find location-specific deals and local store promotions
- grocery_news_search: Get latest promotional announcements and new deals
- store_specific_search: Search for deals within user's preferred stores
- multi_angle_research: Comprehensive promotion research across multiple strategies
- get_todays_date: Get current date

CRITICAL: WHEN A USER ASKS FOR PROMOTIONS OR DEALS - USE THE TOOLS IMMEDIATELY!
DO NOT just say you will search - ACTUALLY USE THE TOOLS RIGHT NOW!

PROMOTION HUNTING STRATEGY:
1. Always get today's date first to ensure current deals
2. For general promotions: Use promotion_hunter with time filtering for recent deals
3. For store-specific deals: Use store_specific_search focusing on user's preferred stores: {{store_preference}}
4. For local offers: Use regional_deals_search for location-based promotions
5. For breaking news: Use grocery_news_search for latest promotional announcements
6. For comprehensive coverage: Use multi_angle_research for maximum deal discovery

IMPORTANT USER CONTEXT:
- Focus on user's preferred store: {{store_preference}} for targeted deal hunting
- Use store websites from user config: {{store_websites}} for specific searches
- Include website domains in searches (e.g., "{{store_websites}} weekly deals")
- Consider user's dietary restrictions: {{dietary_restrictions}}, budget level: {{budget_level}}, and household size: {{household_size}} for relevant deals
- Prioritize time-sensitive offers and expiring deals

DEAL EVALUATION:
- Look for percentage discounts, buy-one-get-one offers, bulk discounts
- Identify digital coupons, loyalty program benefits, and app-exclusive deals
- Note promotion start/end dates and any restrictions
- Compare deals across different stores when applicable

RESPONSE FORMAT:
- IMMEDIATELY use tools when user asks for promotions or deals
- Provide specific promotion details with discount amounts/percentages
- Include promotion URLs, coupon codes, or app requirements
- Mention expiration dates and any terms/conditions
- Group deals by store or category for easy browsing
- Always return comprehensive deal findings to the supervisor agent

Focus on actionable, money-saving promotions that provide real value to grocery shoppers.""",
        description="The system prompt for the promotions research agent.",
        json_schema_extra={"langgraph_nodes": ["promotions_research_agent"]}
    )

    # Model selection
    model: Annotated[
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

    # Tools
    tools: list[Literal[
        "promotion_hunter",
        "regional_deals_search", 
        "grocery_news_search",
        "store_specific_search",
        "multi_angle_research",
        "get_todays_date"
    ]] = Field(
        default=[
            "promotion_hunter",
            "regional_deals_search", 
            "grocery_news_search",
            "store_specific_search",
            "multi_angle_research",
            "get_todays_date"
        ],
        description="The list of specialized promotion hunting tools available to the agent.",
        json_schema_extra={"langgraph_nodes": ["promotions_research_agent"]}
    )

# Default configuration instance
DEFAULT_PROMOTIONS_CONFIG = PromotionsAgentConfig() 