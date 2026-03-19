```
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓                                                                            ▓
▓    ███████╗██╗  ██╗██╗██╗   ██╗ █████╗                                    ▓
▓    ██╔════╝██║  ██║██║██║   ██║██╔══██╗                                   ▓
▓    ███████╗███████║██║██║   ██║███████║                                   ▓
▓    ╚════██║██╔══██║██║╚██╗ ██╔╝██╔══██║                                   ▓
▓    ███████║██║  ██║██║ ╚████╔╝ ██║  ██║                                   ▓
▓    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝  v2.0                           ▓
▓                                                                            ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

         ॐ  THE COSMIC DESTROYER OF VULNERABILITIES  ॐ
    ▓▒░ AdiscLabs  |  @Aditya Bhosale  |  ॐ नमः शिवाय ॐ  ░▒▓
```

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-red?style=for-the-badge&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/Version-2.0-darkred?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**The Third Eye opens. Every port is revealed. Nothing is hidden.**

*Inspired by Lord Shiva — The Hindu God of Destruction and Transformation*

</div>

---

## ॐ What is SHIVA?

**SHIVA** (Scanner for Host Introspection, Vulnerability Analysis) is an advanced network port scanner written from scratch in Python. Named after the Hindu God of Destruction, SHIVA channels the power of Shiva's **Third Eye** — the all-seeing eye that perceives what is hidden — to expose every open port, service, banner, and vulnerability on a target network.

Unlike basic scanners, SHIVA combines:
- **750+ service fingerprints** with intelligent detection
- **6 scan modes** from quick recon to full aggressive analysis
- **CVE-mapped vulnerability intel** for 40+ critical services
- **SSL/TLS certificate inspection** built-in
- **OS detection** via TTL analysis
- **CIDR subnet scanning** for entire network ranges
- **JSON export** for reporting and integration

> ⚠️ **SHIVA is for authorized security testing ONLY. Only scan systems you own or have explicit written permission to test. Unauthorized scanning is illegal in most jurisdictions.**

---

## 🔱 The Shiva Symbolism

Every element of SHIVA is inspired by Lord Shiva:

| Symbol | Shiva Meaning | SHIVA Tool Meaning |
|--------|---------------|--------------------|
| **Third Eye (तृतीय नेत्र)** | Sees beyond illusion, burns ignorance | Scans beyond firewalls, reveals hidden services |
| **Trishul (त्रिशूल)** | Trident destroying past, present, future | Three-phase scan: detect, fingerprint, exploit |
| **Vasuki (वासुकी)** | King cobra — deadly but controlled | Payload probes that extract service banners |
| **Neelakantha (नीलकण्ठ)** | Blue throat — consumed poison for others | Absorbs network noise to find signal |
| **Nataraja (नटराज)** | Cosmic dance of destruction & creation | The scanning dance — methodical destruction of ignorance |
| **Rudra (रुद्र)** | The Howler, fierce destroyer | Aggressive mode — tears through all defenses |
| **Ganga (गंगा)** | Sacred river flowing from Shiva's hair | Data stream flowing from target to analyst |
| **OM (ॐ)** | The primordial sound, beginning of all | The first packet sent — the beginning of the scan |

---

## 🚀 Installation

### Requirements

```bash
Python 3.8 or higher
pip install rich          # For colored terminal output (recommended)
```

### Quick Install

```bash
# Clone or download
git clone https://github.com/adisclabs/shiva   # or download shiva.py directly

# Install dependency
pip install rich

# Make executable (Linux/macOS)
chmod +x shiva.py

# Run
python3 shiva.py --help
```

### Optional: Add to PATH (Linux/macOS)

```bash
sudo cp shiva.py /usr/local/bin/shiva
sudo chmod +x /usr/local/bin/shiva

# Now run from anywhere
shiva -t 192.168.1.1 --mode vuln
```

---

## ⚡ Quick Start

