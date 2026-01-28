from langchain_core.prompts import ChatPromptTemplate

# Router
router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Tu es un routeur de requêtes.
Ta tâche est de décider quel outil utiliser :
- send_email : si l'utilisateur veut envoyer un email
- create_calendar_event : si l'utilisateur veut créer un événement
- fallback : si aucune action n'est nécessaire
     Ne réponds jamais en texte libre. Renvoie uniquement le nom de la destination.""",
        ),
        ("human", "{input}"),
    ]
)

# Email
email_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Tu es un assistant qui extrait les informations pour envoyer un email.
Analyse le texte et appelle le tool send_email avec les paramètres appropriés :
- to : adresse email du destinataire
- subject : sujet clair et concis
- body : corps du message complet

        Si le sujet n'est pas explicite, crée-en un pertinent basé sur le contenu.""",
        ),
        ("human", "{input}"),
    ]
)


# Calendrier
calendar_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Tu es un assistant qui extrait automatiquement les informations pour créer un événement calendrier.
Renvoie TITLE, DATE et TIME de manière complète.
Si certaines informations ne sont pas dans le texte, invente-les de façon plausible.
Renvoie uniquement les champs du Pydantic CalendarInput en JSON.
     Ensuite appelle le tool create_calendar_event.""",
        ),
        ("human", "{input}"),
    ]
)

# Réponse lisible
response_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Tu es un assistant amical qui explique ce qu'il vient de faire.
Réécris la réponse de façon lisible et compréhensible pour l'utilisateur.
     Ne répète pas le JSON brut, écris en phrases complètes.""",
        ),
        ("human", "{tool_output}"),
    ]
)

# Conversation libre
conversation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Tu es un assistant amical et bavard.
Réponds naturellement à l'utilisateur même si aucune action n'est nécessaire.
     Sois clair, concis et convivial.""",
        ),
        ("human", "{input}"),
    ]
)
