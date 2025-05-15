# app.py
import streamlit as st

st.set_page_config(
    page_title="Consumidor Gov - ReclamaRank",
    page_icon="https://www.gov.br/pt-br/apps/consumidor-gov.br/@@images/imagem/mini"
)

from src.frontend.main import Frontend

frontend = Frontend(st.session_state)

def main():
    if "pagina" not in frontend.session_state:
        frontend.session_state.pagina = "login"

    pagina = frontend.session_state.pagina

    if pagina == "project":
        frontend.run("project")
    elif "user" not in frontend.session_state or frontend.session_state.user is None:
        frontend.run("login")
    elif frontend.session_state.user.user_type == "cidadao":
        frontend.run("consumer")
    elif frontend.session_state.user.user_type == "empresa":
        frontend.run("company")
    elif frontend.session_state.user.user_type == "servidor":
        frontend.run("servant")
    else:
        st.error("Página não encontrada!")


if __name__ == "__main__":
    main()
