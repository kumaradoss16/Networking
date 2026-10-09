# DHCP Snooping Lab Configuration — Technical Documentation

> **Platform:** Cisco IOS / Cisco Packet Tracer  
> **Topic:** Layer 2 Network Security  
> **Document type:** Configuration Reference

## Reference repository

[Networking — lab-dhcp-snooping](https://github.com/kumaradoss16/Networking/tree/main/network-labs/lab-dhcp-snooping)

## 1. Lab overview

### Objective

Configure DHCP Snooping on Cisco switches to prevent unauthorized DHCP servers from assigning incorrect IP addresses, default gateways, or DNS server information to network clients.

DHCP Snooping examines DHCP messages passing through a switch and distinguishes between **trusted interfaces**, which are permitted to receive DHCP server responses, and **untrusted interfaces**, where unauthorized server responses are blocked.

### Learning outcomes

- Understand the DHCP Discover, Offer, Request, and Acknowledgment process.
- Configure global and VLAN-specific DHCP Snooping.
- Identify and configure trusted and untrusted interfaces.
- Explain DHCP Snooping rate limiting and Option 82.
- Verify DHCP Snooping operation and binding-table entries.
- Troubleshoot clients that fail to obtain an IP address.

## 2. Prerequisites and lab information

| Requirement | Description |
|---|---|
| Simulation software | Cisco Packet Tracer or compatible Cisco IOS environment |
| Devices | The router, switches, servers, and PCs present in the original lab |
| Existing configuration | VLANs, switchports, trunks, and DHCP service as required by the topology |
| Access | Privileged EXEC and configuration mode |
| Important restriction | Do not change the original IP addressing or topology without checking the lab files |

The exact VLAN numbers, interface names, IP addresses, device names, and DHCP server location must be taken from the repository's lab configuration.

## 3. Understand how DHCP Snooping works

DHCP Snooping operates at Layer 2 and filters DHCP messages based on the interface through which they arrive.

The normal DHCP allocation process is:

1. **DHCP Discover:** The client broadcasts a request to find a DHCP server.
2. **DHCP Offer:** The legitimate server offers an IP address and configuration.
3. **DHCP Request:** The client requests the offered address.
4. **DHCP ACK:** The server confirms the lease and the client configures its network settings.

With DHCP Snooping enabled:

- Client DHCP requests can enter through untrusted access ports.
- DHCP server messages, such as Offer and ACK, are accepted only when permitted by the snooping trust policy.
- DHCP server responses arriving on an untrusted port are discarded.
- Valid DHCP exchanges can create entries in the DHCP Snooping binding table.

**Important:** A trusted interface is not necessarily an interface that is physically connected to a server. It is an interface deliberately configured to accept DHCP server messages. Trust should be assigned according to the actual topology and DHCP message path.

## 4. Configuration procedure

The following is a standard Cisco IOS configuration template, not a verified transcription of the repository's device configurations.

### Step 1 — Inspect the existing switch configuration

Run these commands on each relevant switch before making changes.

```cisco
enable
show running-config
show vlan brief
show interfaces status
show interfaces trunk
show ip dhcp snooping
```

| Command | Purpose and working |
|---|---|
| `enable` | Enters privileged EXEC mode, allowing administrative and verification commands. |
| `show running-config` | Displays the active configuration, including VLANs, interfaces, and existing security settings. |
| `show vlan brief` | Shows VLAN IDs, names, and access-port membership. |
| `show interfaces status` | Shows port status, VLAN assignment, and interface connectivity information. |
| `show interfaces trunk` | Identifies operational trunk interfaces and the VLANs carried across them. |
| `show ip dhcp snooping` | Displays DHCP Snooping status and applicable trust or VLAN settings, when supported. |

**Why this step matters:** If the wrong uplink is trusted, legitimate DHCP responses may be blocked. If a client-facing interface is trusted, a rogue DHCP server connected there may bypass the intended protection.

### Step 2 — Configure DHCP service

If the original lab uses a Cisco router as its DHCP server, the following illustrates a common configuration pattern. Use it only if it matches the existing topology and addressing plan.

```cisco
enable
configure terminal

interface <ROUTER-LAN-INTERFACE>
 ip address <GATEWAY-IP> <SUBNET-MASK>
 no shutdown
exit

ip dhcp excluded-address <EXCLUDED-START-IP> <EXCLUDED-END-IP>

ip dhcp pool <POOL-NAME>
 network <NETWORK-ADDRESS> <SUBNET-MASK>
 default-router <GATEWAY-IP>
 dns-server <DNS-IP>
exit

end
```

| Command | Purpose and working |
|---|---|
| `configure terminal` | Enters global configuration mode. |
| `interface ...` | Selects the router interface connected to the LAN. |
| `ip address ...` | Assigns the router's LAN address and subnet mask. |
| `no shutdown` | Administratively enables the interface. |
| `ip dhcp excluded-address ...` | Prevents specified addresses from being dynamically leased. |
| `ip dhcp pool ...` | Creates or selects a DHCP pool. |
| `network ...` | Defines the subnet from which the pool allocates addresses. |
| `default-router ...` | Advertises the default gateway to DHCP clients. |
| `dns-server ...` | Advertises the DNS resolver address to clients. |
| `end` | Returns to privileged EXEC mode. |

Verify the DHCP service using:

```cisco
show ip dhcp pool
show ip dhcp binding
show ip interface brief
```

If the lab uses a dedicated server in Packet Tracer, configure its DHCP service through the server's interface instead of applying router DHCP-pool commands.

### Step 3 — Enable DHCP Snooping globally

On each switch that must inspect DHCP traffic:

```cisco
enable
configure terminal
ip dhcp snooping
```

**Command purpose:** `ip dhcp snooping` enables the DHCP Snooping feature globally on the switch.

**How it works:** The switch can now apply DHCP Snooping policies to VLANs for which the feature is enabled. Enabling it globally alone does not activate inspection for every VLAN.

### Step 4 — Enable DHCP Snooping on the required VLAN

```cisco
ip dhcp snooping vlan <VLAN-ID>
```

Replace `<VLAN-ID>` with the VLAN used by the original lab.

**Command purpose:** Activates DHCP Snooping for the specified VLAN.

**How it works:** The switch applies DHCP Snooping inspection to the DHCP traffic associated with that VLAN.

For multiple VLANs, IOS platforms may support a comma-separated list or a range, depending on the command syntax and software version.

### Step 5 — Configure the legitimate DHCP path as trusted

Identify the interface through which legitimate DHCP server responses enter the switch.

```cisco
interface <UPLINK-INTERFACE>
 ip dhcp snooping trust
exit
```

**Command purpose:** Marks the selected interface as trusted for DHCP Snooping.

**How it works:** The switch permits DHCP server messages to arrive on this interface without applying the untrusted-port server-message restriction.

The correct interface depends on where the DHCP server is connected:

- If the DHCP server is connected directly to the switch, the server-facing interface may need to be trusted.
- If the DHCP server is behind a router or upstream switch, the relevant interface toward that legitimate DHCP path may need to be trusted.
- On downstream switches, the uplink carrying legitimate DHCP responses may need to be trusted as well.

Do not blindly trust every trunk or uplink. A trunk can also carry traffic from untrusted access networks.

### Step 6 — Keep client-facing ports untrusted

Client-facing interfaces should remain untrusted by default.

```cisco
interface <CLIENT-ACCESS-INTERFACE>
 ! Leave DHCP Snooping trust disabled
exit
```

The comment above is explanatory, not a command. Do not enter it as configuration.

**Command purpose:** Preserves the default untrusted status of the client-facing interface.

**How it works:** A DHCP Offer or other server response arriving from an unauthorized server on this port is dropped by DHCP Snooping. Normal client-originated DHCP messages are permitted subject to the other snooping rules.

If the port was previously trusted, explicitly remove that trust:

```cisco
interface <CLIENT-ACCESS-INTERFACE>
 no ip dhcp snooping trust
exit
```

This is particularly important when converting an existing configuration to a secure design.

### Step 7 — Optional: Configure DHCP rate limiting

On supported switches, a per-interface DHCP packet rate limit can reduce DHCP flooding from untrusted ports.

```cisco
interface <CLIENT-ACCESS-INTERFACE>
 ip dhcp snooping limit rate <PACKETS-PER-SECOND>
exit
```

| Element | Purpose |
|---|---|
| `ip dhcp snooping limit rate` | Limits the permitted DHCP packet rate on the interface. |
| `<PACKETS-PER-SECOND>` | Replace with a justified threshold based on the platform and network requirements. |

**Operational warning:** Depending on the platform, exceeding the configured threshold can trigger violation handling, including shutting down the interface. Confirm the device's behavior before enabling this feature on production ports.

### Step 8 — Save the configuration

```cisco
end
copy running-config startup-config
```

- `end` returns to privileged EXEC mode.
- `copy running-config startup-config` saves the active configuration so that it persists after a restart.

Save after validating the configuration, not before checking for incorrect trusted interfaces or VLAN assignments.

## 5. DHCP Snooping command reference

| Command | Purpose |
|---|---|
| `ip dhcp snooping` | Enables DHCP Snooping globally. |
| `ip dhcp snooping vlan <VLAN-ID>` | Enables inspection for the specified VLAN. |
| `ip dhcp snooping trust` | Marks an interface as trusted. |
| `no ip dhcp snooping trust` | Removes trust from an interface. |
| `ip dhcp snooping limit rate <RATE>` | Limits DHCP packet rate on a supported interface. |
| `ip dhcp snooping information option` | Enables insertion of DHCP Option 82 information, where supported and applicable. |
| `no ip dhcp snooping information option` | Disables Option 82 insertion. |
| `show ip dhcp snooping` | Displays the operational configuration and status. |
| `show ip dhcp snooping binding` | Displays learned client bindings. |
| `show running-config` | Displays the active running configuration. |

### Understanding DHCP Option 82

Option 82, also known as the DHCP Relay Agent Information Option, can carry information about the relay or network access point through which a DHCP request arrived. It can help a DHCP server apply policies based on where a client is connected.

Option 82 insertion is not required for the basic rogue DHCP server protection demonstrated by DHCP Snooping. Support and behavior vary by platform, server, and topology. Do not enable or disable it without considering the original lab's intended configuration.

## 6. Verification and expected behavior

Run the following on the relevant switches after configuration.

```cisco
show ip dhcp snooping
show ip dhcp snooping binding
show vlan brief
show interfaces trunk
show running-config
```

| Verification | Expected observation |
|---|---|
| DHCP Snooping status | The feature is enabled globally and on the intended VLANs. |
| Trusted interfaces | Only interfaces required to receive legitimate DHCP server messages are trusted. |
| Client ports | Client-facing ports are untrusted. |
| DHCP binding table | Entries appear when clients complete DHCP exchanges and the platform learns the bindings. |
| VLAN membership | Client interfaces belong to the correct VLAN. |
| Trunk configuration | Required VLANs are carried across relevant trunk links. |
| Client IP configuration | Clients receive addresses, subnet masks, gateways, and DNS settings consistent with the DHCP scope. |

The exact output varies by switch model and IOS version. An empty binding table immediately after configuration does not necessarily mean the feature is broken: clients may not yet have completed a DHCP exchange.

### Test the protection

1. Configure DHCP Snooping on the relevant VLANs and switches.
2. Verify that the legitimate DHCP path is trusted and client ports are untrusted.
3. Renew the client IP address using the DHCP controls available in Packet Tracer.
4. Confirm that the client receives valid addressing from the legitimate DHCP service.
5. Connect a test rogue DHCP server to an untrusted access port in an isolated lab.
6. Renew the client address and observe the DHCP exchange.
7. Verify that rogue server responses arriving on the untrusted port are blocked.

A successful test should show that legitimate DHCP allocation continues while unauthorized DHCP server responses are filtered.

## 7. Troubleshooting guide

| Problem | What to inspect | Corrective action |
|---|---|---|
| Client receives no IP address | DHCP Snooping VLAN, server reachability, VLAN membership | Correct the VLAN or DHCP path; check trusted interfaces. |
| Client receives an incorrect gateway | DHCP pool or server scope | Correct the gateway option on the legitimate DHCP server. |
| Legitimate DHCP Offer is dropped | Trust configuration along the server-to-client path | Trust only the appropriate interface or interfaces. |
| Rogue DHCP server can assign addresses | Snooping status and VLAN coverage | Enable snooping on the correct VLAN and ensure the rogue-facing port is untrusted. |
| Binding table remains empty | Whether a DHCP lease has completed | Renew the client lease and inspect DHCP traffic. |
| DHCP stops after rate limiting | Rate threshold and violation behavior | Review the configured threshold and platform-specific violation handling. |
| DHCP fails across switches | VLAN trunks and trust on each switch | Trace the DHCP Offer path hop by hop. |

For diagnosis, work from the client toward the DHCP server. Confirm VLAN membership first, then trace the Discover and Offer messages across each switch. This makes it easier to distinguish an addressing problem from a DHCP Snooping trust problem.

## 8. Security limitations and production considerations

DHCP Snooping is an important Layer 2 control, but it is not a complete network security solution.

- **Dynamic ARP Inspection (DAI)** can use DHCP Snooping bindings to validate ARP traffic.
- **IP Source Guard** can use learned bindings to restrict IP traffic on supported interfaces.
- Unused switch ports should be disabled or assigned to an appropriately isolated VLAN.
- Trust settings should follow the actual topology and be reviewed after network changes.
- Rate limits should be tested against legitimate DHCP traffic.
- Binding persistence and recovery behavior should be checked for the specific platform.

Do not assume that enabling DHCP Snooping automatically enables DAI, IP Source Guard, or comprehensive protection against every DHCP-related attack.

## 9. Configuration completion checklist

### Preparation

- [ ] Inspect original VLANs, interfaces, trunks, and addressing.
- [ ] Verify the legitimate DHCP service and address pool.

### Configuration

- [ ] Enable DHCP Snooping globally on the required switches.
- [ ] Enable DHCP Snooping on the intended VLANs.
- [ ] Trust only the legitimate DHCP response path.
- [ ] Keep client-facing ports untrusted.

### Validation

- [ ] Verify snooping status and learned bindings.
- [ ] Test legitimate DHCP allocation and rogue DHCP blocking.
- [ ] Save and review the final configuration.

## 10. Source accuracy and final step

The configuration above documents standard Cisco IOS DHCP Snooping behavior. It is **not yet an exact reference implementation of the GitHub lab**, because the files in the specified directory could not be read when this document was prepared.

To make the documentation match the lab precisely, provide the lab's configuration files or paste the README and device configuration files. The final version can then include:

- The exact topology and addressing table.
- Initial configurations for each device in the original order.
- Every original command, explained line by line.
- The actual DHCP Snooping configuration for each switch.
- Expected verification outputs and lab-specific troubleshooting.
- A ready-to-commit Markdown document that fits the repository's directory structure.

That is the safest way to ensure the documentation preserves the actual configuration rather than substituting a different DHCP Snooping lab.
