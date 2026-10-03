# Static NAT Lab — Technical Documentation

## 1. Lab Overview

**Static Network Address Translation (Static NAT)** provides a permanent **one-to-one mapping** between a private inside-local IP address and a public inside-global IP address.

This lab demonstrates how to configure a Cisco router to:

* Identify the **inside** and **outside** NAT interfaces.
* Create a permanent one-to-one Static NAT mapping.
* Allow an internal server to be represented by a public IP address.
* Verify NAT translations.
* Test connectivity from an external network.
* Troubleshoot common Static NAT configuration problems.

Static NAT is commonly used when an internal resource, such as a **web server, mail server, DNS server, or application server**, must be reachable using a predictable public IP address. ([GitHub][1])

---

## 2. Network Address Translation Concepts

NAT changes IP addressing information as packets cross a router.

For Static NAT, the important terminology is:

| NAT Term           | Description                                      |
| ------------------ | ------------------------------------------------ |
| **Inside Local**   | Private IP address assigned to the internal host |
| **Inside Global**  | Public IP address representing the internal host |
| **Outside Local**  | Outside host's address as seen from the inside   |
| **Outside Global** | Actual address of the outside host               |

The fundamental Static NAT relationship is:

```text
Inside Local  <──────────>  Inside Global
Private IP                Public IP
```

For example:

```text
192.168.1.10  <──────────>  203.0.113.10
   Private                     Public
```

The mapping remains configured even when there is no active traffic.

---

# 3. Lab Objective

The objectives of this lab are to:

1. Configure the router's internal interface as `ip nat inside`.
2. Configure the external interface as `ip nat outside`.
3. Configure a Static NAT translation.
4. Test communication between internal and external hosts.
5. Verify the NAT translation table.
6. Verify NAT statistics.
7. Troubleshoot failed translations.

---

# 4. Reference Topology

The logical topology can be represented as:

```text
             PRIVATE / INSIDE                    PUBLIC / OUTSIDE

       ┌──────────────┐
       │ Internal     │
       │ Server       │
       │ Private IP   │
       └──────┬───────┘
              │
              │
        ip nat inside
              │
        ┌─────┴─────┐
        │   Cisco   │
        │   Router  │
        │    NAT    │
        └─────┬─────┘
              │
        ip nat outside
              │
              │
       ┌──────┴───────┐
       │ External     │
       │ Network /    │
       │ Client       │
       └──────────────┘
```

The internal server uses a **private address**, while external devices communicate with the server through its **public Static NAT address**.

---

# 5. Prerequisites

Before configuring the lab, ensure that:

* Cisco Packet Tracer or the appropriate Cisco IOS environment is available.
* Router interfaces are physically connected.
* Internal and external interfaces have valid IP addresses.
* The internal server has the router configured as its default gateway.
* The external network has a route toward the NAT router.
* The public IP used for Static NAT is available on the outside network.
* Basic IP connectivity has been verified before configuring NAT.

---

# 6. Static NAT Configuration

## Step 1 — Configure the Inside Interface

The interface connected to the internal/private network must be identified as a NAT inside interface.

```cisco
Router(config)# interface GigabitEthernet0/0
Router(config-if)# ip nat inside
Router(config-if)# exit
```

Depending on the topology, the interface could instead be `FastEthernet0/0`, `GigabitEthernet0/1`, or another interface.

The important requirement is:

```cisco
ip nat inside
```

---

## Step 2 — Configure the Outside Interface

The interface connected toward the external/public network must be identified as the NAT outside interface.

```cisco
Router(config)# interface GigabitEthernet0/1
Router(config-if)# ip nat outside
Router(config-if)# exit
```

Therefore, the NAT boundary becomes:

```text
Internal LAN
     │
     │
ip nat inside
     │
  Router
     │
ip nat outside
     │
     │
External Network
```

Cisco Static NAT examples similarly designate the internal-facing interface as `ip nat inside` and the Internet-facing interface as `ip nat outside`. ([GitHub][1])

