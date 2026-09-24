# Standard ACL Lab

## Overview

This lab demonstrates the configuration and testing of Standard Access Control Lists (ACLs) using Cisco Packet Tracer.

The lab covers:

* Basic router configuration
* OSPF routing
* Numbered Standard ACL
* Named Standard ACL
* ACL application and verification
* Connectivity testing

## Lab File

The main Packet Tracer file is:

`acl.pkt`

Open the file with Cisco Packet Tracer to view and test the complete network topology.

## Objectives

* Understand how Standard ACLs work.
* Configure a numbered Standard ACL.
* Configure a named Standard ACL.
* Apply an ACL to a router interface.
* Control traffic based on source IP address.
* Verify ACL configuration and operation.

## Standard ACL

A Standard ACL filters traffic primarily based on the source IPv4 address.

Basic syntax:

```text
access-list <number> permit|deny <source>
```

Example:

```cisco
access-list 1 deny 192.168.1.10
access-list 1 permit any
```

Apply the ACL to an interface:

```cisco
interface gigabitEthernet 0/0
 ip access-group 1 out
```

## Named Standard ACL

A named ACL provides a descriptive name instead of using only a number.

Example:

```cisco
ip access-list standard BLOCK-HOST
 deny host 192.168.1.10
 permit any
```

Apply it to an interface:

```cisco
interface gigabitEthernet 0/0
 ip access-group BLOCK-HOST out
```

## ACL Direction

### Inbound

```cisco
ip access-group 1 in
```

The ACL checks traffic entering the interface.

### Outbound

```cisco
ip access-group 1 out
```

The ACL checks traffic leaving the interface.

## Verification Commands

Check configured ACLs:

```cisco
show access-lists
```

Check interface configuration:

```cisco
show ip interface
```

Check routing information:

```cisco
show ip route
```

Check OSPF neighbors:

```cisco
show ip ospf neighbor
```

Test connectivity:

```cisco
ping <destination-ip>
```

## Lab Structure

```text
standard-acl/
│
├── acl.pkt
│
├── configs/
│   ├── 1. initial-config-R1.png
│   ├── 2. initial-config-R2.png
│   ├── 3. ospf-R1.png
│   ├── 4. ospf-R2.png
│   ├── 5. numbered-acl-R1.png
│   └── 6. named-R2.png
│
└── topology/
    └── standard-acl-network-topology-diagram.png
```

The repository currently contains the Packet Tracer file and separate `configs` and `topology` directories.

The topology directory contains the Standard ACL network diagram.

## Learning Outcome

After completing this lab, you should be able to:

* Explain the purpose of Standard ACLs.
* Create numbered and named ACLs.
* Apply ACLs to router interfaces.
* Understand inbound and outbound ACL processing.
* Verify ACL configuration.
* Test permitted and denied traffic.
* Troubleshoot basic ACL connectivity problems.

## Requirements

* Cisco Packet Tracer
* Basic IPv4 networking knowledge
* Basic Cisco IOS CLI knowledge
* Understanding of routing fundamentals

## Practice

After opening the lab, modify the ACL rules and test different source IP addresses.

Verify the result using:

```cisco
show access-lists
```

and:

```cisco
ping <destination-ip>
```

Compare the connectivity before and after applying the ACL.

## Note

Standard ACLs should generally be positioned close to the destination because they make filtering decisions primarily using the source IP address.
