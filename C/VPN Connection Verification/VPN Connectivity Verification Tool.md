<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# VPN Connectivity Verification Tool

> **Advanced cross-platform VPN connection validator written in C**

[
[
[

***

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Code Structure](#code-structure)
- [Platform-Specific Notes](#platform-specific-notes)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

***

## 🎯 Overview

**VPN Connectivity Verification Tool** is a lightweight, cross-platform command-line utility that validates whether your VPN connection is active and properly routing traffic. It performs comprehensive checks before and after VPN activation to ensure your privacy and security.

### Why This Tool?

- 🔒 **Security Verification:** Confirms that your traffic is actually routed through the VPN
- 🌐 **DNS Leak Detection:** Identifies if DNS queries bypass the VPN tunnel
- 🖥️ **Adapter Detection:** Scans for VPN network adapters across platforms
- 📊 **Before/After Comparison:** Shows clear differences when VPN connects
- ⚡ **Zero Dependencies:** Pure C with standard libraries only

***

## ✨ Features

### Core Functionality

✅ **Public IP Address Detection**

- Fetches your current public IP before and after VPN connection
- Uses `ifconfig.me` API via curl

✅ **DNS Server Analysis**

- Extracts active DNS servers from system configuration
- Compares DNS settings pre/post VPN connection

✅ **VPN Adapter Detection**

- Scans network interfaces for VPN-related adapters
- Supports 25+ VPN providers and protocols including:
    - OpenVPN, WireGuard, Cisco AnyConnect
    - NordVPN, ExpressVPN, ProtonVPN, Surfshark
    - L2TP, PPTP, IPSec, SoftEther

✅ **Comprehensive Verification Summary**

- Clear status indicators (ACTIVE / LIKELY ACTIVE / PARTIAL / NOT ACTIVE)
- Side-by-side comparison of network settings
- Security recommendations and leak test links

✅ **Cross-Platform Support**

- **Windows:** ipconfig, netsh
- **Linux:** resolv.conf, ip addr
- **macOS:** resolv.conf, ifconfig

***

## 🔍 How It Works

### Workflow

```
1. Check Public IP (Before VPN)
          ↓
2. Check DNS Servers (Before VPN)
          ↓
3. Scan Network Adapters (Before VPN)
          ↓
4. [USER CONNECTS TO VPN]
          ↓
5. Check Public IP (After VPN)
          ↓
6. Check DNS Servers (After VPN)
          ↓
7. Scan Network Adapters (After VPN)
          ↓
8. Compare Results & Display Verdict
```


### Detection Logic

| Condition | IP Changed | VPN Adapter Found | Status |
| :-- | :-- | :-- | :-- |
| Best Case | ✅ YES | ✅ YES | **ACTIVE** |
| Likely OK | ✅ YES | ❌ NO | **LIKELY ACTIVE** |
| Suspicious | ❌ NO | ✅ YES | **PARTIAL** |
| Not Working | ❌ NO | ❌ NO | **NOT ACTIVE** |


***

## 📦 Prerequisites

### System Requirements

- **Operating System:** Windows 10+, Linux (any distro), macOS 10.12+
- **Compiler:** GCC, Clang, or MSVC
- **Dependencies:**
    - `curl` (must be installed and in PATH)
    - Standard C library


### Installing curl

**Windows:**

```powershell
# Windows 10/11 includes curl by default
# Verify:
curl --version
```

**Linux:**

```bash
# Debian/Ubuntu
sudo apt-get install curl

# RHEL/CentOS
sudo yum install curl

# Arch
sudo pacman -S curl
```

**macOS:**

```bash
# Included by default
# If missing:
brew install curl
```


***

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/vpn-checker.git
cd vpn-checker
```


### Compile

**Linux/macOS:**

```bash
gcc -o vpn_checker main.c -Wall -Wextra
```

**Windows (MinGW):**

```bash
gcc -o vpn_checker.exe main.c
```

**Windows (MSVC):**

```bash
cl main.c /Fe:vpn_checker.exe
```


***

## 💻 Usage

### Basic Execution

```bash
# Linux/macOS
./vpn_checker

# Windows
vpn_checker.exe
```


### Sample Output

```
=================================================================
             Advanced VPN Connectivity Verification Tool
=================================================================
Operating System: Linux
=================================================================

[Step 1] Checking current public IP address...
Public IP before VPN: 203.0.113.45

[Step 2] Checking current DNS Servers...
DNS Servers (Before VPN): 
   nameserver 8.8.8.8
   nameserver 8.8.4.4

[Step 3] Scanning for VPN network adapters...
No VPN adapters detected (before VPN).

=================================================================

>>> NOW CONNECT TO YOUR VPN <<<
>>> Press ENTER when connected <<<

[Step 4] Checking current public IP address...
Public IP after VPN: 185.220.102.8

[Step 5] Checking current DNS Servers...
DNS Servers (After VPN): 
   nameserver 10.8.0.1

[Step 6] Scanning for VPN network adapters...
VPN Adapters Found (After VPN): 
   tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP>

=================================================================
                    Verification Summary
=================================================================

IP Address (Before):           203.0.113.45
IP Address (After):            185.220.102.8
IP Changed:                    YES
DNS Changed:                   YES
VPN Adapter Detected:          YES

=================================================================

*****************************************************************
                     VPN STATUS: ACTIVE
      Your connection is successfully routed through VPN!
*****************************************************************

[SECURITY NOTE] For complete security verification:
  1. Check DNS leaks: https://dnsleaktest.com
  2. Check WebRTC leaks: https://browserleaks.com/webrtc
  3. Verify IPv6 is disabled or routed through VPN
=================================================================
```


***

## 🔧 Technical Details

### Function Reference

| Function | Purpose | Parameters | Returns |
| :-- | :-- | :-- | :-- |
| `fetch_public_ip()` | Retrieves public IP via curl | `char *ip_buffer` | 0 on success, 1 on error |
| `fetch_dns_servers()` | Extracts DNS servers | `char *dns_buffer` | 0 on success, 1 on error |
| `detect_vpn_adapter()` | Scans for VPN interfaces | `char *adapter_buffer` | 0 if found, 1 if not |
| `check_vpn_keywords_windows()` | Windows adapter filter | `const char *line` | 1 if VPN keyword found |
| `check_vpn_keywords_unix()` | Unix/Linux adapter filter | `const char *line` | 1 if VPN keyword found |
| `print_separator()` | Prints decorative line | `char c, int length` | void |
| `safe_copy()` | Secure string copy | `char *dest, const char *src, size_t size` | void |


***

## 📂 Code Structure

```c
main.c
├── Platform Detection Macros
│   ├── OS_WINDOWS
│   ├── OS_LINUX
│   └── OS_UNKNOWN
│
├── Constants
│   ├── MAX_BUFFER (2048)
│   ├── IP_SIZE (100)
│   └── DNS_SIZE (1024)
│
├── Function Prototypes
│
├── main()
│   ├── Variable Initialization
│   ├── Pre-VPN Checks
│   ├── User Prompt (Connect VPN)
│   ├── Post-VPN Checks
│   ├── Comparison Logic
│   └── Status Display
│
└── Helper Functions
    ├── fetch_public_ip()
    ├── fetch_dns_servers()
    ├── detect_vpn_adapter()
    ├── check_vpn_keywords_*()
    └── Utility Functions
```


***

## 🖥️ Platform-Specific Notes

### Windows

**Commands Used:**

- `ipconfig /all` - DNS server extraction
- `netsh interface show interface` - Adapter listing
- `curl -s --max-time 10 ifconfig.me` - Public IP

**Detected Adapters:**

- TAP, TUN, Virtual Adapters
- Cisco AnyConnect, Pulse Secure
- OpenVPN, WireGuard, NordVPN, ExpressVPN, etc.

***

### Linux

**Commands Used:**

- `cat /etc/resolv.conf` - DNS servers
- `ip addr show` - Network interfaces
- `curl -s --max-time 10 ifconfig.me` - Public IP

**Detected Interfaces:**

- `tun0`, `tap0`, `wg0` (WireGuard)
- `ppp0`, `utun`, `vpn`
- IPSec, L2TP, PPTP interfaces

***

### macOS

**Commands Used:**

- `cat /etc/resolv.conf` - DNS servers
- `ifconfig` - Network interfaces
- `curl -s --max-time 10 ifconfig.me` - Public IP

**Detected Interfaces:**

- `utun*` (native macOS VPN)
- `tun*`, `tap*` (OpenVPN)
- `wg*` (WireGuard)

***

## 🔐 Security Considerations

### ⚠️ Important Notes

1. **False Positives:** Some virtual network adapters may trigger VPN detection
2. **IPv6 Leaks:** Tool checks IPv4 only—manually verify IPv6 routing
3. **DNS Leaks:** Use external tests (dnsleaktest.com) for comprehensive validation
4. **WebRTC Leaks:** Browser-based leaks are not detected by this tool

### 🛡️ Best Practices

- Always test with external leak detection websites
- Verify kill switch functionality (disconnect VPN and check connectivity)
- Monitor for DNS cache poisoning
- Ensure IPv6 is disabled if VPN doesn't support it

***

## 🐛 Troubleshooting

### Issue: "ERROR: Unable to fetch public IP address"

**Causes:**

- No internet connection
- `curl` not installed or not in PATH
- Firewall blocking outbound HTTP requests

**Solutions:**

```bash
# Verify curl installation
curl --version

# Test curl manually
curl -s ifconfig.me

# Check firewall settings
```


***

### Issue: "WARNING: Unable to fetch DNS information"

**Causes:**

- Insufficient permissions (Windows)
- Missing `/etc/resolv.conf` (Linux/macOS)

**Solutions:**

```bash
# Run with elevated privileges
sudo ./vpn_checker   # Linux/macOS
# Run as Administrator (Windows)

# Verify resolv.conf exists
cat /etc/resolv.conf
```


***

### Issue: VPN adapter not detected despite active connection

**Causes:**

- VPN uses non-standard interface naming
- Proprietary VPN implementation

**Solutions:**

- Add custom keywords to `check_vpn_keywords_*()` functions
- Check interface names manually:

```bash
# Linux
ip link show

# Windows
ipconfig /all

# macOS
ifconfig
```


***

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Areas for Improvement

- [ ] Add IPv6 support
- [ ] Implement WebRTC leak detection
- [ ] Add GUI version
- [ ] Support for more VPN providers
- [ ] Automated leak testing integration
- [ ] JSON output mode

***

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

***

## 🙏 Acknowledgments

- **ifconfig.me** for public IP API
- VPN provider communities for adapter naming conventions
- Open-source security research community

***

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/vpn-checker/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/vpn-checker/discussions)
- **Email:** your.email@example.com

***

## 📊 Project Stats


***

**Made with ❤️ for privacy and security enthusiasts**

*Last Updated: November 28, 2025*
<span style="display:none">[^1]</span>

<div align="center">⁂</div>

[^1]: main.c

