from src.backend.database import Database
from src.config import Config
from pandas import DataFrame, to_datetime
from numpy import where, nan
import streamlit as st

class Servant:
    def __init__(self, session_state):
        self.db = Database()
        self.config = Config()
        self.session_state = session_state

    def get_reports(self):
        return self.db.get_reports(self.session_state.user)

    def get_table(self, table_name):
        return self.db.get_table(table_name)

    def get_dashboard_data(self):
        reports = self.get_reports()
        predictions = self.get_table('predicitons')
        companies = self.get_table('companies')

        
        df_reports = DataFrame(reports)
        df_predictions = DataFrame(predictions)
        df_companies = DataFrame(companies)

        df = (
            df_reports
            .merge(df_predictions, on='id_report', how='left')
            .merge(df_companies, on='id_company', how='left')
            .assign(
                non_resolution_prob=lambda x: 1 - x.prediction,
                date_format=lambda x: to_datetime(x.date.str.slice(0, 10), dayfirst=True),
                rating = lambda x: x.rating_score.str.extract('(\d+)').astype('Int64')                
            )
            .sort_values('prediction', ascending=False)
        )

        return df
        
