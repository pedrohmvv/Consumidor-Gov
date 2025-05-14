from src.frontend.pages.login import LoginPage
from src.frontend.pages.consumer import ConsumerPage
from src.frontend.pages.company import CompanyPage
from src.frontend.pages.servant import ServantPage

class Frontend:
    def __init__(self, session_state):
        self.session_state = session_state
        
        if "user" not in self.session_state or self.session_state.user is None:
            self.pages = {
                "login": LoginPage(self.session_state),
            }
        else:
            self.pages = {
                "login": LoginPage(self.session_state),
                "consumer": ConsumerPage(self.session_state),
                "company": CompanyPage(self.session_state),
                "servant": ServantPage(self.session_state),
            }
    
    def run(self, page):
        self.pages[page].main()
