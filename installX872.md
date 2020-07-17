Setting up the X872 NVMe to USB3 Gen 2 Adapter
===============================================

**NOTE: I HAVE FOUND X872 WORKS, BUT IS UNRELIABLE FOR ME, ESPECIALLY AFTER SHUTDOWN OR REBOOT AND IS VERY SENSITIVE (PLUGGING IN ANOTHER USB DEVICE CRASHES THE PI4). UNTIL IT CAN BE DETERTMINED WHY IT FAILS, I WOULD NOT RECOMMEND USING THIS ADDON CARD.  Weith a second card I have found idProduct of 0x0583 shown below and also 0x0562 - I have not determined if there is a difference**

There are different approaches to setting up your NVMe SSD,  I chose to take a Pi-only approach that requires no extra tools and minimal editing of configuration files.  This results in a single partition on your SSD, long term it might be better to have a boot partition on the SSD, but for now we'll keep it simple.

How you create your SD card is up to you, likely the easiest is using a PC using the new official Raspberry Pi tool which will download and write the image to your SD card, but here we assume for this you have an RPI4 that boots successfully from an SD card before we start with monitor(s) and keyboard and mouse operational.  When you boot Raspian the first time you should go through localizing and apply the latest updates, once you are ready to boot from your new X872 adapter shutdown, power it off by disconnecting power.

1. Assemble your X872 and make sure the USB3 to USB3 bridge connector is fully seated. 
1. Attach your NVMe SSD with one screw and make sure the SD Card is inserted and seated.
1. Assemble your X735 and make sure it is seated correctly on the GPIO pins.
1. Make sure you have 3A or better USB C power adapter, a weak power supply will cause all sorts of random problems.
1. Plug the power adapter into the X735 USB C connector, no other power should be connected to any port
1. Power on and it should boot up as normal.  You can check that the USB adapter is working using:

`sudo lsusb -v -d 152d:`

And you will find this info with the X872 model number if it is connected correctly:

```
  idVendor           0x152d JMicron Technology Corp. / JMicron USA Technology Corp.
  idProduct          0x0583
  bcdDevice            2.08
  iManufacturer           1 X870
  iProduct                2 External
  iSerial                 3 DD564198838D9
  ...
    SuperSpeed USB Device Capability:
    bLength                10
    bDescriptorType        16
    bDevCapabilityType      3
    bmAttributes         0x00
    wSpeedsSupported   0x000e
      Device can operate at Full Speed (12Mbps)
      Device can operate at High Speed (480Mbps)
      Device can operate at SuperSpeed (5Gbps)
    bFunctionalitySupport   1
      Lowest fully-functional device speed is Full Speed (12Mbps)
    bU1DevExitLat          10 micro seconds
    bU2DevExitLat          32 micro seconds
  SuperSpeedPlus USB Device Capability:
    bLength                20
    bDescriptorType        16
    bDevCapabilityType     10
    bmAttributes         0x00000001
      Sublink Speed Attribute count 1
      Sublink Speed ID count 0
    wFunctionalitySupport   0x1100
    bmSublinkSpeedAttr[0]   0x000a4030
      Speed Attribute ID: 0 10Gb/s Symmetric RX SuperSpeedPlus
    bmSublinkSpeedAttr[1]   0x000a40b0
      Speed Attribute ID: 0 10Gb/s Symmetric TX SuperSpeedPlus
```

Which shows that your device is attached and can operate at 10Gb/s rate!  Unfortunately the USB 3 Gen 1 port on the RPi4 is limited to 5Gbps so we'll have to live with that.  You can also look at the boot log information with `journalctl` and search for `usb 2-2` and you will see:

```
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: new SuperSpeed Gen 1 USB device number 2 using xhci_hcd
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: New USB device found, idVendor=152d, idProduct=0583, bcdDevice= 2.08
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: Product: External
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: Manufacturer: X870
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: SerialNumber: DD564198838D9
Mar 16 19:53:15 raspberrypi kernel: scsi host0: uas
Mar 16 19:53:15 raspberrypi kernel: scsi 0:0:0:0: Direct-Access     NVME                      0208 PQ: 0 ANSI: 6

```

Which shows it is using USB Attached Storage or UAS for communication. It turns out that UAS is not as compatible with USB devices as we would like so there are quirks we can setup in the boot command by adding`usb-storage.quirks=152d:0583:u` which is supposed to tune the kernel to use the best options for a specific adapter.  In this case it disables UAS.  It's not clear to me if this is needed at this point, but it does reduce performance and while the information is here, I am not using this myself.

Speaking of journals and the journalctl command, there is a very useful feature of this subsystem that enables looking at old boot logs which can be especially helpful.  I would suggest at this point you enable that feature with `sudo nano /etc/systemd/journald.conf` and uncomment the storage configuration line in `[Journal]` so it says `Storage=persistent` which allows you to look at previous logs.  Once you have rebooted, for example to look at the log from the previous boot use `journalctl -b -1` to look at any messages.

Next we are going to format the SSD deleting all the data on the device (if any) using the following commands:

`sudo fdisk -l /dev/sda`    # to double check you have the right device as /dev/sda
`sudo fdisk /dev/sda`       # to launch fdisk

