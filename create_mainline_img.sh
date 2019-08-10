#!/bin/bash
VERSION=fb65f4841845f63d32f8f6f246a7aaac21074d49

if [ ! -d rockchip-buildroot ]
then
	git clone https://github.com/rockchip-linux/buildroot.git rockchip-buildroot
fi

if [ ! -f .br_patched ]
then
	cd rockchip-buildroot
	git checkout "$VERSION"
	patch -p1 < ../patches/buildroot/0000-add-pd-tk.patch
	cd ..
	touch .br_patched
fi


make O=$PWD -C rockchip-buildroot/  defconfig BR2_DEFCONFIG=../configs/br_rk_defconfig
#make
