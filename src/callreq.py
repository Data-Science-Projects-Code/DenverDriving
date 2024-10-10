import os
import logging
import sys
import requests
import pandas as pd
from requests.exceptions import RequestException

# Set up logging (file + console)
log_file = "data_processing.log"
logging.basicConfig(
    filename=log_file,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# Constants for directories and URLs
DATA_DIR = "data"
FILE_NAME = "denver_accidents.csv"
ACCIDENTS_URL = "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/arcgis/rest/services/ODC_CRIME_TRAFFICACCIDENTS5YR_P/FeatureServer/replicafilescache/ODC_CRIME_TRAFFICACCIDENTS5YR_P_1817589215432503270.csv"


def create_data_directory(directory: str) -> None:
    """
    Create the data directory if it doesn't exist.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
    else:
        logging.info(f"Directory already exists: {directory}")


def fetch_accident_data() -> pd.DataFrame:
    """
    Fetch accident data from the specified URL.
    """
    try:
        headers = {"Cache-Control": "no-cache"}
        response = requests.get(ACCIDENTS_URL, headers=headers)
        response.raise_for_status()
        logging.info("Denver accident data downloaded successfully.")
        return pd.read_csv(
            response.content.decode("utf-8")
        )  # Load the CSV data into a DataFrame
    except RequestException as req_err:
        logging.error(f"Error fetching accident data: {req_err}")
        raise


def save_accident_data(df: pd.DataFrame, directory: str, file_name: str) -> None:
    """
    Save the accident data DataFrame to a CSV file.
    """
    file_path = os.path.join(directory, file_name)
    try:
        df.to_csv(file_path, index=False)
        logging.info(f"Data saved successfully to {file_path}")
    except Exception as e:
        logging.error(f"Error saving data to {file_path}: {e}")
        raise


def main():
    logging.info("Data processing script started.")

    try:
        # Ensure the data directory exists
        create_data_directory(DATA_DIR)

        # Fetch accident data
        denver_accidents = fetch_accident_data()

        # Save the data to the CSV file in the data directory
        save_accident_data(denver_accidents, DATA_DIR, FILE_NAME)

    except FileNotFoundError as fnf_error:
        logging.error(f"File not found: {fnf_error}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

    logging.info("Data processing script completed successfully.")
    print("Data downloaded and saved as a CSV file.")


if __name__ == "__main__":
    main()

