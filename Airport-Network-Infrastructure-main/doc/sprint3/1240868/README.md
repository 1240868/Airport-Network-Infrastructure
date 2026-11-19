RCOMP 2025-2026 Project 1 - Sprint 3 - Member 1240868 folder
===========================================

## Índice

1. [Dispositivos do Terminal 2](#1-dispositivos-do-terminal-2)
2. [OSPF Dynamic Routing](#2-ospf-dynamic-routing)
3. [Servidor HTTP adicional na DMZ](#3-servidor-http-adicional-na-dmz)
4. [Serviço DHCPv4](#4-serviço-dhcpv4)
5. [Serviço VoIP (Cisco Telephony)](#5-serviço-voip-cisco-telephony)
6. [Servidor DNS (Root Domain)](#6-servidor-dns-root-domain)
7. [NAT (Network Address Translation)](#7-nat-network-address-translation)
8. [Static Firewall (ACLs)](#8-static-firewall-acls)
9. [Testes finais](#9-testes-finais)

---

## 1. Dispositivos do Terminal 2

| Dispositivo | Modelo | Nome | VLAN | IP | Função |
|-------------|--------|------|------|----|--------|
| Router | Cisco 2811 | T2-Router | Várias | Ver abaixo | Router do terminal |
| Switch IC | Switch-PT-Empty | T2-IC | 762 (gestão) | 10.57.130.1/23 | Switch intermédio |
| Switch HC Piso 0 | Switch-PT-Empty | T2-HC-L2 | 762 (gestão) | 10.57.130.2/23 | Switch acesso piso 0 |
| Switch HC Piso 1 | Switch-PT-Empty | T2-HC-L4 | 762 (gestão) | 10.57.130.3/23 | Switch acesso piso 1 |
| Servidor DNS | Server-PT | Server-L4 | 766 (DMZ) | 10.57.158.10/25 | DNS + HTTP |
| Servidor HTTP | Server-PT | T2-Server-HTTP | 766 (DMZ) | 10.57.158.20/25 | HTTP (server1) |
| Access Point | AccessPoint-PT | AP-L2 | 764 (WiFi) | DHCP | Ponto acesso WiFi |
| PC Users | PC-PT | PC-User-L2 | 763 (users) | DHCP | Cliente com fio |
| Laptop WiFi | Laptop-PT | Laptop-L2 | 764 (WiFi) | DHCP | Cliente WiFi |
| IP Phone | 7960 | IP Phone-L2 | 765 (VoIP) | DHCP | Telefone 2001 |
| IP Phone | 7960 | IP Phone-L4 | 765 (VoIP) | DHCP | Telefone 2000 |

### IPs do T2-Router por sub-interface

| Sub-interface | VLAN | IP | Máscara | Rede |
|---------------|------|----|---------|------|
| FastEthernet0/0.1 | 761 (backbone) | 10.57.128.2 | 255.255.255.0 | /24 |
| FastEthernet0/0.2 | 763 (users) | 10.57.152.1 | 255.255.252.0 | /22 |
| FastEthernet0/0.3 | 764 (WiFi) | 10.57.144.1 | 255.255.248.0 | /21 |
| FastEthernet0/0.4 | 765 (VoIP) | 10.57.156.1 | 255.255.254.0 | /23 |
| FastEthernet0/0.5 | 766 (DMZ) | 10.57.158.1 | 255.255.255.128 | /25 |
| FastEthernet1/0 | WAN (ISP) | 89.73.67.85 | 255.255.255.252 | /30 |

---

## 2. OSPF Dynamic Routing

### O que foi feito
Removeu-se o static routing (exceto a rota default para o ISP) e configurou-se OSPF como protocolo de routing dinâmico. O Terminal 2 ficou responsável por redistribuir a rota default para todo o domínio OSPF.

### Porquê
O enunciado do Sprint 3 determina que o static routing deve ser substituído por OSPF, com o backbone na área 0 e cada terminal numa área própria. O Terminal 2, por ser o único ligado ao ISP, deve injetar a rota default no OSPF.

### Configuração aplicada
- OSPF Process ID: 1
- Router ID: 2.2.2.2
- Área 0: rede backbone (10.57.128.0/24)
- Área 1 (Terminal 2): redes T2-users, T2-wifi, T2-voip, T2-servers
- Ativado `default-information originate` para redistribuir a rota default (0.0.0.0/0 via 89.73.67.86) no OSPF
- As wildcard masks foram calculadas corretamente para cada subnet:
    - Backbone: 0.0.0.255 (/24)
    - Users: 0.0.3.255 (/22)
    - WiFi: 0.0.7.255 (/21)
    - VoIP: 0.0.1.255 (/23)
    - DMZ: 0.0.0.127 (/25)

### Estado dos vizinhos OSPF

| Vizinho | IP | Estado |
|---------|----|--------|
| T3-Router | 10.57.128.3 | FULL/BDR |
| T5-Router | 10.57.128.5 | FULL/DR |
| T4-Router | 10.57.128.4 | INIT/DROTHER (problema no T4) |

---

## 3. Servidor HTTP adicional na DMZ

### O que foi feito
Adicionou-se um segundo servidor à DMZ local (VLAN 766), dedicado exclusivamente ao serviço HTTP/HTTPS. Foi ligado ao switch T2-IC e configurado com IP estático.

### Porquê
O enunciado exige dois servidores em cada DMZ: um que já existia do Sprint 2 (que agora acumula funções DNS + HTTP) e um novo exclusivamente para HTTP (server1).

### Configuração aplicada
- **Nome:** T2-Server-HTTP
- **IP:** 10.57.158.20
- **Máscara:** 255.255.255.128
- **Gateway:** 10.57.158.1
- **DNS Server:** 10.57.158.10
- **Serviço HTTP/HTTPS:** ativado
- **Página HTML:** criada com identificação do Terminal 2

---

## 4. Serviço DHCPv4

### O que foi feito
Configuraram-se três pools DHCP no T2-Router para atribuição automática de IPs nas VLANs 763 (users), 764 (WiFi) e 765 (VoIP). A VLAN 766 (DMZ) e 761 (backbone) mantêm configuração estática.

### Porquê
O enunciado determina que o router de cada terminal deve fornecer DHCP para todas as redes internas, exceto DMZ e backbone. Para a VLAN VoIP, é obrigatório o option 150 (TFTP server) para os telefones IP 7960.

### Configuração aplicada
Foram excluídos dos ranges DHCP os endereços já usados estaticamente:
- DMZ: 10.57.158.1 a 10.57.158.30
- Backbone: 10.57.128.1 a 10.57.128.5

| Pool | VLAN | Rede | Máscara | Gateway | DNS | Domain | Option 150 |
|------|------|------|---------|---------|-----|--------|------------|
| T2-users-pool | 763 | 10.57.152.0 | /22 | 10.57.152.1 | 10.57.158.10 | rcomp-25-26-dd-g1 | - |
| T2-wifi-pool | 764 | 10.57.144.0 | /21 | 10.57.144.1 | 10.57.158.10 | rcomp-25-26-dd-g1 | - |
| T2-voip-pool | 765 | 10.57.156.0 | /23 | 10.57.156.1 | 10.57.158.10 | rcomp-25-26-dd-g1 | 10.57.128.2 |

**Nota:** O option 150 aponta para o IP do T2-Router na interface de backbone (10.57.128.2), que é onde corre o serviço TFTP integrado no Cisco Telephony.

---

## 5. Serviço VoIP (Cisco Telephony)

### O que foi feito
Configurou-se o serviço de telefonia Cisco no T2-Router, atribuindo números aos dois IP Phones 7960 e criando dial-peers para encaminhamento de chamadas para outros terminais.

### Porquê
O enunciado exige serviço VoIP em cada terminal, com pelo menos dois telefones 7960, e capacidade de encaminhar chamadas entre terminais com base em prefixos.

### Configuração aplicada
- **IP source-address do Telephony Service:** 10.57.156.1 (VLAN VoIP)
- **Porto SCCP:** 2000
- **Max ephones:** 10 / Max dn: 10
- **Auto assign:** 1 to 2

**Números atribuídos:**

| ephone-dn | Número | Telefone | MAC |
|-----------|--------|----------|-----|
| 1 | 2000 | IP Phone-L4 | 0004.9AE0.90D7 |
| 2 | 2001 | IP Phone-L2 | 0090.2BAD.543D |

**Dial-peers para outros terminais:**

| Dial-peer | Prefixo | Session Target | Terminal destino |
|-----------|---------|----------------|-----------------|
| 3 | 3... | 10.57.128.3 | Terminal 3 |
| 4 | 4... | 10.57.128.4 | Terminal 4 |
| 5 | 5... | 10.57.128.5 | Terminal 5 |

**Configuração das portas dos switches:**
As portas onde os telefones estão ligados foram configuradas com `switchport voice vlan 765` e sem access VLAN (`no switchport access vlan`):
- IP Phone-L4: switch T2-HC-L4, porta Ethernet0/1
- IP Phone-L2: switch T2-HC-L2, porta Ethernet2/1

---

## 6. Servidor DNS (Root Domain)

### O que foi feito
O servidor Server-L4 (10.57.158.10) foi configurado como DNS name server do domínio raiz `rcomp-25-26-dd-g1`. Foi também ativado o serviço HTTP neste servidor (exigido para NAT).

### Porquê
O Terminal 2 gere o domínio de topo, conforme planeamento da equipa. Os outros terminais gerem subdomínios (`terminal-3`, `terminal-4`, `terminal-5`). O servidor raiz precisa de conhecer os NS dos subdomínios e respetivos glue records.

### Configuração aplicada
**Serviço DNS ativado.** Base de dados configurada com todos os registos em FQDN (terminando em `rcomp-25-26-dd-g1`).

**Registos A (Address):**

| Nome FQDN | IP |
|-----------|----|
| ns.rcomp-25-26-dd-g1 | 10.57.158.10 |
| server1.rcomp-25-26-dd-g1 | 10.57.158.20 |
| ns.terminal-3.rcomp-25-26-dd-g1 | 10.57.174.10 |
| ns.terminal-4.rcomp-25-26-dd-g1 | 10.57.190.10 |
| ns.terminal-5.rcomp-25-26-dd-g1 | 10.57.218.10 |

**Registos CNAME (Alias):**

| Nome FQDN | Alvo |
|-----------|------|
| www.rcomp-25-26-dd-g1 | server1.rcomp-25-26-dd-g1 |
| web.rcomp-25-26-dd-g1 | server1.rcomp-25-26-dd-g1 |
| dns.rcomp-25-26-dd-g1 | ns.rcomp-25-26-dd-g1 |

**Registos NS (Name Server) + Glue Records:**

| Domínio | Name Server | Glue Record (A) |
|---------|-------------|-----------------|
| terminal-3.rcomp-25-26-dd-g1 | ns.terminal-3.rcomp-25-26-dd-g1 | 10.57.174.10 |
| terminal-4.rcomp-25-26-dd-g1 | ns.terminal-4.rcomp-25-26-dd-g1 | 10.57.190.10 |
| terminal-5.rcomp-25-26-dd-g1 | ns.terminal-5.rcomp-25-26-dd-g1 | 10.57.218.10 |

**Serviço HTTP no servidor DNS:** Ativado com página HTML a identificar "Terminal 2 - DNS Server".

---

## 7. NAT (Network Address Translation)

### O que foi feito
Configurou-se NAT estático no T2-Router para redirecionar pedidos HTTP (porta 80) e HTTPS (porta 443) recebidos na interface de backbone para o servidor DNS na DMZ (10.57.158.10).

### Porquê
O enunciado exige que pedidos HTTP/HTTPS que cheguem ao router pela backbone sejam redirecionados para o servidor DNS local. Isto permite que utilizadores de outros terminais acedam ao servidor via o IP de backbone do router (10.57.128.2).

### Configuração aplicada
- Tradução estática TCP porta 80: 10.57.158.10:80 ↔ 10.57.128.2:80
- Tradução estática TCP porta 443: 10.57.158.10:443 ↔ 10.57.128.2:443

### Interfaces e lados NAT

| Interface | VLAN | NAT Side |
|-----------|------|----------|
| FastEthernet0/0.1 | 761 (backbone) | outside |
| FastEthernet0/0.2 | 763 (users) | inside |
| FastEthernet0/0.3 | 764 (WiFi) | inside |
| FastEthernet0/0.4 | 765 (VoIP) | inside |
| FastEthernet0/0.5 | 766 (DMZ) | inside |
| FastEthernet1/0 | ISP (WAN) | outside |

---

## 8. Static Firewall (ACLs)

### O que foi feito
Implementaram-se Access Control Lists (ACLs) no T2-Router para filtrar tráfego de acordo com as regras de precedência definidas no enunciado.

### ACLs criadas e aplicadas

| Nome da ACL | Interface | Direção | Função |
|-------------|-----------|---------|--------|
| ACL-BACKBONE-IN | FastEthernet0/0.1 | in | Filtra tráfego da backbone |
| ACL-INTERNAL-IN | FastEthernet0/0.2 | in | Filtra tráfego dos users |
| ACL-INTERNAL-IN | FastEthernet0/0.3 | in | Filtra tráfego do WiFi |
| ACL-INTERNAL-IN | FastEthernet0/0.4 | in | Filtra tráfego do VoIP |
| ACL-DMZ-IN | FastEthernet0/0.5 | in | Filtra tráfego da DMZ |

### Conteúdo das ACLs

**ACL-BACKBONE-IN:**

| Seq | Ação | Protocolo | Origem | Destino | Porta | Justificação |
|-----|------|-----------|--------|---------|-------|--------------|
| 5 | deny | ip | 10.57.144.0/20 | any | - | Anti-spoofing WiFi |
| 6 | deny | ip | 10.57.152.0/22 | any | - | Anti-spoofing users |
| 7 | deny | ip | 10.57.156.0/23 | any | - | Anti-spoofing VoIP |
| 8 | deny | ip | 10.57.158.0/25 | any | - | Anti-spoofing DMZ |
| 20 | permit | icmp | any | any | echo | ICMP permitido |
| 30 | permit | icmp | any | any | echo-reply | ICMP permitido |
| 40 | permit | ospf | any | any | - | OSPF |
| 45 | permit | udp | any | 10.57.128.2 | bootps | DHCP |
| 50 | permit | tcp | any | 10.57.128.2 | 80 | NAT HTTP |
| 60 | permit | tcp | any | 10.57.128.2 | 443 | NAT HTTPS |
| 70 | permit | tcp | any | 10.57.128.2 | 2000 | VoIP SCCP |
| 80 | deny | ip | any | 10.57.128.2 | - | Bloqueia router |
| 90-130 | deny | ip | any | IPs internos | - | Bloqueia router |
| 140 | permit | ip | any | any | - | Resto permitido |

**ACL-INTERNAL-IN:**

| Seq | Ação | Protocolo | Origem | Destino | Porta | Justificação |
|-----|------|-----------|--------|---------|-------|--------------|
| 10 | permit | icmp | any | any | echo | ICMP permitido |
| 20 | permit | icmp | any | any | echo-reply | ICMP permitido |
| 25 | permit | ospf | any | any | - | OSPF |
| 30-50 | permit | udp | any | gateways | bootps | DHCP |
| 60 | permit | udp | any | 10.57.128.2 | tftp | TFTP phones |
| 70 | permit | tcp | any | 10.57.128.2 | 2000 | VoIP SCCP |
| 80-90 | permit | udp/tcp | any | 10.57.158.10 | 53 | DNS |
| 100-130 | permit | tcp | any | DMZ servers | 80/443 | HTTP/HTTPS |
| 140 | deny | ip | any | 10.57.158.0/25 | - | Bloqueia resto DMZ |
| 150-200 | deny | ip | any | IPs router | - | Bloqueia router |
| 210 | permit | ip | any | any | - | Resto permitido |

**ACL-DMZ-IN:**

| Seq | Ação | Protocolo | Origem | Destino | Porta | Justificação |
|-----|------|-----------|--------|---------|-------|--------------|
| 10 | permit | icmp | any | any | echo | ICMP permitido |
| 15 | permit | ospf | any | any | - | OSPF |
| 20 | permit | icmp | any | any | echo-reply | ICMP permitido |
| 30-40 | permit | udp | 10.57.158.10 | any | 53 | DNS queries |
| 35 | permit | tcp | 10.57.158.10 | any | 53 | DNS TCP |
| 50-100 | deny | ip | any | IPs router | - | Bloqueia router |
| 110 | permit | ip | any | any | - | Resto permitido |

:** Os problemas com T4 (OSPF INIT, VoIP) e T5 (VoIP) não são da responsabilidade do Terminal 2 — as configurações do lado do T2 estão corretas e os dial-peers estão devidamente configurados.