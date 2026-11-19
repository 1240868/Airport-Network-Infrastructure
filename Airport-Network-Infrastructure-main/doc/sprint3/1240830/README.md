# RCOMP 2025-2026 Project 1 - Sprint 3 - Member 1240830 folder

### Terminal 4 — Task T.3.4

## OSPF Dynamic Routing

Static routing was replaced by OSPF. The T4-Router is part of OSPF Area 3, and the backbone network belongs to Area 0.

| Network / Terminal | OSPF Area ID |
|--------------------|-------------|
| Campus Backbone | 0 |
| Terminal 2 | 1 |
| Terminal 3 | 2 |
| Terminal 4 | 3 |
| Terminal 5 | 4 |

### OSPF Networks configured on T4-Router

| Network | Wildcard | Area |
|---------|----------|------|
| 10.57.128.0 | 0.0.0.255 | 0 |
| 10.57.180.0 | 0.0.7.255 | 3 |
| 10.57.184.0 | 0.0.3.255 | 3 |
| 10.57.188.0 | 0.0.1.255 | 3 |
| 10.57.190.0 | 0.0.0.127 | 3 |

---

## DHCPv4 Service

The T4-Router provides DHCP to all local VLANs except DMZ and backbone networks.

| Pool | Network | Gateway | DNS Server | Domain |
|------|---------|---------|------------|--------|
| T4-Users | 10.57.184.0/22 | 10.57.184.1 | 10.57.190.10 | terminal-4.rcomp-25-26-dd-g1 |
| T4-VoIP | 10.57.188.0/23 | 10.57.188.1 | 10.57.190.10 | terminal-4.rcomp-25-26-dd-g1 |
| WiFi4 | 10.57.180.0/21 | 10.57.180.1 | 10.57.190.10 | terminal-4.rcomp-25-26-dd-g1 |

**Note:** Option 150 (TFTP server) is set to 10.57.188.1 in the VoIP pool for Cisco 7960 phones.

### Excluded addresses

| Range | Reason |
|-------|--------|
| 10.57.184.1 – 10.57.184.15 | Router gateway + static devices |
| 10.57.188.1 – 10.57.188.15 | Router gateway + static devices |
| 10.57.180.1 – 10.57.180.70 | Router gateway + static devices |

---

## VoIP Service

The T4-Router provides Cisco Telephony Service for the local VoIP network (VLAN 777).

| Phone | Number | MAC Address |
|-------|--------|-------------|
| T4-Phone-1 | 4000 | 0010.1146.C6AD |
| T4-Phone-2 | 4001 | 0001.438A.A570 |

### Call forwarding to other terminals

| Prefix | Destination | Next-hop |
|--------|-------------|----------|
| 2... | Terminal 2 | 10.57.128.2 |
| 3... | Terminal 3 | 10.57.128.3 |
| 5... | Terminal 5 | 10.57.128.5 |

---

## HTTP Server

A second server was added to the DMZ network to run the HTTP/HTTPS service.

| Device | VLAN | IP | Mask | Gateway |
|--------|------|----|------|---------|
| T4-Server (DNS) | 778 | 10.57.190.10 | 255.255.255.128 | 10.57.190.1 |
| T4-Server-HTTP | 778 | 10.57.190.20 | 255.255.255.128 | 10.57.190.1 |

---

## DNS Configuration

| DNS Domain | terminal-4.rcomp-25-26-dd-g1 |
|------------|-------------------------------|
| DNS Server | ns.terminal-4.rcomp-25-26-dd-g1 |
| DNS Server IP | 10.57.190.10 |

### DNS Records

| Type | Name | Value |
|------|------|-------|
| A | ns.terminal-4.rcomp-25-26-dd-g1 | 10.57.190.10 |
| A | server1.terminal-4.rcomp-25-26-dd-g1 | 10.57.190.20 |
| A | ns.rcomp-25-26-dd-g1 | 10.57.158.10 |
| CNAME | www.terminal-4.rcomp-25-26-dd-g1 | server1.terminal-4.rcomp-25-26-dd-g1 |
| CNAME | web.terminal-4.rcomp-25-26-dd-g1 | server1.terminal-4.rcomp-25-26-dd-g1 |
| CNAME | dns.terminal-4.rcomp-25-26-dd-g1 | ns.terminal-4.rcomp-25-26-dd-g1 |
| NS | terminal-4.rcomp-25-26-dd-g1 | ns.terminal-4.rcomp-25-26-dd-g1 |
| NS | rcomp-25-26-dd-g1 | ns.rcomp-25-26-dd-g1 |

**Note:** All end-nodes within Terminal 4 are configured to use 10.57.190.10 as the DNS server, with default domain name terminal-4.rcomp-25-26-dd-g1.

---

## NAT (Network Address Translation)

Static NAT rules redirect HTTP and HTTPS traffic received on the router's backbone interface to the DNS server in the local DMZ.

| Protocol | Outside (Backbone) | Inside (DMZ) |
|----------|--------------------|--------------|
| TCP/80 (HTTP) | 10.57.128.4:80 | 10.57.190.10:80 |
| TCP/443 (HTTPS) | 10.57.128.4:443 | 10.57.190.10:443 |

---

## Static Firewall (ACLs)

ACLs were configured on the T4-Router to enforce traffic access policies.

| ACL | Applied to | Direction | Purpose |
|-----|-----------|-----------|---------|
| BACKBONE-IN | Fa0/0.761 | Inbound | Anti-spoofing, allow required services, block router access |
| SPOOF-IN | Fa0/0.775, .776, .777 | Inbound | Block internal spoofing |
| DMZ-IN | Fa0/0.778 | Outbound | Allow only DNS and HTTP/HTTPS to DMZ |
| DMZ-OUT | Fa0/0.778 | Inbound | Allow all traffic from DMZ |