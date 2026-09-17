# Floating Static Routes Lab

A Cisco Packet Tracer lab demonstrating floating static routes for network redundancy between two LANs connected via a direct link and a backup transit path.

## Topology Overview

- **R1** - connects LAN 10.0.1.0/24 (SW1, PC1) to the network core
- **R2** - connects LAN 10.0.2.0/24 (SW2, SRV1) to the network core
- **Direct link** - R1 ↔ R2 via 10.0.0.0/30 (primary path)
- **Transit path** - R1 → SPR1 → SPR2 → R2 via the ISPA cloud (backup path)
- **ISPBR1 / ISPBR2** - optional external routers simulating internet uplinks

## What This Lab Covers

1. Initial device configuration (hostnames, interface IPs, `no shutdown`)
2. Primary static routes across the direct R1–R2 link
3. Floating static routes (higher administrative distance) as automatic backup via the transit path
4. Verification and failover testing
5. (Optional) Floating default routes for redundant internet access via ISPER1/ISPER2

## Key Concept: Administrative Distance (AD)

| Route Type | AD | Behavior |
|---|---|---|
| Primary static route | 1 (default) | Always preferred while valid |
| Floating static route | 10 (or higher) | Hidden in the routing table; activates automatically only if the primary route fails |

## Files in This Folder

- `initial-config/` - starting configs for all devices before any routing is added
- `floating-static-routes/` - final configs with primary + floating routes applied
- `topology.pkt` - Packet Tracer file for the lab

## Quick Test

```
show ip route static      ! confirm active route
! simulate failure:
interface <primary-link>
 shutdown
! confirm backup route takes over, then:
 no shutdown
```

## Notes

- Transit routers (SPR1, SPR2) run no dynamic routing protocol - they need explicit static routes to both LANs for the backup path to work end-to-end.
- IP addressing should be confirmed against the actual Packet Tracer file before applying commands, as labels in diagrams can be hard to read precisely.
