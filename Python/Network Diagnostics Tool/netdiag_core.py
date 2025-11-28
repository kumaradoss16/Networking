"""
Core network diagnostics engine.
Provides functions used by CLI, GUI, Monitor, API, Reporter.
"""
from __future__ import annotations
import platform, subprocess, re, socket, json, shutil, time, asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging, ipaddress

try:
    import psutil
except Exception:
    psutil = None

try:
    import dns.resolver
except Exception:
    dns = None

try:
    import requests
except Exception:
    requests = None

LOG = logging.getLogger("netdiag_core")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def which(cmd: str):
    # Use shutil.which to search for 'cmd' in the system PATH
    # Returns full path to the command if found, otherwise None
    return shutil.which(cmd)

def run_cmd(cmd, timeout=30):
    # Define a function 'run_cmd' to execute a shell/CLI command.
    # 'cmd' is the command to run (as a list, e.g. ['ping', '8.8.8.8']).
    # 'timeout' is the maximum allowed time in seconds (default 30).
    try:
        p = subprocess.run(
            cmd,                       # The command list
            stdout=subprocess.PIPE,    # Capture standard output
            stderr=subprocess.PIPE,    # Capture standard error
            text=True,                 # Return output as string (not bytes)
            timeout=timeout            # Max seconds before forced kill
        )
        # Return tuple: (exit code, stdout, stderr), trimming whitespace.
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except subprocess.TimeoutExpired:
        # If command takes too long, indicate timeout occurred
        return -1, "", "timeout"
    except Exception as e:
        # For any other error, return error message as stderr
        return -1, "", str(e)
    
# Ping
def ping_host(host: str, count: int = 4, timeout: int=2) -> Dict[str, Any]:
    import ipaddress
    system = platform.system().lower()
    if system == "windows":
        try:
            ip = None
            try:
                ip = str(ipaddress.ip_address(host))
            except ValueError:
                ip = socket.gethostbyname(host)
            host_arg = ip
        except Exception:
            host_arg = host
        cmd = ["ping", "-n", str(count), "-w", str(timeout*1000), host_arg]
    else:
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
    rc, out, err = run_cmd(cmd, timeout=(count*timeout*5))
    res = {"host": host, "rc": rc, "raw": out or err}
    m = re.search(r"(\d+)% packet loss", out) or re.search(r"Lost = \d+ \((\d+)% loss\)", out)
    if m:
        res["loss"] = float(m.group(1))
    else:
        res["loss"] = None
        res["parse_error"] = "Could not parse packet loss"
        res["ping_output"] = out
    # Existing Linux-style regex first...
    m2 = re.search(r"min/avg/max(?:/mdev)? = ([\d\.]+)/([\d\.]+)/([\d\.]+)", out)
    if m2:
        res.update({"min":float(m2.group(1)), "avg":float(m2.group(2)), "max":float(m2.group(3))})
    else:
        # Windows-style: "Average = Xms"
        avg_match = re.search(r"Average = (\d+)ms", out)
        if avg_match:
            res["avg"] = float(avg_match.group(1))
        else:
            res["avg"] = None
    return res

# Traceroute
def traceroute(host: str, max_hops: int=30, timeout: int=2) -> Dict[str, Any]:
    import ipaddress
    system = platform.system().lower()

    try:
        ip = str(ipaddress.ip_address(host))
        host_arg = ip
    except ValueError:
        host_arg = host

    if system == "windows":
        cmd = ["tracert", "-d" ,"-h", str(max_hops), host_arg]
    else:
        if which("traceroute"):
            cmd = ["traceroute", "-n", "-w", str(timeout), "-m", str(max_hops), host_arg]
        elif which("tracepath"):
            cmd = ["tracepath", host_arg]
        else:
            return {"host": host, "error": "no traceroute available"}
    rc, out, err = run_cmd(cmd, timeout=60)
    return {"host": host, "raw": out or err}

async def _tcp_check(host: str, port: int, timeout: float=0.8):
    loop = asyncio.get_event_loop()
    try:
        fut = loop.create_connection(lambda: asyncio.Protocol(), host, port)
        conn = await asyncio.wait_for(fut, timeout=timeout)
        try:
            transport, proto = conn
            transport.close()
        except Exception:
            pass
        return port, True
    except Exception:
        return port, False
    