```bash
# See the full help + banner
python3 shiva.py --help

# Basic scan of a single host
python3 shiva.py -t 192.168.1.1

# Vulnerability scan
python3 shiva.py -t 192.168.1.1 --mode vuln

# Full aggressive scan with banner grabbing
python3 shiva.py -t 192.168.1.1 --mode aggressive

# Scan your entire local subnet
python3 shiva.py -t 192.168.1.0/24 -p top100 --mode quick

# Save results to JSON
python3 shiva.py -t myserver.com --mode full -o report.json
```

---

## 📖 Complete Usage Reference

```
python3 shiva.py -t TARGET [OPTIONS]
```

### Arguments

| Flag | Long Form | Description | Default |
|------|-----------|-------------|---------|
| `-t` | `--target` | Target IP, hostname, CIDR, or comma-separated list | **Required** |
| `-p` | `--ports` | Port specification (see formats below) | `top1000` |
| | `--mode` | Scan mode (see modes below) | `quick` |
| | `--threads` | Number of concurrent threads | `300` |
| | `--timeout` | Socket timeout in seconds | `1.0` |
| `-o` | `--output` | Save results to JSON file | — |
| | `--no-color` | Disable rich colour output | — |
| `-h` | `--help` | Show help menu and exit | — |
| `-v` | `--version` | Show version and exit | — |

---

## 🎯 Scan Modes

### `quick` — The Scout
> Fastest mode. Pure TCP connect scan. No banner grabbing or extra probes.

```bash
python3 shiva.py -t 192.168.1.1 --mode quick
```
- TCP connect scan on specified ports
- Identifies open / closed / filtered state
- Service name lookup from database
- Risk level classification
- OS hint via TTL

**Best for:** Initial reconnaissance, subnet sweeps, time-sensitive scans

---

### `full` — The Investigator
> Complete scan with banner grabbing, version detection, UDP probing, and SSL info.

```bash
python3 shiva.py -t 192.168.1.1 --mode full
```
- Everything in `quick` mode
- Banner grabbing on all open ports
- Version string extraction (Apache, nginx, OpenSSH, MySQL, etc.)
- UDP scan on key ports (DNS/53, NTP/123, SNMP/161, etc.)
- SSL/TLS certificate info (CN, expiry, cipher, TLS version)

**Best for:** Thorough host enumeration, service inventory

---

### `stealth` — The Shadow
> Evades IDS/IPS by randomising port order and introducing timing jitter.

```bash
python3 shiva.py -t 192.168.1.1 --mode stealth --threads 50 --timeout 2
```
- Port scan order randomised (not sequential 1,2,3...)
- Slower pacing to stay below threshold-based alerts
- Reduces signature of pattern-based detection
- Recommended: lower threads (50-100) and higher timeout (2-3s)

**Best for:** Avoiding detection during authorized red team engagements

---

### `banner` — The Reader
> Aggressive banner grabbing with multiple probe types per service.

```bash
python3 shiva.py -t 192.168.1.1 --mode banner
```
- Everything in `full` mode
- Multiple banner probe payloads tried per port
- Extended read timeout to catch slow responders
- Deep version string extraction with 20+ regex patterns
- Catches services that don't respond to generic probes

**Best for:** Service version enumeration before exploit research

---

### `vuln` — The Hunter
> Full scan plus CVE-mapped vulnerability intelligence for every open service.

```bash
python3 shiva.py -t 192.168.1.1 --mode vuln
```
- Everything in `full` mode
- Vulnerability hints per open port from built-in CVE database
- Covers 40+ critical services with specific CVE references
- Risk prioritisation: CRITICAL > HIGH > MEDIUM > LOW
- Flags known default-credential and no-authentication services

**Best for:** Security audits, pentest prep, vulnerability assessment

---

### `aggressive` — The Destroyer (Rudra Mode)
> Maximum information gathering. Everything SHIVA has.

