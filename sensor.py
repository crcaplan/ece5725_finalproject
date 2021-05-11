# author Tamzid Ahmed(ta326) and Claire Caplan(crc235)
# code for sensing hand gesture code
# date: 05/10/2021
import RPi.GPIO as GPIO
import time
import glob
import subprocess
import os
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN) # right sensor
GPIO.setup(6, GPIO.IN)  # left sensor
# covering both sensor, pause play
# right sensor go forward
# left sensor go backward
os.chdir('/home/pi/final_project/playlist/ta326')
f = glob.glob('*mp3')
length = len(f)
pointer = 0
player = subprocess.Popen(["omxplayer",f[pointer]],stdin=subprocess.PIPE,bufsize=0)
while (1):
	time.sleep(0.1)
	if ( not GPIO.input(16) and not GPIO.input(6) ):
		print (" ")
		print ("Pause/Play")
		player.stdin.write(b'p')
		time.sleep(0.5)
	elif ( not GPIO.input(6) ):
		print (" ")
		print ("go backward")
		player.stdin.write(b'q')
		pointer +=1
		if (pointer == length):
			pointer = 0
		time.sleep(0.5)
		player = subprocess.Popen(["omxplayer",f[pointer]],stdin=subprocess.PIPE,bufsize=0)
	elif ( not GPIO.input(16) ):
		print (" ")
		print ("go forward")
		player.stdin.write(b'q')
		pointer -= 1
		if (pointer == -1):
			pointer = length-1
		time.sleep(0.5)
		player = subprocess.Popen(["omxplayer",f[pointer]],stdin=subprocess.PIPE,bufsize=0)
