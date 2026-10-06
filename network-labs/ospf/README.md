# OSPF Network Protocol Configuration Lab

## 1. Lab Overview

**Protocol:** OSPF - Open Shortest Path First
**Protocol Type:** Link-State Interior Gateway Protocol (IGP)
**OSPF Version:** OSPFv2 for IPv4
**Platform:** Cisco IOS / Cisco Packet Tracer
**Lab File:** `ospf.pkt`

### Repository

The complete Packet Tracer lab and configuration references are available in the Networking repository:

`network-labs/ospf/`

The lab contains:

* Cisco Packet Tracer topology
* OSPF topology diagram
* Router configurations
* Switch configurations
* Device-specific configuration screenshots

---

# 2. Lab Objectives

The objectives of this lab are to:

1. Configure IPv4 addressing on network devices.
2. Configure OSPF routing between multiple routers.
3. Place interfaces into the appropriate OSPF area.
4. Establish OSPF neighbor relationships.
5. Advertise connected networks through OSPF.
6. Verify OSPF neighbor adjacency.
7. Verify routes learned through OSPF.
8. Verify end-to-end connectivity.
9. Understand the purpose of common OSPF verification commands.
10. Understand how OSPF dynamically maintains routing information.

---

# 3. Network Topology

The repository contains the topology diagram:

`network-labs/ospf/diagram/ospf-diagram.png`

The lab uses:

```text
                +---------+
                |   R1    |
                +----+----+
                     |
                     |
                +----+----+
                |   R2    |
                +----+----+
                     |
                     |
                +----+----+
                |   R3    |
                +---------+
```

The topology also contains:

```text
SW1
SW2
SW3
```

The exact interface-to-interface connections and IP addressing should be taken from the Packet Tracer file and topology diagram in the repository.

---

# 4. OSPF Fundamentals

OSPF is a link-state routing protocol used to dynamically exchange routing information between routers within an autonomous system.

Instead of simply advertising routes to neighbors, OSPF routers build a topology database and calculate the shortest path using the **Shortest Path First (SPF)** algorithm.

OSPF uses:

```text
Router ID
Area
Link-State Database
Neighbor Adjacency
LSAs
SPF Calculation
Cost
```

---

# 5. OSPF Configuration Workflow

A typical Cisco OSPF configuration follows this sequence:

```text
Configure interfaces
        ↓
Assign IP addresses
        ↓
Enable interfaces
        ↓
Start OSPF process
        ↓
Configure Router ID
        ↓
Advertise networks
        ↓
Establish neighbor adjacency
        ↓
Verify OSPF
        ↓
Verify routing table
        ↓
Test connectivity
```

---

# 6. Router Interface Configuration

Before configuring OSPF, router interfaces must have valid IP addresses.

Example:

```cisco
R1(config)# interface gigabitEthernet 0/0
R1(config-if)# ip address 192.168.10.1 255.255.255.0
R1(config-if)# no shutdown
```

### Purpose

```text
interface gigabitEthernet 0/0
```

Selects the interface that will be configured.

```text
ip address 192.168.10.1 255.255.255.0
```

Assigns an IPv4 address and subnet mask to the interface.

```text
no shutdown
```

Administratively enables the interface.

Without `no shutdown`, an interface can remain administratively down.

---

# 7. Verify Interface Status

```cisco
R1# show ip interface brief
```

### Purpose

Displays a summarized view of router interfaces.

Important columns include:

```text
Interface
IP-Address
Status
Protocol
```

Example:

```text
Interface              IP-Address      Status       Protocol
GigabitEthernet0/0     192.168.10.1    up           up
GigabitEthernet0/1     10.0.12.1       up           up
```

For normal operation, the important state is:

```text
Status:   up
Protocol: up
```

---

# 8. Start the OSPF Process

Example:

```cisco
R1(config)# router ospf 1
```

### Purpose

Enables an OSPF routing process on the router.

The number:

```text
1
```

is the local OSPF process ID.

It is locally significant and does not have to be identical on every router.

For example:

```text
R1 → router ospf 1
R2 → router ospf 1
R3 → router ospf 1
```

is common, but different process IDs can also be used.

---

# 9. Configure the OSPF Router ID

Example:

```cisco
R1(config-router)# router-id 1.1.1.1
```

### Purpose

Manually assigns the OSPF Router ID.

The Router ID uniquely identifies the OSPF router.

A common convention is:

