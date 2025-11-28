#!/usr/bin/env python3
import socket
import sys
from datetime import datetime

# Top 100 common TCP ports
TOP_100_PORTS = [
    20,21,22,23,25,53,67,68,69,80,110,111,123,135,137,138,139,143,161,389,
    443,445,514,587,631,636,873,902,989,990,993,995,1025,1026,1027,1028,
    1433,1434,1723,2049,2082,2083,2181,2375,2376,2484,2487,3050,3128,
    3306,3389,3690,4369,5000,5432,5555,5672,5900,5985,5986,6379,6443,
    6667,6881,7001,7002,7077,8000,8008,8080,8081,8123,8443,8888,9000,
    9001,9042,9092,9200,9300,9418,11211,27017,27018,27019,28017
]

def scan_port(ip, port, timeout=0.8):
    """Return True if port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python portscan100.py <target-ip>")
        sys.exit(1)

    target = sys.argv[1]
    print(f"\n🔎 Scanning top 100 ports on {target}")
    print("Start time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 50)

    for port in TOP_100_PORTS:
        if scan_port(target, port):
            print(f"OPEN   →  Port {port}")
        else:
            pass  # silent for closed ports

    print("-" * 50)
    print("Scan completed.")

if __name__ == "__main__":
    main()
