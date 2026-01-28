from langchain.tools import tool


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Envoie un email (simulé)"""
    return f"Email simulé envoyé à {to} avec sujet '{subject}' et contenu '{body}'"


@tool
def create_calendar_event(title: str, date: str, time: str) -> str:
    """Crée un événement (simulé)"""
    return f"Événement simulé créé : '{title}' le {date} à {time}"
