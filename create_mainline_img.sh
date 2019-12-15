#!/bin/bash
VERSION=2019.11

if [ ! -d buildroot-"$VERSION" ]
then
	wget https://git.busybox.net/buildroot/snapshot/buildroot-"$VERSION".tar.gz
	tar zvxf buildroot-"$VERSION".tar.gz
fi

cd buildroot-"$VERSION"
patch -p1 < ../patches/buildroot/0000-add-pd-tk.patch
cd ..


make O=$PWD -C buildroot-"$VERSION"/ defconfig BR2_DEFCONFIG=../configs/buildroot-vanilla-config
make
