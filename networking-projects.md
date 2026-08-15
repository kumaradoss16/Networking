# Portfolio strategy

You do not need dozens of disconnected labs. Build **six integrated flagship projects** and use smaller focused labs only to support them:

1. **Secure SMB/branch network**
2. **Enterprise routed and switched network**
3. **Identity-aware access control and Active Directory**
4. **Security monitoring, IDS/IPS, and SIEM**
5. **Cloud hybrid network**
6. **Network automation and compliance platform**

Together, these demonstrate:

```text
Design → Configure → Secure → Monitor → Troubleshoot
       → Test → Automate → Document
```

This portfolio structure reflects modern enterprise practice: segmented trust zones, centralized monitoring, identity-aware access, vulnerability validation, and cloud controls. NIST’s zero-trust guidance emphasizes inventory, policy-driven access, segmentation, enforcement points, logging, vulnerability assessment, and continuous monitoring rather than relying only on a perimeter. [nvlpubs.nist](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-35.pdf)

***

# Portfolio ranking

| Rank | Project | Main proof |
|---|---|---|
| 🔴 Essential | Secure SMB/branch network | Practical deployment and troubleshooting |
| 🔴 Essential | Enterprise VLAN, STP, LACP, and OSPF network | Core network engineering |
| 🔴 Essential | Firewall, DMZ, segmentation, and VPN architecture | Network security engineering |
| 🔴 Essential | Monitoring, IDS/IPS, and SIEM platform | SOC and operational security |
| 🔴 Essential | Active Directory, 802.1X, RADIUS, and AAA lab | Enterprise identity and access |
| 🔴 Essential | Network automation and configuration backup platform | Engineering productivity and reliability |
| 🟠 High Value | Hybrid cloud network with VPN and centralized logging | Cloud networking/security |
| 🟠 High Value | BGP internet edge and route-security lab | Advanced routing |
| 🟠 High Value | Vulnerability assessment and remediation platform | Security validation |
| 🟠 High Value | Incident-response network investigation lab | Security operations |
| 🟠 High Value | Secure public web infrastructure | TLS, WAF, load balancing, DMZ |
| 🟠 High Value | Network migration and documentation project | Freelance and consulting capability |
| 🟡 Useful | IPv6 dual-stack enterprise network | Future-ready operations |
| 🟡 Useful | NetFlow/IPFIX traffic-analysis platform | Visibility and threat hunting |
| 🟡 Useful | Wireless guest and corporate segmentation | SMB deployment |
| 🟡 Useful | Backup and disaster-recovery network | Operational resilience |
| 🟢 Advanced | VXLAN/EVPN data-center fabric | Data-center specialization |
| 🟢 Advanced | SD-WAN multi-site architecture | Enterprise WAN specialization |
| 🟢 Advanced | BGP/RPKI/route-leak defense lab | Internet-routing security |
| 🟢 Advanced | Kubernetes network-security architecture | Cloud-native specialization |
| 🟢 Advanced | OT/ICS network monitoring lab | Industrial-security specialization |

***

# Flagship 1: Secure SMB network

## Objective

Design and deploy a realistic small-office network with separate corporate, guest, voice, server, IoT, and management segments.

## Business problem

A small business needs reliable internet, Wi-Fi, shared services, secure guest access, remote administration, and basic monitoring without exposing internal systems.

## Topology

```text
                         Internet
                            │
                      ISP modem/ONT
                            │
                    Firewall/router
                 WAN ───────┼─────── VPN
                            │
                         802.1Q trunk
                            │
                       Managed switch
          ┌─────────────┼─────────────┬─────────────┐
       VLAN 10        VLAN 20       VLAN 30       VLAN 40
      Corporate       Servers        Guest          Voice
          │              │             │              │
       PCs/APs        NAS/app       Wi-Fi only      IP phones
                            │
                       VLAN 50
                      Management
```

## Required components

- Firewall: pfSense, OPNsense, MikroTik, FortiGate VM, or Cisco firewall.
- Managed switch: physical or Cisco IOSvL2/Aruba/Arista lab equivalent.
- Wireless AP or virtual wireless demonstration.
- Linux server for DNS, DHCP, monitoring, and logging.
- Optional Windows Server for file sharing and identity.
- One attacker/test VM and two client VMs.

## Protocols and tools

- Ethernet, IPv4, IPv6, ARP, ICMP.
- VLAN/802.1Q, STP/RSTP, LACP.
- DHCP, DNS, NTP, NAT.
- SSH, HTTPS, SNMPv3, Syslog.
- Wireshark, tcpdump, Nmap.
- Grafana/Prometheus, Zabbix, LibreNMS, or Netdata.

## Configuration work

- Create an IP addressing and VLAN plan.
- Configure access and trunk ports.
- Configure inter-VLAN routing or firewall subinterfaces.
- Build default-deny inter-zone policies.
- Configure DHCP scopes and reservations.
- Configure DNS forwarding and local records.
- Configure guest internet-only access.
- Configure management access only from the management VLAN.
- Add DHCP snooping, port security, and STP edge protections where supported.
- Configure backups and restore testing.

## Security controls

- Corporate and guest isolation.
- Management-plane restriction.
- No direct guest access to RFC1918 internal networks.
- DNS filtering and logging.
- SSH keys and MFA where available.
- SNMPv3 instead of community-string monitoring.
- Disable unused switch ports.
- Port security and BPDU Guard.
- Firmware and configuration backup.
- Firewall rule review and logging.

## Testing

Test both allowed and denied flows:

| Test | Expected result |
|---|---|
| Corporate client → DNS | Allowed |
| Corporate client → server application | Allowed only on required port |
| Guest client → internet | Allowed |
| Guest client → corporate VLAN | Denied |
| User VLAN → switch management | Denied |
| Admin VLAN → network devices | Allowed |
| Unknown device → unused switch port | Disabled or restricted |
| New DHCP client | Correct scope, gateway, and DNS |
| VPN user → approved subnet | Allowed |
| VPN user → management subnet | Denied unless explicitly authorized |

