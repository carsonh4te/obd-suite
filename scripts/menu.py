import os
import sys
import time
import subprocess

# ANSI Terminal Colors
CYAN, GREEN, YELLOW, RED, BLUE, BOLD, RESET = '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[94m', '\033[1m', '\033[0m'

def clear_screen():
    os.system('clear')

def print_header():
    clear_screen()
    print(f"{CYAN}{BOLD}========================================={RESET}")
    print(f"{CYAN}{BOLD}    UNIVERSAL OBD2 & CAN DIAGNOSTICS     {RESET}")
    print(f"{CYAN}{BOLD}========================================={RESET}")
    print(f"{YELLOW}Please select a module to launch:{RESET}\n")

def run_script(script_name, is_python=True):
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    
    if not os.path.exists(script_path) and script_name != "cansniffer":
        print(f"\n{RED}[-] Error: Could not find {script_name} in the scripts/ folder.{RESET}")
        input(f"{YELLOW}[Press Enter to return to menu]{RESET}")
        return

    try:
        if is_python:
            subprocess.run(["python3", script_path])
        elif script_name == "cansniffer":
            print(f"{YELLOW}[!] Launching cansniffer. Press CTRL+C to exit back to menu.{RESET}")
            time.sleep(1)
            subprocess.run(["cansniffer", "-c", "slcan0"])
        else:
            subprocess.run(["bash", script_path])
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n{RED}[-] Execution error: {e}{RESET}")

    if script_name != "uds_probe.py": # uds_probe has its own enter prompt
        print(f"\n{CYAN}-----------------------------------------{RESET}")
        input(f"{BOLD}[Press Enter to return to the Main Menu]{RESET}")

def main():
    while True:
        print_header()
        print(f"  {BOLD}[1]{RESET} Read & Clear DTC Codes")
        print(f"  {BOLD}[2]{RESET} Live Telemetry {GREEN}(Universal){RESET}")
        print(f"  {BOLD}[3]{RESET} Live Telemetry {BLUE}(Subaru Crosstrek){RESET}")
        print(f"{CYAN}-----------------------------------------{RESET}")
        print(f"  {BOLD}[4]{RESET} Initialize CAN Interface {YELLOW}(Run First!){RESET}")
        print(f"  {BOLD}[5]{RESET} Subaru CAN Decoder {GREEN}(Human Readable){RESET}")
        print(f"  {BOLD}[6]{RESET} Raw CAN Sniffer {YELLOW}(cansniffer){RESET}")
        print(f"{CYAN}-----------------------------------------{RESET}")
        print(f"  {BOLD}[7]{RESET} Read VIN via UDS {BLUE}(uds_vin.py){RESET}")
        print(f"  {BOLD}[8]{RESET} Manual UDS Probe {RED}(uds_probe.py){RESET}")
        print(f"{CYAN}========================================={RESET}")
        print(f"  {BOLD}[0]{RESET} Exit to Container Shell\n")

        choice = input(f"{BOLD}Enter your choice (0-8): {RESET}").strip()

        if choice == '1': run_script("read_codes.py")
        elif choice == '2': run_script("live_data.py")
        elif choice == '3': run_script("subaru_live.py")
        elif choice == '4': run_script("start_can.sh", is_python=False)
        elif choice == '5': run_script("subi_can.py")
        elif choice == '6': run_script("cansniffer", is_python=False)
        elif choice == '7': run_script("uds_vin.py")
        elif choice == '8': run_script("uds_probe.py")
        elif choice == '0':
            clear_screen()
            print(f"{GREEN}[+] Exiting menu. You are now in the container bash shell.{RESET}")
            print(f"{YELLOW}[!] Type 'exit' to shut down the container entirely.{RESET}\n")
            sys.exit(0)
        else:
            print(f"{RED}[-] Invalid choice. Please enter a number between 0 and 8.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print(f"{GREEN}[+] Exiting menu. You are now in the container bash shell.{RESET}\n")
        sys.exit(0)