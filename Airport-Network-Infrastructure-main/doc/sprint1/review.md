RCOMP 2025-2026 Project 1 - Sprint 1 review
=========================================
### Sprint master: 1240868 ###
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
- 
# 2. Subtasks assessment #
One by one, each team member presents his/her outcomes to the team, the team assesses 		the accomplishment of the subtask backlog.
The subtask backlog accomplishment can be assessed as one of:

  * Totally implemented with no issues
  * Totally implemented with issues
  * Partially implemented with no issues
  * Partially implemented with issues

For the last three cases, a text description of what has not been implemented and present issues must be added.
Unimplemented features and issues solving is assigned to the same member on the next sprint.


## 2.1. 1240830 - Structured cable design for Terminal X #
### Outcomes :  ###
1240830 — REVesponsável pela Tarefa T.1.3, implementei na totalidade o projeto de cablagem estruturada para o Terminal 5, abrangendo o Level 0 (Arrivals) e o Level 2 (Departures). O trabalho começou com a medição cuidadosa das dimensões de todas as salas com base na escala fornecida nas plantas, garantindo cálculos de área precisos para a estimativa da densidade de tomadas. Para cada piso, foi produzido um plano de distribuição de tomadas de rede, detalhando a colocação de todas as tomadas ISO 8877 por sala. Foi ainda criado um plano de distribuição de pontos de acesso wireless (WAP) para cada nível, garantindo cobertura Wi-Fi completa em ambos os pisos com sobreposição máxima de 15% entre WAPs adjacentes. Foi também desenvolvido um plano de infraestrutura separado para cada nível, ilustrando a colocação do Horizontal Cross-Connect (HC), do Intermediate Cross-Connect (IC) no Level 0, dos Consolidation Points (CP) e o traçado dos caminhos dos cabos, tanto para a cablagem horizontal (Cat7 S/FTP) como para a fibra de backbone (OM4). Por fim, foi compilado um inventário de hardware por piso, incluindo os comprimentos totais de cabo por tipo, número de tomadas, WAPs, CPs, HCs, IC, patch panels e armários de telecomunicações.
Podem existir algumas imprecisões nas medições das dimensões das salas, uma vez que a conversão manual a partir da escala fornecida introduziu potenciais erros de arredondamento. A colocação dos Consolidation Points foi uma das decisões mais exigentes do projeto, dado que o Terminal 5, no Level 2, apresenta apenas passagem verticais na parede direita e as salas estão mais perto da parede esquerda, obrigando a um planeamento cuidado para garantir que nenhum cabo horizontal excedesse os 90 metros normativos — em particular nas salas da fila inferior do Level 0 e nas salas mais afastadas do Level 2. O cálculo dos comprimentos de cabo foi feito medindo a distância do centro de cada sala ao seu CP pelas condutas instaladas, multiplicando pelo número de tomadas, o que, apesar de ser uma aproximação metodologicamente fundamentada, pode não refletir com total precisão os percursos reais de cada cabo individual. A distribuição dos caminhos dos cabos poderia eventualmente ter sido mais otimizada de forma a minimizar o comprimento total de cabo utilizado, uma vez que as escolhas de traçado feitas podem não representar sempre o percurso mais eficiente entre dispositivos.
* 1240868 :    Totally implemented with issues
* 1240850-Totally implemented with no issues
* 1240835 :    Totally implemented with issues


## 2.2. 1240835 - Structured cable design for Terminal Y #
### Outcomes :  ###
1240835 — Responsável pela Tarefa T.1.4, implementei na totalidade o projeto de cablagem estruturada para o Terminal 4, abrangendo o Level 0 (Arrivals) e o Level 2 (Departures). O trabalho começou com a medição cuidadosa das dimensões de todas as salas com base na escala fornecida nas plantas, garantindo cálculos de área precisos para a estimativa da densidade de tomadas. Para cada piso, foi produzido um plano de distribuição de tomadas de rede, detalhando a colocação de todas as tomadas ISO 8877 por sala, bem como as tomadas nas paredes externas do Level 2 espaçadas de cinco em cinco metros. Foi ainda criado um plano de distribuição de pontos de acesso wireless (WAP) para cada nível, garantindo cobertura Wi-Fi completa em ambos os pisos com sobreposição máxima de 15% entre WAPs adjacentes. Foi também desenvolvido um plano de infraestrutura separado para cada nível, ilustrando a colocação do Horizontal Cross-Connect (HC), do Intermediate Cross-Connect (IC) no Level 0, dos Consolidation Points (CP) e o traçado dos caminhos dos cabos, tanto para a cablagem horizontal (Cat7 S/FTP) como para a fibra de backbone (OM4). Por fim, foi compilado um inventário de hardware por piso, incluindo os comprimentos totais de cabo por tipo, número de tomadas, WAPs, CPs, HCs, IC, patch panels e armários de telecomunicações.
Podem existir algumas imprecisões nas medições das dimensões das salas, uma vez que a conversão manual a partir da escala fornecida introduziu potenciais erros de arredondamento. A colocação dos Consolidation Points foi uma das decisões mais exigentes do projeto, dado que o Terminal 4 apresenta apenas uma passagem vertical por piso e um único HC por piso, obrigando a um planeamento cuidado para garantir que nenhum cabo horizontal excedesse os 90 metros normativos — em particular nas salas da fila inferior do Level 0 e nas salas mais afastadas do Level 2. O cálculo dos comprimentos de cabo foi feito medindo a distância do centro de cada sala ao seu CP pelas condutas instaladas, multiplicando pelo número de tomadas, o que, apesar de ser uma aproximação metodologicamente fundamentada, pode não refletir com total precisão os percursos reais de cada cabo individual. A distribuição dos caminhos dos cabos poderia eventualmente ter sido mais otimizada de forma a minimizar o comprimento total de cabo utilizado, uma vez que as escolhas de traçado feitas podem não representar sempre o percurso mais eficiente entre dispositivos.

