from dagster import asset, Output, MetadataValue
import requests
import json
import pandas as pd

CSV_FILE_PATH = "weather_data.csv"

@asset
def fetch_weather_data():
    """Fetches weather data from Open-Meteo API and returns JSON."""
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&hourly=temperature_2m"
    response = requests.get(url)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"API request failed with status {response.status_code}")

@asset
def process_weather_data(fetch_weather_data):
    """Processes JSON data and saves it to CSV, then materializes it."""
    data = fetch_weather_data
    df = pd.DataFrame({"Timestamp": data["hourly"]["time"], "Temperature (C)": data["hourly"]["temperature_2m"]})
    
    # Save to CSV
    df.to_csv(CSV_FILE_PATH, index=False)

    # Return as a Dagster Output (so we can materialize it)
    return Output(
        value=df,
        metadata={
            "csv_path": MetadataValue.path(CSV_FILE_PATH),
            "preview": MetadataValue.md(df.head().to_markdown())  # Show preview in Dagster UI
        }
    )
