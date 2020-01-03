pidesktopx V0.1
===============
This project provides software to support Geekworm's X856 for storage and X735 for power control to create a more PC-like experience for Raspberry Pi 4 (RPi4) I call Pi Desktop X.  This repository contains is a fork of the "offical" X730 power management board from http://geekworm.com sourced from SupTronics.  Because the RPi4 has made quite a few changes in HDMI, USB, and Network connections there are limited case options.  Combined, the X856 and X735 provide mSATA USB 3 Gen 1 Disk and power management integrated with the Raspberry Pi GPIO Connector.  Together they provide the missing mass storage, power management common in a desktop PC.   As I have it configured my RPi 4 has:
- Quadcore CPU
- 4GB RAM
- Gigabit Network
- 5G Wifi and Bluetooth Wireless
- USB 3.1 Gen 1 5Gbps 
- Dual 4K monitors

The performance of X856 is nearly 10X my previous Pi Desktop solution so motivated a change.  The X735 has auto-power on, and expansion headers for an external momentary switch that provides support for reboot, shutdown, and forced power off. PInterestingly, the Raspberry Pi 4 does not support boot from USB directly at launch but it is a planned feature.  I expect this will evolve to use NVME SSD using the USB-C port and we'll see a case solution.  I've reached out to Geekworm with my recommendations on those points.

This is a work in progress.

Setting up the X856 mSATA to USB3 Gen 1 Storage Adapter
-------------------------------------------------------
There are different approaches to setting up your SSD,  I chose to take a RPi4-only approach that requires no extra tools and minimal fiddlng with configuration files.  How you create your SD card is up to you so we assume for this you have an RPI4 that boots from an SD card before we start with monitor(s) and keyboard and mouse operational.  Shutdown and power it off.

1.  Assemble your X856 and make sure the USB3 to USB3 bridge connector is fully seated. Attached your mSATA SSD with two screws and make sure the SD Card is inserted.
2. Power on and it should boot up as normal.  You can check that the USB adapter is working using 




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
