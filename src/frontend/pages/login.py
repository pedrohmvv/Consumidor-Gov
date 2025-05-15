# src/frontend/login.py
import streamlit as st
from src.config import Config
from src.backend.database import Database
from src.backend.login import Login
from src.frontend.pages.project import Project


class LoginPage:
    def __init__(self, session_state):
        self.db = Database()
        self.session_state = session_state
        self.backend = Login(session_state)
        self.config = Config()
        self.project_page = Project(session_state)

    def main(self):
        st.title("Login / Registro")
        st.warning('Por favor, use dados fictícios, não há verificação de credenciais.')

        if "usuario" in self.session_state:
            self.session_state.pagina = ''
            st.success("Usuário já logado!")
            return  

        option = st.radio("Escolha uma opção", ["Login", "Registrar"])

        if option == "Login":
            self.login_form()
        elif option == "Registrar":
            self.register_form()

    def login_form(self):
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            user = self.backend.login(email, password)
            if user:
                st.success("Login bem-sucedido!")
                self.session_state.user = user
                self.session_state.pagina = user.user_type
                st.rerun()
            else:
                st.error("Email ou senha inválidos!")

        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col2:
            if st.button("Conheça o projeto"):
                self.session_state.pagina = "project"
                st.rerun()

    def register_form(self):
        roles_map = {
            "Consumidor": "cidadao",
            "Empresa": "empresa",
            "Servidor": "servidor"
        }
        companies = self.backend.get_companies()

        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        role = st.selectbox("Informe o seu papel", ["Consumidor", "Empresa", "Servidor"])
        
        cpf_user = st.text_input("CPF")
        if cpf_user and not self.backend.validate_cpf(cpf_user):
            st.error("CPF inválido. Use o formato: XXX.XXX.XXX-XX")
            return
            
        name = st.text_input("Nome")
        if role == "Empresa":
            company_name = st.selectbox("Nome da empresa", companies)
        else:
            company_name = None
        
        if st.button("Registrar"):
            user = self.backend.create_user(email, password, name, roles_map[role], company_name, cpf_user)
            if self.backend.insert_user(user):
                st.success("Registro bem-sucedido!")    
                self.session_state.user = user
                self.session_state.pagina = user.user_type
                st.rerun()
            else:
                st.error("Este email já está registrado!")
