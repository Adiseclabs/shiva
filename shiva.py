#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
#   SHIVA Port Scanner v2.0  —  Inspired by the Hindu God of Destruction
#   The Destroyer of Vulnerabilities | The Third Eye of Network Vision
#   AdiscLabs | @Aditya Bhosale
#   For authorized use on your own systems ONLY
# ═══════════════════════════════════════════════════════════════════════════════

import socket, struct, sys, time, random, ipaddress, argparse
import threading, concurrent.futures, json, re, os, ssl, hashlib
import subprocess, platform
from datetime import datetime
from typing import Optional
from queue import Queue

try:
    from rich.console import Console
    from rich.table   import Table
    from rich.panel   import Panel
    from rich.text    import Text
    from rich         import box
    from rich.columns import Columns
    from rich.rule    import Rule
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

console = Console() if HAS_RICH else None

# ─── SHIVA ASCII ART LOGO ────────────────────────────────────────────────────
# Inspired by Lord Shiva: Trishul, Third Eye, Crescent Moon, Vasuki Cobra,
# Rudra (The Howler), Nataraja (Cosmic Dancer), Neelakantha (Blue Throat)
# Aggressive hacker-style aesthetic — The Destroyer of Vulnerabilities

# Banner lines stored separately so print_logo can colour each segment precisely
# Line format: (text, style_hint)
#   style_hint: "title" | "trishul" | "meta" | "quote" | "dim"
SHIVA_BANNER_LINES = [
    # top rule
    ("───────────────────────────────────────────────────────────────", "rule"),
    # trishul — the trident, minimal 3-spike glyph
    ("                   |     |     |                               ", "trishul"),
    ("                   |     |     |                               ", "trishul"),
    ("    ───────────────┼─────┼─────┼───────────────                ", "trishul"),
    ("              ☽   🔱  S H I V A  🔱   ☾                       ", "title"),
    ("    ───────────────┼─────┼─────┼───────────────                ", "trishul"),
    ("                         |                                      ", "trishul"),
    ("                    🐍 VASUKI 🐍                                ", "meta"),
    # bottom rule
    ("───────────────────────────────────────────────────────────────", "rule"),
    # tag line
    ("  v2.0  ·  Port Scanner  ·  AdiscLabs  ·  @Aditya Bhosale      ", "dim"),
    ("  ॐ नमः शिवाय  ·  The Third Eye opens. Nothing is hidden.      ", "dim"),
    ("───────────────────────────────────────────────────────────────", "rule"),
]

SHIVA_QUOTES = [
    "  \" I am Death, the destroyer of worlds. \"  — Bhagavad Gita",
    "  \" Shiva's third eye burns away all ignorance. \"",
    "  \" The Trishul strikes past, present, and future. \"",
    "  \" Har Har Mahadev — every vulnerability shall fall. \"",
    "  \" What Shiva destroys, He destroys for good. \"",
]

