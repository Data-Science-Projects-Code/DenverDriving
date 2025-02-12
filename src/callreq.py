import logging
import os
import pandas as pd
import requests
from requests.exceptions import RequestException

# Constants for directories and URLs
DATA_DIR = "data"
LOG_FILE = os.path.join(DATA_DIR, "data_processing.log")
FILE_PATH = os.path.join(DATA_DIR, "denver_accidents.csv")
ACCIDENTS_URL = "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/arcgis/rest/services/ODC_CRIME_TRAFFICACCIDENTS5YR_P/FeatureServer/replicafilescache/ODC_CRIME_TRAFFICACCIDENTS5YR_P_1817589215432503270.csv"


def setup_logging():
    """Setup logging to file and console."""
    os.makedirs(DATA_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    logging.info("Logging setup complete.")


def ensure_data_directory_exists():
    """Ensure the data directory exists; create it if it does not."""
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logging.info(f"Created directory: {DATA_DIR}")
        else:
            logging.info(f"Directory already exists: {DATA_DIR}")
    except Exception as e:
        logging.error(f"Error creating data directory: {e}")
        raise


def fetch_accident_data() -> pd.DataFrame:
    """Download accident data from the provided URL and return as a DataFrame."""
    try:
        headers = {"Cache-Control": "no-cache"}
        logging.info(f"Attempting to download data from {ACCIDENTS_URL}")
        response = requests.get(ACCIDENTS_URL, headers=headers)
        response.raise_for_status()
        logging.info("Denver accident data downloaded successfully.")

        # Read the downloaded data into a DataFrame
        df = pd.read_csv(pd.compat.StringIO(response.text))
        logging.info(
            f"Data successfully read into DataFrame with columns: {df.columns.tolist()}"
        )
        return df
    except RequestException as req_err:
        logging.error(f"Error fetching accident data: {req_err}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading the data: {e}")
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
    setup_logging()
    logging.info("Data processing script started.")
    try:
        denver_accidents = fetch_accident_data()
        save_accident_data(denver_accidents)
    except Exception as e:
        logging.error(f"An unexpected error occurred during data processing: {e}")
        logging.error("Process terminated due to the error.")
    logging.info("Data processing script completed successfully.")


if __name__ == "__main__":
    main()
