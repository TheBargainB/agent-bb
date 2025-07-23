"""Create all subagents using the make_graph pattern from react_agent."""
from agents.supervisor.supervisor_configuration import Configuration

from agents.react_agent.graph import make_graph
from langchain_core.runnables import RunnableConfig

# Load supervisor configuration
supervisor_config = Configuration()

async def create_subagents(configurable: dict = None):
    """Create all subagents using the make_graph pattern from react_agent."""
    
    # Use configurable values if provided, otherwise fall back to defaults
    if configurable is None:
        configurable = {}
    
    # Create finance research agent using make_graph
    finance_config = RunnableConfig(
        configurable={
            "model": configurable.get("finance_model", supervisor_config.finance_model),
            "system_prompt": configurable.get("finance_system_prompt", supervisor_config.finance_system_prompt),
            "selected_tools": configurable.get("finance_tools", supervisor_config.finance_tools),
            "name": "finance_research_agent"
        }
    )
    finance_research_agent = await make_graph(finance_config)

    # Create general research agent using make_graph  
    research_config = RunnableConfig(
        configurable={
            "model": configurable.get("research_model", supervisor_config.research_model),
            "system_prompt": configurable.get("research_system_prompt", supervisor_config.research_system_prompt),
            "selected_tools": configurable.get("research_tools", supervisor_config.research_tools),
            "name": "general_research_agent"
        }
    )
    general_research_agent = await make_graph(research_config)

    # Create writing agent using make_graph
    writing_config = RunnableConfig(
        configurable={
            "model": configurable.get("writing_model", supervisor_config.writing_model),
            "system_prompt": configurable.get("writing_system_prompt", supervisor_config.writing_system_prompt),
            "selected_tools": configurable.get("writing_tools", supervisor_config.writing_tools),
            "name": "writing_agent"
        }
    )
    writing_agent = await make_graph(writing_config)
    
    return [finance_research_agent, general_research_agent, writing_agent]


"""Define the configurable parameters for the agent."""
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

