# langBot

from langchain.llms import Ollama
from langchain.prompts import PromptTemplate

# Initialize Ollama
llm = Ollama(model="phi3-mini", base_url="http://localhost:11434")

# Create a prompt template with system message and context
template = """
System: You are a helpful AI assistant with expertise in science and technology.
Context: {context}
User: {query}
"""

prompt = PromptTemplate(
    input_variables=["context", "query"],
    template=template,
)

# Use the model with context
response = llm.invoke(prompt.format(
    context="Important context document content here...",
    query="What can you tell me about this information?"
))

print(response)