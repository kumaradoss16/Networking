# Network Labs

A collection of practical **Cisco networking labs and protocol configuration exercises** built using Cisco Packet Tracer. The labs focus on network protocols, routing, network services, redundancy, device discovery, access control, and basic network security.

The purpose of this directory is to maintain hands-on configurations that can be used for **network engineering learning, troubleshooting practice, interview preparation, and practical documentation**.

---

## Lab Environment

* Cisco Packet Tracer
* Cisco IOS-based routers and switches
* IPv4 networking
* Ethernet interfaces
* Routing protocols
* Network services
* Network security features
* CLI-based configuration and verification

---

# Available Network Labs

| # | Lab                                               | Technology / Protocol | Main Purpose                 |
| - | ------------------------------------------------- | --------------------- | ---------------------------- |
| 1 | [CDP and LLDP](cdp-and-lldp/)                     | CDP, LLDP             | Neighbor discovery           |
| 2 | [DNS](dns/)                                       | DNS                   | Name resolution              |
| 3 | [EIGRP](eigrp/)                                   | EIGRP                 | Dynamic routing              |
| 4 | [Floating Static Routes](floating-static-routes/) | Static Routing        | Backup path / route failover |
| 5 | [HSRP](hsrp/)                                     | HSRP                  | First-hop gateway redundancy |
| 6 | [NTP](ntp/)                                       | NTP                   | Network time synchronization |
| 7 | [OSPF](ospf/)                                     | OSPF                  | Dynamic routing              |
| 8 | [Standard ACL](standard-acl/)                     | IPv4 ACL              | Traffic filtering            |

---

# 1. CDP and LLDP

**CDP — Cisco Discovery Protocol** and **LLDP — Link Layer Discovery Protocol** are Layer 2 neighbor-discovery protocols.

They allow network devices to discover information about directly connected neighboring devices.

### Topics Covered

* CDP
* LLDP
* Neighbor discovery
* Device identification
* Local interface information
* Remote interface information
* Network topology discovery

### Main Verification Commands

```cisco
show cdp neighbors
show cdp neighbors detail
show lldp neighbors
show lldp neighbors detail
```

### Lab Resources

The lab contains:

```text
cdp-and-lldp/
├── configs/
├── diagram/
├── lab-cdp-lldp.pkt
└── readme.md
```

The Packet Tracer lab and configuration/diagram directories are present in the repository.

---

# 2. DNS

**DNS — Domain Name System** translates hostnames and domain names into IP addresses.

Example:

```text
server.example.com
        ↓
    DNS Lookup
        ↓
192.168.10.10
```

### Topics Covered

* DNS fundamentals
* DNS server configuration
* Router DNS configuration
* Hostname resolution
* Public DNS
* DNS troubleshooting

### Important Configuration

```cisco
ip name-server <DNS-SERVER-IP>
```

Example:

```cisco
ip name-server 1.1.1.1
```

### Important Port

```text
UDP 53
TCP 53
```

### Lab Resources

```text
dns/
├── configs/
├── diagram/
├── dns.pkt
└── readme.md
```

---

# 3. EIGRP

**EIGRP — Enhanced Interior Gateway Routing Protocol** is a dynamic routing protocol used to exchange routing information between routers.

### Topics Covered

* EIGRP configuration
* Neighbor relationships
* Dynamic route advertisement
* EIGRP metrics
* Network statements
* Route verification
* Routing table analysis

### Important Commands

```cisco
router eigrp <AS-NUMBER>
network <NETWORK>
```

Verification:

```cisco
show ip eigrp neighbors
show ip route
show ip protocols
show ip eigrp topology
```

The EIGRP lab currently contains dedicated `configs`, `diagram`, and `topology` directories.

---

# 4. Floating Static Routes

A **floating static route** is a static route configured with a higher administrative distance so that it acts as a **backup route**.

Example:

```text
Primary Route
     │
     ▼
Network ─── R1 ─── R2
               \
                \
              Backup Route
```

When the primary route becomes unavailable, the floating static route can be installed in the routing table.

### Topics Covered

