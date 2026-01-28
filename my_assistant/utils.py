from chains import router_llm, email_chain, calendar_chain, response_chain


def route_user_input(user_text: str):
    route = router_llm.invoke({"input": user_text})
    return route.destination


def send_email_with_readable_response(user_text: str):
    tool_output = email_chain.invoke({"input": user_text})
    return response_chain.invoke({"tool_output": tool_output})


def create_event_with_readable_response(user_text: str):
    tool_output = calendar_chain.invoke({"input": user_text})
    return response_chain.invoke({"tool_output": tool_output})
