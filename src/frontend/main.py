from src.frontend.pages.login import LoginPage
from src.frontend.pages.consumer import ConsumerPage
from src.frontend.pages.company import CompanyPage
from src.frontend.pages.servant import ServantPage

class Frontend:
    def __init__(self, session_state):
        self.session_state = session_state

        if "user" not in self.session_state or self.session_state.user is None:
            self.pages = {
                "login": lambda: LoginPage(self.session_state),
            }
        else:
            self.pages = {
                "login": lambda: LoginPage(self.session_state),
                "consumer": lambda: ConsumerPage(self.session_state),
                "company": lambda: CompanyPage(self.session_state),
                "servant": lambda: ServantPage(self.session_state),
            }

    def run(self, page):
        self.pages[page]().main()
