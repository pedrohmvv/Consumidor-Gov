from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.load_model()

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def predict(self, X):
        pass