```bash
python3 shiva.py -t 192.168.1.1 --mode aggressive
```
- Everything in `vuln` mode
- SSL/TLS deep inspection on ALL potentially TLS ports
- Maximum banner probe coverage
- All UDP probes
- Highest information density output

**Best for:** Full security assessment, CTF, authorized penetration testing

---

## 🗂️ Port Formats

| Format | Description | Example |
|--------|-------------|---------|
| Single port | One specific port | `-p 80` |
| Comma list | Multiple specific ports | `-p 22,80,443,3306,6379` |
| Range | Inclusive port range | `-p 1-1000` |
| `top100` | Top 100 well-known ports | `-p top100` |
| `top1000` | Top 1000 ports (default) | `-p top1000` |
| `vuln` | High-risk ports only | `-p vuln` |
| `all` | All 65535 ports | `-p all` |

> **Tip for `all`:** Use `--threads 1000 --timeout 0.5` for speed:
> ```bash
> python3 shiva.py -t 192.168.1.1 -p all --threads 1000 --timeout 0.5
> ```

---

## 🎯 Target Formats

```bash
# Single IP
python3 shiva.py -t 192.168.1.1

# Hostname
python3 shiva.py -t myserver.com

# CIDR subnet (scans all hosts in range)
python3 shiva.py -t 192.168.1.0/24

# Multiple targets (comma-separated)
python3 shiva.py -t 192.168.1.1,192.168.1.2,192.168.1.50

# Mix of formats
python3 shiva.py -t 10.0.0.1,10.0.0.0/29,myserver.local
```

---

## 🚨 Risk Levels

SHIVA classifies every open port by risk level:

| Level | Color | Criteria | Examples |
|-------|-------|----------|---------|
| `CRITICAL` | 🔴 Red | Known unauthenticated access, default creds, direct RCE surface | Redis, MongoDB, Docker API, Telnet, Memcached |
| `HIGH` | 🟠 Orange | Well-known services on standard ports | SSH, FTP, SMB, RDP, MySQL |
| `MEDIUM` | 🟡 Yellow | Services on non-standard ports (1024–7999) | Custom apps, alternate HTTP |
| `LOW` | 🟢 Green | Services on high ports | Dev servers, metrics endpoints |

---

## 🧠 Vulnerability Intelligence

In `vuln` and `aggressive` mode, SHIVA surfaces known CVEs and security issues per service. Examples:

| Port | Service | Intel |
|------|---------|-------|
| 22 | SSH | OpenSSH username enumeration (CVE-2018-15473), cipher weakness check |
| 23 | Telnet | CRITICAL — cleartext credentials, instant MitM |
| 445 | SMB | EternalBlue (MS17-010), EternalRomance, SMBv1 check |
| 3389 | RDP | BlueKeep (CVE-2019-0708), DejaBlue (CVE-2019-1181) |
| 6379 | Redis | Unauthenticated access → arbitrary code execution, SSH key injection |
| 9200 | ElasticSearch | No-auth data exposure, dynamic scripting RCE |
| 2375 | Docker API | No TLS = full host compromise trivial |
| 8009 | AJP | Apache Ghostcat (CVE-2020-1938) |
| 27017 | MongoDB | Default no-auth in older versions |
| 11211 | Memcached | No auth + UDP amplification (50,000x DDoS factor) |
| 502 | Modbus | ICS/SCADA — zero authentication on industrial systems |

---

## 📊 Output Format

### Terminal Output

