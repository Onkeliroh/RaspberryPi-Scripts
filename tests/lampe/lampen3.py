import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(14,gpio.OUT)


for i in range(25):
	gpio.output(14, gpio.HIGH)
	time.sleep(3)

gpio.cleanup()

