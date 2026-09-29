# DHCP Lab — Cisco IOS DHCP Server and Client Configuration

## Overview

This lab demonstrates how to configure a Cisco router as a **DHCP server** and another router as a **DHCP client** using Cisco IOS.

The lab is implemented in **Cisco Packet Tracer** and focuses on the configuration and verification of Dynamic Host Configuration Protocol (DHCP).

The configuration demonstrates how a DHCP server dynamically allocates IPv4 addressing information to a DHCP client instead of requiring the client interface to be manually configured with a static IP address.

---

## Objectives

By completing this lab, you will learn how to:

* Configure a Cisco router as a DHCP server.
* Create a DHCP address pool.
* Define the network distributed by the DHCP server.
* Configure a default gateway for DHCP clients.
* Exclude addresses from the DHCP allocation range.
* Configure a router interface as a DHCP client.
* Obtain an IPv4 address dynamically.
* Verify DHCP bindings and pool information.
* Verify the dynamically assigned address on the client.
* Understand the DHCP DORA process.
* Troubleshoot basic DHCP allocation problems.

---

## Lab Environment

| Component          | Technology          |
| ------------------ | ------------------- |
| Simulator          | Cisco Packet Tracer |
| Protocol           | DHCP                |
| Addressing         | IPv4                |
| DHCP Server        | Cisco Router R2     |
| DHCP Client        | Cisco Router R1     |
| Device OS          | Cisco IOS           |
| Transport Protocol | UDP                 |
| DHCP Server Port   | UDP 67              |
| DHCP Client Port   | UDP 68              |

---

## Repository Structure

```text
dhcp/
├── configs/
│   ├── 1.1 R2-initial-config.png
│   ├── 1.2 R1-initial-config.png
│   ├── 2. R2-dhcp-server-config.png
│   ├── 3. R1-dhcp-client-config.png
│   └── 4. R1-dhcp-client-config.png
│
├── diagram/
│   └── dhcp-network-topology.png
│
└── dhcp.pkt
```

The repository contains the Packet Tracer topology, network diagram, and configuration screenshots used during the lab.

---

# Network Topology

The lab uses two Cisco routers:

```text
                    DHCP Request
                         |
                         v
              +---------------------+
              |         R1          |
              |    DHCP Client      |
              +----------+----------+
                         |
                         |
                    Network Link
                         |
                         |
              +----------+----------+
              |         R2          |
              |    DHCP Server      |
              +---------------------+
```

### Device Roles

| Device | Role        |
| ------ | ----------- |
| R1     | DHCP Client |
| R2     | DHCP Server |

R2 provides the IPv4 addressing information, while R1 requests its interface address through DHCP.

---

# DHCP Architecture

DHCP uses a client-server architecture.

```text
+----------------+                  +----------------+
|                |                  |                |
|      R1        |                  |      R2        |
| DHCP Client    |                  | DHCP Server    |
|                |                  |                |
+-------+--------+                  +--------+-------+
        |                                    |
        | DHCP Discover                      |
        |----------------------------------->|
        |                                    |
        | DHCP Offer                         |
        |<-----------------------------------|
        |                                    |
        | DHCP Request                       |
        |----------------------------------->|
        |                                    |
        | DHCP ACK                           |
        |<-----------------------------------|
        |                                    |
```

This process is commonly called **DORA**:

1. **Discover**
2. **Offer**
3. **Request**
4. **Acknowledgment (ACK)**

---

# DHCP DORA Process

## 1. DHCP Discover

The client does not initially have a usable IPv4 address.

It sends a DHCP Discover message to locate available DHCP servers.

```text
R1 → DHCP Discover → R2
```

---

## 2. DHCP Offer

The DHCP server responds with an available address and other configuration parameters.

```text
R2 → DHCP Offer → R1
```

The offer can contain information such as:

* IPv4 address
* Subnet mask
* Default gateway
* DNS server
* Lease duration

---

## 3. DHCP Request

The client requests the offered address.

```text
R1 → DHCP Request → R2
```

---

## 4. DHCP ACK

The DHCP server confirms the allocation.

```text
R2 → DHCP ACK → R1
```

R1 can then use the dynamically assigned IPv4 address.

---

# DHCP Server Configuration

R2 is configured as the DHCP server.

The basic Cisco IOS configuration consists of:

