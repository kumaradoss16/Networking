# Networking Protocol Mastery Guide — Network Engineering + Security Engineering

**How to use this guide:** This is not a memorization list. For every protocol you'll find what it actually solves, where you'll touch it in real jobs, and what tier of effort it deserves. Priority meanings:

- **Essential** — you cannot do the job without this. Master config + troubleshooting + security implications.
- **High** — you'll hit this constantly in enterprise or freelance work. Know it well.
- **Medium** — situational but non-negotiable when it comes up (e.g., a client runs it).
- **Low** — know what it is and why it matters historically/rarely; don't invest deep hours.

Legend for the four columns of *practical depth* used throughout: **NE** = Network Engineer, **Sec** = Security Engineer, **Free** = Freelance/SMB technician. ✅ = important, ⚠️ = situational, ➖ = low relevance.

---

## TIER 1 — Must-Master Protocols (the foundation everything else sits on)

### Ethernet (IEEE 802.3)
- **Purpose / problem solved:** Frames data for transmission on a local physical/data-link segment; defines how devices on the same wire or switch fabric address each other (MAC addressing) and share media.
- **Real-world use:** Every wired LAN, every switch port, every server NIC, every uplink between switches.
- **NE:** ✅ Essential — you configure duplex/speed, port security, trunking on top of this daily.
- **Sec:** ✅ Essential — MAC spoofing, ARP/L2 attacks, port security bypass all live here.
- **Free:** ✅ Essential — cabling, switch port issues are the #1 SMB troubleshooting call.
- **Config relevance:** Port speed/duplex, MTU, port security (MAC limiting), storm control.
- **Troubleshooting relevance:** CRC errors, collisions, duplex mismatches, cable faults — `show interfaces`, `show mac address-table`.
- **Security relevance:** MAC flooding, CAM table overflow, rogue switches, VLAN hopping foundations.
- **Priority:** Essential.
- **Standards/notes:** 802.3 (wired), frame has Preamble/SFD, Dest MAC, Src MAC, EtherType, Payload, FCS. Min frame 64B, max standard 1518B (1522B tagged).

### ARP (Address Resolution Protocol)
- **Purpose:** Maps an IPv4 address to a MAC address on the local segment so Ethernet frames can actually be delivered.
- **Problem solved:** IP is L3 logical addressing; Ethernet needs L2 physical addressing — ARP bridges the two.
- **Real-world use:** Every IPv4 LAN, every default gateway resolution, every "why can't this device reach the gateway" ticket.
- **NE:** ✅ Essential — `show arp`, static ARP entries, gratuitous ARP behavior on failover (HSRP/VRRP).
- **Sec:** ✅ Essential — ARP spoofing/poisoning is one of the most common MITM techniques on LANs; Dynamic ARP Inspection (DAI) is a core mitigation you must know.
- **Free:** ✅ Essential — duplicate IP issues, ARP cache problems are everyday SMB troubleshooting.
- **Config relevance:** Static ARP entries, DAI, ARP timeout tuning.
- **Troubleshooting relevance:** Stale ARP cache, ARP table exhaustion, ARP storms.
- **Security relevance:** ARP spoofing (Ettercap/arpspoof), DAI + DHCP snooping trust as mitigation.
- **Priority:** Essential.
- **Notes:** No port (L2/L3 boundary protocol), EtherType 0x0806. IPv6 replaces this with NDP.

### IPv4
- **Purpose:** Logical/global addressing and routing of packets between networks.
- **Problem solved:** Ethernet only works on a local segment; IP lets packets traverse multiple networks to reach any destination.
- **Real-world use:** The addressing scheme underneath almost all traffic today (still, despite IPv6 growth).
- **NE:** ✅ Essential — subnetting, VLSM, summarization, routing table logic is the core skill of the job.
- **Sec:** ✅ Essential — every ACL, firewall rule, and IDS signature is built around IP addressing/subnets.
- **Free:** ✅ Essential — you will subnet home/SMB networks constantly.
- **Config relevance:** Static/DHCP addressing, subnetting, routing, NAT boundaries.
- **Troubleshooting relevance:** Subnet mismatches, exhausted DHCP scopes, routing loops, asymmetric routing.
- **Security relevance:** Spoofing, fragmentation attacks, ACL design, segmentation.
- **Priority:** Essential.
- **Notes:** Header fields: Version, IHL, ToS/DSCP, Total Length, ID/Flags/Fragment Offset, TTL, Protocol (6=TCP,17=UDP,1=ICMP), Header Checksum, Src/Dst IP. You must be able to subnet in your head fast (VLSM, CIDR).

### IPv6
- **Purpose:** Successor addressing scheme with a vastly larger address space and simplified header.
- **Problem solved:** IPv4 exhaustion; also improves autoconfiguration (SLAAC) and removes the need for NAT in many designs.
- **Real-world use:** Mandatory in large enterprises, ISPs, mobile carriers, cloud providers (AWS/Azure/GCP all support/require IPv6 planning now); still patchy in SMB.
- **NE:** ✅ Essential (increasingly) — dual-stack design, SLAAC vs DHCPv6, prefix delegation.
- **Sec:** ✅ Essential — IPv6 is frequently *misconfigured or unmonitored*, making it a common bypass path around IPv4-only firewalls/IDS.
- **Free:** ⚠️ Medium-High — less common in SMB gear but growing; ISPs are pushing it.
- **Config relevance:** Address types (link-local, ULA, global unicast), SLAAC, DHCPv6, prefix delegation, dual-stack routing.
- **Troubleshooting relevance:** Missing RA (Router Advertisement), duplicate address detection failures, dual-stack asymmetry.
- **Security relevance:** Rogue RA attacks, IPv6 tunneling used to bypass IPv4 firewalls, NDP spoofing (the IPv6 analog of ARP spoofing).
- **Priority:** Essential.
- **Notes:** 128-bit addresses, no header checksum, no fragmentation by routers (path MTU discovery only), NDP (ICMPv6) replaces ARP.