* Static routing
* Administrative distance
* Backup routes
* Route failover
* Primary and secondary paths
* Basic redundancy

### Important Configuration

Example:

```cisco
ip route <NETWORK> <MASK> <NEXT-HOP>
```

Floating route:

```cisco
ip route <NETWORK> <MASK> <NEXT-HOP> 200
```

The higher administrative distance makes the second route less preferred.

The lab contains a README, `configs`, `diagram`, and `topology` directories.

---

# 5. HSRP

**HSRP — Hot Standby Router Protocol** provides default-gateway redundancy for hosts in a LAN.

Instead of depending on a single router:

```text
       PC
        |
   Default Gateway
        |
       R1
```

HSRP provides redundant routers:

```text
              Virtual Gateway
                   │
             192.168.10.1
                   │
             ┌─────┴─────┐
             │           │
            R1           R2
          Active        Standby
```

If the active router becomes unavailable, another router can take over the gateway role.

### Topics Covered

* HSRP
* Active router
* Standby router
* Virtual IP address
* Gateway redundancy
* Priority
* Preemption
* Failover

### Important Commands

```cisco
standby 1 ip <VIRTUAL-IP>
standby 1 priority <VALUE>
standby 1 preempt
```

Verification:

```cisco
show standby
```

The repository contains the HSRP Packet Tracer file, configuration directory, diagram directory, and README.

---

# 6. NTP

**NTP — Network Time Protocol** synchronizes the clocks of network devices.

Accurate time is important for:

* Network logs
* Troubleshooting
* Security investigations
* Monitoring
* Event correlation

### Basic Architecture

```text
              NTP Server
                   |
        ┌──────────┼──────────┐
        |          |          |
       R1         R2         SW1
```

### Important Port

```text
UDP 123
```

### Cisco Configuration

```cisco
ntp server <NTP-SERVER-IP>
```

Example:

```cisco
ntp server 192.168.10.10
```

### Verification

```cisco
show ntp status
show ntp associations
```

The NTP lab contains `ntp.pkt`, configuration references, topology/diagram resources, and documentation.

---

# 7. OSPF

**OSPF — Open Shortest Path First** is a link-state dynamic routing protocol used to exchange routing information within an autonomous system.

### Topics Covered

* OSPF configuration
* OSPF neighbors
* Router ID
* Areas
* Network advertisements
* Cost
* Neighbor adjacency
* Routing table verification

### Basic Configuration

```cisco
router ospf 1
network <NETWORK> <WILDCARD-MASK> area 0
```

### Verification

```cisco
show ip ospf neighbor
show ip ospf
show ip route ospf
show ip protocols
```

### Important Concepts

```text
OSPF
 ├── Link-State Routing
 ├── SPF Algorithm
 ├── Router ID
 ├── Neighbor Adjacency
 ├── Areas
 ├── Cost
 └── LSDB
```

The repository currently contains the OSPF Packet Tracer file along with dedicated `configs` and `diagram` directories.

---

# 8. Standard ACL

**Standard ACL — Access Control List** filters IPv4 traffic primarily based on the **source IP address**.

Example:

```text
PC-A ─── R1 ─── Server
```

An ACL can control whether traffic originating from a particular source network is permitted or denied.

### Topics Covered

* Standard ACL
* Permit and deny statements
* Source IP filtering
* ACL placement
* Inbound ACL
* Outbound ACL
* Implicit deny

### Example

```cisco
access-list 10 deny host 192.168.10.10
access-list 10 permit any
```

Apply to an interface:

```cisco
interface g0/0
ip access-group 10 in
```

### Verification

```cisco
show access-lists
show ip interface
```

The lab currently contains `acl.pkt`, `configs`, `topology`, and a README.

---

# Protocol and Technology Coverage

The current `network-labs` collection covers the following areas:

```text
Network Labs
│
├── Neighbor Discovery
│   ├── CDP
│   └── LLDP
│
├── Network Services
│   ├── DNS
│   └── NTP
│
├── Dynamic Routing
│   ├── EIGRP
│   └── OSPF
│
├── Static Routing
│   └── Floating Static Routes
│
├── High Availability
│   └── HSRP
│
└── Network Security
    └── Standard ACL
```

