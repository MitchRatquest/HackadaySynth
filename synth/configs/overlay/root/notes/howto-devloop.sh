#!/bin/sh
dd if=/dev/zero of=store bs=1M count=5
mkfs.vfat store
losetup /dev/loop0 store
mkdir -p tmp
mount /dev/loop0 tmp/
