# Networking protocol roadmap

For a combined **Network Engineering + Security Engineering** career, do not try to memorize protocol names or port numbers in isolation. Your practical goal is to be able to:

```text
Design → Configure → Verify → Troubleshoot → Monitor → Secure → Document
```

A useful enterprise model is:

```text
Users ── Access switches ── Distribution/core ── Edge router/firewall ── ISP/cloud
  │             │                    │                    │
802.1X        VLAN/STP             OSPF/BGP              NAT/IPsec
DHCP/DNS      LACP                 ACLs                  TLS/VPN
```

The protocol priorities below reflect modern enterprise networks, security operations, cloud infrastructure, and freelance/SMB work. Standards and vendor implementations vary, so always verify behavior against current platform documentation. For example, OSPF is a link-state protocol designed for use within an autonomous system, while BGP exchanges reachability and AS-path information between BGP systems. [datatracker.ietf](https://datatracker.ietf.org/doc/html/rfc2328)

***

## How to read priorities

- **Essential:** You should configure and troubleshoot it confidently.
- **High:** You should understand it deeply and configure it in common deployments.
- **Medium:** You should understand it and troubleshoot common failures; configuration depends on your role.
- **Low:** Learn the purpose, packet behavior, and security implications; defer detailed implementation.

### Practical labels

- **Configure:** Build or change it on equipment.
- **Troubleshoot:** Diagnose failures with CLI tools, packet captures, and logs.
- **Secure:** Harden it, restrict it, monitor it, and understand abuse cases.
- **Understand:** Know its behavior and recognize it in captures or incidents.
- **Later:** Do not spend early study time on it.

***

# 1. Must-master protocols

These are the foundation of every other tier.

| Protocol or technology | Full name and purpose | What problem it solves / real-world use | Network engineer | Security engineer | Freelance/SMB | Configuration | Troubleshooting | Security | Priority |
|---|---|---|---|---|---|---|---|---|---|
| Ethernet / IEEE 802.3 | Wired LAN framing and signaling | Connects hosts, switches, routers, cameras, phones, and APs; used everywhere in enterprise and SMB networks | Critical | High | Critical | Configure speed, duplex, MTU, trunks, interfaces | Link, CRC, duplex, MTU, errors, loops | MAC spoofing, rogue devices, VLAN attacks | Essential |
| MAC addressing | Layer-2 hardware addressing | Lets switches deliver frames to the correct interface | Critical | High | Critical | Usually learned automatically; configure static entries only when needed | MAC table, flapping, unknown unicast, CAM exhaustion | Spoofing, flooding, port security | Essential |
| ARP | Address Resolution Protocol | Maps IPv4 addresses to MAC addresses on a local network | Critical | Critical | Critical | Static ARP only in special cases; inspect ARP caches | Duplicate IPs, stale ARP, gateway resolution | ARP spoofing, poisoning, MITM | Essential |
| IPv4 | Internet Protocol version 4 | Provides logical addressing and routing | Critical | Critical | Critical | Subnets, gateways, routes, DHCP, ACLs, NAT | Addressing, masks, routes, fragmentation, TTL | Spoofing, scanning, exposed services | Essential |
| IPv6 | Internet Protocol version 6 | Expands address space and supports modern IP networking | Critical | Critical | High | Address plans, RA, DHCPv6, OSPFv3/IS-IS, ACLs | Neighbor Discovery, RA, routes, PMTUD, dual stack | Rogue RA, extension headers, exposed services | Essential |
| ICMP / ICMPv6 | Internet Control Message Protocol | Error reporting, diagnostics, reachability, path MTU, time exceeded | Critical | Critical | Critical | Permit appropriate types; do not blindly block it | `ping`, `traceroute`, unreachable, PMTU | Abuse, covert channels, reconnaissance; filtering must be selective | Essential |
| TCP | Transmission Control Protocol | Reliable, ordered, connection-oriented transport | Critical | Critical | Critical | Firewall rules, timers, MSS, load balancers | SYN/SYN-ACK, resets, retransmissions, windows, MTU | SYN floods, session hijacking, exposed ports | Essential |
| UDP | User Datagram Protocol | Lightweight connectionless transport | Critical | Critical | Critical | Firewall rules, QoS, service ports | Loss, reordering, NAT, MTU, rate limits | Amplification, spoofing, floods | Essential |
| Subnetting / CIDR | Classless Inter-Domain Routing | Divides address space and controls route aggregation | Critical | Critical | Critical | IP plans, summaries, ACLs, cloud subnets | Overlap, wrong mask, route selection | Limits blast radius and exposed scope | Essential |
| VLAN / 802.1Q | Virtual LAN tagging standard | Separates broadcast domains over shared switching infrastructure | Critical | Critical | Critical | Access/trunk ports, native VLAN, allowed VLANs, SVIs | Tag mismatch, VLAN pruning, native VLAN, DHCP failure | Segmentation, VLAN hopping, trunk abuse | Essential |
| STP / RSTP / MSTP | Spanning Tree Protocol variants | Prevents Layer-2 loops while preserving redundancy | Critical | High | High | Root bridge, port roles, edge ports, BPDU Guard, MST regions | Root changes, blocked ports, loops, BPDU loss | BPDU attacks, rogue switch, topology manipulation | Essential |
| LACP | Link Aggregation Control Protocol, IEEE 802.1AX | Combines links into one logical bundle for capacity and redundancy | Critical | Medium | High | LAG mode, hashing, member compatibility | Members suspended, mismatch, hashing imbalance | Rogue negotiation or misconfigured aggregation | High |

Ethernet uses frames, MAC addresses, EtherTypes, and usually an FCS. VLAN tagging adds an 802.1Q field to an Ethernet frame. ARP uses request/reply messages, normally within a broadcast domain; ARP does not cross routers.

### Six dimensions for the foundation

| Dimension | What you need to know |
|---|---|
| Purpose | Ethernet moves frames locally; IP moves packets between networks; TCP/UDP provide transport; ICMP reports network conditions |
| How it works | Switches learn source MACs; routers select paths using destination IPs; TCP establishes state with a handshake; UDP sends datagrams without a handshake |
| Frame/packet structure | Ethernet header/trailer, optional 802.1Q tag, IPv4/IPv6 header, TCP/UDP header, payload |
| Ports/addressing | MAC addresses at Layer 2; IPv4/IPv6 addresses at Layer 3; TCP/UDP ports at Layer 4 |
| Configuration | VLANs, trunks, SVIs, IP addresses, routes, ACLs, interface settings, MTU, LAGs |
| Troubleshooting | Start at Layer 1, then VLAN/MAC, ARP/ND, IP route, transport port, application, and policy |

A practical troubleshooting sequence:

```text
Cable/link
  ↓
Interface state and errors
  ↓
VLAN / trunk / MAC table
  ↓
ARP or IPv6 Neighbor Discovery
  ↓
IP address and route
  ↓
TCP/UDP port
  ↓
Application, DNS, TLS, firewall, authentication
```

***

# 2. Enterprise routing and switching

| Protocol / technology | Purpose and real-world use | What you need to do | Network engineering importance | Security importance | SMB relevance | Config / troubleshoot / secure | Priority |
|---|---|---|---|---|---|---|---|
| OSPF / OSPFv2 | Link-state interior gateway protocol for IPv4 | Build adjacencies, assign router IDs, design areas, summarize routes, control metrics | Critical | High | High in larger SMBs | Configure areas, passive interfaces, authentication, redistribution; troubleshoot neighbors, LSDB, routes, MTU, timers | Essential |
| OSPFv3 | OSPF for IPv6 | Route IPv6 networks | High | High | Medium | Configure IPv6 adjacencies, areas, authentication, link-local behavior | Neighbor state, LSAs, RA/ND, route installation | High |
| EIGRP | Enhanced Interior Gateway Routing Protocol | Cisco-oriented advanced distance-vector/hybrid routing | High in Cisco environments | Medium | Medium | Configure AS/process, metrics, summarization, authentication, redistribution | Neighbor, topology table, feasible successor, metrics | Medium |
| BGP-4 | Border Gateway Protocol version 4 | Exchanges reachability between autonomous systems and applies policy | Critical at ISP, data-center, cloud, and multihoming edges | Critical | Medium | Configure ASNs, eBGP/iBGP, route policies, communities, filtering, max-prefix | Peering, UPDATEs, RIB/FIB, policy, route leaks, convergence | High |
| RIP / RIPng | Routing Information Protocol | Simple hop-count-based routing | Rare in modern networks | Medium | Low | Recognize timers, hop count, split horizon, route poisoning | Neighbor/update/timer failures | Low |
| IS-IS | Intermediate System to Intermediate System | Link-state routing used in providers and large backbones | High for service-provider roles | High | Low | Configure levels, areas, NETs, authentication | Adjacency, LSP database, flooding, SPF | Medium |
| VRRP / HSRP / GLBP | First-hop redundancy protocols | Provides resilient default gateways | Critical for enterprise LANs | Medium | High | Configure priorities, tracking, preemption, virtual IP/MAC | Active/standby state, split brain, tracking | High |
| PIM-SM / IGMP | Protocol Independent Multicast / Internet Group Management Protocol | Delivers multicast efficiently | Used for video, market data, discovery, some enterprise apps | Medium | Low | Configure RP, joins, SPT, IGMP snooping | RPF, (*,G)/(S,G), joins, flooding | Medium |
| LLDP / CDP | Link Layer Discovery Protocol / Cisco Discovery Protocol | Discovers directly connected devices and capabilities | Useful for topology and automation | High | High | Enable selectively; use management-plane controls | Neighbor mismatch, wrong cabling, topology inventory | High |
| QinQ / 802.1ad | VLAN stacking | Carries customer VLANs across provider networks | Service providers and managed services | Medium | Low | Configure outer/inner tags and MTU | Tag rewrite, MTU, service mapping | Medium |
| MPLS | Multiprotocol Label Switching | Forwards traffic using labels and supports VPNs/TE | Providers, large WANs, legacy enterprise WANs | High | Low | Configure LDP/RSVP/BGP-LU, VRFs, L3VPN | Label bindings, LSP, PE-CE routing, MTU | Medium |
| VXLAN | Virtual Extensible LAN | Extends Layer-2 segments over Layer-3 underlay using VXLAN Network Identifiers | Data centers and large campus fabrics | High | Low | Configure VTEPs, VNIs, tunnels, MTU, anycast gateway | Underlay first, VTEP reachability, VNI, MAC/IP routes | High |
| EVPN | Ethernet VPN control plane | Uses BGP to distribute MAC/IP reachability for VXLAN/MPLS | Modern data-center fabrics | High | Low | Configure route targets, route distinguishers, VTEPs, multihoming | EVPN route types, BGP, VNI, DF election | High |
| SD-WAN | Software-defined WAN architecture | Centralizes policy and uses multiple WAN transports intelligently | Enterprise branches and managed WANs | High | Medium | Configure overlays, controllers, templates, SLA probes, segmentation | Underlay vs overlay, tunnel state, controller, policy | High |

OSPF troubleshooting must be systematic: verify interfaces, neighbor state, hello/dead timers, area, authentication, MTU, LSDB, and routing table. Cisco’s troubleshooting guidance specifically emphasizes neighbor state, LSDB inspection, matching timers, and consistent MTU. [cisco](https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/12151-trouble-main.html)

### What to master in OSPF

```text
R1 ───── R2
 |       |
LAN     LAN
```

You should be able to:

- Configure router IDs and passive interfaces.
- Explain neighbor states: Down, Init, 2-Way, ExStart, Exchange, Loading, Full.
- Design backbone Area 0 and non-backbone areas.
- Use cost, summarization, stub/NSSA areas, and route filtering.
- Identify MTU mismatch, duplicate router IDs, authentication mismatch, and area mismatch.
- Capture OSPF protocol packets and distinguish Hellos, LSAs, and acknowledgments.
- Secure OSPF with authentication where supported.

OSPF uses IP protocol 89 rather than TCP or UDP ports.

### What to master in BGP

You should be able to:

- Explain eBGP versus iBGP.
- Configure sessions, update sources, loopback peering, and multihop.
- Apply prefix lists, route maps/policies, AS-path filters, communities, local preference, MED, and weight where vendor-specific.
- Understand the difference between the BGP RIB and the installed forwarding table.
- Prevent accidental route leaks with prefix limits and explicit import/export policy.
- Troubleshoot Idle, Active, Established, and flapping sessions.
- Inspect UPDATE messages and route attributes.

BGP runs over TCP port 179 and carries reachability information plus AS-path information used for loop prevention and policy. [rfc-editor](https://www.rfc-editor.org/info/rfc4271/)

***

# 3. Network service protocols

| Protocol | Full name / purpose | Real-world problem solved | Configure | Troubleshoot | Secure | Network / security / SMB value | Priority |
|---|---|---|---|---|---|---|---|
| DHCP / DHCPv4 | Dynamic Host Configuration Protocol | Automatically assigns IP, mask, gateway, DNS, lease, and options | Scopes, exclusions, reservations, relay | DORA, relay, scope exhaustion, conflicts, rogue DHCP | DHCP snooping, trusted ports, rate limits | Critical / High / Critical | Essential |
| DHCPv6 | DHCP for IPv6 | Supplies IPv6 options and sometimes addresses | Stateful/stateless mode, relay, options | RA flags, relay, address/prefix assignment | Rogue DHCPv6 and relay abuse | High / High / Medium | High |
| DNS | Domain Name System | Maps names to addresses and publishes service records | Zones, records, resolvers, forwarding, TTL, DNSSEC | Recursion, delegation, NXDOMAIN, SERVFAIL, stale records | Cache poisoning, tunneling, DNSSEC, split DNS | Critical / Critical / Critical | Essential |
| NAT / PAT | Network / Port Address Translation | Conserves IPv4 and hides internal addressing | Static NAT, dynamic NAT, PAT, policy NAT | Translation table, asymmetric routing, hairpinning | Not a replacement for firewalling; bypass and logging issues | Critical / High / Critical | Essential |
| NTP / SNTP | Network Time Protocol / Simple NTP | Synchronizes clocks | Stratum hierarchy, authentication, source selection | Offset, jitter, reachability, stratum | Spoofing, reflection, time manipulation | Critical / Critical / Critical | Essential |
| ICMPv6 Neighbor Discovery | IPv6 neighbor/router discovery | Replaces ARP and supports address autoconfiguration | RA, RS, NS, NA, DHCPv6 interaction | Missing routes, duplicate address detection, rogue RA | RA Guard, ND inspection, filtering | High / Critical / Medium | High |
| PPP / PPPoE | Point-to-Point Protocol / over Ethernet | Authenticates and carries IP over ISP access links | Dialers, credentials, MTU, PAP/CHAP | Discovery/session stages, MTU, credentials | Prefer stronger authentication; inspect exposure | High / Medium / Medium | Medium |
| mDNS / DNS-SD | Multicast DNS / DNS Service Discovery | Local service discovery without central DNS | Usually enabled only where required | Multicast scope, VLAN boundaries, reflection | Spoofing, information leakage, reflection | Medium / High / High | Medium |
| SSDP / UPnP | Simple Service Discovery Protocol / Universal Plug and Play | Automatic local device discovery and port mapping | Usually disable on enterprise boundaries | Discovery storms, unexpected mappings | Common attack surface; restrict or disable | Low / High / Medium | Low |

DHCP is not merely “the thing that gives an IP.” You should understand DORA:

```text
Client ── DHCPDISCOVER broadcast ──> LAN
Client <─ DHCPOFFER ─────────────── DHCP server
Client ── DHCPREQUEST ─────────────> server
Client <─ DHCPACK ───────────────── server
```

DHCP provides reusable address allocation and configuration options. [datatracker.ietf](https://datatracker.ietf.org/doc/html/rfc2131)

DNS is equally important in operations and security. You need to understand A, AAAA, CNAME, MX, NS, PTR, TXT, SRV, SOA, TTL, recursive versus authoritative service, split-horizon DNS, and DNSSEC.

***

# 4. Web and application protocols

| Protocol | Full name / purpose | Where used | What you need to do | Important ports / security | Priority |
|---|---|---|---|---|---|
| HTTP | Hypertext Transfer Protocol | Websites, APIs, reverse proxies, load balancers | Inspect methods, status codes, headers, redirects, proxies, caching | TCP 80; plaintext; understand request smuggling, cleartext exposure, SSRF context | Essential |
| HTTPS | HTTP over TLS | Nearly all production web traffic | Configure certificates, SNI, redirects, reverse proxies, cipher policies | TCP 443; TLS protects confidentiality/integrity when correctly configured | Essential |
| TLS | Transport Layer Security | Secures web, email, APIs, VPN control planes, directory services | Understand handshake, certificates, trust chains, SNI, ALPN, versions, cipher suites | TLS 1.2/1.3; avoid obsolete SSL and old TLS versions | Essential |
| WebSocket | Full-duplex web communication | Chat, dashboards, real-time apps, browser tools | Proxy upgrades, idle timeouts, origin controls, load balancing | Usually TCP 80/443; `ws`/`wss`; authentication and origin validation | High |
| QUIC | UDP-based secure multiplexed transport | HTTP/3, modern web and some VPN/application systems | Recognize UDP-based encrypted flows, connection IDs, migration, loss behavior | UDP 443; integrates TLS and supports multiplexed streams | High |
| HTTP/3 | HTTP over QUIC | Modern browsers, CDNs, cloud services | Configure ALPN, UDP 443, fallback to HTTP/2, observability | UDP 443; firewall and monitoring tools must understand it | High |
| gRPC | Remote procedure call framework over HTTP/2 | Microservices and internal APIs | Understand HTTP/2 streams, protobuf, deadlines, mTLS, load balancing | Usually TCP 443 or internal ports; identity and authorization matter | High |
| MQTT | Message Queuing Telemetry Transport | IoT telemetry and control | Broker, topics, QoS, retained messages, ACLs | TCP 1883; TLS 8883; weak ACLs can expose devices | Medium |
| AMQP | Advanced Message Queuing Protocol | Enterprise messaging, RabbitMQ, Azure Service Bus | Queues, exchanges, bindings, acknowledgments, TLS | Commonly TCP 5672/5671 | Medium |
| SIP / RTP | Session Initiation Protocol / Real-time Transport Protocol | VoIP call setup and media | NAT traversal, codecs, signaling/media separation, QoS | SIP TCP/UDP 5060, TLS 5061; RTP dynamic UDP range | Medium |
| LDAP application use | Directory queries | Identity-aware applications, network device authentication | Bind, search, filters, referrals, TLS | TCP/UDP 389; prefer LDAPS or StartTLS | High |

TLS 1.3 provides protection against eavesdropping, tampering, and forgery; you should understand certificate validation and handshake failures rather than treating HTTPS as automatically secure.  NIST guidance focuses on selecting and configuring current TLS implementations and recommended cryptographic algorithms. [datatracker.ietf](https://datatracker.ietf.org/doc/html/rfc8446)

### Web troubleshooting workflow

```text
DNS resolution
  ↓
TCP or QUIC reachability
  ↓
TLS handshake / certificate / SNI / ALPN
  ↓
HTTP status and headers
  ↓
Application authentication
  ↓
Backend, database, proxy, or load balancer
```

Useful tools:

```bash
dig example.com
curl -v https://example.com
openssl s_client -connect example.com:443 -servername example.com
curl --http3 https://example.com
tcpdump -ni any port 443
```

***

# 5. Remote administration protocols

| Protocol | Full name / purpose | Real-world use | What you need to do | Security | Priority |
|---|---|---|---|---|---|
| SSH | Secure Shell | Secure CLI administration, tunnels, SCP, SFTP | Configure keys, users, bastions, forwarding, algorithms, session logging | Strong encryption, server authentication, MFA integration; restrict exposure | Essential |
| Telnet | Teletype Network Protocol | Legacy plaintext device administration | Recognize and replace it; troubleshoot only when maintaining old systems | Sends credentials and commands in cleartext; disable | Low / legacy |
| HTTPS management | HTTP over TLS for device interfaces | Firewalls, switches, cloud portals, APIs | Manage certificates, RBAC, API tokens, secure headers | Restrict management source networks and enforce MFA | High |
| NETCONF | Network Configuration Protocol | Structured device configuration over SSH | Understand datastore, candidate, commit, rollback, YANG | SSH and role-based access | High |
| RESTCONF | RESTful Configuration Protocol | HTTP-based network configuration and telemetry | Use REST APIs, JSON/XML, YANG models, tokens | TLS, API authentication, authorization, rate limits | High |
| gNMI | gRPC Network Management Interface | Streaming telemetry and model-driven configuration | Subscribe to telemetry paths and push configuration | mTLS and identity controls | Medium |
| TFTP | Trivial File Transfer Protocol | Legacy device boot/config/image transfer | Recognize use in PXE and old network workflows | UDP 69; no authentication or encryption | Low |
| SNMP | Simple Network Management Protocol | Monitoring and limited management | Prefer v3; understand GET, GETNEXT, GETBULK, SET, traps, informs | v1/v2c community strings are weak; v3 provides authentication/privacy | Essential |

SSH provides secure remote login, encryption, server authentication, and integrity protection over TCP/IP.  For modern network management, learn CLI first, then model-driven methods such as NETCONF, RESTCONF, and gNMI. [datatracker.ietf](https://datatracker.ietf.org/doc/html/rfc4253)

***

# 6. File transfer protocols

| Protocol | Purpose | Where used | Practical expectation | Security / ports | Priority |
|---|---|---|---|---|---|
| FTP | Legacy file transfer | Old servers, appliances, public repositories | Understand active/passive modes, control/data channels, NAT problems | TCP 21 control; TCP 20 active data or dynamic passive ports; plaintext | Low |
| FTPS | FTP secured with TLS | Some enterprise and managed-transfer environments | Understand explicit versus implicit TLS and certificate problems | TCP 21 explicit or 990 implicit; firewall complexity | Medium |
| SFTP | SSH File Transfer Protocol | Secure file transfer and automation | Configure keys, chroot, permissions, automation, logging | Usually TCP 22; encrypted through SSH | High |
| SCP | Secure Copy Protocol | Simple file copying over SSH | Use for controlled administrative transfers; know limitations versus SFTP | TCP 22; encrypted through SSH | High |
| TFTP | Trivial File Transfer Protocol | PXE, firmware/config recovery, legacy devices | Recognize it in captures and restrict it to isolated networks | UDP 69; unauthenticated/plaintext | Low |

Do not confuse **SFTP** with “secure FTP.” SFTP is a file-transfer subsystem over SSH, while FTPS is FTP protected by TLS.

***

# 7. Email protocols and controls

| Protocol | Full name / purpose | Real-world use | What you need to do | Ports / security | Priority |
|---|---|---|---|---|---|
| SMTP | Simple Mail Transfer Protocol | Mail submission and server-to-server delivery | Understand relay, MX delivery, STARTTLS, submission, queues, bounces | TCP 25 server-to-server, 587 submission, 465 implicit TLS | High |
| IMAP | Internet Message Access Protocol | Synchronizes mail stored on a server | Troubleshoot folders, authentication, TLS, mailbox states | TCP 143; 993 TLS | Medium |
| POP3 | Post Office Protocol version 3 | Downloads mail, often with limited synchronization | Recognize legacy clients and download/delete behavior | TCP 110; 995 TLS | Low |
| SPF | Sender Policy Framework | Publishes authorized sending hosts in DNS | Create a single valid TXT policy; understand includes and lookup limits | DNS TXT; reduces spoofing but does not sign messages | High |
| DKIM | DomainKeys Identified Mail | Cryptographically signs email headers/content | Publish selector keys, rotate keys, troubleshoot signatures | DNS TXT; supports message authentication | High |
| DMARC | Domain-based Message Authentication, Reporting, and Conformance | Aligns SPF/DKIM with visible From domain and defines policy | Start with monitoring, then quarantine/reject; analyze reports | DNS TXT at `_dmarc`; policy enforcement | High |
| MTA-STS / TLS-RPT | Mail Transport Agent Strict Transport Security / TLS Reporting | Improves SMTP TLS delivery assurance | Publish policy and report endpoint | HTTPS policy; DNS TXT for reporting | Medium |

For a security role, SPF, DKIM, and DMARC are more important than POP3. For a network engineer, understand how DNS, SMTP connectivity, TLS, firewalls, and MX records interact.

***

# 8. Security and encryption protocols

| Protocol / technology | Purpose | Where used | What you need to be able to do | Security / priority |
|---|---|---|---|---|
| TLS | Encrypts application sessions and authenticates endpoints | Web, APIs, email, LDAP, management | Validate certificates, inspect handshakes, configure versions/ciphers, diagnose SNI/ALPN/time failures | Essential |
| IPsec | Network-layer authentication and encryption | Site-to-site VPNs, remote access, cloud tunnels | Configure policies, proposals, selectors, NAT-T, routing, failover | Essential |
| IKE/IKEv2 | Negotiates IPsec security associations and keys | IPsec VPN control plane | Configure identity, proposals, authentication, lifetimes, DPD, NAT-T | Essential |
| 802.1X | Port-based network access control using EAP | Wired LAN and enterprise Wi-Fi access | Configure supplicant, authenticator, RADIUS, EAP method, fallback | Essential |
| RADIUS | Centralized authentication, authorization, accounting | VPN, Wi-Fi, 802.1X, network access | Configure shared secrets, attributes, accounting, failover | Essential |
| TACACS+ | Device administration AAA | Network-device login and command authorization | Configure per-command authorization, accounting, privilege roles | High |
| MACsec / 802.1AE | Layer-2 encryption | Sensitive Ethernet links and data centers | Understand key management and link support | High |
| DNSSEC | DNS data origin authentication and integrity | Authoritative DNS and validation | Understand DS/DNSKEY/RRSIG, key rollover, validation failures | High |
| SSH | Secure administration and tunneling | Network devices, Linux, automation | Keys, bastions, algorithms, forwarding | Essential |
| WireGuard | Modern VPN tunnel protocol | Site-to-site, remote access, cloud and personal VPNs | Configure peers, keys, allowed IPs, routes, keepalive | High |
| OpenVPN | TLS-based VPN solution | Remote access and site-to-site | Configure certificates, profiles, routes, MTU, split/full tunnel | High |
| DTLS | Datagram TLS | UDP-based secure applications and some VPN/control systems | Recognize handshake and timeout behavior | Medium |
| EAP | Extensible Authentication Protocol framework | 802.1X, wireless, VPN authentication | Understand EAP-TLS, PEAP, certificates, identity flow | High |

TLS should be treated as a protocol family, not just a padlock icon. You need to know where certificate validation occurs, how trust chains work, why time synchronization matters, and how proxies/load balancers terminate and re-establish TLS. NIST specifically provides guidance for selecting and configuring TLS implementations. [nist](https://www.nist.gov/news-events/news/2019/08/guidelines-selection-configuration-and-use-transport-layer-security-tls)

***

# 9. Enterprise authentication and directory protocols

| Protocol / technology | Full name / purpose | Where used | Practical skills | Security | Priority |
|---|---|---|---|---|---|
| 802.1X | Port-based access control | Wired access and enterprise Wi-Fi | Trace supplicant → switch/AP → RADIUS → directory | Prevents unauthorized network access; certificate design matters | Essential |
| RADIUS | Remote Authentication Dial-In User Service | Network access, VPN, Wi-Fi, 802.1X | Attributes, accounting, failover, shared secrets, EAP | Protect shared secrets and restrict clients | Essential |
| TACACS+ | Terminal Access Controller Access-Control System Plus | Network device administration | Separate authentication, authorization, and accounting | Central command authorization and audit | High |
| LDAP | Lightweight Directory Access Protocol | Query and authenticate against directory services | Bind, search filters, DN, schema, groups, referrals | Anonymous binds, injection, exposed directory, TLS | High |
| LDAPS / StartTLS | LDAP over TLS / LDAP TLS upgrade | Secure directory queries and binds | Certificates, trust, port 636 versus 389 StartTLS | Protect credentials and directory data | High |
| Kerberos | Ticket-based network authentication | Active Directory, Linux realms, SSO | Tickets, KDC, TGT, SPNs, delegation, time dependency | Pass-the-ticket, Kerberoasting, clock attacks | High |
| Active Directory protocols | Microsoft directory ecosystem | Enterprise identities, DNS, Group Policy, authentication | Understand DNS, LDAP, Kerberos, SMB, RPC relationships | Critical attack surface | High |
| SAML / OAuth 2.0 / OIDC | Web federation and delegated authorization | SaaS, cloud identity, SSO | Understand browser redirects, tokens, claims, scopes, IdP/SP roles | Token theft, redirect abuse, signing keys | High |
| SCIM | System for Cross-domain Identity Management | Automated SaaS user provisioning | Configure provisioning and deprovisioning | Prevent orphaned accounts | Medium |

RADIUS is commonly involved in 802.1X authentication, and IEEE guidance describes its use by 802.1X authenticators.  Kerberos is highly dependent on DNS and synchronized time; a broken NTP hierarchy can look like an authentication failure. [datatracker.ietf](https://datatracker.ietf.org/doc/rfc3580/)

***

# 10. Network monitoring and management

| Protocol / technology | Purpose | Real-world use | What you need to do | Priority |
|---|---|---|---|---|
| SNMPv3 | Secure network monitoring and management | Polling interfaces, CPU, memory, sensors, routes, and generating traps | Configure users, auth/privacy, views, polling, traps, MIBs | Essential |
| SNMPv1/v2c | Older SNMP versions | Existing network monitoring systems | Read captures and migrate away from community strings | Low / legacy |
| Syslog | Event message transport and logging format | Centralized device, firewall, server, and application logs | Configure facility/severity, timestamps, collectors, parsing | Essential |
| NetFlow | Cisco-originated flow telemetry | Traffic accounting, capacity planning, threat hunting | Configure exporters/collectors, sampling, active/inactive timers | High |
| IPFIX | IP Flow Information Export | Vendor-neutral flow export based on templates | Understand templates, records, collectors, fields | High |
| sFlow | Sampled packet/flow monitoring | High-speed switching and data centers | Configure sampling and polling | Medium |
| RMON | Remote Monitoring MIBs | Legacy embedded monitoring | Recognize historical deployments | Low |
| Streaming telemetry | Push-based structured metrics | Modern model-driven operations | gNMI, YANG, subscriptions, time series | High |
| NTP | Time synchronization | Correlating logs and validating certificates | Build trusted hierarchy and monitor drift | Essential |
| LLDP/CDP | Neighbor discovery | Inventory, topology, automation | Use cautiously on untrusted ports | High |

SNMPv3 uses the User-based Security Model and supports message-level security; in practice, use authentication and privacy rather than exposing v1/v2c community strings. [datatracker.ietf](https://datatracker.ietf.org/wg/snmpv3/documents/)

### Monitoring skills matter more than protocol trivia

You should be able to answer:

- Which interface is dropping packets?
- Is the problem congestion, errors, loss, or a route change?
- Did the device reboot or merely flap an interface?
- Which host is generating abnormal traffic?
- Does the flow collector see bytes, packets, direction, and application ports?
- Can you correlate firewall, DNS, DHCP, authentication, and endpoint events using synchronized timestamps?

***

# 11. VPN protocols and tunneling

| Protocol / technology | Purpose | Where used | Practical skills | Priority |
|---|---|---|---|---|
| IPsec | Encrypts/authenticates IP traffic | Site-to-site and remote-access VPN | IKE negotiation, policies, selectors, NAT-T, routing, failover | Essential |
| IKEv2 | Negotiates IPsec SAs and keys | Modern IPsec VPNs | Debug proposals, identities, authentication, lifetimes, DPD | Essential |
| WireGuard | Lightweight modern encrypted tunnel | Remote access, mesh, cloud, site-to-site | Public/private keys, peers, AllowedIPs, routes, keepalive | High |
| OpenVPN | TLS-based VPN | Remote access and multi-platform VPNs | Certificates, server/client config, routes, MTU, split tunnel | High |
| GRE | Generic Routing Encapsulation | Carries routing protocols or non-IP traffic through IP | Tunnel endpoints, keepalive, MTU, recursive routing | High |
| GRE over IPsec | GRE routing flexibility plus IPsec encryption | Enterprise routed site-to-site VPNs | Separate tunnel and encryption troubleshooting | High |
| DMVPN | Dynamic Multipoint VPN | Hub-and-spoke/multipoint Cisco WANs | NHRP, mGRE, IPsec, spoke-to-spoke paths | Medium |
| SSTP | Secure Socket Tunneling Protocol | Windows-oriented remote access | Recognize HTTPS-based VPN behavior | Low |
| L2TP/IPsec | Layer 2 Tunneling Protocol with IPsec | Legacy remote access | Understand negotiation and NAT-T | Low |
| VXLAN | Overlay tunnel for Layer-2 over Layer-3 | Data centers | VTEP/VNI/underlay troubleshooting | High |
| MPLS L3VPN | Provider VPN using labels and VRFs | Carrier WANs | PE/CE, VRF, route targets, labels | Medium |

A VPN is not a routing protocol by itself. A common failure is to establish the encrypted tunnel but forget to provide a route, security policy, NAT exemption, or return path.

***

# 12. Cloud networking protocols and technologies

Cloud networking is less about one new protocol and more about applying familiar IP, routing, DNS, TLS, VPN, and identity concepts through provider abstractions.

| Technology | Full name / concept | What problem it solves | Where used | Practical skills | Network / security / freelance value | Priority |
|---|---|---|---|---|---|---|
| VPC / VNet | Virtual Private Cloud / Virtual Network | Isolated virtual network in a cloud account/subscription | AWS, Azure, GCP | Design CIDRs, subnets, routes, gateways, peering, endpoints | Critical / Critical / High | Essential |
| Subnets and route tables | Logical IP segments and forwarding rules | Determines reachability and isolation | All clouds | Public/private subnet design, default routes, propagation | Essential |
| Security groups / NSGs | Stateful virtual firewall rules | Controls traffic to virtual interfaces/resources | AWS security groups, Azure NSGs, GCP firewall rules | Source/destination/port rules, least privilege, references | Essential |
| Network ACLs | Stateless subnet-level filtering | Adds subnet boundary control | AWS NACLs and equivalents | Direction, ephemeral ports, return traffic | High |
| Internet gateway | Cloud internet attachment | Provides internet path for public resources | AWS and analogous services | Public IP, route, filtering, egress design | High |
| NAT gateway / NAT instance | Managed outbound translation | Gives private workloads outbound internet access | Cloud private subnets | Route design, cost, availability, port exhaustion | Essential |
| Transit Gateway / Virtual WAN / Cloud Router | Hub-and-spoke cloud connectivity | Connects many VPCs/VNets, sites, and regions | AWS, Azure, GCP | Route propagation, segmentation, attachments | High |
| VPC/VNet peering | Private network-to-network connection | Connects isolated cloud networks | Multi-account and multi-environment designs | Non-transitive routing, overlapping CIDR avoidance | High |
| Private endpoints / PrivateLink | Private access to managed services | Avoids public exposure | AWS PrivateLink, Azure Private Link, GCP Private Service Connect | DNS, endpoint policies, routing | High |
| Cloud VPN | Managed IPsec connectivity | Connects on-premises to cloud | Hybrid networks | BGP/static routing, tunnels, HA, MTU | Essential |
| Direct Connect / ExpressRoute / Interconnect | Dedicated private connectivity | Predictable hybrid connectivity | Enterprise cloud | BGP, VLANs, redundancy, provider circuits | High |
| Cloud load balancers | Layer 4/7 traffic distribution | Availability, scale, TLS termination | All major clouds | Health checks, listeners, target groups, proxy behavior | Essential |
| Cloud DNS | Managed authoritative/recursive DNS | Naming, routing, service discovery | Route 53, Azure DNS, Cloud DNS | Private zones, split horizon, health checks | Essential |
| WAF / DDoS protection | Application and volumetric protection | Protects public workloads | Cloud edge services | Rules, false positives, logging, rate limits | Essential for security |
| Kubernetes networking | Pod/service/ingress networking | Connects workloads in clusters | EKS, AKS, GKE, self-managed Kubernetes | CNI, Services, NetworkPolicies, ingress, overlay | High |
| NetworkPolicy | Kubernetes traffic policy | Restricts pod-to-pod communication | Kubernetes | Default deny and namespace/workload policy | High |
| Service mesh | mTLS and service-to-service policy | Secures and observes microservices | Istio, Linkerd, managed meshes | Identity, sidecars, traffic shifting | Medium |
| Overlay networking | Encapsulation across underlay | Enables virtual networks and containers | VXLAN, Geneve, cloud SDN | MTU, encapsulation, underlay reachability | High |

Cloud security groups behave as virtual firewalls controlling allowed traffic to and from associated resources.  AWS, Azure, and Google Cloud expose different abstractions, but all require understanding IP ranges, routes, ports, statefulness, and identity. [docs.aws.amazon](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)

A typical hybrid design:

```text
Office LAN
   │
IPsec / Direct Connect / ExpressRoute
   │
Cloud transit hub
   ├── Application VPC/VNet
   ├── Database private subnets
   ├── Management network
   └── Shared services DNS
```

***

# 13. Legacy protocols you only need to understand

These are worth recognizing in captures, incident reports, and inherited networks. Do not prioritize deep configuration unless your job requires it.

| Protocol / technology | Why it existed | Where you may encounter it | What to know | Priority |
|---|---|---|---|---|
| Telnet | Remote terminal access before SSH | Old switches, routers, appliances | TCP 23, plaintext, replace with SSH | Low |
| FTP | Early file transfer | Legacy servers and appliances | TCP 21/control, passive mode, plaintext | Low |
| TFTP | Minimal boot/config transfer | PXE, old network gear | UDP 69, no authentication | Low |
| HTTP | Unencrypted web | Redirects, internal legacy apps, health checks | TCP 80, cleartext | Medium |
| POP3 | Download-oriented email | Old mail clients | TCP 110/995, limited synchronization | Low |
| Rlogin/rsh | Unix remote login/command execution | Very old Unix environments | Trust-based and insecure | Low |
| RDP | Microsoft Remote Desktop | Windows administration | TCP/UDP 3389, brute-force and exposure risks | Medium |
| SMBv1 | Early Windows file sharing | Legacy systems and malware investigations | Disable; vulnerable and obsolete | Low |
| NetBIOS over TCP/IP | Legacy Windows name/session services | Old Windows networks | UDP 137/138, TCP 139 | Low |
| WEP | Obsolete Wi-Fi security | Historical equipment | Broken; never deploy | Low |
| WPA/TKIP | Transitional Wi-Fi security | Legacy clients | Know migration history; prefer WPA2-AES/WPA3 | Low |
| RIP | Simple routing | Small legacy networks and labs | UDP 520, hop-count limitation | Low |
| IS-IS | Provider routing | Carrier and large backbone networks | Learn later if provider-focused | Medium |
| Frame Relay | Legacy WAN service | Historical WANs | DLCI, PVC, LMI concepts | Low |
| ATM | Legacy cell-switched WAN | Historical telecom networks | Recognize only | Low |
| X.25 | Early packet-switched WAN | Specialized legacy systems | Recognize only | Low |
| Gopher | Pre-web information protocol | Historical systems | No operational priority | Low |
| rlogin | Insecure remote login | Old Unix | Recognize credentials in cleartext | Low |

Legacy does not mean irrelevant to security. Telnet, FTP, SMBv1, weak SNMP, old TLS, and plaintext management protocols are often high-value findings during assessments.

***

# 14. Advanced and specialized protocols to learn later

| Technology | What it does | Learn when |
|---|---|---|
| IS-IS | Link-state routing for providers and very large networks | Service-provider or backbone role |
| MPLS L3VPN / EVPN | Provider and data-center VPN control planes | WAN, carrier, or data-center role |
| VXLAN/EVPN | Data-center overlays and distributed gateways | Data-center engineering |
| BFD | Bidirectional Forwarding Detection | Fast failure detection with routing protocols |
| RSVP-TE | Resource Reservation Protocol Traffic Engineering | MPLS traffic-engineering environments |
| Segment Routing / SR-MPLS / SRv6 | Source-routed traffic engineering | Modern provider and large WAN networks |
| PCEP | Path Computation Element Protocol | Controller-driven traffic engineering |
| LDP | Label Distribution Protocol | MPLS networks |
| BGP-LS | BGP Link-State | Controllers and topology distribution |
| P4Runtime | Programmable data-plane control | Programmable switches and research |
| OpenFlow | SDN flow programming protocol | Historical SDN and some specialized environments |
| Geneve | Generic Network Virtualization Encapsulation | Cloud and virtualization platforms |
| GENEVE/VXLAN internals | Overlay encapsulation | Virtualized data centers |
| SRTP | Secure Real-time Transport Protocol | Voice/video security |
| WebRTC / ICE / STUN / TURN | Browser real-time communications and NAT traversal | Collaboration and real-time application security |
| Diameter | Carrier-grade AAA | Mobile/core networks |
| GTP | GPRS Tunneling Protocol | Mobile networks and telecom |
| BGP Flowspec | BGP-distributed traffic filtering | DDoS mitigation and provider networks |
| RPKI / ROA / BGPsec | Routing-origin validation and routing security | Internet routing/security role |
| PTP / IEEE 1588 | Precision Time Protocol | Industrial, telecom, financial, and high-precision systems |
| OPC UA | Industrial automation communication | OT/ICS security |
| Modbus/TCP | Industrial control protocol | OT environments |
| DNP3 | Utility/SCADA protocol | Energy and industrial environments |
| BACnet/IP | Building automation | Facilities/OT networks |
| CoAP | Constrained Application Protocol | IoT and constrained devices |

EVPN is a BGP-based Ethernet VPN control plane; the standard defines EVPN network-layer reachability information carried using BGP multiprotocol extensions.  QUIC, by contrast, is an encrypted UDP-based transport with multiplexed streams, flow control, connection migration, and TLS-integrated key negotiation. [dl.acm](https://dl.acm.org/doi/10.17487/RFC7432)

***

# Protocols to configure, troubleshoot, secure, or defer

## Configure confidently

You should be able to build and modify:

- Ethernet interfaces and trunks.
- VLANs and SVIs.
- STP/RSTP protections.
- LACP bundles.
- IPv4 and IPv6 addressing.
- Static routes and default routes.
- DHCP scopes and relays.
- DNS client/resolver settings and common records.
- NAT/PAT.
- OSPF.
- HSRP/VRRP.
- ACLs and firewall rules.
- SSH.
- SNMPv3 and Syslog.
- NTP.
- IPsec site-to-site VPNs.
- RADIUS/TACACS+ integrations.
- 802.1X basics.
- Cloud VPC/VNet routing and security groups.
- Load balancer listeners and health checks.

## Troubleshoot deeply

You should be able to diagnose:

- Ethernet physical errors and duplex mismatch.
- VLAN/trunk/native VLAN problems.
- STP loops and unexpected root changes.
- LACP member failure.
- ARP and IPv6 ND failures.
- Incorrect subnet masks and routes.
- OSPF adjacency and LSDB problems.
- BGP session and route-policy issues.
- DHCP relay and scope exhaustion.
- DNS resolution and delegation failures.
- NAT and asymmetric routing.
- TCP resets, retransmissions, and MTU problems.
- TLS certificates, SNI, time, and ALPN.
- IPsec/IKE negotiation.
- RADIUS/802.1X authentication.
- Cloud route-table and security-group failures.
- Monitoring gaps, log loss, and flow-export problems.

## Secure deliberately

You need to secure:

- SSH and HTTPS administration.
- SNMPv3 and Syslog transport.
- VLANs and trunk ports.
- STP with BPDU Guard, Root Guard, and edge controls.
- DHCP with snooping and trusted ports.
- IPv6 with RA Guard and appropriate filtering.
- DNS with restricted recursion, logging, and DNSSEC where appropriate.
- Routing with authentication, prefix filters, max-prefix limits, and route policies.
- BGP with RPKI validation and anti-leak controls where applicable.
- IPsec, WireGuard, and OpenVPN.
- 802.1X, RADIUS, TACACS+, LDAP, and Kerberos.
- TLS certificates, cipher policies, and private keys.
- Cloud security groups, NACLs, WAFs, and IAM-integrated network controls.
- Email with SPF, DKIM, and DMARC.

## Understand but do not initially configure

- RIP.
- Telnet.
- FTP and TFTP.
- POP3.
- NetBIOS.
- RMON.
- Frame Relay.
- ATM.
- X.25.
- OpenFlow.
- Provider-only MPLS internals.
- Telecom signaling and mobile-core protocols.

## Leave for later

- Segment Routing.
- PCEP.
- BGP-LS.
- P4Runtime.
- EVPN route-type details.
- Deep MPLS traffic engineering.
- PTP.
- OT protocols.
- Carrier-grade Diameter/GTP.
- Specialized multicast engineering.
- Full service-mesh control-plane internals.

***

# Role-based priority lists

## A. Network Engineer

### Tier 1

- Ethernet, MAC, ARP, IPv4, IPv6.
- ICMP, TCP, UDP.
- VLAN/802.1Q, STP/RSTP, LACP.
- DHCP, DNS, NAT, NTP.
- SSH, SNMPv3, Syslog.
- OSPF and first-hop redundancy.

### Tier 2

- BGP.
- OSPFv3.
- ACLs and firewall policy.
- IPsec.
- QoS.
- LLDP/CDP.
- NetFlow/IPFIX.
- 802.1X and RADIUS.
- Cloud VPC/VNet networking.

### Tier 3

- EIGRP.
- MPLS.
- IS-IS.
- VXLAN/EVPN.
- SD-WAN.
- NETCONF/RESTCONF/gNMI.
- Multicast.

## B. Security Engineer

### Tier 1

- Ethernet, ARP, IPv4/IPv6, ICMP.
- TCP/UDP and packet analysis.
- DNS, DHCP, NAT.
- HTTP/HTTPS/TLS.
- SSH.
- Firewalls, ACLs, security groups, NACLs.
- IPsec/IKEv2.
- 802.1X/RADIUS.
- LDAP/LDAPS/Kerberos.
- SNMPv3, Syslog, NetFlow/IPFIX.
- SPF/DKIM/DMARC.

### Tier 2

- VLAN/STP/LACP security.
- OSPF/BGP attack surface and route security.
- WireGuard/OpenVPN.
- Cloud transit, private endpoints, load balancers, WAF.
- Kubernetes networking and NetworkPolicy.
- QUIC/HTTP/3.
- SAML/OAuth/OIDC.
- TLS certificate lifecycle and PKI.

### Tier 3

- VXLAN/EVPN security.
- MPLS/SD-WAN security.
- BGP Flowspec/RPKI.
- OT protocols.
- Service mesh and mTLS.
- PTP and specialized network security.

## C. Freelance network/IT technician

### Tier 1

- Ethernet and Wi-Fi fundamentals.
- IPv4 subnetting.
- DHCP, DNS, NAT.
- VLANs, trunks, basic STP.
- Router, switch, firewall, and AP setup.
- SSH and HTTPS management.
- VPNs: IPsec, WireGuard, OpenVPN.
- Basic TLS and certificates.
- Backup, firmware, logging, and monitoring.

### Tier 2

- IPv6 basics.
- RADIUS/802.1X.
- Site-to-site VPNs.
- LACP and redundancy.
- Guest networks and segmentation.
- Cloud VPC/VNet basics.
- SMB/file services.
- Email DNS: MX, SPF, DKIM, DMARC.

### Tier 3

- OSPF.
- BGP.
- MPLS.
- VXLAN/EVPN.
- SD-WAN.
- Advanced identity integrations.
- Automation with NETCONF/RESTCONF/gNMI.

## D. Combined Network + Security Engineer

Master these in order:

1. Ethernet, VLANs, STP, LACP.
2. IPv4/IPv6, ARP/ND, ICMP.
3. TCP/UDP and packet capture.
4. DHCP, DNS, NAT, NTP.
5. OSPF, first-hop redundancy, ACLs.
6. Firewalls, segmentation, VPNs.
7. TLS, SSH, HTTPS, email authentication.
8. 802.1X, RADIUS, TACACS+, LDAP, Kerberos.
9. SNMPv3, Syslog, NetFlow/IPFIX, telemetry.
10. BGP and routing security.
11. Cloud VPC/VNet, security groups, transit, private endpoints.
12. VXLAN/EVPN, MPLS, SD-WAN, Kubernetes networking.
13. RPKI, BGP Flowspec, service mesh, OT, and specialized protocols.

***

# Recommended learning sequence

## Phase 1: Build a packet-level foundation

Learn:

- Ethernet and MAC addresses.
- IPv4 subnetting and CIDR.
- IPv6 addressing and Neighbor Discovery.
- ARP and ICMP.
- TCP and UDP.
- Ports, sockets, MTU, fragmentation, TTL/hop limit.

Build a lab:

```text
Linux VM ── virtual switch ── Linux VM
       \          │          /
        └──── router/firewall
```

Practice:

```bash
ip addr
ip route
ip neigh
ping
traceroute
ss -tulpn
tcpdump
```

Goal: explain every field involved when one host pings another or opens a TCP connection.

## Phase 2: Learn switching

Learn:

- Ethernet frame structure.
- MAC learning and flooding.
- VLAN access/trunk behavior.
- 802.1Q tagging.
- STP/RSTP.
- LACP.
- LLDP/CDP.
- DHCP snooping, Dynamic ARP Inspection, and port security.

Build:

```text
Switch A ── trunk ── Switch B
   │                    │
 VLAN 10              VLAN 20
```

Goal: configure segmentation and intentionally break/fix trunks, VLANs, STP, and LACP.

## Phase 3: Learn essential network services

Learn:

- DHCP/DHCPv6.
- DNS records, recursion, delegation, split DNS.
- NAT/PAT.
- NTP.
- Syslog and basic SNMP.
- IPv4 and IPv6 ACLs.

Goal: deploy a small office network where clients receive addresses, resolve names, reach the internet, synchronize time, and generate logs.

## Phase 4: Learn routing

Start with:

- Static routes.
- Default routes.
- Route selection.
- OSPF.
- OSPFv3.
- HSRP/VRRP.
- Route redistribution and summarization.

Then learn:

- BGP.
- Route policies.
- Prefix filtering.
- Communities.
- Multihoming.
- Route leaks and RPKI concepts.

Goal: troubleshoot the full path rather than merely checking whether a route exists.

## Phase 5: Learn security controls

Learn:

- Stateful firewall concepts.
- ACL policy design.
- Management-plane protection.
- SSH hardening.
- TLS certificates.
- IPsec/IKEv2.
- WireGuard/OpenVPN.
- 802.1X/RADIUS.
- TACACS+.
- LDAP/LDAPS and Kerberos.
- DNS security.
- Email authentication.

Goal: segment a network so that users, guests, servers, databases, management systems, and VPN clients have only necessary access.

## Phase 6: Learn observability and incident investigation

Learn:

- SNMPv3.
- Syslog.
- NetFlow/IPFIX.
- Packet captures.
- DNS and DHCP logs.
- Firewall logs.
- Authentication logs.
- NTP correlation.
- Streaming telemetry.

Practice:

```text
Device → Syslog collector
Device → SNMP/telemetry collector
Device → Flow collector
Firewall → SIEM
```

Goal: determine what happened, when it happened, which host was involved, and whether the issue was availability, misconfiguration, or attack activity.

## Phase 7: Learn cloud networking

Start with one provider deeply—AWS, Azure, or GCP—then map concepts across providers:

- VPC/VNet.
- Subnets and route tables.
- Security groups/NSGs.
- NACLs.
- Internet and NAT gateways.
- Transit hubs.
- VPN and dedicated connectivity.
- Private endpoints.
- DNS.
- Load balancers.
- WAF.
- Kubernetes networking.

Cloud providers use different names, but the underlying questions remain the same:

```text
Who is the source?
What is the destination?
Which route is selected?
Which policy allows or denies it?
Where is NAT performed?
Where is TLS terminated?
How is the event logged?
```

Cloud security groups and equivalent controls filter traffic using sources, destinations, ports, and protocols. [docs.aws.amazon](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)

## Phase 8: Advanced enterprise networking

Learn later:

- MPLS and L3VPN.
- VXLAN/EVPN.
- SD-WAN.
- IS-IS.
- BFD.
- Segment Routing.
- RPKI/BGP security.
- Network automation with YANG, NETCONF, RESTCONF, and gNMI.
- Kubernetes NetworkPolicy and service mesh.
- OT/ICS protocols if your work requires them.

***

# Practical protocol labs

## Lab 1: VLAN and routing lab

```text
PC-A ── VLAN 10 ──┐
                  ├── L3 switch/router ── Internet
PC-B ── VLAN 20 ──┘
```

Implement:

- DHCP scopes for VLAN 10 and VLAN 20.
- Inter-VLAN routing.
- ACL blocking VLAN 20 from the management VLAN.
- DNS and NTP.
- Syslog and SNMPv3.

Break and troubleshoot:

- Wrong native VLAN.
- Missing allowed VLAN.
- Wrong SVI mask.
- Missing DHCP relay.
- Incorrect ACL direction.
- Missing default route.

## Lab 2: OSPF and failure recovery

```text
LAN-A ── R1 ───── R2 ── LAN-B
             \   /
              R3
```

Implement:

- OSPF Area 0.
- Loopback router IDs.
- Passive interfaces.
- Route summarization.
- Authentication.
- Link failure and reconvergence.

Capture and inspect:

- OSPF Hellos.
- Database Description packets.
- LSAs.
- Adjacency changes.
- Installed routes.

## Lab 3: Secure branch network

```text
Branch users ── switch ── firewall ── IPsec/WireGuard ── cloud VPC
      │            │          │
    802.1X       VLANs      NAT/ACL
```

Implement:

- User, guest, server, and management VLANs.
- 802.1X with RADIUS.
- Site-to-site VPN.
- Least-privilege firewall rules.
- Central Syslog and flow monitoring.
- DNS filtering and NTP.
- Cloud security-group restrictions.

## Lab 4: Web security path

```text
Client ── DNS ── CDN/WAF ── load balancer ── reverse proxy ── application
```

Analyze:

- DNS resolution.
- TCP or QUIC.
- TLS handshake.
- SNI and ALPN.
- HTTP headers and status codes.
- Proxy forwarding.
- Backend health checks.
- WebSocket upgrade.
- Firewall and WAF logs.

***

# Bottom line

Your core mastery target is not “know 100 protocols.” It is being able to trace and secure a real connection:

```text
Name resolution
 → interface and VLAN
 → ARP/IPv6 ND
 → gateway and route
 → firewall/NAT
 → TCP/UDP or QUIC
 → TLS
 → application
 → authentication
 → logging and monitoring
```

For your combined career path, spend most of your early time on **Ethernet, VLANs, STP, IPv4/IPv6, ARP/ND, ICMP, TCP/UDP, DHCP, DNS, NAT, OSPF, ACLs/firewalls, SSH, TLS, IPsec, 802.1X/RADIUS, Syslog, SNMPv3, NetFlow/IPFIX, and cloud VPC/VNet networking**.

Then add **BGP, identity protocols, WireGuard/OpenVPN, VXLAN/EVPN, SD-WAN, MPLS, Kubernetes networking, automation, and routing security**. Avoid spending weeks memorizing obsolete protocols; learn enough to recognize them, secure them, and replace them.
