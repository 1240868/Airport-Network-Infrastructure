# RCOMP 2025-2026 Project 1 - Sprint 2 - Terminal 2
===========================================

## 1. Router Sub-interfaces e Redes do Terminal 2

| Sub-interface | VLAN ID | Nome VLAN | Rede | Máscara | Gateway (Router IP) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Fa0/0.1 | 761 | Backbone | 10.57.128.0/24 | 255.255.255.0 | 10.57.128.2 |
| Fa0/0.2 | 763 | User Outlets | 10.57.152.0/22 | 255.255.252.0 | 10.57.152.1 |
| Fa0/0.3 | 764 | Wi-Fi | 10.57.144.0/21 | 255.255.248.0 | 10.57.144.1 |
| Fa0/0.4 | 765 | VoIP | 10.57.156.0/23 | 255.255.254.0 | 10.57.156.1 |
| Fa0/0.5 | 766 | Servers DMZ | 10.57.158.0/25 | 255.255.255.128 | 10.57.158.1 |

### Dimensionamento das Sub-redes (VLSM Interno)

O bloco de endereços atribuído ao Terminal 2 é **10.57.144.0/20**, que cobre o intervalo
10.57.144.0 – 10.57.159.255, totalizando 4094 endereços utilizáveis.

Aplicando VLSM com ordenação da maior para a menor rede:

#### Wi-Fi — 10.57.144.0/21 (255.255.248.0)
- **Requisito:** 2000 nós
- **Justificação da máscara:** Uma máscara /21 fornece 2^11 - 2 = 2046 endereços utilizáveis,
  sendo o menor bloco capaz de acomodar 2000 hosts.
  Uma máscara /22 apenas forneceria 1022 hosts, insuficiente.
- **Justificação do endereço de rede:** Começa em 10.57.144.0, início do bloco T2.
  Por ser a maior rede, é alocada primeiro, garantindo alinhamento correto do bloco.
- **Range:** 10.57.144.0 – 10.57.151.255
- **Gateway:** 10.57.144.1 (sub-interface Fa0/0.3 do router)

#### User Outlets — 10.57.152.0/22 (255.255.252.0)
- **Requisito:** 1000 nós
- **Justificação da máscara:** Uma máscara /22 fornece 2^10 - 2 = 1022 endereços utilizáveis,
  sendo o menor bloco capaz de acomodar 1000 hosts.
  Uma máscara /23 apenas forneceria 510 hosts, insuficiente.
- **Justificação do endereço de rede:** Começa em 10.57.152.0, imediatamente após o bloco
  Wi-Fi (que termina em 10.57.151.255), sem sobreposições.
- **Range:** 10.57.152.0 – 10.57.155.255
- **Gateway:** 10.57.152.1 (sub-interface Fa0/0.2 do router)

#### VoIP — 10.57.156.0/23 (255.255.254.0)
- **Requisito:** 500 nós
- **Justificação da máscara:** Uma máscara /23 fornece 2^9 - 2 = 510 endereços utilizáveis,
  sendo o menor bloco capaz de acomodar 500 hosts.
  Uma máscara /24 apenas forneceria 254 hosts, insuficiente.
- **Justificação do endereço de rede:** Começa em 10.57.156.0, imediatamente após o bloco
  User Outlets (que termina em 10.57.155.255), sem sobreposições.
- **Range:** 10.57.156.0 – 10.57.157.255
- **Gateway:** 10.57.156.1 (sub-interface Fa0/0.4 do router)

#### Servers DMZ — 10.57.158.0/25 (255.255.255.128)
- **Requisito:** 100 nós
- **Justificação da máscara:** Uma máscara /25 fornece 2^7 - 2 = 126 endereços utilizáveis,
  sendo o menor bloco capaz de acomodar 100 hosts.
  Uma máscara /26 apenas forneceria 62 hosts, insuficiente.
- **Justificação do endereço de rede:** Começa em 10.57.158.0, imediatamente após o bloco
  VoIP (que termina em 10.57.157.255), sem sobreposições.
- **Range:** 10.57.158.0 – 10.57.158.127
- **Gateway:** 10.57.158.1 (sub-interface Fa0/0.5 do router)

#### Campus Backbone — 10.57.128.0/24 (255.255.255.0)
- **Requisito:** 190 nós (definido globalmente no planning da equipa)
- **Justificação da máscara:** Uma máscara /24 fornece 2^8 - 2 = 254 endereços utilizáveis,
  sendo o menor bloco capaz de acomodar 190 hosts.
- **Justificação do endereço de rede:** Rede partilhada por todos os terminais, definida
  no planning da equipa como 10.57.128.0/24, pertencente ao bloco global 10.57.128.0/17.
- **IP do router T2 no Backbone:** 10.57.128.2 (sub-interface Fa0/0.1)

---

## 2. Configuração do Router-on-a-Stick

