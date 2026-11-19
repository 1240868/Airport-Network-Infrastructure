RCOMP 2025-2026 Project 1 - Sprint 3 - Member 1240850 folder
===========================================

## Índice

1. [Dispositivos do Terminal 3](#1-dispositivos-do-terminal-3)
2. [OSPF Dynamic Routing](#2-ospf-dynamic-routing)
3. [Servidor HTTP adicional na DMZ](#3-servidor-http-adicional-na-dmz)
4. [Serviço DHCPv4](#4-serviço-dhcpv4)
5. [Serviço VoIP (Cisco Telephony)](#5-serviço-voip-cisco-telephony)
6. [Servidor DNS](#6-servidor-dns)
7. [NAT (Network Address Translation)](#7-nat-network-address-translation)
8. [Static Firewall (ACLs)](#8-static-firewall-acls)
---

## 1. Dispositivos do Terminal 3

| Dispositivo | Modelo | Nome | VLAN | IP | Função |
|-------------|--------|------|------|----|--------|
| Router | Cisco 2811 | T3-Router | Várias | Ver abaixo | Router do terminal |
| Switch IC | Switch-PT-Empty | T3-IC | 762 (gestão) | 10.57.130.51/23 | Switch intermédio |
| Switch HC Piso 0 | Switch-PT-Empty | T3-HC-L0 | 762 (gestão) | 10.57.130.52/23 | Switch acesso piso 0 |
| Switch HC Piso 1 | Switch-PT-Empty | T3-HC-L1 | 762 (gestão) | 10.57.130.53/23 | Switch acesso piso 1 |
| Servidor DNS | Server-PT | T3-Server | 770 (DMZ) | 10.57.174.10/24 | DNS + HTTP |
| Servidor HTTP | Server-PT | T3-Server-HTTP | 770 (DMZ) | 10.57.174.11/24 | HTTP (server1) |
| Access Point Piso 0 | AccessPoint-PT | T3-AP-L0 | 768 (WiFi) | — | Ponto acesso WiFi |
| Access Point Piso 1 | AccessPoint-PT | T3-AP-L1 | 768 (WiFi) | — | Ponto acesso WiFi |
| PC Users Piso 0 | PC-PT | T3-PC-767 | 767 (users) | DHCP | Cliente com fio |
| PC Users Piso 1 | PC-PT | T3-PC-767-L1 | 767 (users) | DHCP | Cliente com fio |
| Laptop WiFi Piso 0 | Laptop-PT | T3-Laptop-WiFi | 768 (WiFi) | DHCP | Cliente WiFi |
| Laptop WiFi Piso 1 | Laptop-PT | T3-Laptop-WiFi-L1 | 768 (WiFi) | DHCP | Cliente WiFi |
| IP Phone Piso 0 | 7960 | T3-Phone | 769 (VoIP) | DHCP | Telefone 3000 |
| IP Phone Piso 1 | 7960 | T3-Phone-L1 | 769 (VoIP) | DHCP | Telefone 3001 |
| PC Switch DMZ | PC-PT | T3-PC-DMZ | 762 (gestão) | 10.57.130.60/23 | Gestão switches |

### IPs do T3-Router por sub-interface

| Sub-interface | VLAN | IP | Máscara | Rede |
|---------------|------|----|---------|------|
| FastEthernet0/0.1 | 761 (backbone) | 10.57.128.3 | 255.255.255.0 | /24 |
| FastEthernet0/0.2 | 767 (users) | 10.57.168.1 | 255.255.252.0 | /22 |
| FastEthernet0/0.3 | 768 (WiFi) | 10.57.160.1 | 255.255.248.0 | /21 |
| FastEthernet0/0.4 | 769 (VoIP) | 10.57.172.1 | 255.255.254.0 | /23 |
| FastEthernet0/0.5 | 770 (DMZ) | 10.57.174.1 | 255.255.255.0 | /24 |
 
---

## 2. OSPF Dynamic Routing

### O que foi feito
Removeu-se o routing estático (exceto a rota default) e configurou-se OSPF como protocolo de routing dinâmico.

### Configuração aplicada
- OSPF Process ID: 1
- Área 0: rede backbone (10.57.128.0/24)
- Área 2 (Terminal 3): redes T3-users, T3-wifi, T3-voip, T3-servers
- As wildcard masks foram calculadas corretamente para cada subnet:
    - Backbone: 0.0.0.255 (/24)
    - Users: 0.0.3.255 (/22)
    - WiFi: 0.0.7.255 (/21)
    - VoIP: 0.0.1.255 (/23)
    - DMZ: 0.0.0.255 (/24)
---

## 3. Servidor HTTP adicional na DMZ

### O que foi feito
Adicionou-se um segundo servidor à DMZ local (VLAN 770), dedicado exclusivamente ao serviço HTTP/HTTPS.

### Configuração aplicada
- **Nome:** T3-Server-HTTP
- **IP:** 10.57.174.11
- **Máscara:** 255.255.255.0
- **Gateway:** 10.57.174.1
- **DNS Server:** 10.57.174.10
- **Porta no switch:** T3-HC-L0, Ethernet 6/1, configurada como access na VLAN 770
- **Serviço HTTP/HTTPS:** ativado
- **Página HTML:** criada com identificação do Terminal 3
---

## 4. Serviço DHCPv4

### O que foi feito
Configuraram-se três pools DHCP no T3-Router para atribuição automática de IPs nas VLANs 767 (users), 768 (WiFi) e 769 (VoIP). A VLAN 770 (DMZ) e 761 (backbone) mantêm configuração estática.

### Configuração aplicada

| Pool | VLAN | Rede | Máscara | Gateway | DNS | Domain | Option 150 |
|------|------|------|---------|---------|-----|--------|------------|
| T3-Users | 767 | 10.57.168.0 | /22 | 10.57.168.1 | 10.57.174.10 | terminal-3.rcomp-25-26-dd-g1 | — |
| T3-WiFi | 768 | 10.57.160.0 | /21 | 10.57.160.1 | 10.57.174.10 | terminal-3.rcomp-25-26-dd-g1 | — |
| T3-VoIP | 769 | 10.57.172.0 | /23 | 10.57.172.1 | 10.57.174.10 | terminal-3.rcomp-25-26-dd-g1 | 10.57.172.1 |

**Endereços excluídos dos pools:**
- 10.57.168.1 – 10.57.168.10 (gateway e dispositivos estáticos)
- 10.57.160.1 – 10.57.160.10 (gateway e dispositivos estáticos)
- 10.57.172.1 – 10.57.172.10 (gateway e dispositivos estáticos)
---

## 5. Serviço VoIP (Cisco Telephony)

### O que foi feito
Configurou-se o serviço de telefonia Cisco no T3-Router, atribuindo números aos dois IP Phones 7960 e criando dial-peers para encaminhamento de chamadas para outros terminais.

### Configuração aplicada
- **IP source-address do Telephony Service:** 10.57.172.1 (VoIP gateway)
- **Porto SCCP:** 2000 (padrão)
- **Max ephones:** 2 / Max dn: 2
- **Auto assign:** 1 to 2
  **Números atribuídos:**

| ephone-dn | Número | Telefone |
|-----------|--------|----------|
| 1 | 3000 | T3-Phone |
| 2 | 3001 | T3-Phone-L1 |

**Dial-peers para outros terminais (prefixos):**

| Dial-peer | Prefixo | Session Target | Terminal destino |
|-----------|---------|----------------|-----------------|
| 2 | 2... | 10.57.128.2 | Terminal 2 |
| 4 | 4... | 10.57.128.4 | Terminal 4 |
| 5 | 5... | 10.57.128.5 | Terminal 5 |

**Configuração das portas dos switches:**
- T3-HC-L0, Ethernet 2/1: `switchport voice vlan 769`, `no switchport access vlan`
- T3-HC-L1, Ethernet 2/1: `switchport voice vlan 769`, `no switchport access vlan`
---

## 6. Servidor DNS

### O que foi feito
O T3-Server (10.57.174.10) foi configurado como DNS name server do domínio `terminal-3.rcomp-25-26-dd-g1`. Foi também ativado o serviço HTTP neste servidor.

### Configuração aplicada
**Serviço DNS ativado.** Base de dados configurada com todos os registos em FQDN (a terminar em `rcomp-25-26-dd-g1`).

**Registos A (Address):**

| Nome FQDN | IP |
|-----------|----|
| ns.terminal-3.rcomp-25-26-dd-g1 | 10.57.174.10 |
| server1.terminal-3.rcomp-25-26-dd-g1 | 10.57.174.11 |
| ns.rcomp-25-26-dd-g1 | 10.57.158.10 |

**Registos CNAME (Alias):**

| Nome FQDN | Alvo |
|-----------|------|
| www.terminal-3.rcomp-25-26-dd-g1 | server1.terminal-3.rcomp-25-26-dd-g1 |
| web.terminal-3.rcomp-25-26-dd-g1 | server1.terminal-3.rcomp-25-26-dd-g1 |
| dns.terminal-3.rcomp-25-26-dd-g1 | ns.terminal-3.rcomp-25-26-dd-g1 |

**Registos NS (Name Server):**

| Domínio | Name Server |
|---------|-------------|
| rcomp-25-26-dd-g1 | ns.rcomp-25-26-dd-g1 |

**Serviço HTTP no DNS Server:** Ativado com página HTML a identificar "Terminal 3 - DNS Server".
 
---

## 7. NAT (Network Address Translation)

### O que foi feito
Configurou-se NAT estático no T3-Router para redirecionar pedidos HTTP (porta 80) e HTTPS (porta 443) recebidos na interface de backbone para o servidor DNS na DMZ.

### Configuração aplicada
- Tradução estática TCP porta 80: 10.57.174.10:80 ↔ 10.57.128.3:80
- Tradução estática TCP porta 443: 10.57.174.10:443 ↔ 10.57.128.3:443
### Interfaces e lados NAT

| Interface | VLAN | NAT Side |
|-----------|------|----------|
| FastEthernet0/0.1 | 761 (backbone) | outside |
| FastEthernet0/0.2 | 767 (users) | inside |
| FastEthernet0/0.3 | 768 (WiFi) | inside |
| FastEthernet0/0.4 | 769 (VoIP) | inside |
| FastEthernet0/0.5 | 770 (DMZ) | inside |
 
---

## 8. Static Firewall (ACLs)

### O que foi feito
Implementaram-se Access Control Lists (ACLs) no T3-Router para filtrar tráfego de acordo com as regras de precedência definidas no enunciado.

### Regras implementadas (por ordem de precedência)

**Regra 1 - Anti-spoofing:**
- Bloqueia tráfego externo (backbone) com IPs de origem internos do T3
- Bloqueia tráfego das redes locais com IPs de origem que não pertencem a essa rede
  **Regra 2 - ICMP:**
- Echo requests e echo replies são sempre permitidos em todas as ACLs
  **Regra 3 - DMZ:**
- Tráfego para a DMZ bloqueado, exceto:
    - DNS (UDP/TCP 53) para o servidor DNS (10.57.174.10)
    - HTTP (TCP 80) e HTTPS (TCP 443) para ambos os servidores (10.57.174.10 e 10.57.174.11)
- Tráfego da DMZ para fora é todo permitido
  **Regra 4 - Proteção do router:**
- Tráfego destinado a qualquer IP do router bloqueado (10.57.128.3, 10.57.160.1, 10.57.168.1, 10.57.172.1, 10.57.174.1), exceto serviços essenciais:
    - DHCP (UDP 67/68) — em todas as redes locais
    - TFTP (UDP 69) — apenas na rede VoIP
    - VoIP SCCP (TCP 2000) — apenas na rede VoIP
    - HTTP/HTTPS (TCP 80/443) — apenas na backbone (NAT)
    - OSPF — apenas na backbone
      **Regra 5 - Tráfego restante:**
- Todo o tráfego que não foi bloqueado pelas regras anteriores é permitido
### ACLs criadas

| Nome da ACL | Interface | Direção | Função |
|-------------|-----------|---------|--------|
| BACKBONE-IN | FastEthernet0/0.1 | in | Anti-spoofing + OSPF + NAT + proteção do router |
| USERS-IN | FastEthernet0/0.2 | in | Anti-spoofing + DHCP + proteção do router |
| WIFI-IN | FastEthernet0/0.3 | in | Anti-spoofing + DHCP + proteção do router |
| VOIP-IN | FastEthernet0/0.4 | in | Anti-spoofing + DHCP + TFTP + SCCP + proteção do router |
| DMZ-OUT | FastEthernet0/0.5 | out | Controla tráfego que entra na DMZ |
| ROUTER-IN | FastEthernet0/0.5 | in | Permite todo o tráfego saindo da DMZ |