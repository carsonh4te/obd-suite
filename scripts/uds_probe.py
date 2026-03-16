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
    print(f"{CYAN}{BOLD}        UDS CUSTOM DID PROBE             {RESET}")
    print(f"{CYAN}{BOLD}========================================={RESET}")
    
    # Targeting the standard Engine ECU for now
    TARGET_TX_ID = 0x7E0
    TARGET_RX_ID = 0x7E8
    
    print(f"{YELLOW}[*] Target TX: {hex(TARGET_TX_ID)} | RX: {hex(TARGET_RX_ID)}{RESET}")
    
    # Prompt the user for the DID
    did_input = input(f"\n{BOLD}Enter a 4-character Hex DID to probe (e.g., F190, F1A0, 0100): {RESET}").strip()
    
    try:
        # Convert the hex string to an integer for udsoncan
        did_to_read = int(did_input, 16)
    except ValueError:
        print(f"{RED}[-] Invalid Input. Please enter a valid hexadecimal string.{RESET}")
        sys.exit(1)

    print(f"{YELLOW}[*] Opening ISO-TP Socket via slcan0...{RESET}")

    try:
        conn = IsoTPSocketConnection('slcan0', rxid=TARGET_RX_ID, txid=TARGET_TX_ID)
        conn.txdl = 8 
    except Exception as e:
        print(f"{RED}[-] Failed to bind to slcan0. Did you run start_can.sh first?{RESET}")
        sys.exit(1)

    with Client(conn, request_timeout=2) as client:
        try:
            print(f"{CYAN}> Requesting DID 0x{did_input.upper()}...{RESET}")
            response = client.read_data_by_identifier(did_to_read)
            
            # Extract payload (skipping the 3-byte UDS header)
            payload = response.service_data.echo[3:]
            
            # Format the output for reverse engineering
            hex_str = payload.hex(' ').upper()
            ascii_str = payload.decode('ascii', errors='replace')
            
            print(f"\n{GREEN}[+] Response Received!{RESET}")
            print(f"    {BOLD}Raw Hex:{RESET}  {hex_str}")
            print(f"    {BOLD}ASCII:{RESET}    {ascii_str}")

        except NegativeResponseException as e:
            print(f"\n{RED}[-] Negative Response: The module rejected the request.{RESET}")
            print(f"    {e}")
        except TimeoutException:
            print(f"\n{RED}[-] Timeout: No response from module.{RESET}")
            print(f"    {YELLOW}The module is offline or the DID is completely unsupported.{RESET}")
        except Exception as e:
            print(f"\n{RED}[-] An unexpected UDS error occurred: {e}{RESET}")

    print(f"\n{CYAN}-----------------------------------------{RESET}")
    input(f"{BOLD}[Press Enter to return to the menu]{RESET}")

if __name__ == "__main__":
    main()