# Public Server Scanner: Documentation, Usage & Knowledge Base


- [Public Server Scanner: Documentation, Usage \& Knowledge Base](#public-server-scanner-documentation-usage--knowledge-base)
- [Overview](#overview)
- [How the Security Scan Works](#how-the-security-scan-works)
- [Detailed Check Explanations](#detailed-check-explanations)
  - [Port Scan](#port-scan)
  - [Service/Version Scan](#serviceversion-scan)
  - [UDP Port Scan](#udp-port-scan)
  - [Directory Brute-Force](#directory-brute-force)
  - [Certificate Details](#certificate-details)
  - [DNS Enumeration](#dns-enumeration)
  - [HTTP Headers](#http-headers)
  - [Firewall Status](#firewall-status)
  - [User Privileges](#user-privileges)
  - [World-Writable Files](#world-writable-files)
  - [SSH Configuration](#ssh-configuration)
  - [Ping/Availability](#pingavailability)
- [How to Use the App](#how-to-use-the-app)
  - [Command-Line Usage](#command-line-usage)
  - [Technical Requirements](#technical-requirements)
- [Understanding the Results](#understanding-the-results)
  - [Reading the Output](#reading-the-output)
  - [Severity Levels](#severity-levels)
- [Example Output](#example-output)
  - [Summary Output Example](#summary-output-example)
  - [Detailed Check Output Example (Port Scan)](#detailed-check-output-example-port-scan)
  - [Detailed Check Output Example (Certificate Analysis)](#detailed-check-output-example-certificate-analysis)
- [Best Practices for Public Servers](#best-practices-for-public-servers)
  - [Network Security](#network-security)
  - [System Security](#system-security)
  - [Application Security](#application-security)
  - [Monitoring and Response](#monitoring-and-response)
- [Remediation \& Hardening Tips](#remediation--hardening-tips)
  - [Immediate Actions](#immediate-actions)
  - [Short-term Improvements](#short-term-improvements)
  - [Long-term Security Strategy](#long-term-security-strategy)
  - [Common Security Vulnerabilities](#common-security-vulnerabilities)
  - [Customization and Extension](#customization-and-extension)
  - [Customizing Existing Checks](#customizing-existing-checks)
  - [Adding New Security Checks](#adding-new-security-checks)
  - [Advanced Configuration](#advanced-configuration)
  - [Tips for Effective Use](#tips-for-effective-use)
  - [Security Tools Reference](#security-tools-reference)
  - [Network Security Tools](#network-security-tools)
  - [Web Application Security](#web-application-security)
  - [SSL/TLS Security](#ssltls-security)
  - [DNS Security](#dns-security)
  - [System Security](#system-security-1)
  - [Vulnerability Management](#vulnerability-management)
- [Glossary](#glossary)
- [FAQ](#faq)
  - [General Questions](#general-questions)
  - [Technical Questions](#technical-questions)
  - [Security Concerns](#security-concerns)
- [Need Help?](#need-help)
  - [Getting Support](#getting-support)
  - [Contributing](#contributing)
  - [Additional Resources](#additional-resources)

---

# Overview
The Public Server Scanner tool is a comprehensive vulnerability assessment and security scanning solution specifically designed for internet-exposed systems. It helps administrators, DevOps engineers, and security professionals identify, assess, and remediate security weaknesses in their external attack surface. This tool combines multiple security scanning capabilities that would typically require several specialized tools and security expertise to perform manually.

Key features of this tool include:

- **Comprehensive Security Assessment**: Tests multiple aspects of server security from network exposure to configuration issues
- **Multi-Platform Support**: Works on Linux, macOS, and Windows systems 
- **Detailed Reporting**: Provides both summary and in-depth results with actionable recommendations
- **Non-Invasive Testing**: Read-only operations that don't modify your systems
- **Educational Resource**: Serves as a knowledge base with explanations and remediation tips

Whether you're preparing a server for production deployment, conducting regular security audits, or responding to security incidents, this tool provides valuable insights into your server's security posture.

---

# How the Security Scan Works
The Public Server Scanner tool employs a modular architecture where each security check is implemented as a separate Python module that integrates with external security tools. When you run the scan, the following process takes place:

1. **Initialization**: The tool sets up the necessary environment, validates prerequisites, and creates directories for output.

2. **Target Selection**: You specify the target server by hostname or IP address.

3. **Check Selection**: You choose which security checks to run (or select all).

4. **Execution**: For each selected check, the tool:
   - Calls the appropriate Python module
   - Executes the relevant external tools with appropriate parameters
   - Captures output and logs for analysis
   - Processes results to identify security issues
   
5. **Reporting**: Results are consolidated into:
   - A summary report with key findings
   - Detailed logs for each check
   - Color-coded or severity-marked results
   - Recommendations for addressing issues

Each security check is designed to run independently, so you can choose which ones are relevant to your specific needs. The modular design also makes it easy to extend the tool with additional checks in the future.

---

# Detailed Check Explanations

## Port Scan
- **What it does:** Uses `nmap` to scan all TCP ports (1-65535) on the target to identify which ports are open and what services are running.
- **Implementation details:** Executes `nmap -sS -Pn -p-` (or configured options) to perform a SYN scan of all TCP ports. The SYN scan is less intrusive than a full TCP connect scan and is less likely to be logged.
- **Why it matters:** Open ports expose services to the network. Each open port is a potential entry point for attackers, increasing your attack surface. Every unnecessary service increases your vulnerability footprint.
- **What to look for:** 
  - Unexpected open ports
  - High-risk services: Telnet (23), FTP (21), SMB/CIFS (139/445)
  - Admin interfaces exposed to public networks (cPanel, phpMyAdmin, RDP)
  - Services running on non-standard ports (potential hidden services)
- **Common vulnerable ports:**

| **Port** | **Service** | **Common Vulnerabilities** | **Risk Level** |
|------|---------|------------------------|------------|
| 22 | SSH | Brute-force attacks, outdated implementations | 🟠 Medium-High |
| 23 | Telnet | Unencrypted traffic, credential theft | 🔴‼️ Critical |
| 21 | FTP | Unencrypted credentials, anonymous access | 🔴 High |
| 25 | SMTP | Open relay, spam forwarding | 🟠 Medium |
| 53 | DNS | Cache poisoning, amplification attacks | 🟠 Medium-High |
| 80/443 | HTTP/HTTPS | Web vulnerabilities, outdated software | 🔴 High |
| 139/445 | SMB/CIFS | Remote code execution (EternalBlue) | 🔴‼️ Critical |
| 1433 | MS SQL | Database access, weak credentials | 🔴 High |
| 3306 | MySQL | Database access, weak configurations | 🔴 High |
| 3389 | RDP | BlueKeep, connection hijacking | 🔴‼️ Critical |
| 8080 | Alt HTTP | Administration interfaces, proxies | 🟠 Medium-High |
- **Remediation:** 
  - Close unused ports via firewall rules
  - Restrict access to necessary IPs only via firewall
  - Consider moving services to non-standard ports (security by obscurity, a small additional layer)
  - Implement network segmentation to isolate critical services
  - Use TCP wrappers or equivalent access controls where applicable

## Service/Version Scan
- **What it does:** Uses `nmap` with version detection (-sV) and script scanning (-sC) to identify services, versions, and potential vulnerabilities.
- **Implementation details:** Runs `nmap -sV -sC` on ports identified during the port scan. The tool uses service fingerprinting and banner grabbing techniques to identify software versions.
- **Why it matters:** 
  - Outdated or vulnerable services are prime targets for attackers
  - Knowing exact versions helps with vulnerability correlation
  - Unnecessary service details in banners provide attackers with valuable information
- **What to look for:** 
  - Services with known CVEs (Common Vulnerabilities and Exposures)
  - End-of-life software versions no longer receiving security updates
  - Default configurations or installations
  - Excessive version information in banners
- **Vulnerability correlation:**
  - Apache < 2.4.50: Path Traversal (CVE-2021-41773)
  - OpenSSH < 8.4: User Enumeration
  - WordPress < 5.8.3: Multiple vulnerabilities
- **Remediation:** 
  - Update all services to the latest stable version
  - Implement a patch management system/schedule
  - Disable unnecessary services
  - Remove version information from banners where possible
  - Subscribe to security advisories for installed software

## UDP Port Scan
- **What it does:** Uses `nmap` to scan for open UDP ports, which are often overlooked but can be critical for security.
- **Implementation details:** Executes `nmap -sU --top-ports 100` to test the most commonly used UDP ports. UDP scanning is slower than TCP, so only top ports are scanned by default.
- **Why it matters:** 
  - UDP services are frequently forgotten in security audits
  - Many critical services use UDP: DNS (53), SNMP (161), NTP (123)
  - UDP services are commonly used in amplification DDoS attacks
- **What to look for:** 
  - UDP ports that shouldn't be publicly accessible:
    - SNMP (161): Can leak system information
    - NTP (123): Potential for NTP amplification attacks
    - DNS (53): Zone transfers, cache poisoning if misconfigured
    - NetBIOS/LDAP (137-139): Can reveal internal network information
    - TFTP (69): Should never be internet-accessible
- **Attack scenarios:**
  - DNS amplification: Open recursive DNS resolvers
  - SNMP information disclosure: Default community strings
  - RPC vulnerabilities via UDP ports
- **Remediation:** 
  - Block unnecessary UDP services at the firewall
  - Configure SNMP with strong community strings or preferably SNMPv3
  - Secure DNS servers and disable recursive queries if not needed
  - Implement rate limiting for UDP services that must remain open

## Directory Brute-Force
- **What it does:** Uses `gobuster` with wordlists to discover hidden or unlinked directories and files on web servers.
- **Implementation details:** Executes gobuster with a selected wordlist against the target URL, making HTTP requests for each potential path.
- **Why it matters:** 
  - Hidden directories can contain sensitive data, backup files, or admin interfaces
  - Developers often leave test, debug, or backup files on production servers
  - Default installations may include sample files with vulnerabilities
- **What to look for:** 
  - Admin panels: `/admin`, `/administrator`, `/wp-admin`, `/phpmyadmin`
  - Backup files: `.bak`, `.old`, `.backup`, `~`, `.swp`
  - Configuration files: `.env`, `.config`, `web.config`, `.htaccess`
  - Version control: `.git`, `.svn`
  - Test or development files: `/test`, `/dev`, `/stage`
  - Sensitive data: `/backup`, `/db`
- **Common findings and risks:**
  - Exposed .git directories can lead to source code disclosure
  - Backup files may contain credentials or sensitive data
  - Admin interfaces with weak credentials
  - Debug endpoints that reveal application details
- **Remediation:** 
  - Remove or restrict access to sensitive directories
  - Implement proper access controls and authentication
  - Use robots.txt to guide legitimate crawlers, but don't rely on it for security
  - Configure web server to prevent directory listing
  - Regularly audit web content for unintended exposures

## Certificate Details
- **What it does:** Uses `openssl` to fetch and comprehensively analyze SSL/TLS certificates from the target server.
- **Implementation details:** 
  - Connects to the target using OpenSSL's s_client
  - Extracts and parses certificate information
  - Checks certificate chain validity
  - Reviews expiry dates and certificate properties
- **Why it matters:** 
  - Expired or invalid certificates create browser warnings and diminish user trust
  - Weak cryptography can lead to interception of encrypted traffic
  - Self-signed certificates bypass trusted CA validation
  - Incorrect certificates expose users to man-in-the-middle attacks
- **What to look for:** 
  - **Validity period:** Certificates expiring soon (< 30 days) or already expired
  - **Signature algorithm:** Weak algorithms like SHA-1 or MD5 should not be used
  - **Key length:** RSA keys should be at least 2048 bits, ECC keys at least 256 bits
  - **Subject Alternative Names (SANs):** Ensure all domains served are covered
  - **Certificate chain:** Complete and properly constructed
  - **Certificate Authority:** Issued by a trusted CA, not self-signed
  - **Revocation status:** Whether the certificate appears on CRL or OCSP
- **Critical certificate issues:**
  - Hostname mismatch between certificate and server
  - Expired certificates
  - Self-signed certificates in production
  - Insecure cipher suites enabled
  - Missing intermediate certificates
- **Remediation:** 
  - Deploy certificates from trusted CAs (Let's Encrypt offers free options)
  - Implement automatic certificate renewal
  - Use modern cipher suites and protocols (TLS 1.2+, disable SSL 3.0 and TLS 1.0/1.1)
  - Configure HSTS (HTTP Strict Transport Security)
  - Ensure complete certificate chains
  - Use tools like SSL Labs to verify configuration

## DNS Enumeration
- **What it does:** Uses `dig` and other tools to gather DNS records and test for misconfigurations like zone transfers.
- **Implementation details:** 
  - Executes a series of `dig` commands for different record types
  - Performs basic lookups for A, MX, NS, and TXT records
  - Attempts DNS zone transfers (AXFR) to check for this critical misconfiguration
  - Cleans URLs by removing protocol prefixes and paths to focus on the domain
  - Results are combined into a comprehensive DNS report
- **Why it matters:** 
  - DNS records can reveal network architecture and potential targets
  - Misconfigured DNS can leak internal IPs or hostnames
  - Zone transfers can expose your entire DNS infrastructure when incorrectly configured
  - DNS is a critical infrastructure component often overlooked in security reviews
  - DNS misconfigurations can lead to domain hijacking
- **What to look for:** 
  - Exposed internal IP addresses in public DNS records
  - Outdated or forgotten subdomains pointing to vulnerable systems
  - Unintended information in TXT records (SPF, verification codes, API keys)
  - Successful zone transfers to unauthorized servers
  - Misaligned MX records that could lead to mail flow issues
  - Missing or misconfigured DMARC, SPF, or DKIM records
  - Inconsistencies between authoritative nameservers
  - Excessive TTL values or extremely low TTL values
- **Common DNS vulnerabilities:**
  - DNS Zone Transfer (AXFR) allowed to unauthorized hosts
  - DNS cache poisoning susceptibility 
  - Missing DNSSEC implementation
  - Subdomain takeover opportunities (orphaned DNS records)
  - Dangling CNAME records pointing to decommissioned services
  - DNS amplification vulnerabilities from misconfigured recursion
- **Remediation:** 
  - Restrict zone transfers to authorized IP addresses only
  - Implement DNSSEC to prevent spoofing and cache poisoning
  - Regularly audit all DNS records and remove unused entries
  - Secure DNS management interfaces with strong authentication
  - Implement SPF, DKIM, and DMARC for email security
  - Consider using DNS providers with built-in security features
  - Monitor for unexpected DNS changes that could indicate compromise
  - Use split-horizon DNS to separate internal and external DNS
  - Implement proper TTL values

## HTTP Headers
- **What it does:** Uses `curl` to fetch HTTP response headers and analyzes them for security best practices and misconfigurations.
- **Implementation details:** 
  - Makes HTTP requests with different user agents
  - Specifically identifies and analyzes security-related headers
  - Checks for information leakage in server headers
- **Why it matters:** 
  - HTTP headers form a critical part of web security controls
  - Proper security headers can prevent many common web attacks
  - Missing headers can make sites vulnerable to XSS, clickjacking, MIME sniffing
  - Server headers can leak sensitive version information
- **What to look for:** 

| **Security Header** | **Recommended Value** | **Purpose** | **Risk if Missing** |
|----------------|------------------|---------|----------------|
| Content-Security-Policy | `default-src 'self';` (tighten as needed) | Controls resources the browser can load | XSS vulnerabilities |
| X-Frame-Options | `DENY` or `SAMEORIGIN` | Prevents clickjacking attacks | UI redressing attacks |
| X-XSS-Protection | `1; mode=block` | Additional XSS protection for older browsers | XSS in legacy browsers |
| X-Content-Type-Options | `nosniff` | Prevents MIME type confusion | MIME confusion attacks |
| Strict-Transport-Security | `max-age=31536000; includeSubDomains` | Forces HTTPS connections | SSL stripping attacks |
| Referrer-Policy | `no-referrer` or `strict-origin-when-cross-origin` | Controls referrer information | Information leakage |
| Permissions-Policy | `geolocation=(), microphone=()` | Restricts browser features | Abuse of browser APIs |
| Cache-Control | `no-store, max-age=0` (for sensitive data) | Controls browser caching | Sensitive data exposure |
| Server | Minimal information or custom value | Hides server details | Information disclosure |
- **Common header vulnerabilities:**
  - Missing CSP allowing arbitrary script execution
  - Missing X-Frame-Options enabling clickjacking attacks
  - Verbose Server headers revealing exact versions
  - Missing HSTS headers allowing SSL stripping
- **Remediation:** 
  - Implement a comprehensive Content-Security-Policy
  - Add all recommended security headers
  - Configure web server to remove or obfuscate version information
  - Use HTTP security evaluation tools (like securityheaders.com)
  - Set appropriate caching policies for different content types

## Firewall Status
- **What it does:** Checks if a firewall is active and properly configured on the target system.
- **Implementation details:** Examines firewall configuration and rule sets for UFW, iptables, Windows Firewall, or other firewall solutions.
- **Why it matters:** 
  - Firewalls are the first line of defense for network security
  - Misconfigured firewalls give a false sense of security
  - Default configurations may not be sufficient
  - Firewall rules should follow the principle of least privilege
- **What to look for:** 
  - Firewall service status (active vs. disabled)
  - Default policies (should default to DROP or REJECT)
  - Overly permissive rules (any:any)
  - Rules allowing access to sensitive ports from public networks
  - Inconsistent or conflicting rules
  - Rules with no logging
  - Outdated or unused rules
- **Common firewall misconfigurations:**
  - Default ACCEPT policies
  - Allowing all outbound traffic without restrictions
  - Firewall enabled but with no effective rules
  - Rules that are too broad in scope
  - Rules ordered incorrectly (specific rules should precede general ones)
- **Remediation:** 
  - Ensure firewall is enabled at boot
  - Set default policies to DROP
  - Implement explicit rules for necessary services only
  - Restrict source IPs where possible
  - Enable logging for denied traffic
  - Regularly audit and clean up rule sets
  - Consider implementing both host and network firewalls

## User Privileges
- **What it does:** Lists users with sudo/admin rights and analyzes account security.
- **Implementation details:** Examines /etc/sudoers, local group membership, and user account properties.
- **Why it matters:** 
  - Administrative accounts are primary targets for attackers
  - Excessive privileges violate the principle of least privilege
  - Shared admin accounts reduce accountability
  - Inappropriate sudo configuration can lead to privilege escalation
- **What to look for:** 
  - Users with unexpected sudo/admin privileges
  - Default or system accounts with elevated privileges
  - Passwordless sudo configurations
  - Sudo configurations without command restrictions
  - Inactive accounts that still have privileges
  - Service accounts with interactive login capability
- **Common privilege issues:**
  - Too many users with full sudo access
  - Weak password policies for privileged accounts
  - Shared admin credentials
  - No audit trail for privileged commands
  - Misconfigured sudoers entries that allow escalation
- **Remediation:** 
  - Limit admin/sudo access to necessary personnel only
  - Use fine-grained sudo configurations (specific commands only)
  - Enable command logging for all privileged operations
  - Require password re-entry for sudo
  - Implement MFA for privileged accounts
  - Regularly audit admin group membership
  - Remove inactive accounts from privileged groups

## World-Writable Files
- **What it does:** Scans the filesystem for files or directories that are writable by any user on the system.
- **Implementation details:** Uses find commands to identify files with 777, 757, 775, or other world-writable permissions.
- **Why it matters:** 
  - World-writable files can be modified by any user, including attackers
  - They often lead to privilege escalation
  - Configuration files that are world-writable can be altered to introduce backdoors
  - Executable files that are world-writable can be replaced with malicious versions
- **What to look for:** 
  - System binaries or configuration files with incorrect permissions
  - World-writable directories in the PATH
  - World-writable startup scripts or cron jobs
  - Unexpected world-writable files outside of designated areas like /tmp
  - Files owned by privileged users but writable by all
  - SUID/SGID executables that are world-writable
- **Risk scenarios:**
  - Privilege escalation via writable SUID binaries
  - Persistence through modified startup scripts
  - Data exfiltration through altered logging configurations
  - Service hijacking by modifying configuration files
- **Remediation:** 
  - Correct permissions on system files (usually 644 for data, 755 for directories, 700 for sensitive files)
  - Use the sticky bit (1000) on shared directories like /tmp
  - Regularly audit file permissions
  - Use tools like AIDE or Tripwire to detect unexpected changes
  - Implement proper umask settings (022 or stricter)
  - Consider mandatory access controls (SELinux, AppArmor)

## SSH Configuration
- **What it does:** Reviews SSH server settings against security best practices.
- **Implementation details:** Analyzes /etc/ssh/sshd_config or equivalent for security parameters and compares against hardening guidelines.
- **Why it matters:** 
  - SSH is often exposed to the internet and a primary target
  - Default configurations are often too permissive
  - SSH provides direct system access, making it critical to secure
  - Brute force attacks against SSH are extremely common
- **What to look for:** 

| **SSH Configuration Parameter** | **Recommended Setting** | **Security Impact** | **Default Setting Risk** |
|----------------------------|---------------------|----------------|---------------------|
| PermitRootLogin | `no` | Prevents direct root access | 🔴 High |
| PasswordAuthentication | `no` | Requires key-based authentication | 🔴 High |
| PubkeyAuthentication | `yes` | Enables key-based authentication | 🟠 Medium |
| X11Forwarding | `no` | Prevents X11 session hijacking | 🟠 Medium |
| MaxAuthTries | `3` or `4` | Limits authentication attempts | 🟠 Medium |
| Protocol | `2` | Uses only secure SSH protocol version | 🔴 High |
| PermitEmptyPasswords | `no` | Prevents blank password usage | 🔴‼️ Critical |
| ClientAliveInterval | `300` (5 min) | Auto-disconnects idle sessions | 🟢 Low |
| ClientAliveCountMax | `3` | Number of checks before disconnecting | 🟢 Low |
| AllowUsers/AllowGroups | Specific users/groups | Restricts who can connect | 🟠 Medium |
| Banner | Custom without system info | Avoids information disclosure | 🟢 Low |
| ListenAddress | Specific IP(s) | Limits SSH access to specific interfaces | 🟠 Medium |
| LogLevel | `VERBOSE` | Increases logging detail | 🟢 Low |
| UsePAM | `yes` | Integrates with PAM for enhanced security | 🟠 Medium |
- **Common SSH vulnerabilities:**
  - Root login allowed with password authentication
  - SSH protocol 1 enabled (insecure)
  - Default port with no additional protection
  - Weak ciphers or MACs enabled
  - No login attempt limits
- **Remediation:** 
  - Configure key-based authentication only
  - Disable root login via SSH
  - Implement fail2ban or similar to prevent brute-forcing
  - Use strong ciphers only (remove weak ciphers)
  - Consider changing the default port (22)
  - Restrict SSH access to specific IPs where possible
  - Implement MFA for SSH access
  - Set appropriate timeout values

## Ping/Availability
- **What it does:** Uses ICMP echo (ping) to verify basic connectivity and measure latency to the target.
- **Implementation details:** Sends 4 ICMP echo requests and analyzes responses, with platform-specific commands for different operating systems.
- **Why it matters:** 
  - Establishes basic reachability
  - Measures latency which can impact service performance
  - Identifies packet loss which can indicate network issues
  - Some firewalls block ICMP, which can affect network diagnostics
- **What to look for:** 
  - Packet loss percentage
  - Average round-trip time
  - Consistent vs. varying latency
  - ICMP being completely blocked (could indicate firewall rules)
  - Unusual response patterns
- **Network insights from ping results:**
  - High latency might indicate network congestion or routing issues
  - Packet loss patterns can reveal intermittent connectivity problems
  - Varying response times may indicate route changes or load issues
- **Remediation:** 
  - For high latency: Investigate network routing and bandwidth
  - For packet loss: Check for network congestion or faulty equipment
  - For complete blocking: Consider allowing some ICMP for diagnostics
  - Document expected baseline ping results for comparison
  - Configure monitoring to alert on significant changes from baseline

---

# How to Use the App
The Public Server Scanner tool is designed to be user-friendly while providing deep security insights. Here's a detailed guide on how to use it effectively:

## Command-Line Usage

1. **Preparation**:
   - Ensure all prerequisites are installed (see the main README.md)
   - Verify you have necessary permissions (root/admin for some checks)
   - Make sure your target is reachable from your system

2. **Available Command-Line Options**:

| **Option** | **Format** | **Description** | **Example** |
|--------|--------|-------------|---------|
| Basic Usage | `python StartScan.py` | Runs the tool with interactive prompts | `python StartScan.py` |
| Target | `--target` | Specifies the server to scan | `--target example.com` |
| Checks | `--checks` | Comma-separated list of specific checks to run | `--checks portscan,headers,cert` |
| Output Directory | `--output-dir` | Custom location for results | `--output-dir ./my-scan-results` |
| Verbose | `--verbose` | Displays detailed progress information | `--verbose` |
| Help | `--help` | Displays available options and usage | `--help` |
| Version | `--version` | Displays the tool version | `--version` |
| Config | `--config` | Uses a custom configuration file | `--config my-config.json` |

3. **Common Usage Examples**:

```bash
# Basic interactive usage
python StartScan.py

# Scan a specific target with all checks
python StartScan.py --target example.com

# Run only specific security checks
python StartScan.py --target example.com --checks portscan,headers,cert

# Specify a custom output directory
python StartScan.py --target example.com --output-dir ./my-scan-results

# Run in verbose mode for more detailed output
python StartScan.py --target example.com --verbose
```

Once started, the tool will:
- Create an output directory for results
- Run selected checks sequentially
- Display progress in the terminal
- Generate a summary and detailed logs

## Technical Requirements

- **Permissions**: Some checks require elevated permissions:
  - Port scanning requires raw socket access
  - Filesystem checks need read access to system directories
  - Firewall status checks may require admin privileges
  
- **Network Access**:
  - Ensure your system can reach the target on required ports
  - Some networks may block scanning activities
  - Corporate firewalls may interfere with certain checks
  
- **Target Considerations**:
  - Always obtain permission before scanning systems you don't own
  - Some checks may generate significant traffic
  - Sensitive systems might need to be scanned during off-hours

- **Resource Usage**:
  - Comprehensive scans can use significant CPU and network bandwidth
  - Consider using the `--checks` option to limit scope for resource-constrained environments

---

# Understanding the Results

The Public Server Scanner tool provides results in multiple formats to help you easily identify and address security issues.

## Reading the Output

1. **Summary Report**:
   - Located at `[output-dir]/summary.txt`
   - Provides high-level overview of all findings
   - Includes count of issues by severity
   - Lists the most critical issues first

2. **Individual Check Logs**:
   - Located in the output directory with descriptive filenames
   - Contains raw output from the tools used
   - Includes detailed technical information
   - Useful for in-depth analysis

3. **Consolidated Report** (if generated):
   - HTML or PDF format comprehensive report
   - Organizes findings by category
   - Includes visualizations and statistics
   - Provides remediation recommendations

## Severity Levels

Results are categorized by severity to help prioritize remediation:

| **Severity Level** | **Color** | **Description** | **Response Time** | **Example Findings** | **Risk Level** |
|----------------|-------|-------------|---------------|------------------|------------|
| **Critical** ⚠️ | Red | Immediate security risk that could lead to system compromise | Same day | • World-writable system files<br>• Root login allowed via SSH with password<br>• Exposed admin interfaces<br>• Unpatched critical vulnerabilities | 🔴‼️ High |
| **Warning** ⚡ | Yellow | Potential security concern that deviates from best practices | Within 1-2 weeks | • Missing security headers<br>• Certificate expires soon<br>• Weak SSH configuration<br>• Unnecessary open ports | 🟠 Medium |
| **Info** ℹ️ | Blue | Informational finding that provides context but may not require action | As needed | • List of installed services<br>• Certificate details<br>• Detected user accounts<br>• Service version information | 🟢 Low |
| **OK** ✅ | Green | Passed security check, conforming to best practices | No action required | • Proper firewall configuration<br>• Strong SSH settings<br>• Up-to-date certificates<br>• Proper security headers | ✓ None |

Every finding in the report will include a severity indicator to help you prioritize remediation efforts. Always address Critical findings first, followed by Warning items, and then review Informational findings as needed.

Each finding includes:
- Description of the issue
- Technical details and evidence
- Security impact
- Recommended remediation steps
- References to security standards or best practices where applicable

---

# Example Output

Below are examples of what output from the Public Server Scanner tool typically looks like. This will help you understand how to interpret the results.

## Summary Output Example

```
==== PUBLIC SERVER SCANNER SUMMARY ====
Target: example.com (203.0.113.10)
Scan Date: 2023-06-15 14:30:22
Report ID: SSA-202306151430

FINDINGS SUMMARY:
[CRITICAL] Issues Found: 2
[WARNING] Issues Found: 3
[INFO] Items Detected: 8
[OK] Checks Passed: 7

CRITICAL ISSUES:
[!] World-writable files found in system directories (2 files)
[!] SSH allows password authentication and root login

WARNING ISSUES:
[!] Firewall: Inactive (Consider enabling UFW or similar)
[!] Security Headers: Missing Content-Security-Policy, X-Frame-Options
[!] Certificate expires in 15 days (2023-06-30)

DETAILED RESULTS:
[+] Open Ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3306 (MySQL)
[!] Firewall: Inactive (Consider enabling UFW or similar)
[+] Users with sudo: admin, sysop
[!] World-writable files: /var/www/html/uploads/config.php, /home/admin/script.sh
[!] SSH: Root login ENABLED, Password authentication ENABLED
[!] Security Headers: Missing Content-Security-Policy, X-Frame-Options
[!] Certificate: Expires in 15 days (2023-06-30)
[+] DNS: No issues found
[+] Ping: Server reachable, avg latency 24ms
[+] UDP Scan: No unauthorized UDP services found

NEXT STEPS:
1. Address CRITICAL issues immediately
2. Schedule remediation for WARNING items
3. Review detailed logs in the output directory
4. Re-scan after implementing changes
```

## Detailed Check Output Example (Port Scan)

```
# NMAP PORT SCAN RESULTS
# Target: example.com (203.0.113.10)
# Date: 2023-06-15 14:30:25

Starting Nmap 7.93 ( https://nmap.org )
Nmap scan report for example.com (203.0.113.10)
Host is up (0.024s latency).
Not shown: 996 filtered tcp ports (no-response)

PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3306/tcp open  mysql

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.23 seconds

# SECURITY ASSESSMENT:
# [WARNING] MySQL port (3306) exposed to public internet
# [INFO] Standard web ports (80,443) open as expected
# [INFO] SSH service available for remote administration
# 
# RECOMMENDATIONS:
# 1. Restrict MySQL port to internal network or specific IPs
# 2. Consider non-standard SSH port for reduced attack visibility
# 3. Verify all open ports are necessary for operations
```

## Detailed Check Output Example (Certificate Analysis)

```
# SSL/TLS CERTIFICATE DETAILS
# Target: example.com:443
# Date: 2023-06-15 14:31:05

Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 12345678 (0xbc614e)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = Let's Encrypt Authority X3, O = Let's Encrypt, C = US
        Validity
            Not Before: Mar 17 03:39:41 2023 GMT
            Not After : Jun 30 03:39:41 2023 GMT
        Subject: CN = example.com
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
            RSA Public Key: (2048 bit)
                Modulus: [...]
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Key Usage: critical
                Digital Signature, Key Encipherment
            X509v3 Extended Key Usage:
                TLS Web Server Authentication, TLS Web Client Authentication
            X509v3 Subject Alternative Name:
                DNS:example.com, DNS:www.example.com

# SECURITY ASSESSMENT:
# [WARNING] Certificate expires soon (15 days remaining)
# [INFO] Using secure signature algorithm (sha256WithRSAEncryption)
# [INFO] Key strength adequate (RSA 2048-bit)
# [INFO] Issued by trusted CA (Let's Encrypt)
# [OK] SAN includes common variants (www.example.com)
# 
# RECOMMENDATIONS:
# 1. Renew certificate immediately 
# 2. Consider implementing auto-renewal
# 3. Consider stronger key (4096-bit) for next renewal
```

---

# Best Practices for Public Servers

Public-facing servers require special attention to security due to their exposure to the internet. Following these best practices will significantly enhance your server's security posture:

## Network Security

1. **Firewall Configuration**
   - Implement a default-deny policy on all inbound traffic
   - Allow only necessary services and ports
   - Consider implementing egress filtering
   - Use both network and host-based firewalls
   - Configure rate limiting for services like SSH, SMTP, and web logins

2. **Network Segmentation**
   - Separate public-facing and internal systems
   - Use DMZ architecture for public services
   - Implement VLANs to isolate different types of traffic
   - Consider jump boxes for administrative access

3. **Encryption and Protocols**
   - Use TLS 1.2+ for all services
   - Disable legacy protocols (SSLv3, TLS 1.0/1.1)
   - Implement perfect forward secrecy
   - Use strong cipher suites
   - Enable DNSSEC for DNS servers

## System Security

1. **Access Control**
   - Implement principle of least privilege
   - Use key-based authentication for SSH
   - Enable multi-factor authentication where possible
   - Disable direct root logins
   - Implement account lockouts after failed attempts

2. **System Hardening**
   - Remove unnecessary packages and services
   - Disable unused kernel modules
   - Use minimal container/VM images where possible
   - Implement file integrity monitoring
   - Configure proper umask settings

3. **Update Management**
   - Establish regular patch schedule
   - Enable automatic security updates where appropriate
   - Subscribe to vendor security mailing lists
   - Test patches in staging before production
   - Maintain documented update procedures

## Application Security

1. **Web Application Security**
   - Implement all recommended security headers
   - Use content security policy (CSP)
   - Validate all input and sanitize output
   - Protect against common web vulnerabilities (OWASP Top 10)
   - Use web application firewalls where appropriate

2. **Database Security**
   - Use parameterized queries to prevent SQL injection
   - Minimize database user privileges
   - Encrypt sensitive data at rest
   - Regularly audit database access
   - Use strong authentication for database access

3. **API Security**
   - Implement proper authentication mechanisms
   - Rate limit API endpoints
   - Validate all API input
   - Use TLS for all API traffic
   - Implement appropriate CORS policies

## Monitoring and Response

1. **Logging and Monitoring**
   - Centralize logs with a SIEM solution
   - Monitor for unusual activity
   - Set up alerts for critical events
   - Establish baselines for normal behavior
   - Retain logs for an appropriate duration (90+ days)

2. **Incident Response**
   - Develop and document incident response plans
   - Run regular tabletop exercises
   - Establish roles and responsibilities
   - Include communication procedures
   - Document lessons learned from incidents

3. **Backup and Recovery**
   - Implement 3-2-1 backup strategy (3 copies, 2 different media, 1 offsite)
   - Regularly test backup restoration
   - Encrypt backup data
   - Document recovery procedures
   - Set appropriate RPO/RTO objectives

---

# Remediation & Hardening Tips

When your security audit reveals issues, here's how to approach remediation:

## Immediate Actions

1. **Critical Vulnerabilities**
   - Address any findings marked as "Critical" immediately
   - Mitigate exposure by restricting access if immediate fixes aren't possible
   - Document temporary workarounds and their limitations
   - Perform targeted re-testing after remediation
   - Consider notification to stakeholders if systems were at risk

2. **Access Control Issues**
   - Reset compromised credentials
   - Remove unnecessary administrative privileges
   - Disable unused accounts
   - Implement required password policy changes
   - Review and correct file/folder permissions

3. **Exposed Services**
   - Close unnecessary ports immediately
   - Implement proper firewall rules
   - Move sensitive services behind VPN/bastion hosts
   - Disable vulnerable protocol versions
   - Remove or secure unnecessary services

## Short-term Improvements

1. **Patch Management**
   - Apply missing security updates
   - Update end-of-life software to supported versions
   - Implement a systematic approach to future updates
   - Establish vulnerability scanning schedule
   - Document exceptions with compensating controls

2. **Configuration Hardening**
   - Apply secure configuration templates (CIS Benchmarks)
   - Implement proper HTTP security headers
   - Enhance SSH security settings
   - Configure appropriate TLS settings
   - Disable unnecessary features and modules

3. **Authentication Enhancements**
   - Implement multi-factor authentication
   - Enforce strong password policies
   - Deploy key-based authentication where possible
   - Review and update access control lists
   - Implement session timeout policies

## Long-term Security Strategy

1. **Security Architecture**
   - Review overall network architecture
   - Implement defense-in-depth strategies
   - Consider zero-trust security model
   - Document security requirements for future systems
   - Integrate security into development lifecycle

2. **Monitoring and Detection**
   - Deploy intrusion detection/prevention systems
   - Implement log aggregation and analysis
   - Set up automated alerting for security events
   - Consider threat hunting capabilities
   - Establish security operations processes

3. **Process Improvements**
   - Develop formal security policies
   - Implement regular security testing
   - Conduct security awareness training
   - Establish change management procedures
   - Create incident response playbooks

## Common Security Vulnerabilities

Understanding common vulnerabilities helps prioritize your security efforts:

| **Vulnerability Category** | **Specific Vulnerability** | **Mitigation Strategy** | **Risk Level** | **Detection Method** |
|----------------------|----------------------|---------------------|-----------|-----------------|
| **Injection Attacks** | SQL Injection | • Validate all input<br>• Use parameterized queries<br>• Apply least privilege DB accounts<br>• Implement WAF | Critical | • Static code analysis<br>• Dynamic testing<br>• Web scanner tools |
| | Command Injection | • Avoid system calls with user input<br>• Implement strict allowlists<br>• Use library functions instead of shell | Critical | • Code review<br>• Penetration testing |
| | Cross-Site Scripting (XSS) | • Implement Content Security Policy<br>• Sanitize user input<br>• Encode output<br>• Use modern frameworks | High | • Web vulnerability scanners<br>• Browser developer tools |
| **Authentication Weaknesses** | Brute Force Attacks | • Implement account lockouts<br>• Rate limiting<br>• CAPTCHA<br>• Multi-factor authentication | High | • Log analysis<br>• IDS alerts |
| | Insecure Password Storage | • Use strong hashing (bcrypt, Argon2)<br>• Add unique salts<br>• Implement password policies | Critical | • Code review<br>• Database inspection |
| | Session Management | • Use secure cookies<br>• Implement proper timeouts<br>• Regenerate IDs after login<br>• Validate session source | High | • Proxy interception tools<br>• Session analysis |
| **Access Control Flaws** | Insecure Direct Object References | • Implement proper authorization checks<br>• Use indirect references<br>• Verify user ownership | High | • Manual testing<br>• Authorization testing tools |
| | Missing Function-Level Access | • Verify permissions at server side<br>• Consistent access control model<br>• Principle of least privilege | High | • Code review<br>• Penetration testing |
| | Privilege Escalation | • Regular permission audits<br>• Limit sudo access<br>• Implement separation of duties | Critical | • System auditing tools<br>• Log analysis |
| **Cryptographic Failures** | Weak Algorithms | • Use modern encryption standards<br>• Stay updated on deprecated methods<br>• Regular crypto reviews | High | • Configuration scanning<br>• SSL/TLS testing tools |
| | Poor Key Management | • Implement proper key rotation<br>• Secure key storage<br>• Use hardware security modules | High | • Security audits<br>• Configuration review |
| | Insufficient TLS Protection | • Configure TLS properly<br>• Disable older protocols<br>• Implement HSTS | High | • SSL/TLS scanners<br>• Browser security tools |
| **Server Misconfigurations** | Default Settings | • Change default credentials<br>• Remove sample files<br>• Alter default ports | Medium | • Configuration scanners<br>• Penetration testing |
| | Information Disclosure | • Disable verbose errors<br>• Remove version info<br>• Configure proper headers | Medium | • Web scanners<br>• Manual inspection |
| | Directory Listing | • Disable in web server config<br>• Implement proper .htaccess<br>• Use web.config settings | Medium | • Web vulnerability scanners |
| | Unnecessary Services | • Remove unneeded components<br>• Disable unused services<br>• Regular service audits | High | • System scanners<br>• Port scanners |

---

## Customization and Extension

The Public Server Scanner tool is designed to be modular and extensible, allowing you to tailor it to your specific security needs.

## Customizing Existing Checks

Many checks can be customized through configuration settings:

1. **Port Scan Configuration**
   - Custom port ranges for focused scanning
   - Timing options for balancing speed and stealth
   - Service version detection depth
   - Custom Nmap scripts for specialized tests

2. **Directory Brute-Force Customization**
   - Custom wordlists for industry-specific targets
   - Rate limiting to avoid overwhelming target servers
   - Custom file extensions to check (.php, .jsp, etc.)
   - Recursive scanning depth configuration

3. **Output Customization**
   - HTML report generation
   - JSON output for integration with other tools
   - Report severity thresholds
   - Custom report templates

## Adding New Security Checks

You can extend the tool with your own security checks:

1. **Creating a New Check Module**
   - Add a new Python file in the `app/checks/` directory
   - Implement a function that accepts `target` and `output_dir` parameters
   - Return `True` for success or `False` for failure
   - Register the check in `app/core.py` by adding it to `get_available_checks()`

2. **Example: Simple Web Screenshot Check**
   ```python
   # app/checks/screenshot.py
   import os
   from app.utils import run_command
   
   def web_screenshot(target: str, output_dir: str) -> bool:
       """Capture a screenshot of the target website."""
       if not target.startswith('http'):
           target = f"http://{target}"
           
       output_file = os.path.join(output_dir, "screenshot.png")
       cmd = f"wkhtmltoimage --quality 75 {target} {output_file}"
       return run_command(cmd, os.path.join(output_dir, "screenshot_log.txt"))
   ```

3. **Integration with External Tools**
   - Wrapper functions for commercial security scanners
   - API integrations with threat intelligence services
   - Custom checks for compliance requirements (PCI DSS, HIPAA, etc.)
   - Industry-specific security tests

## Advanced Configuration

The tool supports various advanced configuration options:

1. **Configuration File Structure**
   - Located at `~/.config/serveraudit/config.json` by default
   - JSON format for easy editing
   - Supports environment-specific configurations
   
   Example basic configuration:
   ```json
   {
     "default_scan": "full",
     "output_dir": "/var/log/serveraudit"
   }
   ```

2. **Scan Configuration**
   - Settings for different scan types and tool parameters
   
   Example scan configuration:
   ```json
   {
     "nmap": {
       "tcp_options": "-sS -Pn --top-ports 1000",
       "service_options": "-sV -sC -p22,80,443,8080,3389",
       "udp_options": "-sU --top-ports 20"
     },
     "scan_threads": 2,
     "report_format": "html",
     "custom_checks": ["webscreen", "sslscan"]
   }
   ```

3. **Environment Variables**
   - `SERVERAUDIT_CONFIG`: Override default config path
   - `SERVERAUDIT_OUTPUT`: Default output directory
   - `SERVERAUDIT_DEBUG`: Enable verbose logging

**Configuration Options Reference:**

- `scan_threads`: Number of parallel threads for scanning (1-10). ⚠️ Higher values may trigger IDS/IPS
- `tcp_options`: Nmap TCP scan parameters (e.g., `-sS -Pn --top-ports 1000`)
- `service_options`: Service detection parameters (e.g., `-sV -sC -p22,80,443`)
- `udp_options`: UDP scan parameters (e.g., `-sU --top-ports 20`). Note: UDP scans are slower
- `report_format`: Output report format (`html`, `json`, `text`, `xml`). HTML provides best readability
- `custom_checks`: Additional modules to run (e.g., `["webscreen", "sslscan"]`). Defined in `app/checks/`
- `timeout`: Maximum time for checks in seconds (e.g., `300`). Default is module-specific
- `retry_count`: Attempts before failing a check (e.g., `3`). Helps with unreliable networks

## Tips for Effective Use

Getting the most out of your security scans requires proper planning and follow-through. Here are practical tips for maximizing the effectiveness of the Public Server Scanner tool:

| **Best Practice Category** | **Recommendations** | **Benefits** | **Implementation Complexity** |
|----------------------|-----------------|----------|--------------------------|
| **Establish a Regular Schedule** | • Conduct monthly audits for critical systems<br>• Perform quarterly audits for less critical systems<br>• Schedule additional audits after significant changes<br>• Automate recurring audits where possible | • Ensures consistent security posture<br>• Helps identify new vulnerabilities quickly<br>• Establishes security patterns over time<br>• Meets compliance requirements | Medium |
| **Prepare for Scanning** | • Document test scope and objectives<br>• Obtain proper authorization before scanning<br>• Notify stakeholders if scans might affect production<br>• Schedule intensive scans during low-traffic periods<br>• Create a baseline for comparison | • Prevents misunderstandings<br>• Minimizes operational disruption<br>• Provides context for result interpretation<br>• Establishes clear expectations | Low |
| **Prioritize and Track Issues** | • Address Critical findings first, then High, Medium, and Low<br>• Create tickets for each security issue found<br>• Set realistic remediation deadlines based on risk<br>• Track remediation progress over time<br>• Verify fixes with targeted rescans | • Focuses resources on highest risks<br>• Ensures accountability<br>• Provides metrics for security improvements<br>• Validates remediation effectiveness | Medium |
| **Extend Your Security Program** | • Combine with vulnerability scanning tools (Nessus, OpenVAS)<br>• Use alongside web application security tools (OWASP ZAP, Burp Suite)<br>• Incorporate findings into broader risk assessments<br>• Use results to inform security architecture decisions<br>• Support compliance requirements with audit documentation | • Provides comprehensive security coverage<br>• Identifies vulnerabilities across systems<br>• Informs strategic security decisions<br>• Simplifies compliance reporting | High |
| **Continuous Improvement** | • Review scan configurations after each audit<br>• Adjust check parameters based on your environment<br>• Consider adding custom checks for your specific needs<br>• Update tool dependencies regularly<br>• Contribute improvements back to the project | • Enhances detection capabilities<br>• Reduces false positives<br>• Keeps security tests current<br>• Improves overall security posture | Medium |

---

## Security Tools Reference

The Public Server Scanner tool integrates with and complements many popular security tools. Understanding these tools helps you interpret results and extend your security testing:

## Network Security Tools

- [nmap](https://nmap.org/): Powerful network discovery and security scanning tool
  - **Key Features**: SYN/TCP/UDP scanning, service detection, OS fingerprinting, NSE script engine, flexible timing options
  - **Installation**: `apt install nmap` / `brew install nmap` 
  - **Example Command**: `nmap -sV -sC -p- -T4 --script vuln target.com`

- [hping3](http://www.hping.org/): Advanced packet crafting tool
  - **Key Features**: Custom packet creation, advanced scanning techniques, firewall testing, TCP/IP stack analysis
  - **Installation**: `apt install hping3` / `brew install hping`
  - **Example Command**: `hping3 -S -p 80 -c 5 target.com`

- [masscan](https://github.com/robertdavidgraham/masscan): Fast port scanner for large networks
  - **Key Features**: Asynchronous operation, high-speed scanning, Internet-scale scanning, similar syntax to nmap
  - **Installation**: `apt install masscan` / `brew install masscan`
  - **Example Command**: `masscan -p0-65535 --rate=10000 target.com`
  
- [netcat](http://netcat.sourceforge.net/): Versatile networking utility
  - **Key Features**: TCP/UDP connections, port scanning, banner grabbing, file transfer, listening mode
  - **Installation**: `apt install netcat` / `brew install netcat`
  - **Example Command**: `nc -v -z target.com 20-30`

Documentation:
* nmap: `man nmap` or https://nmap.org/book/
* hping3: `man hping3` or http://wiki.hping.org/
* masscan: `man masscan` or GitHub page
* netcat: `man nc` or https://nc110.sourceforge.io/

## Web Application Security

- [gobuster](https://github.com/OJ/gobuster): Directory and file brute-forcing tool
  - **Primary Use**: Discovering hidden content on web servers
  - **Key Features**: Directory/file enumeration, DNS subdomain brute-forcing, fast scan capabilities, custom wordlist support, multi-threaded scanning
  - **Installation**: `apt install gobuster` / `brew install gobuster`
  - **Example Command**: `gobuster dir -u https://target.com -w wordlist.txt -t 50`

- [curl](https://curl.se/): Command-line tool for transferring data
  - **Primary Use**: Testing HTTP responses, headers, and APIs
  - **Key Features**: Support for many protocols, verbose output, header manipulation, cookie handling, certificate inspection
  - **Installation**: Pre-installed on most systems
  - **Example Command**: `curl -I -v -H "User-Agent: Mozilla" https://target.com`

- [OWASP ZAP](https://www.zaproxy.org/): Web application security scanner
  - **Primary Use**: Dynamic application security testing
  - **Key Features**: Automated scanning, proxy functionality, API availability, active/passive scanning, scripting support
  - **Installation**: Download from website or package manager
  - **Example Command**: `curl -s "http://localhost:8090/JSON/spider/action/scan/?url=https://target.com"`

- [Nikto](https://cirt.net/Nikto2): Web server scanner
  - **Primary Use**: Checks web servers for dangerous files, outdated software
  - **Key Features**: Comprehensive checks, plugin architecture, SSL support, scan tuning options, integration with other tools
  - **Installation**: `apt install nikto` / `brew install nikto`
  - **Example Command**: `nikto -h https://target.com -ssl -Tuning 9`

Documentation:
* gobuster: `gobuster -h` or project README
* curl: `man curl` or https://curl.se/docs/manpage.html
* OWASP ZAP: https://www.zaproxy.org/docs/
* Nikto: `man nikto` or https://cirt.net/Nikto2

## SSL/TLS Security

- [openssl](https://www.openssl.org/): Cryptography and SSL/TLS toolkit
  - **Primary Use**: Certificate analysis, cipher testing
  - **Key Features**: Certificate operations, cipher testing, key management, protocol checking, cryptographic functions
  - **Installation**: Pre-installed on most systems
  - **Example Command**: `openssl s_client -connect target.com:443 -showcerts`

- [sslyze](https://github.com/nabla-c0d3/sslyze): SSL/TLS configuration analyzer
  - **Primary Use**: In-depth TLS/SSL configuration analysis
  - **Key Features**: Certificate validation, cipher suite analysis, protocol support detection, Heartbleed testing, TLS extensions support
  - **Installation**: `pip install --upgrade sslyze`
  - **Example Command**: `sslyze --regular target.com:443`

- [testssl.sh](https://github.com/drwetter/testssl.sh): SSL/TLS testing script
  - **Primary Use**: Tests TLS/SSL encryption
  - **Key Features**: Encryption tests, vulnerability checks, colorized output, detailed reporting, multiple protocol testing
  - **Installation**: `git clone https://github.com/drwetter/testssl.sh.git`
  - **Example Command**: `./testssl.sh --severity HIGH --full target.com`

Documentation:
* openssl: `man openssl` or https://www.openssl.org/docs/
* sslyze: Project GitHub page at https://github.com/nabla-c0d3/sslyze
* testssl.sh: Project GitHub page at https://github.com/drwetter/testssl.sh

## DNS Security

- [dig](https://linux.die.net/man/1/dig): DNS lookup utility
  - **Primary Use**: DNS record queries, zone transfer testing
  - **Key Features**: Detailed DNS resolution, tracing capability, custom DNS server queries, multiple record type support, query timing statistics
  - **Installation**: `apt install dnsutils` / `brew install bind`
  - **Example Command**: `dig @8.8.8.8 target.com ANY +noall +answer`

- [dnsenum](https://github.com/fwaeytens/dnsenum): DNS enumeration tool
  - **Primary Use**: Domain reconnaissance, subdomain discovery
  - **Key Features**: DNS record enumeration, Google scraping, brute force capabilities, reverse lookups, network range scanning
  - **Installation**: `apt install dnsenum` / `brew install dnsenum`
  - **Example Command**: `dnsenum --enum target.com`

- [dnsrecon](https://github.com/darkoperator/dnsrecon): DNS reconnaissance tool
  - **Primary Use**: Advanced DNS enumeration and cache snooping
  - **Key Features**: Zone transfers, record enumeration, multiple query types, cache snooping, subdomain dictionary attacks
  - **Installation**: `pip install dnsrecon`
  - **Example Command**: `dnsrecon -d target.com -D subdomains.txt -t brt`

Documentation:
* dig: `man dig` or https://linux.die.net/man/1/dig
* dnsenum: Project GitHub page at https://github.com/fwaeytens/dnsenum
* dnsrecon: Project GitHub page at https://github.com/darkoperator/dnsrecon

## System Security

- [ufw](https://help.ubuntu.com/community/UFW): Uncomplicated Firewall for Linux
  - **Primary Use**: Firewall management, rule configuration
  - **Key Features**: Simple iptables interface, application profiles, protocol-specific rules, default deny/allow policies, logging capabilities
  - **Installation**: `apt install ufw` (pre-installed on Ubuntu)
  - **Example Command**: `ufw allow from 192.168.1.0/24 to any port 22`

- [fail2ban](https://www.fail2ban.org/): Intrusion prevention system
  - **Primary Use**: Protection against brute force attacks
  - **Key Features**: Log monitoring, automated banning, custom filters, multiple action responses, rule configurability
  - **Installation**: `apt install fail2ban` / `brew install fail2ban`
  - **Example Usage**: Create custom jail in `/etc/fail2ban/jail.local`

- [Lynis](https://cisofy.com/lynis/): Security auditing tool for Unix/Linux systems
  - **Primary Use**: Comprehensive system hardening
  - **Key Features**: Security scanning, compliance testing, vulnerability detection, security best practices, detailed reporting
  - **Installation**: `apt install lynis` / `brew install lynis`
  - **Example Command**: `lynis audit system --quick`

- [rkhunter](https://rkhunter.sourceforge.net/): Rootkit scanner
  - **Primary Use**: Checks for rootkits, backdoors, and local exploits
  - **Key Features**: Filesystem scans, known exploit detection, property checking, system binaries verification, backdoor detection
  - **Installation**: `apt install rkhunter` / `brew install rkhunter`
  - **Example Command**: `rkhunter --check --skip-keypress`

Documentation:
* ufw: `man ufw` or https://help.ubuntu.com/community/UFW
* fail2ban: https://www.fail2ban.org/wiki/index.php/Main_Page
* Lynis: https://cisofy.com/documentation/lynis/
* rkhunter: `man rkhunter` or https://rkhunter.sourceforge.net/

## Vulnerability Management

- [OpenVAS](https://www.openvas.org/): Open-source vulnerability scanner
  - **Primary Use**: Comprehensive vulnerability assessment
  - **Key Features**: Network scanning, vulnerability detection, detailed reporting, scheduled scans, web interface
  - **Installation**: Available as Docker container
  - **Example Usage**: Accessible via web interface

- [Nuclei](https://github.com/projectdiscovery/nuclei): Vulnerability scanner
  - **Primary Use**: Template-based vulnerability scanning
  - **Key Features**: Community templates, fast scanning, customizable workflows, low false positives, integration options
  - **Installation**: `brew install nuclei` / `GO111MODULE=on go get -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei`
  - **Example Command**: `nuclei -t cves/ -target https://target.com`

- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/): Software composition analysis
  - **Primary Use**: Identifies vulnerable components in applications
  - **Key Features**: Multiple language support, detailed reporting, integration options, NIST NVD integration, CI/CD compatibility
  - **Installation**: Download from website
  - **Example Command**: `dependency-check --scan /path/to/application --out /path/to/reports`

Documentation:
* OpenVAS: https://www.openvas.org/
* Nuclei: Project GitHub page at https://github.com/projectdiscovery/nuclei
* OWASP Dependency-Check: https://owasp.org/www-project-dependency-check/

---

# Glossary

Understanding security terminology is crucial for interpreting audit results effectively:

| **Term** | **Definition** | **Related Concepts** | **Appears In Report Sections** |
|------|-----------|-----------------|----------------------------|
| **Attack Surface** | The sum of all points (attack vectors) where an unauthorized user can attempt to enter or extract data from a system. | Exposure, Attack Vectors, Surface Reduction | Port Scan, Service Detection |
| **Attack Vector** | A specific path or method that an attacker uses to gain unauthorized access to a system. | Vulnerability, Exploit, Entry Point | All Sections |
| **Brute-Force Attack** | A trial-and-error method used to obtain information such as passwords or directory names by systematically trying all possible combinations. | Dictionary Attack, Password Cracking | SSH Configuration, Account Security |
| **CVE (Common Vulnerabilities and Exposures)** | A system that provides reference identifiers for publicly known security vulnerabilities. | Vulnerability Database, Security Advisory | Service Detection, Version Analysis |
| **Defense in Depth** | A security strategy that employs multiple layers of defense mechanisms to protect assets. | Layered Security, Multiple Controls | Security Recommendations |
| **DMZ (Demilitarized Zone)** | A network segment that contains and exposes an organization's external-facing services to the internet while protecting the internal network. | Network Segmentation, Firewall | Network Configuration |
| **Enumeration** | The process of gathering information about a target system to identify potential attack vectors. | Reconnaissance, Information Gathering | Port Scan, Service Detection |
| **Hardening** | The process of securing a system by reducing its vulnerability or attack surface by removing unnecessary functionality and configuring security settings. | Secure Configuration, Lockdown | Security Recommendations |
| **Lateral Movement** | The techniques attackers use to move deeper into a network after gaining initial access. | Privilege Escalation, Pivoting | Security Recommendations |
| **Least Privilege** | A security principle of providing users with the minimum levels of access necessary to complete their job functions. | Need-to-know, Access Control | Account Security, Filesystem Permissions |
| **MITM (Man-in-the-Middle)** | An attack where the attacker secretly relays and possibly alters communications between two parties. | Eavesdropping, Traffic Interception | SSL/TLS Analysis, Network Security |
| **OWASP (Open Web Application Security Project)** | A nonprofit foundation that works to improve software security through community-led open-source projects. | Web Security, Top 10 Vulnerabilities | Web Application Security |
| **Penetration Testing** | An authorized simulated attack performed to evaluate the security of a system. | Security Assessment, Ethical Hacking | Methodology |
| **Privilege Escalation** | The act of exploiting a bug, design flaw, or configuration oversight to gain elevated access to resources that should be protected. | Vertical/Horizontal Escalation | Account Security, Filesystem Permissions |
| **SIEM (Security Information and Event Management)** | Systems that provide real-time analysis of security alerts generated by applications and network hardware. | Log Management, Security Monitoring | Security Recommendations |
| **TLS (Transport Layer Security)** | Cryptographic protocol designed to provide secure communications over a computer network. | Encryption, SSL, HTTPS | SSL/TLS Analysis |
| **Vulnerability** | A weakness that can be exploited by an attacker to compromise system security. | Exposure, Risk, Exploit | All Sections |
| **WAF (Web Application Firewall)** | A firewall that monitors, filters, and blocks HTTP traffic to and from a web application. | Application Security, HTTP Filtering | Web Application Security |
| **World-Writable** | File or directory permissions that allow any user on the system to write to or modify the file. | File Permissions, Security Misconfiguration | Filesystem Permissions |
| **Zero-day** | A previously unknown vulnerability being exploited before a patch is available. | 0day, Unpatched Vulnerability | Security Recommendations |
| **Zone Transfer** | DNS operation that replicates DNS records from a primary DNS server to secondary servers; can leak internal information if improperly configured. | DNS Security, Information Disclosure | DNS Analysis |

---

# FAQ

## General Questions

| **Question** | **Answer** |
|---------|--------|
| **Can I use this tool on internal/private servers?** | Yes, the tool is suitable for both internal and public-facing servers. However, always ensure you have proper authorization before scanning any system, and be aware that some checks may generate significant traffic. |
| **Will this tool make changes to my server?** | No, the Public Server Scanner tool is designed as a read-only assessment tool. It does not modify system configurations or make changes to your server. All operations are non-intrusive. |
| **How often should I run security audits?** | For critical systems, monthly audits are recommended. Less critical systems should be audited at least quarterly. Additionally, run audits after significant system changes, upgrades, or before moving systems to production. |

## Technical Questions

| **Question** | **Answer** |
|---------|--------|
| **What if a check fails or returns an error?** | First, check the detailed logs for error messages. Common causes include missing dependencies, insufficient permissions, or network restrictions. You can re-run individual checks with the `--checks` parameter after resolving the issue. |
| **Can the tool audit multiple servers simultaneously?** | The current version audits one server at a time. For multiple servers, consider creating a wrapper script that calls the tool sequentially or implements parallel execution. |
| **How resource-intensive are the scans?** | Resource usage varies by check. Port scans and directory brute-forcing are the most intensive. On production systems, consider running these checks during off-hours or use the `--checks` option to select less intensive checks. |
| **Does the tool work on cloud-hosted servers?** | Yes, but be aware that some cloud providers have policies against security scanning without prior notification. Some providers might also block scanning traffic. Check your provider's terms of service and security policies before scanning. |
| **Can I integrate this tool with my CI/CD pipeline?** | Yes, the tool can be integrated into CI/CD pipelines. Use exit codes to determine success/failure, and consider using the JSON output option (if available) for easier parsing by other tools. |

## Security Concerns

| **Question** | **Answer** |
|---------|--------|
| **Is using this tool detectable by intrusion detection systems?** | Yes, many checks (especially port scanning and directory brute-forcing) generate traffic patterns that may trigger IDS/IPS systems. Always coordinate with security teams before scanning production environments. |
| **Can I safely run this tool against production systems?** | The tool is designed to be non-disruptive, but intensive checks like comprehensive port scanning or directory brute-forcing can potentially impact performance. Consider testing during off-hours or on staging environments first. |
| **How does this compare to commercial security scanners?** | This tool focuses on common server security misconfigurations and exposures. Commercial scanners often include vulnerability databases and more extensive checks. Consider this tool as complementary to, not a replacement for, comprehensive vulnerability scanners like Nessus or Qualys. |

---

# Need Help?

We're committed to helping you use this tool effectively and improve your server security posture.

## Getting Support

If you have questions about specific findings or how to resolve them, please:

1. **Check the Documentation First**: Many common questions are already answered in this document or the README.

2. **Open an Issue**: If you need further assistance, open an issue on the [GitHub repository](https://github.com/ar4ntic/PublicServerScanner/issues) with:
   - A clear description of your question or problem
   - Relevant sections of your output (with sensitive information removed)
   - Your operating system and tool version
   - Any steps you've already tried

3. **Security Concerns**: For sensitive security matters, consider contacting the maintainers directly rather than posting in public issues.

## Contributing

This tool improves with community involvement. Consider contributing by:

- Reporting bugs or suggesting features via GitHub issues
- Submitting pull requests for improvements or new checks
- Sharing your success stories or use cases
- Helping others in the community by answering questions

## Additional Resources

For further learning about server security, consider these resources:

- [OWASP Security Practices](https://owasp.org/www-project-web-security-testing-guide/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Mozilla Server Side TLS Guidelines](https://wiki.mozilla.org/Security/Server_Side_TLS)

---

**Stay secure and keep auditing!**