# ─── SERVICE DATABASE (750+ entries) ─────────────────────────────────────────
SERVICE_DB = {
    1:   ("TCPMUX",     "TCP Port Multiplexer",           "default"),
    7:   ("ECHO",       "Echo Protocol",                  "default"),
    9:   ("DISCARD",    "Discard Protocol",               "default"),
    11:  ("SYSTAT",     "Active Users",                   "default"),
    13:  ("DAYTIME",    "Daytime Protocol",               "default"),
    17:  ("QOTD",       "Quote of the Day",               "default"),
    19:  ("CHARGEN",    "Character Generator",            "default"),
    20:  ("FTP-DATA",   "FTP Data Transfer",              "ftp"),
    21:  ("FTP",        "File Transfer Protocol",         "ftp"),
    22:  ("SSH",        "Secure Shell",                   "ssh"),
    23:  ("TELNET",     "Telnet (CLEARTEXT!)",            "telnet"),
    25:  ("SMTP",       "Mail Transfer",                  "smtp"),
    37:  ("TIME",       "Time Protocol",                  "default"),
    43:  ("WHOIS",      "WHOIS Lookup",                   "default"),
    49:  ("TACACS",     "TACACS Auth",                    "default"),
    53:  ("DNS",        "Domain Name System",             "dns"),
    67:  ("DHCP",       "DHCP Server",                    "dhcp"),
    68:  ("DHCP",       "DHCP Client",                    "dhcp"),
    69:  ("TFTP",       "Trivial FTP (UDP)",              "tftp"),
    70:  ("GOPHER",     "Gopher Protocol",                "default"),
    79:  ("FINGER",     "Finger Protocol",                "default"),
    80:  ("HTTP",       "Web Server",                     "http"),
    81:  ("HTTP-ALT",   "Alternate HTTP",                 "http"),
    88:  ("KERBEROS",   "Kerberos Auth",                  "kerberos"),
    102: ("ISO-TSAP",   "ISO TSAP",                       "default"),
    110: ("POP3",       "Mail Retrieval",                 "pop3"),
    111: ("RPCBIND",    "RPC Portmapper",                 "rpc"),
    113: ("IDENT",      "Auth/Ident",                     "default"),
    119: ("NNTP",       "Network News",                   "nntp"),
    123: ("NTP",        "Network Time Protocol",          "ntp"),
    135: ("MSRPC",      "MS RPC Endpoint Mapper",         "rpc"),
    137: ("NETBIOS-NS", "NetBIOS Name Service",           "netbios"),
    138: ("NETBIOS-DG", "NetBIOS Datagram",               "netbios"),
    139: ("NETBIOS-SS", "NetBIOS/SMB Session",            "smb"),
    143: ("IMAP",       "Internet Mail Access",           "imap"),
    161: ("SNMP",       "Network Management (UDP)",       "snmp"),
    162: ("SNMPTRAP",   "SNMP Trap",                      "snmp"),
    177: ("XDMCP",      "X Display Manager",              "default"),
    179: ("BGP",        "Border Gateway Protocol",        "bgp"),
    194: ("IRC",        "Internet Relay Chat",            "irc"),
    220: ("IMAP3",      "IMAP v3",                        "imap"),
    264: ("BGMP",       "BGP Multicast",                  "bgp"),
    389: ("LDAP",       "Directory Services",             "ldap"),
    443: ("HTTPS",      "Secure Web Server (TLS)",        "https"),
    444: ("SNPP",       "Simple Network Paging",          "default"),
    445: ("SMB",        "Server Message Block",           "smb"),
    465: ("SMTPS",      "Secure SMTP",                    "smtp"),
    500: ("ISAKMP",     "IPSec VPN IKE",                  "vpn"),
    502: ("MODBUS",     "ICS/SCADA Modbus",               "ics"),
    503: ("INTRINSA",   "Intrinsa",                       "default"),
    512: ("REXEC",      "Remote Exec (CLEARTEXT)",        "default"),
    513: ("RLOGIN",     "Remote Login (CLEARTEXT)",       "default"),
    514: ("SYSLOG",     "System Logging (UDP)",           "syslog"),
    515: ("LPD",        "Line Printer Daemon",            "printer"),
    520: ("RIP",        "Routing Info Protocol",          "routing"),
    523: ("IBM-DB2",    "IBM DB2",                        "database"),
    524: ("NCP",        "NetWare Core Protocol",          "default"),
    543: ("KLOGIN",     "Kerberos Login",                 "kerberos"),
    544: ("KSHELL",     "Kerberos Shell",                 "kerberos"),
    548: ("AFP",        "Apple File Protocol",            "default"),
    554: ("RTSP",       "Streaming Media",                "rtsp"),
    587: ("SMTP-SUB",   "Mail Submission",                "smtp"),
    593: ("HTTP-RPC",   "HTTP RPC Endpoint",              "rpc"),
    631: ("IPP",        "Internet Printing Protocol",     "ipp"),
    636: ("LDAPS",      "Secure LDAP",                    "ldap"),
    646: ("LDP",        "Label Distribution",             "routing"),
    873: ("RSYNC",      "Remote Sync",                    "rsync"),
    902: ("VMWARE",     "VMware ESXi",                    "vmware"),
    993: ("IMAPS",      "Secure IMAP",                    "imap"),
    995: ("POP3S",      "Secure POP3",                    "pop3"),
    1080:("SOCKS",      "SOCKS Proxy",                    "proxy"),
    1099:("JMXRMI",     "Java JMX RMI",                   "java"),
    1194:("OPENVPN",    "OpenVPN",                        "vpn"),
    1433:("MSSQL",      "Microsoft SQL Server",           "database"),
    1434:("MSSQL-UDP",  "MSSQL Browser (UDP)",            "database"),
    1521:("ORACLE",     "Oracle Database",                "database"),
    1522:("ORACLE",     "Oracle DB Alt",                  "database"),
    1604:("CITRIX",     "Citrix ICA",                     "remote"),
    1701:("L2TP",       "L2TP VPN",                       "vpn"),
    1723:("PPTP",       "PPTP VPN",                       "vpn"),
    1812:("RADIUS",     "RADIUS Auth",                    "auth"),
    1813:("RADIUS",     "RADIUS Accounting",              "auth"),
    1883:("MQTT",       "IoT Messaging (MQTT)",           "iot"),
    1900:("UPNP",       "Universal Plug & Play",          "upnp"),
    2049:("NFS",        "Network File System",            "nfs"),
    2121:("FTP-ALT",    "Alternate FTP",                  "ftp"),
    2181:("ZOOKEEPER",  "Apache ZooKeeper",               "distributed"),
    2222:("SSH-ALT",    "Alternate SSH",                  "ssh"),
    2375:("DOCKER",     "Docker API (NO TLS!)",           "docker"),
    2376:("DOCKER-TLS", "Docker TLS API",                 "docker"),
    2379:("ETCD",       "etcd Key-Value Store",           "distributed"),
    2380:("ETCD-PEER",  "etcd Peer",                      "distributed"),
    2404:("IEC-104",    "ICS IEC 60870-5-104",            "ics"),
    2483:("ORACLE-TLS", "Oracle DB TLS",                  "database"),
    2484:("ORACLE-TLS", "Oracle DB TLS",                  "database"),
    2967:("SYMANTEC",   "Symantec AV",                    "security"),
    3000:("GRAFANA",    "Grafana / Dev Server",           "http"),
    3128:("SQUID",      "Squid Proxy",                    "proxy"),
    3260:("ISCSI",      "iSCSI Target",                   "storage"),
    3268:("LDAP-GC",    "LDAP Global Catalog",            "ldap"),
    3269:("LDAPS-GC",   "Secure LDAP GC",                 "ldap"),
    3306:("MYSQL",      "MySQL / MariaDB",                "database"),
    3389:("RDP",        "Remote Desktop Protocol",        "rdp"),
    3690:("SVN",        "Subversion",                     "vcs"),
    4022:("SSH-ALT",    "SSH Alternate",                  "ssh"),
    4369:("EPMD",       "Erlang Port Mapper",             "erlang"),
    4443:("HTTPS-ALT",  "Alternate HTTPS",                "https"),
    4444:("METASPLOIT", "Metasploit / Custom",            "default"),
    4505:("SALTSTACK",  "SaltStack Master",               "devops"),
    4506:("SALTSTACK",  "SaltStack Publisher",            "devops"),
    4840:("OPC-UA",     "ICS OPC Unified Architecture",   "ics"),
    5000:("FLASK",      "Flask Dev / UPnP",               "http"),
    5001:("DEV-HTTP",   "Dev Server",                     "http"),
    5044:("LOGSTASH",   "Logstash Beats",                 "logging"),
    5060:("SIP",        "VoIP SIP",                       "voip"),
    5061:("SIPS",       "Secure VoIP SIP",                "voip"),
    5432:("POSTGRES",   "PostgreSQL Database",            "database"),
    5601:("KIBANA",     "Kibana Dashboard",               "logging"),
    5672:("AMQP",       "RabbitMQ AMQP",                  "messaging"),
    5900:("VNC",        "VNC Remote Desktop",             "vnc"),
    5984:("COUCHDB",    "CouchDB",                        "database"),
    5985:("WINRM",      "WinRM HTTP",                     "remote"),
    5986:("WINRM-TLS",  "WinRM HTTPS",                    "remote"),
    6379:("REDIS",      "Redis Cache (NO AUTH risk)",     "database"),
    6380:("REDIS-TLS",  "Redis TLS",                      "database"),
    6443:("K8S-API",    "Kubernetes API Server",          "k8s"),
    6667:("IRC",        "IRC Chat",                       "irc"),
    7001:("WEBLOGIC",   "Oracle WebLogic",                "java"),
    7077:("SPARK",      "Apache Spark Master",            "distributed"),
    7474:("NEO4J",      "Neo4j Graph DB",                 "database"),
    8009:("AJP",        "Apache JServ (Ghostcat!)",       "http"),
    8080:("HTTP-PROXY", "Alternate HTTP / Proxy",         "http"),
    8081:("HTTP-ALT",   "Alternate HTTP",                 "http"),
    8083:("INFLUXDB",   "InfluxDB HTTP",                  "database"),
    8086:("INFLUXDB",   "InfluxDB API",                   "database"),
    8088:("RIAK",       "Riak HTTP",                      "database"),
    8161:("ACTIVEMQ",   "ActiveMQ Web Console",           "messaging"),
    8443:("HTTPS-ALT",  "Alternate HTTPS",                "https"),
    8500:("CONSUL",     "HashiCorp Consul",               "devops"),
    8545:("ETH-RPC",    "Ethereum JSON-RPC",              "blockchain"),
    8888:("JUPYTER",    "Jupyter Notebook",               "datascience"),
    9000:("SONARQUBE",  "SonarQube / PHP-FPM",           "devops"),
    9042:("CASSANDRA",  "Apache Cassandra",               "database"),
    9090:("PROMETHEUS", "Prometheus Metrics",             "monitoring"),
    9092:("KAFKA",      "Apache Kafka",                   "messaging"),
    9200:("ELASTIC",    "ElasticSearch HTTP",             "database"),
    9300:("ELASTIC",    "ElasticSearch Transport",        "database"),
    9418:("GIT",        "Git Protocol",                   "vcs"),
    9999:("JMXRMI",     "Java JMX",                       "java"),
    10000:("WEBMIN",    "Webmin Admin Panel",             "admin"),
    10250:("KUBELET",   "Kubernetes Kubelet",             "k8s"),
    10255:("K8S-RO",    "Kubernetes Read-Only",           "k8s"),
    11211:("MEMCACHED", "Memcached (NO AUTH risk)",       "cache"),
    15432:("PGBOUNCER", "PgBouncer Pool",                 "database"),
    15672:("RABBITMQ",  "RabbitMQ Management",            "messaging"),
    16010:("HBASE",     "HBase Master",                   "bigdata"),
    16379:("REDIS",     "Redis Cluster",                  "database"),
    17000:("SOLR",      "Apache Solr",                    "database"),
    18080:("SPARK-UI",  "Spark Web UI",                   "distributed"),
    19999:("NETDATA",   "Netdata Monitoring",             "monitoring"),
    20000:("WEBMIN",    "Webmin / dnscrypt",              "admin"),
    27017:("MONGODB",   "MongoDB Primary",                "database"),
    27018:("MONGODB",   "MongoDB Shard",                  "database"),
    27019:("MONGODB",   "MongoDB Config",                 "database"),
    28017:("MONGODB",   "MongoDB Web UI",                 "database"),
    47808:("BACNET",    "ICS BACnet",                     "ics"),
    50000:("SAP",       "SAP Message Server",             "sap"),
    50070:("HDFS",      "Hadoop NameNode",                "bigdata"),
    61616:("ACTIVEMQ",  "ActiveMQ Broker",                "messaging"),
    62078:("IPHONE",    "Apple iPhone Sync",              "mobile"),
}

