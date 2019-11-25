setenv fdt_high ffffffff

setenv bootargs console=ttyS0,115200 earlyprintk root=/dev/mmcblk0p2 rootwait isolcpus=2,3 sunxi_ve_mem_reserve=0 sunxi_g2d_mem_reserve=0 sunxi_no_mali_mem_reserve sunxi_fb_mem_reserve=16 consoleblank=0 nohz=off

setenv bootdelay 0

fatload mmc 0 $kernel_addr_r zImage
fatload mmc 0 $fdt_addr_r sun8i-h3-nanopi-neo.dtb

bootz $kernel_addr_r - $fdt_addr_r

#recompile with: mkimage -A arm -T script -C none -d boot.cmd boot.scr
#see http://linux-sunxi.org/Kernel_arguments
