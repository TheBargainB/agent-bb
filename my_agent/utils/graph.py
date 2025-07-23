"""Define a Reasoning and Action agent using the LangGraph prebuilt react agent. 

Add configuration and implement using a make_graph function to rebuild the graph at runtime.
"""
from my_agent.utils.tools import get_tools
from langgraph.prebuilt import create_react_agent
from my_agent.utils.utils import load_chat_model

from my_agent.supervisor.supervisor_configuration import Configuration
from langchain_core.runnables import RunnableConfig





async def make_graph(config: RunnableConfig):
    """Create a graph using the make_graph pattern from react_agent (tutorial approach)."""
    
    # Extract configuration values directly from the config
    configurable = config.get("configurable", {})
    
    # Get values from configuration
    llm = configurable.get("model", "openai/gpt-4.1")
    selected_tools = configurable.get("selected_tools", ["get_todays_date"])
    prompt = configurable.get("system_prompt", "You are a helpful assistant.")
    name = configurable.get("name", "react_agent")
    

    
    # Get the actual tool functions based on selected_tools
    tools = get_tools(selected_tools)
    
    # Create the react agent with proper tool binding
    # create_react_agent already returns a compiled graph, so no need to call .compile()
    # Don't use config_schema to avoid hardcoded defaults overriding runtime config
    graph = create_react_agent(
        model=load_chat_model(llm), 
        tools=tools,
        prompt=prompt, 
        name=name
    )

    return graph 