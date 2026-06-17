# MITM Attacks – ARP Spoofing & TLS Enforcement
### Man-in-the-Middle Attack Demonstration with Firewall Defense

![Course](https://img.shields.io/badge/Course-Open%20Network%20Security-blue?style=flat-square)
![Tools](https://img.shields.io/badge/Tools-Wireshark%20%7C%20Bettercap%20%7C%20iptables-orange?style=flat-square)
![OS](https://img.shields.io/badge/OS-Kali%20Linux%20%7C%20Ubuntu-purple?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-green?style=flat-square)


---

## Overview

This lab demonstrates how an attacker on a local network can exploit the **Address Resolution Protocol (ARP)** to execute a **Man-in-the-Middle (MITM)** attack and intercept HTTP traffic. It also validates **HTTPS/TLS encryption** and **iptables firewall rules** as effective countermeasures.

Conducted as part of the **Open Network Security** course at the **University of Luxembourg**.

---

## Lab Environment

| VM | OS | IP | Role |
|---|---|---|---|
| Server | Ubuntu 24.04.3 | 192.168.56.101 | Hosts HTTP/HTTPS web server |
| Client | Ubuntu 24.04.3 | 192.168.56.102 | Submits credentials via browser |
| Attacker | Kali Linux 2025.3 | 192.168.56.103 | Performs ARP spoofing & packet capture |

**Network:** Isolated VirtualBox host-only network

**Tools Used:**
- `arpspoof` / `ettercap` — ARP poisoning
- `tcpdump` / `Wireshark` — Packet capture & analysis
- `iptables` — Firewall enforcement
- `openssl` — TLS certificate generation
- `Python3` — Web server implementation

---

## Attack Flow

```
[Client VM] ──────────────────── [Server VM]
     │                                │
     │        ARP Poisoning           │
     └──────► [Attacker VM] ◄─────────┘
              Intercepts all traffic
```

### Phase 1 — HTTP Attack (Successful)
1. Enable IP forwarding on attacker
2. Start packet capture with `tcpdump`
3. Execute ARP spoofing on both Client and Server
4. Client submits credentials via HTTP form
5. Attacker captures **cleartext credentials** from pcap

**Result:**
```
POST /submit HTTP/1.1
username=Alice&password=Alice   ← Fully visible in plaintext 
```

### Phase 2 — HTTPS Attack (Blocked by TLS)
1. Repeat same ARP spoofing attack
2. Client submits credentials via HTTPS form
3. Attacker captures only **encrypted packets**

**Result:**
```
No cleartext username/password found  ← TLS encryption protects data 
```

---

## Key Findings

| Aspect | HTTP (Port 8080) | HTTPS (Port 8443) |
|---|---|---|
| Credentials exposed | Yes plaintext |  No  encrypted |
| MITM attack successful | Fully | Partial traffic intercepted but unreadable |
| Browser warning |  "Not Secure" | Certificate warning |
| Data visible to attacker |  All POST data |  Encrypted packets only |

---

## Defense Mechanisms Implemented

### 1. HTTPS/TLS Enforcement
Generated self-signed certificate and wrapped server with TLS:
```bash
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout key.pem -out cert.pem \
  -subj "/CN=192.168.56.101"
```

### 2. iptables Firewall Rules
Blocked insecure HTTP and enforced HTTPS on Client VM:
```bash
# Block HTTP
sudo iptables -A OUTPUT -p tcp --dport 80 -j DROP
sudo iptables -A OUTPUT -p tcp --dport 8080 -j REJECT --reject-with tcp-reset

# Allow HTTPS only
sudo iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --dport 8443 -j ACCEPT

# Log blocked attempts
sudo iptables -I OUTPUT -p tcp --dport 80 -j LOG \
  --log-prefix "HTTP-BLOCKED: " --log-level 4
```

---

## Files

```
├── server_http.py       # HTTP web server (Python3)
├── server_https.py      # HTTPS web server with TLS (Python3)
├── form.html            # Login form for credential submission
└── lab_report.pdf       # Full lab report with results
```

---

## Conclusion

ARP spoofing is highly effective on unencrypted HTTP connections credentials can be captured in seconds with minimal tooling. **TLS/HTTPS encryption completely defeats credential theft** even when network traffic is intercepted. Combined with iptables firewall rules, HTTPS enforcements provide robust protection against MITM attacks in local network environments.

---

## References
- [ARP Spoofing – OWASP](https://owasp.org/www-community/attacks/Man-in-the-middle_attack)
- [TLS/HTTPS Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- [iptables Documentation](https://linux.die.net/man/8/iptables)

---


