# DNS Configuration Lab

## Overview

This lab demonstrates the configuration and operation of **DNS (Domain Name System)** in a Cisco Packet Tracer network environment.

The lab focuses on configuring a router to use a DNS server and verifying hostname resolution. It also demonstrates how DNS allows network devices to resolve domain names into IP addresses instead of requiring users or administrators to work directly with IP addresses.

The lab is implemented using **Cisco Packet Tracer** and includes a complete topology, addressing configuration, router DNS configuration, and verification steps.

---

## Objectives

By completing this lab, you will learn how to:

* Understand the purpose of DNS.
* Configure IP addressing for network devices.
* Configure a router with a DNS server.
* Configure DNS lookup on a Cisco router.
* Use a public DNS server such as `1.1.1.1`.
* Resolve hostnames from a Cisco router.
* Verify DNS resolution.
* Understand the difference between hostname resolution and IP connectivity.
* Troubleshoot basic DNS resolution problems.

---

## Technologies and Protocols

| Technology          | Purpose                               |
| ------------------- | ------------------------------------- |
| DNS                 | Resolves domain names to IP addresses |
| IPv4                | Provides network addressing           |
| Ethernet            | Provides LAN connectivity             |
| UDP/TCP 53          | Traditional DNS transport             |
| Cisco IOS           | Router configuration                  |
| Cisco Packet Tracer | Network simulation                    |

---

## Lab Files

The lab directory contains:

```text
dns/
├── configs/
│   ├── 1. INTERNET-config.png
│   ├── 1. R1-config.png
│   ├── 2. addressing.png
│   ├── 3. R1-dns-config.png
│   └── 4. dns-enable-1.1.1.1.png
│
├── diagram/
│   ├── dns-network-topology.png
│   └── requirements.png
│
└── dns.pkt
```

These files are part of the repository's DNS lab structure.

---

# DNS Fundamentals

## What is DNS?

**DNS (Domain Name System)** translates domain names into IP addresses.

For example:

```text
www.example.com
        ↓
    DNS lookup
        ↓
93.184.216.34
```

Without DNS, users would need to remember IP addresses for services instead of using human-readable names.

---

# DNS Communication

Traditional DNS uses:

```text
UDP/53
```

TCP port 53 is also used in situations such as DNS zone transfers and DNS exchanges that require TCP.

Basic communication:

```text
DNS Client
    |
    | DNS Query
    | UDP/53
    ↓
DNS Server
    |
    | DNS Response
    ↓
DNS Client
```

---

# Network Topology

The lab includes a network topology designed to demonstrate DNS configuration and connectivity.

Topology:

```text
                 Internet
                    |
                    |
                   R1
                    |
                    |
                LAN Network
                    |
              Network Devices
```

The detailed topology is available in:

```text
diagram/dns-network-topology.png
```

The repository also includes a requirements diagram describing the lab setup.

---

# Configuration Workflow

The lab follows this general sequence:

```text
1. Configure network topology
        ↓
2. Configure IP addressing
        ↓
3. Configure router interfaces
        ↓
4. Verify connectivity
        ↓
5. Configure DNS server
        ↓
6. Configure DNS lookup on R1
        ↓
7. Configure DNS server address
        ↓
8. Test hostname resolution
```

---

# Step 1 — Configure IP Addressing

Before testing DNS, basic IP connectivity must work.

Configure the required IPv4 addresses on the router and connected devices according to the addressing diagram included in the lab.

The addressing reference is:

```text
configs/2. addressing.png
```

Verify router interfaces:

```cisco
R1# show ip interface brief
```

Expected status:

```text
Interface              IP-Address      Status      Protocol
GigabitEthernet0/0     x.x.x.x         up          up
```

Both **Status** and **Protocol** should be `up`.

---

# Step 2 — Configure the Router

Basic router interface configuration follows the normal Cisco IOS workflow.

Example:

```cisco
R1(config)# interface gigabitEthernet0/0
R1(config-if)# ip address <IP_ADDRESS> <SUBNET_MASK>
R1(config-if)# no shutdown
```

Verify:

```cisco
R1# show ip interface brief
```

The repository contains an R1 configuration reference under:

```text
configs/1. R1-config.png
```

---

# Step 3 — Verify IP Connectivity

