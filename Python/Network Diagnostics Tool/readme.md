# NetDiag - Network Diagnostics Tool

## Complete Professional Documentation


***

## 1. Overview

### What is NetDiag?

**NetDiag** is a comprehensive, cross-platform command-line network diagnostics and troubleshooting tool written in Python. It combines multiple network testing capabilities into a single, easy-to-use interface with beautiful colored output powered by the `rich` library.

### Key Features

✅ **Single-Host Diagnostics:**

- Ping testing with packet loss and RTT statistics
- DNS lookups (A, MX records)
- HTTP/HTTPS connectivity checks
- SSL/TLS certificate inspection
- TCP port scanning (single/range)
- Traceroute path discovery
- PathPing (advanced hop-by-hop analysis)
- Network routing table display

✅ **Network Discovery:**

- CIDR-based network sweeps (ping all IPs in a subnet)
- Concurrent scanning with configurable workers
- Adjustable timeout settings

✅ **Local System Information:**

- Network interfaces and IP addresses
- ARP table entries
- Active TCP/UDP connections
- Internet speed test (download/upload/latency)

✅ **Output Flexibility:**

- Beautiful colored terminal output with tables and panels
- JSON export for automation/parsing
- File-based reporting

✅ **Cross-Platform:**

- Windows, Linux, macOS support
- Automatic platform detection and command adaptation


### Purpose and Use Cases

- **IT Support \& Help Desk:** Quick network connectivity troubleshooting
- **Network Administration:** Subnet discovery, host inventory, route verification
- **Security Auditing:** Port scanning, service discovery, certificate validation
- **DevOps \& Monitoring:** Scriptable diagnostics with JSON output
- **Education:** Learn network protocols and troubleshooting techniques

***

## 2. Architecture / Internals

### File Structure

```
netdiag/
├── netdiag_core.py      # Core diagnostic engine (backend functions)
└── netdiag_cli.py       # CLI interface and output formatting (frontend)
```


### Component Breakdown

#### **netdiag_core.py** - Core Engine

**Purpose:** Provides all diagnostic functions as reusable, standalone utilities.

**Key Functions:**


| Function | Purpose | Returns |
| :-- | :-- | :-- |
| `ping_host()` | ICMP echo test | Packet loss, RTT min/avg/max |
| `traceroute()` | Path discovery | Hop-by-hop route data |
| `port_scan()` | TCP port connectivity | Dict of port:open/closed |
| `dns_lookup()` | DNS resolution | A/MX records |
| `http_check()` | HTTP response | Status code, headers, latency |
| `ssl_info()` | Certificate details | Subject, issuer, validity dates |
| `interfaces_info()` | Local NICs | IPs, netmask, up/down status |
| `arp_table()` | ARP cache | IP↔MAC mappings |
| `open_connections()` | Active sockets | Local/remote addr, PID, state |
| `speedtest()` | Bandwidth test | Download/upload Mbps, latency |
| `network_sweep()` | Subnet scan | List of alive IPs |
| `pathping()` | Advanced traceroute | Per-hop loss and RTT stats |
| `route_print()` | Routing table | Active routes with metrics |
| `run_all()` | Orchestrator | Runs all selected tests concurrently |

**Design Patterns:**

- **Async/Concurrency:** Port scanning uses `asyncio` for speed
- **Error Handling:** All functions return dicts with `error` key on failure
- **Platform Abstraction:** Commands auto-adjust for Windows/Linux
- **Optional Dependencies:** Gracefully degrades if `psutil`, `dns.resolver`, or `requests` unavailable


#### **netdiag_cli.py** - CLI Interface

**Purpose:** Command-line argument parsing, user interaction, and formatted output display.

**Key Components:**


| Component | Purpose |
| :-- | :-- |
| `parse_ports()` | Converts "22,80,443,8000-8100" → list of ints |
| `main()` | Argument parser, execution controller |
| Output sections | Ping, DNS, HTTP, SSL, Ports, Traceroute, etc. formatters |

**Output Features:**