---

# 7. Configure Static NAT Mapping

The primary Static NAT command is:

```cisco
Router(config)# ip nat inside source static <inside-local-ip> <inside-global-ip>
```

For example:

```cisco
Router(config)# ip nat inside source static 192.168.1.10 203.0.113.10
```

This creates the permanent mapping:

```text
192.168.1.10
     │
     │ Static NAT
     ▼
203.0.113.10
```

Where:

```text
192.168.1.10   = Inside Local
203.0.113.10   = Inside Global
```

The exact IP addresses should be replaced with the addresses defined in your lab topology.

---

# 8. Complete Router Configuration

A typical Static NAT router configuration is:

```cisco
enable
configure terminal

!
! Inside interface
!
interface GigabitEthernet0/0
 ip address <INSIDE-ROUTER-IP> <SUBNET-MASK>
 ip nat inside
 no shutdown
 exit

!
! Outside interface
!
interface GigabitEthernet0/1
 ip address <OUTSIDE-ROUTER-IP> <SUBNET-MASK>
 ip nat outside
 no shutdown
 exit

!
! Static NAT
!
ip nat inside source static <PRIVATE-SERVER-IP> <PUBLIC-NAT-IP>

end
write memory
```

For example:

```cisco
ip nat inside source static 192.168.1.10 203.0.113.10
```

---

# 9. Packet Flow

## Internal → External

When the internal server sends traffic toward an external destination:

```text
Internal Server
192.168.1.10
      │
      ▼
NAT Router
      │
      │ Source translated
      ▼
203.0.113.10
      │
      ▼
External Network
```

The router translates the source address from the private **inside-local** address to the public **inside-global** address.

---

## External → Internal

Static NAT also permits an external host to initiate communication toward the mapped public address.

```text
External Client
203.0.113.X
      │
      │ Destination:
      │ 203.0.113.10
      ▼
NAT Router
      │
      │ Translation
      ▼
192.168.1.10
      │
      ▼
Internal Server
```

This bidirectional nature is one reason Static NAT is commonly used for publicly reachable internal servers. ([GitHub][2])

---

# 10. Verification Commands

After configuration, use the following commands.

## Check NAT translations

```cisco
Router# show ip nat translations
```

A Static NAT entry should appear similar to:

```text
Pro  Inside global      Inside local       Outside local      Outside global
---  203.0.113.10       192.168.1.10       ---                ---
```

The `---` protocol entry represents the permanent Static NAT mapping.

When traffic is generated, additional protocol/session entries may appear. ([GitHub][1])

---

## Check NAT statistics

```cisco
Router# show ip nat statistics
```

This can be used to inspect:

* Active translations
* Configured translations
* Interfaces marked inside/outside
* NAT hits
* NAT misses

---

## Check interface configuration

```cisco
Router# show ip interface brief
```

Then verify the detailed interface configuration:

```cisco
Router# show running-config interface GigabitEthernet0/0
Router# show running-config interface GigabitEthernet0/1
```

Confirm that the correct interfaces contain:

```cisco
ip nat inside
```

and:

```cisco
ip nat outside
```

---

# 11. Connectivity Testing

## Test 1 — Basic Internal Connectivity

From the internal server:

```text
ping <inside-router-IP>
```

The server should successfully reach its default gateway.

---

## Test 2 — External Connectivity

From the external host, test the public NAT address:

```text
ping <PUBLIC-NAT-IP>
```

For example:

```text
ping 203.0.113.10
```

If ICMP is permitted and routing is correct, the internal server should respond.

---

## Test 3 — Check NAT Table

Immediately after generating traffic:

```cisco
Router# show ip nat translations
```

Traffic should cause the corresponding active translation/session information to appear.

---

# 12. Troubleshooting

## Problem 1 — No NAT Translation

Check:

```cisco
show ip nat translations
```

Then verify:

