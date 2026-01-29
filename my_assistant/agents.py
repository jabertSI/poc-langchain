from langchain.agents import create_agent
from llm_setup import llm
from tools import send_email, create_calendar_event
from langchain.agents.structured_output import ToolStrategy
from schemas import EmailInput
from langchain.agents.middleware import HumanInTheLoopMiddleware

react_agent_system_prompt = """
Tu es un assistant qui extrait les informations pour envoyer un email.
Analyse le texte et appelle le tool send_email avec les paramètres appropriés :
- to : adresse email du destinataire
- subject : sujet clair et concis
- body : corps du message complet"""

# Créer l'agent avec le system prompt
email_agent = create_agent(
    llm,
    [send_email],
    system_prompt=react_agent_system_prompt,
    response_format=ToolStrategy(EmailInput),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"send_email": True},
            description_prefix="Outbound email pending approval",
        ),
    ],
)


CALENDAR_AGENT_PROMPT = """Tu es un assistant de planification de calendrier.
    Analysez les demandes de planification en langage naturel (par ex. : 'mardi prochain à 14 h')
    afin de les convertir en formats de date et d’heure ISO appropriés.
    Analyse le texte et appelle le tool create_calendar_event avec les paramètres appropriés :
    - title : Titre de l'evenement
    - date : La date de l'évenement
    - time : l'heure de l'évenement"""

calendar_agent = create_agent(
    llm,
    tools=[create_calendar_event],
    system_prompt=CALENDAR_AGENT_PROMPT,
)
