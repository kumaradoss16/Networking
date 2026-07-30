import ipaddress
import platform
import subprocess
import concurrent.futures
import re
import socket
from typing import List, Dict, Any, Optional
import time

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Retrieve MAC Address for an IP using ARP Table
def get_mac_address(ip: str) -> Optional[str]:
    system = platform.system().lower()

    try:
        if system == "windows":
            # Windows: arp -a ip
            cmd = ["arp", "-a", ip]
        else:
            # Linux: ip neigh show IP or arp -n IP
            cmd = ["ip", "neigh", "show", ip]
        # Run the OS Commands
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=2
        )

        output = result.stdout

        # Extract MAC address using regex
        # Matches: AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF
        mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'
        match = re.search(mac_pattern, output)

        if match:
            mac = match.group(0)
            mac = mac.replace('-', ':').upper()
            return mac
        return None

    except Exception:
        return None


# Retrieve hostname for an IP using reverse DNS lookup
def get_hostname(ip: str) -> Optional[str]:
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    # Host-related, address-related and timeout related error
    except (socket.herror, socket.gaierror, socket.timeout):
        return None


# Identify device vendor from MAC address using mac-vendor-lookup library
from mac_vendor_lookup import MacLookup

_mac_lookup = MacLookup()

def get_vendor_from_mac(mac: str) -> str:
    if not mac or len(mac) < 8:
        return "Unknown"
    try:
        return _mac_lookup.lookup(mac)
    except Exception:
        return "Unknown"

# Ping a single host and gather additional info.
def ping_single_host(ip: str, timeout: int = 1) -> Dict[str, Any]:
    system = platform.system().lower()

    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), ip]
    else:
        cmd = ["ping", "-c", "1", "-W", str(timeout), ip]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout * 2
        )

        output = result.stdout

        # Check for TTL in output (indicates successful ping)
        if system == "windows":
            # Extract TTL values
            ttl_match = re.search(r'TTL=(\d+)', output, re.IGNORECASE)
            ttl = int(ttl_match.group(1)) if ttl_match else None

            # Extract Response time
            time_match = re.search(r'time[=<](\d+)ms', output, re.IGNORECASE)
            rtt = int(time_match.group(1)) if time_match else None

            # Get MAC and hostname
            mac = get_mac_address(ip)
            hostname = get_hostname(ip)
            vendor = get_vendor_from_mac(mac) if mac else "Unknown"

            return {
                "ip": ip,
                "status": "up",
                "ttl": ttl,
                "rtt_ms": rtt,
                "mac": mac,
                "hostname": hostname,
                "vendor": vendor
            }
        else:
            if "ttl=" in output.lower():
                # Extract TTL values
                ttl_match = re.search(r'TTL=(\d+)', output, re.IGNORECASE)
                ttl = int(ttl_match.group(1)) if ttl_match else None

                # Extract Response time
                time_match = re.search(r'time[=<]([\d.]+)\s*ms', output, re.IGNORECASE)
                rtt = int(time_match.group(1)) if time_match else None

                # Get MAC and hostname
                mac = get_mac_address(ip)
                hostname = get_hostname(ip)
                vendor = get_vendor_from_mac(mac) if mac else "Unknown"

                return {
                    "ip": ip,
                    "status": "up",
                    "ttl": ttl,
                    "rtt_ms": rtt,
                    "mac": mac,
                    "hostname": hostname,
                    "vendor": vendor
                }
            return {"ip": ip, "status": "down"}
    except subprocess.TimeoutExpired:
        return {"ip": ip, "status": "timeout"}
    except Exception as e:
        return {"ip": ip, "status": "error", "error": str(e)}


