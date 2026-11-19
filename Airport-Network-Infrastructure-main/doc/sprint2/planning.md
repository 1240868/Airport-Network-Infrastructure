RCOMP 2025-2026 Project 1 - Sprint 2 planning
===========================================
### Sprint master: 1240835 ###

# 1. Sprint's backlog #

| Task  | Task description                                                                                                                                                                                                |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| T.2.1 | Development of a layer two and layer three Packet Tracer simulation for Terminal 2 encompassed floors, the campus backbone, and including the internet connection                                               |
| T.2.2 | Development of a layer two and layer three Packet Tracer simulation for Terminal 3 encompassed floors and the campus backbone. Integration of every member's Packet Tracer simulation into a single simulation. |
| T.2.3 | Development of a layer two and layer three Packet Tracer simulation for Terminal 5 encompassed floors and the campus backbone.                                                                                  |
| T.2.4 | Development of a layer two and layer three Packet Tracer simulation for Terminal 4 encompassed floors and the campus backbone.                                                                                  |

#### Sprint 2 outputs/products ####

For each task on this sprint, the main output is the Packet Tracer simulation file for the corresponding
terminal, it should be named TerminalN.pkt, with N replaced by the number identifying the terminal.
Each team member is to commit that file into the personal sprint folder at the repository.

A document (in any standard format) detailing how IPv4 network addresses were established and how
static routing tables were created is also required.

Each team member must also commit to the personal sprint folder a text file with a configuration dump
for every switch and every router within the encompassed terminal. These configuration text files can be
easily exported in Packet Tracer: within the device's window click the export button on the Running
Config, or the Startup Config (if the Running Config has been saved).

The default name for the text file may be kept, as it represents the device's display name. During the
sprint, members are to commit changes to these files as change are made to their devices' configurations,
this allows the teacher to follow the progresses along the sprint. These files are also a safeguard, if
somehow the configuration of a device in Packet Tracer is lost, it may be restored from these files.

For task T.2.2 there is one additional output to be committed into the personal sprint folder, it is the
overall simulation integrating all members work, that file should be named campus.pkt. Regarding
configuration files, for task T.2.2, they only encompass the devices in Terminal 3.

---

# 2. Technical decisions and coordination #

## Packet Tracer version ##
Version 9.0.0

## Devices naming ##
- Switches: `T<terminal>-<level>-<id>` (e.g., `T2-MC`, `T2-IC-L0`)
    - MC = Main Cross-Connect, IC = Intermediate Cross-Connect
- Routers: `T<terminal>-Router` (e.g., `T2-Router`)
- End devices: `T<terminal>-PC-<vlan>`, `T<terminal>-Laptop-WiFi`, `T<terminal>-Server`, `T<terminal>-Phone`
- Hostnames (no spaces): same pattern with hyphens only

## VTP domain ##
`rc2526ddg1`

## VLAN IDs ##

Total of 18 VLANs (2 shared + 4 terminals × 4 VLANs each). Default VLAN 1 is kept as native/default.

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

All VLANs must be present in every switch's VLAN database across all terminals.
All inter-switch links must be configured in trunk mode carrying all VLANs.
VTP mode: one switch per terminal acts as server, remaining switches as clients.

## IPv4 addressing ##

Address space assigned to the team: `10.57.128.0/17` (10.57.128.0 – 10.57.255.255)
ISP router IPv4 node address: `89.73.67.86/30`

### Shared networks ###

| Network         | Address        | Mask              | Usable hosts | VLAN ID |
|-----------------|----------------|-------------------|--------------|---------|
| Campus Backbone | 10.57.128.0/24 | 255.255.255.0     | 254          | 761     |
| Switches DMZ    | 10.57.130.0/23 | 255.255.254.0     | 510          | 762     |

### Address blocks assigned per terminal ###

| Terminal | Block          | Mask              | Usable hosts |
|----------|----------------|-------------------|--------------|
| T2       | 10.57.144.0/20 | 255.255.240.0     | 4094         |
| T3       | 10.57.160.0/20 | 255.255.240.0     | 4094         |
| T4       | 10.57.176.0/20 | 255.255.240.0     | 4094         |
| T5       | 10.57.192.0/19 | 255.255.224.0     | 8190         |

### Router IP addresses on Campus Backbone (VLAN 761 – 10.57.128.0/24) ###

| Terminal | Router IP       |
|----------|-----------------|
| T2       | 10.57.128.2     |
| T3       | 10.57.128.3     |
| T4       | 10.57.128.4     |
| T5       | 10.57.128.5     |

### Switch IP ranges on Switches DMZ (VLAN 762 – 10.57.130.0/23) ###

| Terminal | Reserved range                    |
|----------|-----------------------------------|
| Backbone (MC) | 10.57.130.201 – 10.57.130.254 |
| T2       | 10.57.130.1   – 10.57.130.50      |
| T3       | 10.57.130.51  – 10.57.130.100     |
| T4       | 10.57.130.101 – 10.57.130.150     |
| T5       | 10.57.130.151 – 10.57.130.200     |

### Tabela de IPs dos Switches (Switches DMZ - VLAN 762) ###

| Terminal | Dispositivo | Nome     | IP Address |
|----------|-------------|----------|-------------|
| Backbone | MC | T2-MC    | 10.57.130.201 |
| T2 | IC | T2-IC    | 10.57.130.1 |
| T2 | HC Piso 0 | T2-HC-L0 | 10.57.130.2 |
| T2 | HC Piso 1 | T2-HC-L1 | 10.57.130.3 |
| T3 | IC | T3-IC    | 10.57.130.51 |
| T3 | HC Piso 0 | T3-HC-L0 | 10.57.130.52 |
| T3 | HC Piso 1 | T3-HC-L1 | 10.57.130.53 |
| T4 | IC | T4-IC    | 10.57.130.101 |
| T4 | HC Piso 0 | T4-HC-L0 | 10.57.130.102 |
| T4 | HC Piso 1 | T4-HC-L1 | 10.57.130.103 |
| T5 | IC | T5-IC    | 10.57.130.151 |
| T5 | HC Piso 0 | T5-HC-L0 | 10.57.130.152 |
| T5 | HC Piso 2 | T5-HC-L2 | 10.57.130.153 |

---

# 3. Subtasks assignment #

| Student | Task  | Terminal |
|---------|-------|----------|
| 1240868 | T.2.1 | Terminal 2 (+ internet connection) |
| 1240850 | T.2.2 | Terminal 3 (+ campus.pkt integration) |
| 1240835 | T.2.3 | Terminal 5 |
| 1240830 | T.2.4 | Terminal 4 |