async def _port_scan_async(host: str, ports: List[int], concurrency: int=200, timeout :float=0.8):
    sem = asyncio.Semaphore(concurrency)
    results = {}
    async def worker(p):
        async with sem:
            port, ok = await _tcp_check(host, p, timeout)
            results[port] = ok
    await asyncio.gather(*[worker(p) for p in ports])
    return results

# Port Scan
def port_scan(host: str, ports: List[int], concurrency: int=200, timeout: float=0.8) -> Dict[int, bool]:
    try:
        return asyncio.run(_port_scan_async(host, ports, concurrency, timeout))
    except Exception:
        out = {}
        for p in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            try:
                s.connect((host, p)); out[p] = True
            except Exception:
                out[p] = False
            try:
                s.close()
            except:
                pass
        return out
    
# DNS Lookup
def dns_lookup(host: str) -> Dict[str, Any]:
    res = {"host": host, "addresses": []}
    try:
        if dns:
            a = dns.resolver.resolve(host, "A")
            res["addresses"] = [str(x) for x in a]
            try:
                mx = dns.resolver.resolve(host, "MX")
                res["mx"] = [str(m.exchange).rstrip(".") for m in mx]
            except Exception:
                pass
        else:
            ais = socket.getaddrinfo(host, None)
            res["addresses"] = list({ai[4][0] for ai in ais})
    except Exception as e:
        res["error"] = str(e)
    return res

# HTTP Check
def http_check(url: str, timeout: int=10) -> Dict[str, Any]:
    r = {"url": url}
    if requests:
        try:
            t0 = time.perf_counter()
            resp = requests.head(url, timeout=timeout, allow_redirects=True)
            r["status"] = resp.status_code
            r["headers"] = dict(resp.headers)
            r["latency_ms"] = (time.perf_counter() - t0) * 1000.0
        except Exception as e:
            r["error"] = str(e)
    else:
        r["error"] = "requests not installed"
    return r

# SSl Info
def ssl_info(hostname: str, port: int=443, timeout: int=5) -> Dict[str, Any]:
    import ssl
    r = {"host": hostname, "port": port}
    try: 
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                r["subject"] = cert.get("subject")
                r["issuer"] = cert.get("issuer")
                r["notBefore"] = cert.get("notBefore")
                r["notAfter"] = cert.get("notAfter")
    except Exception as e:
        r["error"] = str(e)
    return r

# Interfaces
def interfaces_info() -> Dict[str, Any]:
    if psutil:
        info = {}
        addrs = psutil.net_if_addrs(); stats = psutil.net_if_stats()
        for iface, adds in addrs.items():
            info[iface] = {
                "addresses": [{"family": str(a.family), "addr": a.address, "netmask": a.netmask} for a in adds],
                "isup": stats.get(iface).isup if stats.get(iface) else None
            }
        return info
    else:
        rc, out, err = run_cmd(["ip", "addr"] if which("ip") else ["ifconfig"])
        return {"raw": out or err}
    
# ARP Table
def arp_table() -> Dict[str, Any]:
    if platform.system().lower() == "windows":
        rc, out, err = run_cmd(["arp", "-a"])
        return {"raw": out or err}
    else:
        rc, out, err = run_cmd(["ip", "neigh"] if which("ip") else ["arp", "-n"])
        return {"raw": out or err}
    
# Check open ports
def open_connections() -> Any:
    if psutil:
        conns = psutil.net_connections(kind="inet")
        out = []
        for c in conns:
            out.append({
                "laddr": f"{c.laddr.ip}: {c.laddr.port}" if c.laddr else None,
                "raddr": f"{c.raddr.ip}: {c.raddr.port}" if c.raddr else None,
                "status": c.status, "pid": c.pid
            })
        return out
    rc, out, err = run_cmd(["ss", "-tunap"] if which("ss") else ["netstat", "-ant"])
    return {"raw": out or err}