- Color-coded status (green=success, red=error, yellow=warning)
- Structured tables for ports, connections, routes
- Progress indicators for network sweeps
- Panels for target information

***

### How Components Interact

```
User Input (CLI args)
        ↓
   netdiag_cli.py (parse arguments)
        ↓
   netdiag_core.py (execute diagnostics)
        ↓
   Return JSON-like dicts
        ↓
   netdiag_cli.py (format & display with rich)
```

**Execution Flow:**

1. Parse CLI arguments (`argparse`)
2. Check for network sweep mode (`--sweep`) → exit after sweep
3. Validate `--host` is provided (if not sweeping)
4. Build options dict from flags
5. Call `run_all()` with host, options, ports
6. `run_all()` spawns concurrent workers for each diagnostic
7. Collect results into master report dict
8. Format and display (or export JSON)

***

### Important Variables \& Configurations

**Core Module (`netdiag_core.py`):**

- `LOG`: Logger instance for info/debug messages
- `psutil`, `dns`, `requests`: Optional dependencies (checked at import)
- `timeout`: Default command timeout (30s, customizable per function)
- `concurrency`: Default port scan workers (200)

**CLI Module (`netdiag_cli.py`):**

- `console`: Rich Console instance for styled output
- `opts`: Dictionary mapping CLI flags to boolean enables
- `args`: Parsed argument namespace

***

## 3. Execution Guide

### Environment Requirements

**Python Version:** 3.7+

**Operating Systems:**

- Windows 10/11
- Linux (Ubuntu, Debian, CentOS, Fedora, etc.)
- macOS

**Permissions:**

- Regular user for most functions
- **Administrator/root** required for:
    - Port scanning (< 1024 ports)
    - Network sweep (raw socket access)
    - ARP table access (some systems)
    - Routing table access (some systems)

***

### Dependencies

**Required:**

```bash
pip install rich
```

**Optional (for full functionality):**

```bash
pip install psutil dnspython requests speedtest-cli
```

**Dependency Matrix:**


| Feature | Required Packages |
| :-- | :-- |
| Ping, Traceroute, Route | ✅ Built-in (no deps) |
| Colored Output | `rich` |
| Network Interfaces | `psutil` (fallback to OS commands) |
| DNS (advanced) | `dnspython` (fallback to `socket`) |
| HTTP Check | `requests` |
| Speed Test | `speedtest-cli` |
| Port Scan | ✅ Built-in (`asyncio`) |


***

### Installation

```bash
# Clone or download the files
git clone https://github.com/yourusername/netdiag.git
cd netdiag

# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install rich psutil dnspython requests speedtest-cli

# Make CLI executable (Linux/macOS)
chmod +x netdiag_cli.py

# Run
python netdiag_cli.py --help
```


***

### CLI Usage Examples

#### **Basic Ping Test**

```bash
python netdiag_cli.py --host google.com --ping
```


#### **Full Diagnostics Suite**

```bash
python netdiag_cli.py --host 8.8.8.8 --ping --dns --http --traceroute
```


#### **Port Scan**

```bash
# Single ports
python netdiag_cli.py --host example.com --ports 22,80,443

# Port range
python netdiag_cli.py --host 192.168.1.1 --ports 1-1024

# Mixed
python netdiag_cli.py --host scanme.nmap.org --ports 21,22,80,443,3000-3010
```


#### **Network Sweep (Subnet Discovery)**

```bash
# Standard /24 network
python netdiag_cli.py --sweep 192.168.1.0/24

# Larger network with custom settings
python netdiag_cli.py --sweep 10.0.0.0/16 --sweep-timeout 2 --sweep-workers 100

# Smaller subnet
python netdiag_cli.py --sweep 192.168.1.0/28
```


#### **Local System Information**

```bash
# Network interfaces
python netdiag_cli.py --host localhost --interfaces

# Active connections
python netdiag_cli.py --host localhost --conns

# ARP table
python netdiag_cli.py --host localhost --arp

# Routing table
python netdiag_cli.py --host localhost --route
```


#### **Advanced Diagnostics**

