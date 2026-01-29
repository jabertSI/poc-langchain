from langchain.agents import create_agent
from llm_setup import llm
from tools import send_email
from langchain.agents.structured_output import ToolStrategy
from schemas import EmailInput

react_agent_system_prompt = """
Tu es un assistant qui extrait les informations pour envoyer un email.
Analyse le texte et appelle le tool send_email avec les paramètres appropriés :
- to : adresse email du destinataire
- subject : sujet clair et concis
- body : corps du message complet
Utilise le tool send_email pour envoyer les emails."""

# Créer l'agent avec le system prompt
agent_email = create_agent(
    llm,
    [send_email],
    system_prompt=react_agent_system_prompt,
    response_format=ToolStrategy(EmailInput),
)
