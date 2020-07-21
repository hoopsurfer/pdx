#!/bin/bash
#
# pdx-overclock - check for overclocking stability on Raspberry Pi - this runs for a LONG time.
#

echo "pdx-overclock - Validating Pi Overclock Settings "

echo "config.txt items"

echo -n "CPU freq: " ; cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
echo -n "CPU temp: " ; cat /sys/class/thermal/thermal_zone0/temp

echo "Running infinite loop on all cores..."

# Start worker threads to heat up all CPUs and put pressure on power.
for ((i=0; i<$(nproc --all); i++)); do nice yes >/dev/null & done

echo "Read and Write SSD..."

# Read the entire SSD 10x. Tests RAM and I/O
for i in `seq 1 10`;
  do
      echo "Reading SSD Pass:" $i; sudo dd if=/dev/sda1 of=/dev/null bs=4M count=512;
      echo "Writing SSD Pass:" $i; dd if=/dev/zero of=delete.tmp bs=1M count=512; sync;
      echo -n "CPU freq: " ; cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
      echo -n "CPU temp: " ; cat /sys/class/thermal/thermal_zone0/temp
  done

# Remove workers and clean temp file
killall yes
rm delete.tmp

# Print ending results, check the system log for issues
echo -n "CPU freq: " ; cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
echo -n "CPU temp: " ; cat /sys/class/thermal/thermal_zone0/temp

journalctl | tail

echo "Make sure to check journalctl log for errors."

