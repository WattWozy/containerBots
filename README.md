containerBots
containerizing nlp models for chatbot and agentic purposes

#DONE:

Started a container
pulled and ran Ollama on the container
told ollama to run phi3
give the LLM some tools
give the LLM specific context
give the LLM some system prompts
ran a ec2-instance
installed python on the ec2-instance
installed docker on the ec2-instance
installed docker on the container on the ec2-instance
failed to run a tool-capable model on that docker-ollama-ec2-instance
wrote a python flask app to listen at requests on a port
able to send and receive info from the flask app on the ec2-machine

#2DO:
tink-data-processing


#FURTHER DOWN:
Orchestrate containers to talk and exchange info
Define a pipeline for tought process

# useful
* instantiating a new container with Ollama: docker run -d --gpus=all -v $volumneNameInHost:/root/.ollama -p $port:$port --name $name ollama/ollama
* running an llm on Ollama inside a docker container: docker exec -it $name ollama run $model
* information about the model ran by ollama in a container: docker exec -it $name ollama list

# GPT chat: 
1. LLM & Embedding Model Separation
LLMs like phi3 or gemma are for generating answers, not embeddings.

Use dedicated embedding models (e.g., all-MiniLM-L6-v2, text-embedding-ada-002) for vectorization.

LangChain supports both local and hosted embedding models.

2. Document Chunking
Embedding models do not chunk documents — you must do it beforehand.

Use LangChain’s RecursiveCharacterTextSplitter to split documents into overlapping text chunks for better retrieval quality.

3. Vector Database Integration
Store embedded chunks in a vector store (e.g., FAISS, Chroma, Pinecone).

Chunks are indexed independently and retrieved via similarity search.

4. Multi-Granularity Chunking Strategy
You can chunk the same document multiple ways:

Short chunks → more literal, focused matching

Longer chunks → broader, more contextual understanding

Tag each chunk with metadata (chunk_type: "short" or "long") and store in the same vector DB.

This enables flexible querying depending on the granularity needed.

5. End-to-End Flow
Load document(s)

Split into chunks (short/long)

Embed chunks using a SentenceTransformer model

Store in FAISS or another vector DB

On query:

Perform similarity search

Pass top-k relevant chunks to LLM as context

Generate answer using OllamaLLM

