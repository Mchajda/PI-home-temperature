import time
import requests
import Adafruit_DHT

# Set sensor type and GPIO pin
DHT_SENSOR = Adafruit_DHT.DHT22  # Change to Adafruit_DHT.DHT11 if using DHT11
DHT_PIN = 4  # GPIO pin connected to the DATA pin of the sensor

# API endpoint of your existing web server
API_URL = 'http://localhost:5000/data'  # Assuming the web server runs on port 5000

def read_and_send_data():
    while True:
        # Read data from the DHT sensor
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        
        if humidity is not None and temperature is not None:
            data = {
                'temperature': temperature,
                'humidity': humidity,
                'room': 'room_name',  # Identifier for the data source
                'timestamp': time.strftime('%d/%m/%Y %H:%M:%S')
            }
            try:
                # Send data to the web server
                response = requests.post(API_URL, json=data)
                print(f"Data sent: {data}, Response code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send data: {e}")
        else:
            print("Failed to retrieve data from the sensor")
        
        # Wait for a specified interval before reading again
        time.sleep(1800)  # Read every 60 seconds

if __name__ == '__main__':
    read_and_send_data()