## Troubleshooting scenarios

Intentionally introduce:

- Wrong native VLAN.
- Missing VLAN on a trunk.
- DHCP scope exhaustion.
- Incorrect DNS forwarder.
- Duplicate IP.
- Overly broad firewall rule.
- Incorrect NAT exemption.
- STP root change.
- LACP member mismatch.
- Broken return route.

## Portfolio evidence

Include:

- Requirements document.
- Logical and physical topology.
- VLAN and IP plan.
- Firewall policy matrix.
- Device configurations.
- Screenshots of valid and denied tests.
- Packet capture showing 802.1Q, DHCP, ARP, DNS, and TCP.
- Monitoring dashboard.
- Backup/restore evidence.
- Troubleshooting report.
- Security-hardening checklist.
- Lessons learned.

**Importance:** Network Engineer—Critical; Security Engineer—Critical; Freelancing—Critical; Portfolio value—Critical.  
**Difficulty:** Intermediate.

***

# Flagship 2: Enterprise routed and switched network

## Objective

Build a multi-site enterprise network with redundant switching, VLANs, OSPF, first-hop redundancy, IPv6, and a simulated internet edge.

## Business problem

An organization needs scalable connectivity across headquarters, branches, server networks, and management zones with predictable convergence and redundancy.

## Topology

```text
                         ISP-1       ISP-2
                           │           │
                    ┌──────┴───────────┴──────┐
                    │   Edge routers / BGP     │
                    └──────────┬──────────────┘
                               │
                         Core-1 ═══ Core-2
                           ║          ║
                     ┌─────╨──────────╨─────┐
                     │ Distribution pair     │
                     └───────┬───────┬───────┘
                             │       │
                         Access-1  Access-2
                        /   |   \       │
                    Users Voice APs   Servers
                           
          Branch-1 ── WAN/VPN ── Headquarters
          Branch-2 ── WAN/VPN ── Headquarters
```

## Protocols

- Ethernet, VLAN/802.1Q.
- RSTP/MSTP and LACP.
- IPv4/IPv6 and ICMP.
- OSPF/OSPFv3.
- BGP at the edge.
- HSRP/VRRP.
- DHCP relay, DNS, NTP.
- ACLs, IPsec, SNMPv3, Syslog.
- NetFlow/IPFIX.
- LLDP/CDP.

## Configuration techniques

- Hierarchical campus design.
- Routed access or traditional Layer-2 access.
- Loopback-based router IDs.
- OSPF areas and summarization.
- Passive interfaces.
- First-hop redundancy with tracking.
- LACP port channels.
- STP root placement.
- IPv6 dual stack.
- Route filtering and default-route control.
- Management VRF or dedicated management segment.

## Testing

- Shut down a core link and verify convergence.
- Shut down an active gateway and verify HSRP/VRRP failover.
- Remove one LACP member.
- Change OSPF cost and verify path selection.
- Inject a test route and verify filtering.
- Test IPv4 and IPv6 independently.
- Verify that a user VLAN cannot reach management or database segments.
- Generate flow data and correlate it with logs.

