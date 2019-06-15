#!/usr/bin/python

import time
from sinchsms import SinchSMS
import RPi.GPIO as GPIO           # import RPi.GPIO module  
from time import sleep
import time


number = 'my number'
message = 'You\'ve got mail!'
got_event = 0
expired=time.time()

client = SinchSMS(your_app_key, your_app_secret)

GPIO.setmode(GPIO.BCM)           		   # choose BCM or BOARD  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # set a port/pin as an input  

def send_sms():
    print("Sending '%s' to %s" % (message, number))
    response = client.send_message(number, message)
    message_id = response['messageId']

    response = client.check_status(message_id)
    while response['status'] != 'Successful':
        print(response['status'])
        time.sleep(1)
        response = client.check_status(message_id)


def handler(channel):
    global got_event
    got_event = 1



GPIO.add_event_detect(23,GPIO.RISING, callback=handler, bouncetime=50)

print("Waiting for the postman...")

while True:
    sleep(0.1)
    if got_event == 1 and GPIO.input(23) == 1:
	if time.time() > expired:
		print("got falling edge, send sms")
		send_sms()
		expired = time.time() + 3600      # 3600 seconds in the future for debounce.
	else:
		print("got falling edge, don's send sms")
        got_event = 0
         
