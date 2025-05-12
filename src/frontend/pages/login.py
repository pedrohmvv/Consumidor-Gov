# src/frontend/login.py
import streamlit as st
from src.config import Config
from tinydb import TinyDB, Query
from src.backend.database import Database
from src.backend.user import User

class LoginPage:
    def __init__(self):
        self.db = Database()
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
            user = self.db.get_user(email, password)
            if user:
                st.session_state.usuario = email
                st.session_state.pagina = user.user_type
                st.session_state.user = user
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
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        role = st.selectbox("Escolha o seu papel", ["consumer", "company", "admin"])
        cpf_user = st.text_input("CPF")
        name = st.text_input("Nome")
        company_name = st.selectbox("Nome da empresa", ["<LISTA_NOMES_EMPRESAS>"])
        
        id_company, _ = self.db.get_company(company_name)
        last_id = self.db.get_last_id("users")
        id_user = last_id + 1

        user = User(
            id_user=id_user,
            name=name,
            user_type=role,
            id_company=id_company,
            cpf_user=cpf_user,
            email=email,
            pwd=password
        )

        if st.button("Registrar"):
            if not self.db.search_user(user):
                self.db.insert_user(user)
                st.session_state.usuario = user.name
                st.session_state.pagina = "cidadao"  
                st.success("Registro bem-sucedido!")
            else:
                st.error("Este email já está registrado!")
