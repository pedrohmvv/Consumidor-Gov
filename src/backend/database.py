from tinydb import TinyDB, Query
from src.config import Config
from src.backend.user import User
import streamlit as st

class Database:
    def __init__(self):
        self.config = Config()
        self.db = TinyDB(self.config.database_path)
        self.users_table = self.db.table('users')
        self.reports_table = self.db.table('reports')
        self.companies_table = self.db.table('companies')
        self.predictions_table = self.db.table('predicitons')

    def get_db(self):
        return self.db

    def get_user(self, email, password):
        query = Query()
        user_meta = self.users_table.search((query.email == email) & (query.password == password))
        if user_meta:
            user_meta = user_meta[0]
            user = User(
                id_user=user_meta['id_user'],
                name=user_meta['name'],
                user_type=user_meta['user_type'],
                id_company=user_meta['id_company'],
                cpf_user=user_meta['cpf_user'],
                email=user_meta['email'],
                pwd=user_meta['password']
            )
            st.write('Nome do usuário: ', user.name)
            return user
        else:
            return None
        
    def get_reports(self, user: User):
        query = Query()
        if user.user_type == 'servidor':
            return self.reports_table.all()
        else:
            return self.reports_table.search(query.id_user == user.id_user)
        
    def get_predictions(self, user: User):
        query = Query()

        user_reports = self.reports_table.search(query.id_user == user.id_user)
        user_report_ids = [report['id_report'] for report in user_reports]
        user_predictions = self.predictions_table.search(query.id_report.one_of(user_report_ids))

        return user_predictions

    def update_prediction(self, id_report, predictions):
        query = Query() 
        try:
            self.predictions_table.update(
                {
                'prediction': predictions['prediction'],
                'predicted_label': predictions['predicted_label'],
                'true_label': predictions['true_label']
                }, query.id_report == id_report
            )
            return True
        except Exception as e:
            print(f"Error updating prediction: {e}")
            return False

    def search_user(self, user: User):
        query = Query()
        if self.users_table.search(query.email == user.email):
            return True    
        return False

    def get_user_by_email(self, email):
        users_table = self.db.table("users")
        result = users_table.search(Query().email == email)
        if result:
            return User.from_dict(result[0])
        return None

    def get_company(self, company_name):
        query = Query()
        if self.companies_table.search(query.company_name == company_name):
            result = self.companies_table.search(query.company_name == company_name)
            if result:
                company = result[0]
            return company["id_company"], company["company_name"]    
        return None, None
    
    def get_companies(self):
        return [company["company_name"] for company in self.companies_table.all()]

    def get_states(self):
        return self.config.env_vars.states

    def get_last_id(self, table_name):
        if self.db.table(table_name):
            all_records = self.db.table(table_name).all()
            if all_records:
                return max(record["id_user"] for record in all_records)
        else:
            return 0

    def insert_user(self, user):
        user_meta = {
            "id_user": user.id_user,
            "name": user.name,
            "user_type": user.user_type,
            "id_company": user.id_company,
            "cpf_user": user.cpf_user,
            "email": user.email,
            "password": user.pwd  
        }
        try:
            self.users_table.insert(user_meta)
        except Exception as e:
            print(f"Error inserting user: {e}")

    def insert_report(self, report):
        report_dict = report.to_dict()
        try:
            self.reports_table.insert(report_dict)
        except Exception as e:
            print(f"Error inserting report: {e}")

    def insert_prediction(self, prediction):
        try:
            self.predictions_table.insert(prediction)
        except Exception as e:
            print(f"Error inserting prediction: {e}")

    def get_table(self, table_name):
        return {
            'reports': self.reports_table,
            'predicitons': self.predictions_table,
            'companies': self.companies_table,
        }[table_name]

    def insert_report_company_response(self, report_id, company_response):
        pass
    
    def insert_user_rating(self, report_id, user_rating):
        pass
    
    def update_prediction(self, report_id, prediction):
        pass
    
    def update_user_rating(self, user_rating):
        pass
    
    def get_company_name(self, id_company):
        query = Query()
        company = self.companies_table.search(query.id_company == id_company)
        if company:
            return company[0]['company_name']
        return "Empresa não encontrada"
    
    def get_report(self, report_id):
        query = Query()
        report = self.reports_table.search(query.id_report == report_id)
        if report:
            return report[0]
        return None
    
    def update_report_evaluation(self, report_id, rating, evaluation, resolved):
        query = Query()
        try:
            self.reports_table.update({
                'rating_score': str(rating),
                'consumer_written_evaluation': evaluation,
                'status': 'Resolvido' if resolved else 'Não Resolvido'
            }, query.id_report == report_id)
            return True
        except Exception as e:
            print(f"Error updating report evaluation: {e}")
            return False
    
    
    
    
