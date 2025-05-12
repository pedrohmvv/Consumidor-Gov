from src.backend.database import Database
from src.config import Config
import streamlit as st

class ServantPage:
    def __init__(self, user):
        self.db = Database()
        self.config = Config()
        self.user = user

    def main(self):
        st.title("Página do Servidor")
        pass
