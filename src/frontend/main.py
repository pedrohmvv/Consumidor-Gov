from src.frontend.pages.login import LoginPage
from src.frontend.pages.consumer import ConsumerPage
from src.frontend.pages.company import CompanyPage
from src.frontend.pages.servant import ServantPage

class Frontend:
    def __init__(self):
        self.pages = {
            "login": LoginPage(),
            "consumer": ConsumerPage(),
            "company": CompanyPage(),
            "servant": ServantPage()
        }
    
    def login(self):
        self.pages["login"].main()

    def consumer(self):
        self.pages["consumer"].main()

    def company(self):
        self.pages["company"].main()

    def servant(self):
        self.pages["servant"].main()