# Sweep a network subnet to discover active hosts
def network_sweep(network: str, timeout: int = 1, max_workers: int = 50) -> Dict[str, Any]:
    try:
        # Parse the network
        net = ipaddress.ip_network(network, strict=False)
        # Generate the list of hosts (exclude network and broadcast address)
        hosts = [str(ip) for ip in net.hosts()]

        if not hosts:
            hosts = [str(net.network_address)]

        result = {
            "network": str(net),
            "total_hosts": len(hosts),
            "scanned": 0,
            "up": 0,
            "down": 0,
            "active_hosts": [],
            "all_results": [],
            "start_time": time.time()
        }

        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}Network Sweep Tool{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")
        print(f"{Colors.OKCYAN}Scanning network: {Colors.BOLD}{net}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Total hosts to scan: {Colors.BOLD}{len(hosts)}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Using {Colors.BOLD}{max_workers}{Colors.ENDC}{Colors.OKCYAN} concurrent workers{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'-' * 80}{Colors.ENDC}\n")

        # Perform concurrent ping sweep
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all ping tasks
            future_to_ip = {executor.submit(ping_single_host, ip, timeout): ip for ip in hosts}

            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    ping_result = future.result()   # Retrieves the actual return value from ping_single_host()
                    result["scanned"] += 1   #
                    result["all_results"].append(ping_result)   # Stores every host whether up or down

                    if ping_result["status"] == "up":
                        result["up"] += 1
                        result["active_hosts"].append(ping_result)   # Stores Only online hosts

                        # Print active host immediately with colors
                        ttl = ping_result.get("ttl", "?")
                        rtt = ping_result.get("rtt_ms", "?")
                        mac = ping_result.get("mac", "N/A")
                        hostname = ping_result.get("hostname", "N/A")
                        vendor = ping_result.get("vendor", "Unknown")

                        print(f"{Colors.OKGREEN}[✓] {ip:15}{Colors.ENDC} - "
                              f"{Colors.BOLD}UP{Colors.ENDC} | "
                              f"TTL={Colors.WARNING}{ttl}{Colors.ENDC} | "
                              f"RTT={Colors.OKCYAN}{str(rtt) + 'ms' if rtt is not None else 'N/A'}{Colors.ENDC} | "
                              f"MAC={Colors.OKBLUE}{mac}{Colors.ENDC} | "
                              f"Name={Colors.HEADER}{hostname}{Colors.ENDC} | "
                              f"Vendor={Colors.WARNING}{vendor}{Colors.ENDC}")
                    else:
                        result["down"] += 1

                    # Progress indicator every 25 hosts
                    if result["scanned"] % 25 == 0:
                        progress = (result["scanned"] / len(hosts)) * 100

                        print(f"{Colors.OKCYAN}Progress: {result['scanned']}/{len(hosts)} ({progress:.1f}%){Colors.ENDC}")
                except Exception as e:
                    result["down"] += 1
                    print(f"{Colors.FAIL}[!] Error Scanning {ip}: {str(e)}{Colors.ENDC}")

        result["end_time"] = time.time()
        result["duration_seconds"] = round(result["end_time"] - result["start_time"], 2)

        # Sort active hosts by IP
        result["active_hosts"].sort(key=lambda x: ipaddress.ip_address(x["ip"]))
        return result

    except ValueError as e:
        return {"error": f"Invalid network format: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}


# Automatically detect the local network subnet.
def auto_detect_local_network() -> Optional[str]:
    try:
        # Get local IP address
        # Create a IPv4 UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))   # Choose Ethernet OS decides which interface can reach 8.8.8.8
        local_ip = s.getsockname()[0]
        s.close()

        # Assume /24 network
        network = ipaddress.ip_network(f"{local_ip}/24", strict=False)
        return str(network)
    except Exception:
        return None


# Guess device type based on TTL value.
def identify_device_type(ttl: int) -> str:
    if ttl is None:
        return "Unknown"
    elif ttl <= 64:
        return "Linux/Unix"
    elif ttl <= 128:
        return "Windows"
    elif ttl <= 255:
        return "Network Device"
    else:
        return "Unknown"


# CLI interface for standalone use
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Network Sweep Tool (Enhanced)")
    # python network_sweep.py 192.168.1.0/24
    parser.add_argument(
        "network",
        nargs="?",   # 0 or 1
        help="Network to scan in CIDR notation (e.g., 192.168.1.0/24). If Not provided, auto-detects local network."
    )
    # python network_sweep.py --timeout 2
    parser.add_argument(
        "--timeout",
        type=int,
        default=1,
        help="Ping timeout in seconds (default: 1)"
    )
    # python network_sweep.py --workers 100
    parser.add_argument(
        "--workers",
        type=int,
        default=50,
        help="Number of concurrent workers (default: 50)"
    )
    # python network_sweep.py --json
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )
    # python network_sweep.py 192.168.1.0/24 --timeout 2 --workers 100 --json
    """
    args = Namespace(
        network="192.168.1.0/24",
        timeout=2,
        workers=100,
        json=True
        )
    """
    args = parser.parse_args()

    # Auto-detect network if not provided
    if not args.network:
        print(f"{Colors.WARNING}No network specified. Auto-detecting local network...{Colors.ENDC}")
        args.network = auto_detect_local_network()   # 192.168.1.0/24
        if not args.network:
            print(f"{Colors.FAIL}Error: Could not auto-detect network. Please specify manually.{Colors.ENDC}")
            exit(1)
        print(f"{Colors.OKGREEN}Detected network: {Colors.BOLD}{args.network}{Colors.ENDC}\n")

    # Perform sweep
    start = time.time()
    results = network_sweep(args.network, timeout=args.timeout, max_workers=args.workers)

    if "error" in results:
        print(f"{Colors.FAIL}Error: {results['error']}{Colors.ENDC}")
        exit(1)

    # Display results
    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}NETWORK SWEEP SUMMARY{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Network: {Colors.BOLD}{results['network']}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Total hosts scanned: {Colors.BOLD}{results['total_hosts']}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Active hosts: {Colors.BOLD}{results['up']}{Colors.ENDC}")
        print(f"{Colors.FAIL}Inactive hosts: {Colors.BOLD}{results['down']}{Colors.ENDC}")
        print(f"{Colors.WARNING}Duration: {Colors.BOLD}{results['duration_seconds']} seconds{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

        if results['active_hosts']:
            print(f"{Colors.OKGREEN}{Colors.BOLD}ACTIVE HOSTS{Colors.ENDC}")
            print(f"{Colors.OKBLUE}{'-' * 120}{Colors.ENDC}")
            print(f"{Colors.BOLD}{'IP Address':<18} {'TTL':<6} {'RTT':<10} {'MAC Address  ':<25} {'Hostname':<25} {'Vendor':<20}{Colors.ENDC}")
            print(f"{Colors.OKBLUE}{'-' * 120}{Colors.ENDC}")

            for host in results['active_hosts']:
                # Safely extract values with defaults
                ip = host.get('ip', 'N/A')
                ttl = host.get('ttl')
                rtt = host.get('rtt_ms')
                mac = host.get('mac')
                hostname = host.get('hostname')
                vendor = host.get('vendor')

                # Convert all to strings, handling None values
                ttl_str = str(ttl) if ttl is not None else 'N/A'
                rtt_str = str(rtt) if rtt is not None else 'N/A'
                mac_str = str(mac) if mac is not None else 'N/A'
                hostname_str = str(hostname) if hostname is not None else 'N/A'
                vendor_str = str(vendor) if vendor is not None else 'Unknown'

                # Truncate long hostnames
                if len(hostname_str) > 24:
                    hostname_str = hostname_str[:21] + "..."

                # Print with safe string formatting
                print(f"{Colors.OKGREEN}{ip:<18}{Colors.ENDC} "
                      f"{Colors.WARNING}{ttl_str:<6}{Colors.ENDC} "
                      f"{Colors.OKCYAN}{rtt_str:<10}{Colors.ENDC} "
                      f"{Colors.OKBLUE}{mac_str:<20}{Colors.ENDC} "
                      f"{Colors.HEADER}{hostname_str:<25}{Colors.ENDC} "
                      f"{Colors.WARNING}{vendor_str:<20}{Colors.ENDC}")
            print(f"{Colors.OKBLUE}{'-' * 120}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}No active hosts found.{Colors.ENDC}")