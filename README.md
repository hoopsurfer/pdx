pdx - pi desktop experience
=============================
This project provides software to create a more PC-like experience for Raspberry Pi 4 (RPi4) I call Pi Desktop eXperience or pdx.  It uses the Geekworm X735 for power control and X872 for M.2 NVMe storage but I reserve the right to change that over time.  I upgraded to the X872 in my configuration which is captured here, note that additional power was required to make the X872 reliable for me. This repository contains information on how to best use the X872 and a fairly easy set of instructions to support direct USB booting and a completely new approach to X735 for power management. The hardware is available at http://geekworm.com sourced from SupTronics. 

Combined, the X735 and X872 provide power management integrated with the Raspberry Pi GPIO Connector and M.2 NVMe to USB 3 Gen 1 high speed storage.  Together they provide the missing power management and storage common in a desktop PC. While there is no RTC, in practice that, for me, has been of little value because network time works so well.  Because the RPi4 has made quite a few changes in HDMI, USB, RAM, and Network ports it took some time to select a case, but Geekworm has one exactly matched to these components called the X857-C1 that works very well and provides a nice lighted power button that is completely integrated with the power management solution here.

Key features of pdx:
- Integrated into Raspian's package manager for install/upgrades
- Reliable and fast boot and reboot for the latest M.2 NVMe SSD drives
- Flashing power button to signal pdx reboot/poweroff activity
- Improved installation instructions with Pi-only tools needed
- pdx-check command that provides detailed environment support
- Integration with systemd services and hooks for reboot/poweroff
- Implementation uses wait to minimize CPU use for power management
- full integration with `systemctl` commands and legacy `reboot` or `shudown`
- No unique commands needed to properly shudown or reboot required
- details on how to overclock and tools to test settings to get better performance 

The performance of X872 is more than 10X my previous Pi Desktop solution so that motivated a change.  The X735 has auto-power on, and expansion headers for an external momentary switch that provides support for reboot, shutdown, and forced power off.  The Raspberry Pi 4 now is available with 8GB RAM and offically supports boot directly from USB directly with no SD required. Boot and reboot times are fast.  Geekworm has been a great partner answering questions and provides excellent technical support and they welcomeed my recommendations. If you need to acquire hardware here is where would start [looking for the kit](kit.md).

The code and .deb file works reliably for me and can be installed by downloading the .deb file. The power control is coded using wait so it consumes minimal CPU.  When running just window manager it consumes between 0 and 1% CPU.  I suppose registering the package so it is even easier to install would be a good idea.

Setup and Install
-----------------
How you create your SD card is up to you, likely the easiest is using a PC using the new official Raspberry Pi SD tool which will download and write an OS image to your SD card, but here we assume for this you have a Pi 4 that boots successfully from an SD card with monitor(s) and keyboard and mouse operational. When you boot Raspian the first time you should go through localizing and apply the latest updates, check that you don't need any updates by using `sudo apt update` and if needed `sudo apt full-upgrade` to apply any missing updates.  Once your system is updated, you can immediately install the pdx code so the moment you get the hardwire setup it will work correctly.  To install the pdx code download [pdx-base.deb](https://github.com/hoopsurfer/pdx), however if you wish to wait until you are booting from your SSD the instructions will remind you to do that as well.

Once your SD card is ready to go, power off your Pi4 and disconnect power so you can install all the required hardware.

[Fast Installation to boot NVMe from SD](installX872.md) - Boot from NVMe SSD & USB with an existing SD card - cleanest.

[Fast Installation boot mSATA from SD](installX856.md) - Boot from mSATA SSD & USB with an existing SD card - needs to be updated.

[TODO: Capture overclocking instructions, stability testing, and overall system benchmark.]

systemd service files
---------------------
lib/systemd/system/pdx-poweroff.service which uses [pdx-poweroff.py](pdx-base/usr/share/pdx/python/pdx-poweroff.py)

lib/systemd/system/pdx-reboot.service which uses [pdx-reboot.py](pdx-base/usr/share/pdx/python/pdx-reboot.py)

lib/systemd/system/pdx-powerkey.service which uses [pdx-powerkey.py](pdx-base/usr/share/pdx/python/pdx-powerkey.py)

package files
-------------
control - package control info

postinst - post installation script

postrm - post uninstall script

building pdx-base
-----------------------
There is a simple Makefile to build pdx-base.deb file from sources if you clone or fork the repos.

`make uninstall`   will uninstall the current pdx package
`make clean`       will clean the build environment
`make`             will make the .deb file
`make install`     will install the rebuilt pdx package

Or you can simply download the provided .deb file and install with the following command:

`dpkg -i pdx-base.deb`

If you want to change things you can clone this repository `make uninstall`, `make clean`, edit the underlying code, then `make` to build a new .deb package and install it with `make install`.  You need to reboot for systemd changes to take effect.

Hardware Documentation from Geekworm
------------------------------------
[Geekworm X735 - Power Management](http://www.raspberrypiwiki.com/index.php/X735)
[Geekworm X872 - M.2 NVMe Adapter](http://www.raspberrypiwiki.com/index.php/X872)
[Geekworm X856 - M.2 mSATA Adapter](http://www.raspberrypiwiki.com/index.php/X856)

X735 PCU working model
-----------------------
read GPIO4 / Pin 7 to signal physical button press
- hardware reboot (short) or shutdow (longer) signals
- OS must respond to this signal
- reboot: power led flashes rapidly through reboot process, shutdown: led flashes slowly and gets faster until poweroff

write GPIO17 / Pin 11 to enable PCU activity
- system operational with GPIO 17, once enabled the PCU will observe GPIO18 signals, when not enabled the PCU will ignore GPIO18.

write GPIO18 / Pin 12 to signal reboot (short) or shutdown (longer) signals
- 1-2 sec says reboot 3-7 says shutdown 8+ says power off immediately (crash)
- essentially GPIO18 is the power button, the physical button on the board only generates signals and initiates LED flashing

physical power button
- pressing 1-2 seconds initiates reboot signal on GPI04, 3-7 seconds initiates poweroff to GPIO4
- while the LEDs may flash they, without signals from GPIO18 power will stay on and LED will stop flashing after 50 secs
- The LED lights do behave well, which is a combination of GPIO code provided here and by the PCU
- pressing for more than 8 seconds causes immediate poweroff - useful for an unresponsive system


Footnote
--------
An earlier version of this writeup used the X856 for mSATA storage, I expect the steps are fairly identical to use this device, but I have not tested them yet.

The original software provided by Geekworm worked, but was brute force, used too much CPU, was not well integrated with the OS and required special commands to safely reboot or shutdown.  None of the code from the original scripts was used given this is a completely different approach, so while Geekworm is noted as a contributor here, it is their documentation that was used so this is not a fork of their code.  Also, this is a second generation effort for me, the original was based on hardware from element14 and an RPi3. The original Pi Desktop product suffered from poor firmware in power management, and I was reverse engineering the firmware when the Raspberry Pi 4 was released.  It quickly became clear that was not the path forward. See https://github.com/hoopsurfer/pidesktop for that history.
