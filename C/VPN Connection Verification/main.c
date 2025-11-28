#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Platform detection macros
#ifdef _WIN32
#define OS_WINDOWS
#define DNS_COMMAND "ipconfig /all"
#define INTERFACE_COMMAND "netsh interface show interface"
#elif __linux__
#define OS_LINUX
#define DNS_COMMAND "cat /etc/resolv.conf"
#define INTERFACE_COMMAND "ip addr show"
#elif __APPLE
#define OS_LINUX
#define DNS_COMMAND "cat /etc/resolv.conf"
#define INTERFACE_COMMAND "ifconfig"
#else
#define OS_UNKNOWN
#endif

#define MAX_BUFFER 2048
#define IP_SIZE 100
#define DNS_SIZE 1024

// Function prototypes
int fetch_public_ip(char *ip_buffer);
int fetch_dns_servers(char *dns_buffer);
int detect_vpn_adapter(char *adapter_buffer);
void print_separator(char c, int length);
void safe_copy(char *dest, const char *src, size_t size);
int check_vpn_keywords_windows(const char *line);
int check_vpn_keywords_unix(const char *line);

int main()
{
    char ip_before[IP_SIZE] = {0};
    char ip_after[IP_SIZE] = {0};
    char dns_before[DNS_SIZE] = {0};
    char dns_after[DNS_SIZE] = {0};
    char vpn_adapter_before[MAX_BUFFER] = {0};
    char vpn_adapter_after[MAX_BUFFER] = {0};

    int ip_changed = 0;
    int dns_changes = 0;
    int vpn_adapter_detected = 0;

    print_separator('=', 65);
    printf("      Advanced VPN Connectivity Verfication Tool\n");
    print_separator('=', 65);

#ifdef OS_WINDOWS
    printf("Operating System: Windows\n");
#elif defined(OS_LINUX)
    printf("Operating System: Linux\n");
#elif defined(OS_MAC)
    printf("Operating System: macOS\n");
#else
    printf("Operting System: unknown\n");
#endif
    print_separator('=', 65);

    // Step 1: Check IP Before VPN Connection
    printf("\n[Step 1] Checking current public IP address...\n");
    if (fetch_public_ip(ip_before) != 0)
    {
        printf("ERROR: Unable to fetch public IP address.\n");
        printf("Please check your internet connection.\n");
        return 1;
    }
    printf("Public IP before VPN: %s\n", ip_before);

    // Step 2: Check DNS Servers Before VPN Connection
    printf("\n[Step 2] Checking cuurent DNS Servers...\n");
    if (fetch_dns_servers(dns_before) != 0)
    {
        printf("WARNING: Unable to fetch DNS information.\n");
    }
    else
    {
        printf("DNS Servers (Before VPN): \n%s\n", dns_before);
    }

    // Step 3: Check VPN Network Adapter Before VPN Connection
    printf("\n[Step 3] Scanning for VPN network adapters...\n");
    detect_vpn_adapter(vpn_adapter_before);
    if (strlen(vpn_adapter_before) > 0)
    {
        printf("VPN Adapters Found (Before VPN): \n%s\n", vpn_adapter_before);
    }
    else
    {
        printf("No VPN adapters detected (before VPN).\n");
    }

    print_separator('=', 65);
    printf("\n>>> NOW CONNECT TO YOUR VPN <<<\n");
    printf(">>> Press ENTER when connected <<<\n");
    getchar();

    print_separator('=', 65);

    // Step 4: Check IP Before VPN Connection
    printf("\n[Step 1] Checking current public IP address...\n");
    if (fetch_public_ip(ip_after) != 0)
    {
        printf("ERROR: Unable to fetch public IP address.\n");
        return 1;
    }
    printf("Public IP before VPN: %s\n", ip_after);

    // Step 5: Check DNS Servers Before VPN Connection
    printf("\n[Step 2] Checking cuurent DNS Servers...\n");
    if (fetch_dns_servers(dns_after) != 0)
    {
        printf("WARNING: Unable to fetch DNS information.\n");
    }
    else
    {
        printf("DNS Servers (After VPN): \n%s\n", dns_after);
    }

    // Step 6: Check VPN Network Adapter Before VPN Connection
    printf("\n[Step 3] Scanning for VPN network adapters...\n");
    detect_vpn_adapter(vpn_adapter_after);
    if (strlen(vpn_adapter_after) > 0)
    {
        printf("VPN Adapters Found (After VPN): \n%s\n", vpn_adapter_after);
        vpn_adapter_detected = 1;
    }
    else
    {
        printf("No VPN adapters detected (After VPN).\n");
    }

    print_separator('=', 65);
    printf("                    Verification Summary\n");
    print_separator('=', 65);

    printf("\n%-30s %s\n", "IP Address (Before): ", ip_before);
    printf("%-30s %s\n", "IP Address (After): ", ip_after);

    // Compare IPs
    ip_changed = (strcmp(ip_before, ip_after) != 0);
    printf("%-30s %s\n", "IP Changed:", ip_changed ? "YES" : "NO");

    // Compare DNS Servers
    dns_changes = (strcmp(dns_before, dns_after) != 0);
    printf("%-30s %s\n", "DNS Changed:", dns_changes ? "YES" : "NO");

    // VPN Adapter Status
    printf("%-30s %s\n", "VPN Adapter Detected:", vpn_adapter_detected ? "YES" : "NO");

    print_separator('=', 65);

    printf("\n");
    print_separator('*', 65);

    if (ip_changed && vpn_adapter_detected)
    {
        printf("              VPN STATUS: ACTIVE\n");
        printf("    Your connection is successfully routed through VPN!\n");
    }
    else if (ip_changed && !vpn_adapter_detected)
    {
        printf("              VPN STATUS: LIKELY ACTIVE\n");
        printf("  IP changed but no VPN adapter detected. Verify manually.\n");
    }
    else if (!ip_changed && !vpn_adapter_detected)
    {
        printf("              VPN STATUS: PARTIAL\n");
        printf("  VPN adapter found but IP did not change. Check routing.\n");
    }
    else
    {
        printf("              VPN STATUS: NOT ACTIVE\n");
        printf("     Your connection is NOT protected by VPN!\n");
    }

    print_separator('*', 65);
    printf("\n[SECURITY NOTE] For complete security verification:\n");
    printf("  1. Check DNS leaks: https://dnsleaktest.com\n");
    printf("  2. Check WebRTC leaks: https://browserleaks.com/webrtc\n");
    printf("  3. Verify IPv6 is disabled or routed through VPN\n");
    print_separator('=', 65);
    return 0;
}

