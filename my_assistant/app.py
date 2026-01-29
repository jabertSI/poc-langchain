import streamlit as st
from chains import conversation_chain
import logging
from logging import getLogger
from supervisor import supervisor_agent


def main():
    app_logger = getLogger()
    app_logger.addHandler(logging.StreamHandler())
    app_logger.setLevel(logging.INFO)

    st.title("Assistant Email + Calendrier Automatique")

    if "history" not in st.session_state:
        st.session_state.history = []

    for user_text, assistant in st.session_state.history:
        st.chat_message("user").write(user_text)
        reply_text = assistant if isinstance(assistant, str) else assistant.content
        st.chat_message("assistant").write(reply_text)

    user_input = st.chat_input("Tapez votre message...")

    if user_input:
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(
                """
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
                """,
                unsafe_allow_html=True,
            )
            full_response = ""

            for step in supervisor_agent.stream(
                {"messages": [{"role": "user", "content": user_input}]}
            ):
                for update in step.values():
                    for message in update.get("messages", []):
                        if message.type == "ai" and message.content:
                            full_response = message.pretty_repr()
                            message_placeholder.write(full_response)

            if full_response:
                st.session_state.history.append((user_input, full_response))

        st.rerun()


if __name__ == "__main__":

    main()
