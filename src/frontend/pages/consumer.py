import streamlit as st
import pandas as pd
from datetime import datetime
from src.backend.database import Database
from src.backend.consumer import Consumer

class ConsumerPage:
    def __init__(self, session_state):
        self.db = Database()
        self.session_state = session_state
        self.backend = None

    def main(self):
        st.title("Área do Consumidor")
        st.write(f"Bem-vindo, {self.session_state.user.name}!")

        if "backend_loaded" not in self.session_state:
            self.session_state.backend_loaded = False

        if not self.session_state.backend_loaded:
            with st.spinner("Carregando recursos de IA..."):
                self.backend = Consumer(self.session_state)
                self.session_state.backend = self.backend
                self.session_state.backend_loaded = True
            st.success("Modelos carregados com sucesso!")
            st.experimental_rerun()
        else:
            self.backend = self.session_state.backend

            col1, col2 = st.columns([2, 1])
            with col1:
                self.complaint_form()

            with col2:
                self.complaints_sidebar()

            self.dashboard()

    def complaint_form(self):
        st.subheader("Nova Reclamação")

    def complaints_sidebar(self):
        st.subheader("Suas Reclamações")

    def dashboard(self):
        st.subheader("Dashboard de Reclamações")

    
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from src.backend.database import Database
from src.models.ml.models import ANN
from src.models.transformers.preprocessor import Preprocessor

class ConsumerPage:
    def __init__(self, user):
        self.user = user
        self.db = Database()
        self.preprocessor = Preprocessor()  
        self.ann_model = ANN()

    def main(self):
        st.title("Área do Consumidor")
        st.write(f"Bem-vindo, {self.user.name}!")

        col1, col2 = st.columns([2, 1])

        with col1:
            self.complaint_form()

        with col2:
            self.complaints_sidebar()

        self.dashboard()

    def complaint_form(self):
        st.subheader("Nova Reclamação")

        
        #Informações necessárias:
        #- status: Automático -> Não Resolvido
        #- data: Automático -> Data atual
        #- report: Texto da reclamação
        #- id_user: Automático -> ID do usuário
        #- id_company: Automático -> ID da empresa
        #- state: Estado selecionado pelo usuário
#
        #OBS: Ao inserir na tabela 'reports', a coluna data é
        #data, - state
        
        with st.form("complaint_form"):
            complaint_text = st.text_area("Descreva sua reclamação", height=150)
            company = st.selectbox("Empresa", self.db.get_companies())
            state = st.selectbox("Estado", self.db.get_states())
            status = "Não Resolvido"
            # Data quero APENAS a data no formato dd/mm/yyyy
            date = datetime.now().strftime("%d/%m/%Y")
            id_user = self.user.id_user
            id_company = self.db.get_company(company)

            submitted = st.form_submit_button("Enviar Reclamação")

"""