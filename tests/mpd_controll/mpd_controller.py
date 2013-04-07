#!/usr/bin/python

## Created by Onkeliroh


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
		print "Got connected!"
	else:
		lcd.clear()
		lcd.message("Error while connecting!")
		print "Error while connecting!"
		sys.exit(1)

	# Auth if password is set non False
	if PASSWORD:
		if mpdAuth(client, PASSWORD):
			lcd.clear()
			lcd.message("Pass auth!")
			print "Pass auth!"
		else:
			lcd.clear()
			lcd.message("Error trying to pass auth!")
			print "Error trying to pass auth!"
			sys.exit(2)
	sleep(1)
	return True

def generate_status(client):
	line0 = ""
	line1 = ""
	
	state = client.status()['state']
		
	if state == 'pause':
		#paused
		line1 = "PAUSED"
	elif state == 'play' :
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
	#MPD is stopped if playlist is emty or simply stopped by user
	elif state == 'stop':
		line1 = "STOPPED"
	#just to prevent errors any unkown state is handled here
	else:
		line1 = "UNKNOWN STATE"

	return (line0+"\n"+line1)

#Produces formated string for displaying the desired informations
def display_status(lcd,message):
	try:
		lcd.backlight(lcd.BLUE)
		lcd.clear()
		lcd.message(message)
	except:
		print "Error calling LCD"
	return True
	
#turns display off
def idle(lcd):
	try:
		lcd.clear()
		lcd.backlight(lcd.OFF)
	except:
		print "Error calling LCD"
	return True

def BTN_UP(client):
	vol = int(client.status()['volume'])
	if  vol <= 90:
		vol = vol + 10
	else:
		vol = 100
	client.setvol(vol)
	return True

def BTN_DOWN(client):
	vol = int(client.status()['volume'])
	if  vol >= 10:
		vol = vol - 10
	else:
		vol = 0
	client.setvol(vol)
	return True

def BTN_RIGHT(client):
	client.next()
	return True
	
def BTN_LEFT(client):
	client.previous()
	return True

def BTN_SELECT(client):
	try:
		if client.status()['state'] == 'play':
			#playing
			client.pause()
		else:
			#stopped
			client.play()
	except:
		print "Error getting client status state"
	return True

def main():

	## MPD object instance
	client = MPDClient()
	lcd = Adafruit_CharLCDPlate(1)

	lcd.clear()
	lcd.message("Wellcome to the\nMPD Interface!")
	print "Wellcome to the\nMPD Interface!"
	sleep(1)

	#initialize mpd connection
	startup(client,lcd)

	#Printing first known informations on lcd
	message = generate_status(client)
	display_status(lcd, message)

	print client.status()
	try:
		print client.listplaylists()
	except:
		print "error"
	try:
		print client.listplaylist()
	except:
		print "error"
	try:
		print client.listplaylistinfo()
	except:
		print "error"

	# Poll buttons, display message & set backlight accordingly
	btn = ( (lcd.LEFT  , 'LEFT' , lcd.ON),
			(lcd.UP    , 'UP' , lcd.ON),
			(lcd.DOWN  , 'DOWN' , lcd.ON),
			(lcd.RIGHT , 'RIGHT' , lcd.ON),
			(lcd.SELECT, 'SELECT' , lcd.ON) )

	t0 = clock() #start time
	refresh_display = clock() #time of the last display refresh
	last_action = clock() #time of the last action
	prev = -1 # last pressed button
	
	while True:
		
		#refresh display every 0.1 sec
		if (clock() - refresh_display >= 0.1):
			refresh_display = clock()
			#turn display after 5 sec off
			if (clock()-last_action <= 2.5):
				message = generate_status(client)
				display_status(lcd,message)
			else:
				idle(lcd)
			
		for b in btn:
			#begin "if button pressed"
			if lcd.buttonPressed(b[0]):
				if (b is not prev) or (clock()-t0 >= 0.3):
					if b[0] == lcd.UP:
						BTN_UP(client)
							
					elif b[0] == lcd.DOWN:
						BTN_DOWN(client)
							
					elif b[0] == lcd.RIGHT:
						BTN_RIGHT(client)
						
					elif b[0] == lcd.LEFT:
						BTN_LEFT(client)
						
					elif b[0] == lcd.SELECT:
						BTN_SELECT(client)

					t0 = clock()
					last_action = clock()
					prev = b
				break
			#end "if buffon pressed"
				


	client.disconnect()
	sys.exit(0)

#Script starts here
if __name__ == "__main__":
	main()
