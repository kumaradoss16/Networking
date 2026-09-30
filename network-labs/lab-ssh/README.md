# SSH Lab Configuration

## Overview

This lab demonstrates the configuration and verification of Secure Shell (SSH) for remote management of Cisco network devices.

The lab uses Cisco Packet Tracer and includes routers, switches, and an end-user laptop. SSH is configured on the network devices to provide encrypted remote CLI access instead of using Telnet.

The configuration is built in multiple stages:

1. Initial device configuration
2. SSH configuration
3. VTY and access-control configuration
4. SSH connectivity testing

---

## Lab Objectives

- Configure basic management settings on Cisco devices
- Configure SSH for secure remote access
- Create a local username and password
- Configure a hostname and domain name
- Generate RSA cryptographic keys
- Enable SSH version 2
- Configure VTY lines for SSH access
- Restrict remote management access using an ACL
- Disable insecure Telnet access
- Test SSH connectivity from an end device
- Verify the SSH configuration and active sessions

---

## Technologies Used

| Technology | Purpose |
|---|---|
| SSH | Secure remote device management |
| TCP | Transport protocol used by SSH |
| RSA | Cryptographic key generation |
| VTY | Virtual terminal access |
| IPv4 | Management connectivity |
| Standard/Extended ACL | Restrict remote management sources |
| Cisco IOS | Device configuration |
| Cisco Packet Tracer | Network simulation |

### Default SSH Port

```text
TCP/22
````

SSH provides encrypted communication between the management client and the Cisco device.

---

## Lab Topology

The lab contains multiple Cisco devices and an end-user laptop used to establish and test SSH sessions.

```text
                    +-------------+
                    |     R1      |
                    | SSH Server  |
                    +-------------+
                           |
                           |
                    +-------------+
                    |     R2      |
                    | SSH Server  |
                    +-------------+
                           |
                           |
                    +-------------+
                    |     SW1     |
                    | SSH Server  |
                    +-------------+
                           |
                           |
                    +-------------+
                    |     SW2     |
                    | SSH Server  |
                    +-------------+
                           |
                           |
                    +-------------+
                    |    Laptop   |
                    | SSH Client  |
                    +-------------+
```

The exact physical and logical connections are available in:

```text
diagram/ssh-network-topology.png
```

The complete Packet Tracer implementation is available in:

```text
lab-ssh.pkt
```

---

# 1. Initial Device Configuration

Before configuring SSH, each device must have basic management connectivity.

The initial configuration screenshots are stored under:

```text
configs/
```

Initial configuration evidence includes:

```text
1.1 R1-initial-config.png
1.2 R2-initial-config.png
1.3 SW1-initial-config.png
1.4 SW1-initial-config.png
```

The initial configuration establishes the basic device state required before SSH configuration.

Typical requirements include:

* Hostname
* Management IP address
* Interface configuration
* Interface activation
* Basic connectivity
* Local management parameters

---

# 2. SSH Configuration

SSH requires several configuration parameters before remote access can be established.

The basic Cisco IOS SSH configuration process is:

```text
Configure hostname
        ↓
Configure domain name
        ↓
Create local user
        ↓
Generate RSA keys
        ↓
Enable SSH version 2
        ↓
Configure VTY lines
        ↓
Allow SSH transport
        ↓
Configure local authentication
        ↓
Test SSH connectivity
```

---

## 2.1 Configure Hostname

A hostname should be configured before generating the RSA keys.

Example:

```cisco
enable
configure terminal

hostname R1
```

The hostname identifies the device during remote administration.

---

## 2.2 Configure Domain Name

Configure an IP domain name:

```cisco
ip domain-name lab.local
```

The domain name is used together with the hostname when generating the RSA key pair.

For example:

```text
R1.lab.local
```

---

## 2.3 Create a Local User

Create a local administrative account:

```cisco
username admin privilege 15 secret <PASSWORD>
```

The `secret` keyword stores the password in a protected form in the Cisco configuration.

For a real production environment, use a strong unique password rather than a simple lab password.

---

## 2.4 Generate RSA Keys

Generate the RSA key pair:

```cisco
crypto key generate rsa modulus 2048
```

The RSA keys are required for SSH server operation.

A successful configuration should produce RSA key information similar to:

```text
The name for the keys will be:
R1.lab.local

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys...
```

---

## 2.5 Enable SSH Version 2

Configure SSH version 2:

```cisco
ip ssh version 2
```

SSH version 2 should be used for the lab instead of SSH version 1.

Verify the configuration:

```cisco
show ip ssh
```

Example:

```text
SSH Enabled - version 2.0
```

---

# 3. Configure VTY Lines

VTY lines provide remote terminal access to the Cisco device.

Enter VTY configuration mode:

```cisco
line vty 0 4
```

Configure local user authentication:

```cisco
login local
```

Restrict the VTY lines to SSH:

```cisco
transport input ssh
```

Complete example:

```cisco
line vty 0 4
 login local
 transport input ssh
