import machine
import network
import urequests
import time
import dht

SSID = "network_name"
PASSWORD = "network_password"
ROOM_NAME = "room_name"

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        time.sleep(1)
    print("Connected! IP Address:", wlan.ifconfig()[0])

def send_data(temp, humidity):
    try:
        url = "http://192.168.138.2:5000/data"
        data = {"temperature": str(temp), "humidity": str(humidity), "room": ROOM_NAME}
        headers = {"Content-Type": "application/json"}
        response = urequests.post(url, json=data, headers=headers)
        print("Response:", response.text)
        response.close()
    except:
        print("Failed to send data to server.")

def blink_led(times, interval):
    led = machine.Pin("LED", machine.Pin.OUT)
    for _ in range(times):
        led.value(1)
        time.sleep(interval)
        led.value(0)
        time.sleep(interval)

def read_dht_sensor():
    sensor = dht.DHT11(machine.Pin(16))
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        print("Temperature: {} C".format(temp))
        print("Humidity: {} %".format(humidity))
        return (temp, humidity)
    except OSError as e:
        print("Failed to read sensor:", e)
        return None
    
def read_lm_temperature():
    adc = machine.ADC(26)
    raw_value = adc.read_u16()
    voltage = (raw_value / 65535.0) * 3.3
    temperature = voltage / 0.01
    
    return temperature

# Main function
def main():
    blink_led(3, 0.1) 
    connect_to_wifi()

    while True:
        blink_led(3, 0.5)
        
        # temperature = read_lm_temperature()
        (temperature, humidity) = read_dht_sensor()

        if temperature is not None:
            # send_data(temperature, 'none')
            send_data(temperature, humidity)
        else:
            print("Skipping data sending due to sensor read failure.")

        print("Going to light sleep for 0.5 hour...")
        time.sleep(1800)

main()
