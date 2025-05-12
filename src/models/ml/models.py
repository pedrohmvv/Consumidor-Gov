import joblib
from tensorflow.keras.models import load_model
from src.config import Config
from src.models.ml.base_model import BaseModel

config = Config()

class LogisticRegression(BaseModel):
    def __init__(self, model_path: str = config.logit_model_path):
        super().__init__(model_path)

    def load_model(self):
        self.model = joblib.load(self.model_path)

    def predict(self, X):
        return self.model.predict(X)
    
class ANN(BaseModel):
    def __init__(self, model_path: str = config.ann_model_path):
        super().__init__(model_path)

    def load_model(self):
        self.model = load_model(self.model_path)

    def predict(self, X):
        return self.model.predict(X)    