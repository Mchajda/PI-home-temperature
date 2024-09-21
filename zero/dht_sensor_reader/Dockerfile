FROM python:3.9-slim

# Install dependencies for the Adafruit DHT library
RUN apt-get update && \
    apt-get install -y build-essential python3-dev libgpiod-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python libraries
RUN pip install --no-cache-dir Adafruit_DHT requests

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY app.py /app/

# Run the script
CMD ["python", "app.py"]
