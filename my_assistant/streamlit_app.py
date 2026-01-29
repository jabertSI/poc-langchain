import streamlit as st
from chains import conversation_chain
import logging
from logging import getLogger
from supervisor import supervisor_agent
from utils import display_interupt_streamlit, ia_placeholder
from langgraph.types import Interrupt
from langgraph.types import Command


class StreamlitChatApp:
    def __init__(self):
        self.app_logger = getLogger()
        self.app_logger.addHandler(logging.StreamHandler())
        self.app_logger.setLevel(logging.INFO)
        self.config = {"configurable": {"thread_id": "6"}}
        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialise toutes les variables de session"""
        if "history" not in st.session_state:
            st.session_state.history = []
        if "waiting_interrupt" not in st.session_state:
            st.session_state.waiting_interrupt = False
        if "interrupt_id" not in st.session_state:
            st.session_state.interrupt_id = None
        if "user_decision" not in st.session_state:
            st.session_state.user_decision = None

    def display_history(self):
        """Affiche l'historique des messages"""
        for user_text, assistant in st.session_state.history:
            st.chat_message("user").write(user_text)
            if isinstance(assistant, Interrupt):
                display_interupt_streamlit(assistant)
            else:
                reply_text = assistant if isinstance(assistant, str) else assistant.content
                st.chat_message("assistant").write(reply_text)

    def display_interrupt_buttons(self):
        """Affiche les boutons d'approbation/rejet pour une interruption"""
        if not st.session_state.waiting_interrupt:
            return

        st.info(f"⏳ Décision requise pour l'interruption ID: {st.session_state.interrupt_id}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Approuver", key="approve_btn", use_container_width=True):
                st.session_state.user_decision = "approve"
                st.rerun()

        with col2:
            if st.button("❌ Rejeter", key="reject_btn", use_container_width=True):
                st.session_state.user_decision = "reject"
                st.rerun()

    def stream_supervisor_agent(self, stream_input):
        """Stream le supervisor agent et retourne la réponse et les interruptions"""
        full_response = ""
        interrupts = []

        for step in supervisor_agent.stream(stream_input, self.config):
            for update in step.values():
                if isinstance(update, dict):
                    for message in update.get("messages", []):
                        if message.type == "ai" and message.content:
                            full_response = message.pretty_repr()
                            yield full_response
                else:
                    interrupts.append(update[0])

        return full_response, interrupts

    def handle_interrupt(self, interrupt_, user_message):
        """Gère une interruption détectée"""
        display_interupt_streamlit(interrupt_)
        st.session_state.history.append((user_message, interrupt_))
        st.session_state.waiting_interrupt = True
        st.session_state.interrupt_id = interrupt_.id

    def handle_normal_response(self, full_response, user_message):
        """Gère une réponse normale (sans interruption)"""
        st.session_state.history.append((user_message, full_response))
        st.session_state.waiting_interrupt = False
        st.session_state.interrupt_id = None

    def process_user_decision(self):
        """Traite la décision de l'utilisateur sur une interruption"""
        if not st.session_state.user_decision:
            return

        decision_type = st.session_state.user_decision
        interrupt_id = st.session_state.interrupt_id
        decision_text = f"{'✅ Approuvé' if decision_type == 'approve' else '❌ Rejeté'}"

        st.chat_message("user").write(decision_text)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(ia_placeholder(), unsafe_allow_html=True)

            # Reprendre avec la décision
            stream_input = Command(resume={interrupt_id: {"decisions": [{"type": decision_type}]}})

            full_response = ""
            interrupts = []

            for step in supervisor_agent.stream(stream_input, self.config):
                for update in step.values():
                    if isinstance(update, dict):
                        for message in update.get("messages", []):
                            if message.type == "ai" and message.content:
                                full_response = message.pretty_repr()
                                message_placeholder.write(full_response)
                    else:
                        interrupts.append(update[0])

            # Si nouvelle interruption
            if interrupts:
                for interrupt_ in interrupts:
                    self.handle_interrupt(interrupt_, decision_text)
            else:
                self.handle_normal_response(full_response, decision_text)

        # Réinitialiser la décision
        st.session_state.user_decision = None
        st.rerun()

    def process_user_input(self, user_input):
        """Traite un nouveau message de l'utilisateur"""
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(ia_placeholder(), unsafe_allow_html=True)

            # Stream initial
            stream_input = {"messages": [{"role": "user", "content": user_input}]}

            full_response = ""
            interrupts = []

            for step in supervisor_agent.stream(stream_input, self.config):
                for update in step.values():
                    if isinstance(update, dict):
                        for message in update.get("messages", []):
                            if message.type == "ai" and message.content:
                                full_response = message.pretty_repr()
                                message_placeholder.write(full_response)
                    else:
                        interrupts.append(update[0])

            # Si interruption
            if interrupts:
                for interrupt_ in interrupts:
                    self.handle_interrupt(interrupt_, user_input)
            else:
                self.handle_normal_response(full_response, user_input)

        st.rerun()

    def run(self):
        """Point d'entrée principal de l'application"""
        st.title("Assistant Email + Calendrier Automatique")

        # Afficher l'historique
        self.display_history()

        # Afficher les boutons si en attente d'interruption
        self.display_interrupt_buttons()

        # Traiter une décision si elle existe
        self.process_user_decision()

        # Chat input (désactivé si en attente d'interruption)
        user_input = st.chat_input(
            "Tapez votre message...",
            disabled=st.session_state.waiting_interrupt
        )

        if user_input:
            self.process_user_input(user_input)
