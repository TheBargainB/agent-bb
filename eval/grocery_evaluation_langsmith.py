"""
LangSmith evaluation script for the Grocery Shopping Assistant
Evaluates memory system, regional agents (USA/Netherlands), and tool functionality
"""

import asyncio
import requests
import json
import re
import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not available, try to load manually
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

from langsmith import Client
from eval.grocery_dataset_memory import (
    examples_memory, 
    examples_regional_usa, 
    examples_regional_netherlands, 
    examples_tools
)

# Initialize LangSmith client
client = Client()

# API Configuration
LANGGRAPH_API_URL = "http://127.0.0.1:2024"
ASSISTANT_ID = "09d81d39-7709-4999-b9bf-afe345f6776f"

def create_thread():
    """Create a new thread for testing"""
    response = requests.post(f"{LANGGRAPH_API_URL}/threads", 
                           headers={"Content-Type": "application/json"},
                           json={"metadata": {"test": "evaluation"}})
    return response.json()["thread_id"]

def invoke_agent(thread_id: str, message: str, config: dict = None):
    """Invoke the grocery shopping agent with a message"""
    payload = {
        "assistant_id": ASSISTANT_ID,
        "input": {
            "messages": [{"role": "user", "content": message}]
        }
    }
    
    if config:
        payload["config"] = {"configurable": config}
    
    response = requests.post(
        f"{LANGGRAPH_API_URL}/threads/{thread_id}/runs/stream",
        headers={"Content-Type": "application/json"},
        json=payload,
        stream=True
    )
    
    # Parse streaming response to get final message
    final_message = ""
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8')
            if line_text.startswith('data: '):
                try:
                    data = json.loads(line_text[6:])
                    if 'messages' in data and data['messages']:
                        last_msg = data['messages'][-1]
                        if last_msg.get('type') == 'ai' and last_msg.get('content'):
                            final_message = last_msg['content']
                except json.JSONDecodeError:
                    continue
    
    return final_message

# =============================================================================
# TARGET FUNCTIONS (These call our agents)
# =============================================================================

def target_memory_system(inputs: dict) -> dict:
    """Test the memory system functionality"""
    thread_id = create_thread()
    response = invoke_agent(thread_id, inputs["user_query"])
    
    # Analyze response for memory indicators
    analysis = {
        "has_dietary_restrictions": any(word in response.lower() for word in ["gluten", "dairy", "allergen", "restriction"]),
        "mentions_budget": any(word in response.lower() for word in ["$", "euro", "€", "budget", "cost", "price"]),
        "references_past": any(phrase in response.lower() for phrase in ["last week", "previous", "recommended", "before"]),
        "health_conscious": any(word in response.lower() for word in ["organic", "healthy", "nutrition", "heart", "sodium"]),
        "store_specific": any(store in response.lower() for store in ["target", "walmart", "whole foods", "albert heijn", "jumbo"]),
        "response_content": response
    }
    
    return analysis

def target_regional_usa(inputs: dict) -> dict:
    """Test the USA regional agent"""
    thread_id = create_thread()
    config = inputs["config"]
    response = invoke_agent(thread_id, inputs["user_query"], config)
    
    analysis = {
        "response_language": "en" if any(word in response for word in ["the", "and", "or", "at"]) else "other",
        "mentions_target": "target" in response.lower(),
        "mentions_walmart": "walmart" in response.lower(),
        "mentions_dollar_pricing": "$" in response,
        "price_focused": any(word in response.lower() for word in ["cheap", "price", "cost", "budget", "affordable"]),
        "organic_focus": "organic" in response.lower(),
        "response_content": response
    }
    
    return analysis

def target_regional_netherlands(inputs: dict) -> dict:
    """Test the Netherlands regional agent"""
    thread_id = create_thread()
    config = inputs["config"]
    response = invoke_agent(thread_id, inputs["user_query"], config)
    
    analysis = {
        "response_language": "nl" if any(word in response for word in ["de", "het", "bij", "zijn"]) else "other",
        "mentions_albert_heijn": "albert heijn" in response.lower(),
        "mentions_jumbo": "jumbo" in response.lower(),
        "mentions_euro_pricing": "€" in response,
        "price_focused": any(word in response.lower() for word in ["goedkoop", "prijs", "kosten", "budget"]),
        "organic_focus": "biologisch" in response.lower(),
        "response_content": response
    }
    
    return analysis

