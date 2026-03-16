#!/bin/bash

# Configuration variables
IMAGE_NAME="universal-obd-suite"
CONTAINER_NAME="obd_diag"
USB_PORT="/dev/ttyUSB0" # Change this if your cable mounts as /dev/ttyACM0

# Function to display usage instructions
show_help() {
    echo "Usage: ./obd-suite [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  new      - Starts a fresh diagnostic session."
    echo "  rebuild  - Rebuilds the Docker image from the local Dockerfile."
    echo "  all      - Rebuilds the image and immediately starts a new session."
    echo ""
}

# Function to pause until the USB cable is detected
check_usb() {
    while [ ! -e "$USB_PORT" ]; do
        echo ""
        echo "[!] WARNING: Hardware not detected at $USB_PORT."
        read -p "[?] Please plug in your OBD2-to-USB cable and press [Enter] to check again..."
    done
    echo "[+] Hardware detected at $USB_PORT!"
}

case "$1" in
    new)
        echo "[+] Preparing a new diagnostic session..."
        
        check_usb
        
        # Clean up any old, stopped containers with the same name
        docker rm -f "$CONTAINER_NAME" 2>/dev/null
        
        echo "[+] Launching container and mounting local directory..."
        # Run the new container interactively, map volume, and immediately execute menu.py
        # We wrap it in bash so that if you exit the menu, the container stays alive in the shell
        docker run -it --rm \
            --privileged \
            -v "$PWD":/diagnostics \
            --device="$USB_PORT":"$USB_PORT" \
            --name "$CONTAINER_NAME" \
            "$IMAGE_NAME" \
            /bin/bash -c "python3 scripts/menu.py; /bin/bash"
        ;;
        
    rebuild)
        echo "[+] Rebuilding the $IMAGE_NAME image..."
        # Build the image based on the Dockerfile in the current directory
        docker build -t "$IMAGE_NAME" .
        
        echo "[+] Rebuild complete."
        ;;

    all)
        echo "[+] Executing full rebuild and launch..."
        # Call the script itself to run the rebuild command
        "$0" rebuild
        # Call the script itself to run the new command
        "$0" new
        ;;
        
    *)
        # Catch-all for invalid commands or no arguments
        show_help
        exit 1
        ;;
esac