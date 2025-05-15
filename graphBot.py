from langchain_community.chat_models import ChatOllama
from langchain_core.tools import tool
from typing import Annotated
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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

    return a * b

@tool
def divide(a: Annotated[float, "First number"], b: Annotated[float, "Second number"]) -> float:
    """Divide first number by second number."""
    if b == 0:
        return "Error: Division by zero"
    return a / b

def create_math_agent():
    # Configure the local Phi-3 model
    model = ChatOllama(
        base_url="http://localhost:11434/",
        model="phi3",
        temperature=0.0
    )

    # Create the prompt template with more specific instructions
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful math machine. Use the available tools to perform calculations.
        Be concise in your responses. Only use the tools to perform the calculation and return the result.
        Do not explain your reasoning or show your work unless specifically asked."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    tools = [add, subtract, multiply, divide]
    agent = create_openai_tools_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)  # Set verbose to False

# Test the agent
if __name__ == "__main__":
    # Test addition
    agent = create_math_agent()
    result = agent.invoke({"input": "What is 5 plus 3?"})
    print("\nAddition result:", result["output"])
    
    # Test subtraction
    result = agent.invoke({"input": "What is 10 minus 7?"})
    print("\nSubtraction result:", result["output"])
    
    # Test multiplication
    result = agent.invoke({"input": "What is 4 times 2?"})
    print("\nMultiplication result:", result["output"])
    
    # Test division
    result = agent.invoke({"input": "What is 8 divided by 4?"})
    print("\nDivision result:", result["output"])
