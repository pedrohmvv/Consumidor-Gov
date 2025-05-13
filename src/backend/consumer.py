import streamlit as st
import re
from numpy import nan, isnan
from pandas import DataFrame
from datetime import datetime

from src.backend.database import Database
from src.models.ml.models import ANN
from src.models.transformers.preprocessor import Preprocessor
from src.backend.report import Report

class Consumer:
    def __init__(self, session_state):
        self.session_state = session_state
        self.db = Database()
        self.preprocessor = Preprocessor()  
        self.ann_model = ANN()

    def create_report(self, text, company, state):
        status = "Não Resolvido"
        date = datetime.now().strftime("%d/%m/%Y")
        id_user = self.session_state.user.id_user
        id_company, _ = self.db.get_company(company)
        date_str = date + ', - ' + state
        last_id = self.db.get_last_id('reports')
        id_report = last_id + 1
        report = Report(
            status=status,
            date=date_str,
            report=text,
            id_user=id_user,
            id_company=id_company,
            state=state,
            id_report=id_report
        )

        return report
    
    def insert_report(self, report):
        try:
            self.db.insert_report(report)
        except Exception as e:
            st.error(f"Erro ao inserir reclamação: {e}")

    def insert_prediction(self, prediction):
        try:
            self.db.insert_prediction(prediction)
        except Exception as e:
            st.error(f"Erro ao inserir predição: {e}")

    def create_features(self, report):
        report_dict = report.to_dict()
        # Extract main fields
        report = report_dict['report']
        response = report_dict['company_response']
        # Check if the consumer answered
        consumidor_respondeu = 1
        if report_dict['consumer_written_evaluation'] == '<não há comentários do consumidor>':
            consumidor_respondeu = 0
        # Extract rating (1 to 5) or use -1 if absent
        match_nota = re.search(r'\d', str(report_dict['rating_score']))
        nota_logit = int(match_nota.group(0)) if match_nota else -1
        # Calculate days for response and if it was answered
        response_date = report_dict['response_date']
        if response_date is None or isinstance(response_date, float): 
            dias_para_resposta = -1
            respondido = 0
        else:
            if response_date == '(no mesmo dia)':
                dias_para_resposta = 0
            else:
                dias_para_resposta = (datetime.now() - datetime.strptime(response_date, "%d/%m/%Y")).days
            respondido = 1
        # State
        state = report_dict['state']
        # Features
        df_dict = {
            'clean_report': [report], 
            'clean_response': [response], 
            'consumidor_respondeu': [consumidor_respondeu],
            'dias_para_resposta': [dias_para_resposta], 
            'nota_logit': [nota_logit], 
            'respondido': [respondido], 
            'uf': [state]
        }

        features = self.preprocessor.transform(DataFrame(df_dict))
        return features

    def predict_report(self, report):
        report_id = report.id_report
        features = self.create_features(report)
        # Predictions
        prediction = self.ann_model.predict(features)
        label = self.ann_model.predict_label(prediction)
        
        return {
            'id_report': report_id, 
            'prediction': prediction, 
            'predicted_label': label,
            'true_label': None
        }
        
    def get_reports(self):
        return self.db.get_reports(self.session_state.user)
    
    def get_predictions(self):
        return self.db.get_predictions(self.session_state.user)

    def update_prediction(self, id_report, predictions):
        return self.db.update_prediction(id_report, predictions)