```
─────────────────── SHIVA · 192.168.1.100 [192.168.1.100] ──────────────────
  OS: Linux / Unix / macOS (TTL=64)  Open: 5  Closed: 995  Time: 3.2s

  Port   Proto  State   Service        Risk       RTT     Version / Banner
  ─────────────────────────────────────────────────────────────────────────
  22     TCP    open    SSH            HIGH       12ms    OpenSSH 8.9p1 Ubuntu
  80     TCP    open    HTTP           HIGH       8ms     Apache/2.4.52
  443    TCP    open    HTTPS          HIGH       9ms     CN=myserver.com | TLS=TLSv1.3
  3306   TCP    open    MYSQL          HIGH       11ms    MySQL 8.0.33
  6379   TCP    open    REDIS          CRITICAL   6ms     Redis 7.0.5

  VULNERABILITY INTEL

  PORT 6379 / REDIS
    [CRIT]  Redis — unauthenticated access allows arbitrary code execution
    [CRIT]  Redis SLAVEOF can write files to disk (SSH key injection)
```

### JSON Output (`-o report.json`)

```json
[
  {
    "target": "192.168.1.100",
    "ip": "192.168.1.100",
    "hostname": "myserver.local",
    "os_hint": "Linux / Unix / macOS (TTL=64)",
    "ttl": 64,
    "scan_time": 3.21,
    "timestamp": "2026-03-19T11:30:00",
    "open_ports": [
      {
        "port": 22,
        "state": "open",
        "protocol": "TCP",
        "service": "SSH",
        "description": "Secure Shell",
        "risk": "HIGH",
        "response_ms": 12.3,
        "version": "OpenSSH 8.9p1 Ubuntu",
        "banner": "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6",
        "ssl_info": "",
        "vuln_hints": ["[INFO] Check cipher suites: avoid arcfour, 3des-cbc"]
      }
    ]
  }
]
```

---

## 💡 Usage Examples

### Scenario 1: Quick network inventory
```bash
# Scan entire /24 subnet for common services
python3 shiva.py -t 192.168.1.0/24 -p top100 --mode quick --threads 500
```

### Scenario 2: Full audit of a web server
```bash
# Aggressive scan of a web server with vuln intel
python3 shiva.py -t mywebserver.com -p 1-10000 --mode aggressive -o webserver_audit.json
```

### Scenario 3: Check only known dangerous ports
```bash
# Quick check of high-risk ports only
python3 shiva.py -t 192.168.1.1 -p vuln --mode vuln
```

### Scenario 4: Thorough database server check
```bash
# Scan database-relevant ports
python3 shiva.py -t 10.0.0.50 -p 1433,1521,3306,5432,6379,27017,9200 --mode vuln
```

### Scenario 5: Stealth red team recon
```bash
# Low and slow — evade detection
python3 shiva.py -t 10.0.0.1 -p top1000 --mode stealth --threads 30 --timeout 3
```

### Scenario 6: Full port sweep (all 65535)
```bash
# Maximum coverage — be patient
python3 shiva.py -t 192.168.1.1 -p all --threads 1000 --timeout 0.5 -o full_sweep.json
```

### Scenario 7: Multiple hosts with report
```bash
# Scan multiple targets and save combined report
python3 shiva.py -t 10.0.0.1,10.0.0.2,10.0.0.10 --mode vuln -o multi_host_report.json
```

### Scenario 8: No color (for logging/piping)
```bash
# Clean output for log files or piping
python3 shiva.py -t 192.168.1.1 --no-color --mode full | tee scan.log
```

---

## 🛡️ Understanding Output

### Port States

| State | Meaning |
|-------|---------|
| `open` | Port is accepting connections. Service is running. |
| `closed` | Port responded with RST — host is up but nothing running there. |
| `filtered` | No response / ICMP unreachable — firewall likely blocking. |
| `open\|filtered` | UDP — could not determine definitively. |

### OS Detection

SHIVA uses ICMP ping TTL values to estimate the OS family:

| TTL Range | OS Hint |
|-----------|---------|
| 1 – 64 | Linux / Unix / macOS / Android |
| 65 – 128 | Windows (NT/XP/7/10/11/Server) |
| 129 – 255 | Network Device (Cisco/Juniper/Solaris/HP) |

