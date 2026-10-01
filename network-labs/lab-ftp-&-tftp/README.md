# FTP and TFTP Lab Configuration

## Overview

This lab demonstrates how to configure and verify **FTP (File Transfer Protocol)** and **TFTP (Trivial File Transfer Protocol)** in a Cisco Packet Tracer network.

The lab covers:

* FTP server configuration
* FTP client connectivity
* TFTP client configuration
* TFTP file transfer
* Router configuration backup using TFTP
* Router configuration restoration using TFTP
* IOS image transfer using TFTP
* FTP file transfer from a router

---

## Lab Objectives

By completing this lab, you will learn how to:

1. Configure basic router connectivity.
2. Configure a server for FTP and TFTP services.
3. Configure router IP addresses.
4. Test network connectivity.
5. Transfer router configuration files using TFTP.
6. Transfer an IOS image using TFTP.
7. Access an FTP server from a Cisco router.
8. Understand the difference between FTP and TFTP.

---

## FTP vs TFTP

| Feature        | FTP                              | TFTP                                            |
| -------------- | -------------------------------- | ----------------------------------------------- |
| Full Name      | File Transfer Protocol           | Trivial File Transfer Protocol                  |
| Transport      | TCP                              | UDP                                             |
| Default Port   | TCP 21                           | UDP 69                                          |
| Authentication | Username/password supported      | No authentication                               |
| Reliability    | TCP provides reliable delivery   | UDP provides no connection-oriented reliability |
| Use Case       | General file transfer            | Network device configuration/image transfer     |
| Cisco Usage    | File transfer to/from FTP server | Configuration and IOS image backup/restore      |

### FTP

FTP is commonly used when authentication and reliable file transfer are required.

### TFTP

TFTP is lightweight and is commonly used by network engineers for:

* Router configuration backup
* Router configuration restoration
* IOS image backup
* IOS image upgrades

---

# 1. Lab Topology

The lab uses Cisco Packet Tracer with routers and server-based FTP/TFTP services.

Example logical topology:

```text
          +----------+
          |   R1     |
          +----------+
               |
               |
          +----------+
          |   R2     |
          +----------+
               |
               |
        +---------------+
        |     SRV1      |
        | FTP / TFTP    |
        +---------------+
```

The exact topology and addressing can be viewed in the Packet Tracer file and topology diagram included in this directory.

---

# 2. Basic Router Configuration

Before testing FTP or TFTP, routers must have working IP connectivity.

## Enter privileged EXEC mode

```text
enable
```

### Purpose

Moves from user EXEC mode to privileged EXEC mode.

---

## Enter global configuration mode

```text
configure terminal
```

### Purpose

Enters global configuration mode where router configuration can be changed.

---

## Configure an interface

```text
interface gigabitEthernet 0/0
```

### Purpose

Selects the GigabitEthernet interface that will be configured.

---

## Assign an IP address

```text
ip address <IP_ADDRESS> <SUBNET_MASK>
```

Example:

```text
ip address 192.168.10.1 255.255.255.0
```

### Purpose

Assigns an IPv4 address and subnet mask to the interface.

---

## Enable the interface

```text
no shutdown
```

### Purpose

Activates the interface.

Cisco router interfaces are administratively shutdown by default in many configurations, so `no shutdown` is required to bring the interface up.

---

## Exit interface configuration

```text
exit
```

### Purpose

Returns to the previous configuration mode.

---

# 3. Verify Interface Configuration

Use:

```text
show ip interface brief
```

### Purpose

Displays a summary of router interfaces.

Important fields:

```text
Interface
IP-Address
Status
Protocol
```

You generally want to see:

```text
Status    = up
Protocol  = up
```

This indicates that the interface is operational and the Layer 2 protocol is functioning.

---

# 4. Test Connectivity

Use:

```text
ping <SERVER_IP>
```

Example:

```text
ping 192.168.10.10
```

### Purpose

Tests IP connectivity between the router and the server.

A successful ping confirms basic Layer 3 connectivity.

