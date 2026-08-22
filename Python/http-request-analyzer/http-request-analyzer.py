from __future__ import annotations   # how python handles type annotations

import argparse   # creating a command-line interfaces
import socket   # provides low-level network communication functionality
import ssl   # TLS functionality
import sys
import time
from dataclasses import dataclass, field   # Creating clean data containers
from datetime import datetime, timezone
from urllib.parse import urlparse   # Parse URLs

import requests   # HTTP client
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from requests.exceptions import RequestException


# Data Containers
@dataclass
class DNSInfo:
    hostname: str
    ip_addresses: list[str] = field(default_factory=list)   # creates a new list for every DNSInfo instance
    resolve_time_ms: float | None = None
    error: str |None = None


@dataclass
class TLSInfo:
    protocol: str | None = None            # TLS protocol version used
    cipher: str | None = None              # Cipher suite used to protect the connection
    issuer: str | None = None               # Certificate Authority that issued the certificate
    subject: str | None = None             # Identity/domain represented by the certificate
    not_before: str | None = None          # When certificate validity starts
    not_after: str | None = None           # When certificate expires
    dats_until_expiry: int | None = None   # Approximate remaining validity
    error: str | None = None               # No TLS error occurred


@dataclass
class HTTPInfo:
    status_code: int | None = None                              # Stores the HTTP status code
    reason: str | None = None                                   # Stores the textual explanation associated with the status code
    headers: dict[str, str] = field(default_factory=dict)       # Stores the HTTP response headers
    redirect_chain: list[str] = field(default_factory=list)     # Stores URLs involved in redirects
    response_time_ms: float | None = None                       # Stores the elapsed time for the HTTP request
    content_length: int | None = None                           # Stores the amount of response content your program downloaded
    error: str | None = None                                    # Stores an error message if the HTTP request fails


@dataclass
class AnalysisResult:
    url: str
    dns: DNSInfo
    http: HTTPInfo
    tls: TLSInfo | None


# Analyzer
# Runs DNS, HTTP and TLS inspection against a target URL>
class HTTPRequestAnalyzer:
    def __init__(self, timeout: float = 8.0, verify_tls: bool = True) -> None:
        self.timeout = timeout
        self.verify_tls = verify_tls

    def analyze(self, url: str) -> AnalysisResult:
        parsed = urlparse(url if "://" in url else f"https://{url}")
        hostname = parsed.hostname or ""

        dns_info = self._resolve_dns(hostname)
        http_info = self._inspect_http(parsed.geturl())

        tls_info = None  # Because not every URL uses HTTPS
        if parsed.scheme == "https" and dns_info.ip_addresses:
            port = parsed.port or 443
            tls_info = self._inspect_tls(hostname, port)


        return AnalysisResult(
            url=parsed.geturl(),
            dns=dns_info,
            http=http_info,
            tls=tls_info
        )

    # DNS
    def _resolve_dns(self, hostname) -> DNSInfo:
        info = DNSInfo(hostname=hostname)

        try:
            start = time.perf_counter()  # Measuring elapsed time (better for measure a short duration)

            results = socket.getaddrinfo(hostname, None)  # Return IPv4 and IPv6 addresses

            elapsed_ms = (time.perf_counter() - start) * 1000

            seen: set[str] = set()
            ips: list[str] = []

            for _family, _type, _proto, _canon, sockaddr in results:
                ip = sockaddr[0]

                if ip not in seen:
                    seen.add(ip)
                    ips.append(ip)

            info.ip_addresses = ips
            info.resolve_time_ms = round(elapsed_ms, 2)

        except socket.gaierror as exc:
            info.error = f"DNS resolution failed: {exc}"

        return info


    # HTTP
    def _inspect_http(self, url: str) -> HTTPInfo:
        info = HTTPInfo()

        try:
            start = time.perf_counter()
            response = requests.get(
                url,
                timeout=self.timeout,
                verify=self.verify_tls,
                allow_redirects=True,
                headers={"User-Agents": "HTTP-Request-Analyzer/1.0"}
            )
            elapsed_ms = (time.perf_counter() - start) * 1000

            info.status_code = response.status_code
            info.reason = response.reason
            info.headers  = dict(response.headers)
            info.response_time_ms = round(elapsed_ms, 2)
            info.content_length = len(response.content)
            info.redirect_chain = [r.url for r in response.history] + (
                [response.url] if response.history else []
            )

        except RequestException as exc:
            info.error = f"HTTP request failed: {exc}"
        return info


    # TLS
    def _inspect_tls(self, hostname: str, port: int) -> TLSInfo:
        info = TLSInfo()
        context = ssl.create_default_context()  # create a secure TLS/SSL configuration object
        if not self.verify_tls:
            context.check_hostname = False        # Disable hostname verification
            context.verify_mode = ssl.CERT_NONE   # Disable certificate verification

        try:
            # Create the TCP connection
            with socket.create_connection(
                    (hostname, port), timeout=self.timeout
            ) as sock:
                # Wrap the TCP socket with TLS
                with context.wrap_socket(sock, server_hostname=hostname) as tls_sock:
                    cipher_name, protocol, _bits = tls_sock.cipher()   # Retrieves information about the negotiated TLS connection.
                    info.protocol = protocol
                    info.cipher = cipher_name

                    der_cert = tls_sock.getpeercert(binary_form=True)   # server's certificate is retrieved in DER-encoded binary format (DER)
                    if der_cert:
                        cert = x509.load_der_x509_certificate(der_cert, default_backend())   # Converts the raw DER bytes into a usable X.509 certificate object.
                        info.subject = cert.subject.rfc4514_string()   # converts the X.509 subject into a standardized readable string.
                        info.issuer = cert.issuer.rfc4514_string()
                        info.not_before = cert.not_valid_before_utc.strftime(
                            "%b %d %H:%M:%S %Y UTC"
                        )
                        info.not_after = cert.not_valid_after_utc.strftime(
                            "%b %d %H:%M:%S %Y UTC"
                        )
                        delta = cert.not_valid_after_utc - datetime.now(timezone.utc)
                        info.dats_until_expiry = delta.days
        except ssl.SSLError as exc:
            info.error = f"TLS handshake failed: {exc}"
        except (socket.timeout, OSError) as exc:
            info.error = f"TLS connection failed: {exc}"
        return info


