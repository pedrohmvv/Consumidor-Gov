from typing import Optional
from dataclasses import dataclass


class Report:

    def __init__(self, 
        status: Optional[str] = None, 
        date: Optional[str] = None, 
        report: Optional[str] = None, 
        company_response: Optional[str] = '<não respondido pela empresa>', 
        response_date: Optional[str] = None, 
        rating_score: Optional[str] = '<não há comentários do consumidor>', 
        consumer_written_evaluation: Optional[str] = '<não há comentários do consumidor>', 
        id_user: Optional[str] = None, 
        id_company: Optional[str] = None, 
        id_report: Optional[str] = None,
        state: Optional[str] = None
    ):
        self.status = status  
        self.date = date  
        self.report = report  
        self.company_response = company_response  
        self.response_date = response_date  
        self.rating_score = rating_score 
        self.consumer_written_evaluation = consumer_written_evaluation  
        self.id_user = id_user  
        self.id_company = id_company  
        self.id_report = id_report  
        self.state = self.get_state(self.date)
    
    def get_state(self, date: str = None):
        state = date.split('-')[-1].replace(' ', '')
        return state

    def to_dict(self):
        return {
            'status': self.status,
            'date': self.date,
            'report': self.report,
            'company_response': self.company_response,
            'response_date': self.response_date,
            'rating_score': self.rating_score,
            'consumer_written_evaluation': self.consumer_written_evaluation,
            'id_user': self.id_user,
            'id_company': self.id_company,
            'id_report': self.id_report,
            'state': self.state
        }
