# app.py
import streamlit as st
from src.frontend.main import Frontend

frontend = Frontend(st.session_state)

def main():
    if "pagina" not in st.session_state:
        st.session_state.pagina = "login"

    if st.session_state.pagina == "login":
        frontend.run("login")
    elif st.session_state.pagina == "cidadao":
        frontend.run("consumer")
    elif st.session_state.pagina == "empresa":
        frontend.run("company")
    elif st.session_state.pagina == "servidor":
        frontend.run("servant")
    else:
        st.error("Página não encontrada!")

if __name__ == "__main__":
    main()
