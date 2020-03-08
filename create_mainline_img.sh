#!/bin/bash
VERSION=2019.11

if [ ! -d buildroot-"$VERSION" ]
then
	wget https://git.busybox.net/buildroot/snapshot/buildroot-"$VERSION".tar.gz
	tar zvxf buildroot-"$VERSION".tar.gz
fi

cd buildroot-"$VERSION"
patch -p1 < ../patches/buildroot/0000-puredata.patch
patch -p1 < ../patches/buildroot/0001-trx.patch
patch -p1 < ../patches/buildroot/0002-orca.patch
patch -p1 < ../patches/buildroot/0003-ssh-root-x11.patch
cd ..


make O=$PWD -C buildroot-"$VERSION"/ defconfig BR2_DEFCONFIG=../configs/buildroot_defconfig
make