```bash
# PathPing (hop-by-hop loss analysis)
python netdiag_cli.py --host google.com --pathping

# SSL Certificate Check
python netdiag_cli.py --host github.com --ssl

# Speed Test
python netdiag_cli.py --host google.com --speed
```


#### **JSON Output \& Reporting**

```bash
# Print JSON to console
python netdiag_cli.py --host 1.1.1.1 --ping --dns --json

# Save to file
python netdiag_cli.py --host cloudflare.com --ping --dns --report cloudflare_report.json

# Pipe to jq for parsing
python netdiag_cli.py --host example.com --ping --json | jq '.ping.avg'
```


***

### All Supported Command-Line Arguments

| Argument | Type | Description | Example |
| :-- | :-- | :-- | :-- |
| `--host` | string | Target hostname or IP address | `--host google.com` |
| `--ping` | flag | Run ping test (4 packets, RTT/loss stats) | `--ping` |
| `--traceroute` | flag | Trace route to host | `--traceroute` |
| `--dns` | flag | Perform DNS lookup (A, MX records) | `--dns` |
| `--http` | flag | Check HTTP connectivity and response time | `--http` |
| `--ssl` | flag | Retrieve and display SSL/TLS certificate | `--ssl` |
| `--ports` | string | Comma-separated ports or ranges to scan | `--ports 22,80,443,8000-8100` |
| `--arp` | flag | Display ARP table | `--arp` |
| `--interfaces` | flag | Show local network interfaces | `--interfaces` |
| `--conns` | flag | List active network connections | `--conns` |
| `--speed` | flag | Run internet speed test (requires speedtest-cli) | `--speed` |
| `--pathping` | flag | Advanced traceroute with per-hop statistics | `--pathping` |
| `--route` | flag | Display routing table | `--route` |
| `--sweep` | CIDR | Network sweep (ping all IPs in range) | `--sweep 192.168.1.0/24` |
| `--sweep-timeout` | int | Timeout per host in sweep (seconds, default: 1) | `--sweep-timeout 2` |
| `--sweep-workers` | int | Concurrent workers for sweep (default: 50) | `--sweep-workers 100` |
| `--json` | flag | Output results as JSON | `--json` |
| `--report` | file | Save report to JSON file | `--report output.json` |


***

## 4. Workflow Explanation

### Step-by-Step Execution Flow

**1. Argument Parsing**

- CLI collects all user flags/options
- Validates required arguments (either `--host` or `--sweep`)

**2. Network Sweep Branch (if `--sweep` provided)**

- Call `network_sweep()` with CIDR range
- Spawn `workers` threads to ping all IPs concurrently
- Display alive hosts in real-time
- Exit after completing sweep

**3. Single-Host Diagnostics Branch**

- Build `opts` dictionary from flags
- Parse port list if `--ports` provided
- Call `run_all(host, opts, ports)`

**4. Core Execution (`run_all` in netdiag_core.py)**

- Resolve hostname → IP
- Execute ping \& traceroute sequentially (if requested)
- Spawn ThreadPoolExecutor for parallel tasks:
    - DNS lookup
    - HTTP check
    - SSL info
    - Port scan
    - Local system info (interfaces, ARP, connections)
    - Speed test
    - Route table
- Collect all results into `report` dict

**5. Output Formatting**

- If `--json` or `--report`: serialize to JSON
- Otherwise: format with Rich library
    - Colored panels, tables, status indicators
    - Section-by-section display (Ping, DNS, HTTP, etc.)

**6. Exit**

- Return to shell with status code 0 (success) or 1 (error)

***

### Input/Output Behavior

**Input Types:**

- **Hostname:** `google.com`, `example.org`
- **IPv4 Address:** `8.8.8.8`, `192.168.1.1`
- **CIDR Notation:** `10.0.0.0/24`, `172.16.0.0/16`
- **Port Specifications:** `80`, `22,443`, `1-1024`, `8000-8100`

**Output Types:**

- **Terminal (default):** Color-coded, formatted with tables/panels
- **JSON (--json):** Machine-readable structured data
- **File (--report):** JSON saved to specified path

