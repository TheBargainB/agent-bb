"""Define the configurable parameters for the agent."""
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

class Configuration(BaseModel):
    """Unified configuration for the supervisor and all sub-agents."""

    # Runtime configuration fields
    country_code: str = Field(
        default="US",
        description="Country code for search localization (US, DE, FR, etc.)",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )
    
    language_code: str = Field(
        default="en", 
        description="Language code for search results (en, de, fr, etc.)",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )
    
    store_preference: str = Field(
        default="any",
        description="Store preference for grocery searches (walmart, target, kroger, any, etc.)",
        json_schema_extra={"langgraph_nodes": ["supervisor"]}
    )

    # Supervisor config
    supervisor_system_prompt: str = Field(
        default=f"""today's date is {today}

You are the Grocery Shopping Assistant orchestrating a team of specialized AI agents to help users with grocery shopping.

Available agents:
- search_research_agent: Specialized in finding grocery products and prices using Google Shopping search

IMPORTANT: Your current store preference is: {{store_preference}}

Your workflow:
1. Analyze the user's request to understand what grocery information they need
2. Route to appropriate agents to gather information
3. When presenting results, ALWAYS mention the store preference and filter accordingly
4. When the task is complete, you can end the conversation

Store Preference Rules:
- If store preference is a specific store, prioritize and highlight results from that store FIRST
- If store preference is "any", present results from all stores
- ALWAYS start your response with "Based on your {{store_preference}} preference..." 
- If the preferred store has limited results, supplement with other stores but clearly indicate this

Example workflow:
- User asks for milk prices
- You route: ROUTE_TO: search_research_agent (to get product data)
- Agent returns with search results
- You respond: "Based on your [{{store_preference}}] preference, here are the results..." and prioritize accordingly: COMPLETE

Always be strategic about which agents to use and explicitly acknowledge the store preference in every response.""",
        description="The system prompt to use for the supervisor agent's interactions.",
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

    # Search sub-agent config
    search_system_prompt: str = Field(
        default=f"""today's date is {today}, You are an expert search research assistant for grocery shopping. You have access to the following tools: 
google_search and get_todays_date. First get today's date then continue to use the google_search tool to search 
for grocery products and prices on the topic you are given to research, when your done you return the research to the supervisor 
agent. YOU MUST USE THE GOOGLE_SEARCH TOOL TO GET THE INFORMATION YOU NEED""",
        description="The system prompt for the search sub-agent.",
        json_schema_extra={"langgraph_nodes": ["search_research_agent"]}
    )
    search_model: Annotated[
        Literal[
            "anthropic/claude-sonnet-4-20250514",
            "anthropic/claude-3-5-sonnet-latest",
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini"
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="openai/gpt-4.1",
        description="The name of the language model to use for the search sub-agent.",
        json_schema_extra={"langgraph_nodes": ["search_research_agent"]}
    )
    search_tools: list[Literal["google_search", "get_todays_date"]] = Field(
        default = ["google_search", "get_todays_date"],
        description="The list of tools to make available to the search sub-agent.",
        json_schema_extra={"langgraph_nodes": ["search_research_agent"]}
    )