1. Excluding addresses
2. Creating a DHCP pool
3. Defining the client network
4. Defining the default gateway
5. Optionally defining DNS information

### Example Configuration

```cisco
R2# configure terminal

R2(config)# ip dhcp excluded-address 192.168.10.1 192.168.10.20

R2(config)# ip dhcp pool LAN-POOL

R2(dhcp-config)# network 192.168.10.0 255.255.255.0

R2(dhcp-config)# default-router 192.168.10.1

R2(dhcp-config)# dns-server 8.8.8.8

R2(dhcp-config)# exit
```

> The addressing values above illustrate the Cisco IOS DHCP configuration format. Use the exact addressing shown in the Packet Tracer topology when reproducing this repository lab.

---

# DHCP Address Pool

A DHCP pool defines the network from which the server allocates client addresses.

```cisco
ip dhcp pool LAN-POOL
 network 192.168.10.0 255.255.255.0
```

This tells R2 that the DHCP pool belongs to:

```text
Network:      192.168.10.0/24
Subnet Mask:  255.255.255.0
```

The DHCP server can allocate addresses from this network except for addresses explicitly excluded from the pool.

---

# Excluding DHCP Addresses

Some addresses should normally remain statically assigned.

For example:

```cisco
ip dhcp excluded-address 192.168.10.1 192.168.10.20
```

This prevents DHCP from dynamically assigning:

```text
192.168.10.1
192.168.10.2
...
192.168.10.20
```

These addresses can be reserved for infrastructure such as:

* Router interfaces
* Network management
* Servers
* Printers
* Network appliances

This reduces the possibility of an address conflict between statically configured devices and DHCP clients.

---

# Default Gateway

The DHCP server can provide the client's default gateway through:

```cisco
default-router 192.168.10.1
```

The client receives this information through DHCP.

Conceptually:

```text
DHCP Server
     |
     | Default Gateway
     v
192.168.10.1
     |
     v
DHCP Client
```

The default gateway is used when the client needs to communicate with destinations outside its local subnet.

---

# DNS Server

A DNS server can also be distributed through DHCP:

```cisco
dns-server 8.8.8.8
```

The client then receives the DNS server address automatically.

The DHCP server can therefore provide several pieces of network configuration simultaneously:

```text
IPv4 Address
      +
Subnet Mask
      +
Default Gateway
      +
DNS Server
      +
Lease Information
```

---

# DHCP Client Configuration

R1 is configured to obtain an IPv4 address dynamically.

The relevant interface is configured with:

```cisco
interface GigabitEthernet0/0
 ip address dhcp
 no shutdown
```

The important command is:

```cisco
ip address dhcp
```

This tells the router to act as a DHCP client on that interface.

Instead of:

```cisco
ip address 192.168.10.10 255.255.255.0
```

the interface obtains its address dynamically.

---

# Static Address vs DHCP Address

### Static Configuration

```cisco
interface GigabitEthernet0/0
 ip address 192.168.10.10 255.255.255.0
 no shutdown
```

The administrator manually specifies the address.

### DHCP Configuration

```cisco
interface GigabitEthernet0/0
 ip address dhcp
 no shutdown
```

The interface requests an address from a DHCP server.

---

# DHCP Communication

DHCP uses UDP.

| Device/Service |   Port |
| -------------- | -----: |
| DHCP Server    | UDP 67 |
| DHCP Client    | UDP 68 |

During the initial DHCP process, the client may not yet have a valid source IP address. Therefore, DHCP uses broadcast communication during the initial discovery process.

---

# Verification

After configuring the DHCP server and client, verify the configuration from both routers.

## R2 — Verify DHCP Bindings

```cisco
R2# show ip dhcp binding
```

This displays addresses that have been allocated to DHCP clients.

Example:

```text
Bindings from all pools not associated with VRF:
IP address       Client-ID/              Lease expiration
                 Hardware address
192.168.10.21    ...                     ...
```

The important information is the dynamically allocated IPv4 address.

---

## R2 — Verify DHCP Pool

```cisco
R2# show ip dhcp pool
```

This displays information about the configured DHCP pool.

Useful information includes:

* Pool name
* Network
* Address range
* Allocated addresses
* Available addresses
* Current utilization

---

## R2 — Verify DHCP Configuration

```cisco
R2# show running-config | section dhcp
```

This is useful for quickly checking the DHCP configuration.

