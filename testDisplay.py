import cv2
import RPi.GPIO as GPIO
import os
import pygame, sys
import time
from pygame.locals import *
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
red =  (255,   0,   0)
green =  (0,   255,   0)
black = 0, 0, 0
white = 255,255,255
# settting up environment varialble for piTFT
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()
pygame.mouse.set_visible(False)
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
my_font = pygame.font.Font(None,30)
log_font = pygame.font.Font(None,20)
my_font_coord = pygame.font.Font(None,20)
b1 = (150,110)
b2 = (270,220)
my_buttons = {b1:'scan', b2: 'quit' }
# set up camera object
#cap = cv2.VideoCapture(0)

# QR code detection object
#detector = cv2.QRCodeDetector()

while (1):
    if ( not GPIO.input(27) ):
        print (" ")
        print ("Butoon 27 pressed")
        quit()
    screen.fill(black)
    pos = (150,110)
    if (my_buttons[b1] == 'scan'):
        pygame.draw.rect(screen, red, pygame.Rect(30, 30, 60, 60))
    for text_pos,my_text in my_buttons.items():
        if ( my_text == 'scan'):
            text_surface = my_font.render(my_text,True, black)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        else:
            text_surface = my_font.render(my_text,True, white)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        if(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            if ( y > 180 ):
                if ( x > 190 ):
                    print ( "quit button pressed" )
                    quit()
    pygame.display.flip()
