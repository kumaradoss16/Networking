#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#ifdef _WIN32
#include <windows.h>
#define sleep(x) Sleep((x) * 1000)
#else
#include <unistd.h>
#endif

// Platform detection macros
#ifdef _WIN32
#define OS_WINDOWS
#define DNS_COMMAND "ipconfig /all"
#define INTERFACE_COMMAND "netsh interface show interface"
#define PING_COMMAND "ping -n 4 %s"
#elif __APPLE__
#define OS_MAC
#define DNS_COMMAND "cat /etc/resolv.conf"
#define INTERFACE_COMMAND "ifconfig"
#define PING_COMMAND "ping -c 4 %s"
#elif __linux__
#define OS_LINUX
#define DNS_COMMAND "cat /etc/resolv.conf"
#define INTERFACE_COMMAND "ip addr show"
#define PING_COMMAND "ping -c 4 %s"
#else
#define OS_UNKNOWN
#endif

#define MAX_BUFFER 2048
#define IP_SIZE 100
#define DNS_SIZE 1024
#define COUNTRY_SIZE 100
#define REGION_SIZE 100
#define CITY_SIZE 100

// Function prototypes
int fetch_public_ip(char *ip_buffer);
int fetch_public_ipv6(char *ip_buffer);
int fetch_dns_servers(char *dns_buffer);
int detect_vpn_adapter(char *adapter_buffer);
void print_separator(char c, int length);
void safe_copy(char *dest, const char *src, size_t size);
int check_vpn_keywords_windows(const char *line);
int check_vpn_keywords_unix(const char *line);
int fetch_geolocation(char *country_buffer, char *region_buffer, char *city_buffer);
int measure_latency(const char *host);
int extract_first_dns_ip(const char *dns_buffer, char *ip_output);
int check_dns_leak(const char *dns_servers, const char *isp_dns);
int monitor_vpn_connection(int interval_seconds, int duration_seconds);

