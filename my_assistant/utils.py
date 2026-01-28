from chains import router_llm, email_chain, calendar_chain, response_chain
from logging import getLogger
from tools import send_email

app_logger = getLogger(__name__)

def route_user_input(user_text: str):
    route = router_llm.invoke({"input": user_text})
    return route.destination


def send_email_with_readable_response(user_text: str):
    app_logger.info("send_email_with_readable_response")
    app_logger.info(user_text)

    response_email_chain = email_chain.invoke({"input": user_text})
    app_logger.info(response_email_chain)
    if response_email_chain.tool_calls:
        tool_call = response_email_chain.tool_calls[0]
        result = send_email.invoke(tool_call["args"])
        print(result)
#TODO : REACT AGENT !!!! 
    return response_chain.invoke({"tool_output": response_email_chain})


def create_event_with_readable_response(user_text: str):
    tool_output = calendar_chain.invoke({"input": user_text})
    return response_chain.invoke({"tool_output": tool_output})
