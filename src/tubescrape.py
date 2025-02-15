from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)
import time

# Initialize the driver
driver = webdriver.Chrome()  # Ensure you have the correct driver installed


def download_data():
    try:
        driver.get(
            "https://opendata-geospatialdenver.hub.arcgis.com/datasets/geospatialDenver::traffic-accidents-offenses/explore?location=39.758664%2C-104.945587%2C9.60"
        )

        # Wait for the page to fully load
        time.sleep(5)  # Ensure all JavaScript elements load properly

        # Wait for the Download button to be clickable
        print("Waiting for Download button to be clickable...")
        try:
            download_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[contains(text(), "Download")]')
                )
            )
            print("Download button found, attempting to click...")
            download_button.click()
        except TimeoutException:
            print("Error: Download button not found within the timeout period.")
            return
        except ElementClickInterceptedException:
            print("Download button could not be clicked normally, using JavaScript.")
            driver.execute_script("arguments[0].click();", download_button)

        # Wait for the side panel to appear and click the CSV download button
        print("Waiting for side panel to appear...")
        try:
            csv_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[contains(@class, "download-list")]//*[contains(text(), "CSV")]',
                    )
                )
            )
            print("CSV button found, attempting to click...")
            csv_button.click()
        except TimeoutException:
            print("Error: CSV download button not found within the timeout period.")
            return
        except ElementClickInterceptedException:
            print("CSV button could not be clicked normally, using JavaScript.")
            driver.execute_script("arguments[0].click();", csv_button)

        print("Download initiated successfully")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    download_data()
