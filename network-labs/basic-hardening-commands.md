**Basic Hardening Commands – Purpose of Each**

These commands apply common security best practices on a Cisco router/switch (IOS). They reduce the chance of unauthorized access and make the device more resistant to casual attacks.

### `enable secret Cisc0EnablePa55`
- Sets the **privileged EXEC (enable) mode password** using a strong, one-way MD5 (or stronger) hash.
- Protects the highest privilege level. Anyone who wants to enter configuration mode or run privileged commands must know this password.
- Prefer `enable secret` over the older `enable password` (which is weakly encrypted or stored in clear text).

### `service password-encryption`
- Turns on **password encryption** for passwords that would otherwise be stored in clear text in the running/startup configuration.
- Encrypts console, VTY, and other line passwords with a weak reversible cipher (Type 7).  
- Does **not** affect the `enable secret` (which already uses a stronger hash).  
- Main benefit: prevents casual viewing of passwords when someone looks at the config.

### `no ip domain-lookup`
- Disables the router’s attempt to resolve unknown command words as DNS hostnames.
- Prevents the device from sending unnecessary DNS queries (and waiting for timeouts) when you mistype a command.
- Slightly improves security by reducing outbound traffic and potential DNS-based reconnaissance.

### Console Line Configuration
```cisco
line console 0
 password Cisc0ConsolePa55
 login
 logging synchronous
 exit
```
- **`line console 0`** – Enters configuration mode for the physical console port.
- **`password Cisc0ConsolePa55`** – Sets the console login password.
- **`login`** – Requires a password before granting access on the console.
- **`logging synchronous`** – Prevents console log messages from interrupting the command you are typing (makes the console cleaner and easier to use).
- **`exit`** – Returns to global configuration mode.

### VTY (Virtual Terminal) Lines Configuration
```cisco
line vty 0 4
 password Cisc0VtyPa55
 login
 transport input ssh telnet
 exit
```
- **`line vty 0 4`** – Configures the first five virtual terminal lines (used for remote management via Telnet/SSH).
- **`password Cisc0VtyPa55`** – Sets the login password for these lines.
- **`login`** – Requires authentication before granting remote access.
- **`transport input ssh telnet`** – Allows both SSH and Telnet as transport protocols.  
  - In modern hardening you would normally restrict this to **`transport input ssh`** only (Telnet sends credentials in clear text).
- **`exit`** – Leaves line configuration mode.

### Overall Effect
These commands together:
- Protect privileged mode with a strong secret.
- Encrypt most passwords in the configuration.
- Stop unwanted DNS lookups.
- Require passwords on both local console and remote (VTY) access.
- Allow remote management via SSH and Telnet (with the noted security caveat about Telnet).

**Security note:** The passwords shown (`Cisc0EnablePa55`, etc.) are examples only. In production always use long, unique, complex passwords and prefer SSH-only remote access with local user accounts or AAA.

---
**Local Console vs Remote (VTY) vs Enable Password**

These three protect different stages of access on a Cisco device.

### 1. Local Console Password
**Configured under:** `line console 0`

- Controls access when you connect **physically** with a console cable (serial/USB) to the device’s console port.
- This is **out-of-band** access — it does not go over the network.
- Once you enter the correct console password, you land in **user EXEC mode** (`Router>`).
- Useful for initial setup, recovery, or when the network is down.

**Example from earlier:**
```cisco
line console 0
 password Cisc0ConsolePa55
 login
```

### 2. Remote (VTY) Password
**Configured under:** `line vty 0 4` (or `0 15`)

- Controls **remote** access over the network using Telnet or SSH.
- This is **in-band** management.
- After successful authentication you also land in **user EXEC mode** (`Router>`).
- Without a VTY password (and `login`), remote access is usually blocked.

**Example from earlier:**
```cisco
line vty 0 4
 password Cisc0VtyPa55
 login
 transport input ssh telnet
```

### 3. Enable Password / Enable Secret
**Configured in global configuration mode**

- This is **not** an access method password.
- It protects the jump from **user EXEC mode** (`Router>`) to **privileged EXEC mode** (`Router#`).
- You need it **regardless** of how you connected (console or remote).
- Privileged mode is required to view the full configuration, enter configuration mode, and run most administrative commands.

| Command              | Strength          | Recommendation          |
|----------------------|-------------------|-------------------------|
| `enable password`    | Weak (Type 7 or clear text) | Avoid                 |
| `enable secret`      | Strong (MD5/SHA hash)     | Always use this       |

**Example:**
```cisco
enable secret Cisc0EnablePa55
```

### Quick Comparison

| Aspect                  | Console Password          | VTY (Remote) Password       | Enable Secret / Password      |
|-------------------------|---------------------------|-----------------------------|-------------------------------|
| **Where configured**    | `line console 0`          | `line vty 0 4`              | Global config                 |
| **Protects**            | Physical console access   | Remote Telnet/SSH access    | Privilege escalation          |
| **Access type**         | Local / Out-of-band       | Network / In-band           | Any connection method         |
| **Mode after success**  | User EXEC (`>`)           | User EXEC (`>`)             | Privileged EXEC (`#`)         |
| **Required for**        | Sitting in front of the device | Managing from another computer | Running `show run`, `configure terminal`, etc. |

### Typical Login Flow

1. Connect (console cable **or** SSH/Telnet) → enter console or VTY password → reach `Router>`
2. Type `enable` → enter the **enable secret** → reach `Router#`

**Best practice summary:**
- Always set a strong `enable secret`.
- Always protect both console and VTY lines with passwords (or better, local usernames + AAA).
- Prefer SSH only on VTY lines (`transport input ssh`) and disable Telnet.
