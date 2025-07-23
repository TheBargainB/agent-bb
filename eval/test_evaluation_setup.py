"""
Test script to validate evaluation setup before running full evaluations
"""

import requests
import json
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent  
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not available, try to load manually
    env_file = project_root / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def test_langgraph_server():
    """Test if LangGraph server is running"""
    try:
        response = requests.post("http://127.0.0.1:2024/threads",
                               headers={"Content-Type": "application/json"},
                               json={"metadata": {"test": "connection"}},
                               timeout=5)
        if response.status_code == 200:
            print("✅ LangGraph server is running")
            return True
        else:
            print(f"❌ LangGraph server returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to LangGraph server: {e}")
        return False

def test_agent_response():
    """Test basic agent response"""
    try:
        # Create thread
        thread_response = requests.post("http://127.0.0.1:2024/threads",
                                      headers={"Content-Type": "application/json"},
                                      json={"metadata": {"test": "agent_test"}})
        
        if thread_response.status_code != 200:
            print(f"❌ Failed to create thread: {thread_response.status_code}")
            return False
            
        thread_id = thread_response.json()["thread_id"]
        print(f"✅ Created test thread: {thread_id}")
        
        # Test agent with simple query
        payload = {
            "assistant_id": "09d81d39-7709-4999-b9bf-afe345f6776f",
            "input": {
                "messages": [{"role": "user", "content": "Hello, can you help me find organic apples?"}]
            }
        }
        
        response = requests.post(f"http://127.0.0.1:2024/threads/{thread_id}/runs/stream",
                               headers={"Content-Type": "application/json"},
                               json=payload,
                               stream=True,
                               timeout=30)
        
        if response.status_code == 200:
            print("✅ Agent responded successfully")
            return True
        else:
            print(f"❌ Agent request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

def test_regional_configs():
    """Test regional configurations"""
    configs = [
        {
            "name": "USA Config",
            "config": {"country_code": "US", "language_code": "en", "store_preference": "target"},
            "query": "Find organic pasta under $5"
        },
        {
            "name": "Netherlands Config", 
            "config": {"country_code": "NL", "language_code": "nl", "store_preference": "albert_heijn"},
            "query": "Ik zoek biologische pasta onder €5"
        }
    ]
    
    print("\n🌍 Testing regional configurations...")
    
    for config_test in configs:
        try:
            # Create thread
            thread_response = requests.post("http://127.0.0.1:2024/threads",
                                          headers={"Content-Type": "application/json"},
                                          json={"metadata": {"test": f"config_{config_test['name']}"}})
            
            thread_id = thread_response.json()["thread_id"]
            
            # Test with config
            payload = {
                "assistant_id": "09d81d39-7709-4999-b9bf-afe345f6776f", 
                "config": {"configurable": config_test["config"]},
                "input": {
                    "messages": [{"role": "user", "content": config_test["query"]}]
                }
            }
            
            response = requests.post(f"http://127.0.0.1:2024/threads/{thread_id}/runs/stream",
                                   headers={"Content-Type": "application/json"},
                                   json=payload,
                                   stream=True,
                                   timeout=15)
            
            if response.status_code == 200:
                print(f"✅ {config_test['name']}: Configuration working")
            else:
                print(f"❌ {config_test['name']}: Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {config_test['name']}: Error - {e}")

def test_langsmith_connection():
    """Test LangSmith API connection"""
    if not os.getenv("LANGSMITH_API_KEY"):
        print("❌ LANGSMITH_API_KEY not set")
        return False
        
    try:
        from langsmith import Client
        client = Client()
        
        # Try to list projects (simple API test)
        # This will fail gracefully if API key is invalid
        client.list_projects(limit=1)
        print("✅ LangSmith API connection working")
        return True
        
    except Exception as e:
        print(f"❌ LangSmith API test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🧪 Grocery Assistant Evaluation Setup Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test 1: LangGraph Server
    print("\n1️⃣ Testing LangGraph Server Connection...")
    if not test_langgraph_server():
        all_tests_passed = False
        
    # Test 2: Basic Agent Response  
    print("\n2️⃣ Testing Basic Agent Response...")
    if not test_agent_response():
        all_tests_passed = False
        
    # Test 3: Regional Configurations
    print("\n3️⃣ Testing Regional Configurations...")
    test_regional_configs()
    
    # Test 4: LangSmith Connection
    print("\n4️⃣ Testing LangSmith API Connection...")
    if not test_langsmith_connection():
        all_tests_passed = False
    
    # Final Result
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! Ready to run evaluations")
        print("Run: python eval/run_evaluation.py")
    else:
        print("❌ Some tests failed. Fix issues before running evaluations")
        print("\nTroubleshooting:")
        print("- Ensure LangGraph server is running: langgraph dev")
        print("- Set LANGSMITH_API_KEY environment variable")
        print("- Check network connectivity")

if __name__ == "__main__":
    main() 