```text
R1 → 1.1.1.1
R2 → 2.2.2.2
R3 → 3.3.3.3
```

The exact Router IDs should follow the configuration used in the repository lab.

---

# 10. Advertise Networks into OSPF

Example:

```cisco
R1(config-router)# network 10.0.12.0 0.0.0.3 area 0
```

### Purpose

The `network` command tells OSPF which local interfaces should participate in OSPF.

The syntax is:

```text
network <network-address> <wildcard-mask> area <area-id>
```

Example:

```text
network 10.0.12.0 0.0.0.3 area 0
```

means:

```text
Network:       10.0.12.0
Wildcard mask: 0.0.0.3
Area:          0
```

---

# 11. Understanding the Wildcard Mask

OSPF uses a wildcard mask rather than a traditional subnet mask.

For:

```text
255.255.255.252
```

the wildcard mask is:

```text
0.0.0.3
```

For:

```text
255.255.255.0
```

the wildcard mask is:

```text
0.0.0.255
```

The wildcard mask determines which addresses are matched by the OSPF `network` statement.

---

# 12. Configure Area 0

Example:

```cisco
R1(config-router)# network 10.0.12.0 0.0.0.3 area 0
```

### Purpose

Places the matching interface/network into OSPF **Area 0**.

Area 0 is the OSPF backbone area.

A simple single-area OSPF lab normally uses:

```text
Area 0
```

for all participating networks.

---

# 13. Configure Multiple OSPF Networks

A router may have several networks that need to participate in OSPF.

Example:

```cisco
R1(config-router)# network 10.0.12.0 0.0.0.3 area 0
R1(config-router)# network 192.168.10.0 0.0.0.255 area 0
```

The first statement enables OSPF on the router-to-router network.

The second statement advertises the LAN network.

Conceptually:

```text
R1
├── Router-to-Router Network
│       ↓
│      OSPF
│
└── LAN Network
        ↓
       OSPF
```

---

# 14. Passive Interfaces

For LAN interfaces where OSPF neighbor formation is not required, a passive interface can be used.

Example:

```cisco
R1(config-router)# passive-interface gigabitEthernet 0/0
```

### Purpose

The interface can still advertise its connected network through OSPF, but OSPF does not send neighbor-formation packets through that interface.

This is useful for:

* User LANs
* Server networks
* Printer networks
* Management networks

It reduces unnecessary OSPF neighbor formation.

---

# 15. OSPF Neighbor Formation

After OSPF is configured on connected routers, they exchange OSPF Hello packets.

The general process is:

```text
R1
 │
 │ Hello
 ↓
R2
 │
 │ Hello
 ↓
R1
```

If OSPF parameters are compatible, the routers establish an adjacency.

Typical state progression includes:

```text
Down
Init
2-Way
ExStart
Exchange
Loading
Full
```

The final:

```text
FULL
```

state indicates that the routers have successfully formed a full OSPF adjacency.

---

# 16. Verify OSPF Neighbors

Use:

```cisco
R1# show ip ospf neighbor
```

### Purpose

Displays OSPF neighbors discovered by the router.

Important information includes:

```text
Neighbor ID
Priority
State
Dead Time
Address
Interface
```

Example:

```text
Neighbor ID     State        Interface
2.2.2.2         FULL         GigabitEthernet0/1
```

The important part is:

```text
FULL
```

which indicates a fully established adjacency.

---

# 17. Detailed OSPF Information

Use:

```cisco
R1# show ip ospf
```

### Purpose

Displays general OSPF process information.

It can show:

* OSPF process ID
* Router ID
* Areas
* SPF statistics
* LSA information
* Reference bandwidth
* Number of interfaces participating in OSPF

This is useful when troubleshooting the OSPF process itself.

---

# 18. Display OSPF Interface Information

Use:

```cisco
R1# show ip ospf interface
```

### Purpose

Displays detailed OSPF information for interfaces.

Useful information includes:

```text
Area
Process ID
Router ID
Network type
Hello interval
Dead interval
Cost
Neighbor count
DR/BDR information
```

This is particularly useful when two routers fail to establish an adjacency.

---

# 19. Display the Routing Table

Use:

```cisco
R1# show ip route
```

### Purpose

Displays the router's routing table.

OSPF routes are identified by:

```text
O
```

For example:

```text
O    192.168.30.0/24 [110/2] via 10.0.12.2
```

The `O` indicates that the route was learned through OSPF.

---

