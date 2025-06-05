# Lierre - Advanced Dork Scanner

Lierre is a Python-based tool for discovering potential SQL injection and XSS vulnerabilities in websites using Google dorks. It searches for URLs via Bing, filters them based on specific patterns, and tests for vulnerabilities with predefined payloads. Features include proxy support, randomized User-Agents, and domain blacklisting to avoid irrelevant or high-profile sites.

## Features
- **Dork-Based Scanning**: Queries Bing to find URLs matching user-defined dorks.
- **Vulnerability Detection**: Tests URLs for SQL injection and XSS vulnerabilities.
- **Proxy Integration**: Supports HTTP/HTTPS proxies for anonymized scanning.
- **User-Agent Rotation**: Randomizes User-Agent headers to evade detection.
- **Blacklist Filtering**: Skips domains like google.com and patterns like login pages.
- **Error Logging**: Records errors to a log file for troubleshooting.
- **Result Export**: Saves scan results and vulnerable URLs to a text file.

## Requirements
- Python 3.6 or later
- Python packages:
  - `requests`
  - `beautifulsoup4`
  - `colorama`

## Installation
1. **Clone or Download**:
   ```bash
   git clone
   https://github.com/lierree/Advanced-Dork-Scanner
   cd Advanced-Dork-Scanner
   ```

2. **Install Dependencies**:
   ```bash
   pip install requests beautifulsoup4 colorama
   ```

3. **Set Up Input Files**:
   - Create `dorks.txt` in the same directory as `scanner.py`, listing one dork per line (e.g., `inurl:login.php`).
   - (Optional) Create `proxies.txt` with one proxy per line (e.g., `http://proxy:port`).

## Usage
1. **Run the Tool**:
   ```bash
   python scanner.py
   ```

2. **Respond to Prompts**:
   - **Use proxy? (yes/no)**: Type `yes` to use proxies from `proxies.txt`, or `no` to skip.
   - **Select scan type (sql/xss)**: Enter `sql` for SQL injection tests or `xss` for XSS tests.

3. **Output**:
   - URLs and vulnerabilities are shown in the console.
   - Results, including dorks and vulnerable URLs with payloads, are saved to `results.txt`.
   - Errors are logged to `errors.log`.

## Example
```bash
$ python scanner.py
Lierre - Advanced Dork Scanner
MIT License. See LICENSE for details.
Use proxy? (yes/no): no
Select scan type (sql/xss): sql
[*] Loaded 3 dorks from dorks.txt.
[*] Scanning dork: inurl:login.php
[+] http://example.com/login.php?id=1
[!] SQL vuln: http://example.com/login.php?id=1 [']
[*] Results for 'inurl:login.php' saved to 'results.txt'. Vulnerable URLs: 1
```

## File Structure
- `scanner.py`: Core script for scanning and vulnerability testing.
- `dorks.txt`: Input file for dork queries (one per line).
- `proxies.txt`: (Optional) Input file for proxy addresses (one per line).
- `results.txt`: Output file for scan results.
- `errors.log`: Log file for errors.

## Configuration
- **Dorks**: Edit `dorks.txt` to customize queries. Example:
  ```plaintext
  inurl:login.php
  inurl:admin.asp
  inurl:search.jsp
  ```
- **Proxies**: Add proxies to `proxies.txt` (e.g., `http://proxy:port`).
- **Blacklist**: Update `blacklist_domains` and `blacklist_patterns` in `scanner.py` to filter domains or URLs.
- **Payloads**: Modify `sql_payloads` and `xss_payloads` in `scanner.py` for custom injection tests.

## Troubleshooting
- **SyntaxWarning: invalid escape sequence '\ '**: Check for stray `\ ` in code or files; replace with `\\ ` or fix.
- **Syntax Errors**: Verify parentheses and f-strings in `scanner.py` are correct.
- **No Results**: Ensure `dorks.txt` exists with valid queries and check internet/proxy settings.
- **Colorama Issues**: Confirm `colorama` is installed and `init(autoreset=True)` is in the script.

## Disclaimer
Lierre is for ethical security research and educational purposes only. The author is not liable for misuse or damage caused by this tool. Always obtain explicit permission before scanning or testing any system.