// Fetch public IP address using curl
int fetch_public_ip(char *ip_buffer)
{
    FILE *fp;
    char command[] = "curl -s --max-time 10 ifconfig.me";

    fp = popen(command, "r");
    if (fp == NULL)
    {
        return 1;
    }

    if (fgets(ip_buffer, IP_SIZE, fp) == NULL)
    {
        pclose(fp);
        return 1;
    }

    pclose(fp);
    return 0;
}

// Fetch DNS Server based pn platform
int fetch_dns_servers(char *dns_buffer)
{
    FILE *fp;
    char line[256];
    int found = 0;

#ifdef OS_WINDOWS
    fp = popen(DNS_COMMAND, "r");
    if (fp == NULL)
    {
        return 1;
    }

    dns_buffer[0] = '\0';
    while (fgets(line, sizeof(line), fp) != NULL)
    {
        // strstr() is a standard library function that searches for a substring within a string.
        if (strstr(line, "DNS Servers") != NULL || strstr(line, "DNS Server") != NULL)
        {
            strncat(dns_buffer, line, DNS_SIZE - strlen(dns_buffer) - 1);
            found = 1;

            // Read continuation lines (indented IPs)
            while (fgets(line, sizeof(line), fp) != NULL)
            {
                if (line[0] == ' ' && (strstr(line, ".") != NULL || strstr(line, ":") != NULL))
                {
                    strncat(dns_buffer, line, DNS_SIZE - strlen(dns_buffer) - 1);
                }
                else
                {
                    break;
                }
            }
        }
    }
#else
    fp = popen(DNS_COMMAND, "r");
    if (fp == NULL)
    {
        return 1;
    }

    dns_buffer[0] = '\0';
    while (fgets(line, sizeof(line), fp) != NULL)
    {
        if (strstr(line, "nameserver") != NULL)
        {
            strncat(dns_buffer, "  ", DNS_SIZE - strlen(dns_buffer) - 1);
            strncat(dns_buffer, line, DNS_SIZE - strlen(dns_buffer) - 1);
            found = 1;
        }
    }
#endif
    pclose(fp);
    if (!found)
    {
        strcpy(dns_buffer, "   No DNS Servers found.\n");
    }

    return 0;
}