***

### Error Handling Logic

**Per-Function Level:**

- All diagnostic functions return dict with `error` key on failure
- Example: `{"host": "example.com", "error": "Connection timeout"}`

**CLI Level:**

- Missing `--host` (and no `--sweep`): Print error + help, exit
- Invalid CIDR in `--sweep`: Display error message
- Missing dependencies: Graceful fallback or install hint
    - Example: Speed test without `speedtest-cli` → "Module not installed, run: pip install speedtest-cli"

**Core Level:**

- Command timeout: Return `-1` return code, indicate timeout
- DNS resolution failure: Record in report, continue with other tests
- Port scan exceptions: Mark ports as closed/filtered

***

### Logging Behavior

**Log Level:** INFO (default)

**Log Destination:** Console (stderr)

**Log Format:** `%(asctime)s - %(levelname)s - %(message)s`

**Logged Events:**

- Network sweep start/completion
- Alive hosts discovered
- Function errors (debug purposes)

**To Enable Debug Logging:**

```python
# In netdiag_core.py, change:
logging.basicConfig(level=logging.DEBUG, ...)
```


***

## 5. Security Notes \& Best Practices

### Risks

⚠️ **Port Scanning:**

- Can trigger IDS/IPS alerts
- May violate network policies or laws if performed without authorization
- **Never scan networks you don't own or have permission to test**

⚠️ **Network Sweep:**

- Generates high volumes of ICMP traffic
- Can be mistaken for reconnaissance/attack
- Use only on authorized networks

⚠️ **Speed Test:**

- Consumes bandwidth during testing
- May impact other users on shared connections

⚠️ **Credential Exposure:**

- Avoid storing sensitive data in reports
- JSON reports may contain internal network topology


### Safe Deployment

✅ **Authorization:**

- Always obtain written permission before scanning
- Document authorized IP ranges and tests

✅ **Rate Limiting:**

- Use conservative sweep settings (lower workers, higher timeout)
- Avoid aggressive port scanning on production systems

✅ **Monitoring:**

- Log all scan activities with timestamps
- Integrate with SIEM for audit trails

✅ **Least Privilege:**

- Run as non-root when possible
- Use sudo/runas only for required functions


### Access Control

**Restrict Tool Access:**

```bash
# Linux: Limit to specific group
chown root:netadmin netdiag_cli.py
chmod 750 netdiag_cli.py

# Create wrapper with logging
#!/bin/bash
logger "NetDiag executed by $USER: $*"
python3 /opt/netdiag/netdiag_cli.py "$@"
```

**Firewall Rules:**

- Allow ICMP outbound (ping/traceroute)
- Allow DNS queries (UDP 53)
- Allow HTTP/HTTPS (TCP 80/443)


### Production-Ready Considerations

✅ **Input Validation:**

- Sanitize hostnames to prevent command injection
- Validate CIDR notation before network sweep

✅ **Resource Limits:**

- Set max concurrent workers (avoid DoS to local system)
- Implement timeout caps (prevent hung processes)

✅ **Scheduling:**

- Run scans during maintenance windows
- Use cron/scheduled tasks with logging

✅ **Reporting:**

- Centralize JSON reports for trend analysis
- Archive old reports per retention policy

***

## 6. Troubleshooting

### Common Issues

#### **Issue: "Module not found: rich"**

**Cause:** Missing dependency
**Fix:**

```bash
pip install rich
```


#### **Issue: "Permission denied" when running port scan**

**Cause:** Ports < 1024 require admin rights
**Fix:**

```bash
# Linux
sudo python netdiag_cli.py --host example.com --ports 22,80,443

# Windows (Run as Administrator)
# Right-click CMD/PowerShell → Run as Administrator
```


#### **Issue: Network sweep returns no alive hosts**

**Cause:** Firewall blocking ICMP, or incorrect CIDR
**Fix:**

- Verify CIDR notation is correct
- Test single host first: `--host 192.168.1.1 --ping`
- Check firewall allows ICMP egress
- Increase timeout: `--sweep-timeout 3`