* 1240868 :    Totally implemented with issues
1240850-Totally implemented with no issues
* 1240830 :    Totally implemented with issues

## 2.3. 1240850 - Structured cable design for Terminal Z #
### Outcomes :  ###
1240850 - responsável pela Tarefa T.1.2 implementei na totalidade o projeto de cablagem estruturada para o Terminal 3, abrangendo o Nível 1 (Partidas) e o Nível 2 (Chegadas). O trabalho começou com a medição cuidadosa das dimensões de todas as salas com base na escala fornecida nas plantas, garantindo cálculos de área precisos para a estimativa da densidade de tomadas. Para cada piso, foi produzido um plano de distribuição de tomadas de rede, detalhando a colocação de todas as tomadas ISO 8877 por sala, bem como as tomadas nas paredes externas espaçadas de cinco em cinco metros. Foi ainda criado um plano de distribuição de pontos de acesso wireless (WAP) para cada nível, garantindo cobertura Wi-Fi completa em ambos os pisos. Foi também desenvolvido um plano de infraestrutura separado para cada nível, ilustrando a colocação de todos os Horizontal Cross-Connects (HC), Pontos de Consolidação (CP) e o Intermediate Cross-Connect (IC), juntamente com o traçado dos caminhos dos cabos, tanto para a cablagem horizontal (CAT6A) como para a fibra de backbone. Por fim, foi compilado um inventário detalhado de hardware por piso, incluindo os comprimentos totais de cabo por tipo, número de tomadas, WAPs, CPs, HCs, IC, patch panels e armários de telecomunicações.
Podem existir algumas imprecisões nas medições das dimensões das salas, uma vez que a conversão manual a partir da escala fornecida introduziu potenciais erros de arredondamento. Além disso, a distribuição dos caminhos dos cabos poderia eventualmente ter sido mais otimizada de forma a minimizar o comprimento total de cabo utilizado, uma vez que as escolhas de traçado feitas podem não representar sempre o percurso mais eficiente entre dispositivos.
* 1240868 :    Totally implemented with issues
* 1240830 :    Totally implemented with issues
* 1240835 :    Totally implemented with issues

## 2.4. 1240868 - Structured cable design for Terminal 2 #
### Outcomes : ###
No âmbito da tarefa T.1.1, foi elaborado o projeto de cablagem estruturada para os dois pisos do Terminal 2 (Nível 1 — Arrivals e Nível 4 — Departures), bem como o backbone de campus.
Para cada piso foram desenvolvidos e documentados os seguintes elementos: o cálculo detalhado do número de tomadas de rede para todas as salas com base na fórmula normativa (área ÷ 10 × 2), incluindo tomadas de paredes externas (1 a cada 5 metros nas paredes direita e inferior) e tomadas dedicadas aos WAPs; plantas esquemáticas com a distribuição de tomadas por sala; o deployment dos cross-connects (HC, IC no Nível 1, e ligação ao IC no Nível 4); os caminhos de cabo (pathways) com justificação das rotas escolhidas (teto falso e underfloor); e inventários detalhados de cabo CAT7 e fibra ótica multimodo com comprimentos reais, margem de 15% e redundância ×2 na fibra. O inventário de hardware inclui patch panels, patch cords, switches, WAPs e enclosures. Foi ainda elaborado o inventário final do Terminal 2 consolidado por nível, e o inventário de campus com os quatro terminais.

1240850-Totally implemented with no issues
* 1240830 :    Totally implemented with issues
* 1240835 :    Totally implemented with issues


