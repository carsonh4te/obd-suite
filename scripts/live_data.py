import obd
import time
import os
import sys
import csv
from datetime import datetime

# ANSI Terminal Colors
CYAN, GREEN, YELLOW, RED, BOLD, RESET = '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[1m', '\033[0m'

def clear_screen(): os.system('clear')

def get_value(connection, command):
    response = connection.query(command)
    return response.value if not response.is_null() else "N/A"

def main():
    clear_screen()
    print(f"{CYAN}{BOLD}Initializing Live Telemetry...{RESET}")
    
    connection = obd.OBD("/dev/ttyUSB0", fast=False)
    if not connection.is_connected():
        print(f"{RED}[-] Failed to connect. Check cable and ignition.{RESET}")
        sys.exit(1)

    sensors = {
        "Engine RPM": obd.commands.RPM,
        "Vehicle Speed": obd.commands.SPEED,
        "Coolant Temp": obd.commands.COOLANT_TEMP,
        "Intake Pressure": obd.commands.INTAKE_PRESSURE,
        "Mass Air Flow (MAF)": obd.commands.MAF,
        "Throttle Position": obd.commands.THROTTLE_POS,
        "Timing Advance": obd.commands.TIMING_ADVANCE,
        "Engine Load": obd.commands.ENGINE_LOAD
    }

    # Setup CSV Logging
    script_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_filename = os.path.join(script_dir, f"live_data-{timestamp}.csv")

    try:
        with open(log_filename, mode='w', newline='') as log_file:
            writer = csv.writer(log_file)
            # Write CSV Headers
            headers = ["Timestamp"] + list(sensors.keys())
            writer.writerow(headers)

            while True:
                clear_screen()
                print(f"{CYAN}{BOLD}=== OBD2 LIVE DATA (LOGGING ENABLED) ==={RESET}")
                print(f"{YELLOW}Log File:{RESET} {log_filename}")
                print(f"{CYAN}-----------------------------------------{RESET}")
                
                row_data = [datetime.now().strftime("%H:%M:%S.%f")[:-3]]
                
                for name, command in sensors.items():
                    val = get_value(connection, command)
                    # Print to terminal
                    print(f"{BOLD}{name:<20}:{RESET} {GREEN}{val}{RESET}")
                    # Append to CSV row
                    row_data.append(val)
                    
                print(f"{CYAN}-----------------------------------------{RESET}")
                print(f"{YELLOW}[Press CTRL+C to stop streaming]{RESET}")
                
                # Write row to CSV and force flush to disk
                writer.writerow(row_data)
                log_file.flush()
                
                time.sleep(0.1)

    except KeyboardInterrupt:
        clear_screen()
        connection.close()
        print(f"{GREEN}[+] Connection closed. Log saved to {log_filename}{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()