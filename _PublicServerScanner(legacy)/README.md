# PublicServerScanner

A comprehensive, cross-platform security assessment tool for public-facing servers. This Python applic### macOS

1. Install [Python 3.8+](https://www.python.org/downloads/) if not already installed (macOS usually comes with Python, but you may want to upgrade).
2. Download the main script and requirements file:

   ```sh
   wget https://github.com/ar4ntic/PublicServerScanner/raw/main/StartScan.py
   wget https://github.com/ar4ntic/PublicServerScanner/raw/main/requirements-dev.txt
   wget -r -np -nH --cut-dirs=2 https://github.com/ar4ntic/PublicServerScanner/raw/main/app/ vulnerability scanning and security scanning processes to identify misconfigurations and vulnerabilities in internet-exposed systems. Designed for security professionals, system administrators, and DevOps engineers who need an efficient way to evaluate their external attack surface.

## Features

- **External Attack Surface Analysis**: Comprehensive port scanning to identify exposed services
- **Web Security Assessment**: Checks HTTP security headers and tests for directory brute-force vulnerabilities
- **TLS Security**: Analyzes SSL/TLS certificates for vulnerabilities and misconfigurations
- **Network Security**: Reviews firewall status and configuration to prevent unauthorized access
- **Remote Access Security**: Evaluates SSH configuration for hardening compliance
- **DNS Security**: Examines DNS configuration to prevent information leakage and zone transfer attacks
- **System Security**: Lists users with sudo/admin privileges and detects world-writable files
- **Actionable Reporting**: Provides clear recommendations prioritized by security impact
- **Non-Invasive**: Performs read-only operations that won't disrupt your production systems
- **Cross-Platform**: Works on Linux, Windows, and macOS with minimal dependencies

## Why Use This Tool?

Public Server Scanner is specifically tailored for internet-facing systems where security vulnerabilities can lead to significant breaches. It functions as both a vulnerability scanner and security scanner, identifying misconfigurations and security weaknesses in externally accessible services. Security professionals use this tool to:

- Discover exposed services and potentially vulnerable endpoints
- Assess TLS/SSL configuration and certificate validity
- Identify risky server configurations before attackers can exploit them  
- Generate comprehensive reports for security compliance and remediation
- Schedule automated security posture assessments

The tool works on Linux, Windows, and macOS, requiring only Python 3.8+ and is designed to be integrated into your security operations workflow.

## Documentation

For comprehensive information about the tool, security checks, best practices, and remediation strategies, refer to our detailed [documentation](documentation.md). The documentation includes:

- In-depth explanations of each security check
- Implementation details and technical background
- Common vulnerabilities and their remediation
- Best practices for server hardening
- Detailed usage instructions and command examples
- Advanced configuration options
- Security terminology glossary
- Troubleshooting guide and FAQs

## Prerequisites

Before running Public Server Scanner, you need Python 3.8 or newer.

- Some security checks require external command-line tools such as `nmap`, `curl`, `dig`, `openssl`, etc. Please ensure these are installed and available in your system PATH for full functionality.
  - On macOS, you can install most tools with Homebrew, e.g.:
    ```sh
    brew install nmap curl dig openssl
    ```
  - On Windows, you may need to download and install these tools separately (see their official websites).
- An active internet connection is recommended for certain checks.
- For best results, run the tool with administrator/root privileges.

### Windows
1. Download the latest Python 3 installer from the [official website](https://www.python.org/downloads/windows/).
2. Run the installer. **Important:** On the first screen, check the box that says "Add Python to PATH" before clicking "Install Now".
3. Complete the installation.

### macOS
1. Open Terminal.
2. Check if Python 3 is already installed:
   ```sh
   python3 --version
   ```
   If you see a version number (e.g., `Python 3.9.7`), you are ready to go.
3. If not installed, install Homebrew (if you don't have it):
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
4. Install Python 3:
   ```sh
   brew install python
   ```
5. Verify installation:
   ```sh
   python3 --version
   ```

### Verifying Python Installation (All Platforms)
To check if Python is installed and available in your PATH, run:
```sh
python --version
```
or
```sh
python3 --version
```
If you see a version number 3.8 or higher, you are ready to proceed.

## Installation

You can install and run the Public Server Scanner app without cloning the entire repository. Simply download the latest version of the app using `wget` or `curl`.

### Windows

1. Install [Python 3.8+](https://www.python.org/downloads/) if not already installed.
2. Download the main script and requirements file:

   ```sh
   wget https://github.com/ar4ntic/PublicServerScanner/raw/main/StartScan.py
   wget https://github.com/ar4ntic/PublicServerScanner/raw/main/requirements-dev.txt
   wget -r -np -nH --cut-dirs=2 https://github.com/ar4ntic/PublicServerScanner/raw/main/app/
   ```
   Or use `curl`:
   ```sh
   curl -O https://github.com/ar4ntic/PublicServerScanner/raw/main/StartScan.py
   curl -O https://github.com/ar4ntic/PublicServerScanner/raw/main/requirements-dev.txt
   # Download the app directory as needed
   ```

3. (Optional) Create and activate a virtual environment:

   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install dependencies:

   ```sh
   pip install -r requirements-dev.txt
   ```

5. Run the scan:

   ```sh
   python StartScan.py
   ```

### macOS

1. Install [Python 3.8+](https://www.python.org/downloads/) if not already installed (macOS usually comes with Python, but you may want to upgrade).
2. Download the main script and requirements file:

   ```sh
   wget https://github.com/ar4ntic/PublicServerScanner/raw/main/StartScan.py
   wget https://github.com/ar4ntic/PublicServerScanner/raw/main/requirements-dev.txt
   wget -r -np -nH --cut-dirs=2 https://github.com/ar4ntic/PublicServerScanner/raw/main/app/
   ```
   Or use `curl`:
   ```sh
   curl -O https://github.com/ar4ntic/PublicServerScanner/raw/main/StartScan.py
   curl -O https://github.com/ar4ntic/PublicServerScanner/raw/main/requirements-dev.txt
   # Download the app directory as needed
   ```

3. (Optional) Create and activate a virtual environment:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:

   ```sh
   pip install -r requirements-dev.txt
   ```

5. Run the scan:

   ```sh
   python3 StartScan.py
   ```

## Troubleshooting

- **Permission Denied**: Try running the script as an administrator (Windows) or with `sudo` (macOS) for full access to system checks.
- **Module Not Found**: Ensure all dependencies are installed with `pip install -r requirements-dev.txt`.
- **Python Not Found**: Make sure Python 3.8 or newer is installed and available in your system PATH.
- **Download Issues**: If `wget` or `curl` is not available, you can manually download the files from the GitHub web interface.
- **Virtual Environment Issues**: If you have trouble activating the virtual environment, check your Python installation and consult the [Python venv documentation](https://docs.python.org/3/library/venv.html).
- **Scan Errors**: For detailed troubleshooting of specific security checks, refer to the [comprehensive documentation](documentation.md#faq).

## Support

If you encounter issues or have suggestions, please:

1. Check the [comprehensive documentation](documentation.md) for answers to common questions and troubleshooting tips.
2. Review the [FAQ section](documentation.md#faq) for solutions to frequently encountered issues.
3. If you still need help, open an issue on the [GitHub repository](https://github.com/ar4ntic/PublicServerScanner/issues) with details about your problem.

## Notes

- For best results, run the script with administrator/root privileges.
- The tool is intended for educational and informational purposes only.
- Before scanning production systems, please review the [documentation](documentation.md#best-practices-for-public-servers) for best practices.
- See the [comprehensive documentation](documentation.md) for detailed information on interpreting results and implementing security improvements.

## License

See [LICENSE](LICENSE).

## Acknowledgements

This tool makes use of the following open-source projects and resources:

- **SecLists** ([danielmiessler/SecLists](https://github.com/danielmiessler/SecLists)) — for common wordlists used in directory brute-forcing and security checks.
- **nmap** ([nmap.org](https://nmap.org/)), **nikto**, **sslscan**, **gobuster**, **dig**, **openssl**, **curl** — external command-line tools used for various security checks (see requirements in the tool).
- **pytest**, **pytest-mock**, **pytest-cov** — for testing and code coverage.
- **flake8**, **black**, **isort**, **mypy**, **pylint** — for code quality, linting, and formatting.
- **bandit**, **safety** — for security analysis of Python code and dependencies.
- **tox** — for test automation.
- **sphinx** and related plugins — for documentation generation.

Special thanks to the maintainers and contributors of these projects for their valuable work.

---

**Found a bug? Have a feature request?** Please open an [issue](https://github.com/ar4ntic/PublicServerScanner/issues)!