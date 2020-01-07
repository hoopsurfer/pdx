#!/user/bin/env python

# pdx-poweroff.py - oneshot service so do your thing and exit
#
# We are in poweroff processing because shutdown has started for whatever reason.
# This code can do any needed poweroff specific processing for power management.
# The critical activity is a long press of the power button through GPIO18
#

import RPi.GPIO as GPIO
import time,os,sys

print 'pdx: poweroff service - service initializing'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)   # Use traditional pin numbering
GPIO.setup(17, GPIO.OUT) # Pi to Power MCU system active
GPIO.setup(18, GPIO.OUT) # Pi to Power MCU soft button press
GPIO.setup(4, GPIO.IN)   # Power MCU to Pi on power button

# disable the power button if it has not already been pressed
if GPIO.input(4):
	# Power button was pressed and we can tell
	print 'pdx: poweroff service - power button press detected'

# poweroff initiated enable power control
GPIO.output(17, GPIO.HIGH)  # enable power control
print("pdx: shutdown service - power control enabled")

print 'pdx: poweroff service - long press power button'
GPIO.output(18, GPIO.HIGH) # long press soft power button
time.sleep(3)              # poweroff
GPIO.output(18, GPIO.LOW)  # release soft power button

# poweroff initiated disable power control
GPIO.output(17, GPIO.LOW)  # disable power control
print("pdx: shutdown service - power control disabled")

#  unmount SD card to clean up logs
#print("pdx: poweroff service - unmounting SD card")
#os.system("umount /dev/mmcblk0p1")

# stash the current system clock setting into the RTC hardware
#print("pdx: poweroff service - saving system clock to hardware clock")
#os.system("/sbin/hwclock --systohc")

GPIO.cleanup()
print 'pdx: poweroff service - service complete'
sys.exit()
