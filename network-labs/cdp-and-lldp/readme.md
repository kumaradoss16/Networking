# CDP and LLDP Network Lab

Cisco Packet Tracer lab for configuring and verifying **Cisco Discovery Protocol (CDP)** and **Link Layer Discovery Protocol (LLDP)**.

The lab uses three routers and demonstrates neighbor discovery, device/interface identification, protocol configuration, interface-level control, and verification.

## Lab Objectives

* Configure CDP on Cisco routers.
* Configure LLDP on Cisco routers.
* Discover directly connected network devices.
* Identify local and remote interfaces.
* Verify CDP neighbor information.
* Verify LLDP neighbor information.
* Compare CDP and LLDP operation.
* Disable discovery protocols on selected interfaces.
* Verify the effect of interface-level configuration.
* Use CDP and LLDP for network troubleshooting and topology identification.

## Technologies

| Technology          | Purpose                         |
| ------------------- | ------------------------------- |
| Cisco Packet Tracer | Network simulation              |
| Cisco IOS           | Router configuration            |
| CDP                 | Cisco device discovery          |
| LLDP                | Vendor-neutral device discovery |
| Ethernet            | Inter-device connectivity       |

## Repository Structure

```text
cdp-and-lldp/
│
├── configs/
│   ├── 1. initial-config-R1.png
│   ├── 1. initial-config-R2.png
│   ├── 1. initial-config-R3.png
│   ├── 2. enable-cdp-lldp.png
│   ├── 3. interface-hardening.png
│   └── 4. verifications.png
│
├── diagram/
│   └── cdl-lldp-network-topology-diagram.png
│
└── lab-cdp-lldp.pkt
```

The repository currently contains these lab resources under `network-labs/cdp-and-lldp`.

---

# 1. CDP

## Cisco Discovery Protocol

CDP is a Cisco proprietary Layer 2 protocol used to discover information about directly connected Cisco devices.

CDP advertisements can provide information such as:

* Device ID
* Local interface
* Remote interface
* Platform
* Device capabilities
* Software information
* Management address

CDP operates independently of normal Layer 3 routing. A device can discover a directly connected neighbor without requiring an IP route to that neighbor.

---

# 2. LLDP

## Link Layer Discovery Protocol

LLDP is a vendor-neutral Layer 2 neighbor discovery protocol standardized as IEEE 802.1AB.

It allows network devices from different vendors to advertise information about themselves to directly connected devices.

LLDP can provide:

* System name
* Chassis information
* Port information
* Device capabilities
* Management information
* Port description

LLDP is useful when the network contains equipment from multiple vendors.

---

# 3. CDP vs LLDP

| Feature               | CDP                      | LLDP                          |
| --------------------- | ------------------------ | ----------------------------- |
| Full name             | Cisco Discovery Protocol | Link Layer Discovery Protocol |
| Standard              | Cisco proprietary        | IEEE 802.1AB                  |
| OSI layer             | Layer 2                  | Layer 2                       |
| Vendor support        | Cisco-focused            | Multi-vendor                  |
| Neighbor discovery    | Yes                      | Yes                           |
| IP routing required   | No                       | No                            |
| Device information    | Yes                      | Yes                           |
| Interface information | Yes                      | Yes                           |
| Interface control     | Yes                      | Yes                           |
| Typical use           | Cisco networks           | Multi-vendor networks         |

---

# 4. Lab Topology

The lab topology is provided in:

```text
diagram/cdl-lldp-network-topology-diagram.png
```

The Packet Tracer implementation is provided in:

```text
lab-cdp-lldp.pkt
```

The topology contains:

```text
R1
 |
R2
 |
R3
```

The exact interface connections should be taken from the Packet Tracer topology and the supplied topology diagram.

---

# 5. Initial Configuration

Before configuring CDP and LLDP, verify the router interfaces.

```cisco
show ip interface brief
```

Check that the required interfaces are operational.

Expected interface state:

```text
Status: up
Protocol: up
```

Test connectivity where required:

```cisco
ping <destination-ip>
```

The initial configuration screenshots for R1, R2, and R3 are available under:

```text
configs/
```

The repository contains separate initial configuration files for all three routers.

---

# 6. Configure CDP

## Enable CDP Globally

Enter global configuration mode:

```cisco
enable
configure terminal
```

Enable CDP:

```cisco
cdp run
```

Exit:

```cisco
end
```

Verify:

```cisco
show cdp
```

---

# 7. Verify CDP

## Display CDP Neighbors

```cisco
show cdp neighbors
```

This provides a summary of directly connected CDP-enabled devices.

Typical information includes:

```text
Device ID
Local Interface
Holdtime
Capability
Platform
Port ID
```

Example:

```text
R1#show cdp neighbors
```

---

## Display Detailed CDP Information

```cisco
show cdp neighbors detail
```

This provides additional information about discovered neighbors.

Depending on the device and IOS version, the output can include:

```text
Device ID
IP address
Platform
Capabilities
Local interface
Remote port
Software version
```

---

## Display CDP Interface Status

```cisco
show cdp interface
```

This shows CDP operational information for the router's interfaces.

---