class Configuration(BaseModel):
    """Unified configuration for the supervisor and all sub-agents."""

    # Supervisor config
    supervisor_system_prompt: str = Field(
        default=f"""today's date is {today}

You are the Executive Content Director orchestrating a team of specialized AI agents to produce exceptional content for clients.

Available agents:
- finance_research_agent: Specialized in financial data research and analysis using Yahoo Finance and other financial sources
- general_research_agent: Expert at comprehensive web research on any topic using advanced search tools
- writing_agent: Professional content writer that creates final polished content in any format

Your workflow:
1. Analyze the user's request to understand what type of content they need
2. Route to appropriate research agents to gather information
3. Once you have sufficient research, route to the writing agent to create the final content
4. When the task is complete, you can end the conversation

Example workflow:
- User asks for LinkedIn post about Tesla's latest earnings
- You route: ROUTE_TO: finance_research_agent (to get Tesla financial data)
- Agent returns with research
- You route: ROUTE_TO: writing_agent (to create the LinkedIn post)
- Agent returns with final content
- You respond: COMPLETE

Always be strategic about which agents to use and in what order to produce the best possible content.""",
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

    # Finance sub-agent config
    finance_system_prompt: str = Field(
        default=f"""today's date is {today}, You are an expert finance research assistant for a digital content agency.
You have access to the following tools: finance_research, basic_research, and get_todays_date. 
First get today's date then continue. 
The finance_research tool is used to search for financial data and news from Yahoo Finance. 
The basic_research tool is used to search for general information. 
The get_todays_date tool is used to get today's date. 
When you are done with your research, return the research to the supervisor agent.""",
        description="The system prompt for the finance sub-agent.",
        json_schema_extra={"langgraph_nodes": ["finance_research_agent"]}
    )
    finance_model: Annotated[
        Literal[
            "anthropic/claude-sonnet-4-20250514",
            "anthropic/claude-3-5-sonnet-latest",
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini"
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="openai/gpt-4.1",
        description="The name of the language model to use for the finance sub-agent.",
        json_schema_extra={"langgraph_nodes": ["finance_research_agent"]}
    )
    finance_tools: list[Literal["finance_research", "advanced_research_tool", "basic_research_tool", "get_todays_date"]] = Field(
        default = ["finance_research", "basic_research_tool", "get_todays_date"],
        description="The list of tools to make available to the finance sub-agent.",
        json_schema_extra={"langgraph_nodes": ["finance_research_agent"]}
    )

    # Research sub-agent config
    research_system_prompt: str = Field(
        default=f"""today's date is {today}, You are an expert general research agent. You have access to the following tools: 
advanced_research_tool and get_todays_date. First get today's date then continue to use the advanced_research_tool tool to search 
for general information on the topic you are given to research, when your done you return the research to the supervisor 
agent. YOU MUST USE THE ADVANCED_RESEARCH_TOOL TO GET THE INFORMATION YOU NEED""",
        description="The system prompt for the research sub-agent.",
        json_schema_extra={"langgraph_nodes": ["general_research_agent"]}
    )
    research_model: Annotated[
        Literal[
            "anthropic/claude-sonnet-4-20250514",
            "anthropic/claude-3-5-sonnet-latest",
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini"
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="openai/gpt-4.1",
        description="The name of the language model to use for the research sub-agent.",
        json_schema_extra={"langgraph_nodes": ["general_research_agent"]}
    )
    research_tools: list[Literal["finance_research", "advanced_research_tool", "basic_research_tool", "get_todays_date"]] = Field(
        default = ["advanced_research_tool", "get_todays_date"],
        description="The list of tools to make available to the general research sub-agent.",
        json_schema_extra={"langgraph_nodes": ["general_research_agent"]}
    )

    # Writing sub-agent config
    writing_system_prompt: str = Field(
        default="""You are an expert writing assistant.
Your primary responsibility is to help draft, edit, and improve written content to ensure clarity, 
correctness, and engagement. You are strictly supposed to take in the content you are given and write the 
final content based on the requested format for the user, then return the final content to the supervisor agent.""",
        description="The system prompt for the writing sub-agent.",
        json_schema_extra={"langgraph_nodes": ["writing_agent"]}
    )
    writing_model: Annotated[
        Literal[
            "anthropic/claude-sonnet-4-20250514",
            "anthropic/claude-3-5-sonnet-latest",
            "openai/gpt-4.1",
            "openai/gpt-4.1-mini"
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="openai/gpt-4.1",
        description="The name of the language model to use for the research sub-agent.",
        json_schema_extra={"langgraph_nodes": ["writing_agent"]}
    )
    writing_tools: list[Literal["finance_research", "advanced_research_tool", "basic_research_tool", "get_todays_date"]] = Field(
        default = ["advanced_research_tool", "get_todays_date"],
        description="The list of tools to make available to the general research sub-agent.",
        json_schema_extra={"langgraph_nodes": ["writing_agent"]}
    )

    from langchain_core.runnables import RunnableConfig
from agents.supervisor.supervisor_configuration import Configuration
from agents.supervisor.subagents import create_subagents
from agents.utils import load_chat_model

from langgraph_supervisor import create_supervisor

# Main graph construction
async def make_supervisor_graph(config: RunnableConfig):
    # Extract configuration values directly from the config
    configurable = config.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "openai/gpt-4.1")
    supervisor_system_prompt = configurable.get("supervisor_system_prompt", "You are a helpful supervisor agent.")
    
    # Create subagents using the new async function, passing configurable values
    subagents = await create_subagents(configurable)

    # Create supervisor graph
    supervisor_graph = create_supervisor(
        agents=subagents,
        model=load_chat_model(supervisor_model),
        prompt=supervisor_system_prompt,
        config_schema=Configuration
    )

    compiled_graph = supervisor_graph.compile()
    return compiled_graph

    """Utility & helper functions."""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)
    return init_chat_model(model, model_provider=provider)