# 20. Understanding an OSPF Route

Example:

```text
O 192.168.30.0/24 [110/2] via 10.0.12.2
```

Breakdown:

```text
O
```

Route was learned through OSPF.

```text
192.168.30.0/24
```

Destination network.

```text
110
```

OSPF administrative distance.

```text
2
```

OSPF metric/cost.

```text
via 10.0.12.2
```

Next-hop router.

---

# 21. OSPF Administrative Distance

The default administrative distance for OSPF is:

```text
110
```

Administrative distance determines which routing source is preferred when multiple routing protocols provide routes to the same destination.

Example:

```text
Connected → 0
Static    → 1
EIGRP     → 90
OSPF      → 110
RIP       → 120
```

Lower administrative distance is preferred.

---

# 22. OSPF Cost

OSPF uses **cost** as its routing metric.

The router selects the path with the lowest total cost.

Conceptually:

```text
R1 ----10---- R2 ----10---- R3
 \                       /
  --------30-------------
```

OSPF compares:

```text
Path 1:
R1 → R2 → R3
10 + 10 = 20

Path 2:
R1 → R3
30
```

OSPF selects:

```text
20
```

because it is the lower cost.

---

# 23. Display OSPF Database

Use:

```cisco
R1# show ip ospf database
```

### Purpose

Displays the OSPF Link-State Database (LSDB).

The LSDB contains information that routers use to build a common view of the network topology.

OSPF then runs the SPF algorithm against this information to calculate routes.

---

# 24. Test Connectivity

Use:

```cisco
R1# ping <destination-ip>
```

Example:

```cisco
R1# ping 192.168.30.10
```

### Purpose

Tests IP connectivity between the source and destination.

A successful ping verifies that the routing and Layer 3 forwarding path is working.

---

# 25. Trace the Routing Path

Use:

```cisco
R1# traceroute <destination-ip>
```

Example:

```cisco
R1# traceroute 192.168.30.10
```

### Purpose

Displays the Layer 3 path used to reach the destination.

This is useful for determining which routers are forwarding traffic.

---

# 26. Verify Specific OSPF Routes

Use:

```cisco
R1# show ip route ospf
```

### Purpose

Displays only routes learned through OSPF.

This is useful when the routing table contains many different route types.

Example:

```text
O    192.168.20.0/24
O    192.168.30.0/24
O    10.0.23.0/30
```

---

# 27. OSPF Configuration Verification Workflow

After configuration, verify the lab in this order:

### Step 1 - Interfaces

```cisco
show ip interface brief
```

Check:

```text
Status = up
Protocol = up
```

### Step 2 - OSPF Process

```cisco
show ip ospf
```

Check:

```text
Router ID
Area
Interfaces
```

### Step 3 - Neighbors

```cisco
show ip ospf neighbor
```

Check:

```text
FULL
```

### Step 4 - Routing Table

```cisco
show ip route ospf
```

Check that remote networks appear.

### Step 5 - Connectivity

```cisco
ping <remote-ip>
```

### Step 6 - Path Verification

```cisco
traceroute <remote-ip>
```

---

# 28. Common OSPF Troubleshooting Commands

## Check interfaces

```cisco
show ip interface brief
```

Purpose:

```text
Verify interface IP addresses and operational status.
```

---

## Check OSPF neighbors

```cisco
show ip ospf neighbor
```

Purpose:

```text
Verify OSPF adjacency.
```

---

## Check OSPF interfaces

```cisco
show ip ospf interface
```

Purpose:

```text
Check OSPF parameters on individual interfaces.
```

---

## Check routing table

```cisco
show ip route
```

Purpose:

```text
Verify whether routes have been installed.
```

---

## Check OSPF-only routes

```cisco
show ip route ospf
```

Purpose:

```text
Display routes learned specifically through OSPF.
```

---

## Check OSPF database

```cisco
show ip ospf database
```

Purpose:

```text
Inspect the Link-State Database.
```

---

# 29. Common OSPF Problems

## Problem 1 - Neighbor is not appearing

Check:

```cisco
show ip ospf neighbor
show ip ospf interface
show ip interface brief
```

Possible causes:

* Interface is down.
* Incorrect IP address.
* Incorrect subnet mask.
* Incorrect area.
* Hello/dead interval mismatch.
* Network type mismatch.
* Authentication mismatch.
* OSPF not enabled on the interface.
* ACL blocking OSPF traffic.

---

