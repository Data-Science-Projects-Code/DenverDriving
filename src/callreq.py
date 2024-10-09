import requests

# Direct link to the file (try first or second link)
url = "https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/arcgis/rest/services/ODC_CRIME_TRAFFICACCIDENTS5YR_P/FeatureServer/replicafilescache/ODC_CRIME_TRAFFICACCIDENTS5YR_P_1817589215432503270.csv"

# Alternative signed URL if the first one doesn't work
# url = "https://stg-arcgisazurecdataprod1.az.arcgis.com/exportfiles-7647-160430/ODC_CRIME_TRAFFICACCIDENTS5YR_P_1817589215432503270.csv?sv=2018-03-28&sr=b&sig=1i1p8lienRQJZE+gxnz37NLql2wJKmt/Jf6UHL53trc=&se=2024-09-27T19:50:55Z&sp=r"

# Download the CSV file
response = requests.get(url)

# Save the file locally
if response.status_code == 200:
    with open("../data/denver_accidents.csv", "wb") as f:
        f.write(response.content)
    print("File downloaded successfully!")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