### ICMP / ICMPv6
- **Purpose:** Control-plane messaging — error reporting and diagnostics for IP.
- **Problem solved:** IP has no built-in way to report "unreachable," "TTL exceeded," etc. — ICMP provides that feedback channel.
- **Real-world use:** ping, traceroute, PMTUD (Path MTU Discovery), IPv6 NDP (ICMPv6 types 133-137).
- **NE:** ✅ Essential — your primary reachability/troubleshooting tool.
- **Sec:** ✅ Essential — ICMP tunneling (data exfil), ping sweeps/recon, smurf attacks, and knowing *what to block vs allow* (don't blanket-block ICMP — it breaks PMTUD).
- **Free:** ✅ Essential — first tool for every "is it up" question.
- **Config relevance:** Rate-limiting ICMP, selectively allowing (echo-reply, unreachable, time-exceeded) through firewalls.
- **Troubleshooting relevance:** ping, traceroute/tracert, mtr — bread and butter tools.
- **Security relevance:** ICMP tunneling, covert channels, reconnaissance, smurf/DoS.
- **Priority:** Essential.
- **Notes:** No ports — identified by Type/Code (Echo Request=8, Echo Reply=0, Dest Unreachable=3, TTL Exceeded=11). ICMPv6 additionally carries NDP.

### TCP
- **Purpose:** Reliable, ordered, connection-oriented delivery of data between hosts.
- **Problem solved:** IP is best-effort/unreliable; TCP adds retransmission, ordering, flow control, congestion control.
- **Real-world use:** HTTP/S, SSH, database connections, email — most application traffic that needs reliability.
- **NE:** ✅ Essential — MTU/MSS issues, window scaling, TCP resets in troubleshooting.
- **Sec:** ✅ Essential — the three-way handshake underlies SYN floods, port scanning (SYN/connect scans), session hijacking, firewall stateful inspection logic.
- **Free:** ✅ Essential — "why is this connection slow/dropping" is a TCP-analysis question 90% of the time.
- **Config relevance:** MSS clamping (common on VPN/tunnel links), TCP keepalives, firewall stateful tracking.
- **Troubleshooting relevance:** Packet captures (Wireshark) reading SYN/SYN-ACK/ACK, retransmissions, resets, window size collapse.
- **Security relevance:** SYN flood/DoS, scanning techniques, stateful firewall bypass attempts, session hijacking.
- **Priority:** Essential.
- **Notes:** Header: Src/Dst Port, Seq/Ack numbers, Flags (SYN, ACK, FIN, RST, PSH, URG), Window Size, Checksum. 3-way handshake: SYN → SYN-ACK → ACK.

### UDP
- **Purpose:** Lightweight, connectionless, low-overhead delivery.
- **Problem solved:** Some applications (DNS, streaming, VoIP, gaming) need speed over reliability — TCP's overhead isn't worth it.
- **Real-world use:** DNS, DHCP, NTP, SNMP, VoIP (RTP), QUIC/HTTP3, VPN tunnels (WireGuard, IPsec/IKE, OpenVPN-UDP).
- **NE:** ✅ Essential — many core services (DNS/DHCP/NTP) ride on UDP.
- **Sec:** ✅ Essential — UDP is spoofable (no handshake) and is the basis of amplification DDoS (DNS, NTP, memcached reflection).
- **Free:** ✅ Essential — DNS/DHCP troubleshooting requires understanding UDP behavior.
- **Config relevance:** Firewall rules for stateless traffic, timeout tuning for "pseudo-sessions."
- **Troubleshooting relevance:** No handshake to inspect — you rely on payload-level and application-level diagnostics.
- **Security relevance:** Spoofing, reflection/amplification DDoS, requires careful ACL design since there's no session state.
- **Priority:** Essential.
- **Notes:** Header only has Src/Dst Port, Length, Checksum — 8 bytes total, no reliability logic.

---

## TIER 2 — Enterprise Routing and Switching Protocols

### VLAN / 802.1Q Trunking
- **Purpose:** Logically segments a single physical switch fabric into multiple broadcast domains.
- **Problem solved:** Without VLANs, every device shares one broadcast domain — bad for security, performance, and organization.
- **Real-world use:** Every enterprise switch deployment: data VLAN, voice VLAN, guest VLAN, management VLAN, DMZ VLAN.
- **NE:** ✅ Essential — VLAN design is core switch configuration work.
- **Sec:** ✅ Essential — segmentation is a primary control; VLAN hopping (double-tagging, switch spoofing) is a real attack you must defend against.
- **Free:** ✅ Essential — separating guest Wi-Fi from internal LAN is one of the most common SMB jobs.
- **Config relevance:** Trunk/access ports, native VLAN, VTP/no-VTP, inter-VLAN routing (router-on-a-stick or L3 SVIs).
- **Troubleshooting relevance:** Wrong VLAN assignment, native VLAN mismatch, trunk not passing expected VLANs.
- **Security relevance:** VLAN hopping, native VLAN exploitation — always set native VLAN to an unused ID and disable auto-trunking (DTP) on access ports.
- **Priority:** Essential.
- **Notes:** 802.1Q inserts a 4-byte tag (12-bit VLAN ID, 1-4094) into the Ethernet frame.

### STP / RSTP / MSTP (Spanning Tree family)
- **Purpose:** Prevents Layer 2 loops in switched networks with redundant links.
- **Problem solved:** Redundant switch links create broadcast storms and MAC table instability without a loop-prevention protocol.
- **Real-world use:** Any enterprise with redundant switch uplinks (basically all of them).
- **NE:** ✅ Essential — root bridge election, port roles/states, PortFast/BPDU Guard are daily config knowledge.
- **Sec:** ⚠️ High — BPDU spoofing attacks can manipulate root election and manipulate traffic paths; you configure BPDU Guard/Root Guard as defenses.
- **Free:** ⚠️ Medium-High — smaller networks may have only 1-2 switches (no loops), but any redundant SMB design needs it.
- **Config relevance:** Root bridge priority, PortFast, BPDU Guard, Root Guard, choosing RSTP over legacy STP (much faster convergence), MSTP for multiple VLAN instances at scale.
- **Troubleshooting relevance:** Topology change notifications, unexpected root bridge changes, flapping ports.
- **Security relevance:** BPDU spoofing/attacks, unauthorized root bridge takeover.
- **Priority:** Essential (NE) / High (Sec, Free).
- **Notes:** STP = 802.1D (slow, 30-50s convergence), RSTP = 802.1w (sub-second), MSTP = 802.1s (multiple instances mapped to VLAN groups).

### LACP (Link Aggregation Control Protocol, 802.3ad)
- **Purpose:** Bundles multiple physical links into one logical link for redundancy and bandwidth.
- **Problem solved:** Single links are both a bandwidth bottleneck and single point of failure between switches/servers.
- **Real-world use:** Switch-to-switch uplinks, server NIC teaming, firewall HA links.
- **NE:** ✅ Essential — port-channel/EtherChannel configuration is routine.
- **Sec:** ⚠️ Medium — mostly a reliability/performance concern, minor security surface (LACP spoofing is rare but possible).
- **Free:** ⚠️ Medium — matters more once redundancy/performance requirements grow past a single switch.
- **Config relevance:** Active/passive LACP modes, load-balancing hash algorithms, matching config on both ends.
- **Troubleshooting relevance:** Mismatched LACP mode, one member down silently degrading capacity, hashing causing uneven load.
- **Security relevance:** Low — mostly availability, not confidentiality/integrity.
- **Priority:** High.
- **Notes:** Standard is 802.3ad (now under 802.1AX). Alternative: static EtherChannel (no negotiation) or Cisco PAgP (legacy/proprietary).

### OSPF (Open Shortest Path First)
- **Purpose:** Interior Gateway Protocol (IGP) for dynamic routing inside an autonomous system, using link-state (Dijkstra SPF) logic.
- **Problem solved:** Manually maintaining static routes across large networks doesn't scale or adapt to failures.
- **Real-world use:** The dominant IGP in enterprise, data center, and service-provider internal networks.
- **NE:** ✅ Essential — core routing protocol knowledge; areas, LSAs, DR/BDR election, cost metrics.
- **Sec:** ⚠️ High — routing protocol authentication (MD5/SHA), route filtering to prevent injection of malicious routes.
- **Free:** ⚠️ Medium — smaller SMB networks often just use static routes/default routes, but you'll meet OSPF on any client with more than one router.
- **Config relevance:** Area design (area 0 backbone + other areas), network statements, passive interfaces, authentication, route summarization.
- **Troubleshooting relevance:** Neighbor adjacency stuck states (2-way, ExStart), mismatched area IDs/hello timers/MTU, DR/BDR issues.
- **Security relevance:** Routing protocol authentication, filtering to prevent route injection/route poisoning.
- **Priority:** Essential (NE), High (Sec, Free).
- **Notes:** Uses IP protocol 89 directly (no TCP/UDP). Metric = cost (based on bandwidth). Multicast addresses 224.0.0.5/224.0.0.6 for neighbor discovery.

### EIGRP (Enhanced Interior Gateway Routing Protocol)
- **Purpose:** Cisco's advanced distance-vector (hybrid) IGP using DUAL algorithm for fast convergence.
- **Problem solved:** Same as OSPF (dynamic internal routing) but with different mechanics — easier to configure, very fast convergence, but historically Cisco-proprietary (now partially open, RFC 7868).
- **Real-world use:** Still common in legacy/existing Cisco-heavy enterprise networks; less common in new greenfield or multi-vendor designs.
- **NE:** ⚠️ High — you'll encounter it in Cisco shops, and it's a CCNA/CCNP-required protocol.
- **Sec:** ⚠️ Medium — same authentication/filtering concerns as OSPF, smaller attack surface exposure due to Cisco-only prevalence.
- **Free:** ⚠️ Medium — relevant if a client runs all-Cisco gear.
- **Config relevance:** AS numbers, K-values (metric weighting), summarization, authentication.
- **Troubleshooting relevance:** Neighbor mismatches (K-values, AS number), stuck-in-active routes, feasible successor logic.
- **Security relevance:** Route authentication (MD5/SHA), route filtering.
- **Priority:** High (Cisco shops) / Medium (multi-vendor).
- **Notes:** Uses IP protocol 88. Composite metric (bandwidth, delay, reliability, load).

### BGP (Border Gateway Protocol)
- **Purpose:** The Exterior Gateway Protocol (EGP) that routes between autonomous systems — the protocol that runs the internet.
- **Problem solved:** IGPs don't scale to internet-size or handle policy-based routing between independent organizations; BGP does path-vector routing with rich policy control.
- **Real-world use:** ISPs, large enterprises with multiple internet uplinks (multihoming), cloud provider peering, data center underlays (BGP is now common even inside data centers, e.g., EVPN/VXLAN fabrics).
- **NE:** ✅ Essential at senior/ISP/large-enterprise level — High for general enterprise.
- **Sec:** ✅ High — BGP hijacking (route leaks/hijacks) is a major internet-security topic; RPKI, prefix filtering, and BGP monitoring matter.
- **Free:** ➖ Low-Medium — rare in SMB unless the client multihomes to two ISPs.
- **Config relevance:** eBGP/iBGP peering, route maps, prefix lists, AS-path filtering, communities, local preference/MED for path selection.
- **Troubleshooting relevance:** Peering down states, route flapping, incorrect path selection, missing route advertisements.
- **Security relevance:** BGP hijacking, route leaks, RPKI/ROV, prefix filtering, MD5 authentication (TCP AO now preferred).
- **Priority:** Essential (ISP/large enterprise) / Medium (general enterprise) / Low (small SMB).
- **Notes:** Runs over TCP port 179. Path-vector protocol; AS-path is the core loop-prevention/selection mechanism.

### RIP / RIPv2 (Routing Information Protocol)
- **Purpose:** Simple distance-vector IGP using hop count as the metric.
- **Problem solved:** Was an early, simple answer to dynamic routing — now mostly superseded by OSPF/EIGRP.
- **Real-world use:** Legacy networks, some lab/教育 environments, very small/simple topologies. Rare in modern production enterprise.
- **NE:** ⚠️ Low-Medium — good to understand distance-vector concepts, unlikely to configure in production.
- **Sec:** ➖ Low — mostly a "know it exists and is insecure" item (RIPv1 has no authentication at all; RIPv2 supports plaintext/MD5).
- **Free:** ➖ Low — you might inherit it in an old client network, rarely deploy it new.
- **Config relevance:** Minimal — understand `router rip`, hop-count limit of 15 (16 = unreachable).
- **Troubleshooting relevance:** Slow convergence, count-to-infinity, split horizon issues.
- **Security relevance:** Lack of/weak authentication makes it trivially spoofable — a reason it's phased out.
- **Priority:** Low (understand only, tier 13-adjacent).
- **Notes:** UDP port 520. Max 15 hops. RIPng exists for IPv6 (also legacy-status).

---

## TIER 3 — Network Service Protocols

### DHCP (Dynamic Host Configuration Protocol)
- **Purpose:** Automatically assigns IP addresses and network configuration (gateway, DNS, etc.) to hosts.
- **Problem solved:** Manual IP assignment doesn't scale and is error-prone (duplicate IPs, misconfiguration).
- **Real-world use:** Every network — client devices, VoIP phones, guest Wi-Fi, IoT.
- **NE:** ✅ Essential — scope design, relay/IP helper config, exclusions, reservations.
- **Sec:** ✅ High — rogue DHCP servers (handing out malicious gateway/DNS) are a real MITM technique; DHCP snooping is a key L2 defense.
- **Free:** ✅ Essential — the most common "why can't this device get on the network" root cause.
- **Config relevance:** Scopes, reservations, relay (`ip helper-address`), option 43/66 (VoIP/PXE), DHCP snooping trust boundaries.
- **Troubleshooting relevance:** Scope exhaustion, relay misconfiguration, rogue server conflicts, lease renewal failures (DORA process).
- **Security relevance:** Rogue DHCP servers, DHCP starvation attacks, DHCP snooping + dynamic ARP inspection pairing.
- **Priority:** Essential.
- **Notes:** UDP 67 (server), UDP 68 (client). DORA = Discover, Offer, Request, Acknowledge.

### DNS (Domain Name System)
- **Purpose:** Resolves human-readable names to IP addresses (and other records).
- **Problem solved:** Humans can't memorize IPs; DNS provides a distributed, hierarchical naming system.
- **Real-world use:** Everything — web browsing, internal Active Directory, service discovery, email routing (MX records), cloud service endpoints.
- **NE:** ✅ Essential — internal DNS zones, conditional forwarding, split-horizon DNS.
- **Sec:** ✅ Essential — DNS is a top attack/exfiltration vector (DNS tunneling, cache poisoning, DGA malware, typosquatting) and a top defense point (DNS filtering/sinkholing, DNSSEC).
- **Free:** ✅ Essential — you configure DNS for every client (internal AD DNS, public domain records for websites/email).
- **Config relevance:** A/AAAA/CNAME/MX/TXT/NS/PTR records, forwarders, split-horizon, DNSSEC signing.
- **Troubleshooting relevance:** `nslookup`/`dig`, propagation delays, incorrect records, resolver loops.
- **Security relevance:** Cache poisoning, DNS tunneling (exfil/C2), DNSSEC, DNS-based content filtering.
- **Priority:** Essential.
- **Notes:** UDP/TCP 53 (TCP for zone transfers and large responses, also used more now due to DNS-over-TCP fallback). DNS-over-HTTPS (DoH)/DNS-over-TLS (DoT) are modern encrypted variants you should know exist for both privacy and as an evasion technique attackers use to bypass DNS filtering.

### NAT (Network Address Translation)
- **Purpose:** Translates private IP addresses to public (or between address spaces) to conserve public IPv4 and hide internal addressing.
- **Problem solved:** IPv4 address exhaustion; also provides a layer of address obfuscation.
- **Real-world use:** Every SOHO/enterprise edge router/firewall, cloud NAT gateways.
- **NE:** ✅ Essential — static NAT, PAT (overload), NAT pools are everyday firewall/router config.
- **Sec:** ⚠️ High — NAT is *not* a security boundary by itself (common misconception) but does obscure internal topology; you must understand NAT traversal issues for VPNs (NAT-T) and how NAT interacts with logging/attribution (SMB clients often think NAT = firewall — correct that).
- **Free:** ✅ Essential — practically every SMB router does NAT/PAT by default.
- **Config relevance:** Static NAT (1:1), Dynamic NAT, PAT/NAT overload, port forwarding.
- **Troubleshooting relevance:** Port forwarding failures, NAT table exhaustion, double-NAT scenarios, asymmetric NAT breaking VoIP/VPN.
- **Security relevance:** False sense of security (NAT ≠ firewall), NAT-T for IPsec, logging challenges (many hosts appear as one public IP).
- **Priority:** Essential.
- **Notes:** Works with IPv4 primarily (IPv6 generally avoids NAT via abundant address space, though NPTv6 exists).

### NTP (Network Time Protocol)
- **Purpose:** Synchronizes clocks across devices on a network.
- **Problem solved:** Accurate, consistent time is required for logging correlation, certificate validation, Kerberos authentication, and troubleshooting.
- **Real-world use:** Every enterprise network, every server, every network device — foundational and invisible until it breaks.
- **NE:** ✅ Essential — misconfigured NTP breaks Kerberos auth, cert validation, and makes log correlation across devices impossible.
- **Sec:** ✅ Essential — SIEM correlation, forensic timelines, and certificate/Kerberos validity all depend on accurate synced time; NTP can also be abused for DDoS amplification (monlist).
- **Free:** ✅ High — small networks still need consistent time for AD, backups, cert-based VPNs.
- **Config relevance:** NTP server/client hierarchy (stratum), authentication (NTP with symmetric keys), redundant sources.
- **Troubleshooting relevance:** Clock drift, stratum errors, firewall blocking UDP 123 breaking sync silently.
- **Security relevance:** NTP amplification DDoS (mitigate by disabling `monlist`), time-based auth/cert failures if unsynced.
- **Priority:** Essential.
- **Notes:** UDP 123.

### SNMP / SNMPv3
- **Purpose:** Monitors and manages network devices (polling stats, receiving traps/alerts).
- **Problem solved:** Manual, device-by-device status checking doesn't scale; SNMP gives centralized visibility.
- **Real-world use:** Network monitoring platforms (SolarWinds, PRTG, LibreNMS, Zabbix, Nagios) polling switches/routers/firewalls.
- **NE:** ✅ Essential — configuring SNMP for monitoring tools is routine.
- **Sec:** ✅ High — SNMPv1/v2c use plaintext community strings ("public"/"private" defaults are a classic pentest finding); SNMPv3 adds real authentication/encryption and should be mandated.
- **Free:** ⚠️ Medium-High — useful once you're managing more than a handful of devices for a client.
- **Config relevance:** Community strings (v1/v2c, avoid in production), SNMPv3 users/auth/priv, trap destinations, MIBs/OIDs.
- **Troubleshooting relevance:** Polling failures, ACL blocking SNMP, wrong OIDs for specific metrics.
- **Security relevance:** Default/weak community strings, always prefer SNMPv3 with authPriv, restrict via ACLs.
- **Priority:** Essential (NE/monitoring context), High (Sec).
- **Notes:** UDP 161 (agent), UDP 162 (traps/notifications).

### Syslog
- **Purpose:** Standard logging protocol — devices send log/event messages to a central collector.
- **Problem solved:** Without centralized logging, incident response and troubleshooting require logging into every device individually.
- **Real-world use:** Every enterprise network sends switch/router/firewall/server logs to a SIEM or syslog server (Splunk, Graylog, ELK, rsyslog).
- **NE:** ✅ Essential — you configure logging levels/destinations on every device you touch.
- **Sec:** ✅ Essential — this is the backbone of detection, alerting, and forensic investigation; understanding severity levels and facility codes matters for building correlation rules.
- **Free:** ✅ High — even a small centralized log setup dramatically improves troubleshooting for SMB clients.
- **Config relevance:** Logging levels (0-7, emergency to debug), facility codes, remote logging destination, log rotation.
- **Troubleshooting relevance:** Missing logs (wrong severity threshold), log storage exhaustion, time-sync issues skewing correlation.
- **Security relevance:** SIEM ingestion, tamper-evidence (send logs off-device immediately so an attacker can't erase local logs), alerting rules.
- **Priority:** Essential.
- **Notes:** UDP 514 traditionally (unencrypted, unreliable); TCP 514 or TLS-syslog (RFC 5425, port 6514) preferred for reliability/security in modern deployments.

---

## TIER 4 — Web and Application Protocols

### HTTP
- **Purpose:** The application-layer protocol for transferring web content.
- **Problem solved:** Provides a standard request/response model for retrieving/submitting web resources.
- **Real-world use:** Legacy/internal web traffic, API backends behind TLS termination points, and still common for internal-only/non-sensitive traffic.
- **NE:** ✅ High — you'll load-balance, proxy, and troubleshoot HTTP traffic constantly.
- **Sec:** ✅ Essential — understanding HTTP methods, status codes, and headers underlies both web app security testing and firewall/proxy rule design.
- **Free:** ✅ High — basic web hosting/troubleshooting requirement.
- **Config relevance:** Reverse proxy rules, load balancer health checks, header inspection.
- **Troubleshooting relevance:** Status codes (2xx/3xx/4xx/5xx), header issues, caching problems.
- **Security relevance:** Should almost never be used unencrypted for anything sensitive today; understand it to understand HTTPS.
- **Priority:** High.
- **Notes:** TCP 80. Methods: GET, POST, PUT, DELETE, HEAD, OPTIONS, PATCH.

### HTTPS
- **Purpose:** HTTP secured with TLS — encrypted, authenticated web traffic.
- **Problem solved:** Plaintext HTTP is trivially interceptable/modifiable; HTTPS provides confidentiality, integrity, and server authentication.
- **Real-world use:** Essentially all modern web/API traffic.
- **NE:** ✅ Essential — TLS termination on load balancers, cert management, SNI-based routing.
- **Sec:** ✅ Essential — cert validation, cipher suite hardening, TLS inspection/interception (and its trade-offs), certificate pinning awareness.
- **Free:** ✅ Essential — every client site needs valid, properly configured HTTPS.
- **Config relevance:** Certificate installation/renewal (Let's Encrypt/ACME), TLS version/cipher policy, HSTS.
- **Troubleshooting relevance:** Cert expiry, chain issues, mixed content, TLS handshake failures (cipher mismatch).
- **Security relevance:** Core to almost every security control — see TLS entry below for depth.
- **Priority:** Essential.
- **Notes:** TCP 443.

### TLS (Transport Layer Security)
*(This is covered in depth in the Tier 8/Deep-Dive section below since it's one of the most important protocols in this entire list.)*
- **Priority:** Essential.

### WebSocket
- **Purpose:** Provides full-duplex, persistent communication channels over a single TCP connection (upgraded from HTTP).
- **Problem solved:** HTTP's request/response model is inefficient for real-time bidirectional data (chat apps, live dashboards, trading platforms, IoT telemetry).
- **Real-world use:** Real-time web apps, monitoring dashboards, chat/collaboration tools, some VoIP signaling.
- **NE:** ⚠️ Medium — matters when load balancing/proxying real-time apps (sticky sessions, timeout tuning).
- **Sec:** ⚠️ Medium-High — WebSocket traffic often bypasses traditional HTTP-aware inspection; understand it as a potential blind spot for DLP/proxy tools.
- **Free:** ⚠️ Medium — relevant if hosting/supporting real-time web applications for a client.
- **Config relevance:** Reverse proxy WebSocket upgrade support (`Upgrade: websocket` header), long idle timeouts.
- **Troubleshooting relevance:** Proxies/firewalls dropping long-idle connections, load balancer session stickiness.
- **Security relevance:** Inspection blind spots, cross-site WebSocket hijacking (CSWSH) awareness.
- **Priority:** Medium.
- **Notes:** Starts as an HTTP/1.1 Upgrade request, then runs as its own framed protocol over the same TCP connection (typically 80/443).

### QUIC / HTTP/3
- **Purpose:** A UDP-based transport (QUIC) carrying HTTP/3, designed to reduce latency and handle connection migration better than TCP+TLS.
- **Problem solved:** TCP+TLS handshake overhead and head-of-line blocking slow down modern web performance, especially on mobile/lossy networks.
- **Real-world use:** Google/YouTube, Facebook, increasingly widespread across CDNs (Cloudflare, Fastly) and browsers (Chrome, Firefox).
- **NE:** ⚠️ Medium-High and growing — firewalls/load balancers need explicit QUIC/UDP-443 support, and it changes how you troubleshoot (no more simple TCP handshake analysis).
- **Sec:** ⚠️ High — QUIC encrypts more of the handshake than TLS-over-TCP, meaning traditional network-based inspection (SNI-based filtering, some IDS signatures) has reduced visibility; many security teams explicitly block UDP/443 to force fallback to inspectable HTTP/2.
- **Free:** ⚠️ Low-Medium — mostly relevant if hosting high-traffic public services.
- **Config relevance:** Allowing/blocking UDP 443, ensuring firewalls/proxies understand QUIC.
- **Troubleshooting relevance:** Different tooling needed (can't rely on classic TCP-based captures the same way); fallback behavior when QUIC is blocked.
- **Security relevance:** Reduced inspectability is the headline issue; many orgs deliberately block it.
- **Priority:** Medium (rising).
- **Notes:** UDP 443. HTTP/3 is the application layer riding on QUIC.


---

## TIER 5 — Remote Administration Protocols

### SSH (Secure Shell)
- **Purpose:** Encrypted remote command-line access and secure tunneling.
- **Problem solved:** Telnet sends everything (including passwords) in plaintext; SSH provides encrypted, authenticated remote access.
- **Real-world use:** Managing every router, switch, firewall, Linux server, cloud instance. The single most-used remote admin tool in networking/security.
- **NE:** ✅ Essential — daily device management tool.
- **Sec:** ✅ Essential — key-based auth, hardening (disable password auth, disable root login, change default port, fail2ban), SSH tunneling/port forwarding (used both defensively and by attackers for pivoting).
- **Free:** ✅ Essential — how you'll manage every client device remotely.
- **Config relevance:** Key-based authentication, disabling weak ciphers, `AllowUsers`/jump hosts, port forwarding (`-L`/`-R`/`-D` tunnels).
- **Troubleshooting relevance:** Auth failures, host key mismatches, MTU/fragmentation issues over SSH tunnels.
- **Security relevance:** Brute-force targeting (harden with key-only auth + fail2ban), SSH used maliciously for tunneling/pivoting/data exfil — know both sides.
- **Priority:** Essential.
- **Notes:** TCP 22. SSHv2 only (SSHv1 is broken/deprecated).

### Telnet
- **Purpose:** Unencrypted remote terminal access (SSH's ancestor).
- **Problem solved:** Historically solved remote CLI access before encryption was standard — today it solves nothing that SSH doesn't do better and safer.
- **Real-world use:** Still found on legacy industrial/OT equipment, old switches, some console-server setups, and lab environments (e.g., Cisco Packet Tracer/GNS3 exercises).
- **NE:** ⚠️ Low-Medium — know it for legacy gear and exam purposes; never enable it in production.
- **Sec:** ✅ High to *know as a finding* — Telnet on any device is a textbook pentest/audit failure (plaintext credentials); part of your job will be finding and eliminating it.
- **Free:** ⚠️ Low — occasionally you'll find an old client device still using it and need to disable/replace it.
- **Config relevance:** Know how to disable it (`no ip domain-lookup`... `transport input ssh` on Cisco) more than how to configure it.
- **Troubleshooting relevance:** Minimal — mainly used to confirm/demonstrate a security gap.
- **Security relevance:** Plaintext credentials sniffable on the wire — a hard "must remediate" finding.
- **Priority:** Low (understand + know how to remediate).
- **Notes:** TCP 23.

---

## TIER 6 — File Transfer Protocols

### FTP (File Transfer Protocol)
- **Purpose:** Transfers files between client and server.
- **Problem solved:** Historically the standard way to move files over a network before secure alternatives existed.
- **Real-world use:** Legacy systems, some public file distribution (anonymous FTP), older embedded/industrial devices, some ISP/hosting environments still default to it.
- **NE:** ⚠️ Medium — you'll need to support/troubleshoot it in legacy environments (especially active vs passive mode NAT/firewall issues, which is a genuinely tricky, common ticket).
- **Sec:** ✅ High as a *finding* — plaintext credentials and data; a common audit/pentest flag, similar to Telnet.
- **Free:** ⚠️ Medium — website hosting/client file transfer setups sometimes still use it (should push clients to SFTP).
- **Config relevance:** Active vs passive mode (huge for firewall/NAT config — passive mode is generally the fix for "FTP doesn't work through my firewall").
- **Troubleshooting relevance:** The classic active/passive mode + NAT/firewall interaction problem — you must understand this cold.
- **Security relevance:** Plaintext auth and data — migrate clients to SFTP/FTPS.
- **Priority:** Medium (understand deeply because of the NAT/firewall troubleshooting angle, even though you'll rarely deploy new FTP).
- **Notes:** TCP 21 (control), TCP 20 or dynamic high ports (data, depending on active/passive mode).

### SFTP (SSH File Transfer Protocol)
- **Purpose:** Secure file transfer running over an SSH connection.
- **Problem solved:** Provides FTP-like file transfer functionality with SSH's encryption/authentication — no separate credentials/data channel to secure.
- **Real-world use:** The modern default for secure file transfer in enterprise and SMB — backup jobs, automated file drops, secure client file exchange.
- **NE:** ✅ High — you'll set this up for automated transfers and remote backups regularly.
- **Sec:** ✅ High — key-based auth, chroot-jailing SFTP users, audit logging.
- **Free:** ✅ High — a very common client deliverable ("secure file transfer for our vendor").
- **Config relevance:** SSH key auth, chroot/jail configuration, restricting to SFTP-only (no shell access).
- **Troubleshooting relevance:** Permission errors, chroot misconfig, key mismatches.
- **Security relevance:** Much safer default than FTP — no plaintext credentials, single encrypted channel, easier to firewall (one port).
- **Priority:** High.
- **Notes:** Runs over SSH — TCP 22, not related to FTP protocol despite the name.

### SCP (Secure Copy Protocol)
- **Purpose:** Simple secure file copy over SSH.
- **Problem solved:** Quick one-off encrypted file transfers without the overhead of setting up a full SFTP session.
- **Real-world use:** Quick admin file transfers, scripted backups/config pulls (e.g., pulling device configs).
- **NE:** ✅ High — you'll use this constantly to pull/push configs and backups.
- **Sec:** ⚠️ Medium — same security posture as SSH; note SCP's legacy protocol has had CVEs, many tools now default to SFTP under the hood even when called "scp."
- **Free:** ⚠️ Medium-High — fast day-to-day tool.
- **Config relevance:** Basically just SSH access — no separate service to configure.
- **Troubleshooting relevance:** Same as SSH connectivity issues.
- **Security relevance:** Inherits SSH's security; be aware modern OpenSSH deprecates the old SCP protocol implementation in favor of SFTP-based transfer under the `scp` command.
- **Priority:** High.
- **Notes:** TCP 22 (rides on SSH).

---

## TIER 7 — Email Protocols

### SMTP (Simple Mail Transfer Protocol)
- **Purpose:** Sends/relays email between mail servers.
- **Problem solved:** Standardizes how mail servers hand off messages to each other across the internet.
- **Real-world use:** Every mail server (Exchange, Google Workspace, Postfix), transactional email systems, application notification systems.
- **NE:** ⚠️ Medium-High — mail relay/routing, firewall rules for mail flow.
- **Sec:** ✅ Essential — email is the #1 initial-access vector (phishing/BEC); SMTP relay security, open-relay prevention, and its role in spoofing (fixed via SPF/DKIM/DMARC below) are core blue-team knowledge.
- **Free:** ✅ High — setting up business email (often via M365/Google Workspace) and correct DNS/MX records is a very common SMB engagement.
- **Config relevance:** MX records, relay restrictions, STARTTLS enforcement, open relay prevention.
- **Troubleshooting relevance:** Mail queue backups, relay rejections, DNS/MX misconfiguration, SPF/DKIM/DMARC failures blocking legitimate mail.
- **Security relevance:** Open relay abuse, spoofing (mitigated by SPF/DKIM/DMARC), phishing infrastructure analysis.
- **Priority:** High (Essential for Sec specifically due to phishing/BEC relevance).
- **Notes:** TCP 25 (server-to-server relay), TCP 587 (submission, client-to-server, should require STARTTLS+auth), TCP 465 (SMTPS, implicit TLS).

### IMAP (Internet Message Access Protocol)
- **Purpose:** Retrieves and manages email while keeping it synced/stored on the server.
- **Problem solved:** Lets users access the same mailbox state (read/unread, folders) from multiple devices.
- **Real-world use:** Standard protocol for modern email clients (Outlook, mobile mail apps) connecting to mail servers.
- **NE:** ⚠️ Medium — mostly firewall/connectivity, not deep config.
- **Sec:** ⚠️ Medium-High — compromised credentials are frequently abused via IMAP for silent mailbox access/exfiltration (a classic BEC follow-on technique) — monitor for anomalous IMAP logins.
- **Free:** ⚠️ Medium — client email configuration support.
- **Config relevance:** Ensuring TLS-wrapped IMAP (IMAPS) is enforced, disabling legacy basic auth where possible (modern auth/OAuth instead).
- **Troubleshooting relevance:** Sync issues, folder mismatches, auth failures.
- **Security relevance:** Credential-stuffing target, legacy auth bypass of MFA — a real BEC investigation skill.
- **Priority:** Medium-High.
- **Notes:** TCP 143 (plaintext), TCP 993 (IMAPS/TLS).

### POP3 (Post Office Protocol v3)
- **Purpose:** Downloads email from server to a single client (traditionally deleting from server after download).
- **Problem solved:** Was an early, simple way to fetch mail before multi-device access was the norm.
- **Real-world use:** Legacy/simple setups, some backup/archival mail pulls; largely superseded by IMAP for anything multi-device.
- **NE:** ➖ Low — rarely a config concern today.
- **Sec:** ⚠️ Medium — same credential-target concern as IMAP, though less prevalent now.
- **Free:** ➖ Low-Medium — occasionally a client insists on it, mostly legacy.
- **Config relevance:** Minimal — know it exists and how it differs from IMAP (download-and-delete vs. sync).
- **Troubleshooting relevance:** "Email missing from other device" is a classic symptom of POP3 misuse.
- **Security relevance:** Similar credential exposure risk to IMAP if unencrypted.
- **Priority:** Low.
- **Notes:** TCP 110 (plaintext), TCP 995 (POP3S/TLS).

### SPF (Sender Policy Framework)
- **Purpose:** DNS TXT record listing which mail servers are authorized to send email for a domain.
- **Problem solved:** Prevents attackers from trivially spoofing "From: yourcompany.com" in phishing emails.
- **Real-world use:** Every legitimate business domain should publish SPF; mandatory for good email deliverability today.
- **NE:** ⚠️ Medium — DNS record management.
- **Sec:** ✅ Essential — a core anti-phishing/anti-spoofing control you'll configure, audit, and investigate constantly.
- **Free:** ✅ High — a standard deliverable when setting up business email for any client.
- **Config relevance:** Publishing a correct SPF TXT record (`v=spf1 include:... -all`), keeping it under the 10-lookup DNS limit.
- **Troubleshooting relevance:** SPF failures causing legitimate mail to be marked spam, misconfigured `-all` vs `~all` (hard vs soft fail).
- **Security relevance:** Directly mitigates domain spoofing (part of the SPF/DKIM/DMARC trio).
- **Priority:** Essential (Sec) / High (NE, Free).
- **Notes:** Published as DNS TXT record; no port (it's a policy record, checked by the receiving mail server).

### DKIM (DomainKeys Identified Mail)
- **Purpose:** Cryptographically signs outgoing email to prove it wasn't altered and genuinely came from the claimed domain.
- **Problem solved:** SPF only checks the sending server's IP; DKIM adds message-level integrity/authenticity via public-key signatures.
- **Real-world use:** Paired with SPF at every legitimate business domain; required by Gmail/Microsoft bulk sender policies.
- **NE:** ⚠️ Medium — DNS record + mail platform key configuration.
- **Sec:** ✅ Essential — part of the core anti-spoofing trio; you'll validate/investigate DKIM signature failures during phishing/BEC investigations.
- **Free:** ✅ High — standard part of setting up business email deliverability for clients.
- **Config relevance:** Generating key pairs, publishing the public key as a DNS TXT record, enabling signing on the mail platform.
- **Troubleshooting relevance:** Signature failures from body/header modification (e.g., mailing list footers breaking DKIM), key rotation issues.
- **Security relevance:** Confirms message integrity/origin — directly supports DMARC alignment.
- **Priority:** Essential (Sec) / High (NE, Free).
- **Notes:** DNS TXT record under a selector subdomain (e.g., `selector1._domainkey.yourdomain.com`).

### DMARC (Domain-based Message Authentication, Reporting & Conformance)
- **Purpose:** Tells receiving mail servers what to do when SPF/DKIM checks fail, and provides reporting.
- **Problem solved:** SPF and DKIM alone don't specify enforcement — DMARC closes that gap and adds visibility (aggregate/forensic reports).
- **Real-world use:** Required by major mailbox providers for bulk senders; a baseline expectation for any legitimate business domain in 2026.
- **NE:** ⚠️ Medium — DNS record publishing.
- **Sec:** ✅ Essential — DMARC policy (`p=none/quarantine/reject`) and report analysis is core anti-phishing/BEC defense work.
- **Free:** ✅ High — a standard, expected deliverable for client email security hardening.
- **Config relevance:** Publishing the DMARC TXT record, choosing policy strictness, setting up report aggregation.
- **Troubleshooting relevance:** Legitimate mail failing alignment (SPF/DKIM domain must align with the From: domain), third-party sender breakage.
- **Security relevance:** The enforcement layer that actually stops spoofed mail from landing in inboxes — a top-tier phishing defense.
- **Priority:** Essential (Sec) / High (NE, Free).
- **Notes:** DNS TXT record at `_dmarc.yourdomain.com`.


---

## TIER 8 — Security and Encryption Protocols

### TLS (Transport Layer Security) — DEEP DIVE
- **Purpose:** Provides confidentiality, integrity, and authentication for data in transit.
- **How it works:** Client and server perform a handshake — negotiate TLS version/cipher suite, server presents a certificate (validated via chain of trust to a root CA), a shared symmetric key is derived (via Diffie-Hellman in modern TLS 1.3 for forward secrecy), and all subsequent application data is encrypted with that symmetric key.
- **Structure (TLS 1.3 handshake, simplified):** ClientHello (supported versions/ciphers/key share) → ServerHello + Certificate + Finished → Client Finished → Application Data encrypted. (TLS 1.2 has more round trips; 1.3 reduced this to 1-RTT, with 0-RTT resumption available.)
- **Addressing:** Not a separate port — it wraps existing application protocols (HTTPS=443, SMTPS=465, IMAPS=993, etc.) or is negotiated via STARTTLS on the original plaintext port.
- **Configuration:** Certificate installation (public CA or internal PKI), disabling TLS 1.0/1.1 and weak ciphers (RC4, export ciphers), enabling HSTS, OCSP stapling.
- **Troubleshooting:** Cert chain errors, expired certs, SNI mismatches, cipher suite incompatibility between client and server, clock skew breaking cert validation.
- **NE:** ✅ Essential.
- **Sec:** ✅ Essential — you must understand handshake internals to do TLS interception/inspection, certificate pinning bypass analysis, and to spot downgrade attacks.
- **Free:** ✅ Essential — every client site/service needs correctly configured, current TLS.
- **Priority:** Essential.
- **Notes:** Current standard is TLS 1.3 (RFC 8446); TLS 1.2 still widely supported; SSL (the predecessor) is fully deprecated/insecure — never use it.

### IPsec — DEEP DIVE
- **Purpose:** Provides authenticated, encrypted communication at the IP layer — the foundation of most site-to-site and many remote-access VPNs.
- **How it works:** Two phases — **Phase 1 (IKE)** establishes a secure, authenticated channel between peers (negotiating encryption/hash/DH group, authenticating via PSK or certificates) to build an ISAKMP SA; **Phase 2** negotiates the actual IPsec SAs used to encrypt real traffic, using either **AH** (Authentication Header — integrity only, rarely used today) or **ESP** (Encapsulating Security Payload — encryption + integrity, the standard choice).
- **Modes:** Transport mode (encrypts payload only, host-to-host) vs Tunnel mode (encrypts entire original IP packet, used for site-to-site VPNs).
- **Addressing:** IKE uses UDP 500 (and UDP 4500 for NAT-Traversal when peers are behind NAT). ESP is IP protocol 50; AH is IP protocol 51.
- **Configuration:** Peer IPs, PSK or cert-based auth, IKE Phase 1/2 parameters (encryption algorithm, hash, DH group, lifetime), interesting traffic ACLs (what triggers the tunnel).
- **Troubleshooting:** Phase 1 vs Phase 2 mismatch (most common failure — mismatched proposals), NAT-T not enabled when peer is behind NAT, asymmetric routing breaking the tunnel, MTU/fragmentation issues (requires MSS clamping).
- **NE:** ✅ Essential — site-to-site VPN configuration is a core enterprise/freelance skill.
- **Sec:** ✅ Essential — cipher suite selection/hardening, PSK vs cert-based auth trade-offs, IKE vulnerability history (e.g., aggressive mode PSK cracking).
- **Free:** ✅ High — a very common SMB request ("connect our two offices securely").
- **Priority:** Essential.
- **Notes:** IKEv2 (RFC 7296) is the modern standard over IKEv1 — faster, more resilient (MOBIKE for connection mobility), better DoS resistance.

### IKE / IKEv2 (Internet Key Exchange)
- **Purpose:** The key-management/negotiation protocol used to establish IPsec security associations.
- **Problem solved:** IPsec needs a secure way to negotiate keys/algorithms before any encrypted data can flow — IKE does that negotiation.
- **Real-world use:** Underlies essentially all IPsec VPNs (site-to-site and IKEv2-based remote access, including built-in OS VPN clients on Windows/macOS/iOS).
- **NE:** ✅ Essential (bundled with IPsec config above).
- **Sec:** ✅ Essential — IKEv1 aggressive mode PSK weaknesses are a classic pentest finding; prefer IKEv2 with certificate auth where possible.
- **Free:** ✅ High.
- **Config relevance:** See IPsec above.
- **Troubleshooting relevance:** See IPsec above.
- **Security relevance:** Downgrade attacks (forcing IKEv1/aggressive mode), weak DH groups (avoid Group 2/5, use 14+ or ECC groups).
- **Priority:** Essential.
- **Notes:** UDP 500 / UDP 4500 (NAT-T).

### 802.1X (Port-Based Network Access Control)
- **Purpose:** Requires authentication before a device is granted network access at the switch port or wireless AP level.
- **Problem solved:** Without it, anyone who plugs into a wall jack or associates to a corporate SSID gets network access — 802.1X ties access to verified identity.
- **Real-world use:** Enterprise wired ports (NAC), enterprise Wi-Fi (WPA2/3-Enterprise), often paired with RADIUS as the backend.
- **NE:** ✅ Essential (large enterprise) — you configure this on switches/WLCs.
- **Sec:** ✅ Essential — this is a foundational Zero Trust/NAC control; understanding EAP methods (PEAP, EAP-TLS) and their relative security is core.
- **Free:** ⚠️ Medium — less common in small SMB (cost/complexity), but increasingly expected as "good practice" upsell.
- **Config relevance:** Supplicant/authenticator/authentication-server roles, EAP method selection, fallback (MAB — MAC Authentication Bypass — for non-802.1X devices like printers).
- **Troubleshooting relevance:** Supplicant misconfiguration, certificate trust issues (EAP-TLS), RADIUS server unreachable causing lockouts.
- **Security relevance:** EAP-TLS (cert-based) is far stronger than PEAP-MSCHAPv2 (credential-based, crackable) — know the difference and push clients toward EAP-TLS where feasible.
- **Priority:** Essential (large enterprise/Sec) / Medium (SMB).
- **Notes:** Uses EAPOL (EAP over LAN) at L2 between supplicant and authenticator; authenticator talks RADIUS to the auth server.


---

## TIER 9 — Enterprise Authentication and Directory Protocols

### RADIUS (Remote Authentication Dial-In User Service)
- **Purpose:** Centralized AAA (Authentication, Authorization, Accounting) protocol.
- **Problem solved:** Managing separate local credentials on every network device/AP doesn't scale or provide central control/audit.
- **Real-world use:** 802.1X backend, VPN authentication, Wi-Fi enterprise auth, network device admin login (paired with TACACS+ often for device admin specifically).
- **NE:** ✅ Essential — you'll point switches/WLCs/VPN concentrators at a RADIUS server constantly.
- **Sec:** ✅ Essential — shared secret management, RADIUS attribute-based authorization (VLAN assignment on successful auth), auditing failed auth attempts.
- **Free:** ⚠️ Medium-High — relevant once a client wants centralized Wi-Fi/VPN auth (e.g., via NPS on Windows Server, or cloud RADIUS).
- **Config relevance:** Shared secrets, RADIUS attributes (e.g., Tunnel-Private-Group-ID for dynamic VLAN assignment), accounting configuration.
- **Troubleshooting relevance:** Shared secret mismatches, UDP packet loss (RADIUS is UDP — a lossy link causes intermittent auth failures), server timeout/failover config.
- **Security relevance:** Legacy RADIUS uses weak MD5-based obfuscation for the shared secret (not full encryption of the packet) — know this limitation; RadSec (RADIUS over TLS) addresses it.
- **Priority:** Essential.
- **Notes:** UDP 1812 (auth), UDP 1813 (accounting) — legacy ports 1645/1646 still seen.

### TACACS+ (Terminal Access Controller Access-Control System Plus)
- **Purpose:** Cisco-originated (now open, RFC 8907) AAA protocol, primarily for **device administration** (not network access like RADIUS).
- **Problem solved:** Separates authentication, authorization, and accounting more granularly than RADIUS, and encrypts the entire packet body — better suited to controlling exactly which commands an admin can run on network gear.
- **Real-world use:** Enterprise network device admin AAA (who can log into this router, and what commands can they run) — very common in larger, security-mature enterprises.
- **NE:** ✅ High — you'll configure device access control against a TACACS+ server in mature enterprise shops.
- **Sec:** ✅ High — command-level authorization logging is a strong audit control (who ran `no shutdown` on which interface, when).
- **Free:** ➖ Low-Medium — mostly relevant in larger environments, rare in small SMB.
- **Config relevance:** Per-command authorization levels, accounting for command logging.
- **Troubleshooting relevance:** Server unreachable lockouts (always keep a local fallback account!), authorization denials for legitimate commands.
- **Security relevance:** Full packet encryption (unlike RADIUS's partial encryption) and command-level accounting make it the stronger choice specifically for device administration.
- **Priority:** High.
- **Notes:** TCP 49.

### LDAP (Lightweight Directory Access Protocol)
- **Purpose:** Queries and modifies directory service information (users, groups, computers).
- **Problem solved:** Provides a standard way for applications to look up identity/directory data instead of each app maintaining its own user database.
- **Real-world use:** Active Directory (Microsoft's directory service speaks LDAP), authentication backends for countless enterprise apps, VPNs, Wi-Fi, printers, SSO systems.
- **NE:** ⚠️ Medium-High — you'll integrate network devices (Wi-Fi, VPN) against LDAP/AD for auth.
- **Sec:** ✅ Essential — LDAP is central to Active Directory attacks (enumeration, Kerberoasting reconnaissance, LDAP injection); AD security is one of the highest-value security domains to know deeply.
- **Free:** ⚠️ Medium-High — setting up/integrating AD for SMB clients is common.
- **Config relevance:** Bind accounts, search base/filters, integrating third-party apps/devices with AD via LDAP.
- **Troubleshooting relevance:** Bind failures, search scope misconfiguration, referral issues across domains.
- **Security relevance:** Unencrypted LDAP is a credential-sniffing risk (use LDAPS), LDAP injection in poorly written apps, anonymous bind misconfiguration exposing directory data.
- **Priority:** Essential (Sec) / High (NE, Free).
- **Notes:** TCP 389 (plaintext, or StartTLS-upgradable), TCP 636 (LDAPS, implicit TLS).

### LDAPS (LDAP over SSL/TLS)
- **Purpose:** Encrypted LDAP.
- **Problem solved:** Plaintext LDAP exposes bind credentials and directory data on the wire.
- **Real-world use:** Should be the default for any production LDAP integration.
- **NE:** ✅ High.
- **Sec:** ✅ Essential — enforcing LDAPS (or StartTLS) instead of plaintext LDAP is a standard hardening recommendation you'll make repeatedly.
- **Free:** ✅ High.
- **Config relevance:** Certificate deployment on the directory server, client trust of that cert.
- **Troubleshooting relevance:** Cert trust failures, port confusion (636 vs 389).
- **Security relevance:** Directly prevents credential sniffing during directory binds.
- **Priority:** High.
- **Notes:** TCP 636.

### Kerberos
- **Purpose:** Ticket-based network authentication protocol — proves identity without repeatedly sending passwords over the network.
- **Problem solved:** Sending passwords (even hashed) across the network for every authentication is risky; Kerberos uses time-limited tickets issued by a trusted third party (KDC).
- **Real-world use:** The default authentication protocol in Active Directory environments (and many Unix/Linux enterprise environments via MIT Kerberos).
- **NE:** ⚠️ Medium — you mostly need to ensure NTP sync (Kerberos is extremely time-sensitive — >5 min skew breaks it) and that required ports are open.
- **Sec:** ✅ Essential — Kerberos attacks (Kerberoasting, Golden/Silver Ticket, Pass-the-Ticket, AS-REP Roasting) are some of the most important Active Directory attack techniques in modern security engineering/red-blue teaming.
- **Free:** ⚠️ Low-Medium — mostly relevant if managing AD environments for clients.
- **Config relevance:** Mostly automatic within AD, but you should understand SPNs (Service Principal Names), ticket lifetimes.
- **Troubleshooting relevance:** Clock skew (the #1 Kerberos failure cause), SPN duplication/misconfiguration.
- **Security relevance:** Deep, ongoing relevance in AD security assessments — this is a must-know-well topic for a Security Engineer specifically.
- **Priority:** Essential (Sec) / Medium (NE).
- **Notes:** TCP/UDP 88.

### SMB (Server Message Block)
- **Purpose:** File/printer sharing and inter-process communication protocol, primarily in Windows environments.
- **Problem solved:** Provides a network filesystem/sharing layer so users and applications can access shared resources transparently.
- **Real-world use:** Windows file shares, print servers, and — critically — one of the most heavily attacked/abused protocols in enterprise environments (WannaCry/EternalBlue, ransomware lateral movement, pass-the-hash relaying).
- **NE:** ⚠️ Medium — file share connectivity troubleshooting.
- **Sec:** ✅ Essential — SMB is central to lateral movement in nearly every enterprise ransomware/APT case study; you must know SMB relay attacks, SMBv1 deprecation, signing requirements.
- **Free:** ⚠️ Medium-High — setting up/troubleshooting Windows file shares for SMB(business) clients is common.
- **Config relevance:** Disable SMBv1 entirely, enable SMB signing, restrict share permissions.
- **Troubleshooting relevance:** Access denied errors, share permission vs NTFS permission conflicts, SMB version negotiation issues.
- **Security relevance:** SMB relay attacks, EternalBlue-class vulnerabilities, ransomware lateral movement vector — a top priority to lock down (disable SMBv1, require signing, segment access).
- **Priority:** Essential (Sec) / Medium-High (NE, Free).
- **Notes:** TCP 445 (modern, direct over TCP), historically also NetBIOS ports 137-139.


---

## TIER 10 — Network Monitoring and Management Protocols

### NetFlow (and sFlow, J-Flow as vendor variants)
- **Purpose:** Records metadata about traffic flows (source/dest IP/port, protocol, bytes, packets, timestamps) traversing a device — not full packet capture, but flow-level visibility.
- **Problem solved:** Full packet capture doesn't scale for continuous, network-wide visibility; flow records give you "who talked to whom, how much, when" cheaply.
- **Real-world use:** Bandwidth analysis, capacity planning, and — very importantly — security investigations (identifying C2 beaconing, data exfiltration patterns, lateral movement) when full PCAP isn't available.
- **NE:** ✅ High — capacity planning, top-talkers analysis, troubleshooting congestion.
- **Sec:** ✅ Essential — flow data is often your *only* historical visibility into an incident when packet captures weren't running; NetFlow analysis is a core SOC/IR skill.
- **Free:** ⚠️ Medium — valuable but often skipped in small SMB due to lack of collector infrastructure; good upsell for security-conscious clients.
- **Config relevance:** Enabling flow export on routers/switches/firewalls, pointing to a collector (e.g., a SIEM or dedicated flow analyzer).
- **Troubleshooting relevance:** Identifying top talkers, unexpected traffic patterns, bandwidth hogs.
- **Security relevance:** Beaconing detection, exfiltration volume analysis, lateral movement mapping, retrospective investigation when logs are gone.
- **Priority:** Essential (Sec) / High (NE) / Medium (Free).
- **Notes:** Cisco NetFlow v5/v9 are common; v9 is template-based/flexible. Vendor-neutral variant: IPFIX (below).

### IPFIX (IP Flow Information Export)
- **Purpose:** The IETF-standardized, vendor-neutral evolution of NetFlow v9.
- **Problem solved:** NetFlow was Cisco-proprietary; IPFIX standardizes flow export so multi-vendor environments (and modern cloud flow logs) can interoperate.
- **Real-world use:** Multi-vendor flow collection, and it's the underlying model that cloud flow logs (AWS VPC Flow Logs, Azure NSG Flow Logs) conceptually mirror.
- **NE:** ⚠️ Medium-High — relevant in multi-vendor and cloud-hybrid environments.
- **Sec:** ✅ High — same investigative value as NetFlow, standardized across more platforms including cloud.
- **Free:** ⚠️ Medium.
- **Config relevance:** Template-based export configuration, collector setup.
- **Troubleshooting relevance:** Same as NetFlow — traffic pattern analysis.
- **Security relevance:** Same as NetFlow — flow-based detection and investigation, now extending naturally into cloud VPC/NSG flow log analysis.
- **Priority:** High.
- **Notes:** RFC 7011, standard export port UDP/TCP 4739 (implementation-dependent), based on NetFlow v9 architecture.

*(SNMP and Syslog, also core to monitoring/management, are covered in Tier 3 above — don't treat them as separate "later" learning; they belong in your first pass.)*

---

## TIER 11 — VPN Protocols

### WireGuard
- **Purpose:** Modern, minimal, high-performance VPN protocol.
- **Problem solved:** Legacy VPN protocols (IPsec, OpenVPN) are complex to configure and audit; WireGuard is a small, modern codebase using state-of-the-art cryptography (Curve25519, ChaCha20, Poly1305) with a tiny, auditable attack surface.
- **Real-world use:** Rapidly growing adoption — cloud provider VPN offerings, modern remote-access solutions, site-to-site links for performance-sensitive use cases, many commercial VPN products now built on it.
- **NE:** ✅ High and rising — increasingly the default recommendation for new VPN deployments.
- **Sec:** ✅ High — simple, modern cryptography is easier to reason about/audit than legacy IKE/IPsec stacks, but note it lacks some enterprise AAA integration (no native RADIUS/802.1X-style user auth — it's key-based, so key distribution/revocation process matters).
- **Free:** ✅ High — a great, low-overhead VPN solution for SMB remote access and site-to-site links.
- **Config relevance:** Public/private key pair generation per peer, simple config file (`[Interface]`/`[Peer]` sections), allowed IPs (defines routing/split-tunnel behavior).
- **Troubleshooting relevance:** Key mismatches, allowed-IPs misconfiguration (most common issue — controls both routing AND acts as a packet filter), NAT/firewall UDP port issues.
- **Security relevance:** Strong modern crypto by default, small attack surface — but no built-in user-revocation-by-username (you revoke by removing a key), so key lifecycle management is your responsibility.
- **Priority:** High.
- **Notes:** UDP, typically port 51820 (configurable).

### OpenVPN
- **Purpose:** Mature, highly flexible, widely supported open-source VPN protocol/software.
- **Problem solved:** Provides configurable, certificate or PSK-based encrypted tunnels across almost any network condition (including restrictive firewalls, since it can run over TCP 443 and look like HTTPS).
- **Real-world use:** Still extremely common — pfSense/OPNsense deployments, commercial VPN services, remote-access VPNs for SMB and enterprise alike.
- **NE:** ✅ High — very commonly deployed, especially in SMB/mid-market firewalls.
- **Sec:** ⚠️ High — PKI management (client certs), cipher/config hardening (avoid outdated defaults), understanding TLS-based control channel plus a separate data channel.
- **Free:** ✅ Essential — one of the most common freelance/SMB VPN deployments (pfSense + OpenVPN is a very standard stack).
- **Config relevance:** Server/client config files, certificate authority setup for client certs, routing (tunnel-all vs split-tunnel), TLS-auth/tls-crypt hardening.
- **Troubleshooting relevance:** Cert issues, routing table conflicts, MTU/fragmentation over the tunnel, TCP-over-TCP performance issues if run over TCP.
- **Security relevance:** PKI hygiene (revoking lost/compromised client certs via CRL), config hardening against known weak defaults.
- **Priority:** Essential (Free) / High (NE, Sec).
- **Notes:** Default UDP 1194 (configurable, can run on TCP 443 for firewall-evasion/restrictive-network scenarios).

*(IPsec/IKEv2 — the third major VPN protocol family — is covered in depth in Tier 8 above.)*


---

## TIER 12 — Cloud Networking Protocols/Technologies

Cloud networking isn't really a new protocol stack — it's the same fundamentals (IP, TCP/UDP, DNS, TLS, BGP, VXLAN) applied through provider-specific abstractions. What you need is fluency in how those abstractions map to what you already know.

### VXLAN / EVPN
- **Purpose:** VXLAN (Virtual Extensible LAN) tunnels L2 Ethernet frames over an L3 IP network; EVPN (Ethernet VPN) is the modern control plane (BGP-based) that makes VXLAN scalable and manageable.
- **Problem solved:** Traditional VLANs are capped at 4094 IDs and don't scale across L3 boundaries (e.g., between data centers or in massive multi-tenant cloud/DC fabrics); VXLAN provides 16 million logical segments (24-bit VNI) tunneled over any routed IP network.
- **Real-world use:** Modern data center fabrics (spine-leaf architectures), cloud provider underlays, multi-tenant hosting, NSX/ACI-style SDN data centers.
- **NE:** ✅ High (data center/cloud infra roles) — Essential if you move toward DC/cloud network engineering specifically.
- **Sec:** ⚠️ Medium-High — understanding tenant isolation boundaries in VXLAN/EVPN fabrics matters for multi-tenant security assessments.
- **Free:** ➖ Low — rarely relevant to SMB-scale freelance work; this is data-center/large-enterprise territory.
- **Config relevance:** VNI assignment, VTEP (VXLAN Tunnel Endpoint) configuration, EVPN BGP address-family setup.
- **Troubleshooting relevance:** VTEP reachability, VNI mapping errors, MTU (VXLAN adds ~50 bytes overhead — a very common real-world MTU/fragmentation bug).
- **Security relevance:** Multi-tenant segmentation correctness, VNI isolation verification.
- **Priority:** High (specialized DC/cloud track) / Low (general SMB).
- **Notes:** UDP 4789 (VXLAN encapsulation).

### SD-WAN
- **Purpose:** Software-defined approach to WAN connectivity — abstracts and centrally manages multiple underlying transport links (MPLS, broadband, LTE/5G) with policy-based, application-aware routing.
- **Problem solved:** Traditional WAN (MPLS-only) is expensive and inflexible; SD-WAN lets enterprises use cheaper broadband/internet links intelligently while maintaining performance/security policy centrally.
- **Real-world use:** Multi-site enterprises connecting branch offices, replacing or augmenting MPLS with broadband+LTE hybrid links, integrated with cloud security (SASE architectures).
- **NE:** ✅ High and rising — a major modern enterprise WAN skill (Cisco Viptela/Meraki, VMware VeloCloud, Fortinet, Palo Alto Prisma SD-WAN are common platforms).
- **Sec:** ✅ High — SD-WAN is increasingly bundled with security (SASE — Secure Access Service Edge), so understanding the security policy layer (not just routing) matters.
- **Free:** ⚠️ Medium — larger SMB/multi-site clients increasingly want this instead of traditional site-to-site VPN mesh.
- **Config relevance:** Overlay tunnel configuration (usually IPsec-based under the hood), application-aware path selection policies, centralized orchestrator management.
- **Troubleshooting relevance:** Underlying transport link issues manifesting as SD-WAN policy failures, orchestrator connectivity.
- **Security relevance:** Policy misconfiguration exposing traffic to the wrong path/security posture; SASE integration security.
- **Priority:** High.
- **Notes:** Vendor-specific implementations; conceptually builds on IPsec/GRE tunnels with a centralized SDN control plane.

### Cloud Networking Constructs (AWS/Azure/GCP — conceptual, not a single "protocol")
- **What this covers:** VPC/VNet design, subnets, route tables, security groups/NSGs (stateful L3/L4 filtering), NACLs (stateless), Transit Gateway/VNet peering/VPC peering, VPN Gateways (IPsec-based), Direct Connect/ExpressRoute (private L2/L3 links to cloud), cloud load balancers, cloud DNS (Route53/Azure DNS/Cloud DNS), flow logs.
- **Problem solved:** Translates traditional on-prem networking concepts into API-driven, software-defined cloud infrastructure.
- **Real-world use:** Any modern enterprise with hybrid or cloud-native infrastructure — which is nearly all of them today.
- **NE:** ✅ Essential (increasingly, regardless of specialization) — cloud networking is now baseline enterprise NE knowledge.
- **Sec:** ✅ Essential — security groups/NSG misconfiguration (overly permissive rules, "0.0.0.0/0 allow all") is one of the most common real-world cloud breach root causes; IAM-network intersection matters a lot here too.
- **Free:** ✅ High and rising — clients increasingly run infrastructure (partially or fully) in the cloud, and freelancers who can bridge on-prem + cloud networking are more valuable.
- **Config relevance:** Security group/NSG rules, route table design, peering, VPN/Direct Connect setup — all via console/CLI/IaC (Terraform).
- **Troubleshooting relevance:** Misrouted traffic between VPCs/subnets, security group vs NACL confusion, DNS resolution across peered/hybrid networks.
- **Security relevance:** The #1 practical cloud security skill — auditing and correctly scoping security groups/NSGs/IAM is enormously high-value.
- **Priority:** Essential.
- **Notes:** Not literally "protocols" but essential modern context — the underlying traffic is still IP/TCP/UDP/TLS/BGP (cloud providers use BGP extensively for Direct Connect/ExpressRoute and their own backbone).

### GRE (Generic Routing Encapsulation)
- **Purpose:** A simple tunneling protocol that encapsulates a wide variety of network layer protocols inside point-to-point IP tunnels.
- **Problem solved:** Provides a generic way to tunnel traffic (including non-IP or multicast/routing-protocol traffic) across an IP network — often used as the "carrier" tunnel that IPsec then encrypts (GRE-over-IPsec).
- **Real-world use:** Legacy and still-current site-to-site tunnels, carrying routing protocols or multicast across a provider network, DMVPN (Cisco's dynamic multipoint VPN, built on GRE + NHRP + IPsec), some SD-WAN underlay tunnels.
- **NE:** ✅ High — you'll encounter and configure this in enterprise WAN and DMVPN designs.
- **Sec:** ⚠️ Medium — GRE alone has **no encryption or authentication** (common misconception to correct with clients: "GRE is a tunnel, not a VPN" — it must be paired with IPsec for confidentiality).
- **Free:** ⚠️ Medium — mostly relevant if building multi-site tunnels for a client without full IPsec, or supporting DMVPN.
- **Config relevance:** Tunnel source/destination, tunnel interface IP addressing, MTU adjustment (GRE overhead reduces usable MTU by 24 bytes).
- **Troubleshooting relevance:** Tunnel flapping (source/dest reachability), MTU/fragmentation (a very frequent real-world GRE issue), routing protocol adjacency failures over the tunnel.
- **Security relevance:** No native encryption — must combine with IPsec if confidentiality is required; recon/attack surface if exposed without protection.
- **Priority:** High.
- **Notes:** IP protocol 47.

### MPLS (Multiprotocol Label Switching)
- **Purpose:** Label-based forwarding technology used primarily by service providers to fast-path traffic without full IP lookups at every hop, and to provide traffic engineering/VPN services (L2VPN/L3VPN).
- **Problem solved:** Efficient, scalable traffic forwarding and provider-based VPN service delivery (the traditional "MPLS WAN" enterprises buy from carriers) with QoS/traffic engineering.
- **Real-world use:** Still very common as the underlying enterprise WAN technology (though increasingly supplemented/replaced by SD-WAN + broadband), and universally used inside ISP/carrier cores.
- **NE:** ⚠️ Medium-High — mostly relevant if you work with/for a service provider, or manage enterprise WAN circuits that ride on MPLS (you'll interact with it at the CE-PE boundary even if you don't run the provider's core).
- **Sec:** ⚠️ Medium — MPLS VPNs provide traffic *separation* by default but are not encrypted — a common misconception to correct (an MPLS VPN circuit is not the same as an encrypted VPN).
- **Free:** ➖ Low — essentially never relevant to freelance/SMB work (this lives inside carrier/large-enterprise infrastructure).
- **Config relevance:** Mostly relevant at the CE (Customer Edge) router — BGP or static routing to the provider's PE (Provider Edge), QoS marking.
- **Troubleshooting relevance:** CE-PE routing adjacency issues, understanding that core MPLS troubleshooting is generally the provider's responsibility, not yours.
- **Security relevance:** No encryption by default — recommend IPsec overlay for sensitive traffic even across "private" MPLS circuits.
- **Priority:** Medium.
- **Notes:** Labels inserted between L2 and L3 headers; LDP/RSVP-TE distribute labels; largely a service-provider-operated technology from the enterprise customer's perspective.


---

## TIER 13 — Legacy Protocols (Understand Only — Don't Deep-Invest)

These show up in exams, old client infrastructure, or as "why is this insecure" audit findings. Know what they are, why they're deprecated, and what replaces them. Don't spend real study hours mastering their configuration.

| Protocol | What it was for | Why it's legacy | What replaced it | Depth needed |
|---|---|---|---|---|
| **Telnet** | Remote CLI access | Plaintext credentials/data | SSH | Know it, disable it, explain the risk. |
| **FTP** | File transfer | Plaintext credentials/data | SFTP/FTPS | Understand active/passive NAT behavior (real troubleshooting value); don't deploy new. |
| **RIP/RIPv1** | Simple IGP routing | Slow convergence, hop-count limit of 15, weak/no auth | OSPF/EIGRP | Understand distance-vector concepts; unlikely to configure in production. |
| **SSLv2/SSLv3, TLS 1.0/1.1** | Encrypted transport | Multiple known cryptographic breaks (POODLE, BEAST, etc.) | TLS 1.2/1.3 | Know they must be disabled everywhere; a standard hardening/audit item. |
| **WEP / WPA (TKIP)** | Wi-Fi encryption | Trivially crackable (WEP) / weak (TKIP) | WPA2/WPA3 (AES-CCMP/GCMP) | Know why they're broken; you'll flag them in wireless assessments. |
| **NetBIOS / WINS** | Legacy Windows name resolution | Replaced by DNS + Active Directory | DNS | Recognize it in old environments (ports 137-139); rarely configure new. |
| **SNMPv1/v2c (plaintext community strings)** | Device monitoring | No real authentication/encryption | SNMPv3 | Know to always recommend/migrate to v3; you'll still *see* v2c in the wild constantly. |
| **PPTP** | Early VPN protocol | Broken encryption (MS-CHAPv2 crackable) | IPsec/IKEv2, WireGuard, OpenVPN | Know it's insecure; never recommend it. |
| **X.25 / Frame Relay** | Legacy WAN circuit-switching/packet-switching | Replaced by IP/MPLS-based WAN | MPLS, internet-based WAN/SD-WAN | Historical awareness only — you will not encounter these in modern production networks. |

---

## TIER 14 — Advanced / Specialized Protocols to Learn Later

These matter once you specialize — data center engineer, ISP/carrier engineer, cloud network architect, or offensive/red-team security specialist. Don't front-load these; return to them once Tiers 1-12 are solid and your career direction narrows.

- **BGP FlowSpec / RPKI (ROV)** — advanced internet routing security, relevant for ISP/large-enterprise BGP operators.
- **VRRP / HSRP / GLBP** — first-hop router redundancy protocols; genuinely useful sooner than "advanced" if you're doing enterprise routing — worth pulling forward into Tier 2 study once comfortable with OSPF, since HA gateway design is common.
- **PIM / Multicast routing (IGMP, PIM-SM/DM)** — needed for video/voice/IPTV/financial market-data multicast environments.
- **Segment Routing (SR-MPLS, SRv6)** — the modern evolution of MPLS traffic engineering; relevant to carrier/large-DC roles.
- **802.1AE (MACsec)** — L2 encryption between switches; relevant in high-security campus/DC environments.
- **Zero Trust Network Access (ZTNA) architectures** — conceptual framework more than a single protocol; builds on TLS, mTLS, and identity-aware proxying — a natural "next step" after mastering 802.1X/RADIUS/IAM basics.
- **SASE (Secure Access Service Edge)** — architectural convergence of SD-WAN + cloud security; relevant once SD-WAN and cloud networking are solid.
- **BFD (Bidirectional Forwarding Detection)** — sub-second failure detection paired with routing protocols in high-availability designs.
- **DNS-over-HTTPS/TLS (DoH/DoT) at scale, DNSSEC** — deepen after core DNS is solid; important for both privacy design and detecting evasion.
- **Container/Kubernetes networking (CNI plugins, service mesh/mTLS, Istio/Linkerd)** — essential if your career trajectory moves toward cloud-native/DevSecOps.
- **Offensive protocol abuse in depth** (LLMNR/NBT-NS poisoning, Kerberoasting tooling, NTLM relay chains, mDNS/SSDP recon) — pull forward earlier if you're leaning specifically toward offensive security/red teaming rather than blue-team/defensive Security Engineering.


---

## The Five Verbs: Understand vs. Configure vs. Troubleshoot vs. Secure vs. Later

Not every protocol deserves the same *kind* of effort. Here's the honest breakdown so you don't burn hours configuring something you'll only ever need to recognize, or skim something you'll be paged about at 2am.

### Protocols you mainly need to **UNDERSTAND** (recognize, explain, reason about — rarely hands-on configure)
RIP, legacy SSL/TLS versions, WEP/WPA-TKIP, NetBIOS/WINS, PPTP, X.25/Frame Relay, MPLS core internals (you'll touch the CE edge, not the provider core), AH (the IPsec mode nobody uses).
→ *Why:* You'll meet these in legacy environments, audits, or certification exams — not in new deployments you build yourself.

### Protocols you must be able to **CONFIGURE** fluently, from memory, under pressure
Ethernet/VLAN/802.1Q, IPv4/IPv6 addressing & subnetting, STP/RSTP, LACP, OSPF, DHCP, DNS, NAT, SSH, TLS/certificate management, IPsec/IKEv2, WireGuard/OpenVPN, SNMP, Syslog, RADIUS/TACACS+, 802.1X, cloud VPC/security groups.
→ *Why:* These are what you'll actually build — client networks, enterprise infrastructure, VPNs — day one on the job.

### Protocols you must be excellent at **TROUBLESHOOTING** (even where you rarely configure them from scratch)
ARP, ICMP, TCP (packet capture analysis), FTP (active/passive+NAT), GRE (MTU/fragmentation), DHCP (scope/relay issues), DNS resolution chains, BGP peering states (if you touch multi-homing), Kerberos (clock skew).
→ *Why:* These generate the tickets. "It's a DNS/ARP/DHCP/clock problem" solves a shocking percentage of real-world outages.

### Protocols you must think about primarily through a **SECURITY** lens
SPF/DKIM/DMARC, Kerberos (attack techniques), SMB (lateral movement), LDAP/LDAPS, SNMP (community strings), Telnet/FTP (as findings, not deployments), TLS (cipher/cert hardening), DNS (tunneling/exfiltration/DNSSEC).
→ *Why:* Their configuration is often simple; their *misconfiguration* is where entire security careers are built and broken.

### Protocols you can genuinely **LEAVE FOR LATER**
Everything in Tier 14 (Segment Routing, MACsec, SASE architecture, BFD, container networking, BGP FlowSpec/RPKI, PIM multicast) plus RIPng, VRRP/HSRP (pull forward a bit sooner than "later," honestly — see note in Tier 14), IPFIX beyond a conceptual level.
→ *Why:* These require Tiers 1-12 as prerequisites and matter mainly once you specialize.


---

## Role-Based Priority Lists

### A. Network Engineer (routing/switching/infrastructure focus)
**Essential (learn first, master deeply):**
Ethernet, ARP, IPv4/subnetting, IPv6, ICMP, TCP/UDP, VLAN/802.1Q, STP/RSTP, LACP, OSPF, DHCP, DNS, NAT, NTP, SSH, TLS, IPsec/IKEv2.

**High priority (learn next):**
EIGRP (if Cisco-heavy), BGP (if multi-homed/ISP-adjacent), SNMP, Syslog, SFTP/SCP, GRE, WireGuard/OpenVPN, cloud VPC/routing constructs, RADIUS/TACACS+, VRRP/HSRP.

**Medium (situational, learn as needed):**
FTP (for NAT troubleshooting literacy), SD-WAN, MPLS (CE-edge level), VXLAN/EVPN (if DC-track), 802.1X.

**Low/legacy-awareness only:**
RIP, Telnet, PPTP, WEP/WPA-TKIP, Frame Relay/X.25.

### B. Security Engineer (defense/detection/hardening focus)
**Essential:**
TCP/UDP/IP fundamentals (for packet analysis), ARP (spoofing/DAI), TLS (deep), IPsec/IKEv2, DNS (attacks + DNSSEC), SPF/DKIM/DMARC, Kerberos (attack techniques), SMB (lateral movement), LDAP/LDAPS, RADIUS/TACACS+, 802.1X, SNMP (hardening), Syslog (SIEM), NetFlow/IPFIX, SSH (hardening + tunneling abuse), cloud security groups/IAM-network intersection.

**High priority:**
OSPF/BGP (route authentication/hijacking awareness), VLAN hopping, STP attacks (BPDU spoofing), SMTP/IMAP (BEC investigation), WireGuard/OpenVPN (key/PKI hygiene).

**Medium:**
QUIC/HTTP3 (inspection blind spots), WebSocket (inspection blind spots), MPLS/GRE (as unencrypted transport misconceptions to correct).

**Low/legacy-awareness (know as findings, not deployments):**
Telnet, FTP, SNMPv1/v2c, PPTP, WEP/WPA-TKIP, SSLv2/v3/TLS1.0/1.1.

### C. Freelance / SMB IT-Networking Technician
**Essential:**
Ethernet, ARP, IPv4/subnetting, DHCP, DNS, NAT, SSH, TLS/HTTPS, VLAN (guest/internal separation), STP (basic), SPF/DKIM/DMARC (email setup is a constant client request), WireGuard/OpenVPN (site-to-site/remote access is a top freelance request), SFTP.

**High priority:**
IPv6 (growing ISP requirement), SNMP (once managing multiple devices), Syslog (basic centralized logging), RADIUS (Wi-Fi/VPN auth for clients who want it), LACP, cloud VPC/security groups (client cloud migrations).

**Medium:**
OSPF (multi-router client sites), 802.1X (security-conscious client upsell), SD-WAN (multi-site clients), IPsec site-to-site.

**Low:**
BGP, EIGRP, MPLS, VXLAN/EVPN, TACACS+ — essentially never needed at SMB scale.

### D. Combined Network Engineer + Security Engineer (your actual target path)
This is the union of A and B, prioritized by how often the combination matters in real hybrid roles:

**Tier 1 (absolute bedrock — learn together, they reinforce each other):**
Ethernet, ARP, IPv4/IPv6, ICMP, TCP/UDP, VLAN/802.1Q, STP/RSTP, DHCP, DNS, NAT, NTP, SSH, TLS.

**Tier 2 (core infrastructure + its security implications, learned as pairs):**
OSPF (+ route auth/filtering), IPsec/IKEv2 (+ cipher hardening), 802.1X (+ EAP method security), RADIUS/TACACS+ (+ shared-secret/encryption limitations), SNMP (+ v3 vs v1/2c), Syslog (+ SIEM/forensics), LDAP/LDAPS (+ AD attack surface), Kerberos (+ Kerberoasting/Golden Ticket).

**Tier 3 (email + web security, high real-world attack relevance):**
SPF/DKIM/DMARC, SMTP/IMAP (BEC), HTTP/HTTPS, WebSocket/QUIC (inspection implications).

**Tier 4 (specialize based on which direction you lean — ISP/DC vs SMB/enterprise generalist):**
BGP + RPKI/hijacking (ISP/large enterprise lean), VXLAN/EVPN + SD-WAN (DC/cloud lean), or deepen WireGuard/OpenVPN + cloud VPC/security groups (SMB/generalist + cloud-security lean).

**Tier 5 (legacy literacy — audit/exam knowledge, not deployment skill):**
RIP, Telnet, FTP, SNMPv1/v2c, PPTP, WEP/TKIP.


---

## Recommended Learning Sequence: Beginner → Advanced

This sequence is designed so each stage gives you the *tools* to understand the next stage. Don't jump ahead to routing protocols before subnetting is automatic, and don't jump to security-specific attacks before you understand the protocol being attacked.

### Stage 0 — Physical/Data-Link Foundation (Weeks 1-3)
**Learn:** Ethernet framing, switching concepts, MAC addressing, ARP.
**Why first:** Nothing above this makes sense without understanding how two devices on the same wire actually talk. ARP is the first "aha" moment connecting L2 and L3.

```
[PC-A]---(switch port)---[Switch]---(switch port)---[PC-B]
   |  MAC: AA:AA:AA         |            MAC: BB:BB:BB  |
   |------ ARP: "Who has 192.168.1.20?" -------------->|
   |<----- ARP Reply: "192.168.1.20 is BB:BB:BB" -------|
   |------ Ethernet frame (dst=BB:BB:BB) -------------->|
```

### Stage 1 — IP Addressing and Core Transport (Weeks 3-8)
**Learn:** IPv4 addressing/subnetting (practice until instant), IPv6 basics, ICMP, TCP, UDP.
**Why now:** Subnetting fluency is the single most load-bearing skill in networking — every VLAN, ACL, route, and firewall rule depends on it. TCP/UDP mechanics are required before troubleshooting *anything* application-layer.
**Milestone check:** You should be able to subnet a /24 into eight /27s in your head, and explain a TCP 3-way handshake while looking at a Wireshark capture.

### Stage 2 — Local Network Services (Weeks 8-12)
**Learn:** DHCP, DNS, NAT, NTP, VLAN/802.1Q, STP/RSTP, LACP.
**Why now:** This is what makes a LAN a *usable* network instead of a collection of wired cables. This stage alone qualifies you for basic SMB/freelance work.
**Milestone check:** Build a small lab (GNS3/Packet Tracer/EVE-NG or real gear) with 2 VLANs, DHCP scopes for each, inter-VLAN routing, and a redundant switch link running RSTP.

### Stage 3 — Remote Access and Encryption Basics (Weeks 12-16)
**Learn:** SSH (deep), TLS (deep — this is a career-long investment starting now), HTTPS, SFTP/SCP.
**Why now:** You need secure remote access and an understanding of TLS *before* touching VPNs, since VPNs build directly on these concepts (and TLS understanding is required almost everywhere in security work).

```
Client                                    Server
  |---- ClientHello (ciphers, TLS ver) --->|
  |<--- ServerHello + Certificate ---------|
  |  (validate cert chain to trusted CA)   |
  |---- Key exchange, Finished ----------->|
  |<--- Finished ---------------------------|
  |======= Encrypted Application Data ======|
```

### Stage 4 — Enterprise Routing (Weeks 16-24)
**Learn:** OSPF (deeply), EIGRP (if Cisco-focused), static/default routing interplay, basic BGP concepts.
**Why now:** With L2/L3 fundamentals and services solid, you're ready for dynamic routing — the core "Network Engineer" identity skill.
**Milestone check:** Build a 3-router OSPF lab across 2 areas, break something intentionally (mismatched MTU or area ID), and fix it using only `show ip ospf neighbor` output.

### Stage 5 — Security Fundamentals Layered on Top (Weeks 20-30, overlapping Stage 4)
**Learn:** ARP spoofing + DAI, VLAN hopping + mitigations, SPF/DKIM/DMARC, SNMP hardening (v3), Syslog centralization, RADIUS/TACACS+, 802.1X.
**Why now:** You now have enough infrastructure knowledge to understand *what's being attacked* — security concepts land far better once you've configured the thing being secured.

### Stage 6 — VPNs and Site Interconnection (Weeks 26-34)
**Learn:** IPsec/IKEv2 (deeply), WireGuard, OpenVPN, GRE, NAT-T concepts.
**Why now:** This combines everything so far — routing, TLS/crypto concepts, NAT — into practical site-to-site and remote-access deployments, which is one of the most requested freelance/SMB and enterprise skills.

```
   Site A (192.168.1.0/24)              Site B (192.168.2.0/24)
        [Router A]======IPsec Tunnel======[Router B]
   IKE Phase 1: authenticate peers, build secure channel
   IKE Phase 2: negotiate ESP SAs for actual traffic
   Result: 192.168.1.0/24 <--encrypted--> 192.168.2.0/24
```

### Stage 7 — Identity, Directory, and AD-Adjacent Security (Weeks 32-42)
**Learn:** LDAP/LDAPS, Kerberos (+ common attack techniques), SMB security, deeper RADIUS/802.1X integration.
**Why now:** This is where "Security Engineer" identity really sharpens — Active Directory security is one of the highest-value, highest-demand security skill areas, and it requires the directory/auth fundamentals from Stage 5-6 as prerequisites.

### Stage 8 — Monitoring, Detection, and Investigation (Weeks 38-46, overlapping Stage 7)
**Learn:** NetFlow/IPFIX, deeper Syslog/SIEM correlation, DNS security (tunneling detection, DNSSEC), TLS inspection trade-offs.
**Why now:** You now have enough breadth across the network to meaningfully *investigate* incidents rather than just configure devices — this is the blue-team/SOC-adjacent skill set that differentiates a combined NE+Sec profile.

### Stage 9 — Cloud and Modern WAN (Weeks 42-52)
**Learn:** Cloud VPC/VNet networking, security groups/NSGs, SD-WAN concepts, QUIC/HTTP3 implications, BGP for cloud connectivity (Direct Connect/ExpressRoute context).
**Why now:** Cloud networking is now a baseline expectation, but it's genuinely easier to learn *after* on-prem fundamentals are solid — cloud abstractions map onto concepts you already know (route tables = routing, security groups = stateful ACLs).

### Stage 10 — Specialize (Year 2+)
**Choose your lean and go deep:**
- **ISP/Service Provider lean:** BGP mastery, RPKI/ROV, MPLS, Segment Routing.
- **Data Center/Cloud Architect lean:** VXLAN/EVPN, spine-leaf design, container/Kubernetes networking, service mesh mTLS.
- **Offensive Security lean:** Active Directory attack chains in depth, protocol abuse (LLMNR/NBT-NS poisoning, NTLM relay), red team infrastructure.
- **Defensive/Blue Team + Zero Trust lean:** SASE, ZTNA architectures, deep SIEM/detection engineering, MACsec, advanced DNS security.

---

## Quick-Reference: What to Build in Your Home Lab at Each Stage

1. **Stage 0-2:** Two VLANs, a DHCP server, inter-VLAN routing, one redundant switch link with RSTP.
2. **Stage 3:** An SSH-hardened Linux box (key-only auth, fail2ban) and a self-signed/Let's Encrypt HTTPS site to inspect with Wireshark.
3. **Stage 4-5:** A 3+ router OSPF topology with a RADIUS server (FreeRADIUS or Windows NPS) doing 802.1X on at least one switch port.
4. **Stage 6:** A real site-to-site IPsec tunnel between two virtual routers/firewalls (pfSense/OPNsense/Cisco CSR in GNS3), plus a WireGuard remote-access setup.
5. **Stage 7-8:** A small Active Directory domain (2-3 VMs) with centralized Syslog/SIEM (e.g., a free ELK or Wazuh stack) ingesting logs from your lab devices, and practice basic Kerberoasting/AD attack detection in an isolated lab (never against systems you don't own).
6. **Stage 9:** A free-tier AWS/Azure VPC with subnets, route tables, security groups, and a site-to-site VPN back to your home lab.

---

*This guide is meant to be a living reference — revisit the tier tables as checklists, and use the learning sequence as your actual study roadmap rather than trying to absorb everything at once.*
