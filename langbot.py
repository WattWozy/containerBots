# langBot

import os

from langchain_ollama import OllamaLLM
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader

# Initialize Ollama
llm = OllamaLLM(
    model="phi3:3.8b", #gemma3:4b works, phi3:3.8b 
    base_url="http://localhost:11434/"
)

# Create a prompt template with system message and context
template = """
System: You are a kind assistant. Answer politely.
Context: {context}
User: {query}
"""

prompt = PromptTemplate(
    input_variables=["context", "query"],
    template=template,
)

# Load documents
def load_documents(file_path):
    if file_path.endswith('.txt'):
        loader = TextLoader(file_path)
    elif file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    
    return loader.load()

#load documents from a directory
def load_documents_from_directory(directory_path):
    loader = DirectoryLoader(
        directory_path, 
        glob="**/*.txt",  # Load all .txt files, including in subdirectories
        loader_cls=TextLoader
    )
    return loader.load()

# Example: Load a single document
# Get the absolute path
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
file_path = os.path.join(script_dir, "..", "assets", "test.txt")
file_path = os.path.abspath(file_path)  # Normalize the path

documents = load_documents(file_path)
document_content = "\n\n".join([doc.page_content for doc in documents])


context_string = """
    Torsten strömberg is a professor of computer science at the University of California, Berkeley. He is known for his work in the field of artificial intelligence and machine learning. He has published numerous papers and has been involved in various research projects related to these fields.
    He has also been a speaker at several conferences and has received several awards for his contributions to the field.
    He is also known for his work in the field of natural language processing and has been involved in various projects related to this area.
    He has also been a speaker at several conferences and has received several awards for his contributions to the field.
    He is 170cm tall and weighs 70kg. He is married and has two children.
    He enjoys hiking, reading, and spending time with his family. He is also an avid traveler and has visited several countries around the world.     
"""

# Use the model with the document content as context
response = llm.invoke(prompt.format(
    context=context_string,
    query="Describe his appearance",
))

print(response)