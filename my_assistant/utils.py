from chains import response_chain
from logging import getLogger
import streamlit as st
from langgraph.types import Command

app_logger = getLogger(__name__)


def display_interupt_streamlit(interrupt_: dict):
    resume = {}

    for interupt in interrupt_.value["action_requests"]:
        interupt_args = interupt.get("args", {})
        to = interupt_args.get("to", "N/A")
        subject = interupt_args.get("subject", "N/A")
        body = interupt_args.get("body", "N/A")

        with st.chat_message("assistant"):
            st.write("Je suis prêt à envoyer cet email :")
            with st.container(border=True):
                st.write(f"**📬** {to}")
                st.write(f"**📝** {subject}")
                st.divider()
                st.text(body)

def ia_placeholder():
    return """
    <style>
    .typing {
    display: inline-block;
    }
    .typing span {
    animation: blink 1.4s infinite;
    }
    .typing span:nth-child(2) {
    animation-delay: 0.2s;
    }
    .typing span:nth-child(3) {
    animation-delay: 0.4s;
    }
    @keyframes blink {
    0%, 60%, 100% { opacity: 1; }
    30% { opacity: 0.3; }
    }
    </style>
    <div class="typing"><span>.</span><span>.</span><span>.</span></div>
    """
