import logging
import os
import pandas as pd
import requests
from requests.exceptions import RequestException

# Constants for directories and URLs
DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "denver_accidents.csv")
ACCIDENTS_URL = "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/arcgis/rest/services/ODC_CRIME_TRAFFICACCIDENTS5YR_P/FeatureServer/replicafilescache/ODC_CRIME_TRAFFICACCIDENTS5YR_P_1817589215432503270.csv"


def ensure_data_directory_exists():
    """Ensure the data directory exists; create it if it does not."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        logging.info(f"Created directory: {DATA_DIR}")
    else:
        logging.info(f"Directory already exists: {DATA_DIR}")


def fetch_accident_data() -> pd.DataFrame:
    """Download accident data from the provided URL and return as a DataFrame."""
    try:
        headers = {"Cache-Control": "no-cache"}
        logging.debug(f"Attempting to download data from {ACCIDENTS_URL}")
        response = requests.get(ACCIDENTS_URL, headers=headers)
        response.raise_for_status()
        logging.info("Denver accident data downloaded successfully.")
        return pd.read_csv(pd.compat.StringIO(response.text))
    except RequestException as req_err:
        logging.error(f"Error fetching accident data: {req_err}")
        raise
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while reading the data: {e}")
        raise


def save_accident_data(df: pd.DataFrame) -> None:
    """Save the DataFrame to a CSV file in the data directory."""
    try:
        ensure_data_directory_exists()
        df.to_csv(FILE_PATH, index=False)
        logging.info(f"Data successfully saved to {FILE_PATH}")
    except Exception as e:
        logging.error(f"Error saving data to {FILE_PATH}: {e}")
        raise


def main():
    logging.info("Data processing script started.")
    try:
        denver_accidents = fetch_accident_data()
        save_accident_data(denver_accidents)
    except Exception as e:
        logging.error(
            f"An unexpected error occurred during data processing: {e}")
    logging.info("Data processing script completed successfully.")


if __name__ == "__main__":
    main()

