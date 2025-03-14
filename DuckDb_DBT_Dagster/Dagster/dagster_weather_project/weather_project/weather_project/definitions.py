from dagster import Definitions, define_asset_job, ScheduleDefinition
from .assets import fetch_weather_data, process_weather_data

# Define a job to materialize assets
materialize_weather_data_job = define_asset_job("materialize_weather_data")

# Define a schedule referencing the job
weather_data_schedule = ScheduleDefinition(
    job=materialize_weather_data_job,
    cron_schedule="0 0 * * *",  # Runs daily at midnight
)

# Register assets, jobs, and schedules
defs = Definitions(
    assets=[fetch_weather_data, process_weather_data],
    jobs=[materialize_weather_data_job],  # Ensure this is included
    schedules=[weather_data_schedule],
)
