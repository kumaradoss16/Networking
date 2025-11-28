import argparse, json
from netdiag_core import run_all, port_scan
from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
console = Console()

def parse_ports(s: str) -> List[int]:
    if not s: return []
    ports = s.split(","); out = set()
    for p in ports:
        p = p.strip()
        if "-" in p:
            a, b = p.split("-", 1); out.update(range(int(a), int(b)+1))
        else:
            out.add(int(p))
    return sorted(out)


def main():
    p = argparse.ArgumentParser(description="NetDiag CLI")
    p.add_argument("--host", help="Target host or P address")
    p.add_argument("--ping", action="store_true", help="Run ping test")
    p.add_argument("--sweep", help="Network sweep (CIDR notation, e.g., 192.168.1.0/24, 10.0.0.0/16)")
    p.add_argument("--sweep-timeout", type=int, default=1, help="Ping timeout for sweep (default: 1s)")
    p.add_argument("--sweep-workers", type=int, default=50, help="Concurrent workers for sweep (default: 50)")
    p.add_argument("--traceroute", action="store_true", help="Run traceroute")
    p.add_argument("--dns", action="store_true", help="Perform DNS lookup")
    p.add_argument("--http", action="store_true", help="Check HTTP connectivity")
    p.add_argument("--arp", action="store_true", help="Show ARP table")
    p.add_argument("--ssl", action="store_true", help="Check SSL/TLS certificate")
    p.add_argument("--ports", help="Port scan (e.g., 22,80,443,8000-8100)")
    p.add_argument("--speed", action="store_true", help="Run speedtest")
    p.add_argument("--interfaces", action="store_true", help="Show local network interfaces")
    p.add_argument("--conns", action="store_true", help="Show open connections")
    p.add_argument("--pathping", action="store_true", help="Run pathping (advanced route diagnostics)")
    p.add_argument("--route", action="store_true", help="Show routing table (route print)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.add_argument("--report", help="Save report to JSON file")
    args = p.parse_args()
    ports = parse_ports(args.ports) if args.ports else None
    opts = {
        "ping": args.ping,
        "traceroute": args.traceroute,
        "dns": args.dns,
        "http": args.http,
        "ssl": args.ssl,
        "speed": args.speed,
        "interfaces": args.interfaces,
        "arp": args.arp,
        "conns": args.conns,
        "pathping": args.pathping,
        "route": args.route
    }

    report = run_all(args.host, opts, ports)
    # Handle network sweep separately
    if args.sweep:
        from netdiag_core import network_sweep
        
        console.print(f"\n[bold cyan]🔍 NETWORK SWEEP: {args.sweep}[/bold cyan]")
        console.print("[dim]" + "─" * 60 + "[/dim]\n")
        
        sweep_result = network_sweep(
            args.sweep, 
            timeout=args.sweep_timeout, 
            workers=args.sweep_workers
        )
        
        if args.json or args.report:
            s = json.dumps(sweep_result, indent=2)
            if args.report:
                with open(args.report, "w") as f:
                    f.write(s)
                console.print(f"[green]✓[/green] Sweep report saved to: [bold]{args.report}[/bold]")
            else:
                print(s)
        else:
            # Pretty output for sweep
            if "error" in sweep_result:
                console.print(f"[red]✗ Error: {sweep_result['error']}[/red]\n")
            elif sweep_result.get("success"):
                total = sweep_result.get("total_hosts", 0)
                alive = sweep_result.get("alive_count", 0)
                
                console.print(f"[bold]Target:[/bold] [white]{sweep_result['cidr']}[/white]")
                console.print(f"[bold]Total Hosts:[/bold] [white]{total}[/white]")
                console.print(f"[bold]Alive Hosts:[/bold] [green]{alive}[/green] ({(alive/total*100) if total else 0:.1f}%)")
                console.print(f"[bold]Timeout:[/bold] [dim]{sweep_result['timeout']}s[/dim]")
                console.print(f"[bold]Workers:[/bold] [dim]{sweep_result['workers']}[/dim]\n")
                
                if sweep_result["alive_hosts"]:
                    console.print("[bold cyan]Alive Hosts:[/bold cyan]")
                    table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE)
                    table.add_column("#", style="dim", width=5)
                    table.add_column("IP Address", style="green", width=18)
                    
                    for idx, ip in enumerate(sweep_result["alive_hosts"], 1):
                        table.add_row(str(idx), ip)
                    
                    console.print(table)
                else:
                    console.print("[yellow]⚠ No alive hosts found[/yellow]")
            
            console.print("[bold cyan]═" * 30 + "[/bold cyan]")
            console.print("[bold cyan] Sweep Complete [/bold cyan]")
            console.print("[bold cyan]═" * 30 + "[/bold cyan]\n")
        
        return  # Exit after sweep
    
    # Require --host if not doing sweep
    if not args.host:
        console.print("[red]Error: --host is required (or use --sweep for network discovery)[/red]")
        p.print_help()
        return

    
    if args.json or args.report:
        s = json.dumps(report, indent=2)
        if args.report:
            with open(args.report, "w") as f:
                f.write(s)
            console.print(f"[green]✓[/green] Report saved to: [bold]{args.report}[/bold]")
        else:
            print(s)
    else:
        host_panel = Panel(
            f"[bold]Host:[/bold] {report.get('host', 'N/A')}\n"
            f"[bold]IP Address:[/bold] {report.get('ip', 'N/A')}\n"
            f"[bold]Timestamp:[/bold] {report.get('time', 'N/A')}",
            title="[bold cyan]Target Information[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        )
        console.print(host_panel)
        console.print()

        # Ping results
        if report.get("ping"):
            console.print("[bold cyan]🔵 PING TEST[/bold cyan]")
            console.print("[dim]" + "-" * 60 + "[/dim]")
            p = report["ping"]
            if "error" in p:
                console.print(f"   [red]x ERROR: {p['error']}[/red]")
            else:
                loss = p.get("loss", "N/A")
                avg = p.get("avg", "N/A")
                min_rtt = p.get("min", "N/A")
                max_rtt = p.get("max", "N/A")

                if loss == 0.0:
                    status_color = "green"
                    status_icon = "✓"
                elif loss < 50:
                    status_color = "yellow"
                    status_icon = "⚠"
                else:
                    status_color = "red"
                    status_icon = "x"
                
                console.print(f"   [{status_color}]{status_icon} Status: {'Reachable' if loss < 100 else 'Unreachable'}[/{status_color}]")
                console.print(f"   Packet Loss: [{status_color}]{loss}%[/{status_color}]")
                console.print(f"   Average RTT: [cyan]{avg} ms[/cyan]")
                if min_rtt != "N/A" and max_rtt != "N/A":
                    console.print(f"   RTT Range: [dim]{min_rtt} - {max_rtt} ms[/dim]")
            console.print()

        # Pathping
        if report.get("pathping"):
            console.print("[bold cyan] 🛣️  PATHPING (Advanced Route Diagnostics)[/bold cyan]")
            console.print("[dim]" + "-" * 60 + "[/dim]")
            pp = report["pathping"]

            if "error" in pp:
                console.print(f"    [red]✗ Error: {pp['error']}[/red]")
            elif pp.get("success"):
                console.print(f"   [green]✓[/green] Analysis Complete")
                console.print(f"   Target: [white]{pp.get('host')}[/white]")

                if "resolved_ip" in pp and pp["resolved_ip"]:
                    console.print(f"   Resolved IP: [cyan]{pp['resolved_ip']}[/cyan]")

                console.print(f"   Total Hops: [white]{pp.get('total_hops', 'N/A')}[/white]\n")

                if "hops" in pp and pp["hops"]:
                    console.print("   [bold]Hop Statistics:[/bold]")

                    table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE)
                    table.add_column("Hop", style="white", width=5)
                    table.add_column("Address", style="cyan", width=18)
                    table.add_column("Loss %", style="yellow", width=8)
                    table.add_column("Sent", style="dim", width=6)
                    table.add_column("Lost", style="dim", width=6)
                    table.add_column("RTT (ms)", style="green", width=15)

                    for hop in pp["hops"]:
                        hop_num = str(hop.get("hop", "?"))
                        address = hop.get("address", "N/A")[:18]
                        loss_pct = hop.get("loss_percent", "N/A")
                        sent = str(hop.get("sent", "N/A"))
                        lost = str(hop.get("lost", "N/A"))

                        if "rtt_avg" in hop:
                            rtt_min = hop.get("rtt_min", "?")
                            rtt_avg = hop.get("rtt_avg", "?")
                            rtt_max = hop.get("rtt_max", "?")
                            rtt_str = f"{rtt_min} / {rtt_avg} / {rtt_max}"
                        else:
                            rtt_str = "N/A"

                        if isinstance(loss_pct, (int, float)):
                            if loss_pct == 0:
                                loss_color = "green"
                            elif loss_pct < 10:
                                loss_color = "yellow"
                            else:
                                loss_color = "red"
                            loss_display = f"[{loss_color}]{loss_pct}%[/{loss_color}]"
                        else:
                            loss_display = str(loss_pct)
                        table.add_row(hop_num, address, loss_display, sent, lost, rtt_str)

                    console.print(table)
                    if "note" in pp:
                        console.print(f"\n   [dim]Note: {pp['note']}[/dim]")
                if "raw" in pp and len(pp["raw"]) < 2000:
                    console.print("\n   [bold]Raw Output:[/bold]")
                    console.print(f"   [dim]{pp['raw'][:500]}[/dim]")
            console.print("\n")
        
        #DNS
        if report.get("dns"):
            console.print("[bold cyan]🌐 DNS LOOKUP[/bold cyan]")
            console.print("[dim]" + "-" * 60 + "[/dim]")
            dns = report["dns"]
            if "error" in dns:
                console.print(f"   [red]x ERROR: {dns['error']}[/red]")
            else:
                addresses = dns.get("addresses", [])
                if addresses:
                    console.print(f"   [green]✓[/green] IP Addresses:")
                    for idx, addr in enumerate(addresses, 1):
                        console.print(f"   {idx}. [white]{addr}[/white]")
                else:
                    console.print("   [yellow]⚠ No addresses found[/yellow]")
                
                if "mx" in dns and dns["mx"]:
                    console.print(f"\n  [green]✓[/green] MX Records:")
                    for idx, mx in enumerate(dns["mx"], 1):
                        console.print(f"   {idx}. [white]{mx}[/white]")
            console.print()

        #HTTP
        if report.get("http"):
            console.print("[bold cyan]📡 HTTP CHECK[/bold cyan]")
            console.print("[dim]" + "-" * 60 + "[/dim]")
            http = report["http"]
            if "error" in http:
                console.print(f"[red]x ERROR: {http['error']}[/red]")
            else:
                status = http.get("status", "N/A")
                latency = http.get("latency_ms", "N/A")

                if status < 300:
                    status_color = "green"
                    status_icon = "✓"
                elif status < 400:
                    status_color = "yellow"
                    status_icon = "↻"
                else:
                    status_color = "red"
                    status_icon = "x"
                console.print(f"   [{status_color}]{status_icon} Status Code: {status}[/{status_color}]")
                if isinstance(latency, (int, float)):
                    console.print(f"   Response Time: [cyan]{latency: .2f} ms[/cyan]")

                headers = http.get("headers", {})
                if headers:
                    console.print(f"\n   [bold]Key Headers:[/bold]")
                    important_headers = ["Server", "Content-Type", "Content-Length"]
                    for h in important_headers:
                        if h in headers:
                            console.print(f"   {h}: [dim]{headers[h]}[/dim]")
            console.print()
                   
        # SSL
        if report.get("ssl"):
            console.print("[bold cyan]🔒 SSL/TLS CERTIFICATE[/bold cyan]")
            console.print("[dim]" + "-" * 60 + "[/dim]")
            ssl = report["ssl"]
            if "error" in ssl:
                console.print(f"  [red]✗ Error: {ssl['error']}[/red]")
            else:
                console.print(f"   [green]✓[/green] Certificate Found")
                subject = ssl.get("subject", "N/A")
                if subject != "N/A" and isinstance(subject, tuple):
                    for item in subject:
                        for key, value in item:
                            if key == "commonName":
                                console.print(f"   Common Name: [white]{value}[/white]")
                issuer = ssl.get("issuer", "N/A")
                if issuer != "N/A" and isinstance(issuer, tuple):
                    for item in subject:
                        for key, value in item:
                            if key == "oragnizationsName":
                                console.print(f"   Issuere: [white]{value}[/white]")
                not_before = ssl.get("notBefore", "N/A")
                not_after = ssl.get("notAfter", "N/A")
                console.print(f"   Valid From: [dim]{not_before}[/dim]")
                console.print(f"   Valid Until: [cyan]{not_after}[/cyan]")
            console.print("\n")

        # Speedtest
        if report.get("speed"):
            console.print("[bold cyan]⚡ INTERNET SPEED TEST[/bold cyan]")
            console.print("[dim]" + "-" * 60 + "[/dim]")
            s = report["speed"]
            if "error" in s:
                console.print(f"  [red]✗ Error: {s['error']}[/red]")
                if "install_hint" in s:
                    console.print(f"   yellow]💡 Hint: {s['install_hint']}[/yellow]")
            else:
                download = s.get("download", "N/A")
                upload = s.get("upload", "N/A")
                latency = s.get("latency", "N/A")
                server = s.get("server", "N/A")
                console.print(f"   [green]✓[/green] Speed Test Complete")
                console.print(f"   Download: [bold green]{download} Mbps[/bold green]")
                console.print(f"   Upload: [bold blue]{download} Mbps[/bold blue]")
                console.print(f"   Latency: [cyan]{latency} ms[/cyan]")
                console.print(f"   Server: [dim]{server}[/dim]")
            console.print("\n")
        
        # Port Scan
        if report.get("ports"):
            console.print("[bold cyan] 🔍 PORT SCAN RESULTS[/bold cyan]")
            console.print("[dim]" + "-" * 60 + "[/dim]")
            ports_data = report["ports"]
            if "error" in ports:
                console.print(f"   [red]✗ Error: {ports_data['error']}[/red]")
            else:
                open_ports = [p for p, state in ports_data.items() if state]
                closed_ports = [p for p, state in ports_data.items() if not state]

                console.print(f"   Total Ports Scanned: [white]{len(ports_data)}[/white]")
                console.print(f"   [green]Open:[/green] {len(open_ports)}")
                console.print(f"   [red]Closed/Filtered:[/red] {len(closed_ports)}\n")

                if open_ports:
                    console.print("    [bold]Open Ports:[/bold]")

                    table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE)
                    table.add_column("Port", style="green", width=10)
                    table.add_column("State", style="green", width=12)
                    table.add_column("Common Service", style="dim")

                    common_services = {
                        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
                        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
                        443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
                        5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Alt",
                        8443: "HTTPS-Alt", 27017: "MongoDB"
                    }
                    for port in sorted(open_ports)[:20]:  # Show first 20
                        service = common_services.get(int(port), "Unknown")
                        table.add_row(str(port), "OPEN", service)
                    console.print(table)

                    if len(open_ports) > 20:
                        console.print(f"   [dim]... and {len(open_ports) - 20} more open ports[/dim]")
            console.print("\n")

        # Traceroute
        if report.get("traceroute"):
            console.print("[bold cyan]🗺️  TRACEROUTE[/bold cyan]")
            console.print("[dim]" + "-" * 60 + "[/dim]")
            tr = report["traceroute"]

            if "error" in tr:
                console.print(f"   [red]✗ Error: {tr['error']}[/red]")
            else:
                raw = tr.get("raw", "N/A")
                lines = raw.split("/n")

                for line in lines[:25]:
                    if line.strip():
                        console.print(f"[dim]{line}[/dim]")
                
                if len(lines) > 25:
                    console.print(f"   [dim]... ({len(lines) - 25} more hops)[/dim]")
            console.print("\n")

        # Open Connections
        if report.get("conns"):
            console.print("[bold cyan]🔗 OPEN CONNECTIONS[/bold cyan]")
            console.print("[dim]" + "─" * 60 + "[/dim]")
            conns = report["conns"]
            
            if "error" in conns:
                console.print(f"  [red]✗ Error: {conns['error']}[/red]")
            elif isinstance(conns, list):
                console.print(f"  Total Connections: [white]{len(conns)}[/white]\n")
                
                # Show first 15 connections
                if conns:
                    table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE)
                    table.add_column("Local Address", style="cyan", width=22)
                    table.add_column("Remote Address", style="yellow", width=22)
                    table.add_column("Status", style="green", width=12)
                    table.add_column("PID", style="dim", width=8)
                    
                    for conn in conns[:15]:
                        laddr = conn.get("laddr", "N/A")
                        raddr = conn.get("raddr", "N/A")
                        status = conn.get("status", "N/A")
                        pid = str(conn.get("pid", "N/A"))
                        table.add_row(laddr, raddr, status, pid)
                    
                    console.print(table)
                    
                    if len(conns) > 15:
                        console.print(f"  [dim]... and {len(conns) - 15} more connections[/dim]")
                else:
                    console.print("  [yellow]No connections found[/yellow]")
            elif "raw" in conns:
                console.print(f"  [dim]{conns['raw'][:500]}[/dim]")
            console.print()

        # ARP
        if report.get("arp"):
            arp = report["arp"]
            if "error" in arp:
                console.print(f"\n[bold red]❌ ARP Table Error:[/bold red] {arp['error']}")
            elif "entries" in arp:
                entries = arp["entries"]
                if entries:
                    console.print(f"\n[bold cyan] ARP Table ({arp.get('count', len(entries))} enries):[/bold cyan]")
                    console.print("[dim]" + "-" * 70 + "[/dim]")
                    console.print(f"{'IP Address': <18} {'Mac Address': <20} {'Interface': <12} {'State': <10}")
                    console.print("[dim]" + "-" * 70 + "[/dim]")
                    for entry in entries:
                        ip = entry.get('ip', 'N/A')
                        mac = entry.get('mac', 'N/A')
                        iface = entry.get('iface', 'N/A')
                        state = entry.get('state', entry.get('type', 'N/A'))
                        console.print(f"[yellow]{ip:<18}[/yellow] [cyan]{mac:<20}[/cyan] [green]{iface:<12}[/green] [dim]{state:<10}[/dim]")
                else:
                   console.print("[red]ARP Table: No entries found (cache may be empty)[/red]")
            elif "raw" in arp:
                console.print(f"\n[bold cyan]ARP Table (raw output):[/bold cyan]")
                console.print("[dim]" + "-" * 60 + "[/dim]")
                console.print(f"[dim]{arp['raw']}[/dim]")
            console.print("\n")
        
        # Interfaces
        if report.get("interfaces"):
            iface = report["interfaces"]
            if "error" in iface:
                console.print(f"Interfaces: [red]{iface['error']}[/red]")
            elif "raw" in iface:
                console.print(f"\n[bold cyan] Network Interfaces [/ bold cyan]")
                console.print(f"[dim]{iface['raw'][:1000]}[/dim]")
            else:
                console.print("[bold cyan]Network Interfaces:[/ bold cyan]")
                console.print("[dim]" + "-" * 80 + "[/dim]")
                for name, fields in iface.items():
                    is_up = fields.get("isup", False)
                    status_icon = "🟢" if is_up else "🔴"
                    status_text = "[green]UP[/green]" if is_up else "[red]DOWN[/red]"
                    console.print(f"\n{status_icon} [bold yellow]{name}[/bold yellow] - {status_text}")

                    addresses = fields.get("addresses", [])
                    if addresses:
                        console.print("   [bold]Addresses:[/bold]")
                        for idx, addr in enumerate(addresses, 1):
                            if isinstance(addr, dict):
                                family = addr.get("family", "N/A")
                                ip = addr.get("addr", "N/A")
                                netmask = addr.get("netmask", "N/A")

                                if "AF_INET" in str(family) and "AF_INET6" not in str(family):
                                    console.print(f"   {idx}. [cyan]IPv4:[/cyan] [white]{ip}[/white] [dim]Netmask[/dim]")
                                elif "AF_INET6":
                                    console.print(f"   {idx}. [magenta]IPv6:[/magenta] [white]{ip}[/white]")
                                elif "AF_LINK" in str(family) or "AF_PACKET" in str(family):
                                    console.print(f"   {idx}. [blue]IPv6:[/blue] [white]{ip}[/white]")
                                else:
                                    console.print(f"   {idx}. [dim]{family}:[/dim] [white]{ip}[/white]")
                    else:
                        console.print("   [dim]No Addresses assigned[/dim]")
                console.print("\n[dim]" + "-" * 80 + "[/dim]")
            console.print("\n")

            # Routing Table
            if report.get("route"):
                console.print("[bold cyan]🛣️   ROUTING TABLE[/bold cyan]")
                console.print("[dim]" + "-" * 60 + "[/dim]")

                route_data = report["route"]

                if "error" in route_data:
                    console.print(f"   [red]✗ Error: {route_data['error']}[/red]")

                elif route_data.get("success"):
                    total = route_data.get("total_routes", 0)
                    console.print(f"   [green]✓[/green] Routing table retrieved")
                    console.print(f"   Command: [dim]{route_data.get('command', 'N/A')}[/dim]")
                    console.print(f"   Total Routes: [white]{total}[/white]\n")
                    
                    if route_data.get("parsed_routes"):
                        console.print("   [bold]Active Routes:[/bold]")

                        table = Table(show_header=True, header_style="bold cyan", box=box.SIMPLE)
                        table.add_column("Destination", style="green", width=18)
                        table.add_column("Gateway", style="green", width=18)
                        table.add_column("Interface", style="yellow", width=18)
                        table.add_column("Metric", style="dim", width=18)

                        # Show first 20
                        for route in route_data["parese_routes"][:-1]:
                            dest = route.get("destination", "N/A")
                            gateway = route.get("gateway", "N/A")
                            iface = route.get("interface", "N/A")
                            metric = route.get("metric", "N/A")

                            # Truncate long values
                            if len(dest) > 17:
                                dest = dest[::] 
                            if len(gateway) > 17:
                                gateway = gateway[::]
                            if len(iface) > 17:
                                iface = iface[::] 

                            table.add_row(dest, gateway, iface, str(metric))

                        console.print(table)
                        if total > 20:
                            console.print(f"   [dim]... and {total - 20} more routes[\dim]")
                    else:
                        # Fallback: show raw output
                        console.print("\n   [bold]Raw Output:[/bold]")
                        raw_lines = route_data.get("raw", "").split("\n")
                        for line in raw_lines[:30]:
                            if line.strip():
                                console.print(f"   [dim]{line}[/dim]")
                        if len(raw_lines) > 30:
                            console.print(f"   [dim]... ({len(raw_lines) - 30}) more lines[/dim]")
                console.print("\n")

        # Footer
        console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
        console.print("[bold cyan]                    Diagnostics Complete                   [/bold cyan]")
        console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]\n")


if __name__ == "__main__":
    main()
