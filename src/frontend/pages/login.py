# src/frontend/login.py
import streamlit as st
from src.config import Config
from src.backend.database import Database
from src.backend.login import Login

class LoginPage:
    def __init__(self):
        self.db = Database()
        self.backend = Login(st.session_state)
        self.config = Config()

    def main(self):
        st.title("Login / Registro")

        if "usuario" in st.session_state:
            st.session_state.pagina = ''
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
                st.experimental_rerun()
            else:
                st.error("Email ou senha inválidos!")

        st.markdown(
            '<p style="font-size: 14px;">Ainda não criou uma conta? '
            '<a href="javascript:void(0);" onclick="window.location.reload();">'
            'Clique aqui para Registrar-se</a></p>',
            unsafe_allow_html=True
        )

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
        name = st.text_input("Nome")
        if role == "Empresa":
            company_name = st.selectbox("Nome da empresa", companies)
        else:
            company_name = None
        
        user = self.backend.create_user(email, password, name, roles_map[role], company_name, cpf_user)

        if st.button("Registrar"):
            if self.backend.insert_user(user):
                st.success("Registro bem-sucedido!")
                st.experimental_rerun()
            else:
                st.error("Este email já está registrado!")
