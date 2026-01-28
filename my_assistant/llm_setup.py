from langchain_ollama import ChatOllama

# LLM Ollama partagé par tout le projet
llm = ChatOllama(model="ministral-3", temperature=0)
