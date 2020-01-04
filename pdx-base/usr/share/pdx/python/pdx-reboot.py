#!/user/bin/env python

# pd-reboot.py - oneshot service so do your thing and exit
#
# We are in reboot processing either because reboot is running. 
#
import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use physical board pin numbering
GPIO.setup(31,GPIO.OUT)  # Pi to Power MCU communication
GPIO.setup(33,GPIO.IN)   # Power MCU to Pi on power button

# In practice detecting power button press is unfortunately not reliable, message if detected
if GPIO.input(33):
	# Power Key was already pressed - shut the system down immediately
	print("pidesktop: reboot service unexpected power button detected")
else:
	# reboot initiated do whatever is needed on reboot
	# GPIO.output(31,GPIO.HIGH) #  tell power MCU and exit immediately
	print("pidesktop: reboot service active")

# we're done
print("pidesktop: reboot service completed")
