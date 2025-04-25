from scrapper import Scrapper
import os

URL = 'https://consumidor.gov.br/pages/indicador/relatos/abrir'
scrapper = Scrapper(url=URL)

cwd = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(cwd, 'data')
filename = 'relatos'

try:
    scrapper.scrap(lines=50_000)
except KeyboardInterrupt:
    print("\nInterrupção manual detectada no test.py. Encerrando...")
    scrapper.save_data(data_dir=data_dir, filename=filename, format='csv')
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    scrapper.save_data(data_dir=data_dir, filename=filename, format='csv')
    scrapper.close()
