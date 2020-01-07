#!/user/bin/env python

# pdx-reboot.py - oneshot service so do your thing and exit
#
# We are in reboot processing because reboot has started for whatever reason.
# This code can do any needed reboot specific processing for power management.
# The critical activity is a short press of the power button through GPIO18
#
import RPi.GPIO as GPIO
import time,os,sys

print 'pdx: reboot service - service initializing'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)   # Use traditional pin numbering
GPIO.setup(17, GPIO.OUT) # Pi to Power MCU system active
GPIO.setup(18, GPIO.OUT) # Pi to Power MCU soft button press
GPIO.setup(4, GPIO.IN)   # Power MCU to Pi on power button

# disable the power button if it has not already been pressed
if GPIO.input(4):
	# Power button was pressed and we can tell
	print 'pdx: reboot service - power button press detected'

# reboot initiated, enable power button and do whatever is needed on reboot
print("pdx: reboot service - enable power control")
GPIO.output(17, GPIO.HIGH)  # enable hardware power control

print 'pdx: reboot service - short press power control'
GPIO.output(18, GPIO.HIGH) # short press soft power button
time.sleep(1)              # reboot
GPIO.output(18, GPIO.LOW)  # release soft power button

# disable power control now that reboot has been initiated
print("pdx: reboot service - disable power control")
GPIO.output(17, GPIO.HIGH)  # enable hardware power contro

GPIO.cleanup()
print 'pdx: reboot service - service complete'
sys.exit()
