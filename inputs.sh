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
from time import sleep
from urllib.request import urlopen
#import ssl

input_1 = Button(5)
input_2 = Button(6)
input_3 = Button(22)
input_4 = Button(23)
input_5 = Button(24)
input_6 = Button(26)
input_7 = Button(27)

#51-57 it is idx values from domoticz virtual switch
inputs_list = {
    "51" : input_1,
    "52" : input_2,
    "53" : input_3,
    "54" : input_4,
    "55" : input_5,
    "56" : input_6,
    "57" : input_7
}

def input_action_H2L(input_id):
    print("The " + str(input_id) + " has been changed from H to L")
    response = urlopen('http://127.0.0.1/json.htm?type=command&param=udevice&idx=' + str(input_id) + '&svalue=0', context=ssl._create_unverified_context())

def input_action_L2H(input_id):
    print("The " + str(input_id) + " has been changed from L to H")
    response = urlopen('http://127.0.0.1/json.htm?type=command&param=udevice&idx=' + str(input_id) + '&svalue=1', context=ssl._create_unverified_context())

# --- Main program ---
for s in inputs_list:
    inputs_list[s].when_held = lambda s=s : input_action_H2L(s)
    inputs_list[s].when_released = lambda s=s : input_action_L2H(s)

pause()