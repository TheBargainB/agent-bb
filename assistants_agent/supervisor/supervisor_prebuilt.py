from langchain_core.runnables import RunnableConfig
from assistants_agent.supervisor.supervisor_configuration import Configuration
from assistants_agent.supervisor.subagents import create_subagents
from assistants_agent.utils.utils import load_chat_model

from langgraph_supervisor import create_supervisor

# Memory imports (Phase 1: passive initialization)
from langgraph.store.memory import InMemoryStore
from assistants_agent.memory.schemas import GroceryProfile, ShoppingEpisode, SupervisorInstructions

# Main graph construction
async def make_supervisor_graph(config: RunnableConfig):
    # Extract configuration values directly from the config
    configurable = config.get("configurable", {})
    supervisor_model = configurable.get("supervisor_model", "openai/gpt-4.1")
    supervisor_system_prompt = configurable.get("supervisor_system_prompt", "You are a helpful supervisor agent.")
    
    # Phase 1: Initialize memory store passively (not used yet)
    memory_enabled = configurable.get("memory_enabled", False)
    memory_store = None
    
    if memory_enabled:
        # Initialize InMemoryStore but don't use it yet (Phase 1: passive)
        memory_store = InMemoryStore()
        print(f"🧠 Memory store initialized (enabled: {memory_enabled})")
        print(f"   Semantic: {configurable.get('memory_semantic_enabled', False)}")
        print(f"   Episodic: {configurable.get('memory_episodic_enabled', False)}")
        print(f"   Procedural: {configurable.get('memory_procedural_enabled', False)}")
    
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
    
    # Store memory instance for future phases (not used yet)
    if memory_store:
        compiled_graph._memory_store = memory_store
    
    return compiled_graph 