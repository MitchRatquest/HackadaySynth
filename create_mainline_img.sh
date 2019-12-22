#!/bin/bash
VERSION=2019.11

if [ ! -d buildroot-"$VERSION" ]
then
	wget https://git.busybox.net/buildroot/snapshot/buildroot-"$VERSION".tar.gz
	tar zvxf buildroot-"$VERSION".tar.gz
fi

#extract custom packages to buildroot's directory
tar xvf patches/buildroot/externals.tar.gz -C `pwd`/buildroot-"$VERSION"/package/

#apply patches to buildroot
cd buildroot-"$VERSION"
patch -p1 < ../patches/buildroot/0003-ssh-root-x11.patch
patch -p1 < ../patches/buildroot/0004-package-config.patch
patch -p1 < ../patches/buildroot/genimage_rootfs_size.patch
patch -p1 < ../patches/buildroot/bootcmd.patch
cd ..


make O=$PWD -C buildroot-"$VERSION"/ defconfig BR2_DEFCONFIG=../configs/buildroot-vanilla-config
make
