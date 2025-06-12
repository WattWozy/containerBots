containerBots
containerizing nlp models for chatbot and agentic purposes

# DONE:

* Started a container
* Pulled and ran Ollama on the container
* Told ollama to run phi3
* Give the LLM some tools
* Give the LLM specific context
* Give the LLM some system prompts
* Ran a ec2-instance
* Installed python on the ec2-instance
* Installed docker on the ec2-instance
* Installed docker on the container on the ec2-instance
* Failed to run a tool-capable model on that docker-ollama-ec2-instance
* Wrote a python flask app to listen at requests on a port
* Able to send and receive info from the flask app on the ec2-machine

# 2DO:
* Tink-data-processing


#FURTHER DOWN:
Orchestrate containers to talk and exchange info
Define a pipeline for tought process

# useful
* instantiating a new container with Ollama: docker run -d --gpus=all -v $volumneNameInHost:/root/.ollama -p $port:$port --name $name ollama/ollama
* running an llm on Ollama inside a docker container: docker exec -it $name ollama run $model
* information about the model ran by ollama in a container: docker exec -it $name ollama list

# chroma-db setup
* pulling the chroma-db image: docker pull chromadb/chroma:latest
* running the image: docker run -d --name chroma-db -p 8000:8000 -v $(pwd)/chroma_data:/chroma/chroma -e IS_PERSISTENT=TRUE -e PERSIST_DIRECTORY=/chroma/chroma chromadb/chroma:latest
* (OPTIONAL) verifying it is running: curl http://localhost:8000/api/v1/heartbeat
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