Before troubleshooting DNS, verify basic network connectivity.

For example:

```cisco
R1# ping <DNS_SERVER_IP>
```

If the ping succeeds:

```text
Success rate is 100 percent
```

the router has IP connectivity to the DNS server.

This distinction is important:

```text
IP connectivity
      ≠
DNS resolution
```

A device can have working IP connectivity while DNS resolution is broken.

---

# Step 4 — Configure the DNS Server

The DNS server must contain the appropriate DNS records for the names being resolved.

Conceptually:

```text
Hostname
   ↓
DNS Server
   ↓
IPv4 Address
```

Example:

```text
example.com
     ↓
93.184.216.34
```

The exact DNS-server configuration depends on the Packet Tracer server setup used in the lab.

---

# Step 5 — Configure DNS on R1

Cisco IOS can be configured with a DNS server using:

```cisco
R1(config)# ip name-server <DNS_SERVER_IP>
```

For example:

```cisco
R1(config)# ip name-server 1.1.1.1
```

The repository includes a configuration screenshot specifically showing DNS configuration on R1:

```text
configs/3. R1-dns-config.png
```

---

# Step 6 — Configure Public DNS

The lab also includes a configuration reference for using:

```text
1.1.1.1
```

as a DNS server:

```text
configs/4. dns-enable-1.1.1.1.png
```

Cisco configuration:

```cisco
R1(config)# ip name-server 1.1.1.1
```

You can configure multiple DNS servers when required:

```cisco
R1(config)# ip name-server 1.1.1.1 8.8.8.8
```

This provides alternative DNS servers.

---

# Step 7 — DNS Lookup

Once a DNS server is configured, the router can resolve hostnames.

For example:

```cisco
R1# ping example.com
```

The process is approximately:

```text
R1
 |
 | DNS Query
 | "What is the IP of example.com?"
 ↓
DNS Server
 |
 | DNS Response
 | "example.com = x.x.x.x"
 ↓
R1
 |
 | ICMP Echo
 ↓
Destination
```

This demonstrates two separate operations:

### DNS resolution

```text
example.com
     ↓
IP address
```

### Network communication

```text
IP address
     ↓
Routing
     ↓
Destination
```

---

# Step 8 — Verify DNS Configuration

Check the running configuration:

```cisco
R1# show running-config
```

Look for:

```text
ip name-server
```

You can also use:

```cisco
R1# show hosts
```

to inspect hostname information known to the router.

---

# DNS Lookup Process

A simplified DNS lookup looks like this:

```text
              Client
                |
                | DNS Query
                ↓
          DNS Resolver
                |
                ↓
           Root Server
                |
                ↓
          TLD Server
          (.com/.org/etc.)
                |
                ↓
      Authoritative DNS Server
                |
                ↓
           IP Address
                |
                ↓
          DNS Resolver
                |
                ↓
              Client
```

For a domain such as:

```text
www.example.com
```

the resolver may follow:

```text
Root
 ↓
.com TLD
 ↓
Authoritative DNS
 ↓
www.example.com
 ↓
IP address
```

---

# DNS Record Types

Important DNS records to understand:

| Record | Purpose                     |
| ------ | --------------------------- |
| A      | Hostname → IPv4 address     |
| AAAA   | Hostname → IPv6 address     |
| CNAME  | Alias → hostname            |
| MX     | Mail server                 |
| NS     | Authoritative name server   |
| PTR    | IP address → hostname       |
| TXT    | Text and policy information |

For basic IPv4 DNS labs, the **A record** is particularly important.

Example:

```text
server.example.com
        ↓
192.168.10.10
```

---

# Verification Commands

## Check interface status

```cisco
show ip interface brief
```

## Check routing table

```cisco
show ip route
```

## Test DNS server connectivity

```cisco
ping <DNS_SERVER_IP>
```

## Test hostname resolution

```cisco
ping example.com
```

## Check hostname information

```cisco
show hosts
```

## Check running configuration

```cisco
show running-config
```

---

# Troubleshooting

If DNS resolution doesn't work, don't immediately assume DNS is the problem.

Use a layered troubleshooting approach.

### 1. Check interface status

```cisco
show ip interface brief
```

Look for:

```text
up/up
```

---

