import math
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

output_dir = "/home/claude/T4_outputs_v4"
os.makedirs(output_dir, exist_ok=True)

DARK       = '#6b1a1a'
BG         = '#f7f4ef'
GRID_C     = '#ccc8c0'
BORDER_OUT = '#3a0a0a'
BORDER_IN  = '#7a2020'
OUTLET_SZ  = 0.38


def draw_outlet(ax, x, y, s=OUTLET_SZ):
    ax.add_patch(mpatches.FancyBboxPatch(
        (x - s/2, y - s/2), s, s, boxstyle="square,pad=0",
        facecolor='white', edgecolor=DARK, linewidth=1.3, zorder=5))
    ax.add_patch(plt.Circle((x, y), s * 0.31,
        facecolor='white', edgecolor=DARK, linewidth=1.1, zorder=6))
    ax.add_patch(plt.Circle((x, y), s * 0.10,
        facecolor=DARK, edgecolor='none', zorder=7))


def best_grid(n_postos, comp, larg):
    """
    Escolhe n_cols e n_rows que melhor equilibram:
      • aspect ratio da sala
      • linha final bem preenchida (≥ 50%)
      • espaçamento uniforme
    """
    if n_postos <= 1:
        return 1, n_postos
    aspect = comp / larg
    min_cols = 2 if aspect >= 1.0 else 1
    nc_ideal = max(min_cols, round(math.sqrt(n_postos * aspect)))

    best_nc, best_score = nc_ideal, float('inf')

    for nc in range(max(min_cols, nc_ideal - 5), nc_ideal + 6):
        if nc < min_cols or nc > n_postos:
            continue
        nr = math.ceil(n_postos / nc)
        last = n_postos - nc * (nr - 1)
        last_fill = last / nc          # 1.0 = linha completa

        actual_ratio = nc / nr
        ratio_err = abs(actual_ratio / aspect - 1)

        # Penaliza fortemente última linha com < 50% preenchimento
        if last_fill < 0.50:
            underfill_penalty = (0.50 - last_fill) * 4.0
        else:
            underfill_penalty = 0.0

        score = ratio_err * 1.0 + underfill_penalty + (nc * nr - n_postos) / n_postos * 0.3

        if score < best_score:
            best_score = score
            best_nc = nc

    return best_nc, math.ceil(n_postos / best_nc)


def outlet_positions(n_postos, comp, larg):
    """
    Distribui n_postos numa grelha centrada na sala.
    • Usa divisão (n+1) → espaçamento uniforme sem margens percentuais excessivas
    • Última linha incompleta é centrada horizontalmente
    """
    if n_postos == 0:
        return []

    n_cols, n_rows = best_grid(n_postos, comp, larg)
    last_row_count = n_postos - n_cols * (n_rows - 1)

    spacing_x = comp / (n_cols + 1)   # espaçamento colunas
    spacing_y = larg / (n_rows + 1)   # espaçamento linhas

    positions = []
    for r in range(n_rows):
        y = larg - (r + 1) * spacing_y   # de cima para baixo

        if r == n_rows - 1:
            # Última linha: centra os postos restantes
            k = last_row_count
            if k == n_cols:
                # Linha completa — usa grelha normal
                row_xs = [(c + 1) * spacing_x for c in range(k)]
            elif k == 1:
                row_xs = [comp / 2]
            else:
                # Centra k postos mantendo o mesmo spacing_x
                total_span = spacing_x * (k - 1)
                x_start    = comp / 2 - total_span / 2
                row_xs = [x_start + i * spacing_x for i in range(k)]
        else:
            row_xs = [(c + 1) * spacing_x for c in range(n_cols)]

        for x in row_xs:
            positions.append((x, y))

    return positions