Expected configuration elements include:

```text
ip dhcp excluded-address ...
ip dhcp pool ...
 network ...
 default-router ...
 dns-server ...
```

---

# R1 — Verify DHCP Client Address

On R1:

```cisco
R1# show ip interface brief
```

Example:

```text
Interface              IP-Address      OK? Method Status Protocol
GigabitEthernet0/0     192.168.10.21   YES DHCP   up     up
```

The important fields are:

```text
IP-Address
Method
Status
Protocol
```

`Method DHCP` indicates that the address was obtained dynamically.

---

# Detailed Interface Verification

Use:

```cisco
R1# show interfaces gigabitEthernet 0/0
```

This provides detailed interface information including:

* Hardware information
* IP address
* Encapsulation
* Line protocol
* Interface status
* Packet counters
* Errors
* MTU
* Duplex
* Speed

---

# Connectivity Verification

After the DHCP address has been assigned, test connectivity.

```cisco
R1# ping <R2-IP-address>
```

If the DHCP configuration and underlying connectivity are correct, the ping should succeed.

You can also verify the routing table:

```cisco
R1# show ip route
```

---

# DHCP Troubleshooting

If R1 does not receive an address, troubleshoot in this order.

## 1. Check the interface status

```cisco
R1# show ip interface brief
```

The interface should normally show:

```text
Status: up
Protocol: up
```

If necessary:

```cisco
R1(config)# interface GigabitEthernet0/0
R1(config-if)# no shutdown
```

---

## 2. Check the DHCP client configuration

```cisco
R1# show running-config
```

Verify that the interface contains:

```cisco
ip address dhcp
```

---

## 3. Check the DHCP pool

On R2:

```cisco
R2# show ip dhcp pool
```

Verify that the pool exists and has available addresses.

---

## 4. Check DHCP bindings

```cisco
R2# show ip dhcp binding
```

If R1 successfully obtained an address, the binding should appear here.

---

## 5. Check excluded addresses

Verify that the DHCP pool has not accidentally excluded the entire usable address range.

```cisco
R2# show running-config | section dhcp
```

---

## 6. Check the network statement

The DHCP pool must correspond to the correct client network.

Example:

```cisco
ip dhcp pool LAN-POOL
 network 192.168.10.0 255.255.255.0
```

The connected interface/network must match the DHCP pool design.

---

# Common DHCP Problems

| Problem                    | Possible Cause                       |
| -------------------------- | ------------------------------------ |
| Client receives no address | DHCP server not configured           |
| Interface down             | Missing `no shutdown`                |
| DHCP pool empty            | Incorrect/exhausted address range    |
| Wrong IP address           | Incorrect DHCP pool/network          |
| No connectivity            | Incorrect gateway or routing         |
| Address conflict           | Static address overlaps DHCP pool    |
| DHCP binding absent        | Client DHCP process did not complete |
| Pool unavailable           | Incorrect network statement          |
| Client remains without IP  | Layer 1/Layer 2 connectivity issue   |

---

# Important DHCP Concepts

## DHCP Server

The device that dynamically assigns network configuration.

In this lab:

```text
R2 = DHCP Server
```

---

## DHCP Client

The device requesting network configuration.

In this lab:

```text
R1 = DHCP Client
```

---

## DHCP Pool

A logical collection of addresses and options available for DHCP clients.

```text
DHCP Pool
 ├── Network
 ├── Subnet Mask
 ├── Default Gateway
 ├── DNS Server
 └── Lease Parameters
```

---

## DHCP Lease

A DHCP address is normally assigned for a limited period called a **lease**.

The client may renew the lease before it expires.

This allows addresses to be reused when clients leave the network.

---

# DHCP Server vs DHCP Relay

This lab demonstrates a directly connected DHCP server/client design.

```text
R1 DHCP Client
      |
      |
R2 DHCP Server
```

In a larger network, the DHCP server may be located on another subnet.

For example:

```text
Client VLAN
     |
     v
Layer 3 Router
     |
     | DHCP Relay
     |
     v
DHCP Server
```

A router can relay DHCP messages using:

```cisco
ip helper-address <DHCP-SERVER-IP>
```

The relay is required because routers normally do not forward ordinary Layer 3 broadcasts between subnets.

This is an important distinction:

```text
DHCP Server
    ≠
DHCP Relay
```

