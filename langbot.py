# langBot

import os
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader

# Initialize Ollama
llm = Ollama(model="phi3", base_url="http://localhost:11434")

# Create a prompt template with system message and context
template = """
System: You provide short answers, and only according to the context provided. Do not include any other information.
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

# Use the model with the document content as context
response = llm.invoke(prompt.format(
    context=document_content,
    query="Describe Thorsten Stromberg"
))

print(response)