# RCOMP 2025-2026 Project 1 - Sprint 3 - Member 1240835

### Terminal 5 — Task T.3.3 ###

## 1. OSPF Dynamic Routing Configuration
As rotas estáticas do Sprint 2 foram removidas, com exceção da rota por defeito no Terminal 2. A infraestrutura foi integrada num sistema autónomo **OSPF**, dividido em áreas para otimizar o tráfego.

| Area | Use | Networks Included |
| :--- | :--- | :--- |
| **Area 0** | Campus Backbone | 10.57.128.0/24 (VLAN 761) |
| **Area 4** | Terminal 5 Internal | 10.57.192.0/19 (Engloba VLANs 771, 772, 773 e 774) |

A **rota por defeito** para acesso à Internet é recebida dinamicamente via OSPF, sendo propagada pelo router do Terminal 2 através do comando `default-information originate`.

### T5-Router OSPF Configuration

router ospf 1
network 10.57.192.0 0.0.31.255 area 4
network 10.57.128.0 0.0.0.255 area 0


---

## 2. HTTP Servers
Na DMZ do Terminal 5 (VLAN 774), foram configurados dois servidores com o serviço HTTP/HTTPS ativo e uma página HTML de identificação.

| Server Name | IP Address | Services | Description |
| :--- | :--- | :--- | :--- |
| **T5-L0-Server** | 10.57.218.10 | DNS + HTTP/HTTPS | Servidor original; alvo do NAT estático. |
| **T5-Server-HTTP**| 10.57.218.2 | HTTP/HTTPS | Novo servidor adicionado neste sprint. |

---

## 3. DHCPv4 Service
O **T5-Router** atua como servidor DHCP para as redes locais, excluindo a DMZ e o Backbone.

| Pool Name | VLAN | Network | Default Gateway | DNS Server | Options |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T5-users** | 771 | 10.57.208.0/21 | 10.57.208.1 | 10.57.218.10 | domain-name terminal-5.rcomp-25-26-dd-g1 |
| **T5-wifi** | 772 | 10.57.192.0/20 | 10.57.192.1 | 10.57.218.10 | domain-name terminal-5.rcomp-25-26-dd-g1 |
| **T5-voip** | 773 | 10.57.216.0/23 | 10.57.216.1 | — | Option 150: 10.57.128.5 |

*A **Option 150** aponta para o IP do router na interface de backbone (10.57.128.5), onde reside o serviço TFTP para os telefones IP.*

---

## 4. VoIP Service (Cisco Telephony)
Configuração do serviço **Cisco Telephony** para gestão de chamadas locais e encaminhamento entre terminais.
*   **Prefixo:** 5.
*   **Números Locais:** 5000 e 5001.
*   **Configuração de Porta:** Portas dos switches com `switchport voice vlan 773` e `no switchport access vlan`.

### Dial-peers
Chamadas para os prefixos 2, 3 e 4 são encaminhadas para os routers T2 (10.57.128.2), T3 (10.57.128.3) e T4 (10.57.128.4), respetivamente.

---

## 5. DNS Configuration
O Terminal 5 gere o subdomínio `terminal-5.rcomp-25-26-dd-g1`. O servidor DNS local é o **T5-L0-Server** (10.57.218.10).

### DNS Records
| Record Type | Name (FQDN) | Value / Target |
| :--- | :--- | :--- |
| **A** | ns.terminal-5.rcomp-25-26-dd-g1 | 10.57.218.10 |
| **A** | server1.terminal-5.rcomp-25-26-dd-g1 | 10.57.218.2 |
| **CNAME** | www.terminal-5.rcomp-25-26-dd-g1 | server1.terminal-5.rcomp-25-26-dd-g1 |
| **CNAME** | web.terminal-5.rcomp-25-26-dd-g1 | server1.terminal-5.rcomp-25-26-dd-g1 |
| **CNAME** | dns.terminal-5.rcomp-25-26-dd-g1 | ns.terminal-5.rcomp-25-26-dd-g1 |
| **NS** | rcomp-25-26-dd-g1 | ns.rcomp-25-26-dd-g1 |
| **A (glue)** | ns.rcomp-25-26-dd-g1 | 10.57.158.10 |

*O registo de cola para o domínio raiz (Terminal 2) permite a resolução em toda a árvore DNS.*

---

## 6. Switches IP Table (VLAN 762)
Os switches utilizam endereçamento estático na rede de gestão.

| Switch | IP Address | Mask | VLAN |
| :--- | :--- | :--- | :--- |
| **T5-IC** | 10.57.130.151 | 255.255.254.0 | 762 |
| **T5-HC-L0** | 10.57.130.152 | 255.255.254.0 | 762 |
| **T5-HC-L2** | 10.57.130.153 | 255.255.254.0 | 762 |

---

