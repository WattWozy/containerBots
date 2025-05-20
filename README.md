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