---

# 5. TFTP Server Configuration

In Cisco Packet Tracer:

```text
Server → Services → TFTP
```

Enable the TFTP service.

The server becomes available as a TFTP server.

### TFTP uses

TFTP is commonly used for:

* Configuration backup
* Configuration restoration
* IOS image transfer

TFTP does not provide the authentication features of FTP.

---

# 6. Test TFTP Connectivity

From the router:

```text
ping <TFTP_SERVER_IP>
```

Example:

```text
ping 192.168.10.10
```

### Purpose

Confirms that the router can reach the TFTP server before attempting file transfers.

---

# 7. Backup Router Configuration to TFTP

Use:

```text
copy running-config tftp:
```

The router will ask for the TFTP server address.

Example:

```text
Address or name of remote host []? 192.168.10.10
```

Then specify the destination filename.

Example:

```text
Destination filename [r1-confg]? R1-running-config
```

### Purpose

Copies the router's current running configuration to the TFTP server.

### Flow

```text
Router R1
   |
   | running-config
   |
   v
TFTP Server
   |
   └── R1-running-config
```

This is useful for configuration backup.

---

# 8. Verify the TFTP Backup

On the server:

```text
Services → TFTP
```

Check the available files.

The backup configuration file should appear in the TFTP file list.

---

# 9. Backup Startup Configuration

The startup configuration can also be copied to a TFTP server.

```text
copy startup-config tftp:
```

### Purpose

Copies the configuration stored in NVRAM to the TFTP server.

### Difference

```text
running-config
    ↓
Current configuration in RAM

startup-config
    ↓
Saved configuration used during boot
```

---

# 10. Restore Configuration from TFTP

Use:

```text
copy tftp: running-config
```

The router asks for:

```text
Address or name of remote host []?
```

Enter the TFTP server address.

Then specify the configuration filename.

### Purpose

Downloads a configuration file from the TFTP server and merges it into the running configuration.

---

# 11. Restore Startup Configuration

A configuration file can also be copied to NVRAM:

```text
copy tftp: startup-config
```

### Purpose

Downloads the configuration from the TFTP server and saves it as the router's startup configuration.

The configuration will then be used after a reload.

---

# 12. Verify Configuration

Use:

```text
show running-config
```

### Purpose

Displays the active configuration currently running in RAM.

Use:

```text
show startup-config
```

### Purpose

Displays the configuration saved in NVRAM.

---

# 13. TFTP IOS Image Transfer

TFTP can also be used to transfer a Cisco IOS image.

Use:

```text
copy flash: tftp:
```

The router will ask for:

```text
Source filename?
```

Specify the IOS image stored in flash.

Then provide:

```text
Address or name of remote host?
```

Enter the TFTP server IP address.

### Purpose

Copies an IOS image from the router's flash memory to the TFTP server.

### Flow

```text
Router Flash
     |
     | IOS Image
     v
TFTP Server
```

This is useful for creating an IOS image backup.

---

# 14. Verify Flash Contents

Use:

```text
show flash:
```

### Purpose

Displays files stored in the router's flash memory.

Look for the IOS image filename.

Example:

```text
c1900-universalk9-mz.xxxxx.bin
```

The exact filename depends on the router and IOS image used in the lab.

---

# 15. Copy IOS Image from TFTP to Router

The reverse operation can be performed with:

```text
copy tftp: flash:
```

### Purpose

Downloads an IOS image from the TFTP server into the router's flash memory.

### Flow

```text
TFTP Server
     |
     | IOS Image
     v
Router Flash
```

This is commonly used when preparing a router for an IOS upgrade.

---

# 16. FTP Server Configuration

In Packet Tracer:

```text
Server → Services → FTP
```

Enable the FTP service.

Create an FTP user with:

```text
Username
Password
Permissions
```

The available permissions determine whether the user can perform operations such as reading, writing, deleting, or renaming files.

---

# 17. Test FTP from Router

From the router:

```text
ftp <FTP_SERVER_IP>
```

