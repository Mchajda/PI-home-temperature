import machine
import network
import urequests
import time
import dht

# Replace these with your Wi-Fi credentials
SSID = "network_name"
PASSWORD = "network_password"
ROOM_NAME = "room_name"

# Connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    print("Connected! IP Address:", wlan.ifconfig()[0])

# Send data with timestamp
def send_data(temp, humidity):
    url = "http://192.168.138.2:5000/data"
    data = {"temperature": str(temp), "humidity": str(humidity), "room": ROOM_NAME}  # Include timestamp in data
    headers = {"Content-Type": "application/json"}
    response = urequests.post(url, json=data, headers=headers)
    print("Response:", response.text)
    response.close()

# Function to blink the onboard LED
def blink_led(times, interval):
    led = machine.Pin("LED", machine.Pin.OUT)  # Onboard LED is connected to pin "LED"
    for _ in range(times):
        led.value(1)  # Turn LED on
        time.sleep(interval)
        led.value(0)  # Turn LED off
        time.sleep(interval)

# Define the pin where the DHT11 sensor is connected
def read_dht_sensor():
    sensor = dht.DHT11(machine.Pin(16))  # Adjust pin number if necessary
    try:
        sensor.measure()  # Measure the sensor
        temp = sensor.temperature()  # Get temperature
        humidity = sensor.humidity()  # Get humidity
        print("Temperature: {} C".format(temp))
        print("Humidity: {} %".format(humidity))
        return (temp, humidity)
    except OSError as e:
        print("Failed to read sensor:", e)
        return None  # Return None if reading fails
    
def read_lm_temperature():
    # Set up the ADC pin where LM35 is connected (GP26/ADC0)
    adc = machine.ADC(26)  # Pin 26 is GP26/ADC0
    # Read the raw ADC value (0-65535 for 16-bit resolution)
    raw_value = adc.read_u16()
    
    # Convert raw ADC value to voltage (Pico is 3.3V)
    voltage = (raw_value / 65535.0) * 3.3
    
    # Convert voltage to temperature (LM35 gives 10mV per degree Celsius)
    temperature = voltage / 0.01
    
    return temperature

# Main function
def main():
    blink_led(3, 0.1) 
    connect_to_wifi()

    while True:
        blink_led(3, 0.5)
        # Check if sensor read was successful
        # LM35 sensor
        temperature = read_lm_temperature()
        # (temperature, humidity) = read_dht_sensor()

        if temperature is not None:
            send_data(temperature, 'none')
            # send_data(temperature, humidity)
        else:
            print("Skipping data sending due to sensor read failure.")

        # Put Pico W into light sleep for 0.5 hour (1800 seconds)
        print("Going to light sleep for 0.5 hour...")
        time.sleep(1800)

main()

