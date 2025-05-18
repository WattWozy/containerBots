from flask import Flask, request, jsonify

from langchain_community.chat_models import ChatOllama
from langchain_core.tools import tool
from typing import Annotated
from langchain.agents import AgentExecutor
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Math tool functions
@tool
def add(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Add two numbers together."""
    logger.info(f"Tool 'add' called with: {a}, {b}")
    return a + b

@tool
def subtract(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Subtract second number from first number."""
    logger.info(f"Tool 'subtract' called with: {a}, {b}")
    return a - b

@tool
def multiply(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Multiply two numbers together."""
    logger.info(f"Tool 'multiply' called with: {a}, {b}")
    return a * b

@tool
def divide(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Divide first number by second number."""
    logger.info(f"Tool 'divide' called with: {a}, {b}")
    if b == 0:
        return "Error: Division by zero"
    return a / b

def create_math_agent():
    # Configure the local model
    model = ChatOllama(
        base_url="http://localhost:11436/",
        model="llama3.1:latest",
        temperature=0.0,
        # Add some additional parameters for better performance
        stop=["Observation:"],
        timeout=120
    )

    # Create the prompt template with more specific instructions
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
         You are a specialized math calculator assistant. Your job is to perform mathematical calculations accurately.
         
         INSTRUCTIONS:
         1. Use the available tools to perform calculations.
         2. Only return the final numerical result without explanation, unless the user specifically asks for an explanation.
         3. If the query does not require any of your calculation tools, respond with "I can only help with mathematical calculations."
         4. For mathematical operations, always invoke the appropriate tool rather than calculating manually.
         
         Available tools:
         - add: Add two numbers together
         - subtract: Subtract second number from first number
         - multiply: Multiply two numbers together
         - divide: Divide first number by second number
         """),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create the agent
    tools = [add, subtract, multiply, divide]
    agent = create_react_agent(model=model, tools=tools, prompt=prompt)
    
    # Create the executor with proper error handling
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,  # Set to True during development, False in production
        handle_parsing_errors=True,
        max_iterations=5  # Prevent infinite loops
    )

# Initialize the agent once at startup
agent = create_math_agent()

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    if not data or 'input' not in data:
        return jsonify({'error': 'Invalid input format. Expected JSON with "input" field.'}), 400

    try:
        logger.info(f"Received query: {data['input']}")
        result = agent.invoke({"input": data['input']})
        logger.info(f"Agent result: {result}")
        return jsonify({'response': result['output']})
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500
    
if __name__ == '__main__':
    logger.info("Math Agent API starting up...")
    app.run(host='0.0.0.0', port=5000, debug=False)