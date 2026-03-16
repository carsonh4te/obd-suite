#!/bin/bash
# scripts/start_can.sh

echo "[+] Initializing OBDLink EX for raw CAN sniffing..."

# slcand bridges the serial port to a CAN network interface
# -o (open port), -c (close on exit), -s6 (set speed to 500kbps HS-CAN)
slcand -o -c -s6 /dev/ttyUSB0 slcan0

# Bring the network interface up
ip link set up slcan0

echo "[+] CAN interface 'slcan0' is UP!"
echo "[+] You can now run: candump slcan0  OR  cansniffer -c slcan0"