# Speedtest
def speedtest() -> Dict[str, Any]:
    try:
        import speedtest
    except ImportError:
        return {"error": "speedtest-cli module is not installed", "install_hint": "pip install speedtest-cli"}
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        latency = st.results.server["latency"]
        server_name = st.results.server["name"]
        download = st.download() / 1e6
        upload = st.upload() / 1e6
        return {
            "download": round(download, 2),
            "upload": round(upload, 2),
            "latency": round(latency, 2),
            "server": server_name,
            "units": "Mbps, Mbps, ms",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return{"error": str(e)}
    

# Network Sweep (Multiple ping at a time)
def network_sweep(cidr: str, timeout: int = 1, workers: int = 50) -> Dict[str, Any]:
    """
    Perform a network sweep on a given CIDR range.
    
    Args:
        cidr: Network range in CIDR notation (e.g., '192.168.1.0/24', '10.0.0.0/16')
        timeout: Ping timeout in seconds (default: 1)
        workers: Number of concurrent workers (default: 50)
    
    Returns:
        Dictionary with sweep results including alive hosts
    """

    import concurrent.futures
    import ipaddress
    import platform

    result = {
        "cidr": cidr,
        "timeout": timeout,
        "workers": workers,
        "alive_hosts": [],
        "total_hosts": 0,
        "scanned": 0
    }

    try: 
        network = ipaddress.ip_network(cidr, strict=False)
        hosts = list(network.hosts())
        result["total_hosts"] = len(hosts)

        LOG.info(f"Starting network sweep on {cidr} ({len(hosts)} hosts)")

        # Quick ping fucntion for sweep
        def quick_ping(ip_str: str) -> tuple:
            system = platform.system().lower()

            if system == "windows":
                cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), ip_str]
            else:
                cmd = ["ping", "-c", "1", "-W", str(timeout), ip_str]

            rc, out, er = run_cmd(cmd, timeout=timeout + 2)

            is_alive = rc == 0 and ("ttl" in out.lower() or "TTL" in out)

            return ip_str, is_alive
        
        alive_count = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(quick_ping, str(ip)): str(ip) for ip in hosts}

            for future in concurrent.futures.as_completed(futures):
                result["scanned"] += 1
                ip, is_alive = future.result()

                if is_alive:
                    alive_count += 1
                    result["alive_hosts"].append(ip)
                    LOG.info(f"[ALIVE] {ip}")

        result["alive_count"] = alive_count
        result["success"] = True
        LOG.info(f"Sweep complete: {alive_count}/{len(hosts)} hosts alive")

    except ValueError as e:
        result["error"] = f"Invalid CIDR notation: {str(e)}"
        result["success"] = False
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
    return result

    
