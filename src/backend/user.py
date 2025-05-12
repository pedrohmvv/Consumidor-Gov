class User:
    def __init__(self, id_user, name, user_type, id_company, cpf_user, email, pwd):
        self.id_user = id_user
        self.name = name
        self.user_type = user_type
        self.id_company = id_company
        self.cpf_user = cpf_user
        self.email = email
        self.__pwd = pwd

    def is_consumer(self):
        return self.user_type == "cidadao"

    def is_company(self):
        return self.user_type == "empresa"

    def is_admin(self):
        return self.user_type == "servidor"


