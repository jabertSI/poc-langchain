from chains import response_chain
from logging import getLogger
from agents import agent_email

app_logger = getLogger(__name__)


def send_email_with_readable_response(user_text: str):
    app_logger.info("send_email_with_readable_response")
    app_logger.info(user_text)

    # REACT AGENT WAY
    result_react_agent = agent_email.invoke({"messages": [("user", user_text)]})

    app_logger.info(result_react_agent)
    return response_chain.invoke({"tool_output": result_react_agent})


def create_event_with_readable_response(user_text: str):
    #
    return
