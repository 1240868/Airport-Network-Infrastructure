RCOMP 2025-2026 Project 1 - Sprint 2 - Member 1240850 folder
===========================================

### Terminal 3 — Task T.2.2 ###

## T3-Router Sub-interfaces

| Sub-interface | VLAN | Network | Gateway |
| :--- | :--- | :--- | :--- |
| Fa0/0.1 | 761 - Backbone | 10.57.128.0/24 | 10.57.128.3 |
| Fa0/0.2 | 767 - User Outlets | 10.57.168.0/22 | 10.57.168.1 |
| Fa0/0.3 | 768 - Wi-Fi | 10.57.160.0/21 | 10.57.160.1 |
| Fa0/0.4 | 769 - VoIP | 10.57.172.0/23 | 10.57.172.1 |
| Fa0/0.5 | 770 - Servers DMZ | 10.57.174.0/24 | 10.57.174.1 |

---

## Network Sizing Justification

The base block assigned to Terminal 3 in planning.md is `10.57.160.0/20`. All sub-networks were allocated within this block, respecting non-overlapping with other terminals.

| VLAN | Required Nodes | Network | Mask | Usable Hosts | Justification |
|---|---|---|---|---|---|
| 768 - Wi-Fi | 1500 | 10.57.160.0/21 | 255.255.248.0 | 2046 | /21 is the smallest block supporting 1500 hosts. Allocated first as the largest network. |
| 767 - User Outlets | 950 | 10.57.168.0/22 | 255.255.252.0 | 1022 | /22 is the smallest block supporting 950 hosts. |
| 769 - VoIP | 350 | 10.57.172.0/23 | 255.255.254.0 | 510 | /23 is the smallest block supporting 350 hosts. |
| 770 - Servers DMZ | 150 | 10.57.174.0/24 | 255.255.255.0 | 254 | /24 is the smallest block supporting 150 hosts. |

---

## End-Devices IP Table

All devices (except VoIP phones) have a **static** IPv4 configuration.

| Device | VLAN | IP Address | Mask | Gateway | Justification |
|---|---|---|---|---|---|
| PC0 (User Outlets) | 767 | 10.57.168.10 | 255.255.252.0 | 10.57.168.1 | Network 10.57.168.0/22, gateway is the router on sub-interface Fa0/0.2 |
| PC1 (User Outlets) | 767 | 10.57.168.11 | 255.255.252.0 | 10.57.168.1 | Network 10.57.168.0/22, gateway is the router on sub-interface Fa0/0.2 |
| Laptop0 (Wi-Fi) | 768 | 10.57.160.10 | 255.255.248.0 | 10.57.160.1 | Network 10.57.160.0/21, gateway is the router on sub-interface Fa0/0.3 |
| Laptop1 (Wi-Fi) | 768 | 10.57.160.11 | 255.255.248.0 | 10.57.160.1 | Network 10.57.160.0/21, gateway is the router on sub-interface Fa0/0.3 |
| Server0 (Servers DMZ) | 770 | 10.57.174.10 | 255.255.255.0 | 10.57.174.1 | Network 10.57.174.0/24, gateway is the router on sub-interface Fa0/0.5 |
| PC_Switch (Switches DMZ) | 762 | 10.57.130.60 | 255.255.254.0 | — | Switches DMZ network (10.57.130.0/23), isolated network with no gateway |
| IP Phone0 | 769 | — | — | — | IP configuration deferred to Sprint 3 |
| IP Phone1 | 769 | — | — | — | IP configuration deferred to Sprint 3 |

---

## Static Routing configured on T3-Router

| Destination Network | Mask | Via (Next-Hop) | Description |
|---|---|---|---|
| 10.57.128.0/17 | 255.255.128.0 | 10.57.128.2 | Full team block, via T2 router |
| 10.57.144.0/20 | 255.255.240.0 | 10.57.128.2 | Terminal 2 block (T2-Router at 10.57.128.2) |
| 10.57.176.0/20 | 255.255.240.0 | 10.57.128.4 | Terminal 4 block (T4-Router at 10.57.128.4) |
| 10.57.192.0/19 | 255.255.224.0 | 10.57.128.5 | Terminal 5 block (T5-Router at 10.57.128.5) |
| 0.0.0.0/0 | 0.0.0.0 | 10.57.128.2 | Default route for Internet, via T2 router which has the ISP connection |

**Note:** The network `10.57.160.0/20` (T3 block) is directly connected and requires no static route. The Switches DMZ network (`10.57.130.0/23`) is isolated and has no routing configured.

---

## Switch IP Table (Switches DMZ - VLAN 762)

The range reserved for Terminal 3 in the Switches DMZ (`10.57.130.0/23`) is `10.57.130.51 – 10.57.130.100`.

| Switch | IP Address | Mask | Justification |
|---|---|---|---|
| T3-IC | 10.57.130.51 | 255.255.254.0 | First IP of T3 range (IC - Intermediate Cross-Connect) |
| T3-HC-L0 | 10.57.130.52 | 255.255.254.0 | Second IP of T3 range (HC Floor 0) |
| T3-HC-L1 | 10.57.130.53 | 255.255.254.0 | Third IP of T3 range (HC Floor 1) |

**Note:** All IPs are within the `10.57.130.0/23` network. The mask `255.255.254.0` (/23) must be used on all switches. No gateway is configured as this network is isolated (no routing).