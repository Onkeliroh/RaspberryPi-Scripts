#!/usr/bin/python

import sys

from mpd import (MPDClient, CommandError)
from socket import error as SocketError
from time import sleep
from time import clock
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

##Configuration
HOST		=	'peach'
PORT		=	'6600'
PASSWORD 	= 	False

##A usefull struct with host and port informations
CON_ID = {'host':HOST, 'port':PORT}
##

##Usefull functions

#connects to mpd
def mpdConnect(client, con_id):
	try:
		client.connect(**con_id)
	except SocketError:
		return False
	return True


#authentificates with mpd
def mpdAuth(client, secret):
	try:
		client.password(secret)
	except CommandError:
		return False
	return True

def startup(client, lcd):
	if mpdConnect(client, CON_ID):
		lcd.clear()
		lcd.message("Got connected!")
	else:
		lcd.clear()
		lcd.message("Error while connecting!")
		sys.exit(1)

	sleep(1)
	lcd.clear()

	
	# Auth if password is set non False
	if PASSWORD:
		if mpdAuth(client, PASSWORD):
			lcd.clear()
			lcd.message("Pass auth!")
		else:
			lcd.clear()
			lcd.message("Error trying to pass auth!")
			sys.exit(2)
	sleep(1)
	lcd.clear()
	return True

#Produces formated string for displaying the desired informations
def display_status(client, lcd):
	line0 = ""
	line1 = ""

	if client.status()['state'] == 'pause':
		#stopped
		line1 = "PAUSED"
	else :
		try:
			#try because sometimes for example streams don't have the artist name stored in 'artist' but in 'title'
			try:
				line0 = client.currentsong()['title']
				line1 = client.currentsong()['artist']
			except:
				title = client.currentsong()['title'].split(" - ")
				line0 = title[1]
				line1 = title[0]
		except:
			lcd.message("ERROR greeping Info")

	lcd.clear()
	lcd.message(line0+"\n"+line1)
	
	return True

def main():

	## MPD object instance
	client = MPDClient()
	lcd = Adafruit_CharLCDPlate(1)

	lcd.backlight(lcd.BLUE)
	lcd.clear()
	lcd.message("Wellcome to the\nMPD Interface!")
	sleep(1)

	#initialize mpd connection
	startup(client,lcd)

	#Printing first known informations on lcd
	display_status(client, lcd)

	# Poll buttons, display message & set backlight accordingly
	btn = ( (lcd.LEFT  , 'LEFT' , lcd.RED),
			(lcd.UP    , 'UP' , lcd.ON),
			(lcd.DOWN  , 'DOWN' , lcd.ON),
			(lcd.RIGHT , 'RIGHT' , lcd.GREEN),
			(lcd.SELECT, 'SELECT' , lcd.ON) )

	print client.status()

	t0 = clock()
	refresh_display = clock()
	last_change = clock()
	prev = -1
	
	while True:
		if (clock() - refresh_display >= 0.1):
			display_status(client, lcd)
			refresh_display = clock()
		
		
		for b in btn:
			#begin "if button pressed"
			if lcd.buttonPressed(b[0]):
				if (b is not prev) or (clock()-t0 >= 0.3):
					if b[0] == lcd.UP:
						vol = client.status()['volume']
						if  vol <= 95:
							vol = int(vol) + 5
						else:
							vol = 100
						client.setvol(vol)
							
					if b[0] == lcd.DOWN:
						vol = client.status()['volume']
						if  vol >= 5:
							vol = int(vol) - 5
						else:
							vol = 0
						client.setvol(vol)
							
					if b[0] == lcd.RIGHT:
						client.next()
						
					if b[0] == lcd.LEFT:
						client.previous()
						
					if b[0] == lcd.SELECT:
						if client.status()['state'] == 'play':
							#playing
							client.pause()
						else:
							#stopped
							client.play()

					t0 = clock()
					prev = b
				break
			#end "if buffon pressed"
				


	client.disconnect()
	sys.exit(0)

#Script starts here
if __name__ == "__main__":
	main()
