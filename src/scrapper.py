from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
from os import path
import pandas as pd

# Navegador
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa em modo headless
chrome_options.add_argument("--disable-gpu")  # Desabilita GPU
chrome_options.add_argument("--no-sandbox")  # Desabilita sandbox

service = Service(ChromeDriverManager().install())

from selenium.common.exceptions import TimeoutException
from pandas import DataFrame

class Scrapper:
    """Classe para executar a extração por WebScrapping"""
    def __init__(self, url:str, service:object=service, options:object=chrome_options):
        self.url = url
        self.driver = webdriver.Chrome(service=service, options=options)
        self.data = {
            'ID':[],
            'Company_Name': [],
            'Status': [],
            'Date': [],
            'Report': [],
            'Company_Response': [],
            'Response_Date': [],
            'Rating_Score': [],
            'Consumer_Written_Evaluation': []
        }

    def open_url(self, url: str) -> bool:
        """Abre a URL e espera o elemento 'resultados' ser carregado"""
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "resultados"))
            )
            return True
        except Exception as e:
            print(f"Erro ao abrir a URL: {e}")
            return False

    def get_html(self) -> str:
        """Obtém o HTML da página atual"""
        try:
            return self.driver.page_source
        except Exception as e:
            print(f"Erro ao obter o HTML: {e}")
            return ""

    def get_cards(self) -> list:
        """Obtém os cards dos relatos da página"""
        html = self.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find('div', id='resultados')
        if not results:
            return []
        relates = results.find_all(
            'div',
            class_='cartao-relato col-lg-12 col-md-12 col-sm-12 col-xs-12 conteudoEstatico'
        )
        return relates

    def click_more_results(self, total_relates: int = 50_000):
        """Clica no botão "Carregar mais resultados".
        Args:
            total_relates (int, optional): Número de relatos. Defaults to 50_000.
        """
        pages = total_relates / 10
        counter = 0
        while counter < pages:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "btn-mais-resultados"))
                )
                button = self.driver.find_element(By.ID, "btn-mais-resultados")
                print(f"Carregando mais resultados: ({counter + 1}/{pages})")
                if button.is_displayed() and button.is_enabled():
                    self.driver.execute_script("arguments[0].click();", button)
                    sleep(5) 
                    counter += 1
                else:
                    break
            except Exception as e:
                print("Erro ao clicar no botão:", e)
                break

    def scrap(self, lines: int = 50_000):
        """Executa o scrapping dos relatos.
        Args:
            lines (int, optional): Número de relatos. Defaults to 50_000.
        """
        if not self.open_url(self.url):
            return

        self.click_more_results(total_relates=lines)
        relates = self.get_cards()

        for index, relate in enumerate(relates):
            self.data['ID'].append(index)
            # Nome da empresa
            company_name = relate.find('h3', class_='relatos-nome-empresa')
            self.data['Company_Name'].append(company_name.get_text(strip=True) if company_name else None)
            # Status do relato
            report_status = relate.find('h4', class_='relatos-status')
            self.data['Status'].append(report_status.get_text(strip=True) if report_status else None)
            # Data do relato
            report_date = relate.find('span', class_='relatos-data')
            self.data['Date'].append(report_date.get_text(strip=True) if report_date else None)
            # Texto do relato
            report_text = relate.find('p', style='word-wrap: break-word;')
            self.data['Report'].append(report_text.get_text(strip=True) if report_text else None)
            # Resposta da empresa
            company_response = relate.find_all('strong', string='Resposta')
            response_text = company_response[0].find_next('p') if company_response else None
            self.data['Company_Response'].append(response_text.get_text(strip=True) if response_text else None)
            # Data da resposta
            response_date = relate.find_all('span', class_='relatos-data')
            self.data['Response_Date'].append(response_date[1].get_text(strip=True) if len(response_date) > 1 else None)
            # Avaliação (nota)
            rating = relate.find('strong', string='Avaliação')
            rating_score = rating.find_next('p') if rating else None
            self.data['Rating_Score'].append(rating_score.get_text(strip=True) if rating_score else None)
            # Avaliação escrita
            all_p = relate.find_all('p')
            evaluation = all_p[3] if len(all_p) > 3 else None
            self.data['Consumer_Written_Evaluation'].append(
                evaluation.get_text(strip=True) if evaluation else None
            )

    def get_dataframe(self) -> DataFrame:
        """Converte os dados extraídos em um DataFrame do pandas.
        Returns:
            DataFrame:
        """
        return DataFrame(self.data)

    def save_data(self, data_dir: str, filename: str, format: str = 'csv'):
        """Salva os dados extraídos em um arquivo.
        Args:
            data_dir (str): Diretório onde o arquivo será salvo.
            filename (str): Nome do arquivo.
            format (str): Formato do arquivo ('csv', 'json', 'xlsx').
        """
        full_path = path.join(data_dir, f"{filename}.{format}")
        
        if not path.exists(data_dir):
            raise FileNotFoundError(f"Diretório {data_dir} não existe.")
        
        dataframe = self.get_dataframe()
        # Check if dataframe file exists
        if path.exists(full_path):
            current_dataframe = pd.read_csv(full_path, encoding="utf-8-sig", sep='|')
            dataframe = pd.concat([current_dataframe, dataframe], ignore_index=True)
        
        try:
            match format:
                case 'csv':
                    dataframe.to_csv(full_path, sep='|', index=False, encoding="utf-8-sig")
                case 'json':
                    dataframe.to_json(full_path, orient='records', lines=True, force_ascii=False)
                case 'xlsx':
                    dataframe.to_excel(full_path, index=False)
                case _:
                    raise ValueError("Formato não suportado. Use 'csv', 'json' ou 'xlsx'.")
        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")
            raise    

    def close(self):
        self.driver.quit()
