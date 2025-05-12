from tinydb import TinyDB, Query
from src.config import Config
from src.backend.user import User
import streamlit as st

class Database:
    def __init__(self):
        self.config = Config()
        self.db = TinyDB(self.config.database_path)
        self.tables = {
            'users': self.db.table('users'),
            'reports': self.db.table('reports'),
            'companies': self.db.table('companies'),
            'predictions': self.db.table('predictions')
        }

    def get_db(self):
        return self.db
    
    def get_user(self, email, password):
        query = Query()
        users_table = self.tables['users']
        user_meta = users_table.search((query.email == email) & (query.password == password))
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

    def search_user(self, user: User):
        query = Query()
        users_table = self.tables['users']
        if users_table.search(query.email == user.email):
            return True    
        return False

    def get_company(self, company_name):
        query = Query()
        companies_table = self.tables['companies']
        result = companies_table.search(query.company_name == company_name)
        if result:
            company = result[0]
            return company["id_company"], company["company_name"]    
        return None, None
    
    def get_last_id(self, table_name):
        table = self.db.table(table_name)
        all_records = table.all()
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
            table_users = self.db.table("users")
            table_users.insert(user_meta)
        except Exception as e:
            print(f"Error inserting user: {e}")

    def insert_report(self, report):
        pass

    def insert_report_company_response(self, report_id, company_response):
        pass
    
    def insert_user_rating(self, report_id, user_rating):
        pass
    
    def update_prediction(self, report_id, prediction):
        pass
    
    def update_user_rating(self, user_rating):
        pass
    
    
    
    