O router do Terminal 2 é um **Cisco 2811**, escolhido por ser o único modelo suportado
pelo Packet Tracer que garante compatibilidade com serviços de **VoIP** e **DHCP**
necessários nos sprints seguintes.

Para interligar o router às 6 redes do terminal usando uma única ligação física ao switch IC,
foi utilizada a técnica de **Router-on-a-Stick**: a interface física **FastEthernet0/0**
foi dividida em **sub-interfaces lógicas**, cada uma associada a uma VLAN através de
encapsulamento **dot1Q**. Esta abordagem permite:

- Encaminhamento inter-VLAN sem necessidade de múltiplas interfaces físicas.
- Uma única ligação trunk entre o router e o switch IC, transportando todas as VLANs.
- Escalabilidade — novas VLANs podem ser adicionadas como novas sub-interfaces sem
  alterações físicas.

O módulo **NM-1FE-TX** foi adicionado ao router 2811 para disponibilizar uma terceira
interface **FastEthernet1/0**, utilizada exclusivamente para a ligação WAN ao ISP.

---

## 3. End-Devices do Terminal 2

| Dispositivo | VLAN | IP | Máscara | Gateway | Justificação |
|---|---|---|---|---|---|
| PC-User-L2 (User Outlets) | 763 | 10.57.152.10 | 255.255.252.0 | 10.57.152.1 | Host na rede 10.57.152.0/22. O gateway 10.57.152.1 é o IP do router na sub-interface Fa0/0.2, responsável por encaminhar tráfego desta VLAN para outras redes |
| PC-User-L4 (User Outlets) | 763 | 10.57.152.11 | 255.255.252.0 | 10.57.152.1 | Host na rede 10.57.152.0/22, segundo PC de utilizador no piso 4. Partilha o mesmo gateway que o PC-User-L2 por pertencerem à mesma VLAN |
| Laptop-L2 (Wi-Fi) | 764 | 10.57.144.10 | 255.255.248.0 | 10.57.144.1 | Host na rede 10.57.144.0/21, associado wirelessly ao AP-L2 ligado à VLAN 764. O gateway 10.57.144.1 é o IP do router na sub-interface Fa0/0.3 |
| Laptop-L4 (Wi-Fi) | 764 | 10.57.144.11 | 255.255.248.0 | 10.57.144.1 | Host na rede 10.57.144.0/21, associado wirelessly ao AP-L4. Partilha o mesmo gateway que o Laptop-L2 por pertencerem à mesma VLAN |
| Server-L4 (Servers DMZ) | 766 | 10.57.158.10 | 255.255.255.128 | 10.57.158.1 | Host na rede 10.57.158.0/25. O gateway 10.57.158.1 é o IP do router na sub-interface Fa0/0.5. Rede dedicada a servidores, isolada das restantes por ser uma DMZ |
| PC-Switch (Switches DMZ) | 762 | 10.57.130.10 | 255.255.254.0 | — | Host na rede de gestão 10.57.130.0/23. Rede intencionalmente isolada — não possui gateway nem router, impedindo que tráfego externo entre na rede de gestão dos switches |
| IP Phone-L2 | 765 | — | — | — | Configuração IP via DHCP pelo Call Manager, adiada para o Sprint 3 |
| IP Phone-L4 | 765 | — | — | — | Configuração IP via DHCP pelo Call Manager, adiada para o Sprint 3 |

---

## 4. Configuração dos IP Phones (Voice VLAN)

Os telefones **Cisco 7960** foram ligados a portas dos switches configuradas com
**Voice VLAN** (`switchport voice vlan 765`), em vez da VLAN de acesso normal.
Esta configuração é justificada por três razões:

1. **Separação do tráfego de voz:** O tráfego VoIP é isolado do tráfego de dados,
   permitindo aplicar políticas de QoS (Quality of Service) que priorizam os pacotes
   de voz, garantindo baixa latência e jitter reduzido — essenciais para chamadas de qualidade.
2. **Segurança:** Os telefones ficam numa VLAN separada dos computadores, limitando
   a exposição a ataques provenientes da rede de dados.
3. **Compatibilidade CDP:** Os switches Cisco usam o protocolo CDP para comunicar
   automaticamente a Voice VLAN ao telefone, simplificando a configuração.

---

## 5. Routing Estático e Ligação à Internet

### Tabela de Routing do T2-Router

| Rede destino | Máscara | Via (next-hop) | Justificação |
|---|---|---|---|
| 10.57.160.0/20 | 255.255.240.0 | 10.57.128.3 | Bloco do Terminal 3. Tráfego encaminhado para o router T3, cujo IP no backbone é 10.57.128.3 |
| 10.57.176.0/20 | 255.255.240.0 | 10.57.128.4 | Bloco do Terminal 4. Tráfego encaminhado para o router T4, cujo IP no backbone é 10.57.128.4 |
| 10.57.192.0/19 | 255.255.224.0 | 10.57.128.5 | Bloco do Terminal 5. Tráfego encaminhado para o router T5, cujo IP no backbone é 10.57.128.5 |
| 0.0.0.0 | 0.0.0.0 | 89.73.67.86 | Rota por defeito — todo o tráfego desconhecido (Internet) é encaminhado para o ISP |

