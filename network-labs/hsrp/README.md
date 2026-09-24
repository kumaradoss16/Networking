# HSRP Lab

## Overview

This lab demonstrates **Hot Standby Router Protocol (HSRP)** configuration using Cisco Packet Tracer.

HSRP provides **default gateway redundancy** by allowing multiple routers to share a virtual IP address. If the active router becomes unavailable, another router can take over the virtual gateway.

## Objectives

* Understand HSRP operation.
* Configure HSRP between two routers.
* Configure a virtual IP address.
* Configure HSRP priority.
* Configure the active and standby routers.
* Verify HSRP status and failover.
* Test network connectivity.

## Network Design

```text
                 LAN
                  |
          Virtual Gateway
             192.168.1.1
                  |
          +-------+-------+
          |               |
        R1              R2
      Active           Standby
   192.168.1.2       192.168.1.3
          \               /
           \             /
              Network
```

The hosts use the **HSRP virtual IP** as their default gateway instead of using the physical IP address of either router.

## HSRP Configuration

Example configuration on the primary router:

```cisco
interface gigabitEthernet 0/0
 ip address 192.168.1.2 255.255.255.0
 standby 1 ip 192.168.1.1
 standby 1 priority 110
 standby 1 preempt
```

Configuration on the secondary router:

```cisco
interface gigabitEthernet 0/0
 ip address 192.168.1.3 255.255.255.0
 standby 1 ip 192.168.1.1
 standby 1 priority 100
 standby 1 preempt
```

### Important Commands

```cisco
standby 1 ip 192.168.1.1
```

Creates the HSRP virtual IP address.

```cisco
standby 1 priority 110
```

Sets the router's HSRP priority.

The router with the higher priority normally becomes the **Active** router.

```cisco
standby 1 preempt
```

Allows a higher-priority router to take back the Active role when it becomes available again.

## Verification

Check HSRP status:

```cisco
show standby
```

or:

```cisco
show standby brief
```

Check interface configuration:

```cisco
show ip interface brief
```

Test the virtual gateway:

```cisco
ping 192.168.1.1
```

Test connectivity between hosts and other network devices:

```cisco
ping <destination-ip>
```

## Failover Test

1. Configure R1 as the Active router.
2. Configure R2 as the Standby router.
3. Verify HSRP status.
4. From a PC, ping the virtual gateway.
5. Shut down the active router interface.
6. Check HSRP status on R2.
7. R2 should become Active.
8. Test connectivity again.

Example:

```cisco
interface gigabitEthernet 0/0
 shutdown
```

Restore the interface with:

```cisco
no shutdown
```

## HSRP Roles

| Role       | Description                                           |
| ---------- | ----------------------------------------------------- |
| Active     | Processes traffic sent to the virtual gateway         |
| Standby    | Monitors the Active router and takes over if required |
| Virtual IP | Gateway address shared by the HSRP routers            |

## Verification Commands

```cisco
show standby
show standby brief
show ip interface brief
show running-config
ping <destination-ip>
```

## Learning Outcome

After completing this lab, you should be able to:

* Explain the purpose of HSRP.
* Configure an HSRP virtual gateway.
* Configure Active and Standby routers.
* Use HSRP priority to influence router selection.
* Configure preemption.
* Verify HSRP operation.
* Test gateway redundancy and failover.

## Requirements

* Cisco Packet Tracer
* Basic IPv4 networking knowledge
* Basic Cisco IOS commands
* Understanding of default gateways
* Basic routing knowledge

## Key Concept

HSRP allows hosts to use a **single virtual default gateway** while two or more routers provide redundancy behind that gateway.

```text
PC
 |
 | Default Gateway
 | 192.168.1.1
 |
 +----------------+
 |                |
 R1               R2
Active           Standby
```

If R1 fails, R2 can assume the virtual gateway role without requiring the hosts to change their configured default gateway.
