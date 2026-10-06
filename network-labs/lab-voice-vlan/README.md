# Voice VLAN Configuration

## 1. Overview

This lab demonstrates the configuration of a **Voice VLAN** on a Cisco switch to separate IP phone traffic from normal data traffic.

The design uses:

* Cisco switch — Layer 2 access switching
* Cisco router — Inter-VLAN routing using Router-on-a-Stick
* Data VLAN — User/data traffic
* Voice VLAN — IP phone traffic
* DHCP — Dynamic IP address assignment
* Cisco CME — Basic IP telephony service
* Cisco Packet Tracer — Lab simulation

The lab files are available in the repository:

`network-labs/lab-voice-vlan/`

---

## 2. Purpose

The purpose of a Voice VLAN is to logically separate **voice traffic from normal data traffic** on an access switch port.

A typical IP phone connection looks like:

```text
                Cisco Switch
                    |
              Access Port
                    |
                IP Phone
                 /    \
                /      \
             PC       Voice
                     VLAN
```

The switch port can carry:

* Data traffic → Data VLAN
* Voice traffic → Voice VLAN

This allows a computer and IP phone to share the same physical switch port while remaining logically separated.

---

# 3. Network Design

The implementation follows this general traffic flow:

```text
              ┌─────────────────┐
              │      R1         │
              │ Router-on-a-    │
              │     Stick       │
              └────────┬────────┘
                       │
                     Trunk
                       │
              ┌────────┴────────┐
              │      SW1        │
              │ Cisco Switch    │
              └───────┬─────────┘
                      │
                Access Port
                      │
                  IP Phone
                      │
                     PC
```

The physical connection uses one switch port while the switch logically separates data and voice traffic using VLANs.

---

# 4. VLAN Configuration

## Create the Data VLAN

```cisco
Switch(config)# vlan <DATA_VLAN>
Switch(config-vlan)# name DATA
```

### Purpose

`vlan <DATA_VLAN>`

Creates a VLAN for normal user/data traffic.

`name DATA`

Provides a descriptive name for easier administration and troubleshooting.

---

## Create the Voice VLAN

```cisco
Switch(config)# vlan <VOICE_VLAN>
Switch(config-vlan)# name VOICE
```

### Purpose

`vlan <VOICE_VLAN>`

Creates a dedicated VLAN for IP phone traffic.

`name VOICE`

Makes the VLAN easier to identify in the configuration.

---

# 5. Configure the Switch Access Port

The switch port connected to the IP phone is configured as an access port.

```cisco
Switch(config)# interface fa0/1
Switch(config-if)# switchport mode access
```

### Purpose

```cisco
switchport mode access
```

Forces the interface to operate as an **access port**.

This is appropriate for an endpoint-facing port rather than a switch-to-switch trunk.

---

## Assign the Data VLAN

```cisco
Switch(config-if)# switchport access vlan <DATA_VLAN>
```

### Purpose

Assigns the normal untagged data traffic from the connected PC to the Data VLAN.

For example:

```text
PC
 ↓
Data VLAN
 ↓
Switch
```

---

## Assign the Voice VLAN

```cisco
Switch(config-if)# switchport voice vlan <VOICE_VLAN>
```

### Purpose

This is the most important command in the Voice VLAN configuration.

It tells the Cisco switch to place recognized voice traffic from the IP phone into the specified Voice VLAN.

Example:

```cisco
switchport access vlan 10
switchport voice vlan 20
```

Conceptually:

```text
             SW1 Fa0/1
                 │
        ┌────────┴────────┐
        │                 │
       PC              IP Phone
        │                 │
    VLAN 10           VLAN 20
     DATA              VOICE
```

The PC and phone can therefore share the same physical switch port while using different VLANs.

---

# 6. Configure PortFast

For an endpoint-facing port, PortFast can be enabled:

```cisco
Switch(config-if)# spanning-tree portfast
```

### Purpose

PortFast allows the access port to transition to the forwarding state quickly.

This is useful for end devices such as:

* PCs
* IP phones
* Printers

It avoids unnecessary waiting through normal STP transition states.

**Important:** PortFast should normally be used on ports connected to end devices, not on switch-to-switch links.

---

# 7. Router-on-a-Stick Configuration

Because the Data VLAN and Voice VLAN are separate Layer 2 networks, communication between them requires Layer 3 routing.

A router can perform this using **Router-on-a-Stick**.

Example:

```cisco
Router(config)# interface g0/0
Router(config-if)# no shutdown
```

### Purpose

Enables the physical router interface that connects to the switch.

---

## Data VLAN Subinterface

```cisco
Router(config)# interface g0/0.<DATA_VLAN>
Router(config-subif)# encapsulation dot1Q <DATA_VLAN>
Router(config-subif)# ip address <DATA_GATEWAY> <SUBNET_MASK>
```

### Purpose

`interface g0/0.<DATA_VLAN>`

Creates a logical subinterface for the Data VLAN.

`encapsulation dot1Q <DATA_VLAN>`

