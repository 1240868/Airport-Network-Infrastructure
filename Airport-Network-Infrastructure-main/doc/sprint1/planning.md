RCOMP 2025-2026 Project 1 - Sprint 1 planning
===========================================
### Sprint master: 1240868 
# 1. Sprint's backlog #
| Task                           | Task description                                                               |
|--------------------------------|--------------------------------------------------------------------------------|
| T.1.1                          | Development of a structured cabling project for Terminal 2 encompassed floors, including the campus backbone. |
| T.1.2                          | Development of a structured cabling project for Terminal 3 encompassed floors. |
| T.1.3                          | Development of a structured cabling project for Terminal 5 encompassed floors. |
| T.1.4                          | Development of a structured cabling project for Terminal 4 encompassed floors. |

Whatever the format is, the following items are mandatory and will be subject of assessment:
- Demonstration of calculations regarding the number of network outlets for each room.
- Network outlets deployment schematic plan (including outlets for wireless access points)
  and justification comments.
- Cross-connects deployment schematic plan and justification comments.
- Cable pathways deployment schematic plan and justification comments.
- Hardware inventories, including total cable lengths by cable type, appropriate patch
  panels, network outlets, telecommunication enclosures of proper size.
- There should be also a global inventory made by the sum of the inventories of each
  building, this is a task for the sprint master.

# 2. Technical decisions and coordination #
In this section, all technical decisions taken in the planning meeting should be mentioned. 		Most importantly, all technical decisions impacting on the subtasks implementation must be settled on this 		meeting and specified here.

## 2.1 Campus Backbone cable types

* Single-mode fiber 
* Justification: Este tipo de fibra é ideal para ligações entre edifícios porque suporta distâncias muito longas (vários quilómetros) sem perda significativa de sinal.

## 2.2 Vertical Backbone cable types 

* Multimode fiber
* Justification: Este tipo de fibra é adequado para distâncias médias, normalmente presentes dentro de edifícios. A fibra multimode permite altas velocidades de transmissão, como 10 Gbps, e tem custos mais baixos de equipamentos óticos quando comparada com a fibra single-mode.

## 2.3 Copper cable type 

* CAT7
* Justification: A escolha do cabo CAT7 justifica-se por ser o requisito mínimo exigido para garantir débitos de 10 Gbps (10GbaseT) em todo o subsistema horizontal, assegurando a longevidade da infraestrutura para futuras atualizações tecnológicas
   Enquanto categorias inferiores como o CAT6 estão limitadas a 1 Gbps nestas condições, o CAT7 suporta a performance máxima até ao limite normativo de 90 metros para o cabo fixo (totalizando 100 metros de canal com os patch cords)
   Adicionalmente, a sua constituição como par entrançado blindado (S/STP) oferece uma proteção superior contra interferências eletromagnéticas (EMI), garantindo a integridade do sinal em ambientes de alta densidade
  

## 2.4 Copper cable wiring 

* T568B
* Justification: Este padrão define a ordem correta dos fios dentro do conector RJ45, garantindo compatibilidade e funcionamento adequado da rede.

## 2.5 Redundant links between ICs

* A utilização de ligações redundantes entre os Intermediate Cross-Connects (ICs) é recomendada para aumentar a disponibilidade e fiabilidade da rede. Caso ocorra uma falha num cabo ou equipamento, o tráfego pode ser automaticamente redirecionado por um caminho alternativo, evitando interrupções no serviço. Estas ligações são normalmente feitas com fibra ótica, devido à sua elevada capacidade e baixa latência.

## 2.6 Redundant Links between HCs

* Entre os Horizontal Cross-Connects (HCs) também é aconselhável implementar ligações redundantes para garantir continuidade de serviço em caso de falha de um link principal. Esta redundância melhora a resiliência da rede, reduzindo o impacto de falhas físicas ou manutenção. Normalmente são utilizadas ligações de fibra ótica, que oferecem maior capacidade e desempenho para transportar o tráfego agregado de múltiplos utilizadores.

# 3. Subtasks assignment #

  * 1240830 - Structured cable design for Terminal 5
  * 1240835 - Structured cable design for Terminal 4
  * 1240850 - Structured cable design for Terminal 3
  * 1240868 - Structured cable design for Terminal 2 

# 4. Common criteria

## Normas e Boas Práticas de Cabeamento Estruturado

---

### Comprimento Máximo do Cabo Horizontal (Cobre)

- **90 metros** de cabo horizontal + **5 metros** de patch cord (total 100 m) entre o switch e o dispositivo final.
- Garante desempenho consistente sem perda de sinal.

---

### Comprimento Máximo do Backbone (Fibra ou Cobre)

| Tipo                    | Distância Máxima              |
|-------------------------|-------------------------------|
| Fibra Multimode OM3/OM4 | 1000 metros                   |
| Fibra Single-mode       | Vários km (até 10 km ou mais) |
| Cobre CAT7              | Até 80 metros                 |

---

### Tipo de Cabo Adequado

| Segmento | Cabo Recomendado        | Desempenho      |
|---|-------------------------|-----------------|
| Horizontal | Cat7                    | 10 Gbps / 100 m |
| Backbone vertical | Fibra Multimode OM3/OM4 | 1000 m          |
| Campus backbone | Fibra Single-mode OS2   | Vários km       |

---

### Padrão de Terminação

- **Cobre:** RJ45 com padrão **T568B**, aplicado nas duas pontas do cabo.
- **Fibra:** conectores compatíveis com o transceiver utilizado — **LC, SC ou ST**.

---

### Distância entre Cross-Connects

- **Horizontal:** cada HC deve estar dentro do limite de **80-90 m** do dispositivo final.
- **Backbone:** ICs e HCs conectados segundo o layout físico do edifício, respeitando os limites do cabo utilizado.

---

### Redundância

Para links críticos (IC–IC, HC–HC, IC-HC, IC-MC), devem existir **2 caminhos independentes** para evitar falha total em caso de corte de cabo.

---

### Separação de Cabos

Cabos de energia e cabos de dados devem manter uma distância mínima de **30 cm** para reduzir interferência eletromagnética (EMI).

---

### Condições de Instalação

- Evitar dobras bruscas, tensão excessiva ou passagem por ambientes com calor ou humidade elevados.
- Respeitar os **raios mínimos de curvatura**:

| Tipo de Cabo | Raio Mínimo |
|---|---|
| Cobre | 4× o diâmetro do cabo |
| Fibra | 10× o diâmetro do cabo |

### Raio de WPA a considerar 

- 25 metros:  oferecem a redundância e a penetração de sinal necessárias para evitar reclamações de falta de rede em salas específicas


