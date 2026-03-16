import obd
import time
import os
import sys
import csv
from datetime import datetime

# ANSI Terminal Colors
CYAN, GREEN, YELLOW, RED, BLUE, BOLD, RESET = '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[94m', '\033[1m', '\033[0m'

def clear_screen(): os.system('clear')

def get_value(connection, command):
    response = connection.query(command)
    return response.value if not response.is_null() else "N/A"

def main():
    clear_screen()
    print(f"{BLUE}{BOLD}Initializing Subaru Telemetry...{RESET}")
    
    connection = obd.OBD("/dev/ttyUSB0", fast=False)
    if not connection.is_connected():
        print(f"{RED}[-] Failed to connect. Check cable and ignition state.{RESET}")
        sys.exit(1)

    subaru_sensors = {
        "Vehicle Speed": obd.commands.SPEED,
        "Engine RPM": obd.commands.RPM,
        "Throttle Position": obd.commands.THROTTLE_POS,
        "Coolant Temp": obd.commands.COOLANT_TEMP,
        "Engine Oil Temp": obd.commands.OIL_TEMP, 
        "Intake Air Temp": obd.commands.INTAKE_TEMP,
        "Cat Temp (Bank 1)": obd.commands.CATALYST_TEMP_B1S1,
        "Engine Load (Rel)": obd.commands.ENGINE_LOAD,
        "Engine Load (Abs)": obd.commands.ABSOLUTE_LOAD,
        "Mass Air Flow (MAF)": obd.commands.MAF,
        "Commanded A/F": obd.commands.COMMANDED_EQUIV_RATIO,
        "Timing Advance": obd.commands.TIMING_ADVANCE,
        "Control Module Volts": obd.commands.CONTROL_MODULE_VOLTAGE
    }

    # Setup CSV Logging
    script_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_filename = os.path.join(script_dir, f"subaru_live-{timestamp}.csv")

    try:
        with open(log_filename, mode='w', newline='') as log_file:
            writer = csv.writer(log_file)
            headers = ["Timestamp"] + list(subaru_sensors.keys())
            writer.writerow(headers)

            while True:
                clear_screen()
                print(f"{BLUE}{BOLD}=== SUBARU TELEMETRY (LOGGING ENABLED) ==={RESET}")
                print(f"{YELLOW}Log File:{RESET} {log_filename}")
                print(f"{BLUE}-----------------------------------------{RESET}")
                
                row_data = [datetime.now().strftime("%H:%M:%S.%f")[:-3]]
                
                for name, command in subaru_sensors.items():
                    val = get_value(connection, command)
                    print(f"{BOLD}{name:<20}:{RESET} {GREEN}{val}{RESET}")
                    row_data.append(val)
                    
                print(f"{BLUE}-----------------------------------------{RESET}")
                print(f"{YELLOW}[Press CTRL+C to stop streaming]{RESET}")
                
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