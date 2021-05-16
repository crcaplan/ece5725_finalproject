# author Tamzid Ahmed(ta326) and Claire Caplan(crc235)
# code for sensing hand gesture code
# date: 05/10/2021
import RPi.GPIO as GPIO
import time
import glob
import subprocess
import os
import pygame, sys
import pygame.display
import time
from pygame.locals import *
from pygame.locals import *
# settting up environment varialble for piTFT
#os.putenv('SDL_VIDEODRIVER', 'fbcon')
#os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
red =  (255,   0,   0)
green =  (0,   255,   0)
black = 0, 0, 0
white = 255,255,255
play = pygame.image.load("./button_blue_play.png")
pause = pygame.image.load("./button_blue_pause.png")
pygame.init()
pygame.mouse.set_visible(True)
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
b1 = (140,20)
my_song = {b1:'song name is very long it is'}
my_font = pygame.font.Font(None,30)

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

#os.chdir('/home/pi/ece5725_finalproject/playlist/ta326')
#os.chdir('/home/pi/final_project/playlist/ta326')
def set_directory(user):
    directory = '/home/pi/final_project/playlist/'
    directory += user
    os.chdir(directory)
    return directory
f = glob.glob('*mp3')
#print(f)
#length = len(f)
pointer = 0
#player = subprocess.Popen(["omxplayer",f[pointer]],stdin=subprocess.PIPE,bufsize=0)
volume = 8
def start_player(f,pointer):
    print(pointer)
    return subprocess.Popen(["omxplayer",f[pointer]],stdin=subprocess.PIPE,bufsize=0)
def play_music(user):
    directory = set_directory(user)
    f = glob.glob('*mp3')
    pointer = 0
    print(f)
    print(len(f[pointer][0:27]))
    print("hello")
    player = start_player(f,pointer)
    length = len(f)
    paused = False
    while (1):
        if ( not GPIO.input(23) ):
            print (" ")
            print ("Butoon 23 pressed, quitting music")
            player.stdin.write(b'q')
            #quit()
            return
        screen.fill(black)
        if (paused):
            playrect = play.get_rect()
            playrect = playrect.move(100,80)
            screen.blit(play, playrect)
        else:
            pauserect = pause.get_rect()
            pauserect = pauserect.move(100,80)
            screen.blit(pause, pauserect)
        my_song[b1] = f[pointer][0:27]
        for text_pos,my_text in my_song.items():
	        text_surface = my_font.render(my_text,True, white)
	        rect = text_surface.get_rect(center=text_pos)
	        screen.blit(text_surface,rect)
        pygame.display.flip()
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
            paused = True if paused == False else False;
            time.sleep(0.5)
        elif ( not GPIO.input(6) ):
            print (" ")
            print ("go backward")
            player.stdin.write(b'q')
            pointer +=1
            if (pointer == length):
                pointer = 0
            time.sleep(0.5)
            my_song[b1] = f[pointer][0:27]
            paused = False
            player = start_player(f,pointer)
            #player = subprocess.Popen(["omxplayer",f[pointer]],stdin=subprocess.PIPE,bufsize=0)
        elif ( not GPIO.input(16) ):
            print (" ")
            print ("go forward")
            player.stdin.write(b'q')
            pointer -= 1
            if (pointer == -1):
                pointer = length-1
            time.sleep(0.5)
            my_song[b1] = f[pointer][0:27]
            paused = False
            player = start_player(f,pointer)
            #player = subprocess.Popen(["omxplayer",f[pointer]],stdin=subprocess.PIPE,bufsize=0)
#play_music('ta326')
