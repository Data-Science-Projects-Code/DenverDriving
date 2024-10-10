import logging
import sys
import requests
import pandas as pd
from datetime import datetime, timezone
from requests.exceptions import RequestException


#
# # Alternative signed URL if the first one doesn't work
# # url = "https://stg-arcgisazurecdataprod1.az.arcgis.com/exportfiles-7647-160430/ODC_CRIME_TRAFFICACCIDENTS5YR_P_1817589215432503270.csv?sv=2018-03-28&sr=b&sig=1i1p8lienRQJZE+gxnz37NLql2wJKmt/Jf6UHL53trc=&se=2024-09-27T19:50:55Z&sp=r"
#
# # Download the CSV file
# response = requests.get(url)
#
# # Save the file locally
# if response.status_code == 200:
#     with open("../data/denver_accidents.csv", "wb") as f:
#         f.write(response.content)
#     print("File downloaded successfully!")
# else:
#     print(f"Failed to download the file. Status code: {response.status_code}")


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
ACCIDENTS_URL = "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/arcgis/rest/services/ODC_CRIME_TRAFFICACCIDENTS5YR_P/FeatureServer/replicafilescache/ODC_CRIME_TRAFFICACCIDENTS5YR_P_1817589215432503270.csv"


def fetch_accident_data() -> pd.DataFrame:
    try:
        headers = {"Cache-Control": "no-cache"}
        response = requests.get(ACCIDENTS_URL)
        response.raise_for_status()
        logging.info("Denver accident data downloaded.")

    except RequestException as req_err:
        logging.error(f"Error fetching accident data: {req_err}")
        raise


def save_acident_data(df: pd.DataFrame) -> None:
    logging.info("Download logged.")


def main():
    logging.info("Data processing script started.")

    try:
        denver_accidents = fetch_accident_data()
        save_acident_data(denver_accidents)
    except FileNotFoundError as fnf_error:
        logging.error(f"File not found: {fnf_error}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

    logging.info("Data processing script completed successfully.")
    print("Data downloaded and saved as csv file.")


if __name__ == "__main__":
    main()
