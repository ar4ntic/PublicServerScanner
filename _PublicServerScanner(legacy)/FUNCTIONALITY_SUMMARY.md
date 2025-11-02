# PublicServerScanner (Legacy) - Functionality Summary

## Overview

PublicServerScanner is a comprehensive security assessment tool designed to evaluate the external attack surface of public-facing servers. It performs automated security checks across multiple domains including network security, web application security, DNS configuration, and SSL/TLS implementation.

**Version:** 1.1
**Developer:** Arantic Digital (2025)
**Target Users:** Security professionals, system administrators, DevOps engineers

## Core Purpose

The application performs non-invasive, read-only security assessments to identify:
- Exposed services and potential vulnerabilities
- HTTP security header misconfigurations
- SSL/TLS certificate issues
- DNS information leakage
- Directory enumeration vulnerabilities
- Network service configurations

## Technology Stack

- **Language:** Python 3.8+
- **Architecture:** Modular, cross-platform (Linux, macOS, Windows)
- **UI Options:** CLI (primary) and GUI (Tkinter-based)
- **Configuration:** JSON-based user configuration

### External Security Tools Required

- `nmap` - Port scanning and service detection
- `nikto` - Web server vulnerability scanning
- `sslscan` - SSL/TLS configuration analysis
- `gobuster` - Directory/file brute-forcing
- `dig` - DNS enumeration
- `openssl` - Certificate analysis
- `curl` - HTTP header inspection

## Key Features

### 1. Port Scanning
- Full TCP port scan (1-65535)
- Service version detection
- UDP port scanning (top 100 ports)
- Configurable nmap options

**Output:** Detailed port scan results with service identification

### 2. Web Directory Brute-Force
- Directory and file enumeration using gobuster
- Multiple wordlist support (dirb, SecLists)
- Automatic HTTP/HTTPS handling

**Output:** Discovered directories and files on web servers

### 3. DNS Enumeration
- Multiple DNS record queries (A, MX, NS, TXT, SOA, AAAA)
- Zone transfer (AXFR) vulnerability testing
- Comprehensive DNS configuration analysis

**Output:** Complete DNS profile with potential information leakage

### 4. SSL/TLS Certificate Analysis
- Certificate details extraction
- Expiration date verification
- Certificate chain validation
- Common name and subject alternative names

**Output:** Certificate information and validity status

### 5. HTTP Security Headers Analysis
- Security header presence verification
- Multiple user-agent testing
- Server version information extraction
- Best practices compliance checking

**Output:** Security header audit with recommendations

### 6. Availability Testing
- ICMP ping verification
- Target reachability confirmation
- Latency measurement

**Output:** Basic connectivity status

## Application Structure

```
PublicServerScanner(legacy)/
├── app/
│   ├── checks/          # Security check modules
│   │   ├── ping.py
│   │   ├── portscan.py
│   │   ├── bruteforce.py
│   │   ├── dns.py
│   │   ├── cert.py
│   │   └── headers.py
│   ├── cli.py           # Command-line interface
│   ├── core.py          # Core orchestration
│   ├── config.py        # Configuration management
│   ├── constants.py     # Application constants
│   ├── installer.py     # Installation script
│   └── utils.py         # Utility functions
├── tests/               # Comprehensive test suite
├── StartScan.py         # Main entry point
├── StartAudit.py        # Alternative entry point
└── Install.py           # Installation script
```

## Usage

### Installation

```bash
python Install.py
```

Creates per-user installation in `~/.PublicServerScanner/` with:
- Virtual environment
- Configuration files
- Wordlists (including SecLists)
- Log directories

### Basic Scan

```bash
python StartScan.py --target example.com
```

### Specific Checks

```bash
python StartScan.py --target example.com --checks ping,portscan,headers
```

### Available Checks

- `ping` - Target availability
- `portscan` - Network port scanning
- `bruteforce` - Web directory enumeration
- `dns` - DNS configuration analysis
- `cert` - SSL/TLS certificate details
- `headers` - HTTP security headers

### GUI Mode

```bash
python StartScan.py --target example.com --gui
```

## Configuration

User configuration stored at `~/.PublicServerScanner/config.json`

### Key Configuration Options

```json
{
    "wordlists": {
        "selected": "default",
        "custom_path": ""
    },
    "nmap": {
        "tcp_options": "-sS -Pn -p-",
        "service_options": "-sV -sC -p22,80,443",
        "udp_options": "-sU --top-ports 100"
    },
    "timeout": 3600,
    "scan_threads": 1
}
```

## Output Structure

Each scan creates a timestamped directory:

```
scan_[target]_[YYYYMMDD_HHMMSS]/
├── ping.txt
├── tcp_port_scan.txt
├── service_version_scan.txt
├── udp_port_scan.txt
├── directory_bruteforce.txt
├── dns_enumeration.txt
├── certificate_details.txt
└── http_headers.txt
```

## Security Considerations

### Safe by Design
- **Non-invasive:** All operations are read-only
- **No exploitation:** Identifies vulnerabilities without exploiting them
- **Timeout protection:** All scans have configurable timeouts
- **Permission awareness:** Warns when elevated privileges are needed

### Ethical Use
- Designed for authorized security assessments only
- Should only be used on systems you own or have permission to test
- May trigger intrusion detection systems
- Some scans may be resource-intensive

## Documentation

The application includes extensive documentation:

- **README.md (9.8KB):** Quick start guide and installation instructions
- **documentation.md (71KB):** Comprehensive security knowledge base including:
  - Detailed vulnerability explanations
  - Server hardening best practices
  - Remediation strategies
  - Security tools reference
  - Glossary of security terms

## Development Features

### Code Quality Tools
- `pytest` - Testing framework with comprehensive test coverage
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Static type checking
- `bandit` - Security vulnerability scanning
- `pylint` - Code analysis

### Testing Infrastructure
- Unit tests for all modules
- Integration tests for security checks
- Installer functionality tests
- Test fixtures and mocking support

## Typical Use Cases

1. **Pre-deployment Security Assessment**
   - Verify security configurations before going live
   - Check for common misconfigurations

2. **Regular Security Audits**
   - Periodic assessment of public-facing infrastructure
   - Compliance verification

3. **Vulnerability Management**
   - Identify exposed services
   - Track security posture over time

4. **Security Training**
   - Educational tool for understanding attack surfaces
   - Demonstration of security best practices

## Limitations

- Requires external security tools to be pre-installed
- Some checks need elevated privileges
- GUI mode requires tkinter availability
- Port scanning may impact network performance
- Results accuracy depends on network conditions

## Target Compatibility

- **Operating Systems:** Linux, macOS, Windows
- **Target Systems:** Any public-facing server with IP address or hostname
- **Protocols:** HTTP/HTTPS, DNS, TCP/UDP, SSL/TLS

## Key Differentiators

1. **Modular Architecture:** Easy to extend with new security checks
2. **Comprehensive Reporting:** Detailed output for each security domain
3. **Flexible Configuration:** JSON-based customization
4. **Dual Interface:** Both CLI and GUI options
5. **Educational Value:** Extensive documentation and security guidance
6. **Professional Quality:** Follows development best practices with testing and code quality tools

## Conclusion

PublicServerScanner (Legacy) is a well-architected security assessment tool that provides systematic evaluation of public-facing server security. Its modular design, comprehensive documentation, and professional development practices make it suitable for both production security assessments and educational purposes.
