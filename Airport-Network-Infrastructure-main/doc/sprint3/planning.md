RCOMP 2025-2026 Project 1 - Sprint 3 planning
===========================================
### Sprint master: 1240850 ###
(This file is to be created/edited by the sprint master only)

# 1. Sprint's backlog #

| Task  | Task description                                                                                                                                                                                                                      |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| T.3.1 | Update the Terminal2.pkt layer three Packet Tracer simulation from the previous sprint, to include the described features in this sprint for Terminal 2.                                                                              |
| T.3.2 | Update the Terminal3.pkt layer three Packet Tracer simulation from the previous sprint, to include the described features in this sprint for Terminal 3. Final integration of each member's Packet Tracer simulation into a single simulation (campus.pkt). |
| T.3.3 | Update the Terminal5.pkt layer three Packet Tracer simulation from the previous sprint, to include the described features in this sprint for Terminal 5.                                                                              |
| T.3.4 | Update the Terminal4.pkt layer three Packet Tracer simulation from the previous sprint, to include the described features in this sprint for Terminal 4.                                                                              |

#### Sprint 3 outputs/products ####

For each task on this sprint, the main output is the Packet Tracer simulation file for the corresponding
terminal, it should be named TerminalN.pkt, with N replaced by the number identifying the terminal.
Each team member is to commit that file into the personal sprint folder.

