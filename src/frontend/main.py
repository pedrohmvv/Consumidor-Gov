from src.frontend.pages.login import LoginPage
from src.frontend.pages.consumer import ConsumerPage
from src.frontend.pages.company import CompanyPage
from src.frontend.pages.servant import ServantPage
from src.frontend.pages.project import Project 
import streamlit as st

class Frontend:
    def __init__(self, session_state):
        self.session_state = session_state

        self.pages = {
            "login": lambda: LoginPage(self.session_state),
            "project": lambda: Project(self.session_state), 
        }

        if "user" in self.session_state and self.session_state.user is not None:
            self.pages.update({
                "consumer": lambda: ConsumerPage(self.session_state),
                "company": lambda: CompanyPage(self.session_state),
                "servant": lambda: ServantPage(self.session_state),
            })

    def run(self, page):
        # Configurações específicas de layout para cada página
        if page == "servant":
            st.markdown("""
                <style>
                    .main > div {
                        padding-top: 1rem;
                        padding-bottom: 1rem;
                        padding-left: 2rem;
                        padding-right: 2rem;
                    }
                    .block-container {
                        max-width: 100%;
                    }
                </style>
            """, unsafe_allow_html=True)
        
        self.pages[page]().main()
