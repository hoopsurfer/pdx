#!/user/bin/env python

# pd-shutdown.py - oneshot service so do your thing and exit
#
# We are in shutdown processing either because shutdown or reboot is running or because
# the power button was pressed.  If we're here because the power button was pressed then 
# Power MCU is already in Waiting OFF state and will turn off immediately if it sees 
# pin 31 go high so avoid that!  If power button has not been pressed we should inform power MCU 
# shutdown/reboot is taking place so the shutdown timer can start.
#
# Note: The timer will reset when the Pi powers off so the only purpose REALLY for doing
# this is to capture the current system time in the real time clock.

import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use physical board pin numbering
GPIO.setup(31,GPIO.OUT)  # Pi to Power MCU communication
GPIO.setup(33,GPIO.IN)   # Power MCU to Pi on power button

# In practice detecting power button press is unfortunately not reliable, message if detected
if GPIO.input(33):
	# Power Key was already pressed - shut the system down immediately
	print("pidesktop: shutdown service initated from power button")
else:
	# shutdown or reboot not related to power key
	# GPIO.output(31,GPIO.HIGH) #  tell power MCU and exit immediately
	print("pidesktop: shutdown service active")

#  unmount SD card to clean up logs
print("pidesktop: shutdown service unmounting SD card")
os.system("umount /dev/mmcblk0p1")

# stash the current system clock setting into the RTC hardware
print("pidesktop: shutdown service saving system clock to hardware clock")
os.system("/sbin/hwclock --systohc")

# we're done
print("pidesktop: shutdown service completed")
