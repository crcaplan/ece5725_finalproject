# author Tamzid Ahmed(ta326) and Claire Caplan(crc235)
# code for sensing hand gesture code
# date: 05/10/2021
import time
import glob
import subprocess
import os
import pygame, sys
import pygame.display
import time
import RPi.GPIO as GPIO
from pygame.locals import *
from pygame.locals import *
import random
import string
import qrcode
import shutil # to copy files
# Improting Image class from PIL module
from PIL import Image
# settting up environment varialble for piTFT
#os.putenv('SDL_VIDEODRIVER', 'fbcon')
#os.putenv('SDL_FBDEV', '/dev/fb0')
#os.putenv('SDL_MOUSEDRV', 'TSLIB')
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
red =  (255,   0,   0)
green =  (0,   255,   0)
black = 0, 0, 0
white = 255,255,255
pygame.init()
pygame.mouse.set_visible(False)
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
new_user_buttons = {'Prev':(50,220),'Next':(120,220), 'Select':(190,220), 'done':(270,220)}
qr_screen_buttons = {'Song Selection':(240,220), 'Take a ':(260,80), ' picture of ': (260,100), 'your QR' : (260,120), 'code' : (260,140)}
b1 = (140,20)
current_song = {b1:'song name is very long it is'}
my_font = pygame.font.Font(None,30)
os.chdir('./playlist/ta326') 
f = glob.glob('*mp3')
length = len(f)
pointer = 0
print(f)
# generate a qr code
# generate random string check if the string is in the list
# printing lowercase
def select_playlist():
    while(1):
        global pointer
        screen.fill(black)
        current_song[b1] = f[pointer]
        playlist_dir = '/home/pi/ece5725_finalproject/playlist/ta326' # for now use this but chnage it to actual folder later
        for my_text,text_pos in new_user_buttons.items():
            text_surface = my_font.render(my_text,True,white)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        for text_pos,my_text in current_song.items():
            text_surface = my_font.render(my_text,True,white)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
            if(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x,y = pos
                if y > 180:
                        #if click in vicinity of quit button, quit
                    if x < 150:
                        print ( "next button pressed" )
                        pointer = pointer + 1
                        if (pointer == length):
                            pointer = 0
                        #current_song[b1] = f[pointer]
                        #quit()
                        #if click in vicinity of quit button, quit
                    elif x < 80:
                        print ( "prev button pressed" )
                        pointer = pointer - 1
                        if (pointer == -1):
                            pointer = length - 1
                        #current_song[b1] = f[pointer]
                        #quit()
                    elif x < 220:
                        print ("selecting current song")
                        shutil.copy(os.path.join(playlist_dir, f[pointer]), '.') # copy the song to the user playlist
                    else:
                        print("done")
                        return
				
        pygame.display.flip()
def create_new_user():
    letters = string.ascii_lowercase
    user = ''.join(random.choice(letters) for i in range(5)) # make a new random userid
    print(user)
    #netid = open('/home/pi/ece5725_finalproject/netid.txt', 'a')
    #netid.write(user)
    #netid.write('\n')
    #code = qrcode.make(user) # make a qr code
    print(user+'.png')
    #code.save('./qrcode/'+user+'.png') # save the qr code
    # make a play list corresponding to the new user
    #path = '/home/pi/ece5725_finalproject/playlist/'+user
    #os.makedirs(path)
    #completeName = os.path.join('/home/pi/ece5725_finalproject/qrcode/', user+".png")
    #code.save(completeName)
    completeName = os.path.join('/home/pi/ece5725_finalproject/qrcode/', 'itbfw'+".png")
    im = Image.open(completeName)
    im = im.resize((200,200)) # resize the image to make it fit on piTFT
    im.save("test.png")
    #qr = pygame.image.load(completeName)
    qr = pygame.image.load('test.png')
    # change directory to current user's playlist
    user = 'utsty' # for testing
    directory = '/home/pi/ece5725_finalproject/playlist/'
    directory += user
    os.chdir(directory)
    while(1):
        screen.fill(black)
        qr_rect = qr.get_rect()
        qr_rect = qr_rect.move(0,0)
        screen.blit(qr,qr_rect)
        for my_text,text_pos in qr_screen_buttons.items():
            text_surface = my_font.render(my_text,True,white)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
            if(event.type is MOUSEBUTTONUP):
                pos = pygame.mouse.get_pos()
                x,y = pos
                if y >200 and x > 160: # clicked around song selction
                    select_playlist()
                    return
                    
                
            
#create_new_user()
#new_user()
