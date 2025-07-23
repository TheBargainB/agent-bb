# Grocery Shopping Assistant - LangSmith Evaluations

This directory contains comprehensive evaluations for the Grocery Shopping Assistant system, focusing on **Phase 3 Sophisticated Memory**, **Regional Agents** (USA & Netherlands priority), and **Tool Functionality**.

## 🎯 Evaluation Coverage

### 1. **Memory System Evaluation** (`Phase 3 Sophisticated Memory`)
- **Dataset:** `examples_memory` in `grocery_dataset_memory.py`
- **Tests:**
  - Dietary restrictions detection (gluten-free, dairy-free, etc.)
  - Budget awareness and constraint handling
  - Health-conscious recommendations
  - Store preference memory
  - Past interaction references

### 2. **Regional Agent Evaluation** 
#### **USA Agent**
- **Configuration:** `country_code: "US"`, `language_code: "en"`, `store_preference: "target/walmart"`
- **Tests:**
  - English language responses
  - Dollar pricing format ($)
  - Target/Walmart store mentions
  - US-specific product recommendations

#### **Netherlands Agent** 
- **Configuration:** `country_code: "NL"`, `language_code: "nl"`, `store_preference: "albert_heijn/jumbo"`
- **Tests:**
  - Dutch language responses
  - Euro pricing format (€)
  - Albert Heijn/Jumbo store mentions  
  - Netherlands-specific product recommendations

### 3. **Tool Functionality Evaluation**
- **Dataset:** `examples_tools` in `grocery_dataset_memory.py`
- **Tests:**
  - Search tool usage and accuracy
  - Research capabilities
  - Price comparison functionality
  - Product categorization
  - Response quality and detail

## 🚀 Quick Start

### Prerequisites
1. **LangGraph Server Running:**
   ```bash
   langgraph dev
   ```
   (Should be running on `http://127.0.0.1:2024`)

2. **LangSmith API Key:**
   ```bash
   export LANGSMITH_API_KEY="your-langsmith-api-key"
   ```

3. **Dependencies:**
   ```bash
   pip install langsmith requests
   ```

### Run Evaluation Tests

1. **Validate Setup First:**
   ```bash
   python eval/test_evaluation_setup.py
   ```
   This tests:
   - LangGraph server connectivity
   - Basic agent responses
   - Regional configuration functionality
   - LangSmith API connection

2. **Run Full Evaluations:**
   ```bash
   python eval/run_evaluation.py
   ```

## 📊 Evaluation Metrics

### Memory System Metrics
- **Dietary Restriction Detection:** Accuracy in identifying user dietary needs
- **Budget Awareness:** Correctly handling price constraints
- **Health Consciousness:** Organic/healthy product prioritization
- **Store Preference Memory:** Remembering and applying store preferences

### Regional Agent Metrics
- **Language Accuracy:** Correct language in responses (EN/NL)
- **Store Integration:** Appropriate store mentions
- **Currency Format:** Correct pricing format ($/€)
- **Cultural Localization:** Region-appropriate recommendations

### Tool Functionality Metrics
- **Tool Usage:** Correct tool selection for queries
- **Result Quality:** Specific, actionable results
- **Product Relevance:** Accurate product categorization
- **Information Completeness:** Comprehensive responses

## 📈 Results Viewing

After running evaluations, view results in:
- **LangSmith UI:** `https://smith.langchain.com`
- **Experiments:** Look for experiment prefixes:
  - `Memory System - Phase 3`
  - `Regional Agent - USA`
  - `Regional Agent - Netherlands` 
  - `Tools Functionality`

## 🛠️ Adding New Evaluations

### 1. Add Test Cases
Edit `grocery_dataset_memory.py`:
```python
new_examples = [
    {
        "inputs": {"user_query": "Your test query", "config": {...}},
        "outputs": {"expected_behavior": True, ...}
    }
]
```

### 2. Create Target Function
In `grocery_evaluation_langsmith.py`:
```python
def target_new_functionality(inputs: dict) -> dict:
    # Call your agent
    response = invoke_agent(thread_id, inputs["user_query"], inputs.get("config"))
    
    # Analyze response
    return {"analysis_result": analysis}
```

### 3. Create Evaluator
```python
def new_functionality_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    # Compare outputs vs reference_outputs
    score = calculate_score(outputs, reference_outputs)
    return {"key": "new_functionality_accuracy", "score": score}
```

### 4. Add to Evaluation Runner
```python
new_results = client.evaluate(
    target_new_functionality,
    data="Your Dataset Name",
    evaluators=[new_functionality_evaluator],
    experiment_prefix="New Functionality Test",
    max_concurrency=2,
)
```

## 🔧 Troubleshooting

### Common Issues

1. **"Cannot connect to LangGraph server"**
   - Ensure `langgraph dev` is running
   - Check port 2024 is not blocked

2. **"LANGSMITH_API_KEY not set"**
   - Set environment variable: `export LANGSMITH_API_KEY="..."`
   - Get API key from LangSmith dashboard

3. **"Agent request failed"**
   - Verify assistant ID matches your deployment
   - Check LangGraph server logs for errors

4. **"Import error"**
   - Install dependencies: `pip install langsmith requests`
   - Ensure you're in the project root directory

### Debug Mode
For detailed debugging, edit `grocery_evaluation_langsmith.py` and add:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 File Structure

```
eval/
├── README.md                          # This file
├── grocery_dataset_memory.py          # Test datasets
├── grocery_evaluation_langsmith.py    # Main evaluation logic
├── run_evaluation.py                  # Simple runner script
├── test_evaluation_setup.py           # Setup validation
└── utils.py                          # Utility functions (if needed)
```

## 🌍 Regional Priority

As requested, evaluations prioritize:
1. **USA** (Target, Walmart stores)
2. **Netherlands** (Albert Heijn, Jumbo stores)

Additional regions can be added by extending the datasets and configurations.

---

**Ready to evaluate?** Run `python eval/test_evaluation_setup.py` first! 🚀