Cisco’s enterprise design material emphasizes hierarchical campus design, stable routing domains, and loopback interfaces for routing stability.  Cisco’s OSPF documentation also covers routed-access design and current configuration practices. [cisco](https://www.cisco.com/c/dam/global/shared/assets/pdf/cisco_enterprise_campus_infrastructure_design_guide.pdf)

## Portfolio evidence

- High-level and low-level design.
- Failure-domain analysis.
- IP addressing and summarization plan.
- OSPF neighbor and route tables.
- STP root and port-role evidence.
- HSRP/VRRP failover screenshots.
- IPv6 test results.
- Packet captures.
- Change plan and rollback plan.
- Performance and convergence measurements.

**Importance:** Network Engineer—Critical; Security Engineer—High; Freelancing—High; Portfolio value—Critical.  
**Difficulty:** Advanced.

***

# Flagship 3: Firewall, DMZ, segmentation, and VPN

## Objective

Build a layered security architecture containing internet, DMZ, internal, server, management, and remote-access zones.

## Business problem

A company must expose public services without exposing internal systems and must provide secure remote and site-to-site access.

## Topology

```text
                         Internet
                            │
                     Edge firewall / HA pair
                    ┌───────┼────────┐
                   DMZ   Internal   VPN
                    │       │        │
              Reverse proxy  │   Remote users
              Web/WAF         │
                       ┌──────┴──────┐
                       │ Internal FW │
                       └──┬────┬─────┘
                       Users Servers Databases
```

## Technologies

- pfSense/OPNsense, FortiGate, Palo Alto VM, Cisco FTD, or equivalent.
- IPsec/IKEv2, WireGuard, OpenVPN.
- NAT, ACLs, stateful firewall rules.
- TLS certificates and reverse proxy.
- DMZ, VLANs, routing, DNS split horizon.
- Suricata or Snort.
- Syslog and flow export.

## Configuration work

- Define zones and trust boundaries.
- Use explicit source/destination/service rules.
- Configure destination NAT only for required public services.
- Add separate management access.
- Build site-to-site IPsec.
- Build remote-access VPN with per-user authorization.
- Configure split tunneling deliberately.
- Create NAT exemptions for VPN traffic.
- Configure certificate-based TLS for public services.
- Enable security logging and alerting.

## Security tests

- Internet scan of the public address.
- Verify only intended ports are exposed.
- Test DMZ-to-internal restrictions.
- Test remote-user access to approved resources.
- Test revoked VPN user.
- Test invalid IPsec proposal.
- Test route leak and asymmetric routing.
- Test firewall logging and alert generation.
- Validate that management interfaces are not internet-accessible.

## Portfolio evidence

- Zone model and data-flow diagram.
- Firewall rule matrix with business justification.
- NAT and VPN design.
- IPsec phase 1/phase 2 evidence.
- Certificate chain.
- Nmap exposure report.
- Suricata alerts.
- Before/after hardening results.
- Rule-review and cleanup procedure.

**Importance:** Network Engineer—High; Security Engineer—Critical; Freelancing—Critical; Portfolio value—Critical.  
**Difficulty:** Advanced.

***

# Flagship 4: Monitoring, IDS/IPS, and SIEM

## Objective

Create a security monitoring platform that collects device logs, network metadata, IDS alerts, authentication events, and endpoint telemetry.

## Business problem

Organizations cannot secure or troubleshoot infrastructure they cannot observe. This project demonstrates detection, triage, investigation, and operational monitoring.

## Topology

```text
Switch/router/firewall ── Syslog ──┐
                                   │
Servers/endpoints ── agents ───────┼── SIEM
                                   │
Network TAP/SPAN ── Zeek/Suricata ─┘
                                   │
                         Dashboards and alerts
```

## Tools

Choose a coherent stack rather than installing everything:

### Open-source stack

- Security Onion.
- Zeek.
- Suricata.
- Wazuh.
- OpenSearch/Elastic.
- Grafana.
- TheHive/Cortex if desired.

### Infrastructure monitoring stack

- Zabbix or LibreNMS.
- Prometheus exporters.
- Grafana.
- SNMPv3.
- Syslog collector.
- NetFlow/IPFIX collector.

Security Onion documents Zeek protocol metadata and Suricata’s signature-based network threat detection capabilities.  Wazuh provides file-integrity monitoring, malware detection, security configuration assessment, and active response functionality. [docs.securityonion](https://docs.securityonion.net/en/3/main/suricata/)

## Detection scenarios

Generate only authorized lab traffic:

- Port scanning with Nmap.
- Repeated failed SSH logins.
- DNS tunneling simulation using controlled test domains.
- Suspicious user-agent traffic.
- Web-shell-like test request against a deliberately vulnerable lab app.
- ARP spoofing in an isolated lab.
- Unauthorized SMB access.
- New admin account creation.
- Unusual outbound connection.
- Malware test file such as EICAR in a disposable lab.

## What to demonstrate

- Packet capture.
- Zeek connection, DNS, HTTP, and SSL/TLS logs.
- Suricata alert and rule metadata.
- Wazuh endpoint event.
- SIEM correlation.
- Alert severity and triage.
- Investigation timeline.
- Containment action.
- False-positive tuning.
- Retention and dashboard design.

## Metrics

Track:

- Mean time to detect.
- Mean time to acknowledge.
- Mean time to contain.
- Alert volume.
- False-positive rate.
- Log ingestion delay.
- Packet-loss rate.
- Sensor CPU/memory.
- Storage growth.
- Coverage by asset and protocol.

**Importance:** Network Engineer—High; Security Engineer—Critical; Freelancing—Medium; Portfolio value—Critical.  
**Difficulty:** Advanced.

***

# Flagship 5: Active Directory, AAA, and NAC

## Objective

Build an identity-aware enterprise access architecture using Active Directory, DNS, Kerberos, LDAP, RADIUS, TACACS+, and 802.1X.

## Business problem

Shared passwords and unrestricted internal access make it difficult to control users, devices, administrators, and network access.

## Topology

```text
                        AD/DNS/DHCP
                             │
                       RADIUS/NPS
                             │
Users ── 802.1X ── Switch/AP ── VLAN assignment
                             │
                     Network devices
                             │
                       TACACS+ AAA
```

## Components

- Windows Server domain controller.
- Windows clients.
- Linux server joined to the domain or using LDAP/Kerberos.
- FreeRADIUS or Microsoft NPS.
- Managed switch with 802.1X support.
- Wireless AP or simulated WLAN.
- TACACS+ server.
- Wazuh agent and Sysmon on Windows.
- DNS and DHCP.

## Configuration work

- Build AD forest/domain.
- Configure secure DNS and time synchronization.
- Create users, groups, service accounts, and administrative tiers.
- Apply Group Policy.
- Configure SMB shares with least privilege.
- Configure RADIUS authentication and accounting.
- Configure 802.1X EAP method.
- Assign dynamic VLANs.
- Configure TACACS+ command authorization.
- Join Linux systems to the domain.
- Restrict privileged logon paths.

## Security scenarios

- Disable a user and verify access revocation.
- Test a non-domain device.
- Test wrong certificate or EAP credentials.
- Attempt access from an unauthorized VLAN.
- Detect excessive failed authentication.
- Test SMB share access by role.
- Review Kerberos and LDAP events.
- Simulate a compromised workstation and investigate lateral access.

## Portfolio evidence

- Identity and trust-zone diagram.
- Group and role model.
- RADIUS authentication sequence.
- 802.1X packet capture.
- Group Policy security baseline.
- AD audit policy.
- SMB access matrix.
- TACACS+ command-accounting logs.
- Failed-login investigation.

**Importance:** Network Engineer—High; Security Engineer—Critical; Freelancing—High; Portfolio value—Critical.  
**Difficulty:** Advanced.

***

# Flagship 6: Cloud hybrid network

## Objective

Connect an on-premises lab to a cloud network using VPN or dedicated-connectivity concepts, with private subnets, routing, segmentation, logging, and secure application exposure.

## Topology

```text
On-prem lab
   │
IPsec VPN / simulated Direct Connect
   │
Cloud transit hub
   ├── Public subnet ── Load balancer/WAF
   ├── Private app subnet
   ├── Private database subnet
   └── Management subnet
```

## Cloud components

- AWS VPC, Azure VNet, or GCP VPC.
- Public and private subnets.
- Route tables.
- Security groups.
- Network ACLs.
- NAT gateway.
- Cloud VPN.
- Load balancer.
- Private endpoint.
- Cloud DNS.
- Flow logs.
- Cloud monitoring and alerting.

Cloud security groups operate at resource/interface level, while network ACLs operate at subnet level; cloud flow logs help diagnose overly restrictive or permissive rules. [docs.aws.amazon](https://docs.aws.amazon.com/whitepapers/latest/aws-best-practices-ddos-resiliency/security-groups-and-network-acls-bp5.html)

## Configuration work

- Avoid overlapping CIDRs.
- Build public/private route tables.
- Restrict database access to application security groups.
- Use NAT for controlled outbound access.
- Deploy a load balancer with TLS.
- Enable VPC/VNet flow logs.
- Configure VPN routes and tunnel failover.
- Add cloud IAM least privilege.
- Use private endpoints for managed services.
- Test cross-account or cross-VPC access only where required.

## Testing

- Public user → load balancer → application.
- Public user → database: denied.
- Application → database on required port: allowed.
- Private server → internet through NAT: allowed.
- Internet → private server: denied.
- On-prem → approved cloud subnet: allowed.
- Cloud → unauthorized on-prem subnet: denied.
- VPN tunnel failure and recovery.
- Flow log generation and alerting.

**Importance:** Network Engineer—High; Security Engineer—Critical; Freelancing—High; Portfolio value—Critical.  
**Difficulty:** Advanced.

***

# Focused project categories

The six flagship projects cover most categories, but the following focused projects can be included as components or standalone case studies.

## A. Network engineering projects

### 1. IPv6 dual-stack enterprise

- **Objective:** Deploy IPv4 and IPv6 simultaneously across VLANs and routed links.
- **Business problem:** Modern systems require IPv6 readiness without breaking IPv4.
- **Topology:** Dual-stack access, distribution, server, and internet-edge network.
- **Protocols:** IPv6, ICMPv6, NDP, DHCPv6, OSPFv3, DNS A/AAAA.
- **Tests:** RA failure, duplicate address detection, PMTU, IPv6 ACLs, DNS preference.
- **Difficulty:** High.
- **Value:** Network Engineer—High; Security Engineer—High; Freelance—Medium.

### 2. Redundant campus network

- **Objective:** Prove failure recovery through dual core, HSRP/VRRP, STP, and LACP.
- **Business problem:** Avoid outages caused by single links or devices.
- **Tests:** Link, switch, gateway, and routing failures.
- **Difficulty:** High.
- **Value:** Network Engineer—Critical; Security Engineer—High; Freelance—High.

### 3. BGP internet edge

- **Objective:** Simulate two ISPs with eBGP, inbound/outbound policy, and route filtering.
- **Business problem:** Multihoming, traffic engineering, and route resilience.
- **Security controls:** Prefix limits, bogon filtering, max-prefix, authentication, RPKI concepts.
- **Difficulty:** Advanced.
- **Value:** Network Engineer—Critical; Security Engineer—High; Freelance—Low.

## B. Enterprise networking projects

### 4. Multi-site OSPF network

- **Objective:** Connect headquarters, branches, and data center with OSPF areas.
- **Business problem:** Scalable internal routing and predictable convergence.
- **Evidence:** Neighbor state, LSDB, route summaries, convergence measurement.
- **Difficulty:** High.
- **Value:** Network Engineer—Critical; Security Engineer—High; Freelance—High.

### 5. DMZ architecture

- **Objective:** Host public web, DNS, mail, and reverse-proxy services in controlled zones.
- **Business problem:** Public services must not expose internal networks.
- **Security controls:** NAT, WAF, TLS, internal firewall, least privilege, logging.
- **Difficulty:** High.
- **Value:** Network Engineer—High; Security Engineer—Critical; Freelance—High.

### 6. Zero-trust segmentation

- **Objective:** Design resource-based access rather than trusting network location.
- **Business problem:** Limit lateral movement and enforce least privilege.
- **Evidence:** Asset inventory, policy matrix, segmentation, monitoring, validation.
- **Difficulty:** Advanced.
- **Value:** Network Engineer—High; Security Engineer—Critical; Freelance—Medium.

NIST describes zero trust as a shift away from static perimeter assumptions toward protection of users, assets, and resources.  Its implementation guidance emphasizes discovering assets, defining policy, segmenting resources, deploying enforcement points, and monitoring. [nvlpubs.nist](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1800-35.pdf)

## C. Network security projects

### 7. Network hardening baseline

Create a baseline for routers, switches, firewalls, Linux, and Windows:

- Disable insecure services.
- Use SSH/HTTPS.
- Restrict management sources.
- Configure AAA.
- Synchronize time.
- Enable logging.
- Use SNMPv3.
- Secure STP and DHCP.
- Back up configurations.
- Validate firmware and vulnerability status.

### 8. Security validation lab

- Build a known vulnerable network.
- Scan it with Nmap and authenticated vulnerability tools.
- Validate findings manually.
- Remediate.
- Rescan.
- Document false positives and compensating controls.

Never scan networks without explicit authorization.

## D. Firewall projects

### 9. Firewall policy engineering

Create a policy lifecycle:

```text
Business requirement
 → flow matrix
 → rule design
 → implementation
 → test
 → logging
 → review
 → cleanup
```

Demonstrate object groups, service groups, NAT, zones, rule ordering, logging, change approval, and rollback.

### 10. Firewall migration

Migrate from a flat router ACL to a segmented next-generation firewall:

- Inventory current flows.
- Map dependencies.
- Create temporary logging rules.
- Build least-privilege policy.
- Test cutover.
- Execute rollback plan.
- Compare exposure before and after.

This is highly relevant to freelance and consulting work.

## E. VPN projects

### 11. Site-to-site IPsec/WireGuard comparison

Build the same topology using IPsec and WireGuard:

```text
Branch LAN ── VPN tunnel ── HQ LAN
```

Demonstrate:

- Routing.
- NAT exemption.
- Encryption.
- Key/certificate management.
- Tunnel failure.
- MTU.
- Logging.
- User/device authorization.

### 12. Remote-access VPN

- Per-user authentication.
- MFA.
- Split tunnel versus full tunnel.
- DNS behavior.
- Device posture assumptions.
- Revocation.
- Session logging.
- Least-privilege access.

## F. Network monitoring projects

### 13. Infrastructure monitoring platform

Use LibreNMS, Zabbix, or Prometheus/Grafana to monitor:

- Interface state.
- Errors and discards.
- CPU and memory.
- Temperature and power.
- Bandwidth.
- BGP/OSPF neighbors.
- VPN tunnels.
- DHCP scope usage.
- DNS response time.
- Certificate expiry.

### 14. NetFlow/IPFIX traffic analysis

- Configure exporters.
- Collect source/destination, ports, bytes, packets, and timestamps.
- Identify top talkers.
- Detect scanning, beaconing, data transfer, and unusual egress.
- Correlate flow data with firewall and endpoint logs.

## G. IDS/IPS projects

### 15. Suricata inline and passive comparison

- Deploy passive IDS using SPAN/TAP.
- Deploy inline IPS in a safe lab.
- Test signatures using approved test traffic.
- Tune noisy rules.
- Demonstrate false-positive handling.
- Document prevention versus detection tradeoffs.

### 16. Zeek network security monitoring

- Collect DNS, HTTP, TLS, SSH, SMB, and connection logs.
- Create custom detections.
- Hunt for unusual protocols, long-lived connections, and suspicious DNS.
- Feed metadata into the SIEM.

## H. SIEM/SOC projects

### 17. Mini SOC

Sources:

- Firewall.
- Router/switch Syslog.
- Suricata.
- Zeek.
- Windows Event Logs.
- Sysmon.
- Linux audit logs.
- Wazuh.
- DNS/DHCP.
- Cloud flow logs.

Create playbooks for:

- Port scan.
- Brute-force login.
- Suspicious DNS.
- Unauthorized admin account.
- Malware alert.
- Lateral SMB movement.
- Data exfiltration simulation.

## I. Active Directory and enterprise security

### 18. AD security baseline

Demonstrate:

- Tiered administration.
- Group Policy.
- Windows Firewall.
- Defender.
- PowerShell logging.
- Sysmon.
- LDAP signing/channel binding where supported.
- Kerberos and time.
- SMB hardening.
- Restricted admin access.
- Backup and recovery.

### 19. AD attack-and-defend lab

In an isolated authorized lab:

- Create a vulnerable configuration.
- Demonstrate password spraying or Kerberoasting safely.
- Detect the activity.
- Remediate the configuration.
- Rescan and verify.

Do not use real credentials or production systems.

## J. Network access control

### 20. 802.1X NAC

```text
Endpoint ── EAPOL ── Switch/AP ── RADIUS ── AD/LDAP
```

Demonstrate:

- Supplicant configuration.
- EAP-TLS or PEAP.
- Certificate validation.
- Dynamic VLAN assignment.
- Guest/failed-auth VLAN.
- MAC authentication bypass limitations.
- Accounting and revocation.

## K. Vulnerability assessment

### 21. Network vulnerability management lifecycle

```text
Asset inventory
 → authenticated scan
 → prioritize
 → remediate
 → validate
 → report trend
```

Tools may include Nmap, Greenbone/OpenVAS, Nessus Essentials where appropriate, Nuclei for authorized web testing, and vendor configuration assessors.

Deliver:

- Scope.
- Authorization.
- Scan profile.
- Findings.
- Risk rating.
- Evidence.
- Remediation.
- Validation scan.
- Exceptions and compensating controls.

## L. Incident response

### 22. Network intrusion investigation

Scenario:

```text
Compromised workstation → DNS beaconing → external server
          │
          └── lateral SMB attempt → file server
```

Use:

- PCAP.
- Zeek.
- Suricata.
- Firewall logs.
- DNS logs.
- Windows events.
- Wazuh.
- Timeline analysis.

Document:

- Detection.
- Triage.
- Scope.
- Containment.
- Eradication.
- Recovery.
- Lessons learned.

## M. Secure web infrastructure

### 23. Public web application architecture

```text
Internet → DNS/CDN/WAF → load balancer → reverse proxy → app → database
```

Demonstrate:

- TLS certificates.
- HTTP security headers.
- WAF policies.
- Private database subnet.
- Health checks.
- Access logging.
- WebSocket or HTTP/3 considerations.
- Backup and rollback.
- Rate limiting.
- Vulnerability testing.

## N. Cloud networking/security

### 24. Cloud landing-zone network

Build:

- Shared services network.
- Transit hub.
- Workload VPCs/VNets.
- Public/private subnets.
- Security groups.
- NACLs.
- Flow logs.
- VPN.
- Private endpoints.
- WAF/load balancer.
- Central logging.

AWS documentation distinguishes instance-level security groups from subnet-level network ACLs and recommends flow logs and security analysis for visibility. [docs.aws.amazon](https://docs.aws.amazon.com/whitepapers/latest/aws-best-practices-ddos-resiliency/security-groups-and-network-acls-bp5.html)

## O. Network automation projects

### 25. Network automation platform

**Objective:** Automate inventory, configuration, validation, and reporting.

```text
Git repository
      │
CI/CD pipeline
      │
Ansible/Python controller
      │
Routers ─ Switches ─ Firewalls
      │
Telemetry/config results
```

Implement:

- YAML inventory.
- Secrets handling.
- Device reachability.
- Configuration templates.
- Dry-run mode.
- Idempotency.
- Pre-check and post-check.
- Automatic rollback.
- Git change history.
- Test reports.

Tools:

- Python.
- Netmiko.
- NAPALM.
- Ansible.
- Jinja2.
- Nornir.
- REST APIs.
- NETCONF.
- RESTCONF.
- YANG.
- GitHub Actions.

Ansible provides modules for RESTCONF configuration on RESTCONF-enabled devices, illustrating the move toward model-driven automation. [docs.ansible](https://docs.ansible.com/projects/ansible/latest/collections/ansible/netcommon/restconf_config_module.html)

### 26. Configuration backup system

Build a service that:

- Discovers devices.
- Connects using SSH/API.
- Saves sanitized configurations.
- Encrypts secrets.
- Stores version history.
- Shows diffs.
- Alerts on unauthorized changes.
- Tests restore procedures.
- Produces compliance reports.

### 27. Network security configuration auditor

Check:

- Telnet disabled.
- SSH enabled.
- Strong local credentials.
- AAA configured.
- SNMPv3 used.
- NTP configured.
- Syslog configured.
- Unused ports disabled.
- BPDU Guard enabled.
- DHCP snooping enabled.
- Management ACL present.
- No `0.0.0.0/0` administrative exposure.
- Firewall rules documented.
- Firmware within policy.

Output:

```text
Device | Check | Result | Evidence | Remediation
```

### 28. Network diagnostics tool

Build a Python tool that performs:

- DNS lookup.
- TCP connectivity test.
- ICMP test.
- Traceroute.
- TLS certificate check.
- HTTP status test.
- Route-table inspection.
- ARP/neighbor inspection.
- MTU test.
- JSON/HTML report generation.

Make it useful for freelance troubleshooting, not just a wrapper around commands.

## P. Configuration compliance

### 29. Golden configuration and drift detection

- Define policy as code.
- Compare running configurations to approved baselines.
- Detect unauthorized changes.
- Open a ticket or create a report.
- Support exceptions with expiration dates.
- Run pre-change and post-change validation.

## Q. Freelance/SMB projects

### 30. Small-office deployment package

Deliver:

- Requirements interview.
- Inventory.
- Floor plan and cable map.
- IP/VLAN plan.
- Firewall and Wi-Fi design.
- Configuration.
- Validation.
- User handover.
- Monitoring.
- Backup.
- Documentation.

### 31. Office Wi-Fi and guest isolation

- Corporate SSID.
- Guest SSID.
- VLAN mapping.
- Captive portal where appropriate.
- Client isolation.
- Rate limiting.
- Roaming and coverage validation.
- Rogue AP review.
- WPA2/WPA3 configuration.
- Monitoring and heatmap evidence.

### 32. Network migration

Migrate from:

```text
Flat LAN + consumer router
```

to:

```text
Firewall + managed switch + VLANs + business Wi-Fi + monitoring
```

Demonstrate:

- Discovery.
- Dependency mapping.
- Cutover plan.
- Backup.
- Rollback.
- Downtime communication.
- Post-migration validation.

### 33. Small-business disaster recovery

- Configuration backup.
- Cloud/offsite backup.
- Spare equipment plan.
- ISP failure procedure.
- Firewall restore.
- Critical service recovery.
- Recovery Time Objective and Recovery Point Objective.
- Restore test evidence.

### 34. Small-business hardening assessment

Produce a professional report covering:

- External exposure.
- Firewall configuration.
- Wi-Fi security.
- VLANs.
- Admin accounts.
- Patch status.
- Backups.
- Logging.
- Endpoint protection.
- MFA.
- Email authentication.
- Incident-response contacts.

## R. Advanced/professional projects

### 35. VXLAN/EVPN data-center fabric

Demonstrate:

- Layer-3 underlay.
- Loopbacks.
- BGP EVPN control plane.
- VTEPs and VNIs.
- Anycast gateway.
- Tenant segmentation.
- MAC mobility.
- Failure convergence.

### 36. SD-WAN multi-site design

Demonstrate:

- Multiple underlays.
- Controller/orchestrator.
- Application-aware routing.
- SLA probes.
- Segmentation.
- Local internet breakout.
- Centralized policy.
- Tunnel failure and brownout handling.

### 37. RPKI and BGP route security

Demonstrate:

- Valid, invalid, and not-found route origins.
- Prefix filtering.
- Max-prefix protection.
- Route leak simulation in a lab.
- Monitoring and alerting.

***

# Three Python-heavy projects

## 1. Network automation platform

### Features

- Device inventory.
- Vendor abstraction.
- SSH/API connectivity.
- Configuration templates.
- Pre-checks.
- Change approval.
- Dry-run diff.
- Deployment.
- Post-checks.
- Rollback.
- Git integration.
- HTML reports.

### Architecture

```text
Web UI/API → job queue → Python workers → Netmiko/NAPALM/NETCONF
                    │
                    ├── Git
                    ├── Vault/secrets
                    └── SQLite/PostgreSQL
```

### Portfolio proof

Show a change that:

1. Validates the device.
2. Creates a diff.
3. Requires approval.
4. Applies configuration.
5. Verifies reachability and routing.
6. Rolls back when a test fails.

## 2. Configuration backup and compliance system

### Features

- Scheduled backups.
- Encrypted storage.
- Config diff.
- Secret redaction.
- Baseline checks.
- Drift alerts.
- Compliance score.
- Restore test.

### Portfolio proof

Demonstrate an unauthorized SSH configuration change, detection, diff, alert, remediation, and audit trail.

## 3. Network diagnostics and security auditor

### Features

- DNS, TCP, ICMP, HTTP, TLS, route, and MTU checks.
- Nmap integration for authorized scopes.
- Device configuration checks.
- JSON and HTML reports.
- Severity scoring.
- Remediation suggestions.
- Evidence collection.

### Safety design

- Require explicit target scope.
- Use allowlists.
- Rate-limit scans.
- Require confirmation before active scanning.
- Clearly label authorized-lab mode.
- Never provide destructive actions.

***

# What to document for every flagship project

Use the same professional structure for all six projects.

## 1. Requirements

- Business context.
- Users and locations.
- Applications.
- Availability requirements.
- Security requirements.
- Performance expectations.
- Budget or resource constraints.
- Assumptions and exclusions.

## 2. Architecture

- Executive summary.
- Logical topology.
- Physical/virtual topology.
- Trust zones.
- Traffic flows.
- Failure domains.
- Management plane.
- Data plane.
- Control plane.

## 3. Addressing and segmentation

- IPv4 plan.
- IPv6 plan.
- VLAN table.
- Subnet purpose.
- DHCP scope.
- Gateway.
- DNS zone.
- Route summary.
- Security zone.

Example:

| VLAN | Name | Subnet | Gateway | Trust |
|---:|---|---|---|---|
| 10 | Corporate | `10.10.10.0/24` | `10.10.10.1` | Internal |
| 20 | Servers | `10.10.20.0/24` | `10.10.20.1` | Restricted |
| 30 | Guest | `10.10.30.0/24` | `10.10.30.1` | Internet only |
| 40 | Voice | `10.10.40.0/24` | `10.10.40.1` | Limited |
| 50 | Management | `10.10.50.0/24` | `10.10.50.1` | Privileged |

## 4. Configuration

Include:

- Sanitized device configurations.
- Interface and trunk configuration.
- Routing configuration.
- Firewall rules.
- VPN configuration.
- AAA.
- Monitoring.
- Backup.
- Automation playbooks.
- Version and platform details.

Never publish real credentials, private keys, public IPs, client names, or sensitive logs.

## 5. Security policy

Document:

- Source.
- Destination.
- Protocol/port.
- Action.
- Business justification.
- Logging.
- Owner.
- Review date.
- Expiration date for temporary rules.

## 6. Test cases

For each test:

```text
Test ID:
Objective:
Source:
Destination:
Protocol/port:
Expected result:
Observed result:
Evidence:
Status:
```

Include positive, negative, failure, recovery, and security tests.

## 7. Troubleshooting

Show:

- Symptom.
- Initial hypothesis.
- Commands and evidence.
- Packet capture.
- Root cause.
- Fix.
- Validation.
- Preventive control.

## 8. Monitoring

Document:

- What is collected.
- Where it is stored.
- Retention.
- Alert thresholds.
- Dashboards.
- Escalation.
- False-positive tuning.
- Health checks.

## 9. Attack/security testing

Only test systems you own or are explicitly authorized to test. Use isolated labs and safe test artifacts.

Document:

- Scope and authorization.
- Tool and version.
- Target.
- Time window.
- Expected impact.
- Finding.
- Evidence.
- Remediation.
- Validation result.

## 10. README and evidence

Each repository should include:

```text
README.md
docs/
  requirements.md
  architecture.md
  addressing-plan.md
  security-policy.md
  test-plan.md
  troubleshooting.md
  incident-report.md
diagrams/
configs/
automation/
monitoring/
screenshots/
CHANGELOG.md
LICENSE
```

***

# Recommended roadmap

## Phase 1 — Networking fundamentals

### Build

- Packet-level Linux lab.
- Network diagnostics tool.
- IPv4/IPv6 addressing and troubleshooting lab.

### Learn first

- Ethernet.
- MAC, ARP, IPv4, IPv6.
- ICMP.
- TCP/UDP.
- Subnetting, MTU, routing table.

### Tools

- Linux network namespaces.
- Wireshark.
- tcpdump.
- `ip`, `ss`, `ping`, `traceroute`, `dig`.
- Nmap in an authorized lab.

### Move on when you can

- Explain a packet’s path.
- Identify Layer 2 versus Layer 3 versus Layer 4 failure.
- Diagnose wrong gateway, duplicate IP, MTU, DNS, and TCP-port problems.

## Phase 2 — Switching

### Build

- SMB VLAN and switching lab.
- STP/RSTP/LACP failure lab.

### Learn first

- VLAN/802.1Q.
- Access/trunk.
- MAC learning.
- STP/RSTP/MSTP.
- LACP.
- DHCP snooping and port security.

### Tools

- Cisco IOSvL2, Aruba/Arista lab images, or physical managed switch.
- EVE-NG/GNS3.
- Wireshark.

### Move on when you can

- Configure a trunk.
- Explain a tagged frame.
- Fix a native VLAN issue.
- Identify the STP root.
- Recover from a loop.
- Validate an LACP bundle.

## Phase 3 — Routing

### Build

- Multi-router OSPF network.
- IPv6 OSPFv3 network.
- HSRP/VRRP redundancy lab.

### Learn first

- Static/default routes.
- OSPF.
- OSPFv3.
- First-hop redundancy.
- ACLs.
- DHCP relay.

### Tools

- EVE-NG/GNS3.
- FRRouting.
- Cisco/Juniper virtual images where legally available.
- Wireshark.

### Move on when you can

- Troubleshoot an OSPF adjacency.
- Explain route selection.
- Configure summarization.
- Validate failover and convergence.
- Restrict routing and inter-VLAN traffic with ACLs.

## Phase 4 — Enterprise networking

### Build

- Multi-site enterprise network.
- BGP internet-edge lab.
- IPv6 dual-stack deployment.

### Learn first

- BGP.
- Route policy.
- Prefix filtering.
- HSRP/VRRP.
- Multisite design.
- Network documentation.

### Tools

- EVE-NG/GNS3.
- FRRouting.
- Git.
- draw.io/diagrams.net.
- NetBox or Nautobot.

### Move on when you can

- Build a stable multi-site topology.
- Apply BGP policies.
- Prevent route leaks in a lab.
- Explain failure domains and convergence.
- Produce a professional HLD/LLD.

## Phase 5 — Network security

### Build

- Segmented network.
- DHCP snooping/DAI/port security.
- Secure management baseline.
- Zero-trust segmentation prototype.

### Learn first

- Firewall zones.
- ACL design.
- AAA.
- SSH.
- SNMPv3.
- Syslog.
- Management-plane protection.
- IPv6 security.

### Tools

- pfSense/OPNsense.
- Cisco/Aruba virtual switch.
- FreeRADIUS.
- Wazuh.
- OpenSCAP where appropriate.

### Move on when you can

- Write a least-privilege flow matrix.
- Secure device administration.
- Detect rogue DHCP and ARP behavior.
- Explain why network location alone is not identity.

## Phase 6 — Firewall/VPN

### Build

- Firewall/DMZ project.
- IPsec site-to-site VPN.
- WireGuard remote-access VPN.
- Firewall migration project.

### Learn first

- NAT.
- Stateful inspection.
- IPsec/IKE.
- VPN routing.
- TLS.
- Reverse proxy.
- Rule lifecycle.

### Tools

- pfSense/OPNsense.
- StrongSwan.
- WireGuard.
- Nginx/HAProxy.
- OpenVPN.

### Move on when you can

- Diagnose both phases of IPsec.
- Explain tunnel versus route failure.
- Expose a DMZ service safely.
- Produce firewall rules with business justification and rollback.

## Phase 7 — Monitoring/IDS/SIEM

### Build

- Mini SOC.
- Infrastructure monitoring.
- NetFlow/IPFIX analysis.
- Suricata and Zeek lab.

### Learn first

- Syslog.
- SNMPv3.
- Flow telemetry.
- Packet capture.
- IDS signatures.
- Event correlation.
- Alert triage.

### Tools

- Security Onion.
- Zeek.
- Suricata.
- Wazuh.
- Elastic/OpenSearch.
- Grafana.
- Zabbix/LibreNMS.

### Move on when you can

- Detect and investigate a controlled scan.
- Correlate firewall, DNS, endpoint, and IDS events.
- Tune a noisy alert.
- Write an incident timeline.

## Phase 8 — Windows/AD security

### Build

- AD/AAA/NAC project.
- AD security baseline.
- Authorized attack-and-defend lab.

### Learn first

- DNS and Kerberos.
- LDAP/LDAPS.
- SMB.
- Group Policy.
- RADIUS.
- TACACS+.
- 802.1X.
- Windows event logging.

### Tools

- Windows Server.
- Windows clients.
- Linux.
- FreeRADIUS/NPS.
- Sysmon.
- Wazuh.
- BloodHound only in an authorized lab.

### Move on when you can

- Explain why DNS and time affect Kerberos.
- Configure role-based access.
- Implement 802.1X.
- Investigate failed authentication and lateral movement.
- Harden a domain without breaking operations.

## Phase 9 — Cloud networking/security

### Build

- Hybrid cloud network.
- Cloud landing zone.
- Public web architecture with private backend.

### Learn first

- VPC/VNet.
- Route tables.
- Security groups/NSGs.
- NACLs.
- NAT.
- VPN.
- Load balancers.
- Flow logs.
- IAM and private endpoints.

### Tools

- Choose AWS, Azure, or GCP first.
- Terraform.
- Cloud CLI.
- Cloud monitoring.
- Packer or Ansible.

### Move on when you can

- Design public/private subnets.
- Explain route-table versus security-group failure.
- Secure a private database.
- Enable and query flow logs.
- Connect on-premises and cloud networks.

## Phase 10 — Automation

### Build

- Network automation platform.
- Configuration backup system.
- Compliance auditor.
- Diagnostics tool.

### Learn first

- Python.
- Netmiko.
- NAPALM.
- Ansible.
- Jinja2.
- REST APIs.
- NETCONF/RESTCONF.
- YANG.
- Git and CI/CD.

### Move on when you can

- Automate idempotent changes.
- Generate a diff before deployment.
- Validate before and after a change.
- Roll back safely.
- Protect secrets.
- Produce audit evidence.

## Phase 11 — Full enterprise security architecture

### Build

Combine the previous work into:

```text
Multi-site enterprise
 ├── Redundant campus
 ├── OSPF/BGP
 ├── Segmented firewall/DMZ
 ├── IPsec/WireGuard
 ├── AD/802.1X/NAC
 ├── IDS/IPS/SIEM
 ├── Cloud hybrid connectivity
 ├── Automation/compliance
 └── Incident response
```

### Demonstrate

- Business requirements.
- Risk assessment.
- Architecture decision records.
- Segmentation and zero-trust policy.
- Redundancy and disaster recovery.
- Detection and response.
- Automated compliance.
- Change management.
- Measured test results.
- Operational runbooks.

NIST’s secure enterprise landscape guidance explicitly recognizes hybrid cloud, distributed resources, microsegmentation, ZTNA, and SASE as part of the modern enterprise network rather than treating the network as a single perimeter. [csrc.nist](https://csrc.nist.gov/News/2022/sp-800-215-secure-enterprise-network-landscape)

***

# Final portfolio recommendation

Build these six projects deeply rather than publishing 30 shallow repositories:

1. **Secure SMB/branch network**
2. **Redundant enterprise OSPF/BGP network**
3. **Firewall/DMZ/VPN/segmentation architecture**
4. **Monitoring/IDS/IPS/SIEM mini-SOC**
5. **AD/802.1X/RADIUS/TACACS+ enterprise identity lab**
6. **Hybrid cloud and automation/compliance platform**

For each, publish:

- Architecture.
- Addressing plan.
- VLAN and trust-zone plan.
- Configurations.
- Security policy.
- Test cases.
- Failure injection.
- Packet captures.
- Monitoring dashboards.
- Attack/defense evidence from an authorized lab.
- Automation code.
- Backup and rollback.
- Troubleshooting report.
- Lessons learned.

Your portfolio will be strongest when each project answers this question:

> “What business requirement did I solve, how did I design and secure it, how did I prove it worked, and how would I operate it at 2 a.m. during an incident?”