int main()
{
    char ip_before[IP_SIZE] = {0};
    char ip_after[IP_SIZE] = {0};
    char dns_before[DNS_SIZE] = {0};
    char dns_after[DNS_SIZE] = {0};
    char vpn_adapter_before[MAX_BUFFER] = {0};
    char vpn_adapter_after[MAX_BUFFER] = {0};
    char isp_dns[IP_SIZE] = {0}; // To store original ISP DNS for leak detection
    char dns_ip[IP_SIZE];
    char ipv6_before[IP_SIZE] = {0};
    char ipv6_after[IP_SIZE] = {0};

    int ip_changed = 0;
    int dns_changes = 0;
    int vpn_adapter_detected = 0;
    char country_before[100], country_after[100], region_before[100], region_after[100], city_before[100], city_after[100];

    int monitor_mode = 0;

    print_separator('=', 65);
    printf("      Advanced VPN Connectivity Verification Tool\n");
    print_separator('=', 65);
    printf("\nSelect Mode:\n"); // Fixed: was "/nSelect Mode:"
    printf("   1. Standard VPN Verification (Before/After)\n");
    printf("   2. Real-Time Monitor Mode\n"); // Fixed: was "Real_time"
    printf("\nEnter choice (1 or 2): ");

    int choice;
    scanf("%d", &choice);
    getchar(); // Consume the newline character

    if (choice == 2)
    {
        monitor_mode = 1;
        printf("\nReal-Time Monitor Configuration:\n");
        printf("Enter check interval (seconds, default 5): ");
        int interval = 5;
        scanf("%d", &interval);
        getchar();

        printf("Enter monitoring duration (seconds, default 60): ");
        int duration = 60;
        scanf("%d", &duration); // Fixed: was scanf("%d", duration) - missing &
        getchar();

        printf("\n>>> Connect to your VPN NOW <<<\n");
        printf(">>> Press ENTER to start monitoring <<<\n");
        getchar();

        monitor_vpn_connection(interval, duration);
        return 0;
    }
    // Continue with standard mode...
    print_separator('=', 65);

#ifdef OS_WINDOWS
    printf("Operating System: Windows\n");
#elif defined(OS_LINUX)
    printf("Operating System: Linux\n");
#elif defined(OS_MAC)
    printf("Operating System: macOS\n");
#else
    printf("Operating System: unknown\n"); // Fixed: was "Operting"
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
    printf("\n[Step 1.1] Checking current public IPv6 address...\n");
    if (fetch_public_ipv6(ipv6_before) == 0)
    {
        size_t len = strlen(ipv6_before);
        if (len > 0 && ipv6_before[len - 1] == '\n')
        {
            ipv6_before[len - 1] = '\0';
            printf("Public IPv6 before VPN: %s\n", ipv6_before);
        }
    }
    else
    {
        printf("WARNING: Unable to fetch IPv6 address (IPv6 may not be available)\n");
        strcpy(ipv6_before, "N/A");
    }

    // Step 2: Check DNS Servers Before VPN Connection
    printf("\n[Step 2] Checking current DNS Servers...\n");
    if (fetch_dns_servers(dns_before) != 0)
    {
        printf("WARNING: Unable to fetch DNS information.\n");
    }
    else
    {
        printf("DNS Servers (Before VPN): \n%s\n", dns_before);

        // Extract ISP DNS for leak detection
        if (extract_first_dns_ip(dns_before, isp_dns) == 0)
        {
            printf("ISP DNS recorded: %s\n", isp_dns);
        }
        else
        {
            printf("Could not extract ISP DNS.\n");
        }
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

    // Step 4: Measure Latency Before VPN
    printf("\n[Step 4] Measuring network latency (Before VPN)...\n");
    if (extract_first_dns_ip(dns_before, dns_ip) == 0)
    {
        printf("Pinging DNS server: %s\n", dns_ip);
        measure_latency(dns_ip);
    }
    else
    {
        printf("Could not extract DNS IP. Using 8.8.8.8\n");
        measure_latency("8.8.8.8");
    }

    // Step 4.1: Fetch Geolocation Before VPN
    printf("\n[Step 4.1] Fetching geolocation...\n");
    fetch_geolocation(country_before, region_before, city_before);
    printf("Location: %s, %s, %s\n", city_before, region_before, country_before);

    print_separator('=', 65);
    printf("\n>>> NOW CONNECT TO YOUR VPN <<<\n");
    printf(">>> Press ENTER when connected <<<\n");
    getchar();

    print_separator('=', 65);

    // Step 5: Check IP After VPN Connection
    printf("\n[Step 5] Checking current public IP address...\n"); // Fixed: was "Step 1"
    if (fetch_public_ip(ip_after) != 0)
    {
        printf("ERROR: Unable to fetch public IP address.\n");
        return 1;
    }
    printf("Public IP after VPN: %s\n", ip_after);
    printf("\n[Step 5.1] Checking current public IPv6 address...\n");
    if (fetch_public_ipv6(ipv6_after) == 0)
    {
        size_t len = strlen(ipv6_after);
        if (len > 0 && ipv6_after[len - 1] == '\n')
        {
            ipv6_after[len - 1] = '\0';
            printf("Public IPv6 after VPN: %s\n", ipv6_after); // Fixed: was "before VPN"
        }
    }
    else
    {
        printf("WARNING: Unable to fetch IPv6 address (IPv6 may not be available)\n");
        strcpy(ipv6_after, "N/A");
    }

    // Step 6: Check DNS Servers After VPN Connection
    printf("\n[Step 6] Checking current DNS Servers...\n"); // Fixed: was "Step 2"
    if (fetch_dns_servers(dns_after) != 0)
    {
        printf("WARNING: Unable to fetch DNS information.\n");
    }
    else
    {
        printf("DNS Servers (After VPN): \n%s\n", dns_after);

        // Check for DNS leak
        printf("\n[DNS Leak Test]\n");
        if (strlen(isp_dns) > 0)
        {
            if (check_dns_leak(dns_after, isp_dns) == 0)
            {
                printf("No DNS leak detected - using VPN DNS servers\n");
            }
            else
            {
                printf("DNS leak detected - your DNS queries may be visible to ISP\n");
            }
        }
        else
        {
            printf("Unable to perform DNS leak test (ISP DNS not recorded)\n");
        }
    }

    // Step 7: Check VPN Network Adapter After VPN Connection
    printf("\n[Step 7] Scanning for VPN network adapters...\n"); // Fixed: was "Step 3"
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

    // Step 8: Measure Latency After VPN
    printf("\n[Step 8] Measuring network latency (After VPN)...\n"); // Fixed: was "Step 4"
    if (extract_first_dns_ip(dns_after, dns_ip) == 0)
    {
        printf("Pinging DNS server: %s\n", dns_ip);
        measure_latency(dns_ip);
    }
    else
    {
        printf("Could not extract DNS IP. Using 8.8.8.8\n");
        measure_latency("8.8.8.8");
    }

    print_separator('=', 65);
    printf("                    Verification Summary\n");
    print_separator('=', 65);

    printf("\n%-30s %s\n", "IP Address (Before): ", ip_before);
    printf("%-30s %s\n", "IP Address (After): ", ip_after);

    printf("\n%-30s %s\n", "IPv6 Address (Before): ", ipv6_before);
    printf("%-30s %s\n", "IPv6 Address (After): ", ipv6_after);

    // Compare IPs
    ip_changed = (strcmp(ip_before, ip_after) != 0);
    printf("\n%-30s %s\n", "IP Changed:", ip_changed ? "YES" : "NO");

    int ipv6_changed = (strcmp(ipv6_before, ipv6_after) != 0);
    printf("%-30s %s\n", "IPv6 Changed:", ipv6_changed ? "YES" : "NO"); // Fixed: was "IP Changed"

    // Compare DNS Servers
    dns_changes = (strcmp(dns_before, dns_after) != 0);
    printf("%-30s %s\n", "DNS Changed:", dns_changes ? "YES" : "NO");

    // VPN Adapter Status
    printf("%-30s %s\n", "VPN Adapter Detected:", vpn_adapter_detected ? "YES" : "NO");

    // DNS Leak Status
    int dns_leak = 0;
    if (strlen(isp_dns) > 0)
    {
        dns_leak = check_dns_leak(dns_after, isp_dns);
        printf("%-30s %s\n", "DNS Leak Detected:", dns_leak ? "YES" : "NO");
    }

    // Geolocation changes
    fetch_geolocation(country_after, region_after, city_after);
    printf("\nCountry changed: %s to %s\n", country_before, country_after);
    printf("Region changed: %s to %s\n", region_before, region_after);
    printf("City changed: %s to %s\n", city_before, city_after);

    print_separator('=', 65);

    printf("\n");
    print_separator('*', 65);

    if (ip_changed && vpn_adapter_detected && !dns_leak)
    {
        printf("              VPN STATUS: ACTIVE\n");
        printf("    Your connection is successfully routed through VPN!\n");
    }
    else if (ip_changed && vpn_adapter_detected && dns_leak)
    {
        printf("              VPN STATUS: ACTIVE WITH DNS LEAK\n");
        printf("  VPN is active but DNS queries may leak to your ISP!\n");
    }
    else if (ip_changed && !vpn_adapter_detected)
    {
        printf("              VPN STATUS: LIKELY ACTIVE\n");
        printf("  IP changed but no VPN adapter detected. Verify manually.\n");
    }
    else if (!ip_changed && vpn_adapter_detected)
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

// Real-time VPN connection monitor
int monitor_vpn_connection(int interval_seconds, int duration_seconds)
{
    int elapsed = 0;
    char ip_current[IP_SIZE];
    char ip_first[IP_SIZE] = {0};

    printf("\n");
    print_separator('=', 65);
    printf("           Real-Time VPN Connection Monitor\n");
    printf("           Monitoring for %d seconds...\n", duration_seconds);
    print_separator('=', 65);
    printf("\n");

    while (elapsed < duration_seconds)
    {
        // Check IP
        if (fetch_public_ip(ip_current) == 0)
        {
            // Store first IP
            if (ip_first[0] == '\0')
            {
                strcpy(ip_first, ip_current);
            }

            // Remove newline from current IP
            size_t len = strlen(ip_current);
            if (len > 0 && ip_current[len - 1] == '\n')
            {
                ip_current[len - 1] = '\0';
            }

            // Also remove newline from first IP for comparison
            len = strlen(ip_first);
            if (len > 0 && ip_first[len - 1] == '\n')
            {
                ip_first[len - 1] = '\0';
            }

            // Check for IP change
            int ip_changed = (strcmp(ip_first, ip_current) != 0);
            printf("[%4ds] IP: %-15s ", elapsed, ip_current);

            if (ip_changed)
            {
                printf("WARNING [IP CHANGED!]\n");
            }
            else
            {
                printf("OK [Stable]\n");
            }
        }
        else
        {
            printf("[%4ds] ERROR Unable to fetch IP\n", elapsed);
        }

        sleep(interval_seconds);
        elapsed += interval_seconds;
    }

    print_separator('=', 65);
    printf("Monitoring complete.\n");
    print_separator('=', 65);

    return 0;
}

// Extract the first DNS IP address from dns_buffer
int extract_first_dns_ip(const char *dns_buffer, char *ip_output)
{
    if (dns_buffer == NULL || ip_output == NULL)
        return 1;

    ip_output[0] = '\0';

#ifdef OS_WINDOWS
    const char *line = dns_buffer;

    while (*line != '\0')
    {
        if (strstr(line, "DNS Server") != NULL)
        {
            const char *ip_start = strchr(line, ':');
            if (ip_start != NULL)
            {
                ip_start++;

                // Skip whitespace and dots
                while (*ip_start == ' ' || *ip_start == '.')
                    ip_start++;

                // Extract IP address
                int i = 0;
                while (*ip_start != '\0' && *ip_start != '\n' && i < IP_SIZE - 1)
                {
                    if ((*ip_start >= '0' && *ip_start <= '9') || *ip_start == '.')
                    {
                        ip_output[i++] = *ip_start;
                    }
                    else if (ip_output[0] != '\0')
                    {
                        break;
                    }
                    ip_start++;
                }
                ip_output[i] = '\0';

                // Validate IP (must have at least 7 chars like "1.1.1.1")
                if (strlen(ip_output) > 6)
                    return 0; // Success
            }
        }

        // Move to next line
        line = strchr(line, '\n');
        if (line == NULL)
            break;
        line++;
    }
#else
    // Linux/macOS: Extract from nameserver line
    const char *nameserver = strstr(dns_buffer, "nameserver");
    if (nameserver != NULL)
    {
        if (sscanf(nameserver, "nameserver %s", ip_output) == 1)
        {
            return 0; // Success
        }
    }
#endif

    return 1; // Failed to extract
}

// Measure network latency
int measure_latency(const char *host)
{
    char cmd[256];
    snprintf(cmd, sizeof(cmd), PING_COMMAND, host);

    FILE *fp = popen(cmd, "r");
    if (fp == NULL)
    {
        printf("ERROR: Unable to execute ping command.\n");
        return 1;
    }

    char line[256];
    int found = 0;

    printf("Pinging %s...\n", host);

    while (fgets(line, sizeof(line), fp) != NULL)
    {
#ifdef OS_WINDOWS
        if (strstr(line, "Average") != NULL || strstr(line, "Minimum") != NULL)
        {
            printf("   %s", line);
            found = 1;
        }
#else
        if (strstr(line, "avg") != NULL || strstr(line, "min") != NULL || strstr(line, "rtt") != NULL)
        {
            printf("   %s", line);
            found = 1;
        }
#endif
    }

    if (!found)
    {
        printf("   Unable to extract latency statistics.\n");
    }

    pclose(fp);
    return 0;
}

// Check the DNS leak detection
int check_dns_leak(const char *dns_servers, const char *isp_dns)
{
    if (dns_servers == NULL || isp_dns == NULL)
    {
        return 0;
    }

    // Extract the First DNS IP from the dns_servers buffer
    char first_dns_after_vpn[IP_SIZE] = {0};

    if (extract_first_dns_ip(dns_servers, first_dns_after_vpn) != 0)
    {
        return 0; // Could not extract DNS assume no leak
    }

    // Remove newline if present
    size_t len = strlen(first_dns_after_vpn);
    if (len > 0 && first_dns_after_vpn[len - 1] == '\n')
    {
        first_dns_after_vpn[len - 1] = '\0';
    }

    // Check if PRIMARY DNS changes from ISP DNS
    if (strlen(first_dns_after_vpn) > 0)
    {
        // If first DNS is still the ISP DNS = LEAK
        if (strcmp(first_dns_after_vpn, isp_dns) == 0)
        {
            printf("     WARNING: DNS Leak Detected!\n");
            printf("   Primary DNS is still ISP DNS: %s\n", isp_dns);
            return 1; // Leak detected
        }
        else
        {
            // First DNS is different (VPN DNS) = No Leak
            printf("      DNS Protection Active\n");
            printf("   Primary DNS changed to: %s\n", first_dns_after_vpn);
            return 0; // No leak
        }
    }
    return 0; // No leak
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

int fetch_public_ipv6(char *ip_buffer)
{
    FILE *fp;
    char command[] = "curl -6 -s --max-time 10 ifconfig.me";

    fp = popen(command, "r");
    if (fp == NULL)
        return 1;
    if (fgets(ip_buffer, IP_SIZE, fp) == NULL)
    {
        pclose(fp);
        return 1;
    }

    pclose(fp);
    return 0;
}

int fetch_geolocation(char *country_buffer, char *region_buffer, char *city_buffer)
{
    FILE *fp;

    // Fetch country
    char country_command[] = "curl -s ipinfo.io/country";
    fp = popen(country_command, "r");
    if (fp == NULL)
    {
        return 1;
    }
    if (fgets(country_buffer, COUNTRY_SIZE, fp) == NULL)
    {
        pclose(fp);
        return 1;
    }
    pclose(fp);

    // Remove newline character from country code
    size_t len = strlen(country_buffer);
    if (len > 0 && country_buffer[len - 1] == '\n')
    {
        country_buffer[len - 1] = '\0';
    }

    // Fetch region
    char region_command[] = "curl -s ipinfo.io/region";
    fp = popen(region_command, "r");
    if (fp == NULL)
    {
        return 1;
    }
    if (fgets(region_buffer, REGION_SIZE, fp) == NULL)
    {
        pclose(fp);
        return 1;
    }
    pclose(fp);

    // Remove newline character from region
    len = strlen(region_buffer);
    if (len > 0 && region_buffer[len - 1] == '\n')
    {
        region_buffer[len - 1] = '\0';
    }

    // Fetch city
    char city_command[] = "curl -s ipinfo.io/city";
    fp = popen(city_command, "r");
    if (fp == NULL)
    {
        return 1;
    }
    if (fgets(city_buffer, CITY_SIZE, fp) == NULL)
    {
        pclose(fp);
        return 1;
    }
    pclose(fp);

    // Remove newline character from city
    len = strlen(city_buffer);
    if (len > 0 && city_buffer[len - 1] == '\n')
    {
        city_buffer[len - 1] = '\0';
    }

    return 0;
}

// Fetch DNS Server based on platform
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