```

This configuration ensures that the VTY lines use the local username database and accept SSH connections.

---

# 4. SSH Configuration on Network Devices

The repository contains SSH configuration evidence for the network devices.

Files include:

```text
2.1 R1-ssh-config.png
2.2 R2-ssh-config.png
2.3 SW1-ssh-config.png
2.3 SW2-ssh-config.png
```

These screenshots document the SSH configuration stage for the routers and switches in the lab.

The configuration should include the following logical components:

```text
Hostname
Domain name
Local user
RSA key pair
SSH version 2
VTY authentication
SSH-only transport
```

---

# 5. Configure Management Access Restrictions

SSH provides encrypted communication, but access should also be restricted to authorized management sources.

The lab includes ACL and VTY configuration evidence:

```text
3.1 R1-acl-&-vty-config.png
3.2 R2-acl-&-vty-config.png
3.3 SW1-acl-&-vty-config.png
3.4 SW2-acl-&-vty-config.png
```

The ACL can be applied to the VTY lines to control which source addresses are allowed to establish remote management sessions.

General configuration structure:

```cisco
access-list <NUMBER> permit <SOURCE>
```

Then apply the ACL to the VTY lines:

```cisco
line vty 0 4
 access-class <NUMBER> in
```

The actual ACL number and source address should match the addressing used in the Packet Tracer topology.

---

# 6. Why Restrict VTY Access?

Without an access restriction, any reachable host may attempt to connect to the SSH service.

An ACL provides an additional management-plane control:

```text
SSH Client
    |
    | TCP/22
    v
+----------------+
| VTY ACL        |
+----------------+
    |
    | Allowed source
    v
+----------------+
| SSH Service    |
+----------------+
```

The ACL should allow only trusted management networks or hosts.

---

# 7. Disable Telnet

Telnet sends authentication and session traffic without encryption.

SSH should be used instead.

Configure:

```cisco
line vty 0 4
 transport input ssh
```

Do not use:

```cisco
transport input telnet
```

If both protocols are explicitly allowed:

```cisco
transport input ssh telnet
```

Telnet remains available and should not be used for secure device management.

For SSH-only management:

```cisco
transport input ssh
```

---

# 8. Verify SSH Configuration

After configuration, verify the SSH server.

## Check SSH Status

```cisco
show ip ssh
```

Confirm:

```text
SSH Enabled
SSH version 2
```

---

## Check RSA Keys

```cisco
show crypto key mypubkey rsa
```

This verifies that the RSA key pair exists.

---

## Check Running Configuration

```cisco
show running-config
```

Look for:

```text
hostname
ip domain-name
username
crypto key
ip ssh version 2
line vty
login local
transport input ssh
access-class
```

---

## Check VTY Configuration

```cisco
show running-config | section line vty
```

Expected configuration should contain the SSH transport and local authentication settings.

---

# 9. Test Basic Connectivity

Before testing SSH, verify IP connectivity.

From the client device:

```text
ping <DEVICE-IP>
```

For example:

```text
ping <R1-management-IP>
```

A successful ping confirms that the client can reach the target device at Layer 3.

If ping fails, troubleshoot IP connectivity before troubleshooting SSH.

---

# 10. Test SSH Connectivity

From the Packet Tracer PC/Laptop command prompt:

```text
ssh -l admin <DEVICE-IP>
```

Example:

```text
ssh -l admin 192.168.1.1
```

The device should request the configured password.

After successful authentication, the user should receive the Cisco IOS CLI:

```text
R1>
```

If the account has privilege level 15, the session can enter privileged EXEC mode:

```text
R1#
```

---

# 11. Test SSH from the Laptop

The repository includes the following test evidence:

```text
4.1 test.png
4.2 test-laptop.png
```

These files document the final connectivity and SSH testing stage.

The test should verify:

```text
Laptop
   |
   | SSH TCP/22
   v
Network Device
   |
   | Authentication
   v
