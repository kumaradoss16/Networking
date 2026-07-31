"""
Advanced LAN Network Scanner 
"""

import csv
import ipaddress
import json
import platform
import re
import socket
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Optional
import sys
import time

from mac_vendor_lookup import MacLookup

# Constants

TOP_100_PORTS = [
    20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 111, 123, 135, 137, 138, 139,
    143, 161, 389, 443, 445, 514, 587, 631, 636, 873, 902, 989, 990, 993, 995,
    1025, 1026, 1027, 1028, 1433, 1434, 1723, 2049, 2082, 2083, 2181, 2375,
    2376, 2484, 2487, 3050, 3128, 3306, 3389, 3690, 4369, 5000, 5432, 5555,
    5672, 5900, 5985, 5986, 6379, 6443, 6667, 6881, 7001, 7002, 7077, 8000,
    8008, 8080, 8081, 8123, 8443, 8888, 9000, 9001, 9042, 9092, 9200, 9300,
    9418, 11211, 27017, 27018, 27019, 28017,
]

PORT_SERVICES = {
    20: "FTP-Data",    21: "FTP",          22: "SSH",          23: "Telnet",
    25: "SMTP",        53: "DNS",          67: "DHCP",         68: "DHCP",
    69: "TFTP",        80: "HTTP",         110: "POP3",        111: "RPC",
    123: "NTP",        135: "MS-RPC",      137: "NetBIOS",     138: "NetBIOS",
    139: "NetBIOS",    143: "IMAP",        161: "SNMP",        389: "LDAP",
    443: "HTTPS",      445: "SMB",         514: "Syslog",      587: "SMTP",
    631: "IPP",        636: "LDAPS",       873: "Rsync",       902: "VMware",
    989: "FTPS",       990: "FTPS",        993: "IMAPS",       995: "POP3S",
    1025: "MS-RPC",    1433: "MSSQL",      1434: "MSSQL",      1723: "PPTP",
    2049: "NFS",       2082: "cPanel",     2083: "cPanel",     3306: "MySQL",
    3389: "RDP",       3690: "SVN",        5000: "UPnP",       5432: "PostgreSQL",
    5555: "ADB",       5672: "RabbitMQ",   5900: "VNC",        5985: "WinRM",
    5986: "WinRM-SSL", 6379: "Redis",      6443: "Kubernetes", 7001: "WebLogic",
    8000: "HTTP-Alt",  8008: "HTTP-Alt",   8080: "HTTP-Proxy", 8081: "HTTP-Alt",
    8123: "Polipo",    8443: "HTTPS-Alt",  8888: "HTTP-Alt",   9000: "SonarQube",
    9042: "Cassandra", 9092: "Kafka",      9200: "Elasticsearch", 9300: "Elasticsearch",
    11211: "Memcached", 27017: "MongoDB",  27018: "MongoDB",   27019: "MongoDB",
}

ANDROID_VENDORS = {
    "samsung", "xiaomi", "redmi", "realme", "oppo", "vivo", "oneplus",
    "motorola", "google", "huawei", "honor", "sony", "asus", "nokia", "hmd",
}

# FIX A: MacLookup instantiated once at module level (not per-call)
_mac_lookup = MacLookup()
_mac_lookup_lock = threading.Lock()

# Host Discovery