#### **Issue: "speedtest-cli not installed"**

**Cause:** Optional dependency missing
**Fix:**

```bash
pip install speedtest-cli
```


#### **Issue: Traceroute shows "no traceroute available" on Linux**

**Cause:** Missing system utility
**Fix:**

```bash
# Debian/Ubuntu
sudo apt-get install traceroute

# RHEL/CentOS
sudo yum install traceroute
```


#### **Issue: SSL check fails with "Connection refused"**

**Cause:** Target doesn't support HTTPS or port 443 blocked
**Fix:**

- Verify target supports HTTPS: Try browser first
- Check if custom port needed: Modify `ssl_info()` call in code


#### **Issue: JSON output is truncated or malformed**

**Cause:** Special characters in hostnames/data
**Fix:**

- Already handled by `json.dumps()`, but verify with `jq`:

```bash
python netdiag_cli.py --host example.com --ping --json | jq .
```


***

### How to Verify Correct Execution

**1. Test Basic Ping:**

```bash
python netdiag_cli.py --host 8.8.8.8 --ping
```

**Expected:** Green checkmark, 0% packet loss, RTT values

**2. Test JSON Output:**

```bash
python netdiag_cli.py --host google.com --ping --dns --json
```

**Expected:** Valid JSON structure (test with `jq` or `json.tool`)

**3. Test Network Sweep:**

```bash
python netdiag_cli.py --sweep 127.0.0.1/32
```

**Expected:** Shows `127.0.0.1` as alive

**4. Test Error Handling:**

```bash
python netdiag_cli.py --host nonexistent.invalid --ping
```

**Expected:** Red error message, graceful failure

***

## 7. Enhancement Suggestions

### Code Improvements

**1. Add Logging to File:**

```python
# In netdiag_core.py
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("netdiag.log"),
        logging.StreamHandler()
    ]
)
```

**2. Implement Progress Bars for Long Operations:**

```python
# Use rich.progress for network sweeps
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("[cyan]Scanning...", total=len(hosts))
    for host in hosts:
        # ... ping logic ...
        progress.update(task, advance=1)
```

**3. Add Configuration File Support:**

```python
# Load defaults from netdiag.conf
import configparser
config = configparser.ConfigParser()
config.read('netdiag.conf')
default_timeout = config.getint('sweep', 'timeout', fallback=1)
```

**4. Implement Retry Logic:**

```python
# Retry failed pings
for attempt in range(3):
    result = ping_host(host)
    if "error" not in result:
        break
    time.sleep(1)
```


***

### Feature Addition Ideas

**1. Historical Comparison:**

- Store previous scan results
- Compare current vs. previous (detect new/removed hosts)

**2. Geolocation Lookup:**

- Integrate with IP geolocation API
- Show approximate location of external IPs

**3. Service Version Detection:**

- Enhance port scan to grab banners
- Identify service versions (SSH, HTTP server, etc.)

**4. MAC Address Vendor Lookup:**

- Parse OUI database
- Show manufacturer for MAC addresses

**5. Email/Webhook Notifications:**

- Alert on anomalies (new hosts, port changes)
- Integrate with Slack, Discord, email

**6. GUI Interface:**

- Build PyQt or Tkinter frontend
- Visual network map

**7. Automated Scheduling:**

- Built-in cron-like scheduler
- Run daily/hourly scans automatically

**8. Plugin System:**

- Allow custom diagnostic modules
- Load additional checks dynamically

***

### Performance Tuning Tips

**1. Optimize Port Scanning:**

```python
# Increase concurrency for faster scans
port_scan(host, ports, concurrency=500)  # Default: 200
```

**2. Reduce Network Sweep Timeout:**

```python
# For fast local networks
--sweep-timeout 0.5  # Default: 1
```

**3. Cache DNS Results:**

```python
# Add LRU cache to dns_lookup
from functools import lru_cache

@lru_cache(maxsize=128)
def dns_lookup_cached(host):
    return dns_lookup(host)
```

**4. Batch Processing:**

