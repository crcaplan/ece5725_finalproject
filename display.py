# author Tamzid Ahmed(ta326) and Claire Caplan(crc235)
# code to  scan QR code
# date: 05/06/2021
import cv2
import RPi.GPIO as GPIO
import os
import pygame, sys
import pygame.display
import time
import sensor
from pygame.locals import *
from pygame.locals import *
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
red =  (255,0,0)
green =  (0,   255,   0)
black = 0, 0, 0
white = 255,255,255
# setting up environment varialble for piTFT
#os.putenv('SDL_VIDEODRIVER', 'fbcon')
#os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
# taken from aircanvas project
#Rescales the output frame to 320 x 240 screen

def rescale_frame(frame, wpercent=130, hpercent=130):
    width = int(frame.shape[1] * wpercent / 100)
    #print("width: " + str(width) "\n height" )
    height = int(frame.shape[0] * hpercent / 100)
    return cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)

pygame.init()
pygame.mouse.set_visible(True)
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
my_font = pygame.font.Font(None,30)
log_font = pygame.font.Font(None,20)
my_font_coord = pygame.font.Font(None,20)
b1 = (150,110)
b2 = (240,220)
start_screen_buttons = {'Quit':(240,220), 'Start':(80,220), 'Welcome to':(160,80), 'Touchless Music Player!': (160,100)}
info_screen1_buttons = {'Quit':(240,220), 'Next':(80,220), 'Scan your QR code to load':(160,80), 'your personal playlist!': (160,100)}
info_screen2_buttons = {'Quit':(240,220), 'Next':(80,220), 'Play/Pause: cover L/R sensors':(160,80), 'Next track: cover L sensor': (160,100),
                        'Previous track: cover R sensor': (160,120), 'Volume: Hand distance': (160,140), 'from center sensor':(160,160)}
my_buttons = {b1:'Scan', b2: 'Quit'}
#cap = cv2.VideoCapture(0)
# QR code detection object
detector = cv2.QRCodeDetector()
scan = False
start_screen = True
info_screen1 = False
info_screen2 = False
scan_screen = False
while (1):
    if ( not GPIO.input(27) ):
        print (" ")
        print ("Button 27 pressed")
        GPIO.cleanup()
        quit()
        
    screen.fill(black)
    if(start_screen):
        for my_text,text_pos in start_screen_buttons.items():
                text_surface = my_font.render(my_text,True,white)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface,rect)
        for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                if(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                    if y >200:
                        #if click in vicinity of quit button, quit
                        if x > 160:
                            print ( "quit button pressed" )
                            cv2.destroyAllWindows()
                            cap.release()
                            GPIO.cleanup()
                            quit()
                        #if click in vicinity of start button, set flag
                        if x < 160:
                            start_screen = False
                            info_screen1 = True
        pygame.display.flip()
    
    if(info_screen1):
        screen.fill(black)
        for my_text,text_pos in info_screen1_buttons.items():
                text_surface = my_font.render(my_text,True,white)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface,rect)
        for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                if(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                    if y >200:
                        #if click in vicinity of quit button, quit
                        if x > 160:
                            print ( "quit button pressed" )
                            cv2.destroyAllWindows()
                            cap.release()
                            GPIO.cleanup()
                            quit()
                        #if click in vicinity of next button, set flag
                        if x < 160:
                            info_screen1 = False
                            info_screen2 = True
        pygame.display.flip()
    
    if(info_screen2):
        screen.fill(black)
        for my_text,text_pos in info_screen2_buttons.items():
                text_surface = my_font.render(my_text,True,white)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface,rect)
        for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                if(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                    if y >200:
                        #if click in vicinity of quit button, quit
                        if x > 160:
                            print ( "quit button pressed" )
                            cv2.destroyAllWindows()
                            cap.release()
                            GPIO.cleanup()
                            quit()
                        #if click in vicinity of next button, set flag
                        if x < 160:
                            info_screen2 = False
                            scan_screen = True
        pygame.display.flip()
    
    if(scan_screen):
        screen.fill(black)
        # set up camera object
        pos = (150,110)
        if (my_buttons[b1] == 'scan'):
            rectangle = pygame.draw.rect(screen, red, pygame.Rect(90, 60, 120, 120))
            rectangle.move(pos)
        else:
            rectangle = pygame.draw.rect(screen, green, pygame.Rect(90, 60, 120, 120))
            rectangle.move(pos)
        for text_pos,my_text in my_buttons.items():
            if ( my_text == 'scan'):
                text_surface = my_font.render(my_text,True, white)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface,rect)
            else:
                text_surface = my_font.render(my_text,True, white)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface,rect)
        pygame.display.flip()
        for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                if(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                    if ( y > 180 ):
                        if ( x > 190 ):
                            print ( "quit button pressed" )
                            cv2.destroyAllWindows()
                            cap.release()
                            GPIO.cleanup()
                            quit()
                    if ( y > 30 and y < 170 ):
                        if ( x> 30 and x < 170):
                            scan = True
                            
        #cap = cv2.VideoCapture(0)
        # QR code detection object
        #detector = cv2.QRCodeDetector()
        #video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        #video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        while scan:
        #while cap.isOpened():
            if ( not GPIO.input(27) ):
                print (" ")
                print ("Button 27 pressed")
                cv2.destroyAllWindows()
                cap.release()
                quit()
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                if(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                    if ( y > 180 ):
                        if ( x > 190 ):
                            print ( "quit button pressed" )
                            cv2.destroyAllWindows()
                            cap.release()
                            GPIO.cleanup()
                            quit()
            
            # get the image
            _, img = cap.read()
            #Rescale the display frame to 320 x 240 pixels
            rescaled_frame = rescale_frame(img)
            surface = pygame.surfarray.make_surface(rescaled_frame.transpose(1,0,2)[...,::-1])
            surface.convert()
            screen.blit(surface, (0,0))
            pos = (150,110)
            pygame.display.flip()
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
                #time.sleep(1) # this stops continous detection of data
                print("data found: ", data)
                #sensor.play_music('ta326')
                #os.chdir('.')
                #scan = False
                # display the image preview
                with open('netid.txt') as f:
                    lines = f.readlines()
                    for line in lines:
                        #print('line is ', line)
                        #print('data is ' , data)
                        if ( line.rstrip() == data ):
                            print("match found")
                            #my_buttons[b1] = "success"
                            sensor.play_music(data)
                            os.chdir('.')
                            scan = False
                            #cv2.destroyAllWindows()
                            #cap.release() # need cap release so that go back to while loop
                            #quit()
            # display the image preview
            #cv2.imshow("code detector", img)

            if(cv2.waitKey(1) == ord("q")):
                break
# free camera object and exit
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()