def ping_host(ip: str) -> tuple[bool, Optional[int]]:
    try:
        if platform.system().lower() == "windows":
            # FIX 1: "-n", "1" not "-n", 1
            cmd = ["ping", "-n", "1", "-w", "500", ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        output = result.stdout

        # FIX 3: one case-insensitive check is enough
        if "ttl=" in output.lower():
            return True, extract_ttl(output)
        return False, None
    except Exception:
        return False, None


def extract_ttl(output: str) -> Optional[int]:
    """
    Parse TTL from ping output.
    FIX 2: Corrected regex — 'ttl=64' had no separator between '=' and digits.
    """
    match = re.search(r"ttl[=:](\d+)", output, re.IGNORECASE)
    return int(match.group(1)) if match else None


def guess_os(ttl: Optional[int], vendor: str = "") -> str:
    """
    Infer OS from TTL and MAC vendor.
    FIX 4: Check ttl >= 200 BEFORE ttl >= 128 — otherwise Network Devices
           were always classified as Windows (200 > 128, branch was dead).
    """
    if ttl is None:
        return "Unknown"

    vendor = vendor.lower()

    # FIX 4: highest range first
    if ttl >= 200:
        return "Network Device"
    if ttl >= 128:
        return "Windows"
    if ttl >= 64:
        if "apple" in vendor:
            return "Apple (macOS/iOS)"
        for name in ANDROID_VENDORS:
            if name in vendor:
                return f"Android ({name.title()})"
        return "Linux / Unix"

    return "Unknown"


# Host Information

def get_mac(ip: str) -> Optional[dict]:
    """
    Read MAC from ARP table and look up vendor.
    FIX 5: MAC regex now captures all 6 octets (was only capturing 2).
    FIX A: Reuses global _mac_lookup instead of constructing per call.
    """
    try:
        if platform.system().lower() == "windows":
            output = subprocess.check_output(["arp", "-a", ip], text=True)
        else:
            output = subprocess.check_output(["arp", "-n", ip], text=True)

        # FIX 5: full 6-octet pattern
        match = re.search(
            r"(([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})",
            output,
            re.IGNORECASE,
        )
        if not match:
            return None

        mac = match.group(0).replace("-", ":").upper()

        try:
            with _mac_lookup_lock:
                vendor = _mac_lookup.lookup(mac)
        except Exception:
            vendor = "Unknown"

        return {"mac": mac, "vendor": vendor}

    except Exception:
        return None


def get_hostname(ip: str) -> Optional[str]:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


# Port Scanning

def scan_port(ip: str, port: int, timeout: float = 0.5) -> tuple[bool, str]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip, port))
        if result != 0:
            return False, ""

        banner = ""
        try:
            s.send(b"\r\n")
            banner = s.recv(1024).decode(errors="ignore").strip()
        except Exception:
            pass

        return True, banner
    except Exception:
        return False, ""
    finally:
        s.close()


#  Phase 1: Ping Sweep

def find_alive_hosts(network: str) -> list[tuple[str, Optional[int]]]:
    """
    Ping-sweep the entire subnet in parallel.
    Returns list of (ip, ttl) for alive hosts.
    """
    net = ipaddress.ip_network(network, strict=False)
    hosts = list(net.hosts())

    print(f"\n Step 1: Finding Alive Hosts in {network}...")
    print("=" * 60)

    alive: list[tuple[str, Optional[int]]] = []

    # FIX E: 150 workers is reasonable for /24 ICMP sweeps
    with ThreadPoolExecutor(max_workers=150) as executor:
        futures = {executor.submit(ping_host, str(ip)): str(ip) for ip in hosts}

        for future in as_completed(futures):
            ip = futures[future]
            try:
                is_alive, ttl = future.result()
            except Exception:
                continue

            if is_alive:
                alive.append((ip, ttl))
                print(f"  ✔  {ip} is UP  (TTL={ttl})")

    print("=" * 60)
    print(f"Found {len(alive)} alive hosts\n")
    return alive


# Phase 2: Deep Scan

def scan_alive_host(ip: str, ttl: Optional[int]) -> dict:
    mac_info = get_mac(ip)
    vendor = mac_info["vendor"] if mac_info else ""
    os_guess = guess_os(ttl, vendor)
    hostname = get_hostname(ip)

    open_ports: list[dict] = []

    # FIX F: parallel port scanning per host
    with ThreadPoolExecutor(max_workers=50) as executor:
        port_futures = {executor.submit(scan_port, ip, port, 0.8): port for port in TOP_100_PORTS}
        for future in as_completed(port_futures):
            port = port_futures[future]
            try:
                is_open, banner = future.result()
            except Exception:
                continue

            if is_open:
                open_ports.append({
                    "port": port,
                    "service": PORT_SERVICES.get(port, "Unknown"),
                    "banner": banner[:50] if banner else "",
                })

    open_ports.sort(key=lambda x: x["port"])

    return {
        "ip": ip,
        "hostname": hostname,
        "ttl": ttl,
        "os": os_guess,
        "mac": mac_info,
        "open_ports": open_ports,
        "port_count": len(open_ports),
    }


