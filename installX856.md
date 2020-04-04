Setting up the X856 mSATA to USB3 Gen 1 Adapter
===============================================

There are different approaches to setting up your mSATA SSD,  I chose to take a Pi-only approach that requires no extra tools and minimal editing of configuration files.  How you create your SD card is up to you so we assume for this you have an RPI4 that boots successfully from an SD card before we start with monitor(s) and keyboard and mouse operational.  Shutdown, power it off by disconnecting power.

1. Assemble your X856 and make sure the USB3 to USB3 bridge connector is fully seated. 
1. Attach your mSATA SSD with two screws and make sure the SD Card is inserted.
1. Assemble your X735 and make sure it is seated correctly on the GPIO pins.
1. Make sure you have 3A or better USB C power adapter, a weak power supply will cause all sorts of random problems.
1. Plug the power adapter into the X735 USB C connector, no other power should be connected to any 
1. Power on and it should boot up as normal.  You can check that the USB adapter is working using 

`sudo lsusb -v -d 174c:0856`

And you will find this info with the X856 model number if it is connected correctly:

```
Bus 002 Device 002: ID 174c:0856 ASMedia Technology Inc. 
...
  idVendor           0x174c ASMedia Technology Inc.
  idProduct          0x0856
  bcdDevice            1.00
  iManufacturer           2 SupTronics
  iProduct                3 X856
...
   Device can operate at Full Speed (12Mbps)
   Device can operate at High Speed (480Mbps)
   Device can operate at SuperSpeed (5Gbps)
...
```

Which shows that your device is attached and can operate at 5Gbps rate.  Next we are going to format the SSD using the following commands:

`sudo fdisk -l /dev/sda`        # to double check you have the right device as /dev/sda

`sudo fdisk /dev/sda`  # to launch fdisk

Issue the following commands:

- `p`  to see list of partitions, if any exist then delete them
- `d`  to delete each partition (repeat this if you found more than one)
- `n`  to create a new partition (take the defaults which is the full device)
- `w`  to write your changes to disk - you may see an error, don't worry reboot

Now you should have rebooted with a blank SSD with one partition, double check with fdisk: 

`sudo fdisk -l /dev/sda`

And you should see something like this:

```
Disk /dev/sda: 232.9 GiB, 250059350016 bytes, 488397168 sectors
Disk model: SSD 860 EVO mSAT
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 33553920 bytes
```

Next let's format a parition:

`sudo mkfs.ext4 /dev/sda1`

Finally let's copy the root partition from the SD card to the SSD

`sudo mount /dev/sda1 /media/pi`

`sudo rsync -avx / /media/pi`

To enable boot there are two approaches, first is brute force using the device name which generally would be by adding the following to /boot/cmdline.txt: 

`root=/dev/sda1 rootfstype=ext4 rootwait`

using:

`sudo nano /boot/cmdline.txt`  use ^x, Y, enter to exit

The better way is to use PARTUUID approach which uses a unique ID generated when creating partitions.  This is superior because it is possible that the root device (which is based on a USB port) could end up with a different device name (say /dev/sda2 instead of /dev/sda1.  The PARTUUID approach is a little more complex but more reliable.  

First capture the PARTUUIDs for your partitions using `blkid` then add those to the boot partitions /boot/cmdline.txt and your new root partitions /etc/fstab as follows:

`blkid`

Which will provide an output like this:

```
/dev/mmcblk0p1: LABEL_FATBOOT="boot" LABEL="boot" UUID="9969-E3F2" TYPE="vfat" PARTUUID="97710275-01"
/dev/mmcblk0p2: LABEL="rootfs" UUID="8f2a74a4-809c-471e-b4ad-a91bfd51d6e4" TYPE="ext4" PARTUUID="97709275-02"
/dev/sda1: UUID="e6305a8f-3161-4ff2-9ef4-aec225c43e52" TYPE="ext4" PARTUUID="99130384-01"
```

You want the unique partition id (PARTUUID) from the SD card boot partition and the SSD partition.  So in the above example your SD card boot partitions /boot/cmdline.txt would be edited so it contained the root partition:

`root=PARTUUID=99130384-01 rootfstype=ext4 rootwait`

using:

`sudo nano /boot/cmdline.txt`  use ^x, Y, enter to exit

And edit in the SSD root partition /etc/fstab to contain both the boot and root partition ids which would like this using the above example:

`sudo nano media/pi/*/etc/fstab`

```
PARTUUID=97709275-01  /boot           vfat    defaults          0       2
PARTUUID=99130834-01  /               ext4    defaults,noatime  0       1
```

MAKE SURE YOU USE YOUR PARTUUIDs not those from the example here and note that it is easy to flip back to SD card booting if you have to by editing /boot/cmdline.txt using 'blkid' to retrieve the PARTUUID for the SD card root partition.  Once you have made these changes double check them and reboot.  If you made an error in your edits you may need to put the SD card in a card reader and edit the /boot/cmdline.txt file back to SD card. Assuming your edits are correct reboot and your system should boot up using the SSD root partition.

The final step is overclocking your machine, make sure you active cooling (such as the Geekwork X735 that pdx supports).  Add the following lines to your /boot/config.txt file in the `[pi4]` section.

`sudo nano /boot/config.txt`

```
over_voltage=4
arm_freq=2000
gpu_freq=600
```

Note that for RPi3 you can boot directly from USB and I am not covering this here, for RPi4 there is a commitment to improve the firmware to support direct boot from USB, we'll update this when the firmware is available.


