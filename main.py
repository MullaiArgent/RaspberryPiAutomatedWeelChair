import tm1637
import time
import os
import RPi.GPIO as GPIO
from pad4pi import rpi_gpio
from datetime import datetime
from playsound import playsound
import threading

tm = tm1637.TM1637(clk=5, dio=23)
key = 0
motor1F = 26
motor1R = 19
motor2F = 13
motor2R = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor1F, GPIO.OUT)
GPIO.output(motor1F, 0)
GPIO.setup(motor1R, GPIO.OUT)
GPIO.output(motor1R, 0)
GPIO.setup(motor2F, GPIO.OUT)
GPIO.output(motor2F, 0)
GPIO.setup(motor2R, GPIO.OUT)
GPIO.output(motor2R, 0)

KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [4, 14, 15, 17]  # BCM numbering
COL_PINS = [18, 27, 22]  # BCM numbering

factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)


def printKey(key):
    print(key)
    for k in range(int(key)):
        l = key - k
        tm.number(l)
        GPIO.output(motor1F, 1)
        GPIO.output(motor2F, 1)
        time.sleep(0.5)
        GPIO.output(motor1F, 0)
        GPIO.output(motor2F, 0)
        time.sleep(0.5)
        GPIO.output(motor1R, 1)
        GPIO.output(motor2R, 1)
        time.sleep(0.5)
        GPIO.output(motor1R, 0)
        GPIO.output(motor2R, 0)
        time.sleep(0.5)
    tm.write([0b00000110, 0b01010100, 0b01110011, 0b01111000])


# printKey will be called each time a keypad button is pressed

i = keypad.registerKeyPressHandler(printKey)


def alarm():
    def play(str):
        playsound(str)

    test = None
    test1 = None
    test2 = None
    test3 = None
    while not i:
        if str(datetime.today().strftime("%I:%M %p")) == "07:55 AM" and test is None:
            test = 1
            play("in5min.mp3")
        elif str(datetime.today().strftime("%I:%M %p")) == "08:00 AM" and test1 is None:
            test1 = 1
            play("mrng.mp3")
        elif str(datetime.today().strftime("%I:%M %p")) == "03:55 PM" and test2 is None:
            test2 = 1
            play("in5min.mp3")
        elif str(datetime.today().strftime("%I:%M %p")) == "04:00 PM" and test3 is None:
            test3 = 1
            play("evng.mp3")

t = threading.Thread(target=alarm(), args=())

tm.write([0b00000110, 0b01010100, 0b01110011, 0b01111000])
time.sleep(3)
