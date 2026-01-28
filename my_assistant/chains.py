from llm_setup import llm
from prompts import (
    email_prompt,
    router_prompt,
    calendar_prompt,
    response_prompt,
    conversation_prompt,
)
from tools import send_email, create_calendar_event
from langchain.agents  import create_agent
from langchain.agents.structured_output import ToolStrategy



# Router
from schemas import Route, EmailInput

router_llm = router_prompt | llm.with_structured_output(Route)

# Email chain
email_chain = email_prompt | llm.bind_tools([send_email])

# Calendrier chain
calendar_chain = calendar_prompt | llm.bind_tools([create_calendar_event])

# Réponse lisible
response_chain = response_prompt | llm

# Conversation libre
conversation_chain = conversation_prompt | llm

#
#
# AGENT
#
#


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
    system_prompt=react_agent_system_prompt,  # ← Voici où vous ajoutez votre prompt !
    response_format=ToolStrategy(EmailInput)

)