```python
# Process multiple hosts from file
for host in open('hosts.txt'):
    result = run_all(host.strip(), opts, ports)
    # ... save results ...
```

**5. Use Async for All I/O:**

- Migrate more functions to `asyncio`
- Fully async HTTP checks, DNS, etc.

***

## Complete CLI Commands Reference

### Quick Reference Cheat-Sheet

```bash
# ═══════════════════════════════════════════════════════════
# NETDIAG QUICK REFERENCE
# ═══════════════════════════════════════════════════════════

# Basic Diagnostics
python netdiag_cli.py --host <target> --ping
python netdiag_cli.py --host <target> --dns
python netdiag_cli.py --host <target> --http
python netdiag_cli.py --host <target> --traceroute

# Port Scanning
python netdiag_cli.py --host <target> --ports 22,80,443
python netdiag_cli.py --host <target> --ports 1-1024

# Network Discovery
python netdiag_cli.py --sweep 192.168.1.0/24
python netdiag_cli.py --sweep 10.0.0.0/16 --sweep-workers 100

# Local System Info
python netdiag_cli.py --host localhost --interfaces
python netdiag_cli.py --host localhost --arp
python netdiag_cli.py --host localhost --conns
python netdiag_cli.py --host localhost --route

# Advanced
python netdiag_cli.py --host <target> --pathping
python netdiag_cli.py --host <target> --ssl
python netdiag_cli.py --host <target> --speed

# Output Options
python netdiag_cli.py --host <target> --ping --json
python netdiag_cli.py --host <target> --ping --report output.json

# Combined Tests
python netdiag_cli.py --host <target> --ping --dns --http --traceroute --ports 80,443
```


***

## Real-World Usage Examples

### **Example 1: IT Help Desk - Troubleshoot User Connectivity**

```bash
# User reports: "Can't access company website"
python netdiag_cli.py --host companysite.com --ping --dns --http --traceroute

# Check if issue is local network or ISP
python netdiag_cli.py --host 8.8.8.8 --ping
python netdiag_cli.py --host localhost --interfaces --route
```


### **Example 2: Network Admin - Inventory New Subnet**

```bash
# Discover all devices on new subnet
python netdiag_cli.py --sweep 192.168.50.0/24 --report subnet50_inventory.json

# Identify open SSH/HTTP services
# (After getting alive IPs from sweep)
python netdiag_cli.py --host 192.168.50.10 --ports 22,80,443,3389,8080
```


### **Example 3: Security Audit - Certificate Expiry Check**

```bash
# Check SSL certificates on all web servers
for host in web1.example.com web2.example.com web3.example.com; do
    python netdiag_cli.py --host $host --ssl --json | jq '.ssl.notAfter'
done
```


### **Example 4: DevOps - Monitor Critical Services**

```bash
# Automated monitoring script
python netdiag_cli.py --host db.example.com --ports 3306 --json > db_status.json
python netdiag_cli.py --host api.example.com --http --json > api_status.json

# Parse and alert if failures detected
jq -e '.ping.loss == 0' db_status.json || send_alert "DB unreachable"
```


### **Example 5: Home Network - Troubleshoot Speed Issues**

```bash
# Check internet speed
python netdiag_cli.py --host google.com --speed

# Verify no local network congestion
python netdiag_cli.py --host localhost --conns | grep ESTABLISHED | wc -l

# Test gateway latency
python netdiag_cli.py --host 192.168.1.1 --ping
```


***

## Final Security Reminder

**⚠️ IMPORTANT:**

- **Always obtain authorization** before scanning any network or host
- **Log all scan activities** for auditing and accountability
- **Use responsibly** - scanning networks without permission may violate laws and policies
- **This tool is for authorized IT professionals, educators, and researchers only**

***

**End of Documentation**

*NetDiag - Professional Network Diagnostics Tool*
*Version: 1.0 | Last Updated: November 28, 2025*
<span style="display:none">[^1][^2]</span>

<div align="center">⁂</div>

[^1]: netdiag_cli.py

[^2]: netdiag_core.py

