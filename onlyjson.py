from flask import Flask, request, jsonify
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Math functions
def add(a, b):
    logger.info(f"Tool 'add' called with: {a}, {b}")
    return a + b

def subtract(a, b):
    logger.info(f"Tool 'subtract' called with: {a}, {b}")
    return a - b

def multiply(a, b):
    logger.info(f"Tool 'multiply' called with: {a}, {b}")
    return a * b

def divide(a, b):
    logger.info(f"Tool 'divide' called with: {a}, {b}")
    if b == 0:
        return "Error: Division by zero"
    return a / b

# Create a mapping between tool names and functions
tool_map = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide
}

# Define tools in JSON format (OpenAI function calling format)
tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "Subtract second number from first number",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "Divide first number by second number",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    if not data or 'input' not in data:
        return jsonify({'error': 'Invalid input format. Expected JSON with "input" field.'}), 400

    try:
        user_query = data['input']
        logger.info(f"Received query: {user_query}")
        
        # Initialize conversation
        messages = [
            {"role": "system", "content": "You are a specialized math calculator assistant. Your job is to perform mathematical calculations accurately. Use the available tools to perform calculations."},
            {"role": "user", "content": user_query}
        ]
        
        # Maximum number of iterations to prevent infinite loops
        max_iterations = 5
        iterations = 0
        
        # Start conversation loop
        while iterations < max_iterations:
            iterations += 1
            
            # Send request to model
            response = requests.post(
                "http://localhost:11436/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "llama3.1",
                    "messages": messages,
                    "tools": tools,
                    "tool_choice": "auto",
                    "temperature": 0.0
                }
            )
            
            if response.status_code != 200:
                logger.error(f"Error from LLM API: {response.text}")
                return jsonify({'error': f'LLM API error: {response.text}'}), 500
            
            data = response.json()
            assistant_message = data["choices"][0]["message"]
            messages.append(assistant_message)
            
            logger.info(f"Assistant message: {assistant_message}")
            
            # Check if tool call exists
            if "tool_calls" in assistant_message:
                executed_tools = False
                for tool_call in assistant_message["tool_calls"]:
                    # Extract tool info
                    function_name = tool_call["function"]["name"]
                    function_args = json.loads(tool_call["function"]["arguments"])
                    
                    # Execute the function
                    if function_name in tool_map:
                        executed_tools = True
                        result = tool_map[function_name](**function_args)
                        
                        # Add result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "name": function_name,
                            "content": str(result)
                        })
                
                # If no tools were executed, break the loop
                if not executed_tools:
                    break
            else:
                # No more tool calls, we're done
                break
        
        # Get the final response
        final_response = assistant_message["content"] if "content" in assistant_message else "Calculation completed"
        
        return jsonify({'response': final_response})
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500
    
if __name__ == '__main__':
    logger.info("Math Agent API starting up...")
    app.run(host='0.0.0.0', port=5001, debug=False)