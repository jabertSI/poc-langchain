from langchain.tools import tool
from langchain.agents import create_agent
from llm_setup import llm
from agents import email_agent, calendar_agent


@tool
def schedule_event(request: str) -> str:
    """Planifier des événements de calendrier à l’aide du langage naturel.

    Utilisez ceci lorsque l’utilisateur souhaite créer un rendez-vous dans le calendrier.
    Gère l’analyse des dates/heures et la création d’événements.

    Entrée : demande de planification en langage naturel
    (par ex. : « réunion avec l’équipe design mardi prochain à 14 h »)
    """
    result = calendar_agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text


@tool
def manage_email(request: str) -> str:
    """Envoyer des e-mails à l’aide du langage naturel.

    Utilisez ceci lorsque l’utilisateur souhaite envoyer des notifications,
    des rappels ou toute communication par e-mail.
    Gère l’extraction des destinataires, la génération de l’objet
    et la rédaction de l’e-mail.

    Entrée : demande d’e-mail en langage naturel
    (par ex. : « envoie un mail à toto@foo.fr concernant le projet X »)
    """
    result = email_agent.invoke({"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].text


SUPERVISOR_PROMPT = (
    "Vous êtes un assistant personnel serviable. "
    "Vous pouvez planifier des événements de calendrier et envoyer des e-mails. "
    "Décomposez les demandes des utilisateurs en appels d’outils appropriés et coordonnez les résultats. "
    "Lorsqu’une demande implique plusieurs actions, utilisez plusieurs outils de manière séquentielle."
    "Dans la réponse tu dois afficher tout les détails tools, contenue du mail et sont sujet et les infos de l'evénement."
)

supervisor_agent = create_agent(
    llm,
    tools=[schedule_event, manage_email],
    system_prompt=SUPERVISOR_PROMPT,
)
