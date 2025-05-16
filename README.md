containerBots
containerizing nlp models for chatbot and agentic purposes

#DONE:

Started a container
pulled and ran Ollama on the container
told ollama to run phi3
give the LLM some tools
give the LLM specific context
give the LLM some system prompts

#2DO:
Run several containers
Define a Flask application for managing requests
Define a container that can package the flask application?



#FURTHER DOWN:
Orchestrate containers to talk and exchange info
Define a pipeline for tought process

# useful
* instantiating a new container with Ollama: docker run -d --gpus=all -v ollama:/root/.ollama -p $port:$port --name $name ollama/ollama
* running an llm on Ollama inside a docker container: docker exec -it $name ollama run $model

# Possible folder structure: 
/finance-bot/                    # Root repository folder
  /app/                          # Application code
    app.py                       # Flask application
    langchain_bot.py             # LangChain implementation
    langgraph_agent.py           # LangGraph implementation
    requirements.txt             # Python dependencies
  Dockerfile                     # Container definition
  docker-compose.yml             # Container orchestration
  .env                           # Environment variables (gitignored)
  README.md                      # Documentation