Example:

```text
ftp 192.168.10.10
```

The router requests the FTP username and password.

Example:

```text
Username: admin
Password: ********
```

### Purpose

Establishes an FTP session between the router and FTP server.

---

# 18. FTP File Transfer

After connecting to the FTP server, files can be transferred using the Cisco file-copy mechanism.

For example:

```text
copy running-config ftp:
```

The router requests:

```text
Address or name of remote host []?
```

Enter the FTP server IP address.

Then provide the FTP username and password when prompted.

### Purpose

Copies the router's running configuration to an FTP server.

---

# 19. FTP IOS Image Backup

Use:

```text
copy flash: ftp:
```

### Purpose

Copies a file from router flash memory to an FTP server.

This can be used to back up an IOS image.

---

# 20. Important Verification Commands

### Display interfaces

```text
show ip interface brief
```

Purpose:

```text
Verify interface IP addresses and status.
```

---

### Display running configuration

```text
show running-config
```

Purpose:

```text
View the active router configuration.
```

---

### Display startup configuration

```text
show startup-config
```

Purpose:

```text
View the saved configuration in NVRAM.
```

---

### Display flash contents

```text
show flash:
```

Purpose:

```text
View files and IOS images stored in flash.
```

---

### Test connectivity

```text
ping <IP_ADDRESS>
```

Purpose:

```text
Verify Layer 3 connectivity.
```

---

# 21. Command Summary

| Command                     | Purpose                                 |
| --------------------------- | --------------------------------------- |
| `enable`                    | Enter privileged EXEC mode              |
| `configure terminal`        | Enter global configuration mode         |
| `interface g0/0`            | Select an interface                     |
| `ip address`                | Assign an IPv4 address                  |
| `no shutdown`               | Enable an interface                     |
| `show ip interface brief`   | Check interface status and IP addresses |
| `ping`                      | Test IP connectivity                    |
| `show running-config`       | Display active configuration            |
| `show startup-config`       | Display saved configuration             |
| `show flash:`               | Display files in flash                  |
| `copy running-config tftp:` | Backup running configuration to TFTP    |
| `copy startup-config tftp:` | Backup startup configuration to TFTP    |
| `copy tftp: running-config` | Restore/merge configuration from TFTP   |
| `copy tftp: startup-config` | Restore configuration to startup-config |
| `copy flash: tftp:`         | Copy a flash file to TFTP               |
| `copy tftp: flash:`         | Copy a file from TFTP to flash          |
| `ftp <server-ip>`           | Start an FTP session                    |
| `copy running-config ftp:`  | Copy running configuration to FTP       |
| `copy flash: ftp:`          | Copy flash files to FTP                 |

---

# 22. Verification Checklist

After completing the lab, verify:

* [ ] Router interfaces have correct IP addresses.
* [ ] Interfaces are `up/up`.
* [ ] Router can ping the server.
* [ ] TFTP service is enabled.
* [ ] FTP service is enabled.
* [ ] FTP user is configured.
* [ ] Running configuration can be backed up.
* [ ] Startup configuration can be backed up.
* [ ] Configuration can be restored from TFTP.
* [ ] IOS image can be copied to TFTP.
* [ ] FTP connection works from the router.
* [ ] Files are visible on the server.

---

## Key Takeaways

**FTP** provides authenticated file transfer using TCP and is suitable for general file-transfer operations.

**TFTP** is a lightweight UDP-based file-transfer protocol commonly used by network devices for configuration and IOS image transfers.

For Cisco network administration, the most important practical commands from this lab are:

```text
show ip interface brief
ping <server-ip>
show running-config
show startup-config
show flash:
copy running-config tftp:
copy startup-config tftp:
copy tftp: running-config
copy tftp: startup-config
copy flash: tftp:
copy tftp: flash:
ftp <server-ip>
copy running-config ftp:
copy flash: ftp:
```

This lab provides practical experience with **network-device file transfer, configuration backup/restore, and IOS image management** using FTP and TFTP.