Issue the following commands:

- `p`  to see list of partitions, if any exist then delete them
- `o`  to create a dos partition table (if none exists or it is gpt) -or- 
- `d`  to delete each partition (repeat this if you found more than one)
- `n`  to create a new partition (take the defaults which is the full device)
- `w`  to write your changes to disk - you may see an error, don't worry reboot

Now you should have rebooted with a blank SSD with one partition, double check with fdisk:

`sudo fdisk -l /dev/sda`

And you should see something like this:

```
Disk /dev/sda: 232.9 GiB, 250059350016 bytes, 488397168 sectors
Disk model:                 
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disklabel type: dos
Disk identifier: 0x902766c7

Device     Boot Start       End   Sectors   Size Id Type
/dev/sda1        2048 488397167 488395120 232.9G 83 Linux
```

Next let's create a filesystem in our new root partition and give it the standard name:

`sudo mkfs.ext4 -L rootfs /dev/sda1`

Finally let's mount the new root filesystem and copy the root partition contents from the SD card to the SSD

`sudo mount /dev/sda1 /media/pi`

`sudo rsync -avx / /media/pi`

Ok, now all the files are on both the SD /root AND the SSD /root so next we need to tell the system  how to boot from the SSD /root partition.  But first let's save the existing file so we can switch back to booting from SD should we need to:

`sudo cp /boot/cmdline.txt /boot/cmdline.sd`

IMPORTANT:  To enable boot there are two approaches, first is brute force using the device name which generally would be by using the following in /boot/cmdline.txt: `root=/dev/sda1 rootfstype=ext4 rootwait`. The better way is to use PARTUUID approach which uses a unique ID generated when creating partitions.  This is superior because it is possible that the root device (which is based on a USB port) could end up with a different device name (say /dev/sda2 instead of /dev/sda1.  The PARTUUID approach is a little more complex but more reliable so we will focus on that here.

Configuring Boot from SSD
-------------------------

Ok, let's first capture the PARTUUID for your new root partition using `blkid` then add those to the boot partitions /boot/cmdline.txt and your new root partitions /etc/fstab as follows:

`sudo blkid`

Which will provide an output like this:

```
/dev/mmcblk0p1: LABEL_FATBOOT="boot" LABEL="boot" UUID="9969-E3F2" TYPE="vfat" PARTUUID="97710275-01"
/dev/mmcblk0p2: LABEL="rootfs" UUID="8f2a74a4-809c-471e-b4ad-a91bfd51d6e4" TYPE="ext4" PARTUUID="97709275-02"
/dev/sda1: LABEL="rootfs" UUID="e6305a8f-3161-4ff2-9ef4-aec225c43e52" TYPE="ext4" PARTUUID="99130384-01"
```

You want the unique partition id (PARTUUID) from your new SSD root filesystem.  So in the above example your existing SD card boot PARTUUID is 97710275-01 and the new SSD root PARTUUID 99130384-01.  Now let's edit /boot/cmdline.txt (on the SD card) so it contains the new SSD PARTUUID without the quotes:

`root=PARTUUID=99130384-01 rootfstype=ext4 rootwait`

using:

`sudo nano /boot/cmdline.txt`  use ^x, Y, enter to exit

And second, let's change /etc/fstab on the SSD root partition to contain the new SSD root PARTUUID which would llook like this using the new SSD PARTUUID again without quotes:

`sudo nano media/pi/etc/fstab`

```
PARTUUID=97709275-01  /boot           vfat    defaults          0       2
PARTUUID=99130834-01  /               ext4    defaults,noatime  0       1
```

MAKE SURE you use your PARTUUIDs not those from the example here and once you have made these PARTUUID changes double check them and reboot.  

It is worth taking a look at journalctl and search for the product id 0583 to see what is happening:

```
journalctl

Mar 16 19:53:15 raspberrypi kernel: usb 2-2: new SuperSpeed Gen 1 USB device number 2 using xhci_hcd
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: New USB device found, idVendor=152d, idProduct=0583, bcdDevice= 2.08
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: Product: External
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: Manufacturer: X870
Mar 16 19:53:15 raspberrypi kernel: usb 2-2: SerialNumber: DD564198838D9
Mar 16 19:53:15 raspberrypi kernel: scsi host0: uas
Mar 16 19:53:15 raspberrypi kernel: scsi 0:0:0:0: Direct-Access     NVME                      0208 PQ: 0 ANSI: 6
```

To verify it is booting correctly you can use the command `findmnt -n -o SOURCE /` to verify you have the correct root device. If you made an error in your edits you may need to put the SD card in a card reader and copy the /boot/cmdline.sd file back to /boot/cmdline.txt then boot the SD card and look for mistakes.  In my case I've made several mistakes even just testing this.  Once I had an extra PARTUUID= in the cmdline.txt file.  Another time I had quotes copied from blkid output.  Assuming your edits are correct after a reboot your system should boot up using the SSD root partition.  

Note that for RPi3 you can boot directly from USB and I am not covering this here, for RPi4 there is a commitment to improve the firmware to support direct boot from USB, we'll update this when the firmware is available.
