#!/usr/bin/env python3

from gpiozero import Button
from signal import pause
import requests
from requests.auth import HTTPBasicAuth
import ssl

counter = Button(18,bounce_time=0.05)

USERNAME = "admin"
PASSWORD = "password"


def counter_action():
    base_url = 'http://127.0.0.1:8080/json.htm'
    url = f'{base_url}?type=command&param=udevice&idx=50&svalue=1'
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    #print(response)

counter.when_pressed = counter_action

pause()
