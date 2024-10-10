import logging
import os
import sys
import requests
import pandas as pd
from datetime import datetime, timezone
from requests.exceptions import RequestException

# Set up logging (file + console)
log_file = "data_processing.log"
logging.basicConfig(
    filename=log_file,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,  # Changed to DEBUG to capture more details
)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# Constants for directories and URLs
DATA_DIR = "data"
ACCIDENTS_FILE = "denver_accidents.csv"
ACCIDENTS_URL = "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/arcgis/rest/services/ODC_CRIME_TRAFFICACCIDENTS5YR_P/FeatureServer/replicafilescache/ODC_CRIME_TRAFFICACCIDENTS5YR_P_1817589215432503270.csv"


def fetch_accident_data() -> bytes:
    """
    Fetch accident data from the specified URL and return it as bytes.
    Raises an exception if the data cannot be fetched.
    """
    try:
        headers = {"Cache-Control": "no-cache"}
        logging.debug(f"Attempting to download data from {ACCIDENTS_URL}")
        response = requests.get(ACCIDENTS_URL, headers=headers, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        logging.info("Denver accident data downloaded successfully.")
        return response.content
    except RequestException as req_err:
        logging.error(f"Error fetching accident data: {req_err}")
        raise


def save_accident_data(file_content: bytes) -> None:
    """
    Save the accident data to a CSV file within the data directory.
    Creates the data directory if it does not exist.
    """
    try:
        # Ensure the data directory exists
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logging.info(f"Created directory: {DATA_DIR}")

        file_path = os.path.join(DATA_DIR, ACCIDENTS_FILE)
        with open(file_path, "wb") as file:
            file.write(file_content)
        logging.info(f"Data successfully saved to {file_path}")

    except Exception as e:
        logging.error(
            f"An unexpected error occurred while saving the data: {e}")
        raise


def main():
    logging.info("Data processing script started.")
    try:
        # Fetch and save the accident data
        accident_data = fetch_accident_data()
        save_accident_data(accident_data)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

    logging.info("Data processing script completed successfully.")


if __name__ == "__main__":
    main()

