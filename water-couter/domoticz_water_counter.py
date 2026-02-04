#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gpiozero import Button
from signal import pause
import requests
from requests.auth import HTTPBasicAuth
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Konfiguracja – zmień na swoje wartości
DOMOTICZ_URL = "http://127.0.0.1:8080/json.htm"
IDX_LICZNIK = 50
IMPULSES_PER_LITER = 1000       # np. wodomierz daje 1000 imp/m³
SEND_EVERY_N_IMPULSES = 10      # wysyłaj co 10 impulsów → 0.01 m³
USERNAME = "admin"
PASSWORD = "twoje_haslo_lub_lepiej_api_key"

auth = HTTPBasicAuth(USERNAME, PASSWORD)

def create_counter():
    count = 0
    last_sent = 0

    def on_pulse():
        nonlocal count, last_sent
        count += 1
        logging.info(f"Impuls #{count}")

        if count - last_sent >= SEND_EVERY_N_IMPULSES:
            value = count / IMPULSES_PER_LITER   # np. 0.010 m³
            url = f"{DOMOTICZ_URL}?type=command&param=udevice&idx={IDX_LICZNIK}&svalue={value:.3f}"
            try:
                r = requests.get(url, auth=auth, timeout=5)
                r.raise_for_status()
                logging.info(f"Wysłano {value:.3f} → HTTP {r.status_code}")
                last_sent = count
            except Exception as e:
                logging.error(f"Błąd wysyłania: {e}")

    return on_pulse



pulse_handler = create_counter()

btn = Button(18, bounce_time=0.05)
btn.when_pressed = pulse_handler

logging.info("Licznik wodomierza uruchomiony – czekam na impulsy...")
pause()