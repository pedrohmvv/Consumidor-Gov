from src.backend.database import Database
from src.config import Config
from src.backend.servant import Servant
import streamlit as st

class ServantPage:
    def __init__(self, session_state):
        self.db = Database()
        self.config = Config()
        self.session_state = session_state
        self.backend = Servant(self.session_state)

    def main(self):
        st.title("Página do Servidor")
        st.write(f"Bem-vindo(a), {self.session_state.user.name}!")
        self.dashboard()

    def dashboard(self):
        """
        Informações para o dashboard do servidor:
        - Qtd. de reclamações enviadas
        - Qtd. de reclamações resolvidas e não resolvidas
        - Prop. de reclamações resolvidas e não resolvidas
        - Taxa de resolução das reclamações
        - Resoluções e não resoluções ao longo do tempo
        - Empresas com mais reclamações
        - Empresas com maior taxa de resolução
        - Empresas com menor taxa de resolução
        - Média de avaliação das reclamações
        - Média de avaliação das reclamações por empresa
        - Média de avaliação das reclamações por status
        - Empresas com maior probabilidade média de resolução
        - Empresas com menor probabilidade média de resolução
        - Reclamações com maior e menor probabilidade de resolução
        """
        data = self.backend.get_dashboard_data()
        st.subheader("Reclamações")
        st.dataframe(data)
        