## Display CDP Configuration

```cisco
show running-config | include cdp
```

Use this to confirm whether CDP-related configuration is present.

---

# 8. Configure LLDP

## Enable LLDP Globally

Enter configuration mode:

```cisco
enable
configure terminal
```

Enable LLDP:

```cisco
lldp run
```

Exit configuration mode:

```cisco
end
```

Verify:

```cisco
show lldp
```

The lab's CDP/LLDP configuration is documented in:

```text
configs/2. enable-cdp-lldp.png
```

The repository contains this configuration evidence as part of the lab.

---

# 9. Verify LLDP

## Display LLDP Neighbors

```cisco
show lldp neighbors
```

This displays a summary of discovered LLDP neighbors.

Typical information includes:

```text
Device ID
Local Interface
Hold-time
Capability
Port ID
```

---

## Display Detailed LLDP Information

```cisco
show lldp neighbors detail
```

This provides detailed information advertised by the neighboring device.

---

## Display LLDP Interface Information

```cisco
show lldp interface
```

This can be used to check LLDP operation on individual interfaces.

---

## Display Local LLDP Information

```cisco
show lldp local-information
```

This displays information advertised by the local device.

---

# 10. Interface-Level CDP Control

CDP can be disabled on a specific interface while remaining enabled globally.

Example:

```cisco
configure terminal
interface GigabitEthernet0/0
no cdp enable
end
```

Verify:

```cisco
show cdp interface
```

This configuration is useful when CDP is required on some interfaces but should not operate on others.

---

# 11. Interface-Level LLDP Control

LLDP transmit and receive operations can be controlled independently.

Example:

```cisco
configure terminal
interface GigabitEthernet0/0
no lldp transmit
no lldp receive
end
```

Verify:

```cisco
show lldp interface
```

The exact commands supported can vary with the Cisco IOS/device model used in Packet Tracer.

---

# 12. CDP Verification Workflow

Use the following commands:

```cisco
show cdp
```

```cisco
show cdp interface
```

```cisco
show cdp neighbors
```

```cisco
show cdp neighbors detail
```

```cisco
show cdp entry *
```

Recommended workflow:

```text
Check global CDP
      ↓
Check interfaces
      ↓
Check neighbors
      ↓
Check detailed information
      ↓
Verify local/remote interfaces
```

---

# 13. LLDP Verification Workflow

Use:

```cisco
show lldp
```

```cisco
show lldp interface
```

```cisco
show lldp neighbors
```

```cisco
show lldp neighbors detail
```

```cisco
show lldp local-information
```

Recommended workflow:

```text
Check global LLDP
      ↓
Check interfaces
      ↓
Check neighbors
      ↓
Check detailed information
      ↓
Verify advertised information
```

---

# 14. Neighbor Discovery

After enabling the protocols, directly connected devices can be identified through the neighbor tables.

For CDP:

```cisco
show cdp neighbors
```

For LLDP:

```cisco
show lldp neighbors
```

The important relationship is:

```text
Local Device
     |
Local Interface
     |
Network Link
     |
Remote Interface
     |
Remote Device
```

This information is useful when documenting physical and logical network connectivity.

---

# 15. Understanding CDP Output

When using:

```cisco
show cdp neighbors
```

pay attention to:

### Device ID

Identifies the neighboring device.

### Local Interface

The interface on the current router connected to the neighbor.

### Holdtime

The remaining time before the neighbor information expires if another advertisement is not received.

### Capability

Indicates capabilities advertised by the neighbor.

### Platform

Identifies the neighbor's hardware/platform information.

### Port ID

Identifies the remote interface connected to the local interface.

---

# 16. Understanding LLDP Output

When using:

```cisco
show lldp neighbors
```

pay attention to:

### Device ID

Identifies the remote system.

### Local Interface

The interface through which the neighbor was discovered.

### Holdtime

The lifetime of the received LLDP information.

### Capability

Capabilities advertised by the remote device.

### Port ID

The remote port associated with the connection.

---

# 17. Interface Hardening

Neighbor discovery protocols can provide useful information to network administrators.

However, information such as:

```text
Device name
Platform
Software version
Interface information
Management address
Capabilities
```

may not need to be exposed on every interface.

Where CDP or LLDP is unnecessary, it can be disabled at the interface level.

Example:

```cisco
interface GigabitEthernet0/0
no cdp enable
no lldp transmit
no lldp receive
```

The lab includes a dedicated interface-hardening configuration screenshot:

```text
configs/3. interface-hardening.png
```

Do not disable neighbor discovery globally without considering network-management and troubleshooting requirements.

---

# 18. Troubleshooting CDP

## No CDP Neighbors

Check whether CDP is enabled:

```cisco
show cdp
```

Check interface status:

```cisco
show cdp interface
```

Check neighbors:

```cisco
show cdp neighbors
```

Check the running configuration:

```cisco
show running-config | include cdp
```

Check:

* CDP is globally enabled.
* The interface is operational.
* CDP is not disabled on the interface.
* The neighboring device supports CDP.
* CDP is enabled on the neighboring device.
* The devices are directly connected.

---

# 19. Troubleshooting LLDP

