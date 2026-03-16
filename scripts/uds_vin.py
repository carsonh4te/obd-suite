import os
import sys
import udsoncan
from udsoncan.connections import IsoTPSocketConnection
from udsoncan.client import Client
from udsoncan.exceptions import *

# ANSI Terminal Colors
CYAN, GREEN, YELLOW, RED, BOLD, RESET = '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[1m', '\033[0m'

def main():
    os.system('clear')
    print(f"{CYAN}{BOLD}========================================={RESET}")
    print(f"{CYAN}{BOLD}        DEEP UDS DIAGNOSTIC SCANNER      {RESET}")
    print(f"{CYAN}{BOLD}========================================={RESET}")
    
    # In UDS, you must target a specific module's CAN IDs. 
    # For standard 11-bit CAN, the Engine ECU usually listens on 0x7E0 and replies on 0x7E8.
    TARGET_TX_ID = 0x7E0  # What we send to
    TARGET_RX_ID = 0x7E8  # What we listen for
    
    print(f"{YELLOW}[*] Target Module TX: {hex(TARGET_TX_ID)} | RX: {hex(TARGET_RX_ID)}{RESET}")
    print(f"{YELLOW}[*] Attempting to establish ISO-TP Socket via slcan0...{RESET}")

    try:
        # We leverage Linux's native ISO-TP networking over our virtual CAN interface
        conn = IsoTPSocketConnection('slcan0', rxid=TARGET_RX_ID, txid=TARGET_TX_ID)
        conn.txdl = 8 # Force 8-byte CAN frames for compatibility
    except Exception as e:
        print(f"{RED}[-] Failed to bind to slcan0. Did you run start_can.sh first?{RESET}")
        print(f"Error details: {e}")
        sys.exit(1)

    # Open the UDS Client session
    with Client(conn, request_timeout=2) as client:
        try:
            print(f"{GREEN}[+] Connection established! Sending UDS requests...{RESET}\n")
            
            # Service 0x22: Read Data By Identifier
            # DID 0xF190: Vehicle Identification Number (VIN)
            did_to_read = 0xF190
            print(f"{CYAN}> Requesting DID {hex(did_to_read)} (VIN)...{RESET}")
            
            response = client.read_data_by_identifier(did_to_read)
            
            # The response payload is raw bytes. We decode it to ASCII.
            raw_data = response.service_data.echo
            # The actual payload usually starts after the first few bytes of UDS header
            vin_string = raw_data[3:].decode('ascii', errors='ignore') 
            
            print(f"{GREEN}[+] Success! Module replied with VIN:{RESET} {BOLD}{vin_string}{RESET}")

        except NegativeResponseException as e:
            print(f"{RED}[-] The module rejected the request: {e}{RESET}")
            print(f"{YELLOW}[!] This module might require a security access seed/key to read this data.{RESET}")
        except TimeoutException:
            print(f"{RED}[-] Request timed out.{RESET}")
            print(f"{YELLOW}[!] The module at {hex(TARGET_TX_ID)} is not responding. The car's ignition might be off, or the ID is wrong for this vehicle.{RESET}")
        except Exception as e:
            print(f"{RED}[-] An unexpected UDS error occurred: {e}{RESET}")

    print(f"\n{CYAN}-----------------------------------------{RESET}")
    print(f"{GREEN}[+] UDS Session closed.{RESET}")

if __name__ == "__main__":
    main()