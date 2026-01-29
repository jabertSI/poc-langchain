from langchain_core.prompts import ChatPromptTemplate

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
