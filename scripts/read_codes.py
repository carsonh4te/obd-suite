import obd
import sys
import os
from datetime import datetime

def main():
    # Setup logging paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    log_filename = os.path.join(script_dir, f"read_codes-{timestamp}.txt")
    
    print("=========================================")
    print("      OBD2 Diagnostic Code Scanner       ")
    print("=========================================")
    print("[!] TIP: Ensure the ignition is in the ON position.")
    print("-----------------------------------------")
    
    connection = obd.OBD("/dev/ttyUSB0", fast=False) 
    
    if not connection.is_connected():
        print("[-] Error: Failed to connect to the ECU.")
        sys.exit(1)
        
    protocol = connection.protocol_info().name
    print(f"[+] Connected successfully! Protocol: {protocol}")
    print("[+] Scanning for Diagnostic Trouble Codes (DTCs)...\n")
    
    response = connection.query(obd.commands.GET_DTC)
    dtcs = response.value 
    
    # Prepare log content
    log_content = f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    log_content += f"Protocol: {protocol}\n"
    log_content += "-" * 40 + "\n"
    
    if not dtcs:
        print("[+] No trouble codes found in the ECU. System is clean!")
        log_content += "Result: No trouble codes found.\n"
    else:
        print(f"[!] Found {len(dtcs)} stored code(s):")
        print("-" * 40)
        
        for code, description in dtcs:
            desc_text = description if description else "Unknown OEM-specific code"
            line = f"  > {code}: {desc_text}"
            print(line)
            log_content += line + "\n"
            
        print("-" * 40)
        
        choice = input("\n[?] Do you want to clear these codes? (y/N): ").strip().lower()
        if choice == 'y':
            connection.query(obd.commands.CLEAR_DTC)
            print("[+] Clear command sent! Check Engine Light should turn off.")
            log_content += "\nAction: Codes cleared by user.\n"
        else:
            print("\n[+] Codes were NOT cleared.")
            log_content += "\nAction: Codes retained.\n"
            
    # Write to log file
    with open(log_filename, "w") as f:
        f.write(log_content)
        
    print(f"\n[+] Log saved to: {log_filename}")
    connection.close()

if __name__ == "__main__":
    main()