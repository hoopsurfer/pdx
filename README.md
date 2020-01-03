This project provides software to support Geekworm's X856 for storage and X735 for power control to create a more PC-like experience for Raspberry Pi 4.  The performance of X856 is nearly 10X my previous Pi Desktop solution so motivated a change.  The Pi Desktop project suffered from poor firmware in power management, and I was reverse engineering the firmware when the Raspberry Pi 4 was released and made it clear that was not my path forward.  Interestingly, the Raspberry Pi 4 does not support boot from USB directly at launch but is a planned feature.   This is a work in progress.



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