## No LLDP Neighbors

Check:

```cisco
show lldp
```

Then:

```cisco
show lldp interface
```

Then:

```cisco
show lldp neighbors
```

Check:

* LLDP is globally enabled.
* LLDP transmit is enabled.
* LLDP receive is enabled.
* The interface is operational.
* The neighbor supports LLDP.
* LLDP is enabled on the neighboring device.

---

# 20. Common Problems

| Problem                          | Possible Cause                 |
| -------------------------------- | ------------------------------ |
| No CDP neighbors                 | CDP disabled                   |
| No LLDP neighbors                | LLDP disabled                  |
| Interface missing from discovery | Protocol disabled on interface |
| Neighbor information disappears  | Advertisement timeout          |
| Incorrect neighbor information   | Wrong physical connection      |
| No discovery                     | Interface/link down            |
| CDP works but LLDP does not      | LLDP not enabled               |
| LLDP works but CDP does not      | CDP not enabled                |

---

# 21. Useful Commands

## CDP

```cisco
show cdp
show cdp interface
show cdp neighbors
show cdp neighbors detail
show cdp entry *
```

## LLDP

```cisco
show lldp
show lldp interface
show lldp neighbors
show lldp neighbors detail
show lldp local-information
```

## Interfaces

```cisco
show ip interface brief
show interfaces
show interfaces description
```

## Configuration

```cisco
show running-config
```

---

# 22. Practical Uses

CDP and LLDP are commonly used for:

### Network Troubleshooting

Determine which device is connected to a particular interface.

### Topology Documentation

Identify device-to-device relationships.

### Device Identification

Determine the platform and capabilities of directly connected devices.

### Port Mapping

Map local interfaces to remote interfaces.

### Network Inventory

Collect information about directly connected infrastructure.

### Multi-Vendor Networks

Use LLDP where devices from multiple vendors are deployed.

---

# 23. Security Considerations

CDP and LLDP are management and discovery protocols, not security mechanisms.

Their advertisements can reveal infrastructure information.

For example:

```text
Hostname
Device type
Interface
Software information
Management information
Capabilities
```

For interfaces where neighbor discovery is not required, consider disabling the relevant protocol.

Example:

```cisco
interface <interface-id>
no cdp enable
no lldp transmit
no lldp receive
```

The correct security configuration depends on the purpose of the interface and the network-management requirements.

---

# 24. Lab Verification Checklist

```text
[ ] Packet Tracer file opens correctly

[ ] R1 initial configuration verified
[ ] R2 initial configuration verified
[ ] R3 initial configuration verified

[ ] CDP enabled
[ ] CDP status verified
[ ] CDP interfaces verified
[ ] CDP neighbors discovered
[ ] CDP detailed information verified

[ ] LLDP enabled
[ ] LLDP status verified
[ ] LLDP interfaces verified
[ ] LLDP neighbors discovered
[ ] LLDP detailed information verified

[ ] Interface-level CDP configuration tested
[ ] Interface-level LLDP configuration tested
[ ] Interface hardening verified

[ ] Neighbor information compared with topology
```

The repository includes a separate verification screenshot for the completed lab.

---

# 25. CDP/LLDP Comparison

```text
                 Neighbor Discovery
                         |
              +----------+----------+
              |                     |
             CDP                   LLDP
              |                     |
       Cisco proprietary       IEEE 802.1AB
              |                     |
       Cisco environments     Multi-vendor networks
              |                     |
              +----------+----------+
                         |
                  Device Information
                         |
              +----------+----------+
              |                     |
        Local Interface       Remote Interface
```

---

# 26. Lab Files

### Packet Tracer Lab

[lab-cdp-lldp.pkt](https://github.com/kumaradoss16/Networking/blob/main/network-labs/cdp-and-lldp/lab-cdp-lldp.pkt)

### Topology Diagram

[cdl-lldp-network-topology-diagram.png](https://github.com/kumaradoss16/Networking/blob/main/network-labs/cdp-and-lldp/diagram/cdl-lldp-network-topology-diagram.png)

### Configuration Evidence

[Configuration Screenshots](https://github.com/kumaradoss16/Networking/tree/main/network-labs/cdp-and-lldp/configs)

### Lab Directory

[CDP and LLDP Lab](https://github.com/kumaradoss16/Networking/tree/main/network-labs/cdp-and-lldp)

---

# 27. Key Commands Reference

```cisco
! CDP
cdp run
show cdp
show cdp interface
show cdp neighbors
show cdp neighbors detail

! LLDP
lldp run
show lldp
show lldp interface
show lldp neighbors
show lldp neighbors detail
show lldp local-information

! Interface-level control
interface GigabitEthernet0/0
no cdp enable
no lldp transmit
no lldp receive

! General verification
show ip interface brief
show interfaces description
show running-config
```

## Result

After completing the lab, the routers should be able to discover their directly connected neighbors using CDP and LLDP. The verification commands should provide enough information to identify the neighboring device, local interface, remote interface, platform/capabilities, and protocol state.

The lab files and supporting configuration evidence are maintained in the `network-labs/cdp-and-lldp` directory of the repository.
