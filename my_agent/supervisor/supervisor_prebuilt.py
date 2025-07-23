from langchain_core.runnables import RunnableConfig
from my_agent.supervisor.supervisor_configuration import Configuration
from my_agent.supervisor.subagents import create_subagents
from my_agent.utils.utils import load_chat_model
from my_agent.utils.memory import (
    get_sophisticated_user_memory, 
    build_sophisticated_memory_context, 
    sophisticated_learning_from_interaction
)

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.store.base import BaseStore
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import Literal


# Phase 3: Sophisticated Memory-Enabled Supervisor Node
async def sophisticated_memory_supervisor_node(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Phase 3 supervisor with sophisticated memory intelligence, insights, and proactive recommendations."""
    
    # Extract configuration values
    configurable = config.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "openai/gpt-4.1")
    store_preference = configurable.get("store_preference", "any")
    user_id = configurable.get("user_id", "default_user")
    
    print("🏗️ Building Phase 3 sophisticated memory-enhanced supervisor graph...")
    
    # Get sophisticated memory with insights
    user_prefs, memory_insights = await get_sophisticated_user_memory(store, user_id)
    
    # Get the current user query
    latest_message = state["messages"][-1] if state["messages"] else None
    user_query = latest_message.content if latest_message else ""
    
    # Build sophisticated memory context with insights and predictions
    memory_context = await build_sophisticated_memory_context(user_prefs, memory_insights, user_query)
    
    # Use Configuration class for base prompt
    supervisor_config = Configuration()
    base_prompt = supervisor_config.supervisor_system_prompt.format(store_preference=store_preference)
    
    # Phase 3: Enhanced prompt with sophisticated memory and insights
    sophisticated_prompt = base_prompt + f"""

SOPHISTICATED MEMORY INTELLIGENCE:
{memory_context}

ADVANCED CAPABILITIES:
- You have access to deep user insights, behavioral patterns, and confidence scores
- Use proactive recommendations when confidence is high (>0.8)
- Apply temporal context for time-sensitive suggestions
- Leverage cross-domain learning patterns for better personalization
- Validate recommendations against user's dietary restrictions and preferences

INSIGHT-DRIVEN DECISION MAKING:
- When insights suggest specific actions, incorporate them into your routing decisions
- Use confidence scores to weight the importance of different preferences
- Apply temporal patterns to suggest contextually appropriate products
- Consider cross-category patterns for holistic recommendations

MEMORY LEARNING:
- This interaction will automatically update your understanding of the user
- Memory validation and correction happens automatically
- Confidence scores adjust based on interaction success
- Cross-domain patterns strengthen with each interaction"""

    # Create subagents (await the async function)
    subagents = await create_subagents(configurable)
    
    # Load and configure supervisor model
    supervisor_llm = load_chat_model(supervisor_model)
    
    # Bind tools (subagents)
    supervisor_runnable = supervisor_llm.bind_tools(
        [{"type": "function", "function": subagent["function"]} for subagent in subagents]
    )
    
    # Run the sophisticated supervisor
    messages_for_llm = [SystemMessage(content=sophisticated_prompt)] + state["messages"]
    
    response = await supervisor_runnable.ainvoke(messages_for_llm)
    
    # Phase 3: Advanced learning from interaction
    if latest_message and response.content:
        await sophisticated_learning_from_interaction(
            store=store,
            user_query=user_query,
            supervisor_response=response.content,
            config=configurable,
            insights=memory_insights
        )
    
    print("✅ Phase 3 sophisticated memory-enhanced supervisor graph created!")
    
    # Handle tool calls
    if response.tool_calls:
        return {
            "messages": [response],
            "next": response.tool_calls[0]["name"]
        }
    else:
        return {
            "messages": [response],
            "next": END
        }


# Enhanced graph construction with Phase 3 memory capabilities
async def make_supervisor_graph(config: RunnableConfig):
    """Create Phase 3 sophisticated memory-enhanced supervisor graph."""
    
    # Extract configurable values
    configurable = config.get("configurable", {})
    
    # Create subagents (await the async function)
    subagents = await create_subagents(configurable)
    
    # Initialize graph
    workflow = StateGraph(MessagesState)
    
    # Add sophisticated memory supervisor node
    workflow.add_node("supervisor", sophisticated_memory_supervisor_node)
    
    # Add subagent nodes
    for subagent in subagents:
        workflow.add_node(subagent["name"], subagent["node"])
    
    # Define routing logic - all agents route back to supervisor
    def route_after_subagent(state: MessagesState) -> Literal["supervisor"]:
        return "supervisor"
    
    # Set up edges
    workflow.add_edge(START, "supervisor")
    
    for subagent in subagents:
        workflow.add_edge(subagent["name"], "supervisor")
    
    # Add conditional edges from supervisor to subagents
    workflow.add_conditional_edges(
        "supervisor",
        lambda state: state.get("next", END),
        {subagent["name"]: subagent["name"] for subagent in subagents} | {END: END}
    )
    
    # Compile the graph - store will be injected automatically by platform
    return workflow.compile()


# Main graph construction
graph = make_supervisor_graph