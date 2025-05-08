import logging
from src.backend.extract.extract import Extract
from src.config import Config
import os

config = Config()

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def execute_data_extraction(test:bool = False, lines:int = 50_000):
    """Function that executes the data extraction process from the Consumidor.gov.br platform reports."""

    file = config.env_vars.data_file

    if test:
        lines = 100_000
        file += '-100_000'
        
    try:
        # Create the Extract object with default settings
        logger.info("Starting the data extraction process.")
        extractor = Extract(lines=lines, quantity=10)
        # Making the request and extracting the reports
        logger.info("Fetching reports...")
        extractor.fetch_reports()
        # Scraping the extracted reports
        logger.info("Starting the scraping of the reports...")
        extractor.scrap()
        # Saving the extracted data to a file
        staging_area = os.path.join(config.project_dir, config.env_vars.data_dir, config.env_vars.staging_dir)
        if not os.path.exists(staging_area):
            logger.info(f"Creating Staging Area at {staging_area}...")
            os.makedirs(staging_area)

        logger.info(f"Saving data to Staging Area {staging_area}...")
        extractor.save_data(staging_area, file, format='csv')

        logger.info("Data extraction process completed successfully!")

    except Exception as e:
        logger.error(f"An error occurred during the extraction process: {e}")
        extractor.save_data(staging_area, file, format='csv')

if __name__ == "__main__":
    execute_data_extraction(test=True)