def create_plan(nome, area, tomadas, postos, filename, nivel, larg, comp):
    scale  = 0.18
    fig_w  = comp * scale + 5.5
    fig_h  = larg * scale + 2.8
    fig, ax = plt.subplots(figsize=(max(fig_w, 9), max(fig_h, 5)))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # Fundo da sala
    ax.add_patch(mpatches.FancyBboxPatch(
        (0, 0), comp, larg, boxstyle="square,pad=0",
        facecolor=BG, edgecolor='none', zorder=0))

    # Bordas duplas
    for bw, bc in [(0.28, BORDER_OUT), (0.10, BORDER_IN)]:
        ax.add_patch(mpatches.FancyBboxPatch(
            (-bw/2, -bw/2), comp + bw, larg + bw,
            boxstyle="square,pad=0",
            facecolor='none', edgecolor=bc, linewidth=bw * 28, zorder=3))

    # Grelha técnica 2.5 m
    x = 0
    while x <= comp + 0.01:
        ax.plot([x, x], [0, larg], color=GRID_C, lw=0.5, zorder=1)
        x += 2.5
    y = 0
    while y <= larg + 0.01:
        ax.plot([0, comp], [y, y], color=GRID_C, lw=0.5, zorder=1)
        y += 2.5

    # Tomadas
    positions = outlet_positions(postos, comp, larg)
    for (px, py) in positions:
        draw_outlet(ax, px, py)

    # Anotações (canto sup-esq e inf-dir)
    if positions:
        p0 = positions[0]
        ax.annotate("Posto de rede\n2 tomadas / h=30cm",
                    xy=p0,
                    xytext=(max(0, p0[0] - comp * 0.14), p0[1] + larg * 0.22),
                    fontsize=6.5, color=DARK,
                    arrowprops=dict(arrowstyle='->', color=DARK, lw=0.8), zorder=8)
        p1 = positions[-1]
        ax.annotate("Posto de rede\n2 tomadas / h=30cm",
                    xy=p1,
                    xytext=(comp + comp * 0.06, p1[1]),
                    fontsize=6.5, color=DARK,
                    arrowprops=dict(arrowstyle='->', color=DARK, lw=0.8), zorder=8)

    # Cotas
    dim_gap_h = larg * 0.18
    dim_gap_v = comp * 0.06
    ay = larg + dim_gap_h
    ax.plot([0, comp], [ay, ay], color=DARK, lw=0.9)
    ax.plot([0, 0],        [larg, ay], color=DARK, lw=0.6, ls='--')
    ax.plot([comp, comp],  [larg, ay], color=DARK, lw=0.6, ls='--')
    ax.annotate('', xy=(comp, ay), xytext=(0, ay),
                arrowprops=dict(arrowstyle='<->', color=DARK, lw=0.9))
    ax.text(comp / 2, ay + larg * 0.04, f"{comp:.2f} m",
            ha='center', va='bottom', fontsize=8.5, color=DARK)

    ax2 = comp + dim_gap_v
    ax.plot([ax2, ax2], [0, larg], color=DARK, lw=0.9)
    ax.plot([comp, ax2], [0, 0],    color=DARK, lw=0.6, ls='--')
    ax.plot([comp, ax2], [larg, larg], color=DARK, lw=0.6, ls='--')
    ax.annotate('', xy=(ax2, larg), xytext=(ax2, 0),
                arrowprops=dict(arrowstyle='<->', color=DARK, lw=0.9))
    ax.text(ax2 + comp * 0.025, larg / 2, f"{larg:.2f} m",
            ha='left', va='center', fontsize=8.5, color=DARK, rotation=90)

    # Legenda
    leg_x = comp + dim_gap_v + comp * 0.10
    leg_y = larg
    ax.text(leg_x, leg_y, "Legenda:", fontsize=9, fontweight='bold',
            color='black', va='top')
    sym_y = leg_y - larg * 0.14
    sym_s = max(OUTLET_SZ, larg * 0.08)
    draw_outlet(ax, leg_x + sym_s * 0.7, sym_y, s=sym_s)
    ax.text(leg_x + sym_s * 1.6, sym_y,
            "Posto de rede\n2 tomadas / h=30cm",
            fontsize=7.5, color=DARK, va='center')
    info_y = sym_y - larg * 0.18
    dy     = larg * 0.13
    for i, line in enumerate([
        f"Area:     {area:.2f} m²",
        f"Tomadas:  {tomadas}",
        f"Postos:   {postos}",
        "Norma:    ISO 8877"
    ]):
        ax.text(leg_x, info_y - i * dy, line,
                fontsize=8, color='black', va='top', family='monospace')

    # Caption bar
    cap_h  = larg * 0.22
    cap_y0 = -cap_h - larg * 0.08
    ax.add_patch(mpatches.FancyBboxPatch(
        (0, cap_y0), comp, cap_h, boxstyle="square,pad=0",
        facecolor='#f0ece4', edgecolor=DARK, linewidth=1.2, zorder=0))
    ax.text(comp / 2, cap_y0 + cap_h * 0.70,
            f"{nivel} — {nome}",
            ha='center', va='center', fontsize=10, fontweight='bold', color='black')
    ax.text(comp / 2, cap_y0 + cap_h * 0.22,
            f"Area: {area:.2f} m²  |  Tomadas: {tomadas}  |  "
            f"Postos (2 tom.): {postos}  |  Escala: 1:50",
            ha='center', va='center', fontsize=7.8, color='#333333')

    ax.set_xlim(-comp * 0.18, comp + comp * 0.55)
    ax.set_ylim(cap_y0 - larg * 0.04, larg + larg * 0.32)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout(pad=0.3)
    plt.savefig(filename, dpi=120, bbox_inches='tight', facecolor='white')
    plt.close()