### 2. Test the DNS server IP

```cisco
ping <DNS_SERVER_IP>
```

If this fails, investigate:

```text
Interface
   ↓
IP addressing
   ↓
Subnet mask
   ↓
Default gateway
   ↓
Routing
   ↓
ACL / firewall
```

---

### 3. Check DNS configuration

```cisco
show running-config | include name-server
```

Confirm the configured DNS server is correct.

---

### 4. Test hostname resolution

```cisco
ping example.com
```

If:

```text
ping <IP_ADDRESS>
```

works but:

```text
ping example.com
```

fails, investigate DNS resolution.

---

# Common Problems

| Problem                          | Possible Cause                  |
| -------------------------------- | ------------------------------- |
| DNS server unreachable           | Routing/IP connectivity problem |
| Wrong DNS server                 | Incorrect `ip name-server`      |
| Hostname doesn't resolve         | Missing DNS record              |
| Ping IP works but hostname fails | DNS problem                     |
| Interface down                   | Interface configuration/cabling |
| DNS queries blocked              | ACL/firewall                    |
| Incorrect address                | IP/subnet configuration error   |

---

# Important Network Engineering Concept

DNS and routing perform different jobs.

### DNS

```text
Name
 ↓
IP address
```

### Routing

```text
Source IP
 ↓
Routing table
 ↓
Next hop/interface
 ↓
Destination
```

Example:

```text
www.example.com
       ↓
DNS
       ↓
192.168.20.10
       ↓
Routing
       ↓
192.168.20.10
```

This distinction is important when troubleshooting enterprise networks.

---

# Skills Demonstrated

This lab demonstrates practical knowledge of:

* DNS fundamentals
* IPv4 addressing
* Cisco IOS configuration
* DNS server configuration
* Router DNS configuration
* `ip name-server`
* Hostname resolution
* IP connectivity testing
* Basic network troubleshooting
* Cisco Packet Tracer
* Network service configuration

---

# Lab Verification Checklist

Use this checklist after completing the lab:

```text
[ ] Topology configured
[ ] IP addressing configured
[ ] Router interfaces configured
[ ] Interfaces are up/up
[ ] Routing/connectivity verified
[ ] DNS server configured
[ ] DNS server IP reachable
[ ] R1 configured with DNS server
[ ] DNS lookup tested
[ ] Hostname successfully resolved
[ ] Configuration verified
```

---

# Practical Scenario

A network administrator manages a router and needs to access network services using hostnames rather than IP addresses.

Without DNS:

```text
R1# ping 192.168.1.10
```

With DNS:

```text
R1# ping server.company.local
```

DNS translates:

```text
server.company.local
        ↓
192.168.1.10
```

The router can then communicate with the destination using its IP address.

---

# Key Takeaways

1. **DNS translates domain names into IP addresses.**
2. Traditional DNS uses **UDP/TCP port 53**.
3. A Cisco router can be configured with `ip name-server`.
4. DNS resolution and IP connectivity are separate troubleshooting stages.
5. The `A` record maps a hostname to an IPv4 address.
6. DNS caching reduces repeated DNS queries.
7. A working ping to an IP address does not automatically prove that DNS is working.
8. Always verify **IP connectivity before troubleshooting name resolution**.

---

## Lab Resources

* **DNS Packet Tracer lab:** [dns.pkt](https://github.com/kumaradoss16/Networking/blob/main/network-labs/dns/dns.pkt?utm_source=chatgpt.com)
* **DNS topology:** [dns-network-topology.png](https://github.com/kumaradoss16/Networking/blob/main/network-labs/dns/diagram/dns-network-topology.png?utm_source=chatgpt.com)
* **Configuration references:** [DNS configs](https://github.com/kumaradoss16/Networking/tree/main/network-labs/dns/configs?utm_source=chatgpt.com)
* **DNS lab directory:** [network-labs/dns](https://github.com/kumaradoss16/Networking/tree/main/network-labs/dns?utm_source=chatgpt.com)

**One correction worth making in your lab documentation:** if the Packet Tracer lab uses `1.1.1.1`, describe it specifically as a **public DNS resolver** rather than calling it your DNS server in a generic enterprise sense. The repository's configuration evidence explicitly includes `1.1.1.1`.
