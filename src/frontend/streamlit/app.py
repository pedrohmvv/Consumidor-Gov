import streamlit as st
from pages.login import LoginPage
from pages.consumer import ConsumerPage
from pages.servant import ServantPage
from pages.company import CompanyPage

class App:
    def __init__(self):
        self.setup_page()
        self.initialize_session_state()
        
    def setup_page(self):
        st.set_page_config(
            page_title="Consumidor.gov",
            page_icon="🏛️",
            layout="wide"
        )
        
    def initialize_session_state(self):
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_type' not in st.session_state:
            st.session_state.user_type = None
        if 'username' not in st.session_state:
            st.session_state.username = None
            
    def run(self):
        if not st.session_state.authenticated:
            login_page = LoginPage()
            login_page.render()
        else:
            self.render_authenticated_page()
            
    def render_authenticated_page(self):
        if st.session_state.user_type == 'cidadao':
            consumer_page = ConsumerPage()
            consumer_page.render()
        elif st.session_state.user_type == 'servidor':
            servant_page = ServantPage()
            servant_page.render()
        elif st.session_state.user_type == 'empresa':
            company_page = CompanyPage()
            company_page.render()

if __name__ == "__main__":
    app = App()
    app.run() 