```cisco
show running-config
```

Look for:

```cisco
ip nat inside source static ...
```

---

## Problem 2 — Incorrect NAT Interface

Verify that the interfaces are correctly classified:

```cisco
interface GigabitEthernet0/0
 ip nat inside
```

and:

```cisco
interface GigabitEthernet0/1
 ip nat outside
```

A common configuration error is accidentally applying `ip nat inside` or `ip nat outside` to the wrong interface.

---

## Problem 3 — Routing Problem

NAT does not replace routing.

Check the routing table:

```cisco
Router# show ip route
```

Verify that the router knows how to reach:

* The internal network
* The external network
* The external client's network

---

## Problem 4 — Internal Server Has Incorrect Gateway

The internal server must use the router's inside interface as its default gateway.

For example:

```text
Server IP:       192.168.1.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.1.1
```

The exact values depend on the lab topology.

---

## Problem 5 — NAT Works but Ping Fails

Check whether ICMP is permitted by the devices involved.

Also verify:

```cisco
show ip nat translations
show ip nat statistics
```

Generate traffic again if necessary. NAT translation/session entries associated with traffic can change as traffic is generated and ages out. ([GitHub][1])

---

# 13. Useful Verification Command Summary

| Purpose                         | Cisco Command                               |
| ------------------------------- | ------------------------------------------- |
| Display NAT translations        | `show ip nat translations`                  |
| Display NAT statistics          | `show ip nat statistics`                    |
| Display routing table           | `show ip route`                             |
| Display interfaces              | `show ip interface brief`                   |
| Display running configuration   | `show running-config`                       |
| Display interface configuration | `show running-config interface <interface>` |
| Test connectivity               | `ping <ip-address>`                         |
| Trace packet path               | `traceroute <ip-address>`                   |

---

# 14. Expected Result

After successful configuration:

```text
Private Server
192.168.1.10
      │
      │
      ▼
Cisco Router
      │
      │ Static NAT
      ▼
Public Address
203.0.113.10
      │
      ▼
External Network
```

The router maintains the permanent relationship:

```text
Inside Local       Inside Global
192.168.1.10  ↔    203.0.113.10
```

An external client can therefore address the internal server through its configured public address, provided routing and any relevant filtering/firewall rules permit the traffic.

---

# 15. Key Learning Points

* **Static NAT provides a one-to-one mapping.**
* The mapping is manually configured and permanent.
* `ip nat inside` identifies the internal side of the NAT boundary.
* `ip nat outside` identifies the external side.
* `ip nat inside source static` creates the one-to-one mapping.
* `show ip nat translations` verifies the translation table.
* `show ip nat statistics` provides NAT operational information.
* Static NAT consumes one public IP for each permanently mapped internal host, so it is less scalable than PAT for large numbers of clients. ([GitHub][2])
* Static NAT is particularly useful for internal services that need a predictable public address.

## 16. GitHub Lab Reference

**Source lab:**

[kumaradoss16/Networking — lab-static-nat](https://github.com/kumaradoss16/Networking/tree/main/network-labs/lab-static-nat?utm_source=chatgpt.com)

**Suggested GitHub filename:**

```text
README.md
```

You can place the documentation above directly inside the `lab-static-nat` directory alongside the Packet Tracer `.pkt` file and any topology screenshots.

[1]: https://github.com/GARJE-01/cisco-ccna-lab-notes/blob/main/modules/29-1-NAT-Configuration.md?utm_source=chatgpt.com "cisco-ccna-lab-notes/modules/29-1-NAT-Configuration.md at main · GARJE-01/cisco-ccna-lab-notes · GitHub"
[2]: https://github.com/Arthur-K-99/cisco-nat-lab?utm_source=chatgpt.com "GitHub - Arthur-K-99/cisco-nat-lab: Containerlab lab covering seven Cisco IOS-XE NAT scenarios with guided verification and troubleshooting. · GitHub"
