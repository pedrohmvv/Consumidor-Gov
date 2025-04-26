from dataclasses import dataclass
from yaml import load
from yaml.loader import SafeLoader
from os.path import join, dirname, abspath

@dataclass
class EnvVariables:
    data_dir: str
    staging_dir: str
    data_file: str

@dataclass
class ExtractVariables:
    API_URL: str
    CONTENT_TYPE: str
    USER_AGENT: str
    REFERRER: str
    ORIGIN: str
    CARD_CLASS: str

class Config:

    def __init__(self):
        self.project_dir = abspath(dirname(dirname(__file__)))
        data = {}
        with open(join(dirname(abspath(__file__)), 'vars.yaml'), encoding='utf-8') as file:
            data = load(file, Loader=SafeLoader)
        self.extract_vars = ExtractVariables(
            API_URL=data.get('API_URL'),
            CONTENT_TYPE= data.get('CONTENT_TYPE'),
            USER_AGENT= data.get('USER_AGENT'),
            REFERRER=data.get('REFERRER'),
            ORIGIN=data.get('ORIGIN'),
            CARD_CLASS=data.get('CARD_CLASS'),
        )
        self.env_vars = EnvVariables(
            data_dir=data.get('data_dir'),
            staging_dir=data.get('staging_dir'),
            data_file=data.get('data_file')
        )