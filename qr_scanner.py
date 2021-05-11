import cv2
import RPi.GPIO as GPIO
import os
import pygame, sys
import time
from pygame.locals import *
"""GPIO.setmode(GPIO.BCM)
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
my_buttons = {b1:'scan', b2: 'quit' }"""
# set up camera object
cap = cv2.VideoCapture(0)

# QR code detection object
detector = cv2.QRCodeDetector()

while (1):
    # get the image
    _, img = cap.read()
    # get bounding box coords and data
    data, bbox, _ = detector.detectAndDecode(img)
    
    # if there is a bounding box, draw one, along with the data
    if(bbox is not None):
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                     0, 255), thickness=2)
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        if data:
            print("data found: ", data)
    # display the image preview
    cv2.imshow("code detector", img)
    if(cv2.waitKey(1) == ord("q")):
        break
    """
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
    pygame.display.flip()"""
# free camera object and exit
cap.release()
cv2.destroyAllWindows()
