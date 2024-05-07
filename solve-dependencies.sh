#!/usr/bin/bash
sudo dnf upgrade --refresh
sudo dnf install kernel-devel-*
sudo dnf install kernel-devel-matched.x86_64
sudo dnf install python3
sudo dnf install python3-tkinter
sudo dnf install python3-pip
pip3 install customtkinter
sudo reboot