---

# Lab Structure

Most labs follow a consistent structure:

```text
network-labs/
│
├── cdp-and-lldp/
│   ├── configs/
│   ├── diagram/
│   ├── lab-cdp-lldp.pkt
│   └── readme.md
│
├── dns/
│   ├── configs/
│   ├── diagram/
│   ├── dns.pkt
│   └── readme.md
│
├── eigrp/
│   ├── configs/
│   ├── diagram/
│   └── topology/
│
├── floating-static-routes/
│   ├── README.md
│   ├── configs/
│   ├── diagram/
│   └── topology/
│
├── hsrp/
│   ├── README.md
│   ├── configs/
│   ├── diagram/
│   └── hsrp.pkt
│
├── ntp/
│   ├── configs/
│   ├── diagram/
│   ├── ntp.pkt
│   └── readme.md
│
├── ospf/
│   ├── configs/
│   ├── diagram/
│   └── ospf.pkt
│
├── standard-acl/
│   ├── README.md
│   ├── configs/
│   ├── topology/
│   └── acl.pkt
│
└── basic-hardening-commands.md
```

The actual repository confirms these resources and directory structures for the individual labs.

---

# Verification Approach

Each lab should be approached using the same basic workflow:

```text
1. Understand the topology
        ↓
2. Identify IP addressing
        ↓
3. Configure interfaces
        ↓
4. Configure the protocol/service
        ↓
5. Verify neighbor relationships
        ↓
6. Verify routing/state information
        ↓
7. Test connectivity
        ↓
8. Troubleshoot failures
```

Useful Cisco IOS commands include:

```cisco
show running-config
show ip interface brief
show ip route
show ip protocols
show cdp neighbors
show lldp neighbors
ping
traceroute
```

Protocol-specific verification commands should then be used for each individual lab.

---

# Learning Progression

A practical progression through these labs is:

```text
Basic Connectivity
       ↓
CDP / LLDP
       ↓
Static Routing
       ↓
Floating Static Routes
       ↓
OSPF
       ↓
EIGRP
       ↓
HSRP
       ↓
DNS
       ↓
NTP
       ↓
Standard ACL
       ↓
Troubleshooting & Security
```

This sequence moves from **basic device awareness and routing** toward **redundancy, network services, and traffic control**.

---

# Basic Network Security

The directory also contains:

```text
basic-hardening-commands.md
```

This provides a reference for basic Cisco device-hardening commands. It complements the Standard ACL lab by introducing configuration practices intended to reduce unnecessary exposure on network devices.

---

# Practical Skills Covered

By completing these labs, the following practical skills can be developed:

* Cisco IOS CLI
* IPv4 addressing
* Subnetting
* Routing-table analysis
* Static routing
* Dynamic routing
* OSPF
* EIGRP
* HSRP
* ACL configuration
* DNS configuration
* NTP configuration
* CDP
* LLDP
* Network troubleshooting
* Connectivity verification
* Protocol-state verification
* Basic network device hardening

---

# Lab Documentation Standard

Each future lab should ideally contain:

```text
<lab-name>/
├── README.md
├── <lab-name>.pkt
├── configs/
├── diagram/
└── topology/
```

The README should document:

1. Objective
2. Network topology
3. Addressing table
4. Protocol/technology
5. Configuration steps
6. Verification commands
7. Expected results
8. Troubleshooting
9. Packet Tracer file
10. Configuration screenshots

This keeps the repository consistent as additional networking labs are added.

---

## Repository

[Networking Repository — network-labs](https://github.com/kumaradoss16/Networking/tree/main/network-labs?utm_source=chatgpt.com)

**Current `network-labs` scope:** CDP/LLDP, DNS, EIGRP, Floating Static Routes, HSRP, NTP, OSPF, Standard ACL, plus basic hardening commands.

**Note:** Your main repository also contains other networking work such as BGP, VLAN/Inter-VLAN Routing, DHCP, and Python-based networking tools; I have intentionally kept this README focused on the contents of the `network-labs` directory rather than mixing those projects into this lab index.