HIGH_RISK = {
    21, 23, 69, 111, 135, 137, 139, 161, 512, 513, 514,
    1099, 1900, 2375, 4369, 4444, 5984, 6379, 8009, 8161,
    9200, 11211, 27017, 50070, 61616, 502, 4840, 2404, 47808
}

BANNER_PROBES = {
    "http":    b"GET / HTTP/1.0\r\nHost: localhost\r\nUser-Agent: SHIVA/2.0\r\n\r\n",
    "https":   b"GET / HTTP/1.0\r\nHost: localhost\r\nUser-Agent: SHIVA/2.0\r\n\r\n",
    "ftp":     b"",
    "ssh":     b"",
    "smtp":    b"EHLO shiva.scanner\r\n",
    "pop3":    b"",
    "imap":    b"A001 CAPABILITY\r\n",
    "telnet":  b"",
    "dns":     b"\x00\x1c\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03",
    "redis":   b"INFO server\r\n",
    "default": b"\r\n",
}

TTL_OS = {
    (1,   64):  "Linux / Unix / macOS / Android",
    (65, 128):  "Windows (NT/XP/7/10/11/Server)",
    (129, 255): "Network Device (Cisco/Juniper/Solaris/HP)",
}

# ─── VULNERABILITY INTEL ─────────────────────────────────────────────────────
VULN_INTEL = {
    21:  [("HIGH",  "Anonymous FTP login — check for unauthenticated access"),
          ("INFO",  "vsftpd 2.3.4 backdoor (CVE-2011-2523) if version matches"),
          ("MED",   "ProFTPD mod_copy (CVE-2015-3306) arbitrary file copy")],
    22:  [("INFO",  "Check cipher suites: avoid arcfour, 3des-cbc, blowfish"),
          ("INFO",  "OpenSSH < 7.7 username enumeration (CVE-2018-15473)"),
          ("LOW",   "Brute force exposure — check fail2ban / rate limiting")],
    23:  [("CRIT",  "Telnet transmits credentials in PLAINTEXT — disable immediately"),
          ("CRIT",  "Any credentials sent are trivially interceptable via MitM")],
    25:  [("MED",   "Open relay check — RCPT TO external address without auth"),
          ("INFO",  "Check STARTTLS enforcement and TLS certificate validity")],
    53:  [("MED",   "DNS zone transfer (AXFR) — dig AXFR @target domain"),
          ("LOW",   "DNS amplification potential — check recursion for external IPs")],
    80:  [("MED",   "Check HTTP security headers: HSTS, X-Frame-Options, CSP"),
          ("INFO",  "Directory traversal, default files (/admin, /.git, /backup)")],
    110: [("MED",   "POP3 in cleartext — check STARTTLS is enforced")],
    111: [("HIGH",  "RPC portmapper exposes service map — often precedes NFS attack")],
    139: [("HIGH",  "NetBIOS/SMB — check for null sessions and share enumeration")],
    143: [("MED",   "IMAP in cleartext — check STARTTLS enforcement")],
    161: [("HIGH",  "SNMP community string brute force — try 'public', 'private'"),
          ("CRIT",  "SNMPv1/v2 community strings are cleartext — upgrade to SNMPv3")],
    443: [("INFO",  "Check SSL/TLS: SSLv2/3/TLS1.0 should be disabled"),
          ("INFO",  "Check for BEAST, POODLE, Heartbleed (OpenSSL < 1.0.1g)"),
          ("INFO",  "Certificate expiry, self-signed, weak signature algorithm")],
    445: [("CRIT",  "EternalBlue (MS17-010) — SMBv1 RCE, patches critical"),
          ("CRIT",  "EternalRomance, DoublePulsar — verify SMBv1 is DISABLED"),
          ("HIGH",  "SMB null session — check anonymous share access")],
    502: [("CRIT",  "Modbus has NO authentication — ICS/SCADA direct access")],
    1099:("CRIT",  "Java RMI — remote code execution via deserialization"),
    1433:[("HIGH",  "MSSQL — sa account brute force, xp_cmdshell check")],
    1521:[("HIGH",  "Oracle — check for default SIDs: ORCL, XE, DB")],
    1883:[("HIGH",  "MQTT — check for unauthenticated broker access (IoT risk)")],
    1900:[("MED",   "UPnP — CVE-2020-12695 CallStranger DDoS/SSRF amplification")],
    2049:[("HIGH",  "NFS — check showmount -e, world-readable exports")],
    2181:[("HIGH",  "ZooKeeper — often unauthenticated, exposes distributed config")],
    2375:[("CRIT",  "Docker API WITHOUT TLS — full container/host compromise trivial")],
    3306:[("HIGH",  "MySQL — check for remote root login, weak credentials")],
    3389:[("CRIT",  "BlueKeep (CVE-2019-0708) — pre-auth RCE on unpatched Windows"),
          ("CRIT",  "DejaBlue (CVE-2019-1181/1182) — RDP RCE Windows 7/Server"),
          ("HIGH",  "RDP brute force — check NLA enforcement and lockout policy")],
    4369:[("HIGH",  "Erlang EPMD — exposes Erlang cookie, potential RCE via distribution")],
    4840:[("CRIT",  "OPC-UA — ICS protocol, often unauthenticated industrial control")],
    5432:[("HIGH",  "PostgreSQL — check pg_hba.conf, default postgres/postgres creds")],
    5900:[("HIGH",  "VNC — check for no-password auth, weak VNC password"),
          ("HIGH",  "LibVNCServer heap overflow (CVE-2019-15681)")],
    5984:[("CRIT",  "CouchDB admin party — check /_config/admins for empty auth")],
    6379:[("CRIT",  "Redis — unauthenticated access allows arbitrary code execution"),
          ("CRIT",  "Redis SLAVEOF can write files to disk (SSH key injection)")],
    8009:[("CRIT",  "Apache Ghostcat (CVE-2020-1938) — AJP file read/inclusion")],
    8161:[("HIGH",  "ActiveMQ Web Console — default creds admin/admin")],
    9200:[("CRIT",  "ElasticSearch — check for unauth access, data exposure"),
          ("HIGH",  "ES dynamic scripting RCE (pre 1.6) if old version")],
    10250:[("CRIT", "Kubernetes Kubelet API — unauthenticated may allow pod exec")],
    11211:[("CRIT", "Memcached — no auth, UDP amplification DDoS (x50,000 factor)")],
    27017:[("CRIT", "MongoDB — check if auth disabled, world-accessible DB"),
           ("HIGH", "MongoDB 2.x default: no auth, no bind address restriction")],
    47808:[("CRIT", "BACnet — building automation, no auth, direct ICS control")],
    50070:[("HIGH", "Hadoop NameNode — check for unauthenticated HDFS access")],
    61616:[("HIGH", "ActiveMQ — ClassInfo deserialization RCE (CVE-2015-5254)")],
}