Cisco IOS CLI
```

A successful test confirms that:

* IP connectivity is working
* SSH is enabled
* TCP port 22 is reachable
* RSA keys are available
* SSH version 2 is enabled
* User authentication works
* VTY lines accept SSH
* VTY access restrictions permit the client

---

# 12. Useful Verification Commands

### SSH status

```cisco
show ip ssh
```

### Active SSH sessions

```cisco
show ssh
```

### Users

```cisco
show running-config | include username
```

### RSA keys

```cisco
show crypto key mypubkey rsa
```

### VTY configuration

```cisco
show running-config | section line vty
```

### ACL configuration

```cisco
show access-lists
```

### Interface status

```cisco
show ip interface brief
```

### Routing table

```cisco
show ip route
```

### Running configuration

```cisco
show running-config
```

---

# 13. Troubleshooting

## SSH Connection Refused

Check:

```cisco
show ip ssh
```

Verify that SSH is enabled.

Check:

```cisco
show running-config | section line vty
```

Verify:

```cisco
login local
transport input ssh
```

---

## RSA Keys Are Missing

Check:

```cisco
show crypto key mypubkey rsa
```

If no keys exist, configure:

```cisco
ip domain-name lab.local
crypto key generate rsa modulus 2048
```

---

## Authentication Fails

Verify the local account:

```cisco
show running-config | include username
```

Verify:

```cisco
line vty 0 4
 login local
```

Check the username and password used by the SSH client.

---

## SSH Works but Access Is Denied

Check the VTY ACL:

```cisco
show access-lists
```

Check the VTY configuration:

```cisco
show running-config | section line vty
```

Look for:

```cisco
access-class <ACL-NUMBER> in
```

The SSH client's source address must be permitted by the ACL.

---

## Ping Works but SSH Does Not

If ICMP works but SSH fails, check:

```cisco
show ip ssh
show running-config | section line vty
show access-lists
```

Possible causes include:

* SSH not enabled
* RSA keys missing
* Incorrect VTY configuration
* Incorrect authentication configuration
* ACL blocking the client
* SSH version mismatch
* Incorrect destination IP

---

# 14. Security Considerations

SSH should be used instead of Telnet for remote administration.

Recommended configuration principles:

* Use SSH version 2
* Use strong local passwords
* Use `secret` instead of plaintext passwords
* Restrict VTY access with an ACL
* Permit SSH only on required VTY lines
* Limit management access to trusted networks
* Use centralized AAA in larger environments
* Use TACACS+ or RADIUS where appropriate
* Keep management traffic separated from user traffic
* Disable unused management protocols

For production networks, local authentication should normally be supplemented or replaced by centralized AAA.

---

# 15. Lab Files

```text
lab-ssh/
├── configs/
│   ├── 1.1 R1-initial-config.png
│   ├── 1.2 R2-initial-config.png
│   ├── 1.3 SW1-initial-config.png
│   ├── 1.4 SW1-initial-config.png
│   ├── 2.1 R1-ssh-config.png
│   ├── 2.2 R2-ssh-config.png
│   ├── 2.3 SW1-ssh-config.png
│   ├── 2.3 SW2-ssh-config.png
│   ├── 3.1 R1-acl-&-vty-config.png
│   ├── 3.2 R2-acl-&-vty-config.png
│   ├── 3.3 SW1-acl-&-vty-config.png
│   ├── 3.4 SW2-acl-&-vty-config.png
│   ├── 4.1 test.png
│   └── 4.2 test-laptop.png
│
├── diagram/
│   └── ssh-network-topology.png
│
└── lab-ssh.pkt
```

---

# 16. Configuration Summary

The core SSH configuration on a Cisco IOS device follows this sequence:

```cisco
enable
configure terminal

hostname R1
ip domain-name lab.local

username admin privilege 15 secret <PASSWORD>

crypto key generate rsa modulus 2048

ip ssh version 2

line vty 0 4
 login local
 transport input ssh

end
write memory
```

If management-source restriction is required:

```cisco
access-list <NUMBER> permit <MANAGEMENT-SOURCE>

line vty 0 4
 access-class <NUMBER> in
```

Verify:

```cisco
show ip ssh
show ssh
show crypto key mypubkey rsa
show running-config | section line vty
show access-lists
```

---

# 17. Expected Result

At the end of the lab, the network devices should accept authenticated SSH connections from the permitted management host or network.

The final management path is:

```text
Management Laptop
       |
       | TCP/22
       v
   VTY ACL
       |
       v
   SSH Server
       |
       v
 Local User Authentication
       |
       v
   Cisco IOS CLI
```

The lab demonstrates the complete workflow for configuring secure remote CLI management on Cisco routers and switches using SSH.

```

### Repository-specific notes

The folder currently contains **one Packet Tracer `.pkt` file, one topology image, and 14 configuration/test screenshots**. The screenshots are organized into the four stages reflected above: initial configuration, SSH configuration, ACL/VTY configuration, and testing.

:contentReference[oaicite:0]{index=0}

One filename appears inconsistent: **`1.4 SW1-initial-config.png`** is listed alongside `1.3 SW1-initial-config.png`; if `1.4` is actually intended for **SW2**, I would rename it to `1.4 SW2-initial-config.png` to keep the documentation and evidence structure consistent.
```
