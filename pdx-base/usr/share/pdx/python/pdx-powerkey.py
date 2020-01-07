#!/usr/bin/env python
#
# pdx-powerkey.py - monitor GPIO to detect power key press from Power MCU (PCU)
#
# This code monitors power button on the X7xx without polling to minimize CPU utilization.
# It turns hardware actions into software-based reboot and shutdown processing.
# When booting, first we need to tell the PCU we are ready to process a button press.
# If short press (reboot), then we detect both RISING and FALLING events from PCU as it 
# initates fast "flash flash flash" LED, but on long press (shutdown), we only detect RISING 
# event and PCU intiates slow "pulse" LED.

import RPi.GPIO as GPIO
import time,os,sys

print 'pdx: power button monitor - service starting'

GPIO.setwarnings(False)  # do not display warnings
GPIO.setmode(GPIO.BCM)   # use traditional numbering
GPIO.setup(4,GPIO.IN)    # GPIO4 PCU to Pi - detect power key pressed
GPIO.setup(17,GPIO.OUT)  # GPIO17 Pi to PCU - set active on boot

# inform PCU monitor is active. TODO: create a way to flash the power LED
#GPIO.output(17,GPIO.LOW) # tell PCU to flash the LED

monitor_start = time.time()  # starting monitor datetime
print 'pdx: power button monitor - active on boot', time.asctime(time.localtime(monitor_start))
GPIO.output(17,GPIO.HIGH) # tell PCU this system is active

GPIO.wait_for_edge(4, GPIO.RISING)  # wait forever for power button press
monitor_press = time.time()
print 'pdx: power button monitor - press detected at', time.asctime(time.localtime(monitor_press))

channel = GPIO.wait_for_edge(4, GPIO.FALLING, timeout=5000) # wait 5secs for button release
monitor_release = time.time()  # capture release or timeout
print 'pdx: power button monitor - taking action after', monitor_release - monitor_press

# clean up GPIO use
GPIO.cleanup()       # free up any GPIO related resources
os.system("sync")    # flush any I/O for safety

# power button monitor can determine short or long press based on channel
if channel is 4:
    # reboot
    print "pdx: power button monitor - reboot initiated"
    os.system("systemctl reboot")
else:
    # shutdown
    print "pdx: power button monitor - poweroff initiated" 
    os.system("systemctl poweroff")

print "pdx: power button monitor - service complete"

sys.exit()


