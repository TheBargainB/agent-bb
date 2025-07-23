"""
Main agent definition for the grocery shopping assistant.
This file exposes the compiled supervisor graph for LangGraph deployment.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain_core.runnables import RunnableConfig
from my_agent.supervisor.supervisor_configuration import Configuration
from my_agent.supervisor.subagents import create_subagents
from my_agent.utils.utils import load_chat_model

from langgraph_supervisor import create_supervisor

# Main graph construction function
async def make_supervisor_graph(config: RunnableConfig):
    """Create the supervisor graph with all specialized agents (tutorial approach)."""
    # Extract configuration values directly from the config
    configurable = config.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "openai/gpt-4.1")
    supervisor_system_prompt = configurable.get("supervisor_system_prompt", "You are a helpful supervisor agent.")
    
    # Create subagents using the async function, passing configurable values
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

# Export the graph for LangGraph configuration
graph = make_supervisor_graph 