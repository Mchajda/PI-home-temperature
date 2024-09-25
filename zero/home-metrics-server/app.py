from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_formatted_time():
    # Get the current time using the datetime module
    current_time = datetime.now()

    # Extract day, month, year, hour, minute, second
    day = current_time.day
    month = current_time.month
    year = current_time.year
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second

    # Format the time as "DD/MM/YYYY HH:MM:SS"
    formatted_time = "{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(day, month, year, hour, minute, second)

    return formatted_time

# Define a route to receive POST requests and save data to a text file
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json  # Get JSON data from the request
    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400

    conn = sqlite3.connect('/app/data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS metrics (temperature TEXT, humidity TEXT, date TEXT, room TEXT)''')
    c.execute("INSERT INTO metrics (temperature, humidity, date, room) VALUES (?, ?, ?, ?)", (data['temperature'], data['humidity'], get_formatted_time(), data['room']))

    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Data saved'}), 200

@app.route('/data', methods=['GET'])
def return_data():
    conn = sqlite3.connect('/app/data.db')
    c = conn.cursor()

    c.execute('SELECT * FROM metrics')
    rows = c.fetchall()
    conn.close()

    return jsonify({'status': 'success', 'data': rows}), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    # Run the Flask app on port 5000, accessible on all network interfaces (0.0.0.0)
    app.run(host='0.0.0.0', port=5000)

