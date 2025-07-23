"""
LangSmith dataset structure for grocery shopping assistant evaluation.
Creates datasets for tool calls, response quality, and configuration usage.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.grocery_dataset import (
    grocery_inputs, 
    expected_tool_calls, 
    triage_outputs_list, 
    response_criteria_list,
    test_configs
)

# Dataset for tool calls evaluation
examples_tool_calls = [
    {
        "inputs": {
            "grocery_input": grocery_inputs[i],
            "test_config": test_configs[i]
        },
        "outputs": {
            "expected_tool_calls": expected_tool_calls[i],
            "test_config": test_configs[i]
        }
    }
    for i in range(len(grocery_inputs))
]

# Dataset for response quality evaluation
examples_response_quality = [
    {
        "inputs": {
            "grocery_input": grocery_inputs[i],
            "test_config": test_configs[i]
        },
        "outputs": {
            "response_criteria": response_criteria_list[i],
            "test_config": test_configs[i]
        }
    }
    for i in range(len(grocery_inputs))
]

# Dataset for configuration usage evaluation
examples_config_usage = [
    {
        "inputs": {
            "grocery_input": grocery_inputs[i],
            "test_config": test_configs[i]
        },
        "outputs": {
            "test_config": test_configs[i]
        }
    }
    for i in range(len(grocery_inputs))
]

# Dataset for triage evaluation (which agent should handle the request)
examples_triage = [
    {
        "inputs": {
            "grocery_input": grocery_inputs[i],
            "test_config": test_configs[i]
        },
        "outputs": {
            "expected_agent": triage_outputs_list[i],
            "test_config": test_configs[i]
        }
    }
    for i in range(len(grocery_inputs))
]

# Print example for verification
if __name__ == "__main__":
    print("Tool Calls Dataset Example:")
    print("Inputs:", examples_tool_calls[0]['inputs'])
    print("Outputs:", examples_tool_calls[0]['outputs'])
    print()
    
    print("Response Quality Dataset Example:")
    print("Inputs:", examples_response_quality[0]['inputs'])
    print("Outputs:", examples_response_quality[0]['outputs'])
    print()
    
    print("Config Usage Dataset Example:")
    print("Inputs:", examples_config_usage[0]['inputs'])
    print("Outputs:", examples_config_usage[0]['outputs'])
    print()
    
    print("Triage Dataset Example:")
    print("Inputs:", examples_triage[0]['inputs'])
    print("Outputs:", examples_triage[0]['outputs']) 