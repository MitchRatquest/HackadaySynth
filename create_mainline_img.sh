#!/bin/bash
BRANCH=2019.11-rc3

if [ ! -d buildroot ]
then	
	git clone --branch "$BRANCH" https://github.com/buildroot/buildroot.git
fi

make O=$PWD -C buildroot/ BR2_EXTERNAL=synth/ defconfig BR2_DEFCONFIG=synth/configs/buildroot_defconfig
make
