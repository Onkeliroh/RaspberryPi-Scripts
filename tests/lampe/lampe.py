#dieses Programm testet nur die GPIO Funktionen mit Hilfe einer Lampe

import RPi.GPIO as gpio
import time

#set up pin 14 and 15 as output
gpio.setmode(gpio.BCM)
gpio.setup(15, gpio.OUT)
gpio.setup(14, gpio.OUT)

#Make an LED flash on and off forever
while True:
	gpio.output(15, gpio.HIGH)
	gpio.output(14, gpio.LOW)
	time.sleep(1)
	gpio.output(15, gpio.LOW)
	gpio.output(14, gpio.HIGH)
	time.sleep(1)


