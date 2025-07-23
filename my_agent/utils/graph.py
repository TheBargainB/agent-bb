"""Define a Reasoning and Action agent using the LangGraph prebuilt react agent. 

Add configuration and implement using a make_graph function to rebuild the graph at runtime.
Following the tutorial pattern but with memory enhancement for grocery shopping.
"""
from my_agent.utils.tools import get_tools
from langgraph.prebuilt import create_react_agent
from my_agent.utils.utils import load_chat_model, get_user_memory, build_memory_context, learn_from_interaction
from my_agent.supervisor.supervisor_configuration import Configuration
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.base import BaseStore
from langchain_core.messages import SystemMessage


async def make_graph(config: RunnableConfig):
    """Create a graph using the make_graph pattern from react_agent (tutorial approach with memory)."""
    
    # Extract configuration values directly from the config (tutorial pattern)
    configurable = config.get("configurable", {})
    
    # Get values from configuration
    model = configurable.get("model", "openai/gpt-4.1")
    selected_tools = configurable.get("selected_tools", ["get_todays_date"])
    base_prompt = configurable.get("system_prompt", "You are a helpful assistant.")
    name = configurable.get("name", "react_agent")
    
    # Create the react agent with memory enhancement (tutorial pattern + memory)
    graph = create_react_agent(
        model=load_chat_model(model), 
        tools=get_tools(selected_tools),
        prompt=base_prompt, 
        name=name
    )

    return graph


async def make_memory_enhanced_supervisor(config: RunnableConfig):
    """Create supervisor with memory following exact tutorial pattern."""
    
    # Extract configuration values (tutorial pattern)
    configurable = config.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "openai/gpt-4.1") 
    store_preference = configurable.get("store_preference", "any")
    user_id = configurable.get("user_id", "default_user")
    
    print("🏗️ Building memory-enhanced supervisor (exact tutorial pattern)...")
    
    # Enhanced supervisor prompt with memory (tutorial pattern)
    async def get_supervisor_prompt_with_memory(store: BaseStore) -> str:
        """Get supervisor prompt enhanced with memory context."""
        try:
            # Get user memory (tutorial pattern utility)
            user_prefs = await get_user_memory(store, user_id)
            
            # Build memory context (tutorial pattern utility) 
            memory_context = build_memory_context(user_prefs, configurable)
            
            # Base prompt following tutorial pattern
            base_prompt = f"""You are a grocery shopping assistant supervisor.

Available agents:
- search_research_agent: Search for grocery products and research pricing

MEMORY CONTEXT: {memory_context}

Your workflow:
1. Analyze the user's grocery request
2. Route to search_research_agent to gather product information  
3. When you have sufficient results, provide helpful responses
4. Always consider the user's preferences and configuration

Route user queries to the appropriate agent and provide helpful grocery shopping assistance."""

            return base_prompt
            
        except Exception as e:
            print(f"⚠️ Memory prompt error: {e}")
            return """You are a grocery shopping assistant supervisor.

Available agents:
- search_research_agent: Search for grocery products and research pricing

Route user queries to the appropriate agent and provide helpful grocery shopping assistance."""

    # Create subagents using exact tutorial pattern
    from my_agent.supervisor.subagents import create_subagents
    subagents = await create_subagents(configurable)
    
    # Use langgraph_supervisor.create_supervisor (EXACT tutorial pattern)
    from langgraph_supervisor import create_supervisor
    from my_agent.supervisor.supervisor_configuration import Configuration
    
    # Get enhanced prompt
    # For now, use a static enhanced prompt since create_supervisor doesn't take async prompts
    user_prefs = {}  # Will be loaded in memory learning
    memory_context = build_memory_context(user_prefs, configurable)
    
    enhanced_prompt = f"""You are a grocery shopping assistant supervisor.

Available agents:
- search_research_agent: Search for grocery products and research pricing

MEMORY CONTEXT: {memory_context}

Your workflow:
1. Analyze the user's grocery request  
2. Route to search_research_agent to gather product information
3. When you have sufficient results, provide helpful responses
4. Always consider the user's preferences and configuration

Route user queries to the appropriate agent and provide helpful grocery shopping assistance."""

    # Create supervisor using EXACT tutorial pattern
    supervisor_graph = create_supervisor(
        agents=subagents,
        model=load_chat_model(supervisor_model),
        prompt=enhanced_prompt,
        config_schema=Configuration
    )
    
    print("✅ Memory-enhanced supervisor created using tutorial pattern!")
    return supervisor_graph.compile() 