Setting up the X856 mSATA to USB3 Gen 1 Storage Adapter
-------------------------------------------------------

There are different approaches to setting up your SSD,  I chose to take a RPi4-only approach that requires no extra tools and minimal fiddlng with configuration files.  How you create your SD card is up to you so we assume for this you have an RPI4 that boots successfully from an SD card before we start with monitor(s) and keyboard and mouse operational.  Shutdown and power it off.

1.  Assemble your X856 and make sure the USB3 to USB3 bridge connector is fully seated. Attached your mSATA SSD with two screws and make sure the SD Card is inserted.
2. Make sure you have 3A or better power supply, a weak power supply will cause all sorts of random problems.
3. Power on and it should boot up as normal.  You can check that the USB adapter is working using 

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

`sudo fidsk -l`        # to double check you have the right device as /dev/sda

`sudo fdisk /dev/sda`  # to launch fdisk

Issue the following commands:

- `p`  to see list of partitions, if any exist then delete them
- `d`  to delete each partition (repeat this if you found more than one)
- `n`  to create a new partition (take the defaults which is the full device)
- `w`  to write your changes to disk - you may see an error, don't worry reboot

Now you should have rebooted with a blank SSD with one partition, next let's format a parition

`sudo mkfs.ext4 /dev/sda1`

Finally let's copy the root partition from the SD card to the SSD

`sudo mount /dev/sda1 /media/pi`
`sudo rsync -avx / /media/pi`

To enable boot we add the  to /boot/cmdline.txt `root=/dev/sda1 rootfstype=ext4 rootwait`

`sudo nano /boot/cmdline.txt`  use ^x, Y, enter to exit