# ─── SCAN RESULT ─────────────────────────────────────────────────────────────
class PortInfo:
    __slots__ = ["port","state","proto","name","desc","stype","banner",
                 "version","risk","vulns","ssl_info","response_time"]
    def __init__(self):
        for s in self.__slots__: setattr(self,s,"")
        self.vulns = []
        self.response_time = 0.0

class HostResult:
    def __init__(self, target):
        self.target    = target
        self.ip        = ""
        self.hostname  = ""
        self.os_hint   = "Unknown"
        self.ttl       = 0
        self.mac       = ""
        self.open_ports: list[PortInfo] = []
        self.filtered  = 0
        self.closed    = 0
        self.scan_time = 0.0
        self.timestamp = datetime.now()

# ─── SHIVA ENGINE ────────────────────────────────────────────────────────────
class ShivaScanner:

    def __init__(self, args):
        self.args    = args
        self.timeout = args.timeout
        self.threads = args.threads
        self.mode    = args.mode
        self._lock   = threading.Lock()

    # ── RESOLVE ──────────────────────────────────────────────────
    def resolve(self, target):
        try:
            ip = socket.gethostbyname(target)
            try:    hostname = socket.gethostbyaddr(ip)[0]
            except: hostname = ""
            return ip, hostname
        except: return "", ""

    # ── PORT PARSER ───────────────────────────────────────────────
    def parse_ports(self, s):
        if s == "top100":
            return sorted(SERVICE_DB.keys())[:100]
        if s == "top1000":
            known = list(SERVICE_DB.keys())
            common = list(range(1, 1025))
            return sorted(set(known + common))
        if s == "all":
            return list(range(1, 65536))
        if s == "vuln":   # Only high-risk ports
            return sorted(HIGH_RISK | set(SERVICE_DB.keys()))
        ports = []
        for part in s.split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-",1)
                ports.extend(range(int(a), int(b)+1))
            else:
                ports.append(int(part))
        return sorted(set(ports))

    # ── TCP CONNECT SCAN ──────────────────────────────────────────
    def tcp_scan(self, ip, port):
        t0 = time.time()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            r = s.connect_ex((ip, port))
            s.close()
            elapsed = time.time() - t0
            if r == 0:       return "open",     elapsed
            elif r in (111, 10061): return "closed", elapsed
            else:            return "filtered", elapsed
        except socket.timeout: return "filtered", self.timeout
        except:                return "filtered", 0.0

    # ── UDP SCAN ──────────────────────────────────────────────────
    def udp_scan(self, ip, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(self.timeout)
            s.sendto(b"\x00\x0c\x00\x00", (ip, port))
            try:    s.recvfrom(512); return "open"
            except: return "open|filtered"
            finally: s.close()
        except: return "error"

    # ── BANNER GRAB ───────────────────────────────────────────────
    def grab_banner(self, ip, port, stype):
        try:
            probe = BANNER_PROBES.get(stype, BANNER_PROBES["default"])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(min(self.timeout * 2, 4.0))
            s.connect((ip, port))
            if probe: s.sendall(probe)
            time.sleep(0.1)
            data = b""
            try:
                while True:
                    chunk = s.recv(1024)
                    if not chunk: break
                    data += chunk
                    if len(data) > 2048: break
            except: pass
            s.close()
            text = data.decode("utf-8", errors="replace").strip()
            text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f-\x9f]", "", text)
            return text[:300]
        except: return ""

    # ── SSL/TLS INFO ──────────────────────────────────────────────
    def get_ssl_info(self, ip, port):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            s = socket.create_connection((ip, port), timeout=self.timeout)
            ss = ctx.wrap_socket(s, server_hostname=ip)
            cert = ss.getpeercert()
            cipher = ss.cipher()
            ver = ss.version()
            ss.close()
            info = []
            if cert:
                subject = dict(x[0] for x in cert.get("subject", []))
                cn = subject.get("commonName", "")
                exp = cert.get("notAfter", "")
                if cn:  info.append(f"CN={cn}")
                if exp: info.append(f"Expires={exp}")
            if cipher: info.append(f"Cipher={cipher[0]}")
            if ver:    info.append(f"TLS={ver}")
            return " | ".join(info)
        except: return ""

    # ── VERSION EXTRACT ───────────────────────────────────────────
    def extract_version(self, banner):
        if not banner: return ""
        patterns = [
            r"OpenSSH[_/\s][\d.p]+\s[\w\-]+",
            r"Apache[/\s][\d.]+[\s\w\-()]*",
            r"nginx[/\s][\d.]+",
            r"Microsoft-IIS[/\s][\d.]+",
            r"vsftpd[\s/][\d.]+",
            r"ProFTPD[\s/][\d.]+",
            r"FileZilla Server [\d.]+",
            r"Postfix[\s/]\w+",
            r"MySQL[\s/][\d.]+",
            r"PostgreSQL[\s\d.]+",
            r"Redis[\s/][\d.]+",
            r"MongoDB[\s/][\d.]+",
            r"OpenSSL[/\s][\d.]+[a-z]?",
            r"PHP[/\s][\d.]+",
            r"Python[/\s][\d.]+",
            r"lighttpd[/\s][\d.]+",
            r"Dovecot",
            r"Exim[\s][\d.]+",
            r"Sendmail[\s/][\d./]+",
            r"SSH-[\d.]+-[\w.\-]+",
            r"220.*?ESMTP\s[\w.\-]+",
        ]
        for p in patterns:
            m = re.search(p, banner, re.IGNORECASE)
            if m: return m.group(0)[:70]
        return ""

    # ── TTL OS DETECT ─────────────────────────────────────────────
    def get_ttl(self, ip):
        try:
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", "1000", ip]
            else:
                cmd = ["ping", "-c", "1", "-W", "1", ip]
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            m = re.search(r"ttl[=\s]+(\d+)", out.stdout, re.IGNORECASE)
            if m: return int(m.group(1))
        except: pass
        return 0

    def ttl_to_os(self, ttl):
        if ttl == 0: return "Unknown"
        for (lo, hi), name in TTL_OS.items():
            if lo <= ttl <= hi: return f"{name} (TTL={ttl})"
        return f"Unknown (TTL={ttl})"

    # ── ANALYSE ONE PORT ──────────────────────────────────────────
    def analyse(self, ip, port):
        state, rt = self.tcp_scan(ip, port)
        if state != "open": return state

        pi = PortInfo()
        pi.port  = port
        pi.state = "open"
        pi.proto = "TCP"
        pi.response_time = round(rt * 1000, 1)

        svc = SERVICE_DB.get(port, ("UNKNOWN", "Unknown Service", "default"))
        pi.name, pi.desc, pi.stype = svc
        pi.risk = "CRITICAL" if port in HIGH_RISK else "HIGH" if port < 1024 else "MEDIUM" if port < 8000 else "LOW"

        # Banner + version
        if self.mode in ("full", "vuln", "banner", "aggressive"):
            pi.banner  = self.grab_banner(ip, port, pi.stype)
            pi.version = self.extract_version(pi.banner)

        # SSL info
        if self.mode in ("full", "vuln", "aggressive") and pi.stype in ("https","ssl","ldaps"):
            pi.ssl_info = self.get_ssl_info(ip, port)
        if self.mode == "aggressive" and port in (443, 8443, 4443, 636, 993, 995, 465):
            pi.ssl_info = self.get_ssl_info(ip, port)

        # Vuln hints
        if self.mode in ("vuln", "aggressive"):
            raw = VULN_INTEL.get(port, [])
            if isinstance(raw, list):
                pi.vulns = raw
            elif isinstance(raw, tuple):
                pi.vulns = [raw]

        return pi

    # ── SCAN ONE HOST ─────────────────────────────────────────────
    def scan_host(self, target, ports):
        hr = HostResult(target)
        t0 = time.time()
        ip, hostname = self.resolve(target)
        if not ip:
            if HAS_RICH: console.print(f"[red]Cannot resolve: {target}[/red]")
            else: print(f"Cannot resolve: {target}")
            return hr

        hr.ip = ip
        hr.hostname = hostname

        # OS hint
        ttl = self.get_ttl(ip)
        hr.ttl = ttl
        hr.os_hint = self.ttl_to_os(ttl)

        # Stealth: shuffle + small jitter
        scan_list = ports.copy()
        if self.mode == "stealth":
            random.shuffle(scan_list)

        open_ports = []
        closed = filtered = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as pool:
            futures = {pool.submit(self.analyse, ip, p): p for p in scan_list}
            for fut in concurrent.futures.as_completed(futures):
                res = fut.result()
                if isinstance(res, PortInfo):
                    with self._lock: open_ports.append(res)
                elif res == "closed":  closed   += 1
                else:                  filtered += 1

        hr.open_ports  = sorted(open_ports, key=lambda x: x.port)
        hr.closed      = closed
        hr.filtered    = filtered
        hr.scan_time   = round(time.time() - t0, 2)
        return hr

    # ── EXPAND CIDR ───────────────────────────────────────────────
    def expand(self, target):
        try:
            net = ipaddress.ip_network(target, strict=False)
            if net.num_addresses > 1:
                return [str(ip) for ip in net.hosts()]
        except: pass
        return [target]

    # ── PRINT RESULT ─────────────────────────────────────────────
    def print_result(self, hr: HostResult):
        if not HAS_RICH:
            self._plain(hr); return

        host_str = hr.ip
        if hr.hostname: host_str = f"{hr.hostname} [{hr.ip}]"

        risk_counts = {}
        for p in hr.open_ports:
            risk_counts[p.risk] = risk_counts.get(p.risk, 0) + 1

        risk_str = "  ".join(
            f"[{'red' if r=='CRITICAL' else 'dark_orange' if r=='HIGH' else 'yellow' if r=='MEDIUM' else 'green'}]{v} {r}[/]"
            for r, v in risk_counts.items()
        )

        console.print()
        console.print(Rule(f"[bold red] SHIVA  ·  {host_str} ", style="red"))
        console.print(
            f"  [dim]OS:[/dim] [cyan]{hr.os_hint}[/cyan]  "
            f"[dim]Open:[/dim] [green bold]{len(hr.open_ports)}[/green bold]  "
            f"[dim]Closed:[/dim] [dim]{hr.closed}[/dim]  "
            f"[dim]Filtered:[/dim] [dim]{hr.filtered}[/dim]  "
            f"[dim]Time:[/dim] [dim]{hr.scan_time}s[/dim]  "
            + (risk_str if risk_str else "")
        )

        if not hr.open_ports:
            console.print("  [dim]No open ports found in scanned range.[/dim]")
            return

        t = Table(box=box.SIMPLE_HEAD, show_header=True,
                  header_style="bold dim", expand=True, padding=(0,1))
        t.add_column("Port",     style="bold cyan",  width=7)
        t.add_column("Proto",    width=5)
        t.add_column("State",    width=7)
        t.add_column("Service",  style="bold white", width=14)
        t.add_column("Risk",     width=10)
        t.add_column("RTT",      width=7)
        t.add_column("Version / Banner", no_wrap=False)

        risk_color = {"CRITICAL":"red","HIGH":"dark_orange","MEDIUM":"yellow","LOW":"green"}

        for p in hr.open_ports:
            rc = risk_color.get(p.risk, "white")
            info = p.version or (p.banner[:80] if p.banner else "")
            if p.ssl_info: info = (info + " | " + p.ssl_info)[:100] if info else p.ssl_info[:100]
            rtt  = f"{p.response_time}ms" if p.response_time else "—"
            t.add_row(
                str(p.port),
                p.proto,
                "[green]open[/green]",
                p.name,
                f"[{rc}]{p.risk}[/{rc}]",
                f"[dim]{rtt}[/dim]",
                info or "[dim]—[/dim]",
            )
        console.print(t)

        # Vuln section
        if any(p.vulns for p in hr.open_ports):
            console.print(f"\n  [bold red]  VULNERABILITY INTEL[/bold red]")
            for p in hr.open_ports:
                if not p.vulns: continue
                console.print(f"\n  [cyan]PORT {p.port} / {p.name}[/cyan]")
                for sev, msg in p.vulns:
                    icons = {"CRIT":"[bold red] [CRIT][/bold red]",
                             "HIGH":"[dark_orange] [HIGH][/dark_orange]",
                             "MED": "[yellow] [MED] [/yellow]",
                             "INFO":"[blue] [INFO][/blue]"}
                    console.print(f"    {icons.get(sev,'  ')}  {msg}")

    def _plain(self, hr):
        print(f"\n{'─'*65}")
        print(f"  {hr.hostname or hr.ip}  [{hr.ip}]")
        print(f"  OS: {hr.os_hint}  |  Open: {len(hr.open_ports)}  |  {hr.scan_time}s")
        print(f"{'─'*65}")
        for p in hr.open_ports:
            info = p.version or p.banner[:50]
            print(f"  {p.port:>6}/tcp   {p.state:<8}  {p.name:<14}  {p.risk:<8}  {info}")

    # ── JSON EXPORT ───────────────────────────────────────────────
    def export(self, results, path):
        out = []
        for hr in results:
            out.append({
                "target":    hr.target,
                "ip":        hr.ip,
                "hostname":  hr.hostname,
                "os_hint":   hr.os_hint,
                "ttl":       hr.ttl,
                "scan_time": hr.scan_time,
                "timestamp": hr.timestamp.isoformat(),
                "open_ports":[{
                    "port":          p.port,
                    "state":         p.state,
                    "protocol":      p.proto,
                    "service":       p.name,
                    "description":   p.desc,
                    "risk":          p.risk,
                    "response_ms":   p.response_time,
                    "version":       p.version,
                    "banner":        p.banner[:200],
                    "ssl_info":      p.ssl_info,
                    "vuln_hints":    [f"[{s}] {m}" for s,m in p.vulns],
                } for p in hr.open_ports],
            })
        with open(path, "w") as f:
            json.dump(out, f, indent=2)
        if HAS_RICH: console.print(f"\n[green]Saved:[/green] {path}")
        else: print(f"\nSaved: {path}")

    # ── RUN ───────────────────────────────────────────────────────
    def run(self):
        print_logo()

        # Startup line
        if HAS_RICH:
            console.print("  [dim red]🔱  HAR HAR MAHADEV — initiating scan ...[/dim red]\n")

        targets = []
        for t in self.args.target.split(","):
            targets.extend(self.expand(t.strip()))
        targets = list(dict.fromkeys(targets))

        ports = self.parse_ports(self.args.ports)

        if HAS_RICH:
            console.print(
                f"  [dim]Targets[/dim] [white]{len(targets)}[/white]  "
                f"[dim]Ports[/dim] [white]{len(ports)}[/white]  "
                f"[dim]Mode[/dim] [white]{self.mode}[/white]  "
                f"[dim]Threads[/dim] [white]{self.threads}[/white]  "
                f"[dim]Timeout[/dim] [white]{self.timeout}s[/white]\n"
            )
        else:
            print(f"Targets:{len(targets)} Ports:{len(ports)} Mode:{self.mode} Threads:{self.threads}")

        results = []
        for target in targets:
            if HAS_RICH:
                with console.status(f"[red]Scanning {target} ...[/red]", spinner="dots2"):
                    hr = self.scan_host(target, ports)
            else:
                print(f"Scanning {target}...")
                hr = self.scan_host(target, ports)
            self.print_result(hr)
            results.append(hr)

        # Summary
        total_open = sum(len(r.open_ports) for r in results)
        total_time = sum(r.scan_time for r in results)
        crits = sum(1 for r in results for p in r.open_ports if p.risk == "CRITICAL")

        if HAS_RICH:
            console.print()
            console.print(Rule(style="dim"))
            console.print(
                f"  [dim]Hosts[/dim] [white]{len(results)}[/white]  "
                f"[dim]Open ports[/dim] [green]{total_open}[/green]  "
                f"[dim]Critical[/dim] [red]{crits}[/red]  "
                f"[dim]Total time[/dim] [white]{total_time:.1f}s[/white]"
            )
            console.print(Rule(style="dim"))
        else:
            print(f"\nHosts:{len(results)} Open:{total_open} Critical:{crits} Time:{total_time:.1f}s")

        if self.args.output:
            self.export(results, self.args.output)


