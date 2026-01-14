#!/usr/bin/env python3

import redis
import requests
import time
from requests.auth import HTTPBasicAuth

# Redis configuration
redis_host = "127.0.0.1"  # Redis address
redis_port = 6379         # Redis standard port
redis_password = "redispassword"     # Redis password (if required)

# Domoticz configuration
domoticz_url = "http://127.0.0.1:8080/json.htm"
domoticz_username = "domoticzusername"  # Replace with your Domoticz username
domoticz_password = "domoticzpassword"  # Replace with your Domoticz password

# Map of hset key name -> sensor IDs
sensors_map = {
    "DHT22PicoW01": {"temp_humidity": 77, "vcc": 79},
    "DHT22PicoW02": {"temp_humidity": 78, "vcc": 80},
    "BME280PicoW01": {"temp_hum_pressure": 84, "vcc": 85},
}


# Connection to Redis
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Time interval in seconds (e.g., 60 seconds for 1 minute)
time_interval = 60

try:
    while True:
        for key, sensor_ids in sensors_map.items():
            # Fetch data from Redis
            data = r.hgetall(key)

            if data:
                temperature = data.get("temperature")
                humidity = data.get("humidity")
                pressure = data.get("pressure")
                vcc = data.get("vcc")

                # Check and send temperature and humidity data
                if "temp_humidity" in sensor_ids and (temperature is not None or humidity is not None):
                    svalue_temp_humidity = f"{temperature or ''};{humidity or ''};0"
                    params_temp_humidity = {
                        "type": "command",
                        "param": "udevice",
                        "idx": sensor_ids["temp_humidity"],
                        "svalue": svalue_temp_humidity
                    }
                    #print(f"Sending to Domoticz (temp_humidity): {params_temp_humidity}")  # Debugging output

                    response_temp_humidity = requests.get(domoticz_url, params=params_temp_humidity, auth=HTTPBasicAuth(domoticz_username, domoticz_password))

                    if response_temp_humidity.status_code == 200:
                        print(f"Temperature and humidity data for sensor {key} successfully sent to Domoticz.")
                    else:
                        print(f"Error: {response_temp_humidity.status_code} - {response_temp_humidity.text}")

                # Check and send temperature, humidity, and pressure data
                if "temp_hum_pressure" in sensor_ids and (temperature is not None or humidity is not None or pressure is not None):
                    hum_status = 0  # Replace with actual calculation if available
                    baro_fcst = 0   # Replace with actual forecast value if available
                    svalue_temp_hum_pressure = f"{temperature or ''};{humidity or ''};{hum_status};{pressure or ''};{baro_fcst}"
                    params_temp_hum_pressure = {
                        "type": "command",
                        "param": "udevice",
                        "idx": sensor_ids["temp_hum_pressure"],
                        "svalue": svalue_temp_hum_pressure
                    }
                    #print(f"Sending to Domoticz (temp_hum_pressure): {params_temp_hum_pressure}")  # Debugging output

                    response_temp_hum_pressure = requests.get(domoticz_url, params=params_temp_hum_pressure, auth=HTTPBasicAuth(domoticz_username, domoticz_password))

                    if response_temp_hum_pressure.status_code == 200:
                        print(f"Temperature, humidity, and pressure data for sensor {key} successfully sent to Domoticz.")
                    else:
                        print(f"Error: {response_temp_hum_pressure.status_code} - {response_temp_hum_pressure.text}")

                # Check and send pressure data
                if "pressure" in sensor_ids and pressure is not None:
                    params_pressure = {
                        "type": "command",
                        "param": "udevice",
                        "idx": sensor_ids["pressure"],
                        "svalue": pressure
                    }
                    #print(f"Sending to Domoticz (pressure): {params_pressure}")  # Debugging output

                    response_pressure = requests.get(domoticz_url, params=params_pressure, auth=HTTPBasicAuth(domoticz_username, domoticz_password))

                    if response_pressure.status_code == 200:
                        print(f"Pressure data for sensor {key} successfully sent to Domoticz.")
                    else:
                        print(f"Error: {response_pressure.status_code} - {response_pressure.text}")

                # Check and send vcc data
                if "vcc" in sensor_ids and vcc is not None:
                    params_vcc = {
                        "type": "command",
                        "param": "udevice",
                        "idx": sensor_ids["vcc"],
                        "svalue": vcc
                    }
                    #print(f"Sending to Domoticz (vcc): {params_vcc}")  # Debugging output

                    response_vcc = requests.get(domoticz_url, params=params_vcc, auth=HTTPBasicAuth(domoticz_username, domoticz_password))

                    if response_vcc.status_code == 200:
                        print(f"VCC data for sensor {key} successfully sent to Domoticz.")
                    else:
                        print(f"Error: {response_vcc.status_code} - {response_vcc.text}")

            else:
                print(f"Key {key} does not exist in Redis.")

        # Wait for the specified time interval before repeating
        time.sleep(time_interval)

except Exception as e:
    print(f"An error occurred: {e}")

