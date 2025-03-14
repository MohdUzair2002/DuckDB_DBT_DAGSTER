FROM python:3.10-slim

# # Set environment variables
# ENV PYTHONUNBUFFERED=1 \
#     DBT_PROFILES_DIR=/root/.duck_db_project \
#     DAGSTER_HOME=/app/dagster_home \
#     DBT_PROJECT_DIR=/app/duck_db_project 

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Set up the application directory
WORKDIR /app

# Create required directories
RUN mkdir -p /app/dbtdagster /app/dagster_home /app/duck_db_project /root/.dbt

# Copy project files
COPY . /app

# Move profiles.yml to the correct dbt directory inside Docker
COPY duck_db_project/profiles.yml /root/.duck_db_project/profiles.yml

# Set permissions to avoid permission errors
RUN chmod -R 777 /app /root/.dbt

# Set the default command to execute dbt commands before starting Dagster
CMD ["sh", "-c", "cd /app/duck_db_project && dbt seed && dbt run && cd /app && dagster dev --host 0.0.0.0 --port 3003"]