# 30. Problem 2 - OSPF Neighbor Exists but Route Is Missing

Check:

```cisco
show ip ospf database
show ip route ospf
show ip ospf
```

Possible causes:

* Network was not advertised.
* Incorrect wildcard mask.
* Interface placed in the wrong area.
* Network is not active.
* Route filtering.
* Passive-interface configuration.
* Incorrect addressing.

---

# 31. Problem 3 - Ping Fails

Check the path progressively:

```text
Local Interface
      ↓
Default/OSPF Route
      ↓
Next Hop
      ↓
Remote Router
      ↓
Remote LAN
      ↓
Destination Host
```

Useful commands:

```cisco
show ip interface brief
show ip route
show ip ospf neighbor
ping <next-hop>
ping <remote-router>
ping <destination>
traceroute <destination>
```

---

# 32. Important OSPF Concepts Demonstrated

This lab provides practical experience with:

| Concept                 | Purpose                                     |
| ----------------------- | ------------------------------------------- |
| OSPF                    | Dynamic routing                             |
| OSPF Process ID         | Identifies local OSPF process               |
| Router ID               | Uniquely identifies OSPF router             |
| Area 0                  | OSPF backbone                               |
| Network statement       | Enables OSPF on matching interfaces         |
| Wildcard mask           | Determines matching addresses               |
| Neighbor adjacency      | Allows routers to exchange LSDB information |
| LSDB                    | Stores topology information                 |
| SPF                     | Calculates shortest paths                   |
| OSPF Cost               | Determines preferred path                   |
| Administrative Distance | Selects between routing sources             |
| Passive Interface       | Prevents unnecessary neighbor formation     |
| `show ip route ospf`    | Verifies OSPF-learned routes                |

---

# 33. Command Reference

| Command                   | Purpose                                         |
| ------------------------- | ----------------------------------------------- |
| `show ip interface brief` | Check interface IP/status                       |
| `show ip route`           | Display routing table                           |
| `show ip route ospf`      | Display OSPF routes                             |
| `show ip ospf`            | Display OSPF process information                |
| `show ip ospf neighbor`   | Display OSPF neighbors                          |
| `show ip ospf interface`  | Display OSPF interface details                  |
| `show ip ospf database`   | Display OSPF LSDB                               |
| `ping`                    | Test IP connectivity                            |
| `traceroute`              | Trace Layer 3 path                              |
| `router ospf 1`           | Enter OSPF configuration mode                   |
| `router-id`               | Configure OSPF Router ID                        |
| `network ... area 0`      | Enable OSPF and advertise matching networks     |
| `passive-interface`       | Prevent OSPF neighbor formation on an interface |

---

# 34. Verification Checklist

After completing the lab, confirm:

```text
[ ] All required interfaces are configured
[ ] All required interfaces are up/up
[ ] Correct IPv4 addressing is configured
[ ] OSPF process is running
[ ] Correct Router ID is configured
[ ] Correct OSPF area is configured
[ ] OSPF neighbors are established
[ ] Neighbor state reaches FULL where applicable
[ ] Remote networks appear in the routing table
[ ] OSPF routes begin with O
[ ] Ping succeeds between required networks
[ ] Traceroute follows the expected path
[ ] OSPF database contains expected LSAs
```

---

# 35. Expected Learning Outcome

After completing this lab, you should be able to:

1. Configure OSPF on Cisco routers.
2. Understand OSPF neighbor formation.
3. Configure OSPF areas.
4. Advertise IPv4 networks through OSPF.
5. Verify OSPF neighbor relationships.
6. Identify OSPF routes in the routing table.
7. Understand OSPF cost and path selection.
8. Troubleshoot basic OSPF adjacency problems.
9. Verify end-to-end connectivity.
10. Use Cisco IOS show commands for OSPF troubleshooting.

---

# 36. Repository Reference

The actual lab files are maintained in the Networking GitHub repository:

**OSPF Lab**

`network-labs/ospf/`

Contents include:

```text
ospf/
├── configs/
│   ├── 1. R1-config.png
│   ├── 2. R2-config.png
│   ├── 3. R3-config.png
│   ├── 4. SW1-config.png
│   ├── 5. SW2-config.png
│   └── 6. SW3-config.png
│
├── diagram/
│   └── ospf-diagram.png
│
└── ospf.pkt
```

The `.pkt` file is the executable Cisco Packet Tracer lab, while the configuration screenshots provide device-specific configuration references.
