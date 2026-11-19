# RCOMP 2025-2026 Project 1 - Sprint 2 - Member 1240835

### Terminal 5 — Task T.2.3 ###

## 1. Sub-interfaces do T5-Router

The router used is the **Cisco 2811** model. The connection to the T5-IC switch is established via a single cable in **trunk mode**, utilizing logical sub-interfaces for inter-VLAN routing (Router-on-a-Stick).

| Sub-interface | VLAN | Use | IPv4 Network | Gateway |
| :--- | :--- | :--- | :--- | :--- |
| Fa0/0.761 | 761 | Campus Backbone | 10.57.128.0/24 | 10.57.128.5 |
| Fa0/0.771 | 771 | T5 - User Outlets | 10.57.208.0/21 | 10.57.208.1 |
| Fa0/0.772 | 772 | T5 - Wi-Fi | 10.57.192.0/20 | 10.57.192.1 |
| Fa0/0.773 | 773 | T5 - VoIP | 10.57.216.0/23 | 10.57.216.1 |
| Fa0/0.774 | 774 | T5 - Servers DMZ | 10.57.218.0/24 | 10.57.218.1 |

---

## 2. Network Sizing Justification

The sub-networks were calculated to support the maximum number of required nodes while using the smallest possible prefix. The base block assigned to Terminal 5 is `10.57.192.0/19`.

| VLAN | Required Nodes | Network | Mask | Usable Hosts | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 772 - Wi-Fi | 4000 | 10.57.192.0/20 | 255.255.240.0 | 4094 | /20 is the smallest block supporting 4000 nodes. Allocated first as the largest network. |
| 771 - User Outlets | 1900 | 10.57.208.0/21 | 255.255.248.0 | 2046 | /21 is the smallest block supporting 1900 nodes. |
| 773 - VoIP | 500 | 10.57.216.0/23 | 255.255.254.0 | 510 | /23 is the smallest block supporting 500 nodes. |
| 774 - Servers DMZ | 200 | 10.57.218.0/24 | 255.255.255.0 | 254 | /24 is the smallest block supporting 200 nodes. |

The base block `10.57.192.0/19` covers `10.57.192.0 – 10.57.223.255`. All sub-networks above are allocated within this block with no overlaps.

---

## 3. End-Devices IP Table

According to the project rules, all devices (except VoIP phones) have a **static** IPv4 configuration.

| Level | Device | VLAN | IP Address | Mask | Gateway | Method |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **L0** | T5-L0-User | 771 | 10.57.208.10 | 255.255.248.0 | 10.57.208.1 | Static |
| **L0** | T5-L0-Laptop | 772 | 10.57.192.10 | 255.255.240.0 | 10.57.192.1 | Static |
| **L0** | T5-L0-Phone | 773 | — | — | — | DHCP* |
| **L0** | T5-L0-Server | 774 | 10.57.218.10 | 255.255.255.0 | 10.57.218.1 | Static |
| **L2** | T5-L2-User | 771 | 10.57.208.20 | 255.255.248.0 | 10.57.208.1 | Static |
| **L2** | T5-L2-Laptop | 772 | 10.57.192.20 | 255.255.240.0 | 10.57.192.1 | Static |
| **L2** | T5-L2-Phone | 773 | — | — | — | DHCP* |
| **L2** | T5-L2-Server | 774 | 10.57.218.20 | 255.255.255.0 | 10.57.218.1 | Static |
| **DMZ** | T5-PC-switches-dmz | 762 | 10.57.130.200 | 255.255.254.0 | — | Static |

*\*Note: IPv4 configuration for VoIP phones (model 7960) is out of scope for this sprint.*

---

## 4. Static Routing (T5-Router)

| Destination Network | Mask | Via (Next-Hop) | Description |
| :--- | :--- | :--- | :--- |
| 10.57.144.0/20 | 255.255.240.0 | 10.57.128.2 | Terminal 2 block (T2-Router at 10.57.128.2). |
| 10.57.160.0/20 | 255.255.240.0 | 10.57.128.3 | Terminal 3 block (T3-Router at 10.57.128.3). |
| 10.57.176.0/20 | 255.255.240.0 | 10.57.128.4 | Terminal 4 block (T4-Router at 10.57.128.4). |
| 0.0.0.0/0 | 0.0.0.0 | 10.57.128.2 | Default route for Internet via T2 (only terminal with ISP connection). |

**Note:** The network `10.57.192.0/19` (T5 block) is directly connected and does not require a static route. The Switches DMZ network (`10.57.130.0/23`) is isolated and has no routing configured.

---

## 5. Switches IP Table (Switches DMZ - VLAN 762)

The range reserved for Terminal 5 in the Switches DMZ (`10.57.130.0/23`) is `10.57.130.151 – 10.57.130.200`.

| Switch | IP Address | Mask | Justification |
| :--- | :--- | :--- | :--- |
| T5-IC | 10.57.130.151 | 255.255.254.0 | First IP of T5 range (IC - Intermediate Cross-Connect). |
| T5-HC-L0 | 10.57.130.152 | 255.255.254.0 | Second IP of T5 range (HC Level 0). |
| T5-HC-L2 | 10.57.130.153 | 255.255.254.0 | Third IP of T5 range (HC Level 2). |

**Note:** No gateway is configured on switches as the Switches DMZ is an isolated management network with no routing.