The FriendlyARM Nanopi NEO is a 4x4cm² board with an Allwiner H3 SoC:
  - quad-core Cortex-A7 @1.2GHz
  - 256 or 512MiB of DDR
  - uSDCard as only storage option
  - 3x USB 2.0 host (one socket, two on expansion pin-holes)
  - 1x USB 2.0 OTG (also used as power source)
  - 10/100 ethernet MAC
  - GPIOs, SPI, I2c...

Confirmed working are USB OTG (legacy and configfs), ethernet (100M), GPIO functions (via sysfs), and SPI (using FBTFT library).

Two cores have been reserved for running high priority tasks using isolcpus=2,3 in boot.cmd.

Uboot's Bootdelay has been reduced to zero for faster boot times.

With S40network disabled in /etc/init.d, it boots in roughly 4 seconds. 

These config files create a working 4.13 PREEMPT RT kernel for the Nanopi Neo.

Transfer rate of USB OTG depends on the SD card used for the device. Transferring files to the device I got an averag of 5.01 MB/s. Transfering files from the device to another computer averages at 41.05 MB/s. This was done by dd'ing a file from /dev/urandom, then rsync'ing that file via the usb ethernet gadget. 

# uname -a
Linux nanopi-neo 4.13.11-rt3 #2 SMP PREEMPT RT Thu Nov 30 11:17:18 CST 2017 armv7l GNU/Linux

# cyclictest -a -t -n -p80 
# /dev/cpu_dma_latency set to 0us
policy: fifo: loadavg: 0.11 0.10 0.03 1/94 920          

T: 0 (  915) P:80 I:1000 C: 238476 Min:      6 Act:    9 Avg:    9 Max:      38
T: 1 (  916) P:80 I:1500 C: 158983 Min:      5 Act:    9 Avg:    9 Max:      27
T: 2 (  917) P:80 I:2000 C: 119238 Min:      8 Act:    9 Avg:    8 Max:      17
T: 3 (  918) P:80 I:2500 C:  95390 Min:      7 Act:    9 Avg:    9 Max:      16



Improvements/TODO:

Test I2C
