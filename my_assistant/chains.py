from llm_setup import llm
from prompts import (
    email_prompt,
    router_prompt,
    calendar_prompt,
    response_prompt,
    conversation_prompt,
)
from tools import send_email, create_calendar_event
from langchain_core.output_parsers import PydanticToolsParser

# Router
from schemas import Route

router_llm = router_prompt | llm.with_structured_output(Route)

# Email chain
email_chain = email_prompt | llm.bind_tools([send_email])

# Calendrier chain
calendar_chain = calendar_prompt | llm.bind_tools([create_calendar_event])

# Réponse lisible
response_chain = response_prompt | llm

# Conversation libre
conversation_chain = conversation_prompt | llm
