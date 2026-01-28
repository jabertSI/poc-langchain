import streamlit as st
from chains import conversation_chain
from utils import (
    route_user_input,
    send_email_with_readable_response,
    create_event_with_readable_response,
)
import logging
from logging import getLogger


def main():
    app_logger = getLogger()
    app_logger.addHandler(logging.StreamHandler())
    app_logger.setLevel(logging.INFO)

    st.title("Assistant Email + Calendrier Automatique")

    if "history" not in st.session_state:
        st.session_state.history = []

    # Champ de saisie type chat
    user_input = st.chat_input("Tapez votre message...")

    if user_input:
        # Calculer la réponse immédiatement
        destination = route_user_input(user_input)

        if destination == "send_email":
            response = send_email_with_readable_response(user_input)
        elif destination == "create_calendar_event":
            response = create_event_with_readable_response(user_input)
        else:
            response = conversation_chain.invoke({"input": user_input})

        # Ajouter les deux à l'historique avant d'afficher
        st.session_state.history.append((user_input, response))

    # Affichage de l'historique en bulles de chat
    for user_text, assistant in st.session_state.history:
        st.chat_message("user").write(user_text)
        reply_text = assistant if isinstance(assistant, str) else assistant.content
        st.chat_message("assistant").write(reply_text)


if __name__ == "__main__":

    main()
