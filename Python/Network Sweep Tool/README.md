# Network Sweep Tool

A fast, cross-platform Python command-line tool that scans a subnet to discover all active devices on your network. It collects IP addresses, hostnames, MAC addresses, device vendors, TTL values, and response times using concurrent ping sweeps.

---

## Features

- Concurrent scanning — scans up to 254 hosts in parallel using ThreadPoolExecutor
- MAC address lookup — retrieves hardware addresses from the ARP table
- Vendor identification — resolves manufacturer name from MAC using the IEEE OUI database
- Hostname resolution — reverse DNS lookup for each active host
- OS detection — guesses device OS type (Windows / Linux / Network Device) from TTL value
- JSON output — export full results as JSON for scripting or logging
- Auto network detection — detects your local subnet automatically if no target is provided
- Cross-platform — works on Windows and Linux

---

## Sample Output

```
================================================================================
Network Sweep Tool
================================================================================
Scanning network: 192.168.1.0/24
Total hosts to scan: 254
Using 50 concurrent workers
--------------------------------------------------------------------------------
[v] 192.168.1.1     - UP | TTL=64  | RTT=2ms  | MAC=B4:3D:08:3D:FA:D0 | Name=MYGROUP         | Vendor=GX International BV
[v] 192.168.1.7     - UP | TTL=128 | RTT=1ms  | MAC=FC:34:97:BF:54:71 | Name=BALSAM-10       | Vendor=ASUSTek COMPUTER INC.
[v] 192.168.1.9     - UP | TTL=128 | RTT=1ms  | MAC=A0:36:BC:24:D0:4F | Name=DESKTOP-HEDNV3K | Vendor=ASUSTek COMPUTER INC.
[v] 192.168.1.50    - UP | TTL=128 | RTT=1ms  | MAC=B0:6E:BF:D2:E2:10 | Name=SERVER          | Vendor=ASUSTek COMPUTER INC.

================================================================================
NETWORK SWEEP SUMMARY
================================================================================
Network:             192.168.1.0/24
Total hosts scanned: 254
Active hosts:        12
Inactive hosts:      242
Duration:            6.1 seconds
================================================================================
```

---

## Requirements

- Python 3.7 or higher
- mac-vendor-lookup (one third-party package, install instructions below)

All other libraries used in this project such as ipaddress, socket, subprocess, concurrent.futures, re, platform, and time are part of the Python standard library and do not require any installation.

---

## Installation

**Step 1 — Clone the repository**

```bash
git clone https://github.com/your-username/network-sweep.git
cd network-sweep
```

**Step 2 — Install the required package**

On Windows:
```cmd
pip install -r requirements.txt
```

On Linux or Kali Linux:
```bash
sudo pip install -r requirements.txt --break-system-packages
```

Using a virtual environment (recommended for Linux):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Basic Commands

```bash
# Auto-detect local network and scan it
python network_sweep.py

# Scan a specific subnet
python network_sweep.py 192.168.1.0/24
```

### With Optional Flags

```bash
# Set a custom ping timeout in seconds (default is 1)
python network_sweep.py 192.168.1.0/24 --timeout 2

# Set a custom number of concurrent workers (default is 50)
python network_sweep.py 192.168.1.0/24 --workers 100

# Output the results as JSON
python network_sweep.py 192.168.1.0/24 --json

# Combine all options together
python network_sweep.py 192.168.1.0/24 --timeout 2 --workers 100 --json
```

### Save Output to a File

```bash
# Save plain text output
python network_sweep.py 192.168.1.0/24 > results.txt

# Save as JSON
python network_sweep.py 192.168.1.0/24 --json > results.json
```

### Running with Admin Privileges

MAC address resolution requires administrator or root access to read the system ARP table. Without it, MAC and vendor fields will show as N/A.

On Windows, open Command Prompt as Administrator then run:
```cmd
python network_sweep.py 192.168.1.0/24
```

On Linux, run with sudo:
```bash
sudo python network_sweep.py 192.168.1.0/24
```

---

## Arguments Reference

| Argument    | Type               | Default     | Description                                          |
|-------------|--------------------|-------------|------------------------------------------------------|
| network     | positional/optional| auto-detect | Target subnet in CIDR notation e.g. 192.168.1.0/24  |
| --timeout   | int                | 1           | Ping timeout per host in seconds                     |
| --workers   | int                | 50          | Number of concurrent threads for scanning            |
| --json      | flag               | off         | Print full results as JSON instead of a table        |

---

## How It Works

The script runs as follows when executed:

```
network_sweep.py
|
|-- auto_detect_local_network()   Finds your local subnet using a UDP socket
|
|-- network_sweep()               Main scan function, spawns a thread pool
|   |-- ping_single_host()        Pings one IP and extracts TTL and RTT
|       |-- get_mac_address()     Queries the OS ARP table for the MAC address
|       |-- get_hostname()        Performs a reverse DNS lookup
|       |-- get_vendor_from_mac() Looks up manufacturer via mac-vendor-lookup
|
|-- identify_device_type()        Guesses the OS from the TTL value
```

TTL-based OS detection works as follows:

| TTL Value | Likely OS                    |
|-----------|------------------------------|
| 64 or below  | Linux or Unix             |
| 128 or below | Windows                   |
| 255 or below | Network Device (Router, Switch) |

---

## Platform Notes

| Feature            | Windows      | Linux (native)       | Linux (WSL)              |
|--------------------|--------------|----------------------|--------------------------|
| Host discovery     | Yes          | Yes, needs sudo      | Limited due to NAT       |
| MAC resolution     | Yes          | Yes, needs sudo      | Not available            |
| Vendor lookup      | Yes          | Yes                  | Not available (no MAC)   |
| Hostname resolution| Yes          | Yes                  | Partial                  |

If you are running this tool inside WSL (Windows Subsystem for Linux), MAC addresses and vendor information will not resolve. This is because WSL runs behind a NAT layer that is separate from your actual LAN. For full results, run the script natively on Windows or on a physical Linux machine.

---

## Project Structure

```
network-sweep/
|-- network_sweep.py    Main script
|-- requirements.txt    Python dependencies
|-- README.md           Project documentation
```

---

## License

MIT License. Free to use, modify, and distribute.