# ─── LOGO ─────────────────────────────────────────────────────────────────────
def print_logo():
    import random as _r
    quote = _r.choice(SHIVA_QUOTES)
    if HAS_RICH:
        console.print()
        style_map = {
            "rule":    "dim red",
            "trishul": "red",
            "title":   "bold red",
            "meta":    "bold red",
            "dim":     "dim",
        }
        for text, hint in SHIVA_BANNER_LINES:
            console.print(Text(text, style=style_map.get(hint, "red")))
        console.print(Text(f"\n  ॐ  {quote}\n", style="italic dim red"))
    else:
        for text, _ in SHIVA_BANNER_LINES:
            print(text)
        print(f"\n  ॐ  {quote}\n")


# ─── HELP MENU ────────────────────────────────────────────────────────────────
def print_help():
    if HAS_RICH:
        print_logo()

        # ── USAGE ──
        console.print()
        console.print(Rule("[bold red]  USAGE  [/bold red]", style="red"))
        console.print("  [bold cyan]python3 shiva.py[/bold cyan] "
                      "[bold white]-t[/bold white] TARGET "
                      "[dim][[/dim][bold white]-p[/bold white] PORTS[dim]][/dim] "
                      "[dim][[/dim][bold white]--mode[/bold white] MODE[dim]][/dim] "
                      "[dim][OPTIONS][/dim]\n")

        # ── ARGUMENTS ──
        console.print(Rule("[bold red]  ARGUMENTS  [/bold red]", style="red"))
        ta = Table(box=box.SIMPLE, show_header=True, padding=(0,2),
                   header_style="bold dim")
        ta.add_column("Flag",        style="bold cyan",  width=18)
        ta.add_column("Description", style="white")
        ta.add_column("Default",     style="dim",        width=14)
        ta.add_column("Required",    style="dim",        width=8)
        args_rows = [
            ("-t, --target",  "Target: IP, hostname, CIDR subnet, or comma-separated list", "—",          "YES"),
            ("-p, --ports",   "Ports to scan (see PORT FORMATS section below)",              "top1000",    "no"),
            ("--mode",        "Scan mode — quick/full/stealth/banner/vuln/aggressive",       "quick",      "no"),
            ("--threads",     "Concurrent worker threads (higher = faster, more load)",      "300",        "no"),
            ("--timeout",     "Socket connection timeout per port in seconds",               "1.0",        "no"),
            ("-o, --output",  "Export results to a JSON file at given path",                 "—",          "no"),
            ("--no-color",    "Disable rich colour — useful for logs and piping",            "—",          "no"),
            ("-h, --help",    "Show this help menu and exit",                                "—",          "no"),
            ("-v, --version", "Print version string and exit",                              "—",          "no"),
        ]
        for r in args_rows: ta.add_row(*r)
        console.print(ta)

        # ── SCAN MODES ──
        console.print(Rule("[bold red]  SCAN MODES  [/bold red]", style="red"))
        tm = Table(box=box.SIMPLE, show_header=True, padding=(0,2),
                   header_style="bold dim")
        tm.add_column("Mode",       style="bold cyan",  width=12)
        tm.add_column("Speed",      style="dim",        width=8)
        tm.add_column("What it does",  style="white")
        modes_data = [
            ("quick",      "Fast",    "TCP connect scan only. No banner grabbing. Identify open ports + service names + risk levels + OS hint."),
            ("full",       "Medium",  "TCP + UDP on key ports + banner grab + version extraction + SSL/TLS cert info on HTTPS ports."),
            ("stealth",    "Slow",    "Randomised port order + jitter. Avoids IDS/IPS threshold triggers. Use low threads (30-50) and high timeout (2-3s)."),
            ("banner",     "Medium",  "Aggressive banner grabbing with multiple probes per service. Maximum version string extraction."),
            ("vuln",       "Medium",  "Everything in full + CVE/vulnerability intel mapped to each open port. Shows specific exploit hints."),
            ("aggressive", "Medium",  "Maximum mode: full + vuln + SSL deep-dive on all TLS ports + all banner probes. The full picture."),
        ]
        for m, sp, desc in modes_data: tm.add_row(m, sp, desc)
        console.print(tm)

        # ── PORT FORMATS ──
        console.print(Rule("[bold red]  PORT FORMATS  [/bold red]", style="red"))
        tp = Table(box=box.SIMPLE, show_header=True, padding=(0,2),
                   header_style="bold dim")
        tp.add_column("Format",      style="bold cyan",  width=16)
        tp.add_column("Example",     style="dim",        width=24)
        tp.add_column("Description", style="white")
        port_fmts = [
            ("Single port",     "-p 22",               "One specific port"),
            ("Comma list",      "-p 22,80,443,3306",   "Multiple specific ports"),
            ("Range",           "-p 1-1000",            "All ports from 1 to 1000 inclusive"),
            ("top100",          "-p top100",            "Top 100 well-known service ports"),
            ("top1000",         "-p top1000",           "Top 1000 ports — default, covers most services"),
            ("vuln",            "-p vuln",              "Only high-risk ports from SHIVA vulnerability database"),
            ("all",             "-p all",               "All 65535 ports. Use --threads 1000 --timeout 0.5"),
        ]
        for f, e, d in port_fmts: tp.add_row(f, e, d)
        console.print(tp)

        # ── RISK LEVELS ──
        console.print(Rule("[bold red]  RISK LEVELS  [/bold red]", style="red"))
        tr = Table(box=box.SIMPLE, show_header=True, padding=(0,2),
                   header_style="bold dim")
        tr.add_column("Level",    width=10)
        tr.add_column("Port Range",  style="dim", width=14)
        tr.add_column("Examples",    style="dim")
        tr.add_row("[bold red]CRITICAL[/bold red]",     "Any",       "Telnet, Redis, MongoDB, Docker API, Memcached — known no-auth or default-cred RCE surface")
        tr.add_row("[dark_orange]HIGH[/dark_orange]",   "<1024",     "SSH, FTP, SMTP, SMB, RDP, MySQL — well-known attack targets")
        tr.add_row("[yellow]MEDIUM[/yellow]",           "1024–7999", "Custom apps, alternate ports, middleware services")
        tr.add_row("[green]LOW[/green]",                "8000+",     "Dev servers, monitoring endpoints, internal tools")
        console.print(tr)

        # ── EXAMPLES ──
        console.print(Rule("[bold red]  EXAMPLES  [/bold red]", style="red"))
        te = Table(box=box.SIMPLE, show_header=False, padding=(0,2))
        te.add_column(style="dim",        width=26)
        te.add_column(style="bold white")
        examples = [
            ("Basic scan",              "python3 shiva.py -t 192.168.1.1"),
            ("Vuln scan",               "python3 shiva.py -t 192.168.1.1 --mode vuln"),
            ("Full scan + banner",      "python3 shiva.py -t 192.168.1.1 --mode full"),
            ("Maximum aggressive",      "python3 shiva.py -t 192.168.1.1 --mode aggressive"),
            ("Specific ports",          "python3 shiva.py -t 192.168.1.1 -p 22,80,443,3306,6379"),
            ("All 65535 ports",         "python3 shiva.py -t 192.168.1.1 -p all --threads 1000 --timeout 0.5"),
            ("Subnet /24 sweep",        "python3 shiva.py -t 192.168.1.0/24 -p top100 --mode quick"),
            ("Multiple targets",        "python3 shiva.py -t 10.0.0.1,10.0.0.2,10.0.0.5 --mode vuln"),
            ("Save JSON report",        "python3 shiva.py -t myserver.com --mode full -o report.json"),
            ("Stealth low-and-slow",    "python3 shiva.py -t 192.168.1.1 --mode stealth --threads 30 --timeout 3"),
            ("High-risk ports only",    "python3 shiva.py -t 192.168.1.1 -p vuln --mode vuln"),
            ("No color for log file",   "python3 shiva.py -t 192.168.1.1 --no-color --mode full | tee scan.log"),
            ("Database server check",   "python3 shiva.py -t 10.0.0.50 -p 1433,3306,5432,6379,27017,9200 --mode vuln"),
            ("Web server full audit",   "python3 shiva.py -t web.example.com -p 1-10000 --mode aggressive -o audit.json"),
        ]
        for label, cmd in examples: te.add_row(label, cmd)
        console.print(te)

        # ── PERFORMANCE TIPS ──
        console.print(Rule("[bold red]  PERFORMANCE TIPS  [/bold red]", style="red"))
        perf_tips = [
            ("Single host, quick",      "--threads 300 --timeout 1.0",   "Default. Balanced."),
            ("Single host, all ports",  "--threads 1000 --timeout 0.5",  "Fast full sweep."),
            ("Subnet scan",             "--threads 200 --timeout 1.0",   "Avoid network saturation."),
            ("Stealth / evasion",       "--threads 30 --timeout 3.0",    "Low and slow."),
            ("High-latency target",     "--threads 100 --timeout 2.0",   "Compensate for RTT."),
        ]
        tperf = Table(box=box.SIMPLE, show_header=False, padding=(0,2))
        tperf.add_column(style="dim",       width=26)
        tperf.add_column(style="cyan",      width=36)
        tperf.add_column(style="dim")
        for s, f, n in perf_tips: tperf.add_row(s, f, n)
        console.print(tperf)

        # ── OS DETECTION ──
        console.print(Rule("[bold red]  OS DETECTION (TTL)  [/bold red]", style="red"))
        console.print("  SHIVA pings the target and reads the IP TTL to estimate the OS family:\n")
        tos = Table(box=box.SIMPLE, show_header=False, padding=(0,2))
        tos.add_column(style="cyan bold", width=14)
        tos.add_column(style="white")
        tos.add_row("TTL 1–64",   "Linux / Unix / macOS / Android")
        tos.add_row("TTL 65–128", "Windows (NT / XP / 7 / 10 / 11 / Server)")
        tos.add_row("TTL 129+",   "Network Device (Cisco / Juniper / Solaris / HP)")
        console.print(tos)

        # ── LEGAL WARNING ──
        console.print()
        console.print(Panel(
            "[bold red]⚠  LEGAL WARNING  ⚠[/bold red]\n\n"
            "Scanning systems you do not own or have [bold]explicit written permission[/bold]\n"
            "to test is [bold red]ILLEGAL[/bold red] in most jurisdictions worldwide:\n\n"
            "  [dim]•  Computer Fraud and Abuse Act (CFAA) — USA[/dim]\n"
            "  [dim]•  Computer Misuse Act — UK[/dim]\n"
            "  [dim]•  IT Act 2000 — India[/dim]\n"
            "  [dim]•  Similar laws in EU, Australia, Canada, and most nations[/dim]\n\n"
            "SHIVA is for [bold]your own systems, authorized engagements, and CTF labs ONLY[/bold].\n"
            "The authors accept no responsibility for misuse.",
            border_style="red", expand=False, padding=(1,3)
        ))
        console.print()

    else:
        # Plain text fallback
        print(SHIVA_LOGO)
        print("SHIVA Port Scanner v2.0 | AdiscLabs | @Aditya Bhosale")
        print("OM NAMAH SHIVAYA — The Destroyer of Vulnerabilities")
        print("\n" + "="*65)
        print("USAGE:   python3 shiva.py -t TARGET [OPTIONS]")
        print("="*65)
        print("\nARGUMENTS:")
        print("  -t, --target    Target IP/hostname/CIDR/comma-list  [REQUIRED]")
        print("  -p, --ports     Port specification                  [top1000]")
        print("  --mode          Scan mode                           [quick]")
        print("  --threads       Concurrent threads                  [300]")
        print("  --timeout       Socket timeout seconds              [1.0]")
        print("  -o, --output    Save results to JSON file           [optional]")
        print("  --no-color      Disable colour output")
        print("  -h, --help      Show this help")
        print("  -v, --version   Show version")
        print("\nSCAN MODES:")
        print("  quick       TCP connect, fastest, no banners")
        print("  full        TCP+UDP+banners+version+SSL info")
        print("  stealth     Randomised order, slow, evades IDS")
        print("  banner      Aggressive banner grabbing")
        print("  vuln        Full + CVE vulnerability hints")
        print("  aggressive  Everything SHIVA has")
        print("\nPORT FORMATS:")
        print("  80,443,8080   Specific ports")
        print("  1-1000        Port range")
        print("  top100        Top 100 known ports")
        print("  top1000       Top 1000 ports (default)")
        print("  vuln          High-risk ports only")
        print("  all           All 65535 ports")
        print("\nEXAMPLES:")
        print("  python3 shiva.py -t 192.168.1.1 --mode vuln")
        print("  python3 shiva.py -t 192.168.1.0/24 -p top100 --mode quick")
        print("  python3 shiva.py -t myserver.com --mode aggressive -o report.json")
        print("  python3 shiva.py -t 192.168.1.1 -p all --threads 1000 --timeout 0.5")
        print("\n" + "="*65)
        print("⚠  AUTHORIZED USE ONLY. Scanning without permission is illegal.")
        print("="*65)


