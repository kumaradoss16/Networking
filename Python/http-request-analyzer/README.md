# HTTP Request Analyzer

## Description

HTTP Request Analyzer is a command-line Python tool that inspects a URL and displays its DNS, HTTP, redirect, response header, timing, and TLS certificate information.

The tool accepts a domain name or complete URL. If no scheme is provided, it uses HTTPS by default.

## Features

- Resolves a hostname to IPv4 and IPv6 addresses.
- Measures DNS resolution time.
- Sends an HTTP request to the target URL.
- Displays the HTTP status code and reason.
- Measures HTTP response time.
- Displays response headers.
- Reports downloaded response size.
- Shows the redirect chain.
- Inspects HTTPS/TLS connection details.
- Displays the negotiated TLS protocol and cipher suite.
- Displays certificate subject, issuer, validity dates, and remaining days.
- Supports custom request timeouts.
- Supports insecure TLS connections for self-signed certificates.

## Technologies Used

- Python
- `argparse`
- `socket`
- `ssl`
- `requests`
- `cryptography`
- `dataclasses`
- Python type annotations

## Project Structure

The project currently contains one Python program with the following main parts:

```text
project/
└── analyzer.py
```

The filename of the Python script is not specified in the provided code.

Important components inside the script:

- `DNSInfo`: Stores DNS resolution information.
- `TLSInfo`: Stores TLS connection and certificate information.
- `HTTPInfo`: Stores HTTP response information.
- `AnalysisResult`: Combines DNS, HTTP, and TLS results.
- `HTTPRequestAnalyzer`: Performs the analysis.
- `print_report()`: Prints the analysis results.
- `main()`: Handles command-line arguments and starts the program.

## How It Works

1. The program reads a URL from the command line.
2. If the URL does not contain a scheme, `https://` is added.
3. The hostname is resolved using `socket.getaddrinfo()`.
4. The program sends an HTTP GET request using the `requests` library.
5. Redirects, headers, status information, response time, and content size are collected.
6. For HTTPS URLs, the program creates a TLS connection using Python's `ssl` module.
7. The server certificate is parsed with the `cryptography` library.
8. The final DNS, HTTP, and TLS information is printed in the terminal.

## Requirements

- Python 3.10 or newer is recommended because the code uses modern type annotation syntax.
- `requests`
- `cryptography`

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install requests cryptography
```

The project does not include a dependency file in the provided code. A `requirements.txt` file can be created with:

```text
requests
cryptography
```

Then install the dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Run the program by passing a domain or URL:

```bash
python analyzer.py https://example.com
```

A domain without a scheme is also accepted:

```bash
python analyzer.py example.com
```

Set a custom timeout:

```bash
python analyzer.py https://example.com --timeout 15
```

Skip TLS certificate verification:

```bash
python analyzer.py https://localhost:8443 --insecure
```

The `--insecure` option is useful for self-signed certificates, but it should not be used for normal secure connections.

Example output:

```text
------------------------------------------------------------
HTTP REQUEST ANALYZER = https://example.com

[DNS]
    Hostname     : example.com
    IP Addresses : 93.184.216.34
    Resolve time : 25.41 ms

[HTTP]
    Status        : 200 OK
    Response time : 180.22 ms
    Content size  : 1256 bytes
     Headers:
    Content-Type: text/html

[TLS]
    Protocol: TLSv1.3
    Cipher suite: TLS_AES_256_GCM_SHA384
    Subject: CN=example.com
    Issuer: ...
    Valid from: ...
    Valid until: ...
    Days to expiry: 80
------------------------------------------------------------
```

The exact values depend on the target URL and network connection.

## Configuration

The program does not use a configuration file or environment variables.

Available command-line options:

| Option | Description | Default |
|---|---|---:|
| `url` | Target domain or URL | Required |
| `--timeout` | Request and connection timeout in seconds | `8.0` |
| `--insecure` | Disables TLS certificate and hostname verification | Disabled |

The HTTP request uses this User-Agent header:

```text
HTTP-Request-Analyzer/1.0
```

## Example

Analyze a website:

```bash
python analyzer.py https://example.org
```

Analyze a local HTTPS service with a self-signed certificate:

```bash
python analyzer.py https://localhost:8443 --insecure
```

For an HTTP URL, TLS inspection is skipped:

```bash
python analyzer.py http://example.com
```

The report displays DNS and HTTP information, followed by:

```text
[TLS]
     Not applicable (non-HTTPS URL)
```

## Security Notes

- Only analyze systems and URLs that you own or have permission to test.
- The `--insecure` option disables certificate verification and hostname verification. Use it only for trusted testing environments.
- Response headers are printed directly to the terminal. Avoid using this tool where sensitive header values may be exposed to other users.
- The tool follows HTTP redirects automatically.
- The program performs network connections to the supplied target, so user input should be treated as an external destination.
- The code uses a fixed User-Agent value and does not provide authentication support.
- The command-line help contains a typo: `--insecure` says “TLC” instead of “TLS”.
- The `User-Agent` request header is written as `User-Agents`; this may prevent it from being recognized as the standard HTTP `User-Agent` header.

## Limitations

- The program only performs an HTTP GET request.
- It does not support POST data, custom headers, cookies, authentication, or proxy settings.
- It follows redirects automatically and does not provide an option to disable redirects.
- The redirect output is only printed when more than one URL is present in the redirect chain.
- It does not inspect DNS record types such as MX, TXT, or CNAME.
- It does not validate whether the resolved IP addresses match expected infrastructure.
- It does not perform port scanning.
- It does not save results to JSON, CSV, or another file format.
- It does not retry failed requests.
- It does not handle every possible certificate parsing or TLS error.
- The certificate expiry field is named `dats_until_expiry`; the name should be corrected to `days_until_expiry`.
- HTTP response content is fully loaded into memory to calculate its size.
- The exit status reports HTTP errors, but DNS and TLS errors do not independently change the final exit code.

## Future Improvements

- Correct the `User-Agent` header name.
- Rename `dats_until_expiry` to `days_until_expiry`.
- Add a `requirements.txt` file.
- Add JSON and CSV output formats.
- Add options for custom headers, proxy support, and redirect control.
- Add retry handling for temporary network failures.
- Improve command-line validation for invalid URLs.
- Return non-zero exit codes for DNS and TLS failures.
- Add tests for DNS, HTTP, redirect, and certificate handling.
- Add structured logging instead of printing all results directly.
- Add support for selecting the HTTP method.
- Avoid downloading the complete response when only the content length is needed.

## License

No license specified.