> Note: TTL decrements with each hop. A TTL of 57 from 7 hops away = original TTL of 64 = Linux.

---

## ⚙️ Performance Tuning

### Thread Count Guidelines

| Scenario | Threads | Timeout | Notes |
|----------|---------|---------|-------|
| Single host, quick | 300 | 1.0s | Default — good balance |
| Single host, all ports | 1000 | 0.5s | Fast sweep |
| Subnet scan | 200 | 1.0s | Avoid overwhelming network |
| Stealth scan | 30–50 | 2–3s | Low and slow |
| Cloud target (high latency) | 100 | 2.0s | Compensate for RTT |

### Speed vs Accuracy Trade-off

```bash
# Fastest (may miss filtered ports)
--threads 1000 --timeout 0.3

# Balanced (default)
--threads 300 --timeout 1.0

# Most accurate (slower)
--threads 100 --timeout 3.0
```

---

## 📁 File Structure

```
shiva.py              ← Single file, no dependencies except `rich`
report.json           ← Optional JSON output (generated when -o is used)
```

SHIVA is intentionally a single-file tool. No config files, no databases, no installation beyond `pip install rich`.

---

## 🆚 SHIVA vs nmap — Key Differences

| Feature | SHIVA | nmap |
|---------|-------|------|
| Language | Python — readable, modifiable | C — fast, compiled |
| Service DB | 750+ entries, custom | 10,000+ entries |
| Vuln intel | Built-in 40+ CVE hints | Via NSE scripts |
| SSL inspection | Built-in | Via scripts |
| Output | Rich terminal + JSON | Multiple formats |
| Setup | `pip install rich` | System package |
| Customisable | Full Python source | C/Lua scripts |
| Root required | No (TCP connect) | Yes (SYN scan) |
| Learning value | High — read the source | Black box |

> SHIVA's advantage is that it is **100% readable Python** — you can understand every probe, every decision, every output line. It's designed to be learned from, not just run.

---

## ⚖️ Legal Notice

```
╔══════════════════════════════════════════════════════════════╗
║                      LEGAL WARNING                          ║
║                                                              ║
║  Scanning systems you do not own or have explicit written    ║
║  permission to test is ILLEGAL in most countries worldwide.  ║
║                                                              ║
║  This includes:                                              ║
║    • The Computer Fraud and Abuse Act (CFAA) — USA           ║
║    • Computer Misuse Act — UK                                ║
║    • IT Act 2000 — India                                     ║
║    • Similar laws in EU, Australia, and most nations         ║
║                                                              ║
║  SHIVA is intended ONLY for:                                 ║
║    • Your own systems and networks                           ║
║    • Systems with explicit written authorization             ║
║    • Authorized CTF challenges and lab environments          ║
║    • Security research with proper disclosure                ║
║                                                              ║
║  The authors (AdiscLabs / @Aditya Bhosale) are NOT           ║
║  responsible for any misuse of this tool.                    ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🙏 Credits & Acknowledgements

```
╔══════════════════════════════════════╗
║   DEVELOPED BY                       ║
║   AdiscLabs                          ║
║   @Aditya Bhosale                    ║
╠══════════════════════════════════════╣
║   SHIVA v2.0                         ║
║   The Destroyer of Vulnerabilities   ║
║   ॐ नमः शिवाय                        ║
╚══════════════════════════════════════╝
```

**Inspired by:** Lord Shiva — the Hindu god of destruction, transformation, and the cosmic dance of creation and annihilation.

**Built with:**
- Python 3.8+ standard library (`socket`, `ssl`, `threading`, `concurrent.futures`)
- [Rich](https://github.com/Textualize/rich) — beautiful terminal output

**Concept inspired by:** nmap, masscan, rustscan — but written from scratch to be fully understandable and extensible.

---

*"The Third Eye opens. Every port is revealed. Nothing is hidden."*

*ॐ नमः शिवाय — Har Har Mahadev*
