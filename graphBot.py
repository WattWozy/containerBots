from flask import Flask, request, jsonify

from langchain_community.chat_models import ChatOllama
from langchain_core.tools import tool
from typing import Annotated
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


app = Flask(__name__)

# Math tool functions
@tool
def add(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Add two numbers together."""
    return a + b

@tool
def subtract(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Subtract second number from first number."""
    return a - b

@tool
def multiply(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Multiply two numbers together."""
    print("Multiplying:", a, b)
    return a * b

@tool
def divide(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Divide first number by second number."""
    if b == 0:
        return "Error: Division by zero"
    return a / b

def create_math_agent():
    # Configure the local Gemma3-4b model
    model = ChatOllama(
        base_url="http://localhost:11434/",
        model="phi3", #gemma3:4b, phi3:3.8b ....
        temperature=0.0
    )

    # Create the prompt template with more specific instructions
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
         WHO YOU ARE: You are a helpful math machine. 
         
         ALWAYS DO: Use the available tools to perform calculations.
         ONLY USE: Only use the tools to perform the calculation and return the result.
         ALWAYS ANSWER: The result retrieved from the tool you used. 
         ONLY ANSWER: The result of the calculation.
         
        If the query does not require a calculation, respond with "I cannot help with that." 
        Do not explain your reasoning or show your work unless specifically asked."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    #print("Prompt template created:", prompt)  # Debugging line

    # Create the agent
    tools = [add, subtract, multiply, divide]
    agent = create_openai_tools_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)  # Set verbose to False


# Test the agent
@app.route('/query', methods=['POST'])
def query():
    agent = create_math_agent()
    data = request.get_json()
    if not data or 'input' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # Test addition
    
    print(data['input'])
    result = agent.invoke({"input": data['input']})

    return jsonify({'response': result['output']})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    
    # Test subtraction
    #result = agent.invoke({"input": "What is 10 minus 7?"})
    #print("\nSubtraction result:", result["output"])
    
    # Test multiplication
    #result = agent.invoke({"input": "What is 4 times 2?"})
    #print("\nMultiplication result:", result["output"])
    
    # Test division
    #result = agent.invoke({"input": "What is 8 divided by 4?"})
    #print("\nDivision result:", result["output"])