A router configured with `ip helper-address` is forwarding DHCP requests to another DHCP server; it is not itself creating the DHCP pool.

---

# Security Considerations

DHCP should be treated as part of the network's infrastructure services.

Important security considerations include:

### DHCP Snooping

On managed switches, DHCP Snooping can help protect the network against unauthorized DHCP servers.

Conceptually:

```text
Trusted DHCP Server
        |
        v
   Trusted Port
        |
      Switch
        |
        X
Rogue DHCP Server
```

DHCP Snooping identifies trusted and untrusted switch ports and can prevent unauthorized DHCP responses from reaching clients.

---

# DHCP Lab Workflow

The complete workflow used in this lab can be summarized as:

```text
1. Build topology
       |
       v
2. Configure R2 interfaces
       |
       v
3. Configure R1 interfaces
       |
       v
4. Configure R2 as DHCP Server
       |
       v
5. Configure R1 as DHCP Client
       |
       v
6. Enable interfaces
       |
       v
7. R1 sends DHCP Discover
       |
       v
8. R2 sends DHCP Offer
       |
       v
9. R1 sends DHCP Request
       |
       v
10. R2 sends DHCP ACK
       |
       v
11. Verify DHCP binding
       |
       v
12. Verify R1 IP address
       |
       v
13. Test connectivity
```

---

# Useful Cisco IOS Commands

### DHCP Server

```cisco
show ip dhcp binding
show ip dhcp pool
show ip dhcp conflict
show ip dhcp server statistics
show running-config | section dhcp
```

### DHCP Client

```cisco
show ip interface brief
show interfaces
show running-config
show ip route
```

### Connectivity

```cisco
ping <destination>
traceroute <destination>
```

---

# Key Commands Summary

### Configure DHCP Server

```cisco
ip dhcp excluded-address <start-ip> <end-ip>

ip dhcp pool <POOL-NAME>
 network <NETWORK> <MASK>
 default-router <GATEWAY>
 dns-server <DNS-SERVER>
```

### Configure DHCP Client

```cisco
interface <INTERFACE>
 ip address dhcp
 no shutdown
```

### Verify Server

```cisco
show ip dhcp binding
show ip dhcp pool
show ip dhcp server statistics
```

### Verify Client

```cisco
show ip interface brief
show interfaces
```

---

# Expected Learning Outcome

After completing this lab, you should be able to explain and demonstrate:

* What DHCP is.
* Why DHCP is used.
* DHCP client/server architecture.
* DHCP DORA.
* UDP ports 67 and 68.
* DHCP pools.
* DHCP address exclusions.
* DHCP default gateway assignment.
* DHCP DNS assignment.
* Cisco IOS DHCP server configuration.
* Cisco IOS DHCP client configuration.
* DHCP lease allocation.
* DHCP binding verification.
* Basic DHCP troubleshooting.
* The difference between DHCP server and DHCP relay.
* The purpose of DHCP Snooping.

---

# Lab Files

The Packet Tracer implementation is available here:

[dhcp.pkt — Packet Tracer Lab](https://github.com/kumaradoss16/Networking/blob/main/network-labs/dhcp/dhcp.pkt?utm_source=chatgpt.com)

Topology diagram:

[DHCP Network Topology](https://github.com/kumaradoss16/Networking/blob/main/network-labs/dhcp/diagram/dhcp-network-topology.png?utm_source=chatgpt.com)

Configuration screenshots:

[DHCP Configuration Files](https://github.com/kumaradoss16/Networking/tree/main/network-labs/dhcp/configs?utm_source=chatgpt.com)

---

# Related Concepts

This DHCP lab connects directly with several other network-engineering concepts:

```text
DHCP
 ├── IPv4 Addressing
 ├── Subnetting
 ├── Default Gateway
 ├── UDP
 ├── Broadcast
 ├── Routing
 ├── DHCP Relay
 ├── DHCP Snooping
 └── Network Troubleshooting
```

Understanding these dependencies makes DHCP configuration much easier to troubleshoot in real networks.

---

## Conclusion

This lab demonstrates the complete basic workflow for deploying DHCP using Cisco IOS.

R2 operates as the DHCP server and maintains the address pool, while R1 operates as a DHCP client and dynamically requests its IPv4 configuration.

The lab provides practical experience with DHCP configuration, DORA operation, address allocation, verification, and troubleshooting in a Cisco networking environment.