# ── Salas SEM tomadas (não gerar) ─────────────────────────────────
NO_OUTLETS_L0 = {4, 8, 9, 10, 11}
NO_OUTLETS_L2 = {3, 6, 8, 10, 11}

# ── LEVEL 0 ───────────────────────────────────────────────────────
level0 = [
    ("Sala 1",  316.70, 31.67, 10.00),
    ("Sala 2",  300.00, 30.00, 10.00),
    ("Sala 3",  233.30, 23.33, 10.00),
    ("Sala 4",  100.00, 10.00, 10.00),
    ("Sala 5",  183.30, 18.33, 10.00),
    ("Sala 6",  283.30, 28.33, 10.00),
    ("Sala 7",  233.30, 23.33, 10.00),
    ("Sala 8",  250.00, 25.00, 10.00),
    ("Sala 9",  250.00, 25.00, 10.00),
    ("Sala 10", 288.90, 13.33, 21.67),
    ("Sala 11", 288.90, 13.33, 21.67),
    ("Sala 12", 333.30, 25.00, 13.33),
    ("Sala 13", 288.90, 21.67, 13.33),
    ("Sala 14", 400.00, 30.00, 13.33),
    ("Sala 15", 288.90, 21.67, 13.33),
    ("Sala 16", 288.90, 21.67, 13.33),
]

print("=== LEVEL 0 ===")
for i, (nome, area, comp, larg) in enumerate(level0, 1):
    if i in NO_OUTLETS_L0:
        print(f"  {nome}: SEM tomadas — ignorado")
        continue
    tomadas = math.ceil(area / 10) * 2
    postos  = math.ceil(tomadas / 2)
    nc, nr  = best_grid(postos, comp, larg)
    last    = postos - nc * (nr - 1)
    key = nome.lower().replace(" ", "_")
    create_plan(nome, area, tomadas, postos,
                f"{output_dir}/T4_L0_{key}.png",
                "Terminal 4 — Level 0 (Arrivals)", larg, comp)
    print(f"  {nome}: {tomadas} tom / {postos} postos → {nc}×{nr}  last={last}/{nc}")

# ── LEVEL 2 ───────────────────────────────────────────────────────
level2 = [
    ("Sala 1",  388.90, 33.33, 11.67),
    ("Sala 2",  350.00, 30.00, 11.67),
    ("Sala 3",  100.00, 10.00, 10.00),
    ("Sala 4",  183.30, 18.33, 10.00),
    ("Sala 5",  250.00, 25.00, 10.00),
    ("Sala 6",  233.30, 23.33, 10.00),
    ("Sala 7",  150.00, 10.00, 15.00),
    ("Sala 8",  250.00, 25.00, 10.00),
    ("Sala 9",  150.00, 10.00, 15.00),
    ("Sala 10", 288.90, 13.33, 21.67),
    ("Sala 11", 288.90, 13.33, 21.67),
    ("Sala 12", 155.60, 23.33,  6.67),
    ("Sala 13", 100.00, 15.00,  6.67),
    ("Sala 14", 122.20, 18.33,  6.67),
    ("Sala 15", 122.20, 18.33,  6.67),
    ("Sala 16", 144.40, 21.67,  6.67),
    ("Sala 17", 233.30, 23.33, 10.00),
    ("Sala 18", 216.70, 21.67, 10.00),
    ("Sala 19", 300.00, 30.00, 10.00),
    ("Sala 20", 216.70, 21.67, 10.00),
    ("Sala 21", 216.70, 21.67, 10.00),
]

print("\n=== LEVEL 2 ===")
for i, (nome, area, comp, larg) in enumerate(level2, 1):
    if i in NO_OUTLETS_L2:
        print(f"  {nome}: SEM tomadas — ignorado")
        continue
    tomadas = math.ceil(area / 10) * 2
    postos  = math.ceil(tomadas / 2)
    nc, nr  = best_grid(postos, comp, larg)
    last    = postos - nc * (nr - 1)
    key = nome.lower().replace(" ", "_")
    create_plan(nome, area, tomadas, postos,
                f"{output_dir}/T4_L2_{key}.png",
                "Terminal 4 — Level 2 (Departures)", larg, comp)
    print(f"  {nome}: {tomadas} tom / {postos} postos → {nc}×{nr}  last={last}/{nc}")

print("\nConcluído!")
