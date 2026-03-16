# Universal OBD2 & CAN Diagnostic Suite
[![Build and Test](https://github.com/carsonh4te/obd-suite/actions/workflows/build-test.yml/badge.svg)](https://github.com/carsonh4te/obd-suite/actions/workflows/build-test.yml)

A containerized, CLI-based vehicle diagnostic toolkit designed for lightweight Linux environments. This suite utilizes an OBDLink EX (STN2232) adapter passed through to a privileged Docker container to perform standard OBD2 diagnostics, live telemetry logging, raw CAN bus sniffing, and deep UDS module querying.

## 📁 Directory Structure

Ensure your project folder looks like this before starting:

    obd-project/
    ├── Dockerfile
    ├── obd-suite                               # Main wrapper script
    ├── README.md
    └── scripts/
        ├── menu.py                             # Interactive Master Dashboard
        ├── read_codes.py                       # DTC scanner & clearer
        ├── live_data.py                        # Universal OBD2 telemetry
        ├── subaru_live.py                      # Subaru FB-engine specific telemetry
        ├── start_can.sh                        # CAN interface bridge setup
        ├── subaru_global_2017_generated.dbc    # Comma.ai OpenDBC Translation File
        ├── subi_can.py                         # Human-readable Subaru CAN decoder
        ├── uds_vin.py                          # Deep module query for VIN
        └── uds_probe.py                        # Interactive UDS DID probe

*Note: Make sure your wrapper and shell scripts are executable by running `chmod +x obd-suite scripts/start_can.sh` on your host machine.*

---

## 🚀 Setup & Launch Workflow

The entire environment is managed by the `obd-suite` wrapper script. It handles building the Docker image, checking for the physical USB connection (`/dev/ttyUSB0`), and passing the host directory into the container via a bind mount.

1. **Plug in the OBDLink EX cable** to your machine's USB port.
2. **Turn the vehicle's ignition to ON** (engine off for reading/clearing codes, engine running for live telemetry).
3. **Launch the suite:**
   * First-time setup or after updating the Dockerfile: `./obd-suite all`
   * Standard launch: `./obd-suite new`

The wrapper script will automatically launch the **Interactive Master Dashboard** (`menu.py`). When you exit a module, you will be dropped seamlessly back to the main menu.

---

## 🩺 Module 1: Code Scanning & Clearing (Option 1)
Queries the ECU for standard Diagnostic Trouble Codes (DTCs), decodes them, and provides an interactive prompt to clear them. Saves a `.txt` log to the `scripts/` folder.

---

## 📊 Module 2: Live Telemetry & Logging (Options 2 & 3)
Streams real-time sensor data (Universal or Subaru-specific) to a static terminal dashboard. Flushes all raw data continuously to a timestamped `.csv` file.

---

## 🕸️ Module 3: Raw CAN Bus Sniffing (Options 4 & 6)
**You MUST run Option 4 first to use any CAN or UDS tools.** This bridges the OBDLink EX to the virtual Linux network interface (`slcan0`).
Option 6 launches `cansniffer -c slcan0`, which groups the raw hexadecimal bus traffic by Arbitration ID and highlights changing bytes in red.

---

## 🧠 Module 4: Subaru CAN Decoding (Option 5)
Translates the raw hexadecimal CAN bus firehose into human-readable physical values (e.g., Steering Angle in degrees) in real-time using the Comma.ai database.

---

## 🔬 Module 5: Deep UDS Diagnostics (Options 7 & 8)
Bypasses standard OBD2 completely to speak Unified Diagnostic Services (UDS) directly to the Engine Control Module over the CAN bus via ISO-TP.
* **Option 7 (Read VIN):** Automatically sends a Service `0x22` request to Data Identifier (DID) `0xF190` to pull the hardcoded VIN from the module.
* **Option 8 (Manual Probe):** Acts as a reverse-engineering workbench. Prompts the user to enter custom 4-character hex DIDs (e.g., `F1A0`, `0100`) and displays the ECU's response in both raw hexadecimal and ASCII.
