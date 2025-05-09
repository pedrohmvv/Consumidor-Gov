# src/models/pipelines/builder.py

import os
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from gensim.models import Word2Vec
from src.models.transformers.textcleaner import TextCleaner
from src.models.transformers.w2vec import Word2VecVectorizer
from src.config import Config

class Preprocessor:
    def __init__(self, config: Config):
        self.config = config
        self.model_path = os.path.join(
            config.project_dir,
            config.env_vars.src_dir,
            config.env_vars.models_dir,
            config.env_vars.W2VEC_model
        )
        self.w2vec_model = Word2Vec.load(self.model_path)

    def build_pipeline_w2v(self):
        return Pipeline([
            ('preprocessador', TextCleaner(remove_accents=False)),
            ('vetorizador', Word2VecVectorizer(word2vec_model=self.w2vec_model))
        ])

    def build_column_transformer(self):
        num_cols = ['nota_logit']
        cat_cols = ['uf']
        pipeline_w2v = self.build_pipeline_w2v()

        return ColumnTransformer(
            transformers=[
                ('w2v_report', pipeline_w2v, 'clean_report'),
                ('w2v_response', pipeline_w2v, 'clean_response'),
                ('num', StandardScaler(), num_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
            ]
        )

    def fit_transform(self, data: pd.DataFrame, target_col: str, drop_cols: list):
        """Aplica o ColumnTransformer nos dados, removendo colunas indesejadas e a variável alvo."""
        X = data.drop(columns=drop_cols + [target_col])
        transformer = self.build_column_transformer()
        return transformer.fit_transform(X)
