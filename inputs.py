#!/usr/bin/env python3

# -*- coding:utf-8 -*-
#
#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

from gpiozero import Button
from signal import pause
from urllib.request import urlopen
import ssl



#51-57 it is idx values from domoticz virtual switches
inputs_map = {
    "51" : Button(5, hold_time=0.2),
    "52" : Button(6, hold_time=0.2),
    "53" : Button(22, hold_time=0.2),
    "54" : Button(23, hold_time=0.2),
    "55" : Button(24, hold_time=0.2),
    "56" : Button(26, hold_time=0.2),
    "57" : Button(27, hold_time=0.2)
}

def input_action_H2L(input_id):
    print("The idx=" + str(input_id) + " has been changed to 0")
    response = urlopen('https://127.0.0.1/json.htm?type=command&param=udevice&idx=' + str(input_id) + '&svalue=0', context=ssl._create_unverified_context())

def input_action_L2H(input_id):
    print("The idx=" + str(input_id) + " has been changed to 1")
    response = urlopen('https://127.0.0.1/json.htm?type=command&param=udevice&idx=' + str(input_id) + '&svalue=1', context=ssl._create_unverified_context())

# --- Main program ---
for s in inputs_map:
    inputs_map[s].when_held = lambda s=s : input_action_H2L(s)
    inputs_map[s].when_released = lambda s=s : input_action_L2H(s)

pause()
