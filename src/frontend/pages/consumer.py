import streamlit as st
from src.backend.database import Database
from src.backend.consumer import Consumer

class ConsumerPage:
    def __init__(self, session_state):
        self.db = Database()
        self.session_state = session_state
        self.backend = None

    def main(self):
        st.title("Área do Consumidor")
        st.write(f"Bem-vindo, {self.session_state.user.name}!")

        if "backend_loaded" not in self.session_state:
            self.session_state.backend_loaded = False

        if not self.session_state.backend_loaded:
            with st.spinner("Carregando recursos de IA..."):
                self.backend = Consumer(self.session_state)
                self.session_state.backend = self.backend
                self.session_state.backend_loaded = True
            st.success("Modelos carregados com sucesso!")
            st.experimental_rerun()
        else:
            self.backend = self.session_state.backend

            col1, col2 = st.columns([2, 1])
            with col1:
                self.complaint_form()

            with col2:
                self.complaints_sidebar()

            self.dashboard()

    def complaint_form(self):
        st.subheader("Nova Reclamação")

    def complaints_sidebar(self):
        st.subheader("Suas Reclamações")

    def dashboard(self):
        st.subheader("Dashboard de Reclamações")