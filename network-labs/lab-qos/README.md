# QoS Protocol Lab Configuration

This lab demonstrates a Quality of Service (QoS) configuration workflow using Cisco Packet Tracer, with the configuration stages documented through router, switch, PC, ACL, class-map, QoS policy, and interface-application screenshots.

## 1. Lab Reference

Repository:

[kumaradoss16/Networking — lab-qos](https://github.com/kumaradoss16/Networking/tree/main/network-labs/lab-qos?utm_source=chatgpt.com)

Lab directory:

```text
network-labs/lab-qos/
├── configs/
├── diagram/
└── topology/
```

The repository does not contain a textual README inside `lab-qos`. The lab configuration is represented through the Packet Tracer topology, topology diagram, and configuration screenshots.

The parent `network-labs` documentation identifies the lab environment as Cisco Packet Tracer with Cisco IOS-based routers and switches, IPv4 networking, Ethernet interfaces, CLI configuration, and verification. ([Gist][1])

## 2. Lab Files

The repository contains the following files.

```text
network-labs/lab-qos/
│
├── configs/
│   ├── 1. R1-initial-config.png
│   ├── 2. R1-static-route-config.png
│   ├── 3. R2-initial-config.png
│   ├── 4. R2-static-route-config.png
│   ├── 5. SW1-config.png
│   ├── 6. SW2-config.png
│   ├── 7. PC1-config.png
│   ├── 8. test-connectivity-before-qos.png
│   ├── 9. R1-acl-config.png
│   ├── 10. R1-class-map-config.png
│   ├── 11. R1-qos-policy-config.png
│   ├── 12. apply-qos-to-R1.png
│   ├── 13. R2-qos-config.png
│   └── notes.png
│
├── diagram/
│   └── qos-network-topology.png
│
└── topology/
    └── lab-qos.pkt
```

## 3. Lab Components

The configuration evidence identifies these devices:

| Device                 | Role in Lab                                                                   |
| ---------------------- | ----------------------------------------------------------------------------- |
| R1                     | Primary router where ACL, class-map and QoS policy configuration is performed |
| R2                     | Second router participating in the network and QoS configuration              |
| SW1                    | First switch                                                                  |
| SW2                    | Second switch                                                                 |
| PC1                    | End host used for the lab                                                     |
| Packet Tracer topology | Complete practical lab environment                                            |

## 4. Lab Workflow

The repository's configuration files show the following sequence:

```text
R1 Initial Configuration
        |
        v
R1 Static Route Configuration
        |
        v
R2 Initial Configuration
        |
        v
R2 Static Route Configuration
        |
        v
SW1 Configuration
        |
        v
SW2 Configuration
        |
        v
PC1 Configuration
        |
        v
Connectivity Test
        |
        v
R1 ACL Configuration
        |
        v
R1 Class-Map Configuration
        |
        v
R1 QoS Policy Configuration
        |
        v
Apply QoS to R1
        |
        v
R2 QoS Configuration
```

This ordering is directly represented by the numbered configuration screenshots in the repository.

## 5. Initial R1 Configuration

Reference:

```text
configs/1. R1-initial-config.png
```

This screenshot documents the initial configuration stage for **R1**.

The exact commands and addressing values are contained inside the PNG rather than a text configuration file. Therefore, they should be copied from the repository screenshot when reproducing the lab.

## 6. R1 Static Route Configuration

Reference:

```text
configs/2. R1-static-route-config.png
```

This stage configures the static routing information required on R1.

The lab establishes routing before QoS configuration so that connectivity can be verified independently of the QoS policy.

## 7. Initial R2 Configuration

Reference:

```text
configs/3. R2-initial-config.png
```

This screenshot documents the initial configuration of **R2**.

The exact interface addresses and IOS commands are contained in the screenshot.

## 8. R2 Static Route Configuration

Reference:

```text
configs/4. R2-static-route-config.png
```

The static routing configuration for R2 is documented here.

Both routers therefore have their routing configuration established before the QoS portion of the lab.

## 9. SW1 Configuration

Reference:

```text
configs/5. SW1-config.png
```

This screenshot documents the configuration of **SW1**.

The switch provides the Layer 2 connectivity required by the topology.

## 10. SW2 Configuration

Reference:

```text
configs/6. SW2-config.png
```

This screenshot documents the configuration of **SW2**.

Together with SW1, the switches provide the LAN-side connectivity used by the lab topology.

## 11. PC1 Configuration

Reference:

```text
configs/7. PC1-config.png
```

This screenshot documents the network configuration of **PC1**.

PC1 is used as the end host for connectivity testing.

## 12. Connectivity Test Before QoS

Reference:

```text
configs/8. test-connectivity-before-qos.png
```

The lab performs a connectivity test before applying QoS.

This establishes a baseline:

```text
Network Connectivity
        |
        v
Routing Verification
        |
        v
QoS Configuration
```

The purpose is to verify that the underlying network is functioning before introducing traffic classification and QoS policy configuration.

## 13. ACL Configuration on R1

Reference:

```text
configs/9. R1-acl-config.png
```

The next stage configures an ACL on R1.

The repository explicitly identifies this stage as:

```text
R1 ACL Configuration
```

The ACL forms part of the traffic-identification process used before the QoS policy is configured.

The exact ACL number, statements, addresses, and commands should be taken directly from the screenshot because the repository does not provide this configuration as a text file.

## 14. Class-Map Configuration on R1

Reference:

```text
configs/10. R1-class-map-config.png
```

The lab then configures a **class-map** on R1.

A class-map defines the traffic classification that will subsequently be handled by the QoS policy.

The configuration sequence is therefore:

```text
ACL
 |
 v
Class Map
 |
 v
QoS Policy
 |
 v
Interface
```

The exact class-map name and matching statements are documented in the repository screenshot.

## 15. QoS Policy Configuration on R1

Reference:

```text
configs/11. R1-qos-policy-config.png
```

The QoS policy is configured after the traffic classification stage.

The policy-map determines what QoS treatment is applied to traffic belonging to the configured class.

The repository identifies this configuration specifically as:

```text
R1 QoS Policy Configuration
```

The exact policy name and policy actions should be taken from the screenshot.

## 16. Applying QoS to R1

Reference:

```text
configs/12. apply-qos-to-R1.png
```

After creating the QoS policy, the policy is applied to R1.

The configuration sequence is:

```text
1. Identify traffic
        |
        v
2. Create class-map
        |
        v
3. Create QoS policy
        |
        v
4. Apply policy to R1
```

A QoS policy has no operational effect on an interface until it is associated with the appropriate interface using the configuration shown in the repository.

## 17. R2 QoS Configuration

Reference:

```text
configs/13. R2-qos-config.png
```

The final numbered configuration screenshot documents QoS-related configuration on **R2**.

The exact commands and parameters should be reproduced from this screenshot rather than replaced with a generic Cisco QoS configuration.

## 18. QoS Configuration Model

The configuration sequence in this lab can be represented as:

```text
                    QoS Configuration

                         Traffic
                            |
                            v
                    +---------------+
                    |      ACL      |
                    +---------------+
                            |
                            v
                    +---------------+
                    |   Class-Map   |
                    +---------------+
                            |
                            v
                    +---------------+
                    |   Policy-Map  |
                    +---------------+
                            |
                            v
                    +---------------+
                    |    R1 / R2    |
                    |   Interface   |
                    +---------------+
                            |
                            v
                       QoS Treatment
```

The repository's screenshot sequence supports this configuration order.

## 19. Why the Lab Tests Connectivity First

The file:

```text
configs/8. test-connectivity-before-qos.png
```

is placed before the QoS-specific configuration files.

This is useful when troubleshooting because it separates two possible failure areas:

```text
Connectivity failure
        |
        +-- Interface configuration
        +-- IP addressing
        +-- Switching
        +-- Static routing
        +-- Host configuration

QoS-related problem
        |
        +-- ACL
        +-- Class-map
        +-- Policy-map
        +-- Interface policy application
```

If connectivity already works before QoS configuration, later problems can be investigated specifically within the QoS configuration stages.

## 20. Configuration Dependencies

The lab configuration follows these dependencies:

| Stage                | Depends On                          |
| -------------------- | ----------------------------------- |
| Static routing       | Initial router configuration        |
| Switch configuration | Router/LAN topology                 |
| PC configuration     | LAN addressing                      |
| Connectivity test    | Router, switch and PC configuration |
| ACL                  | Basic network connectivity          |
| Class-map            | Traffic classification requirements |
| QoS policy           | Class-map                           |
| QoS application      | QoS policy                          |
| R2 QoS configuration | Existing network configuration      |

## 21. Verification Approach

The repository contains a dedicated pre-QoS connectivity test:

```text
configs/8. test-connectivity-before-qos.png
```

For reproduction, verification should follow the evidence contained in the lab screenshots and Packet Tracer topology.

The parent network-labs documentation identifies common Cisco IOS verification commands such as:

```cisco
show running-config
show ip interface brief
show ip route
ping
traceroute
```

These are general repository-level verification references; the QoS lab itself does not contain a text file specifying a complete QoS verification command set.

## 22. QoS Troubleshooting Sequence

When reproducing this lab, troubleshoot in the same order as the configuration dependencies.

### Step 1: Check interfaces

Verify that the required router and switch interfaces are operational.

```text
Interface
   |
   +-- Correct configuration
   +-- Correct status
   +-- Correct addressing
```

### Step 2: Check routing

Verify that R1 and R2 have the required static routes.

```text
R1
 |
 +-- Static route
 |
R2
 |
 +-- Static route
```

### Step 3: Check host connectivity

Use the connectivity test represented by:

```text
configs/8. test-connectivity-before-qos.png
```

### Step 4: Check ACL

Inspect:

```text
configs/9. R1-acl-config.png
```

Confirm that the ACL configuration corresponds to the traffic that the lab intends to classify.

### Step 5: Check class-map

Inspect:

```text
configs/10. R1-class-map-config.png
```

Confirm that the class-map references the intended traffic classification.

### Step 6: Check QoS policy

Inspect:

```text
configs/11. R1-qos-policy-config.png
```

Confirm that the policy references the intended class-map.

### Step 7: Check policy application

Inspect:

```text
configs/12. apply-qos-to-R1.png
```

Confirm that the QoS policy is associated with the intended R1 interface.

### Step 8: Check R2

Inspect:

```text
configs/13. R2-qos-config.png
```

Confirm the R2 QoS configuration matches the lab topology.

## 23. Packet Tracer Topology

The complete topology is provided as:

```text
topology/lab-qos.pkt
```

This is the primary file for reproducing the practical lab in Cisco Packet Tracer.

The topology diagram is provided separately:

```text
diagram/qos-network-topology.png
```

Use the `.pkt` file as the working lab and the diagram as the topology reference.

## 24. Configuration Evidence

The `configs` directory provides the configuration history in numbered stages:

|  # | File                                  | Configuration Stage       |
| -: | ------------------------------------- | ------------------------- |
|  1 | `1. R1-initial-config.png`            | R1 initial configuration  |
|  2 | `2. R1-static-route-config.png`       | R1 static routing         |
|  3 | `3. R2-initial-config.png`            | R2 initial configuration  |
|  4 | `4. R2-static-route-config.png`       | R2 static routing         |
|  5 | `5. SW1-config.png`                   | SW1 configuration         |
|  6 | `6. SW2-config.png`                   | SW2 configuration         |
|  7 | `7. PC1-config.png`                   | PC1 configuration         |
|  8 | `8. test-connectivity-before-qos.png` | Pre-QoS connectivity test |
|  9 | `9. R1-acl-config.png`                | R1 ACL                    |
| 10 | `10. R1-class-map-config.png`         | R1 class-map              |
| 11 | `11. R1-qos-policy-config.png`        | R1 QoS policy             |
| 12 | `12. apply-qos-to-R1.png`             | QoS policy applied to R1  |
| 13 | `13. R2-qos-config.png`               | R2 QoS configuration      |
|  — | `notes.png`                           | Additional lab notes      |

## 25. Lab Reproduction Order

Follow the repository's numbered sequence:

```text
1. Open lab-qos.pkt
2. Configure R1
3. Configure R1 static route
4. Configure R2
5. Configure R2 static route
6. Configure SW1
7. Configure SW2
8. Configure PC1
9. Verify connectivity
10. Configure R1 ACL
11. Configure R1 class-map
12. Configure R1 QoS policy
13. Apply QoS to R1
14. Configure QoS on R2
15. Verify the completed topology
```

The exact CLI syntax and addressing should be copied from the corresponding configuration screenshots.

## 26. Important Source Limitation

The repository stores the actual Cisco configurations primarily as PNG screenshots rather than text-based `.txt`, `.cfg`, or `.md` configuration files.

Therefore, this documentation intentionally does **not** invent or substitute Cisco commands, IP addresses, ACL entries, class-map statements, policy-map actions, interface names, bandwidth values, or verification output that cannot be read from the repository's machine-readable content.

The authoritative configuration references are:

```text
network-labs/lab-qos/configs/
```

and:

```text
network-labs/lab-qos/topology/lab-qos.pkt
```

This keeps the documentation aligned with the actual lab rather than replacing the repository configuration with a generic QoS example.

## 27. Lab Resources

* [QoS Lab directory](https://github.com/kumaradoss16/Networking/tree/main/network-labs/lab-qos)
* [Configuration screenshots](https://github.com/kumaradoss16/Networking/tree/main/network-labs/lab-qos/configs)
* [Topology diagram](https://github.com/kumaradoss16/Networking/blob/main/network-labs/lab-qos/diagram/qos-network-topology.png)
* [Packet Tracer topology](https://github.com/kumaradoss16/Networking/blob/main/network-labs/lab-qos/topology/lab-qos.pkt)

## 28. Lab Completion Checklist

```text
[ ] R1 initial configuration completed
[ ] R1 static route configured
[ ] R2 initial configuration completed
[ ] R2 static route configured
[ ] SW1 configured
[ ] SW2 configured
[ ] PC1 configured
[ ] Pre-QoS connectivity verified
[ ] R1 ACL configured
[ ] R1 class-map configured
[ ] R1 QoS policy configured
[ ] QoS policy applied to R1
[ ] R2 QoS configuration completed
[ ] Final connectivity verified
[ ] Configuration compared with repository screenshots
```

## 29. Lab Summary

The `lab-qos` exercise progresses from basic network configuration to QoS policy deployment:

```text
Basic Network Setup
        ↓
Static Routing
        ↓
Switch Configuration
        ↓
PC Configuration
        ↓
Connectivity Verification
        ↓
ACL
        ↓
Class-Map
        ↓
QoS Policy
        ↓
Policy Application
        ↓
R2 QoS Configuration
```

The lab's main practical focus is the configuration workflow represented by the ACL, class-map, QoS policy, and interface application stages, while the Packet Tracer topology provides the environment in which the configuration is tested. ([github.com][2])
