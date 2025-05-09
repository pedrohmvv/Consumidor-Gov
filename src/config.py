from dataclasses import dataclass
from os.path import abspath, dirname, join
from yaml import load, SafeLoader

@dataclass
class EnvVariables:
    data_dir: str
    staging_dir: str
    ml_dir: str
    data_file: str

    src_dir: str
    models_dir: str
    transformers_dir: str
    ml_models_dir: str
    ANN_model: str
    LOGIT_model: str
    W2VEC_model: str

@dataclass
class ExtractVariables:
    API_URL: str
    CONTENT_TYPE: str
    USER_AGENT: str
    REFERRER: str
    ORIGIN: str
    CARD_CLASS: str
    ACCEPT: str
    ACCEPT_ENCODING: str
    ACCEPT_LANGUAGE: str
    CONNECTION: str
    CONTENT_LENGTH: str
    COOKIE: str
    HOST: str
    SEC_CH_UA: str
    SEC_CH_UA_MOBILE: str
    SEC_CH_UA_PLATFORM: str
    SEC_FETCH_DEST: str
    SEC_FETCH_MODE: str
    SEC_FETCH_SITE: str
    X_REQUESTED_WITH: str

class Config:

    def __init__(self):
        self.project_dir = abspath(dirname(dirname(__file__)))
        data = {}
        with open(join(dirname(abspath(__file__)), 'vars.yaml'), encoding='utf-8') as file:
            data = load(file, Loader=SafeLoader)

        self.extract_vars = ExtractVariables(
            API_URL=data.get('API_URL'),
            CONTENT_TYPE=data.get('CONTENT_TYPE'),
            USER_AGENT=data.get('USER_AGENT'),
            REFERRER=data.get('REFERRER'),
            ORIGIN=data.get('ORIGIN'),
            CARD_CLASS=data.get('CARD_CLASS'),
            ACCEPT=data.get('ACCEPT'),
            ACCEPT_ENCODING=data.get('ACCEPT_ENCODING'),
            ACCEPT_LANGUAGE=data.get('ACCEPT_LANGUAGE'),
            CONNECTION=data.get('CONNECTION'),
            CONTENT_LENGTH=data.get('CONTENT_LENGTH'),
            COOKIE=data.get('COOKIE'),
            HOST=data.get('HOST'),
            SEC_CH_UA=data.get('SEC_CH_UA'),
            SEC_CH_UA_MOBILE=data.get('SEC_CH_UA_MOBILE'),
            SEC_CH_UA_PLATFORM=data.get('SEC_CH_UA_PLATFORM'),
            SEC_FETCH_DEST=data.get('SEC_FETCH_DEST'),
            SEC_FETCH_MODE=data.get('SEC_FETCH_MODE'),
            SEC_FETCH_SITE=data.get('SEC_FETCH_SITE'),
            X_REQUESTED_WITH=data.get('X_REQUESTED_WITH')
        )

        self.env_vars = EnvVariables(
            data_dir=data.get('data_dir'),
            staging_dir=data.get('staging_dir'),
            ml_dir=data.get('ml_dir'),
            data_file=data.get('data_file'),
            src_dir=data.get('src_dir'),
            models_dir=data.get('models_dir'),
            transformers_dir=data.get('transformers_dir'),
            ml_models_dir=data.get('ml_models_dir'),
            ANN_model=data.get('ANN_model'),
            LOGIT_model=data.get('LOGIT_model'),
            W2VEC_model=data.get('W2VEC_model')
        )