def target_tools_functionality(inputs: dict) -> dict:
    """Test tool functionality"""
    thread_id = create_thread()
    response = invoke_agent(thread_id, inputs["user_query"])
    
    analysis = {
        "uses_search_tool": any(word in response.lower() for word in ["search", "find", "look", "available"]),
        "provides_specific_results": any(char.isdigit() for char in response),  # Contains numbers (prices, quantities)
        "mentions_products": any(product in response.lower() for product in ["protein", "quinoa", "apples", "bread", "pasta"]),
        "price_information": any(symbol in response for symbol in ["$", "€", "price", "cost"]),
        "detailed_response": len(response) > 100,  # Substantial response
        "response_content": response
    }
    
    return analysis

# =============================================================================
# EVALUATOR FUNCTIONS
# =============================================================================

def memory_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    """Evaluate memory system functionality"""
    score = 0
    max_score = 0
    
    # Check if dietary restrictions were detected when expected
    if "has_dietary_restrictions" in reference_outputs:
        max_score += 1
        if outputs.get("has_dietary_restrictions") == reference_outputs["has_dietary_restrictions"]:
            score += 1
    
    # Check budget awareness
    if "budget_constraint" in reference_outputs:
        max_score += 1
        if outputs.get("mentions_budget") == reference_outputs["budget_constraint"]:
            score += 1
    
    # Check health consciousness
    if "health_conscious" in reference_outputs:
        max_score += 1
        if outputs.get("health_conscious") == reference_outputs["health_conscious"]:
            score += 1
    
    # Check store preference handling
    if "should_remember_store_preference" in reference_outputs:
        max_score += 1
        if outputs.get("store_specific"):
            score += 1
    
    return {
        "key": "memory_accuracy",
        "score": score / max_score if max_score > 0 else 0
    }

def regional_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    """Evaluate regional agent functionality"""
    score = 0
    max_score = 0
    
    # Language accuracy
    if "response_language" in reference_outputs:
        max_score += 2  # Language is critical
        if outputs.get("response_language") == reference_outputs["response_language"]:
            score += 2
    
    # Store mention accuracy
    store_checks = ["mentions_target", "mentions_walmart", "mentions_albert_heijn", "mentions_jumbo"]
    for check in store_checks:
        if check in reference_outputs:
            max_score += 1
            if outputs.get(check) == reference_outputs[check]:
                score += 1
    
    # Currency/pricing format
    currency_checks = ["mentions_dollar_pricing", "mentions_euro_pricing"]
    for check in currency_checks:
        if check in reference_outputs:
            max_score += 1
            if outputs.get(check) == reference_outputs[check]:
                score += 1
    
    # Organic focus
    if "organic_focus" in reference_outputs:
        max_score += 1
        if outputs.get("organic_focus") == reference_outputs["organic_focus"]:
            score += 1
    
    return {
        "key": "regional_accuracy", 
        "score": score / max_score if max_score > 0 else 0
    }

def tools_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    """Evaluate tool functionality"""
    score = 0
    max_score = 0
    
    # Tool usage detection
    if "uses_search_tool" in reference_outputs:
        max_score += 1
        if outputs.get("uses_search_tool") == reference_outputs["uses_search_tool"]:
            score += 1
    
    # Result quality
    if "returns_results" in reference_outputs:
        max_score += 1
        if outputs.get("provides_specific_results"):
            score += 1
    
    # Product relevance
    if "product_category" in reference_outputs:
        max_score += 1
        if outputs.get("mentions_products"):
            score += 1
    
    # Price information when expected
    if "price_filter" in reference_outputs:
        max_score += 1
        if outputs.get("price_information"):
            score += 1
    
    # Response quality
    max_score += 1
    if outputs.get("detailed_response"):
        score += 1
    
    return {
        "key": "tools_accuracy",
        "score": score / max_score if max_score > 0 else 0
    }

