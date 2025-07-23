# 🤖 **ContainerBots**
Containerizing NLP models for chatbot and agentic purposes 

# 2 DO:
- Automate processing files: chunking and vectorizing. 
- Orchestrate containers to talk and exchange info
- Define a pipeline for tought process

# Intro: 
- The goal for this repo is to test which configuration can be **the easiest and most stable way for creating a simple LLM ai-bot and ai-agent**. 
- The current approach divides each model into its own separate container, hosting the LLM via Ollama. 
- The scripts with the logic binding the tools and properties are written in python, and running live via Flask. 
- Also to mention: we are testing the chorma-db for retrieving information from processing files. 

# 🐳 Docker useful commands: 
* <u>Instantiating a new container with Ollama:</u>
    - docker run -d --gpus=all -v $volumneNameInHost:/root/.ollama -p $port:$port --name $name ollama/ollama
* <u>Running an llm on Ollama inside a docker container:</u>
    - docker exec -it $name ollama run $model
* <u>Information about the model ran by ollama in a container:</u> 
    - docker exec -it $name ollama list


# 🖥️ AWS commands:
* sudo systemctl stop ollama
* sudo systemctl disable ollama
* unset OLLAMA_HOST: check if it is gone: env | grep OLLAMA_HOST
* export OLLAMA_HOST="http://0.0.0.0:11434"
* ollama serve: if you want it to run in the background: ollama serve > ollama.log 2>&1 &
* sudo ss -tulnp | grep 11434

# qdrant storage setup
* <u> Pulling the qdrant-db image </u>
```
docker pull qdrant
```
* <u> installing pip qdrant </u>
```
pip install qdrant-client sentence-transformers

```
* <u> Running the image </u>
```
docker run --name -d --name qdrant -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```
# chroma-db setup
* <u>Pulling the chroma-db image:</u>
```
docker pull chromadb/chroma:latest
```
* <u>Running the image:</u>
```
docker run -d --name chroma-db -p 8000:8000 -v $(pwd)/chroma_data:/chroma/chroma -e IS_PERSISTENT=TRUE -e PERSIST_DIRECTORY=/chroma/chroma chromadb/chroma:latest
```
* <u>(OPTIONAL) verifying it is running:</u> 
    - curl http://localhost:8000/api/v1/heartbeat
    - down here a simple python script to check status
```
import chromadb

# Connect to your ChromaDB instance
client = chromadb.HttpClient(host='localhost', port=8000)

# Test connection
print(client.heartbeat())

# Create a test collection
collection = client.create_collection("test_collection")
print("ChromaDB is working!")
```
