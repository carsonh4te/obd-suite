#!/bin/bash
# scripts/start_can.sh

# ANSI Terminal Colors
CYAN='\033[96m'
GREEN='\033[92m'
YELLOW='\033[93m'
RED='\033[91m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${CYAN}${BOLD}[+] Initializing OBDLink EX for raw CAN sniffing...${RESET}"

MAX_RETRIES=3
ATTEMPT=1

while [ $ATTEMPT -le $MAX_RETRIES ]; do
    echo -e "${YELLOW}[*] Attempt $ATTEMPT of $MAX_RETRIES...${RESET}"

    # Step 1: Force cleanup of any stuck or half-open interfaces
    ip link set slcan0 down 2>/dev/null
    pkill slcand 2>/dev/null
    
    # Pause to let the kernel clear the device
    sleep 1

    # Step 2: Initialize slcand (-s6 sets speed to 500kbps HS-CAN)
    slcand -o -c -s6 /dev/ttyUSB0 slcan0
    
    # Pause to give Linux time to actually register the new slcan0 network device
    sleep 2
    
    # Step 3: Bring the network interface up
    ip link set up slcan0 2>/dev/null

    # Step 4: Verify the status
    # We pipe the output of 'ip link' to grep and look for the "UP" state
    if ip link show slcan0 2>/dev/null | grep -q "UP"; then
        echo -e "\n${GREEN}${BOLD}[+] SUCCESS: CAN interface 'slcan0' is UP and verified!${RESET}"
        echo -e "${GREEN}[+] You can now run your raw CAN or UDS modules.${RESET}"
        exit 0
    else
        echo -e "${RED}[-] Interface failed to initialize on attempt $ATTEMPT.${RESET}"
        ATTEMPT=$((ATTEMPT+1))
    fi
done

# If the loop finishes without exiting, it means all 3 attempts failed.
echo -e "\n${RED}${BOLD}[-] FATAL: Failed to initialize CAN interface after 3 attempts.${RESET}"
echo -e "${YELLOW}[!] Troubleshooting steps:${RESET}"
echo "    1. Ensure the key is in the ON position."
echo "    2. Physically unplug the USB cable from your laptop, plug it back in."
echo "    3. Run 'Option 4' again."
exit 1