# PathPing
def pathping(host: str, max_hops: int = 30, queries: int = 100) -> Dict[str, Any]:
    """
    PathPing - Windows-style advanced network diagnostic tool.
    Combines traceroute with ping statistics for each hop.
    
    Args:
        host: Target hostname or IP
        max_hops: Maximum number of hops (default 30)
        queries: Number of queries per hop for statistics (default 100)
    
    Returns:
        Dictionary with pathping results including hop statistics
    """
    import ipaddress
    system = platform.system().lower()
    try:
        ip = str(ipaddress.ip_address(host))
        host_arg = ip
    except ValueError:
        try:
            ip = socket.gethostbyname(host)
            host_arg = ip
        except Exception:
            host_arg = host
    
    result = {
        "host": host,
        "resolved_ip": host_arg if host_arg != host else None,
        "max_hops": max_hops
    }

    if system == "windows":
        cmd = ["pathping", "-h", str(max_hops), "-n", "-q", str(queries), host_arg]
        timeout = (max_hops * 3) + (queries * 0.25) + 30

        rc, out, err = run_cmd(cmd, timeout=timeout)

        if rc == 0 or out:
            result["raw"] = out
            result["success"] = True

            hops = []
            lines = out.split("\n")

            # Find the statistics section
            stats_started = False
            for line in lines:
                line = line.strip()

                if "Computing statistics" in line or "statistics for" in line:
                    stats_started = True
                    continue

                if stats_started and line:
                    # Parse hop statistics line
                    # Format: "  0  hostname [IP]     Lost/Sent = X%   |   RTT: min/avg/max"
                    hop_match = re.search(
                        r'(\d+)\s+([^\[]+(?:\[[^\]]+\])?)\s+(\d+)/\s*(\d+)\s*=\s*(\d+)%',
                        line
                    )

                    if hop_match:
                        hop_num = int(hop_match.group(1))
                        hop_name = hop_match.group(2).strip()
                        lost = int(hop_match.group(3))
                        sent = int(hop_match.group(4))
                        loss_pct = int(hop_match.group(5))

                        hop_data = {
                            "hop": hop_num,
                            "address": hop_name,
                            "sent": sent,
                            "lost": lost,
                            "loss_percent": loss_pct
                        }

                        rtt_match = re.search(r'(\d+)ms/\s*(\d+)ms/\s*(\d+)ms', line)
                        if rtt_match:
                            hop_data["rtt_min"] = int(rtt_match.group(1))
                            hop_data["rtt_avg"] = int(rtt_match.group(2))
                            hop_data["rtt_max"] = int(rtt_match.group(3))

                        hops.append(hop_data)
            if hops:
                result["hops"] = hops
                result["total_hops"] = len(hops)
        else:
            result["error"] = err or "Pathping command failure"
            result["success"] = False
    else:
        # PathPing is Windows-only. Using enhanced traceroute simulation.
        result["note"] = "PathPing is Windows-only. Using enhanced traceroute simulation."

        tr_result = traceroute(host, max_hops=max_hops, timeout=2)

        if "error" in tr_result:
            result["error"] = tr_result["error"]
            result["success"] = False
            return result
        
        tr_lines = tr_result.get("raw", "").split("\n")
        hop_ips = []

        for line in tr_lines:
            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
            if ip_match:
                hop_ips.append(ip_match.group(1))

        hops = []
        queries_per_hop = min(10, queries // 10)

        for idx, hop_ip in enumerate(hop_ips[:max_hops], 1):
            hop_data = {
                "hop": idx,
                "address": hop_ip,
                "sent": queries_per_hop
            }

            ping_result = ping_host(hop_ip, count=queries_per_hop, timeout=2)

            if "error" not in ping_result:
                loss = ping_result.get("loss", 0)
                hop_data["loss_percent"] = loss
                hop_data["lost"] = int((loss / 100.0) * queries_per_hop)

                if "avg" in ping_result:
                    hop_data["rtt_avg"] = ping_result["avg"]
                if "min" in ping_result:
                    hop_data["rtt_min"] = ping_result["min"]
                if "max" in ping_result:
                    hop_data["rtt_max"] = ping_result["max"]
            else:
                hop_data["error"] = "Unreachable"
                hop_data["loss_percent"] = 100
                hop_data["lost"] = queries_per_hop

            hops.append(hop_data)

        result["hops"] = hops
        result["total_hops"] = len(hops)
        result["success"] = True
        result["raw"] = f"Enhanced traceroute with {queries_per_hop} ping per hop\n"
        result["raw"] += "\n".join([
            f"Hop {h['hop']:}: {h['address']} - Loss: {h.get('loss_percent', 'N/A')}%"
            for h in hops
        ])

    return result

# Route print
def route_print() -> Dict[str, Any]:
    """
    Display routing table (route print on Windows, route -n on Linux)
    
    Returns:
        Dictionary with routing table information
    """
    system = platform.system().lower()

    result = {
        "command": "",
        "raw": "",
        "parsed_routes": [],
        "success": False
    }
    
    if system == "windows":
        cmd = ["route", "print"]
        result["command"] = "route print"
    else:
        if which["ip"]:
            cmd = ["ip", "route"]
            result["command"] = "ip route"
        else:
            cmd = ["route", "-n"]
            result["command"] = "route -n"
    rc, out, err = run_cmd(cmd, timeout=10)

    if rc == 0 or out:
        result["raw"] = out
        result["success"] = True

        routes = []
        lines = out.split("\n")

        if system == "windows":
            in_active_routes = False
            for line in lines:
                line = line.split()

                if "Active Routes:" in line or "IPv4 Route Table" in line:
                    in_active_routes = True
                    continue

                if in_active_routes and line:
                    if "Network Destination" in line or "Netmask" in line or "====" in line:
                        continue

                    parts = line.split()
                    if len(parts) >= 5:
                        try:
                            route = {
                                "destination": parts[0],
                                "netmask": parts[1],
                                "gateway": parts[2],
                                "interface": parts[3],
                                "metric": parts[4]
                            }

                            routes.append(route)
                        except (IndexError, ValueError):
                            continue
                    # Stop at IPv6 section
                    if "IPv6 Route Table" in line or "Persistent Routes:" in line:
                        break
                else:
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith("Kernel") or line.startswith("Destination"):
                            if "via" in line or "dev" in line:
                                route_info = {"raw": line}
                                if line.startswith("default"):
                                    route_info["destination"] = "0.0.0.0/0"
                                else:
                                    dest_match = re.search(r'^(\S+)', line)
                                    if dest_match:
                                        route_info["destination"] = dest_match.group[1]

                                # Extract gateway
                                gateway_match = re.search(r"via\s+(\S+)", line)
                                if gateway_match:
                                    route_info["gateway"] = gateway_match.group(1)

                                # Extract interface
                                iface_match = re.search(r"dev\s+(\S+)", line)
                                if iface_match:
                                    route_info["interface"] = iface_match.group(1)

                                # Extract metric
                                metric_match = re.search(r"metric\s+(\d+)", line)
                                if metric_match:
                                    route_info["metric"] = metric_match.group(1)
                                routes.append(route_info)

                result["parsed_routes"] = routes
                result["total_routes"] = len(routes)
    else:
        result["error"] = err or "Failed to retrieve routing table"
        result["success"] = False
    return result


def run_all(host: str, options: Dict[str, Any], ports: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    Convenience runner. options keys: ping, traceroute, dns, http, ssl, interfaces, arp, conns, speed
    """
    # Start the report dictionary with target host and current time
    report = {"host": host, "time": datetime.utcnow().isoformat()}
    try:
        # Try to resolve the hostname to an IP address and save it
        ip = socket.gethostbyname(host)
        report["ip"] = ip
    except Exception as e:
        # If it fails, record the resolve error
        report["resolve_error"] = str(e)
        ip = host  # Fallback to provided host

    # Run ping if enabled in options
    if options.get("ping"):
        report["ping"] = ping_host(host)
    # Run traceroute if enabled in options
    if options.get("traceroute"):
        report["traceroute"] = traceroute(host)

    # Run pathping if enabled (NEW)
    if options.get("pathping"):
        report["pathping"] = pathping(host, max_hops=options.get("max_hops", 30))

    # Run other checks concurrently
    import concurrent.futures
    futures = {}
    # Use a thread pool to run multiple diagnostics in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        # DNS lookup
        if options.get("dns"):
            futures["dns"] = ex.submit(dns_lookup, host)
        # HTTP check (prepends http:// if host doesn't have a scheme)
        if options.get("http"):
            futures["http"] = ex.submit(http_check, ("http://" + host if not host.startswith("http") else host))
        # SSL/TLS certificate info
        if options.get("ssl"):
            futures["ssl"] = ex.submit(ssl_info, host)
        # Local network interfaces info
        if options.get("interfaces"):
            futures["interfaces"] = ex.submit(interfaces_info)
        # ARP table
        if options.get("arp"):
            futures["arp"] = ex.submit(arp_table)
        # Open network connections
        if options.get("conns"):
            futures["conns"] = ex.submit(open_connections)
        # Network speed test
        if options.get("speed"):
            futures["speed"] = ex.submit(speedtest)
        # ARP Table
        if options.get("arp"):
            futures["arp"] = ex.submit(arp_table)
        if options.get("interfaces"):
            futures["interfaces"] = ex.submit(interfaces_info)
        # Port scanning if a port list is supplied
        if ports:
            futures["ports"] = ex.submit(port_scan, host, ports)

        # Routing Table
        if options.get("route"):
            futures["route"] = ex.submit(route_print)
        # Collect the results as tasks finish (wait for each)
        for k, f in futures.items():
            try:
                report[k] = f.result()  # Save result in the report
            except Exception as e:
                # If something fails, record the error for this test
                report[k] = {"error": str(e)}
    # Return the complete report dictionary
    return report
