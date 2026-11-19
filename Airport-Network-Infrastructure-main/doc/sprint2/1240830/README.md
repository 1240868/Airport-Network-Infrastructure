# RCOMP 2025-2026 Project 1 - Sprint 2 - Member 1240830 folder

### Terminal 4 — Task T.2.4

## T4-Router Sub-interfaces

| Sub-interface | VLAN | Network | Gateway |
| :--- | :--- | :--- | :--- |
| Fa0/0.761 | 761 - Backbone | 10.57.128.0/24 | 10.57.128.4 |
| Fa0/0.762 | 762 - Switches DMZ | 10.57.130.0/23 | 10.57.130.1 |
| Fa0/0.775 | 775 - User Outlets | 10.57.184.0/22 | 10.57.184.1 |
| Fa0/0.776 | 776 - Wi-Fi | 10.57.180.0/21 | 10.57.180.1 |
| Fa0/0.777 | 777 - VoIP | 10.57.188.0/23 | 10.57.188.1 |
| Fa0/0.778 | 778 - Servers DMZ | 10.57.190.0/25 | 10.57.190.1 |

---

## Network Justification

| VLAN | Required nodes | Network | Mask | Usable hosts | Justification |
|------|----------------|---------|------|--------------|---------------|
| 775 - User Outlets | 800 | 10.57.184.0/22 | 255.255.252.0 | 1022 | /22 is the smallest block supporting 800 hosts. Moved to 10.57.184.0 due to a Packet Tracer bug causing a false overlap between 10.57.176.0/22 and 10.57.180.0/21 |
| 776 - Wi-Fi | 1800 | 10.57.180.0/21 | 255.255.248.0 | 2046 | /21 is the smallest block supporting 1800 hosts |
| 777 - VoIP | 400 | 10.57.188.0/23 | 255.255.254.0 | 510 | /23 is the smallest block supporting 400 hosts |
| 778 - Servers DMZ | 120 | 10.57.190.0/25 | 255.255.255.128 | 126 | /25 is the smallest block supporting 120 hosts |

The base block assigned to Terminal 4 in planning.md is `10.57.176.0/20`. All subnets above were allocated within this block, respecting non-overlapping with other terminals.

---

## Terminal 4 End-Devices IP Table

| Device | VLAN | IP | Mask | Gateway | Justification |
|--------|------|-----|------|---------|---------------|
| T4-PC-775 (User Outlets Floor 0) | 775 | 10.57.184.10 | 255.255.252.0 | 10.57.184.1 | Network 10.57.184.0/22, gateway is the router on sub-interface Fa0/0.775 |
| T4-PC-775 (User Outlets Floor 2) | 775 | 10.57.184.11 | 255.255.252.0 | 10.57.184.1 | Network 10.57.184.0/22, gateway is the router on sub-interface Fa0/0.775 |
| T4-Laptop-WiFi (Floor 0) | 776 | 10.57.180.50 | 255.255.248.0 | 10.57.180.1 | Network 10.57.180.0/21, gateway is the router on sub-interface Fa0/0.776 |
| T4-Laptop-WiFi (Floor 2) | 776 | 10.57.180.51 | 255.255.248.0 | 10.57.180.1 | Network 10.57.180.0/21, gateway is the router on sub-interface Fa0/0.776 |
| T4-Server | 778 | 10.57.190.10 | 255.255.255.128 | 10.57.190.1 | Network 10.57.190.0/25, gateway is the router on sub-interface Fa0/0.778 |
| T4-PC-762 (Switches DMZ) | 762 | 10.57.130.150 | 255.255.254.0 | — | Switches DMZ network (10.57.130.0/23). Last IP of T4 range (10.57.130.101-150) |

---

## Static Routing configured on T4-Router

| Destination network | Mask | Via (next-hop) | Reason |
|---------------------|------|----------------|--------|
| 10.57.144.0/20 | 255.255.240.0 | 10.57.128.2 | T2 block (10.57.144.0/20), T2 router is at 10.57.128.2 |
| 10.57.160.0/20 | 255.255.240.0 | 10.57.128.3 | T3 block (10.57.160.0/20), T3 router is at 10.57.128.3 |
| 10.57.192.0/19 | 255.255.224.0 | 10.57.128.5 | T5 block (10.57.192.0/19), T5 router is at 10.57.128.5 |
| 0.0.0.0/0 | 0.0.0.0 | 10.57.128.2 | Default route to internet, via T2 router which has the ISP connection |

**Note:** The network `10.57.176.0/20` (T4 block) is directly connected and requires no static route. The Switches DMZ network (`10.57.130.0/23`) is isolated and has no routing configured.

---

## Terminal 4 Switch IP Table (Switches DMZ - VLAN 762)

As planned in planning.md, the Switches DMZ network is `10.57.130.0/23` and the range reserved for Terminal 4 is `10.57.130.101 – 10.57.130.150`.

| Switch | IP | Mask | Justification |
|--------|-----|------|---------------|
| T4-IC | 10.57.130.101 | 255.255.254.0 | First IP of T4 range (IC - Intermediate Cross-Connect) |
| T4-HC-Floor0 | 10.57.130.102 | 255.255.254.0 | Second IP of T4 range (HC Floor 0) |
| T4-HC-Floor2 | 10.57.130.103 | 255.255.254.0 | Third IP of T4 range (HC Floor 2) |

**Note:** All IPs are within the `10.57.130.0/23` network. The mask `255.255.254.0` (/23) must be used on all switches. No gateway is configured as this network is isolated (no routing).