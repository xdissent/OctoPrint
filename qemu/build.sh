#!/usr/bin/env bash

setup_keys() {
  sleep 10
  cat setup-keys
  echo
}

BUILD="$PWD/build"

KERNEL="$BUILD/kernel-qemu"
KERNEL_URL="http://xecdesign.com/downloads/linux-qemu/kernel-qemu"

RASPBIAN_ZIP="$BUILD/raspbian.zip"
RASPBIAN_IMG="$BUILD/raspbian.img"
RASPBIAN_URL="http://downloads.raspberrypi.org/raspbian_latest"

mkdir -p "$BUILD"

echo "*** Downloading Kernel"
[ -f "$KERNEL" ] || curl -sLo "$KERNEL" "$KERNEL_URL"

echo "*** Downloading Raspbian"
[ -f "$RASPBIAN_ZIP" ] || curl -sLo "$RASPBIAN_ZIP" "$RASPBIAN_URL"

echo "*** Extracting Raspbian"
[ -f "$RASPBIAN_IMG" ] || {
  unzip "$RASPBIAN_ZIP" >/dev/null
  mv *-raspbian.img "$RASPBIAN_IMG"
  rm -rf __MACOSX
}

echo "*** Qemu Setup"
exec 5< <( setup_keys )
qemu-system-arm -kernel "$KERNEL" -cpu arm1176 -m 256 -M versatilepb -no-reboot -serial none -monitor stdio -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw init=/bin/bash" -hda "$RASPBIAN_IMG" <&5
echo

echo "*** Resizing IMG"
qemu-img resize "$RASPBIAN_IMG" +4G >/dev/null
