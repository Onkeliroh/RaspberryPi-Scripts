import RPi.GPIO as gpio
import time

gpio.cleanup()

gpio.setmode(gpio.BCM)

gpio.setup(14, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(18, gpio.OUT)

#gpio.output(14, gpio.LOW)
#gpio.output(15, gpio.LOW)
#gpio.output(18, gpio.LOW)

for i in range(10):
	gpio.output(14, gpio.HIGH)
	time.sleep(0.5)
	gpio.output(15, gpio.HIGH)
	time.sleep(0.5)
	gpio.output(18, gpio.HIGH)
	time.sleep(0.5)
	gpio.output(14, gpio.LOW)
	time.sleep(0.5)
	gpio.output(15, gpio.LOW)
	time.sleep(0.5)
	gpio.output(18, gpio.LOW)
	time.sleep(0.5)
	
gpio.cleanup()
