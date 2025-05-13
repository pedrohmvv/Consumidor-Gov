# app.py
import streamlit as st
from src.frontend.pages.login import LoginPage
from src.frontend.pages.consumer import ConsumerPage
from src.frontend.pages.company import CompanyPage
from src.frontend.pages.servant import ServantPage

def main():
    if "pagina" not in st.session_state:
        st.session_state.pagina = "login"

    # Roteamento entre páginas
    if st.session_state.pagina == "login":
        LoginPage().main()
    elif st.session_state.pagina == "cidadao":
        ConsumerPage(st.session_state).main()
    elif st.session_state.pagina == "empresa":
        CompanyPage(st.session_state).main()
    elif st.session_state.pagina == "servidor":
        ServantPage(st.session_state).main()
    else:
        st.error("Página não encontrada!")

if __name__ == "__main__":
    main()