def scan_alive_hosts(alive_hosts: list[tuple[str, Optional[int]]]) -> list[dict]:
    """Run detailed scans on all alive hosts, up to 10 hosts in parallel."""
    print(f"Step 2: Scanning {len(alive_hosts)} alive host(s) for open ports...")
    print("=" * 60)

    # Load/refresh the vendor list once, single-threaded, before the worker
    # threads start hammering _mac_lookup concurrently.
    try:
        _mac_lookup.load_vendors()
    except Exception:
        pass

    results: list[dict] = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(scan_alive_host, ip, ttl): ip
            for ip, ttl in alive_hosts
        }

        for i, future in enumerate(as_completed(futures), 1):
            try:
                result = future.result()
            except Exception as exc:
                ip = futures[future]
                print(f"\n[{i}/{len(alive_hosts)}] {ip} — scan error: {exc}")
                continue

            results.append(result)
            mac_str = result["mac"]["mac"] if result["mac"] else "N/A"
            print(f"\n[{i}/{len(alive_hosts)}] Host: {result['ip']}")
            print(f"     OS       : {result['os']}")
            print(f"     MAC      : {mac_str}")
            print(f"     Hostname : {result['hostname'] or 'N/A'}")
            print(f"     Open Ports: {result['port_count']}")

    print("\n" + "=" * 60)
    return results


# Display

def display_detailed_results(results: list[dict]) -> None:
    if not results:
        print("No results to display.")
        return

    print("\n" + "=" * 80)
    print("DETAILED SCAN RESULTS — OPEN PORTS PER HOST")
    print("=" * 80)

    for i, host in enumerate(results, 1):
        mac_str = host["mac"]["mac"] if host["mac"] else "N/A"
        vendor_str = host["mac"]["vendor"] if host["mac"] else "N/A"

        # FIX I: closed all f-string parentheses properly
        print(f"\n┌─ HOST #{i}: {host['ip']}")
        print(f"│   Hostname  : {host['hostname'] or 'N/A'}")
        print(f"│   OS        : {host['os']}  (TTL={host['ttl']})")
        print(f"│   MAC       : {mac_str}  [{vendor_str}]")
        print(f"│   Open Ports: {host['port_count']}")
        print("│")

        if host["open_ports"]:
            print("│   OPEN PORTS:")
            print("│   " + "─" * 70)
            print("│   {:<8}  {:<20}  {:<40}".format("PORT", "SERVICE", "BANNER"))
            print("│   " + "─" * 70)

            for port_info in host["open_ports"]:
                port    = port_info["port"]
                service = port_info["service"]
                banner  = port_info["banner"][:38] if port_info["banner"] else ""
                print(f"│   {port:<8}  {service:<20}  {banner:<40}")
        else:
            print("│   No open ports detected.")

        print("└" + "─" * 78)


def display_statistics(results: list[dict]) -> None:
    """Print aggregate statistics across all scanned hosts."""
    if not results:
        return

    total_hosts  = len(results)
    total_ports  = sum(r["port_count"] for r in results)

    # FIX 7: use substring match — guess_os returns "Linux / Unix", "Android (Samsung)", etc.
    windows_count = sum(1 for r in results if "Windows"  in r["os"])
    linux_count   = sum(1 for r in results if "Linux"    in r["os"])
    android_count = sum(1 for r in results if "Android"  in r["os"])
    apple_count   = sum(1 for r in results if "Apple"    in r["os"])
    network_count = sum(1 for r in results if "Network"  in r["os"])

    port_counter: dict[int, int] = {}
    for r in results:
        for p in r["open_ports"]:
            port_counter[p["port"]] = port_counter.get(p["port"], 0) + 1

    print("\n" + "=" * 80)
    print("   SCAN STATISTICS")
    print("=" * 80)
    print(f"   Total Hosts Scanned  : {total_hosts}")
    print(f"   Total Open Ports     : {total_ports}")
    print(f"   Windows Systems      : {windows_count}")
    print(f"   Linux / Unix Systems : {linux_count}")
    print(f"   Android Devices      : {android_count}")
    print(f"   Apple Devices        : {apple_count}")
    print(f"   Network Devices      : {network_count}")

    if port_counter:
        print("\n   Most Common Open Ports:")
        top_ports = sorted(port_counter.items(), key=lambda x: x[1], reverse=True)[:10]
        for port, count in top_ports:
            service = PORT_SERVICES.get(port, "Unknown")
            print(f"     Port {port:>5}  ({service:<18})  found on {count} host(s)")