Associates the subinterface with the corresponding IEEE 802.1Q VLAN tag.

`ip address`

Provides the default gateway for devices in the Data VLAN.

---

## Voice VLAN Subinterface

```cisco
Router(config)# interface g0/0.<VOICE_VLAN>
Router(config-subif)# encapsulation dot1Q <VOICE_VLAN>
Router(config-subif)# ip address <VOICE_GATEWAY> <SUBNET_MASK>
```

### Purpose

Creates the Layer 3 gateway for the Voice VLAN.

Voice devices use this address as their default gateway.

---

# 8. Configure the Switch Trunk

The switch interface connected to the router must carry multiple VLANs.

```cisco
Switch(config)# interface g0/1
Switch(config-if)# switchport mode trunk
```

### Purpose

```cisco
switchport mode trunk
```

Configures the interface as a trunk.

A trunk allows multiple VLANs to travel across the same physical link using VLAN tagging.

Traffic flow:

```text
Data VLAN ───┐
             │
             ├── Trunk ─── R1
             │
Voice VLAN ──┘
```

---

# 9. DHCP Configuration

The router can provide DHCP services for the Data and Voice VLANs.

Example:

```cisco
Router(config)# ip dhcp pool DATA
Router(dhcp-config)# network <DATA_NETWORK> <SUBNET_MASK>
Router(dhcp-config)# default-router <DATA_GATEWAY>
```

### Purpose

`ip dhcp pool DATA`

Creates a DHCP address pool.

`network`

Defines the network from which addresses are allocated.

`default-router`

Specifies the default gateway provided to DHCP clients.

---

## Voice DHCP Pool

```cisco
Router(config)# ip dhcp pool VOICE
Router(dhcp-config)# network <VOICE_NETWORK> <SUBNET_MASK>
Router(dhcp-config)# default-router <VOICE_GATEWAY>
```

### Purpose

Provides IP addresses to devices in the Voice VLAN.

For Cisco IP phones, the DHCP configuration may additionally provide **TFTP/CME information**, depending on the lab design.

---

# 10. Cisco CME Configuration

Cisco CallManager Express (CME) can provide basic IP telephony services on the router.

A typical configuration begins with:

```cisco
Router(config)# telephony-service
```

### Purpose

Enters Cisco CME telephony-service configuration mode.

The CME configuration can define parameters such as:

* Maximum directory numbers
* Maximum phones
* IP phone registration
* TFTP service
* Directory numbers

Example:

```cisco
Router(config-telephony)# max-ephones 10
Router(config-telephony)# max-dn 10
```

### Purpose

`max-ephones`

Defines the maximum number of IP phones that can be registered.

`max-dn`

Defines the maximum number of directory numbers.

---

# 11. Verification

Configuration should always be followed by verification.

## Verify VLANs

```cisco
Switch# show vlan brief
```

### Purpose

Displays VLANs configured on the switch and their associated access ports.

Check that:

* Data VLAN exists
* Voice VLAN exists
* Access ports are correctly assigned

---

## Verify the Interface

```cisco
Switch# show interfaces fa0/1 switchport
```

### Purpose

Displays detailed Layer 2 information about the interface.

Verify:

```text
Administrative Mode: static access
Operational Mode: static access
Access Mode VLAN: <DATA_VLAN>
Voice VLAN: <VOICE_VLAN>
```

This is one of the most useful commands for troubleshooting Voice VLAN configuration.

---

## Verify Trunk

```cisco
Switch# show interfaces trunk
```

### Purpose

Confirms that the switch-to-router interface is operating as a trunk.

Verify that the required VLANs are allowed across the trunk.

---

## Verify Router Interfaces

```cisco
Router# show ip interface brief
```

### Purpose

Provides a quick summary of router interfaces and their IP addresses/status.

Check that the required subinterfaces are:

```text
up
up
```

---

## Verify DHCP

```cisco
Router# show ip dhcp binding
```

### Purpose

Displays IP addresses currently leased to DHCP clients.

This helps confirm that devices are successfully receiving addresses.

---

## Verify IP Phone Registration

For Cisco CME:

```cisco
Router# show ephone registered
```

### Purpose

Displays registered Cisco IP phones.

This verifies that the phone can communicate with the CME service.

---

# 12. End-to-End Verification

A successful Voice VLAN implementation should be tested in stages.

### Test 1 — VLAN

```text
show vlan brief
```

Confirm that the VLANs exist.

### Test 2 — Switch Port

```text
show interfaces fa0/1 switchport
```

Confirm:

```text
Access VLAN → Data VLAN
Voice VLAN  → Voice VLAN
```

### Test 3 — Trunk

```text
show interfaces trunk
```

Confirm that the required VLANs are being transported.

### Test 4 — IP Addressing

Check the IP phone and PC addresses.

The devices should receive addresses from their respective networks.

### Test 5 — Gateway Connectivity

Ping the appropriate default gateway.

### Test 6 — Phone Registration

```text
show ephone registered
```

