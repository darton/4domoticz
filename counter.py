#!/usr/bin/env python3

from gpiozero import Button
from signal import pause
from urllib.request import urlopen
import ssl

button = Button(23,bounce_time=0.05)

def button_action():
    response = urlopen('https://127.0.0.1/json.htm?type=command&param=udevice&idx=50&svalue=1', context=ssl._create_unverified_context())

button.when_pressed = button_action

pause()
