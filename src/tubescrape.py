from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the driver (Make sure the correct driver is installed)
driver = webdriver.Chrome()  # Change to your preferred driver


def download_data():
    try:
        driver.get(
            "https://opendata-geospatialdenver.hub.arcgis.com/datasets/geospatialDenver::traffic-accidents-offenses/explore?location=39.758664%2C-104.945587%2C9.60"
        )

        # Wait for the Download button to be clickable
        print("Waiting for Download button to be clickable...")
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Download")]'))
        )
        print("Download button clicked!")
        download_button.click()

        # Wait for the side panel to appear and click the CSV download button
        print("Waiting for side panel to appear...")
        csv_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[contains(@class, "download-list")]//*[contains(text(), "CSV")]',
                )
            )
        )
        print("CSV button clicked!")
        csv_button.click()

        print("Download initiated successfully")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    download_data()
