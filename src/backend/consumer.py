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
        date_str = date + ' - ' + state
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

        df_features = DataFrame(df_dict)
        features = self.preprocessor.transform(df_features)
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

    def get_companies(self):
        return self.db.get_companies()
    
    def get_table(self, table_name):
        return self.db.get_table(table_name)
    
    def get_states(self):
        return self.db.get_states()

    def get_company_name(self, id_company):
        return self.db.get_company_name(id_company)
    
    def get_report(self, report_id):
        return self.db.get_report(report_id)
    
    def update_report_evaluation(self, report_id, rating, evaluation, resolved):
        try:
            self.db.update_report_evaluation(report_id, rating, evaluation, resolved)
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar avaliação: {e}")
            return False
        
    def get_dashboard_data(self):
        reports = self.get_reports()
        predictions = self.get_table('predictions')
        companies = self.get_table('companies')

        
        df_reports = DataFrame(reports)
        df_predictions = DataFrame(predictions)
        df_companies = DataFrame(companies)

        df = (
            df_reports
            .merge(df_predictions, on='id_report', how='left')
            .merge(df_companies, on='id_company', how='left')
            .assign(non_resolution_prob=lambda x: 1 - x.prediction)
            .sort_values('prediction', ascending=False)
        )

        return df
        
        