Confirm that the IP phone has registered with CME.

---

# 13. Troubleshooting

## Problem: Phone does not receive an IP address

Check:

```cisco
Switch# show interfaces fa0/1 switchport
```

Verify:

```text
Voice VLAN: <VOICE_VLAN>
```

Then check DHCP:

```cisco
Router# show ip dhcp binding
```

Possible causes:

* Incorrect Voice VLAN
* DHCP pool misconfiguration
* Trunk problem
* Router subinterface problem
* Physical/link issue

---

## Problem: PC works but IP phone does not

Check:

```cisco
show interfaces fa0/1 switchport
```

The port should have both:

```text
Access VLAN
Voice VLAN
```

For example:

```text
switchport access vlan 10
switchport voice vlan 20
```

---

## Problem: VLAN does not reach the router

Check:

```cisco
show interfaces trunk
```

Verify that the Data and Voice VLANs are allowed on the trunk.

Then check the router subinterfaces:

```cisco
show ip interface brief
```

---

## Problem: Phone receives an IP but does not register

Check:

```cisco
show ephone registered
```

Then verify:

* CME configuration
* DHCP/TFTP information
* Voice VLAN connectivity
* Router subinterface
* IP addressing
* Phone configuration

---

# 14. Key Commands Summary

| Command                       | Purpose                               |
| ----------------------------- | ------------------------------------- |
| `vlan <id>`                   | Creates a VLAN                        |
| `name <name>`                 | Names the VLAN                        |
| `interface <port>`            | Selects a switch interface            |
| `switchport mode access`      | Makes the port an access port         |
| `switchport access vlan <id>` | Assigns the data VLAN                 |
| `switchport voice vlan <id>`  | Assigns the voice VLAN                |
| `switchport mode trunk`       | Makes the link a trunk                |
| `spanning-tree portfast`      | Speeds up endpoint port forwarding    |
| `interface g0/0.<id>`         | Creates a router subinterface         |
| `encapsulation dot1Q <id>`    | Associates a subinterface with a VLAN |
| `ip address`                  | Assigns a Layer 3 address             |
| `ip dhcp pool`                | Creates a DHCP pool                   |
| `default-router`              | Defines the DHCP client's gateway     |
| `telephony-service`           | Enters Cisco CME configuration        |
| `show vlan brief`             | Verifies VLANs                        |
| `show interfaces switchport`  | Verifies switchport configuration     |
| `show interfaces trunk`       | Verifies trunk operation              |
| `show ip interface brief`     | Verifies Layer 3 interfaces           |
| `show ip dhcp binding`        | Verifies DHCP leases                  |
| `show ephone registered`      | Verifies registered IP phones         |

---

# 15. Configuration Logic

The complete configuration can be understood as:

```text
1. Create VLANs
       ↓
2. Configure switch access port
       ↓
3. Assign Data VLAN
       ↓
4. Assign Voice VLAN
       ↓
5. Configure trunk toward router
       ↓
6. Configure Router-on-a-Stick
       ↓
7. Configure DHCP
       ↓
8. Configure CME
       ↓
9. Connect IP phone
       ↓
10. Verify VLAN / trunk / DHCP / phone
```

---

# 16. Important Concept

The most important command for this lab is:

```cisco
switchport voice vlan <VOICE_VLAN>
```

It tells the switch:

> "Use this VLAN for voice traffic on this access port."

While:

```cisco
switchport access vlan <DATA_VLAN>
```

defines the VLAN for normal data traffic.

Therefore, one physical switch port can provide:

```text
             Switch Port
                  │
          ┌───────┴────────┐
          │                │
        Data             Voice
         PC              Phone
          │                │
     Data VLAN         Voice VLAN
```

This is the fundamental concept behind **Voice VLAN configuration**.

---

# 17. Lab Evidence

The repository contains the corresponding lab evidence:

```text
lab-voice-vlan/
├── configs/
│   ├── 1. SW1-initial-config.png
│   ├── 2. config-port-SW1.png
│   ├── 3. R1-roas-config.png
│   ├── 4. R1-dhcp-data-vlan-config.png
│   ├── 5. R1-cme-config.png
│   └── cme-notes.png
│
├── diagram/
│   └── voice-vlan-network-topology.png
│
└── topology/
    └── voice-vlan.pkt
```

These files provide the Packet Tracer topology, configuration evidence, network diagram, DHCP configuration, Router-on-a-Stick configuration, and CME configuration used in the lab.

---

# 18. Learning Outcome

After completing this lab, you should be able to:

* Explain the purpose of a Voice VLAN.
* Create and configure Data and Voice VLANs.
* Configure a switch access port for an IP phone and PC.
* Configure `switchport voice vlan`.
* Configure an 802.1Q trunk.
* Configure Router-on-a-Stick.
* Configure DHCP for network segments.
* Understand the basic Cisco CME workflow.
* Verify Voice VLAN operation using Cisco IOS commands.
* Troubleshoot common VLAN, trunk, DHCP, and IP phone connectivity problems.
