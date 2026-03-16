import can
import cantools
import os
import sys

# ANSI Terminal Colors
CYAN, GREEN, YELLOW, RED, BOLD, RESET = '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[1m', '\033[0m'

def main():
    os.system('clear')
    print(f"{CYAN}{BOLD}Initializing Subaru CAN Decoder...{RESET}")

    # 1. Load the DBC file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dbc_file = os.path.join(script_dir, "subaru_global_2017.dbc")

    if not os.path.exists(dbc_file):
        print(f"{RED}[-] Error: DBC file not found at {dbc_file}{RESET}")
        print(f"{YELLOW}[!] Ensure the file is named exactly that and is in your scripts/ folder.{RESET}")
        sys.exit(1)

    try:
        # Load the translation dictionary
        db = cantools.database.load_file(dbc_file)
        print(f"{GREEN}[+] Loaded DBC: {len(db.messages)} known messages mapped.{RESET}")
    except Exception as e:
        print(f"{RED}[-] Failed to load DBC file: {e}{RESET}")
        sys.exit(1)

    # 2. Connect to the CAN interface
    try:
        # We use python-can's socketcan interface to tap into slcan0
        bus = can.interface.Bus(channel='slcan0', bustype='socketcan')
        print(f"{GREEN}[+] Connected to slcan0. Listening for traffic...{RESET}\n")
        print(f"{YELLOW}--- Waiting for network activity. Press CTRL+C to stop. ---{RESET}\n")
    except OSError:
        print(f"{RED}[-] Error: slcan0 interface is down.{RESET}")
        print(f"{YELLOW}[!] You must run ./scripts/start_can.sh first!{RESET}")
        sys.exit(1)

    last_seen_state = {}

    try:
        # Loop over the firehose of incoming messages
        for msg in bus:
            try:
                # Decode the raw hex into a dictionary of signals
                decoded = db.decode_message(msg.arbitration_id, msg.data)
                
                # Get the English name of the module broadcasting
                msg_name = db.get_message_by_frame_id(msg.arbitration_id).name

                # Format the signals for clean display
                sig_parts = []
                for key, val in decoded.items():
                    # Round floats to 1 decimal place to eliminate electrical noise jitter
                    display_val = round(val, 1) if isinstance(val, float) else val
                    sig_parts.append(f"{YELLOW}{key}:{RESET} {GREEN}{display_val}{RESET}")

                formatted_signals = ", ".join(sig_parts)

                # Only print if the data has actually changed (Print-on-Change)
                if last_seen_state.get(msg_name) != formatted_signals:
                    # Snaps perfectly into a grid
                    print(f"{CYAN}{BOLD}{msg_name:<25}{RESET} | {formatted_signals}")
                    last_seen_state[msg_name] = formatted_signals

            except cantools.database.errors.DecodeError:
                # Silently ignore messages where the data length doesn't perfectly match the DBC
                pass
            except KeyError:
                # Silently ignore Arbitration IDs that aren't defined in the DBC
                pass

    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Stopping CAN decoder...{RESET}")
        bus.shutdown()
        print(f"{GREEN}[+] Disconnected.{RESET}")

if __name__ == "__main__":
    main()
