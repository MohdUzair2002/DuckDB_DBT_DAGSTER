import requests
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
from dagster import job, op, Out

@op(out=Out(str))
def fetch_weather():
    """Fetches weather data from Open-Meteo API."""
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&hourly=temperature_2m"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text  # Return JSON string
    else:
        raise Exception(f"API request failed with status {response.status_code}")

@op(out=Out(str))
def process_weather(weather_json: str):
    """Processes JSON data and saves it as CSV."""
    data = json.loads(weather_json)

    timestamps = data["hourly"]["time"]
    temperatures = data["hourly"]["temperature_2m"]

    csv_filename = "weather_data.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Temperature (C)"])
        for timestamp, temperature in zip(timestamps, temperatures):
            writer.writerow([timestamp, temperature])

    return csv_filename  # Return CSV file path

@op(out=Out(str))
def visualize_weather(csv_file: str):
    """Reads CSV and generates a temperature graph."""
    df = pd.read_csv(csv_file)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    plt.figure(figsize=(10, 5))
    plt.plot(df["Timestamp"], df["Temperature (C)"], marker="o", linestyle="-", color="b")
    plt.xlabel("Timestamp")
    plt.ylabel("Temperature (°C)")
    plt.title("Hourly Temperature")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    output_image = "temperature_plot.png"
    plt.savefig(output_image)
    
    return output_image  # Return image file path

@job
def weather_pipeline():
    """Defines the full Dagster job."""
    csv_file = process_weather(fetch_weather())
    visualize_weather(csv_file)
