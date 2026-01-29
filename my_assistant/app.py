import streamlit as st
from chains import conversation_chain
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
