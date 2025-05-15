class User:
    def __init__(self, id_user, name, user_type, id_company, cpf_user, email, pwd):
        self.id_user = id_user
        self.name = name
        self.user_type = user_type
        self.id_company = id_company
        self.cpf_user = cpf_user
        self.email = email
        self.pwd = pwd

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "name": self.name,
            "user_type": self.user_type,
            "id_company": self.id_company,
            "cpf_user": self.cpf_user,
            "email": self.email,
            "password": self.pwd  
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_user=data["id_user"],
            name=data["name"],
            user_type=data["user_type"],
            id_company=data["id_company"],
            cpf_user=data["cpf_user"],
            email=data["email"],
            pwd=data["password"] 
        )

    def is_consumer(self):
        return self.user_type == "cidadao"

    def is_company(self):
        return self.user_type == "empresa"

    def is_admin(self):
        return self.user_type == "servidor"