A document (any standard format) detailing DNS databases records on the terminal's DNS name server
is also required (may be a screenshot of the server's DNS database).

Each team member must also commit to the personal sprint folder a text file with configuration dumps
for every switch and every router within the encompassed terminal. These configuration text files can be
easily exported in Packet Tracer: within the device's window click the export button on the Running
Config, or the Startup Config (if the Running Config has been saved).

For task T.3.2 there is one additional output to be committed into the personal sprint folder: the overall
simulation integrating all members work, named campus.pkt. Regarding configuration files and other
configuration details, for task T.3.2, they only encompass devices from Terminal 3.

---

# 2. Technical decisions and coordination #

## Packet Tracer version ##
Version 9.0.0

## Devices naming ##
- Switches: `T<terminal>-<level>-<id>` (e.g., `T2-MC`, `T2-IC-L0`)
    - MC = Main Cross-Connect, IC = Intermediate Cross-Connect
- Routers: `T<terminal>-Router` (e.g., `T2-Router`)
- End devices: `T<terminal>-PC-<vlan>`, `T<terminal>-Laptop-WiFi`, `T<terminal>-Server`, `T<terminal>-Phone`
- New HTTP servers: `T<terminal>-Server-HTTP`
- Hostnames (no spaces): same pattern with hyphens only

## VTP domain ##
`rc2526ddg1`

## VLAN IDs ##

| VLAN ID | Name         | Use                          |
|---------|--------------|------------------------------|
| 761     | backbone     | Campus Backbone (shared)     |
| 762     | switches-dmz | Switches DMZ (shared)        |
| 763     | T2-users     | Terminal 2 – User Outlets    |
| 764     | T2-wifi      | Terminal 2 – Wi-Fi           |
| 765     | T2-voip      | Terminal 2 – VoIP            |
| 766     | T2-servers   | Terminal 2 – Servers DMZ     |
| 767     | T3-users     | Terminal 3 – User Outlets    |
| 768     | T3-wifi      | Terminal 3 – Wi-Fi           |
| 769     | T3-voip      | Terminal 3 – VoIP            |
| 770     | T3-servers   | Terminal 3 – Servers DMZ     |
| 771     | T5-users     | Terminal 5 – User Outlets    |
| 772     | T5-wifi      | Terminal 5 – Wi-Fi           |
| 773     | T5-voip      | Terminal 5 – VoIP            |
| 774     | T5-servers   | Terminal 5 – Servers DMZ     |
| 775     | T4-users     | Terminal 4 – User Outlets    |
| 776     | T4-wifi      | Terminal 4 – Wi-Fi           |
| 777     | T4-voip      | Terminal 4 – VoIP            |
| 778     | T4-servers   | Terminal 4 – Servers DMZ     |
| 1       | default      | Default VLAN (native/unused) |

## IPv4 addressing ##

Address space assigned to the team: `10.57.128.0/17` (10.57.128.0 – 10.57.255.255)
ISP router IPv4 node address: `89.73.67.86/30`

### Shared networks ###

| Network         | Address        | Mask          | Usable hosts | VLAN ID |
|-----------------|----------------|---------------|--------------|---------|
| Campus Backbone | 10.57.128.0/24 | 255.255.255.0 | 254          | 761     |
| Switches DMZ    | 10.57.130.0/23 | 255.255.254.0 | 510          | 762     |

### Address blocks assigned per terminal ###

| Terminal | Block           | Mask          | Usable hosts |
|----------|-----------------|---------------|--------------|
| T2       | 10.57.144.0/20  | 255.255.240.0 | 4094         |
| T3       | 10.57.160.0/20  | 255.255.240.0 | 4094         |
| T4       | 10.57.176.0/20  | 255.255.240.0 | 4094         |
| T5       | 10.57.192.0/19  | 255.255.224.0 | 8190         |

### Router IP addresses on Campus Backbone (VLAN 761 – 10.57.128.0/24) ###

| Terminal | Router IP   |
|----------|-------------|
| T2       | 10.57.128.2 |
| T3       | 10.57.128.3 |
| T4       | 10.57.128.4 |
| T5       | 10.57.128.5 |

### Switch IP ranges on Switches DMZ (VLAN 762 – 10.57.130.0/23) ###

| Terminal       | Reserved range                      |
|----------------|-------------------------------------|
| Backbone (MC)  | 10.57.130.201 – 10.57.130.254       |
| T2             | 10.57.130.1   – 10.57.130.50        |
| T3             | 10.57.130.51  – 10.57.130.100       |
| T4             | 10.57.130.101 – 10.57.130.150       |
| T5             | 10.57.130.151 – 10.57.130.200       |

### Switch IP addresses (Switches DMZ - VLAN 762) ###

| Terminal | Device    | Name     | IP Address    |
|----------|-----------|----------|---------------|
| Backbone | MC        | T2-MC    | 10.57.130.201 |
| T2       | IC        | T2-IC    | 10.57.130.1   |
| T2       | HC Piso 0 | T2-HC-L0 | 10.57.130.2   |
| T2       | HC Piso 1 | T2-HC-L1 | 10.57.130.3   |
| T3       | IC        | T3-IC    | 10.57.130.51  |
| T3       | HC Piso 0 | T3-HC-L0 | 10.57.130.52  |
| T3       | HC Piso 1 | T3-HC-L1 | 10.57.130.53  |
| T4       | IC        | T4-IC    | 10.57.130.101 |
| T4       | HC Piso 0 | T4-HC-L0 | 10.57.130.102 |
| T4       | HC Piso 1 | T4-HC-L1 | 10.57.130.103 |
| T5       | IC        | T5-IC    | 10.57.130.151 |
| T5       | HC Piso 0 | T5-HC-L0 | 10.57.130.152 |
| T5       | HC Piso 2 | T5-HC-L2 | 10.57.130.153 |

---

## OSPF dynamic routing ##

Static routing is replaced by OSPF. The overall infrastructure forms a single OSPF Autonomous System,
split into areas — one per terminal plus the backbone area (area 0).
The default route at Terminal 2's router (pointing to the ISP) must be kept and redistributed into OSPF
using the `default-information originate` command.

### OSPF Area IDs ###

| Network / Terminal | OSPF Area ID |
|--------------------|-------------|
| Campus Backbone    | 0           |
| T2                 | 1           |
| T3                 | 2           |
| T4                 | 3           |
| T5                 | 4           |

---

## VoIP phone numbers and prefix digits schema ##

Each terminal uses a unique prefix digit. Phone numbers within a terminal follow the pattern `<prefix><extension>`.
Call forwarding between terminals is based on the prefix digit.

| Terminal | Prefix digit | Local phone numbers |
|----------|-------------|---------------------|
| T2       | 2           | 2000, 2001          |
| T3       | 3           | 3000, 3001          |
| T4       | 4           | 4000, 4001          |
| T5       | 5           | 5000, 5001          |

DHCP option 150 (TFTP server address) must be set in each terminal's VoIP VLAN DHCP pool,
pointing to the terminal's own router IPv4 address on the backbone interface.

---

## DNS domains ##

The highest-level domain matches the team's repository name and is managed by Terminal 2.
All other terminals manage subdomains of this root domain.

| Terminal | DNS Domain name              |
|----------|------------------------------|
| T2       | rcomp-25-26-dd-g1            |
| T3       | terminal-3.rcomp-25-26-dd-g1 |
| T4       | terminal-4.rcomp-25-26-dd-g1  |
| T5       | terminal-5.rcomp-25-26-dd-g1 |

### DNS Name Servers (ns) IPv4 addresses ###

The DNS name server of each domain has the unqualified name `ns` within its domain.
The server used is the one already present in each terminal's DMZ from the previous sprint.

| Terminal | FQDN                            | IPv4 Address  |
|----------|---------------------------------|---------------|
| T2       | ns.rcomp-25-26-dd-g1            | 10.57.158.10  |
| T3       | ns.terminal-3.rcomp-25-26-dd-g1 | 10.57.174.10  |
| T4       | ns.terminal-4.rcomp-25-26-dd-g1 | 10.57.190.10  |
| T5       | ns.terminal-5.rcomp-25-26-dd-g1 | 10.57.218.10  |

These IPv4 addresses correspond to the servers already present in each terminal's Servers DMZ (VLAN)
from Sprint 2. These servers will now also act as DNS name servers for their respective domains.

### DNS records required in each terminal ###

Each terminal's DNS database must contain the following records:

| Record type | Name       | Value / Target                        |
|-------------|------------|---------------------------------------|
| A           | ns         | IPv4 address of the DNS server        |
| A           | server1    | IPv4 address of the HTTP server       |
| CNAME       | www        | server1.\<local-domain\>              |
| CNAME       | web        | server1.\<local-domain\>              |
| CNAME       | dns        | ns.\<local-domain\>                   |
| NS + A (glue) | (subdomains, T2 only) | NS and IPv4 of each subdomain's ns |
| NS + A (glue) | rcomp-25-26-cc-gn (all except T2) | NS and IPv4 of root ns |

All names in DNS databases must be FQDNs ending in `rcomp-25-26-cc-gn`.

---

# 3. Subtasks assignment #

| Student | Task  | Terminal                                    |
|---------|-------|---------------------------------------------|
| 1240868 | T.3.1 | Terminal 2                                  |
| 1240850 | T.3.2 | Terminal 3 (+ campus.pkt integration)       |
| 1240835 | T.3.3 | Terminal 5                                  |
| 1240830 | T.3.4 | Terminal 4                                  |