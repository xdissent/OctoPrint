#!/usr/bin/env bash

exec qemu-system-arm -kernel "$PWD/build/kernel-qemu" -cpu arm1176 -m 256 -M versatilepb -no-reboot -serial stdio -append "root=/dev/sda2 panic=1 rootfstype=ext4 rw" -hda "$PWD/build/raspbian.img" -redir tcp:2222::22 -redir tcp:5000::5000