# Report Saving

def save_results(results: list[dict]) -> None:
    if not results:
        print("No results to save.")
        return

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # JSON
    json_file = f"scan_report_{timestamp}.json"
    with open(json_file, "w", encoding="utf-8") as jf:
        json.dump(results, jf, indent=4, default=str)

    # ── Detailed CSV (one row per open port) ──────────────────────────────────
    csv_file = f"scan_report_{timestamp}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as cf:
        writer = csv.writer(cf)
        writer.writerow(["IP", "Hostname", "OS", "TTL", "MAC", "Vendor",
                         "Total Ports", "Port", "Service", "Banner"])

        for r in results:
            mac_val    = r["mac"]["mac"]    if r["mac"] else ""
            vendor_val = r["mac"]["vendor"] if r["mac"] else ""

            if r["open_ports"]:
                for p in r["open_ports"]:
                    writer.writerow([
                        r["ip"], r["hostname"] or "", r["os"], r["ttl"],
                        mac_val, vendor_val, r["port_count"],
                        p["port"], p["service"], p["banner"],
                    ])
            else:
                writer.writerow([
                    r["ip"], r["hostname"] or "", r["os"], r["ttl"],
                    mac_val, vendor_val, 0, "", "", "",
                ])

    # Summary CSV (one row per host)
    summary_file = f"scan_summary_{timestamp}.csv"
    with open(summary_file, "w", newline="", encoding="utf-8") as cf:
        writer = csv.writer(cf)
        writer.writerow(["IP", "Hostname", "OS", "MAC", "Vendor",
                         "Open Ports Count", "Open Ports List"])

        for r in results:
            mac_val    = r["mac"]["mac"]    if r["mac"] else ""
            vendor_val = r["mac"]["vendor"] if r["mac"] else ""
            # FIX 6: p["port"] not p["ports"]
            ports_list = ", ".join(str(p["port"]) for p in r["open_ports"])
            writer.writerow([
                r["ip"], r["hostname"] or "", r["os"],
                mac_val, vendor_val, r["port_count"], ports_list,
            ])

    print("\n" + "=" * 80)
    print("   REPORTS SAVED")
    print("=" * 80)
    print(f"   JSON Report  : {json_file}")
    print(f"   Detailed CSV : {csv_file}")
    print(f"   Summary CSV  : {summary_file}")


# Orchestrator

def scan_subnet(network: str) -> list[dict]:
    """Two-phase scan: (1) ping sweep → (2) deep scan of alive hosts only."""
    alive_hosts = find_alive_hosts(network)

    if not alive_hosts:
        print("No alive hosts found.")
        return []

    results = scan_alive_hosts(alive_hosts)
    display_detailed_results(results)
    return results


# Entry Point

if __name__ == "__main__":
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "LAN NETWORK SCANNER - DETAILED PORT VIEW" + " " * 18 + "║")
    print("╚" + "═" * 78 + "╝")

    if len(sys.argv) < 2:
        print("\n Usage:")
        print("   python advanced_lan_scanner.py <network/prefix>")
        print("\n Examples:")
        print("   python advanced_lan_scanner.py 192.168.1.0/24")
        print("   python advanced_lan_scanner.py 10.0.0.0/24")
        sys.exit(1)

    network = sys.argv[1]
    start_time = time.time()

    results = scan_subnet(network)
    elapsed = time.time() - start_time

    if results:
        display_statistics(results)
        save_results(results)
        print("\n" + "=" * 80)
        print(f"   SCAN COMPLETED in {elapsed:.2f} seconds")
        print("=" * 80)
    else:
        print("\n   No hosts found or scan failed.")