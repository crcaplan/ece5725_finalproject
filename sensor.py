# author Tamzid Ahmed(ta326) and Claire Caplan(crc235)
# code for sensing hand gesture code
# date: 05/10/2021
import RPi.GPIO as GPIO
import time
import glob
import subprocess
import os

TRIGGER = 26
ECHO = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN) # right sensor
GPIO.setup(6, GPIO.IN)  # left sensor
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
# covering both sensor, pause play
# right sensor go forward
# left sensor go backward



def distance():
    
    print('sensor settling')
    GPIO.output(TRIGGER, GPIO.LOW)
    time.sleep(0.5)
    
    print('calculating distance')
    GPIO.output(TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER, GPIO.LOW)
    
    while GPIO.input(ECHO)==0:
        pulse_start_time = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end_time = time.time()
    
    pulse_duration = pulse_end_time - pulse_start_time
    print('got pulse duration')
    distance = round(pulse_duration * 17150, 2)
    
    return distance
    
    




os.chdir('/home/pi/ece5725_finalproject/playlist/ta326')
f = glob.glob('*mp3')
length = len(f)
pointer = 0
player = subprocess.Popen(["omxplayer",f[pointer]],stdin=subprocess.PIPE,bufsize=0)
volume = 8
while (1):
    dist = int(distance())
    
    if(dist>=0 and dist<=10):
        vol = dist
        print(dist)
        
        counter = 0
        if(vol>volume):
            for counter in range(1,vol-volume):
                player.stdin.write("+")
                volume = volume + 1
                time.sleep(0.1)
                print(counter)
        elif(vol<volume):
            for counter in range(1,volume-vol):
                player.stdin.write("-")
                volume = volume - 1
                time.sleep(0.1)
                print(counter)
        print("new volume is " + str(volume))
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