# =============================================================================
# DATASET CREATION AND EVALUATION EXECUTION
# =============================================================================

def create_datasets():
    """Create LangSmith datasets"""
    
    datasets = [
        {
            "name": "Grocery Assistant - Memory System",
            "description": "Evaluation of Phase 3 sophisticated memory functionality",
            "examples": examples_memory
        },
        {
            "name": "Grocery Assistant - USA Regional Agent", 
            "description": "Evaluation of USA regional agent configuration",
            "examples": examples_regional_usa
        },
        {
            "name": "Grocery Assistant - Netherlands Regional Agent",
            "description": "Evaluation of Netherlands regional agent configuration", 
            "examples": examples_regional_netherlands
        },
        {
            "name": "Grocery Assistant - Tools Functionality",
            "description": "Evaluation of search and research tool capabilities",
            "examples": examples_tools
        }
    ]
    
    created_datasets = []
    for dataset_config in datasets:
        dataset_name = dataset_config["name"]
        
        # Create dataset if it doesn't exist
        if not client.has_dataset(dataset_name=dataset_name):
            dataset = client.create_dataset(
                dataset_name=dataset_name,
                description=dataset_config["description"]
            )
            # Add examples to the dataset
            client.create_examples(dataset_id=dataset.id, examples=dataset_config["examples"])
            print(f"✅ Created dataset: {dataset_name}")
        else:
            print(f"📋 Dataset already exists: {dataset_name}")
        
        created_datasets.append(dataset_name)
    
    return created_datasets

def run_evaluations(run_expt: bool = True):
    """Run all evaluations"""
    if not run_expt:
        print("❌ Evaluations skipped (set run_expt=True to execute)")
        return
    
    print("🚀 Creating datasets...")
    datasets = create_datasets()
    
    print("\n🧪 Running evaluations...")
    
    # Memory System Evaluation
    print("\n1️⃣ Evaluating Memory System...")
    memory_results = client.evaluate(
        target_memory_system,
        data="Grocery Assistant - Memory System",
        evaluators=[memory_evaluator],
        experiment_prefix="Memory System - Phase 3",
        max_concurrency=2,
    )
    
    # USA Regional Agent Evaluation  
    print("\n2️⃣ Evaluating USA Regional Agent...")
    usa_results = client.evaluate(
        target_regional_usa,
        data="Grocery Assistant - USA Regional Agent", 
        evaluators=[regional_evaluator],
        experiment_prefix="Regional Agent - USA",
        max_concurrency=2,
    )
    
    # Netherlands Regional Agent Evaluation
    print("\n3️⃣ Evaluating Netherlands Regional Agent...")
    nl_results = client.evaluate(
        target_regional_netherlands,
        data="Grocery Assistant - Netherlands Regional Agent",
        evaluators=[regional_evaluator], 
        experiment_prefix="Regional Agent - Netherlands",
        max_concurrency=2,
    )
    
    # Tools Functionality Evaluation
    print("\n4️⃣ Evaluating Tools Functionality...")
    tools_results = client.evaluate(
        target_tools_functionality,
        data="Grocery Assistant - Tools Functionality",
        evaluators=[tools_evaluator],
        experiment_prefix="Tools Functionality",
        max_concurrency=2,
    )
    
    print("\n✅ All evaluations completed!")
    print("🔍 View results in LangSmith UI:")
    print("   - Memory System evaluation")
    print("   - USA Regional Agent evaluation") 
    print("   - Netherlands Regional Agent evaluation")
    print("   - Tools Functionality evaluation")
    
    return {
        "memory": memory_results,
        "usa_regional": usa_results, 
        "netherlands_regional": nl_results,
        "tools": tools_results
    }

if __name__ == "__main__":
    # Set to True to run evaluations
    run_expt = True
    results = run_evaluations(run_expt)
    
    if results:
        print(f"\n📊 Evaluation Summary:")
        for eval_name, result in results.items():
            print(f"   {eval_name}: Completed") 