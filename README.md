## Overview

<details>
  <summary>Getting Started</summary>
  ```console
  ./create_mainline_img.sh
  ```
  That should get buildroot in this directory, unpack it, and patch it to add the packages the synth requires. (future plans include making this entire repo a buildroot external, which is the correct way to go about this)

  Once this completes, you should have a build in images/sdcard.img, which you can `dd` to an SD card or use etcher to write to an sd card. 
</details>

<details>
  <summary>Buildroot configuration</summary> 
  
  
  Buildroot is simpler and takes up less space than yocto. You can get started like this:

```console
make menuconfig
make linux-menuconfig
make uboot-menuconfig
make busybox-menuconfig
```
  
  While in any of those menus, you can use `/` to search for a string, which is insanely helpful and I somehow managed to create the first try of this without it. For years. Its a beautiful feature. 
</details>
