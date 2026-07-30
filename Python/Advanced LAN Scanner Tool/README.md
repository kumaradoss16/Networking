# Advanced LAN Network Scanner

A multi-threaded Python LAN scanner that discovers live hosts on a subnet, fingerprints their likely OS, resolves MAC vendors, grabs hostnames, and probes the top 100 common TCP ports — then exports everything to JSON and CSV.

## Features

- **Two-phase scanning** — fast ICMP ping sweep to find alive hosts, followed by a deep scan of only those hosts (avoids wasting time on dead IPs).
- **OS fingerprinting** — infers the likely OS (Windows, Linux/Unix, macOS/iOS, Android, network device) from TTL values and MAC vendor.
- **MAC vendor lookup** — reads the ARP table and resolves the manufacturer via `mac-vendor-lookup`.
- **Hostname resolution** — reverse DNS lookups for alive hosts.
- **Port scanning** — checks the top 100 commonly used ports with basic banner grabbing.
- **Multi-threaded** — uses `ThreadPoolExecutor` for parallel ping sweeps, per-host scans, and per-port scans for fast results on a `/24` network.
- **Reporting** — saves results as a JSON report, a detailed CSV (one row per open port), and a summary CSV (one row per host).
- **Cross-platform** — works on Windows, Linux, and macOS.

## Requirements

- Python 3.9+ (uses `tuple[...]` / `list[...]` type hints)
- [`mac-vendor-lookup`](https://pypi.org/project/mac-vendor-lookup/)

Install dependencies:

```bash
pip install mac-vendor-lookup
```

> **Note:** `mac-vendor-lookup` downloads/caches an OUI vendor database on first use, so an internet connection may be required the first time you run the scanner.

## Usage

```bash
python advanced_lan_scanner.py <network/prefix>
```

### Examples

```bash
python advanced_lan_scanner.py 192.168.1.0/24
python advanced_lan_scanner.py 10.0.0.0/24
```

The scanner will:

1. **Ping-sweep** the given subnet to find alive hosts.
2. **Deep-scan** each alive host: OS guess, MAC/vendor, hostname, and open ports.
3. Print a **detailed breakdown** per host and **aggregate statistics**.
4. **Save reports** to the current directory.

## Sample Output

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    LAN NETWORK SCANNER - DETAILED PORT VIEW              ║
╚══════════════════════════════════════════════════════════════════════════╝

 Step 1: Finding Alive Hosts in 192.168.1.0/24...
============================================================
  ✔  192.168.1.1 is UP  (TTL=64)
  ✔  192.168.1.20 is UP  (TTL=128)
============================================================
Found 2 alive hosts

Step 2: Scanning 2 alive host(s) for open ports...
============================================================

[1/2] Host: 192.168.1.1
     OS       : Linux / Unix
     MAC      : AA:BB:CC:11:22:33
     Hostname : router.local
     Open Ports: 3

================================================================================
DETAILED SCAN RESULTS — OPEN PORTS PER HOST
================================================================================

┌─ HOST #1: 192.168.1.1
│   Hostname  : router.local
│   OS        : Linux / Unix  (TTL=64)
│   MAC       : AA:BB:CC:11:22:33  [Some Vendor Inc.]
│   Open Ports: 3
│
│   OPEN PORTS:
│   ──────────────────────────────────────────────────────────────────
│   PORT      SERVICE               BANNER
│   ──────────────────────────────────────────────────────────────────
│   22        SSH                   SSH-2.0-OpenSSH_8.9
│   80        HTTP
│   443       HTTPS
└──────────────────────────────────────────────────────────────────────────

   SCAN STATISTICS
================================================================================
   Total Hosts Scanned  : 2
   Total Open Ports     : 5
   Windows Systems      : 1
   Linux / Unix Systems : 1
   Android Devices      : 0
   Apple Devices        : 0
   Network Devices      : 0

   Most Common Open Ports:
     Port    80  (HTTP              )  found on 2 host(s)
     ...

================================================================================
   REPORTS SAVED
================================================================================
   JSON Report  : scan_report_20260730-120000.json
   Detailed CSV : scan_report_20260730-120000.csv
   Summary CSV  : scan_summary_20260730-120000.csv

================================================================================
   SCAN COMPLETED in 8.42 seconds
================================================================================
```

## Output Files

Each run generates three timestamped files in the working directory:

| File | Description |
|---|---|
| `scan_report_<timestamp>.json` | Full structured results (all hosts + all fields) |
| `scan_report_<timestamp>.csv` | One row per open port (IP, hostname, OS, TTL, MAC, vendor, port, service, banner) |
| `scan_summary_<timestamp>.csv` | One row per host with a comma-separated list of open ports |

## How It Works

1. **Ping sweep** (`find_alive_hosts`) — every address in the subnet is pinged in parallel (up to 150 workers) using the platform-native `ping` command. TTL is extracted from the reply to help with OS fingerprinting.
2. **OS guess** (`guess_os`) — TTL ranges (≥200, ≥128, ≥64) combined with MAC vendor heuristics are used to classify a host as Network Device, Windows, Apple, Android, or Linux/Unix.
3. **MAC & vendor** (`get_mac`) — reads the local ARP table entry for the host and resolves the vendor via `mac-vendor-lookup`.
4. **Hostname** (`get_hostname`) — reverse DNS lookup, best-effort.
5. **Port scan** (`scan_alive_host` / `scan_port`) — each host's top 100 ports are scanned in parallel (up to 50 workers per host), with a lightweight banner grab on open ports.
6. **Reporting** (`save_results`) — results are written to JSON and two CSV formats.

## Notes & Limitations

- Requires appropriate OS-level permissions to run `ping` and read the ARP table.
- ARP-based MAC lookup only works for hosts on the same local subnet/broadcast domain.
- Port and OS detection are heuristic (TTL/banner-based) and not guaranteed to be 100% accurate.
- Intended for scanning networks you own or have explicit permission to scan.

## Disclaimer

This tool is intended for authorized network administration, auditing, and educational purposes only. Only scan networks and devices you own or have explicit permission to test. Unauthorized scanning of networks may be illegal in your jurisdiction.

## License

MIT License — feel free to use, modify, and distribute.
