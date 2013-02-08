#dieses Programm wird einen Schalter zum Ein- und Ausschalten einer LED nutzen

import RPi.GPIO as gpio


gpio.setmode(gpio.BCM)

#set up pin 14 as input
gpio.setup(14, gpio.IN)

while True:
	input_value = gpio.input(14)
	if input_value == False:
		print('The Button has been pressed.... :)')
		while input_value == False:
			input_value = gpio.input(14)
