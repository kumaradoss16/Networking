# EIGRP Lab Configuration

## Overview

This lab demonstrates the configuration and verification of **EIGRP (Enhanced Interior Gateway Routing Protocol)** in a multi-router Cisco network.

The lab includes:

* R1
* R2
* R3
* R4
* SW1
* SW2
* EIGRP routing
* Network route advertisement
* EIGRP neighbor formation
* Routing table verification
* End-to-end connectivity testing

The Packet Tracer topology is available in the [`topology`](https://github.com/kumaradoss16/Networking/tree/main/network-labs/eigrp/topology) directory.

---

## Objectives

* Configure router interfaces.
* Enable EIGRP on the routers.
* Advertise connected networks.
* Establish EIGRP neighbor relationships.
* Verify EIGRP routes.
* Test end-to-end connectivity.
* Understand basic EIGRP troubleshooting commands.

---

## EIGRP Basics

**EIGRP** is a Cisco-developed dynamic routing protocol based on the Diffusing Update Algorithm (DUAL).

EIGRP uses:

* Neighbor discovery
* Topology table
* Routing table
* DUAL algorithm
* Composite metric
* Feasible successor for backup paths

### Important EIGRP Terms

| Term               | Purpose                                                 |
| ------------------ | ------------------------------------------------------- |
| Neighbor           | EIGRP router directly connected to another EIGRP router |
| Neighbor Table     | Stores information about EIGRP neighbors                |
| Topology Table     | Stores learned EIGRP routes and path information        |
| Routing Table      | Contains the best routes selected for forwarding        |
| Successor          | Best path to a destination                              |
| Feasible Successor | Backup path that satisfies the feasibility condition    |
| AS Number          | Identifies the EIGRP routing process                    |

---

# 1. Configure Router Interfaces

First configure the IP addresses on the router interfaces.

```cisco
enable
configure terminal

interface gigabitEthernet 0/0
ip address <IP_ADDRESS> <SUBNET_MASK>
no shutdown
exit
```

### Command Purpose

| Command                         | Purpose                                    |
| ------------------------------- | ------------------------------------------ |
| `enable`                        | Enters privileged EXEC mode                |
| `configure terminal`            | Enters global configuration mode           |
| `interface gigabitEthernet 0/0` | Selects the interface to configure         |
| `ip address`                    | Assigns an IPv4 address and subnet mask    |
| `no shutdown`                   | Enables the interface                      |
| `exit`                          | Returns to the previous configuration mode |

Configure the remaining router interfaces according to the topology.

---

# 2. Verify Interfaces

After configuring the interfaces:

```cisco
show ip interface brief
```

This displays:

* Interface names
* IP addresses
* Interface status
* Line protocol status

Example:

```text
Interface              IP-Address      OK? Method Status
GigabitEthernet0/0     x.x.x.x         YES manual up
GigabitEthernet0/1     x.x.x.x         YES manual up
```

Both **Status** and **Protocol** should normally be `up`.

---

# 3. Test Direct Connectivity

Before configuring EIGRP, test directly connected networks.

```cisco
ping <NEIGHBOR_IP>
```

Example:

```cisco
ping 10.0.0.2
```

### Purpose

`ping` uses ICMP to test IP connectivity between devices.

If the ping fails, troubleshoot the interfaces and IP addressing before configuring EIGRP.

---

# 4. Configure EIGRP

Enter the EIGRP routing process.

```cisco
enable
configure terminal

router eigrp <AS_NUMBER>
```

Example:

```cisco
router eigrp 100
```

The AS number must match between EIGRP routers that are expected to become neighbors.

---

# 5. Advertise Networks

Inside EIGRP configuration mode:

```cisco
network <NETWORK_ADDRESS>
```

Example:

```cisco
router eigrp 100
network 10.0.0.0
network 192.168.1.0
```

### Purpose

The `network` command tells EIGRP which interfaces/networks should participate in the EIGRP routing process.

It allows EIGRP to:

1. Enable EIGRP on matching interfaces.
2. Form EIGRP neighbor relationships.
3. Advertise connected networks.

---

# 6. Disable Automatic Summarization

For IPv4 EIGRP configurations, it is common to disable automatic classful summarization:

```cisco
no auto-summary
```

### Purpose

Prevents EIGRP from automatically summarizing routes at classful network boundaries.

Example:

```cisco
router eigrp 100
network 10.0.0.0
network 192.168.1.0
no auto-summary
```

---

# 7. Example EIGRP Configuration

A basic router configuration looks like:

```cisco
enable
configure terminal

router eigrp 100
network 10.0.0.0
network 192.168.1.0
no auto-summary

end
```

### Command Summary

| Command               | Purpose                                                         |
| --------------------- | --------------------------------------------------------------- |
| `router eigrp 100`    | Starts EIGRP process AS 100                                     |
| `network 10.0.0.0`    | Enables EIGRP on matching interfaces and advertises the network |
| `network 192.168.1.0` | Advertises another connected network                            |
| `no auto-summary`     | Disables automatic classful summarization                       |
| `end`                 | Returns to privileged EXEC mode                                 |

> Use the actual network addresses and EIGRP AS number from the lab topology.

---

# 8. Verify EIGRP Neighbors

After configuring EIGRP on neighboring routers:

```cisco
show ip eigrp neighbors
```

This displays the EIGRP neighbor table.

Important information includes:

* Neighbor IP address
* Interface
* Hold time
* Uptime
* Sequence information

A neighboring router should appear in the output when the EIGRP adjacency is established.

---

# 9. Verify EIGRP Routes

Use:

```cisco
show ip route
```

EIGRP-learned routes are normally identified with:

```text
D
```

For example:

```text
D    192.168.20.0/24 [90/...] via ...
```

### `D` Meaning

`D` represents a route learned through **EIGRP**.

The routing table contains the routes that the router currently uses for packet forwarding.

---

# 10. Display Only EIGRP Routes

Use:

```cisco
show ip route eigrp
```

### Purpose

Displays only routes learned through EIGRP.

This is useful when checking whether the expected remote networks have been learned.

---

# 11. View the EIGRP Topology Table

```cisco
show ip eigrp topology
```

### Purpose

Displays EIGRP's topology information, including:

* Destination networks
* Successor
* Feasible successor
* Feasible distance
* Reported distance
* Path information

This is useful for understanding how EIGRP selects routes.

---

# 12. View EIGRP Protocol Information

```cisco
show ip protocols
```

This command displays routing protocol information such as:

* EIGRP process
* AS number
* Networks participating in EIGRP
* Passive interfaces
* Routing protocol timers
* Administrative information

This is one of the most useful commands for checking the EIGRP configuration.

---

# 13. Test End-to-End Connectivity

After EIGRP converges, test connectivity to remote networks.

```cisco
ping <REMOTE_IP>
```

For example:

```cisco
ping <REMOTE_ROUTER_INTERFACE>
```

You can also use:

```cisco
traceroute <REMOTE_IP>
```

### `traceroute` Purpose

Shows the Layer 3 path used to reach a remote destination.

It helps identify where traffic stops when troubleshooting routing problems.

---

# 14. Check the Running Configuration

```cisco
show running-config
```

### Purpose

Displays the current active configuration.

Use this to verify:

* Interface IP addresses
* EIGRP configuration
* Network statements
* Other routing configuration

---

# 15. Save the Configuration

After completing the lab:

```cisco
copy running-config startup-config
```

or:

```cisco
write memory
```

### Purpose

Saves the current running configuration so that it can be restored after a device restart.

---

# EIGRP Verification Commands

| Command                   | Purpose                                 |
| ------------------------- | --------------------------------------- |
| `show ip eigrp neighbors` | Displays EIGRP neighbors                |
| `show ip route`           | Displays the routing table              |
| `show ip route eigrp`     | Displays EIGRP-learned routes           |
| `show ip eigrp topology`  | Displays the EIGRP topology table       |
| `show ip protocols`       | Displays routing protocol configuration |
| `show running-config`     | Displays active configuration           |
| `show ip interface brief` | Quickly checks interface status         |
| `ping`                    | Tests IP connectivity                   |
| `traceroute`              | Shows the Layer 3 path to a destination |

---

# EIGRP Troubleshooting

## 1. No EIGRP Neighbor

Check:

```cisco
show ip eigrp neighbors
```

Then verify:

```cisco
show ip interface brief
```

Check:

* Interfaces are up.
* Interfaces have correct IP addresses.
* Routers are directly reachable.
* EIGRP AS numbers match.
* Interfaces are included in the EIGRP `network` statements.

---

## 2. EIGRP Route Is Missing

Check:

```cisco
show ip route eigrp
```

Then:

```cisco
show ip eigrp topology
```

Also verify:

```cisco
show ip protocols
```

Check whether the destination network is correctly advertised by the remote router.

---

## 3. Ping Fails

Use:

```cisco
ping <DESTINATION_IP>
```

Then check:

```cisco
show ip route
show ip eigrp neighbors
show ip interface brief
```

Verify the complete path between source and destination.

---

# EIGRP Configuration Flow

```text
Configure IP addresses
        ↓
Enable interfaces
        ↓
Test direct connectivity
        ↓
Start EIGRP
        ↓
Configure EIGRP AS number
        ↓
Advertise connected networks
        ↓
Disable auto-summary
        ↓
EIGRP neighbors form
        ↓
Routes are exchanged
        ↓
Verify routing table
        ↓
Test end-to-end connectivity
```

---

# Key Takeaways

* EIGRP is a dynamic routing protocol used to exchange routes between routers.
* EIGRP routers form neighbor relationships before exchanging routing information.
* The EIGRP AS number must match between participating neighbors.
* The `network` command enables EIGRP on matching interfaces and advertises their networks.
* `show ip eigrp neighbors` verifies neighbor relationships.
* `show ip route eigrp` verifies EIGRP-learned routes.
* `show ip eigrp topology` provides detailed EIGRP path information.
* `ping` and `traceroute` are used to verify end-to-end connectivity.
* EIGRP uses DUAL to select loop-free paths and can maintain feasible successor paths as backups.

## Lab Files

* **Topology:** `topology/EIGRP.pkt`
* **Diagram:** `diagram/eigrp.png`
* **Router/Switch configurations:** `configs/`
* **R1:** `configs/1. R1.png`
* **R2:** `configs/2. R2.png`
* **R3:** `configs/3. R3.png`
* **R4:** `configs/4. R4.png`
* **SW1:** `configs/5. SW1.png`
* **SW2:** `configs/6. SW2.png`

[View the complete EIGRP lab on GitHub](https://github.com/kumaradoss16/Networking/tree/main/network-labs/eigrp?utm_source=chatgpt.com)
