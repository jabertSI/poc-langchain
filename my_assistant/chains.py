from llm_setup import llm
from prompts import (
    response_prompt,
    conversation_prompt,
)

# Réponse lisible
response_chain = response_prompt | llm

# Conversation libre
conversation_chain = conversation_prompt | llm
