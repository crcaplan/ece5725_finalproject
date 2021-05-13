import RPi.GPIO as GPIO
import time

TRIGGER = 26
ECHO = 4


def distance():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIGGER, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
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
    
    GPIO.cleanup()
    return distance
    
    
while(1):
    dist = distance()
    print('distance ' + str(dist))
    time.sleep(10)