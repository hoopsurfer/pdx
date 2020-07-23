Setting up the X872 NVMe to USB3 Gen 2 Adapter
===============================================

**NOTE: I HAVE FOUND X872 WORKS WELL FOR ME, BUT ONLY IF ADDITIONAL POWER IS SUPPLIED VIA THE ADDED 5V PORT, PAY ATTENTION TO THE DETAILS BELOW.

There are different approaches to setting up your NVMe SSD,  I chose to take a simple Pi-only approach that requires no extra tools and minimal editing of configuration files.  This results in a boot partition and root partition on your NVMe SSD that are appropriately sized.  Since this project is all about creating a desktop capabable system, we only discuss Pi 4 8GB model here, but this should work with any Pi 4 model.

How you create your SD card is up to you, likely the easiest is using a PC using the new official Raspberry Pi SD tool which will download and write an OS image to your SD card, but here we assume for this you have a Pi 4 that boots successfully from an SD card with monitor(s) and keyboard and mouse operational. When you boot Raspian the first time you should go through localizing and apply the latest updates, check that you don't need any updates by using `sudo apt update` and if needed `sudo apt full-upgrade` to apply any missing updates.

Once your SD card is ready to boot from your new X872 adapter shutdown, power it off by disconnecting power.

1. Attach your NVMe SSD to the M.2 slot of your X872 with a screw.
1. Assemble your X872 and connect it with the provided standoffs to the Pi 4.
1. Assemble your X735 and make sure it is seated correctly on the GPIO pins.
1. Insert the 2 pin connector cable from the 5V OUT port on the X735 to the 5V port on the X872.
1. Insert the SD Card made above and make sure it is seated properly in the SD slot of your Pi 4.
1. Attach the assembled X735, Pi 4, and X872 to the X857-C1 case and connect the power switch. NOTE: I did not use the additional case fan because the V5 OUT port on the X735 is used for the X872. 
1. Insert the USB3 to USB3 bridge connector to connect the Pi 4 USB 3 port and the X872. 
1. Make sure you have 3A or better power adapter, a weak power supply will cause all sorts of random problems.  NOTE: If you use the Geekworm 5v 4A adapter with a barrel plug, it frees the USB C port for useful work.
1. Plug the power adapter into one X735 connector (5V Barrel or USB C), no other power should be connected to any port into the case.
1. Power on by pressing the power button and it should boot up as normal using the SD Card.  You can check that the USB adapter is working using:

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

Which shows that your device is attached and can operate at 10Gb/s rate!  Unfortunately the USB 3 Gen 1 port on the Pi 4 is limited to 5Gbps so we'll have to live with that.  You can also look at the boot log information with `journalctl` and search for `usb 2-2` and you will see:

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

Which shows it is using USB Attached Storage or UAS for communication.  If you have compatibility issues you may need to enable quirks in the boot command by adding`usb-storage.quirks=152d:0583:u` which is supposed to tune the kernel to use the best options for a specific adapter.  In this case it disables UAS.  It's not clear to me if this is needed at this point, but it does reduce performance and while the information is here, I am not using this myself.

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

Next let's copy the entire SD card to the blank SSD by using the builtin SD Card Copier accessory to create new partitions and copy boot and root filesystems to the SSD.  Make sure the 'Create New PARTUUIDs" is not checked.  You will notice once this is complete that `sudo fidsk -l /dev/sda` shows two filesystems (boot and root) and they are appropriately sized (in my case boot is 256M and the root is the remainder of the SSD) and you will notice that `sudo blkid` shows the SD card and SSD partitions have the same identifiers - this eliminates the need to edit both /boot/cmdline.txt and /etc/fstab to adjust PARTUUID values.

Ok, now all the files are on both the SD /root AND the SSD /root so next we need to make sure the system will boot from the SSD.

But first let's understand how the system is already setup using PARTUUIDs.  You can see the PARTUUIDs for your partitions by using the `sudo blkid` command.  If you look at `/boot/cmdline.txt` you will see the same PARTUUIDs and if you look at /etc/fstab you will also see the same PARTUUIDs.  This is how the OS keeps from getting confused, remember we copied the PARTUUIDs from the SD card to the SSD so don't get confused on account of that simplification, it is by design.

NOTE: To enable booting there are two approaches, first is brute force using the device name which generally would be by using something like the following in /boot/cmdline.txt: `root=/dev/sda1 rootfstype=ext4 rootwait`. The better way is to use PARTUUID approach which uses a unique ID generated when creating partitions.  This is superior because it is possible that the root device (which is based on a USB port) could end up with a different device name (say /dev/sda2 instead of /dev/sda1.  The PARTUUID approach is a little more complex but more reliable so we will focus on that here and it is configured automatically by the SD Card Copier!

Configuring Boot from SSD
-------------------------

[TODO - Need to add details on checking and installing firmware here - consider updating screen captures these are old]

Once you're confident all is well, shutdown,  remove power, REMOVE THE SSD and then power on - the system should boot within a few minutes. It is worth taking a look at journalctl and search for usb 2-2 and you will see the device detected and the boot partition mounted.

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

To verify you are booting correctly you can use the command `findmnt -n -o SOURCE /` to verify you have the correct root device and you should see /dev/sda2.
