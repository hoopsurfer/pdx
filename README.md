pdx - a pi desktop experience
=============================
This project provides software to support create a more PC-like experience for Raspberry Pi 4 (RPi4) I call Pi Desktop eXperience or pdx.  It uses Geekworm's X856 for storage and X735 for power control, but I reserve the right to change that over time.  This repository contains information on how to best use the X856 and a completely new approach to X730 power management board from http://geekworm.com sourced from SupTronics.  The original software worked, but was brute force, uses too much CPU and is not well integrated with the OS.  None of the code from the original script remains so this is not a fork of that code.  This is a second generation effort, the original was based on hardware from element14.

Combined, the X856 and X735 provide mSATA USB 3 Gen 1 Disk and power management integrated with the Raspberry Pi GPIO Connector.  Together they provide the missing mass storage, power management common in a desktop PC. While there is no RTC, in practice that, for me, has been of little value because network time works so well.  Because the RPi4 has made quite a few changes in HDMI, USB, and Network ports there are limited case options as I write this. I expect that to change as RPi4 is adopted.

Key features of pdx:
- Reliable and fast reboot for mSATA SSD drives
- Flashing to signal pdx reboot/poweroff activity
- Improved installation instructions (Raspian to start)
- pdx-check command that provides detailed environment support
- Integration with systemd services and hooks for reboot/poweroff
- Rationalized file naming scheme

The performance of X856 is nearly 10X my previous Pi Desktop solution so that motivated a change.  The X735 has auto-power on, and expansion headers for an external momentary switch that provides support for reboot, shutdown, and forced power off. Interestingly, the Raspberry Pi 4 does not yet support boot from USB directly but it is a planned feature.  I expect this solution will evolve to use an NVME SSD using the USB-C port, possibly a simpler power managment board, perhaps a real time clock and a case solution.  I've reached out to Geekworm with my recommendations on those points.  If you need to acquire here is where would start [looking for the kit](kit.md).

*This is a work in progress*

Setup and Install
-----------------
[Fast Installation boot mSATA from SD](install.md) - Boot from mSATA USB with an existing SD card - cleanest

Hardware Documentation from Geekworm
------------------------------------
[Geekworm X735](http://www.raspberrypiwiki.com/index.php/X735)
[Geekworm X856](http://www.raspberrypiwiki.com/index.php/X856)

X735 PCU working model
-----------------------
read GPIO4 / Pin 7
- hardware reboot (short) or shutdow (longer) signals
- OS must respond to this signal
- reboot: power led flashes fast through reboot process, shutdown: led starts slow and gets faster until poweroff

write GPIO17 / Pin 11 
- system operational with GPIO 17, once enabled the PCU will observe GPIO18 signals, when not enabled the PCU will ignore GPIO18.

write GPIO18 / Pin 12 to siganl reboot (short) or shutdown (longer) signals
- 1-2 sec says reboot 3-7 says shutdown 8+ says power off immediately (crash)
- essentially GPIO18 is the power button, the physical button on the board only generates signals and initiates LED flashing

physical power button
- pressing 1-2 seconds initiates reboot signal on GPI04, 3-7 seconds initiates poweroff to GPIO4
- while the LEDs may flash they, without signals from GPIO18 power will stay on and LED will stop flashing after 50 secs
- The LED lights do behave well, which is a combination of GPIO code provided here and by the PCU 


Footnote
--------
If you are familiar with the original Pi Desktop product and my repo to support it, that solution suffered from poor firmware in power management, and I was reverse engineering the firmware when the Raspberry Pi 4 was released and made it clear that was not the path forward.  See https://github.com/hoopsurfer/pidesktop for that history.