As rotas estáticas foram configuradas manualmente para cada bloco de terminal usando
o IP do router vizinho no backbone como next-hop. O Terminal 2 é o **único terminal
com ligação à Internet** no campus, pelo que a rota default `0.0.0.0 0.0.0.0 89.73.67.86`
é essencial para que qualquer tráfego desconhecido saia para a Internet através do ISP.

---

## 6. Ligação à Internet (DSL)

### Topologia
```
T2-Router (Fa1/0) → DSL-Modem → Cloud-PT (PSTN) → ISP-Router
89.73.67.85                                          89.73.67.86
```

### Descrição
A ligação à Internet simula uma ligação DSL típica através de uma cadeia de dispositivos:

- **DSL-Modem:** Converte o sinal digital do router em sinal analógico para transporte
  na rede telefónica pública (PSTN), simulando o **lacete local (Local Loop)** do operador.
  Opera na camada 2 — não tem endereço IP.
- **Cloud-PT:** Representa a rede telefónica pública (PSTN) do operador. Opera na camada 2
  com mapeamento interno entre a porta Modem (lado DSL) e a porta Ethernet (lado ISP),
  simulando a infraestrutura de transporte do operador. Não tem endereço IP.
- **ISP-Router:** Router do operador com IP público `89.73.67.86/30`. Tem uma rota
  estática para o bloco da equipa (`10.57.128.0/17`) apontando para o T2-Router,
  permitindo que o tráfego de resposta regresse ao campus.

A ligação entre T2-Router e ISP-Router é **ponto-a-ponto /30**, fornecendo apenas
2 endereços úteis — exatamente o necessário, minimizando o desperdício de IPs públicos.

### IPs da ligação
| Dispositivo | Interface | IP | Máscara | Justificação |
|---|---|---|---|---|
| T2-Router | FastEthernet1/0 | 89.73.67.85 | 255.255.255.252 | IP público do lado do cliente. Pertence à rede ponto-a-ponto 89.73.67.84/30. Módulo NM-1FE-TX adicionado ao 2811 para disponibilizar esta interface |
| ISP-Router | FastEthernet0/0 | 89.73.67.86 | 255.255.255.252 | IP público do ISP, definido no enunciado para o grupo 2DD-1. É o next-hop da rota default do T2-Router |
| DSL-Modem | — | — | — | Camada 2, transparente ao nível IP. Simula o lacete local do operador DSL |
| Cloud-PT | — | — | — | Camada 2, representa a PSTN do operador. Mapeamento Modem ↔ Ethernet internamente |

### Routing estático do ISP-Router
| Rede destino | Máscara | Next-Hop | Justificação |
|---|---|---|---|
| 10.57.128.0 | 255.255.128.0 | 89.73.67.85 | Rota para o bloco completo da equipa (10.57.128.0/17). Necessária para que o ISP encaminhe respostas de volta para a infraestrutura interna do campus |

---

## 7. Gestão Remota dos Switches (Switches DMZ - VLAN 762)

A rede **Switches DMZ (10.57.130.0/23)** é uma rede de gestão dedicada e isolada,
sem router nem gateway, utilizada exclusivamente para acesso administrativo remoto
aos switches via protocolos como SSH ou SNMP. O facto de não ter gateway é
intencional — impede que tráfego externo aceda à rede de gestão, aumentando a segurança.

O range atribuído ao Terminal 2 é **10.57.130.1 – 10.57.130.50**.
O T2-MC, sendo o switch principal (Main Cross-Connect) do campus, tem o IP **10.57.130.201**
no range reservado para o Backbone (10.57.130.201 – 10.57.130.254).
Cada switch tem um IP estático nesta rede, configurado na interface virtual **VLAN 762**.

| Switch | IP | Máscara | Justificação |
|---|---|---|---|
| T2-MC | 10.57.130.201 | 255.255.254.0 | IP no range do Backbone (10.57.130.201-254). Switch principal (Main Cross-Connect) do campus, ponto central de toda a infraestrutura de switching |
| T2-IC | 10.57.130.1 | 255.255.254.0 | Primeiro IP do range T2 (10.57.130.1-50). Switch intermediário (Intermediate Cross-Connect), agrega as ligações dos switches de piso |
| T2-HC-L2 | 10.57.130.2 | 255.255.254.0 | Segundo IP do range T2. Switch do piso 2 (Horizontal Cross-Connect), serve os end-devices do piso 2 |
| T2-HC-L4 | 10.57.130.3 | 255.255.254.0 | Terceiro IP do range T2. Switch do piso 4 (Horizontal Cross-Connect), serve os end-devices do piso 4 |