// Detect VPN adapter based on platform
int detect_vpn_adapter(char *adapter_buffer)
{
    FILE *fp;
    char line[512];
    int found = 0;

    adapter_buffer[0] = '\0';
#ifdef OS_WINDOWS
    fp = popen(INTERFACE_COMMAND, "r");
    if (fp == NULL)
    {
        return 1;
    }

    while (fgets(line, sizeof(line), fp) != NULL)
    {
        if (check_vpn_keywords_windows(line))
        {
            strncat(adapter_buffer, "  ", MAX_BUFFER - strlen(adapter_buffer) - 1);
            strncat(adapter_buffer, line, MAX_BUFFER - strlen(adapter_buffer) - 1);
            found = 1;
        }
    }
#else
    fp = popen(INTERFACE_COMMAND, "r");
    if (fp == NULL)
    {
        return 1;
    }

    while (fgets(line, sizeof(line), fp) != NULL)
    {
        if (check_vpn_keywords_unix(line))
        {
            strncat(adapter_buffer, "  ", MAX_BUFFER - strlen(adapter_buffer) - 1);
            strncat(adapter_buffer, line, MAX_BUFFER - strlen(adapter_buffer) - 1);
            found = 1;
        }
    }
#endif
    pclose(fp);
    return found ? 0 : 1;
}

// Check for VPN keywords in Windows output
int check_vpn_keywords_windows(const char *line)
{
    if (strstr(line, "adapter") != NULL || strstr(line, "Adapter") != NULL)
    {
        if (
            strstr(line, "TAP") != NULL ||
            strstr(line, "TUN") != NULL ||
            strstr(line, "VPN") != NULL ||
            strstr(line, "Tunnel") != NULL ||
            strstr(line, "WireGuard") != NULL ||
            strstr(line, "OpenVPN") != NULL ||
            strstr(line, "NordVPN") != NULL ||
            strstr(line, "ExpressVPN") != NULL ||
            strstr(line, "ProtonVPN") != NULL ||
            strstr(line, "Virtual") != NULL ||
            strstr(line, "AnyConnect") != NULL ||
            strstr(line, "Pulse") != NULL ||
            strstr(line, "Fortinet") != NULL ||
            strstr(line, "SonicWall") != NULL ||
            strstr(line, "Ivacy") != NULL ||
            strstr(line, "VyprVPN") != NULL ||
            strstr(line, "Surfshark") != NULL ||
            strstr(line, "CyberGhost") != NULL ||
            strstr(line, "HotspotShield") != NULL ||
            strstr(line, "Hide.me") != NULL ||
            strstr(line, "PrivateVPN") != NULL ||
            strstr(line, "PureVPN") != NULL ||
            strstr(line, "VPN Gate") != NULL ||
            strstr(line, "SoftEther") != NULL ||
            strstr(line, "L2TP") != NULL ||
            strstr(line, "PPTP") != NULL ||
            strstr(line, "IPSec") != NULL)
        {
            return 1;
        }
    }
    return 0;
}

// Check for VPN keywords in Unix output
int check_vpn_keywords_unix(const char *line)
{
    if (
        strstr(line, "tun") != NULL ||
        strstr(line, "tap") != NULL ||
        strstr(line, "wg") != NULL ||
        strstr(line, "ppp") != NULL ||
        strstr(line, "utun") != NULL ||
        strstr(line, "vpn") != NULL ||
        strstr(line, "wireguard") != NULL ||
        strstr(line, "openvpn") != NULL ||
        strstr(line, "tinc") != NULL ||
        strstr(line, "softether") != NULL ||
        strstr(line, "ipsec") != NULL ||
        strstr(line, "l2tp") != NULL ||
        strstr(line, "pptp") != NULL ||
        strstr(line, "sstp") != NULL ||
        strstr(line, "gre") != NULL ||
        strstr(line, "ovpn") != NULL ||
        strstr(line, "zt") != NULL ||
        strstr(line, "nordlynx") != NULL ||
        strstr(line, "cxn") != NULL ||
        strstr(line, "ipip") != NULL ||
        strstr(line, "sec") != NULL ||
        strstr(line, "peer") != NULL ||
        strstr(line, "masq") != NULL ||
        strstr(line, "netextender") != NULL ||
        strstr(line, "sslvpnd") != NULL)
    {
        // Filter out false positives
        if (strstr(line, "opportun") == NULL) // To ignore 'opportunistic encryption'
        {
            return 1;
        }
    }
    return 0;
}

// Print a separator line
void print_separator(char c, int length)
{
    for (int i = 0; i < length; i++)
    {
        printf("%c", c);
    }
    printf("\n");
}

// Safe string copy
void safe_copy(char *dest, const char *src, size_t size)
{
    strncpy(dest, src, size - 1);
    dest[size - 1] = '\0';
}