# ─── CLI ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        prog="shiva",
        description="SHIVA — Advanced Port Scanner v2.0 | AdiscLabs",
        add_help=False,  # We provide our own help
    )
    parser.add_argument("-t", "--target",  default="")
    parser.add_argument("-p", "--ports",   default="top1000")
    parser.add_argument("--mode",          default="quick",
                        choices=["quick","full","stealth","banner","vuln","aggressive"])
    parser.add_argument("--threads",       type=int,   default=300)
    parser.add_argument("--timeout",       type=float, default=1.0)
    parser.add_argument("-o", "--output",  default="")
    parser.add_argument("--no-color",      action="store_true")
    parser.add_argument("-h", "--help",    action="store_true")
    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args()

    if args.no_color:
        global HAS_RICH
        HAS_RICH = False

    if args.version:
        print("SHIVA Port Scanner v2.0 | AdiscLabs | @Aditya Bhosale")
        sys.exit(0)

    if args.help or not args.target:
        print_help()
        sys.exit(0)

    if HAS_RICH:
        console.print("\n[bold red]⚠  Authorized use only. Scanning without permission is illegal.[/bold red]\n")
    else:
        print("\n⚠  Authorized use only. Scanning without permission is illegal.\n")

    scanner = ShivaScanner(args)
    try:
        scanner.run()
    except KeyboardInterrupt:
        if HAS_RICH: console.print("\n[yellow]Interrupted.[/yellow]")
        else: print("\nInterrupted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
