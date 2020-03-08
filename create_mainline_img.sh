#!/bin/bash
VERSION=2019.11

if [ ! -d buildroot-"$VERSION" ]
then
	wget https://git.busybox.net/buildroot/snapshot/buildroot-"$VERSION".tar.gz
	tar zvxf buildroot-"$VERSION".tar.gz
fi

cd buildroot-"$VERSION"
patch -p1 < ../patches/buildroot/puredata.patch
patch -p1 < ../patches/buildroot/trx.patch
patch -p1 < ../patches/buildroot/orca.patch
patch -p1 < ../patches/buildroot/openssh-x11.patch
cd ..


make O=$PWD -C buildroot-"$VERSION"/ defconfig BR2_DEFCONFIG=../configs/buildroot_defconfig
make