# Report formatting
def print_report(result: AnalysisResult) -> None:
    line = "-" * 60
    print(line)
    print(f"HTTP REQUEST ANALYZER = {result.url}")

    # DNS
    print("\n[DNS]")
    if result.dns.error:
        print(f"    Error: {result.dns.error}")
    else:
        print(f"    Hostname     : {result.dns.hostname}")
        print(f"    IP Addresses : {', '.join(result.dns.ip_addresses)}")
        print(f"    Resolve time : {result.dns.resolve_time_ms} ms")

    # HTTP
    print("\n[HTTP]")
    if result.http.error:
        print(f"    Error: {result.http.error}")
    else:
        print(f"    Status        : {result.http.status_code} {result.http.reason}")
        print(f"    Response time : {result.http.response_time_ms} ms")
        print(f"    Content size  : {result.http.content_length} bytes")
        if len(result.http.redirect_chain) > 1:
            print("     Redirects   :")
            for step in result.http.redirect_chain:
                print(f"    -> {step}")
        print("     Headers         :")
        for key, value in result.http.headers.items():
            print(f"    {key}: {value}")


    # TLS
    print("\n[TLS]")
    if result.tls is None:
        print("     Not applicable (non-HTTPS URL)")
    elif result.tls.error:
        print(f"    Error: {result.tls.error}")
    else:
        print(f"    Protocol: {result.tls.protocol}")
        print(f"    Cipher suite: {result.tls.cipher}")
        print(f"    Subject: {result.tls.subject}")
        print(f"    Issuer: {result.tls.issuer}")
        print(f"    Valid from: {result.tls.not_before}")
        print(f"    Valid until: {result.tls.not_after}")
        if result.tls.dats_until_expiry is not None:
            flag = "    EXPIRING SOON" if result.tls.dats_until_expiry < 30 else ""
            print(f"    Days to expiry: {result.tls.dats_until_expiry}{flag}")

    print(line)


# CLI

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect a URL's DNS, HTTP, headers, timing and TLS info."
    )
    parser.add_argument("url", help="Target URL, e.g. https://example.com")
    parser.add_argument("--timeout", type=float, default=8.0, help="Request timeout in seconds")
    parser.add_argument("--insecure", action="store_true", help="Skip TLC certificate verification (self-signed certs, etc.")
    args = parser.parse_args()

    analyzer = HTTPRequestAnalyzer(timeout=args.timeout, verify_tls=not args.insecure)
    result = analyzer.analyze(args.url)
    print_report(result)

    if result.http.error:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())


