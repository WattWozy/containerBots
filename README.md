containerBots
containerizing nlp models for chatbot and agentic purposes

#DONE:

Started a container
pulled and ran Ollama on the container
told ollama to run phi3

#2DO:

give the LLM some tools
give the LLM specific context
give the LLM some system prompts

#FURTHER DOWN:

Run several containers
Orchestrate containers to talk and exchange info
Define a pipeline for tought process

# useful
* instantiating a new container with Ollama: docker run -d --gpus=all -v ollama:/root/.ollama -p $port:$port --name $name ollama/ollama
* running an llm on Ollama inside a docker container: docker exec -it $name ollama run $model