## 7. Static NAT (Port Forwarding)
Redirecionamento de tráfego HTTP/HTTPS recebido no backbone para o servidor DMZ (10.57.218.10).
Todas as VLANs internas (Users, Wi-Fi, VoIP, DMZ) estão configuradas como **NAT inside**, enquanto a interface de backbone é **NAT outside**.

| Protocol | Outside (Backbone) | Inside (DMZ) |
| :--- | :--- | :--- |
| **TCP** | 10.57.128.5:80 | 10.57.218.10:80 |
| **TCP** | 10.57.128.5:443 | 10.57.218.10:443 |


## 8. Static Firewall (Access Control Lists)
Implementação de políticas de segurança utilizando **ACLs nomeadas** (estilo Cisco), aplicadas nas interfaces conforme a direção do tráfego.

### ACL BACKBONE-IN (Interface Fa0/0.761 — inbound)
| Priority | Rule | Reason |
| :--- | :--- | :--- |
| 1 | **Deny IP source 10.57.192.0/19** | **Anti-spoofing**: Bloqueia IPs internos vindos do exterior. |
| 2 | **Permit OSPF** | Tráfego de routing dinâmico. |
| 3 | **Permit ICMP echo / echo-reply** | **ICMP**: Sempre permitido. |
| 4 | Permit TCP to 10.57.128.5 eq 80, 443 | **NAT**: HTTP/HTTPS para o servidor DMZ. |
| 5 | Permit TCP to 10.57.128.5 eq 2000 | **VoIP**: Encaminhamento de chamadas. |
| 6 | Deny IP any host 10.57.128.5 | Bloqueio de acesso direto ao router. |
| 7 | Deny IP any host 10.57.218.1 | Bloqueio de acesso ao gateway DMZ. |
| 8 | Deny IP any host 10.57.208.1 | Bloqueio de acesso ao gateway Users. |
| 9 | Deny IP any host 10.57.192.1 | Bloqueio de acesso ao gateway Wi-Fi. |
| 10 | Deny IP any host 10.57.216.1 | Bloqueio de acesso ao gateway VoIP. |
| 11 | Permit IP any any | Restante tráfego em trânsito. |

### ACL INTERNAL-IN (Interfaces .771, .772, .773 — inbound)
| Priority | Rule | Reason |
| :--- | :--- | :--- |
| 1 | **Permit ICMP echo / echo-reply** | **ICMP**: Sempre permitido. |
| 2 | **Permit UDP any eq bootps** | **DHCP**: Tráfego necessário. |
| 3 | **Permit UDP/TCP to 10.57.128.5 eq 69,2000** | **TFTP/VoIP**: Serviços do router. |
| 4 | Permit UDP/TCP to 10.57.218.10 eq 53,80,443 | Acesso ao servidor DNS/HTTP. |
| 5 | Permit TCP to 10.57.218.2 eq 80,443 | Acesso ao servidor HTTP secundário. |
| 6 | Deny IP any 10.57.218.0 0.0.0.127 | Bloqueio do restante tráfego para a DMZ. |
| 7 | Deny IP any host 10.57.218.1 | Bloqueio ao gateway DMZ. |
| 8 | Deny IP any host 10.57.208.1 | Bloqueio ao gateway Users. |
| 9 | Deny IP any host 10.57.192.1 | Bloqueio ao gateway Wi-Fi. |
| 10 | Deny IP any host 10.57.216.1 | Bloqueio ao gateway VoIP. |
| 11 | Deny IP any host 10.57.128.5 | Bloqueio ao router. |
| 12 | Permit IP any any | Restante tráfego permitido. |

### ACL DMZ-IN (Interface Fa0/0.774 — inbound)
| Priority | Rule | Reason |
| :--- | :--- | :--- |
| 1 | **Permit ICMP echo / echo-reply** | **ICMP**: Sempre permitido. |
| 2 | Permit UDP host 10.57.218.10 any eq 53 | DNS queries do servidor. |
| 3 | Deny IP any host 10.57.218.1 | Bloqueio ao gateway DMZ. |
| 4 | Deny IP any host 10.57.208.1 | Bloqueio ao gateway Users. |
| 5 | Deny IP any host 10.57.192.1 | Bloqueio ao gateway Wi-Fi. |
| 6 | Deny IP any host 10.57.216.1 | Bloqueio ao gateway VoIP. |
| 7 | Deny IP any host 10.57.128.5 | Bloqueio ao router. |
| 8 | Permit IP any any | Restante tráfego permitido. |

### ACLs Aplicadas nas Interfaces
| Interface | ACL | Direção |
| :--- | :--- | :--- |
| Fa0/0.761 (Backbone) | ACL-BACKBONE-IN | inbound |
| Fa0/0.771 (Users) | ACL-INTERNAL-IN | inbound |
| Fa0/0.772 (Wi-Fi) | ACL-INTERNAL-IN | inbound |
| Fa0/0.773 (VoIP) | ACL-INTERNAL-IN | inbound |
| Fa0/0.774 (DMZ) | ACL-DMZ-IN | inbound |