Pi Desktop X V0.1
=================
This project provides software to support Geekworm's X856 for storage and X735 for power control to create a more PC-like experience for Raspberry Pi 4 (RPi4) I call Pi Desktop X.  This repository contains information on how to best use the X856 and a fork of the "offical" X730 power management board from http://geekworm.com sourced from SupTronics.  While the provided software works, it is brute force, uses too much CPU and is not well integrated with the OS.

Because the RPi4 has made quite a few changes in HDMI, USB, and Network connections there are limited case options as I write this.  Combined, the X856 and X735 provide mSATA USB 3 Gen 1 Disk and power management integrated with the Raspberry Pi GPIO Connector.  Together they provide the missing mass storage, power management common in a desktop PC.   

Key features of pidesktop:
- Reliable reboot for mSATA SSD drives
- Flash on boot to signal pidesktop support is enabled
- Improved installation instructions (Raspian and Berryboot)
- New pd-check command that provides detailed environment support
- Improved logging information
- Improved systemd services
- Rationalized file naming scheme

The performance of X856 is nearly 10X my previous Pi Desktop solution so motivated a change.  The X735 has auto-power on, and expansion headers for an external momentary switch that provides support for reboot, shutdown, and forced power off. Interestingly, the Raspberry Pi 4 does not yet support boot from USB directly but it is a planned feature.  I expect this solution will evolve to use an NVME SSD using the USB-C port, possibly a simpler power managment board (X710?) and we'll see a case solution.  I've reached out to Geekworm with my recommendations on those points.  If you need to acquire here is where would start [looking for the kit](kit.md).

*This is a work in progress*

Setup and Install
-----------------
[Fast Installation boot mSATA from SD](install.md) - Boot from mSATA USB with an existing SD card - cleanest

Hardware Documentatoin
----------------------
[Geekworm X735](http://www.raspberrypiwiki.com/index.php/X735)
[Geekworm X856](http://www.raspberrypiwiki.com/index.php/X856)

X735 working model - 

read GPIO 4 for hardware reboot (short) or shutdow (longer) signals
   OS must respond to this signal
   reboot: power led flashes fast through reboot process, shutdown: led starts slow and gets faster until poweroff
write GPIO17 system operational with GPIO 17 (stops reboot flashing light - stops on its own eventually - seems optional)
write GPIO18 to siganl reboot (short) or shutdown (longer) signals
   1-2 sec says reboot 3-7 says shutdown 8+ says power off immediately (crash)
   essentially GPIO18 is like pressing the physical button on the board

==========



# x730-script
This is the safe shutdown script for x730;

NOTE:

We test this shell script base official Raspbian '2018-11-13-raspbian-stretch.img' version;
We test this shell script base official Raspbian '2019-09-26 Raspbian Buster' version also;

How to use?

* step 1:
> wget https://raw.githubusercontent.com/geekworm-com/x730-script/master/x730.sh

> sudo chmod +x x730.sh

> sudo bash x730.sh

* step 2:

> printf "%s\\n" "alias x730off='sudo x730shutdown.sh'" >> ~/.bashrc

* step 3:
> sudo reboot

* how to safe shut down, run the following comamdn:
> x730off


Footnote
--------
If you are familiar with the original Pi Desktop product and my repo to support it, that solution suffered from poor firmware in power management, and I was reverse engineering the firmware when the Raspberry Pi 4 was released and made it clear that was not my path forward.  See https://github.com/hoopsurfer/pidesktop for that history.
