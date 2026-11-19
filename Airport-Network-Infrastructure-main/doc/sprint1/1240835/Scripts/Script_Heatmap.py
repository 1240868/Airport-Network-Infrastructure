"""
WAP Heatmap Generator — Terminal 5 (Piso 0 e Piso 2)
=====================================================
Gera heatmaps de cobertura WiFi sobrepostos às plantas dos pisos.

Piso 0 (Arrivals) : 400 x 150 m  |  50 WAPs
Piso 2 (Departures): 400 x 150 m  |  50 WAPs
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math

# ── CONFIGURAÇÃO GLOBAL ───────────────────────────────────────────────────────

LEGEND_WIDTH = 290   # largura da margem direita para legenda
PADDING      = 20    # margem extra em volta da planta (px)
COVERAGE_M2  = math.pi * 25**2   # π·r² com r=25m → 1963.5 m²

# ── CONFIGURAÇÃO POR PISO ────────────────────────────────────────────────────

FLOORS = {
    "Piso_0": {
        "src"        : "/mnt/user-data/uploads/Piso_0_AP_distribution_.png",
        "out"        : "/mnt/user-data/outputs/T5_Piso0_heatmap.png",
        "title"      : "Terminal 5 – Level 0 (Arrivals)",
        # Bounds do piso na imagem source (px)
        "fx1": 12, "fy1":  5,
        "fx2": 309, "fy2": 777,
        # Dimensões reais do piso (m) — 150 m de largura, 400 m de comprimento
        "floor_w_m"  : 150.0,
        "floor_h_m"  : 400.0,
        # Posições das estrelas (WAPs) em píxeis na imagem source
        # Detetadas automaticamente da imagem de distribuição
        "stars": [
            (18,  11), (89,  11), (160,  11), (231,  11), (302,  11),
            (53,  87), (124,  87), (195,  87), (266,  87),
            (18, 163), (89, 163), (160, 163), (231, 163), (302, 163),
            (53, 239), (124, 239), (195, 239), (266, 239),
            (18, 315), (89, 315), (160, 315), (231, 315), (302, 315),
            (53, 391), (124, 391), (195, 391), (266, 391),
            (18, 467), (89, 467), (160, 467), (231, 467), (302, 467),
            (53, 543), (124, 543), (195, 543), (266, 543),
            (18, 619), (89, 619), (160, 619), (231, 619), (302, 619),
            (53, 695), (124, 695), (195, 695), (266, 695),
            (18, 771), (89, 771), (160, 771), (231, 771), (302, 771),
        ],
    },
    "Piso_2": {
        "src"        : "/mnt/user-data/uploads/Piso_2_AP_distribution.png",
        "out"        : "/mnt/user-data/outputs/T5_Piso2_heatmap.png",
        "title"      : "Terminal 5 – Level 2 (Departures)",
        "fx1":  6, "fy1":  9,
        "fx2": 301, "fy2": 781,
        "floor_w_m"  : 150.0,
        "floor_h_m"  : 400.0,
        "stars": [
            (12,  15), (82,  15), (153,  15), (224,  15), (295,  15),
            (47,  91), (118,  91), (188,  91), (259,  91),
            (12, 167), (82, 167), (153, 167), (224, 167), (295, 167),
            (47, 243), (118, 243), (188, 243), (259, 243),
            (12, 319), (82, 319), (153, 319), (224, 319), (295, 319),
            (47, 395), (118, 395), (188, 395), (259, 395),
            (12, 471), (82, 471), (153, 471), (224, 471), (295, 471),
            (47, 547), (118, 547), (188, 547), (259, 547),
            (12, 623), (82, 623), (153, 623), (224, 623), (295, 623),
            (47, 699), (118, 699), (188, 699), (259, 699),
            (12, 775), (82, 775), (153, 775), (224, 775), (295, 775),
        ],
    },
}

# ── FUNÇÕES ───────────────────────────────────────────────────────────────────

def build_colormap():
    """Verde(fraco) → amarelo → laranja → vermelho(forte)."""
    return [
        (0.00, (  0,   0,   0,   0)),
        (0.05, ( 60, 170,  60, 110)),
        (0.18, (120, 210,  40, 150)),
        (0.35, (230, 220,  20, 165)),
        (0.55, (235, 120,  20, 175)),
        (0.75, (220,  40,  20, 180)),
        (1.00, (200,  10,  10, 185)),
    ]


def apply_colormap(heat, floor_mask, cmap):
    H, W = heat.shape
    rgba = np.zeros((H, W, 4), dtype=np.float32)
    for i in range(len(cmap) - 1):
        v0, c0 = cmap[i];  v1, c1 = cmap[i+1]
        mask = (heat >= v0) & (heat < v1) & floor_mask
        t = np.where(mask, (heat - v0) / (v1 - v0), 0.0)
        for ch in range(4):
            rgba[:, :, ch] += np.where(mask, c0[ch] + t * (c1[ch] - c0[ch]), 0.0)
    last = (heat >= 1.0) & floor_mask
    for ch, v in enumerate(cmap[-1][1]):
        rgba[:, :, ch] = np.where(last, v, rgba[:, :, ch])
    return np.clip(rgba, 0, 255).astype(np.uint8)


def draw_wap_symbol(d, cx, cy, n, font):
    s = 11
    d.ellipse([cx-s, cy-s, cx+s, cy+s],
              fill=(255, 255, 255, 220), outline=(160, 160, 160, 255), width=2)
    for r in [3, 5, 8]:
        d.arc([cx-r, cy-r, cx+r, cy+r], 210, 330, fill=(20, 20, 210, 230), width=2)
    d.ellipse([cx-2, cy+3, cx+2, cy+7], fill=(20, 20, 210, 230))
    d.text((cx, cy + s + 3), f"W{n:02d}", font=font,
           fill=(10, 10, 10, 255), anchor="mt")


def draw_legend(img, lx, ly, lw, cmap, n_waps, r_m, coverage_m2,
                font_bold, font_small, title):
    d = ImageDraw.Draw(img)
    box_h = 360
    d.rectangle([lx, ly, lx+lw, ly+box_h], fill="#F9F9F9", outline="#444", width=2)

    # Título (duas linhas se necessário)
    d.text((lx+8, ly+8), title, font=font_bold, fill="#111")
    d.line([(lx+4, ly+28), (lx+lw-4, ly+28)], fill="#999", width=1)

    # Barra de gradiente
    bx, by, bw, bh = lx+10, ly+36, lw-20, 16
    for i in range(bw):
        v = 1.0 - (i / bw) * 0.95
        col = (200, 10, 10)
        for ci in range(len(cmap)-1):
            v0, c0 = cmap[ci]; v1, c1 = cmap[ci+1]
            if v0 <= v < v1:
                t = (v-v0)/(v1-v0)
                col = tuple(int(c0[ch]+t*(c1[ch]-c0[ch])) for ch in range(3))
                break
        for j in range(bh):
            img.putpixel((bx+i, by+j), col)
    d.rectangle([bx, by, bx+bw, by+bh], outline="#666", width=1)
    d.text((bx,      by+bh+3), "Forte", font=font_small, fill="#333")
    d.text((bx+bw,   by+bh+3), "Fraco", font=font_small, fill="#333", anchor="ra")

    # Legenda de cores
    ly2 = ly + 78
    for color, label in [
        ((210,  20,  20), "Excelente  (> 85%)"),
        ((230, 100,  20), "Bom        (65–85%)"),
        ((220, 220,  20), "Médio      (40–65%)"),
        ((100, 200,  60), "Fraco      (15–40%)"),
        (( 60, 160,  60), "Limite     (<  15%)"),
    ]:
        d.rectangle([lx+8, ly2, lx+22, ly2+13], fill=color, outline="#555", width=1)
        d.text((lx+28, ly2+1), label, font=font_small, fill="#333")
        ly2 += 20

    d.line([(lx+4, ly2+4), (lx+lw-4, ly2+4)], fill="#ccc", width=1); ly2 += 12

    # Símbolo WAP
    d.ellipse([lx+5, ly2, lx+19, ly2+14],
              fill=(255,255,255), outline=(160,160,160), width=2)
    d.text((lx+26, ly2+1), f"WAP  (W01–W{n_waps:02d})",
           font=font_small, fill="#333"); ly2 += 20

    # Linha de ligação
    d.line([(lx+8, ly2+6), (lx+32, ly2+6)], fill=(255, 200, 0), width=2)
    d.text((lx+38, ly2+2), "Ligação entre WAPs",
           font=font_small, fill="#333"); ly2 += 20

    d.line([(lx+4, ly2+4), (lx+lw-4, ly2+4)], fill="#ccc", width=1); ly2 += 10

    # Estatísticas
    for txt in [
        f"Total WAPs : {n_waps}",
        f"Raio cobr. : {r_m:.1f} m",
        f"Área/WAP   : {coverage_m2:.0f} m²",
        f"Piso       : 400 × 150 m",
        f"Área total : 60 000 m²",
    ]:
        d.text((lx+8, ly2), txt, font=font_small, fill="#555"); ly2 += 17


# ── GERAÇÃO DE UM PISO ───────────────────────────────────────────────────────

def generate_heatmap(cfg):
    src_pil = Image.open(cfg["src"]).convert("RGB")
    SW, SH = src_pil.size

    # Padding extra em volta da planta + espaço para legenda à direita
    W_canvas = SW + PADDING * 2 + LEGEND_WIDTH
    H_canvas = SH + PADDING * 2

    fx1, fy1 = cfg["fx1"] + PADDING, cfg["fy1"] + PADDING
    fx2, fy2 = cfg["fx2"] + PADDING, cfg["fy2"] + PADDING
    floor_w_m, floor_h_m = cfg["floor_w_m"], cfg["floor_h_m"]

    # Escala px/m
    sx = (cfg["fx2"] - cfg["fx1"]) / floor_w_m
    sy = (cfg["fy2"] - cfg["fy1"]) / floor_h_m

    # Raio em píxeis
    r_m  = math.sqrt(COVERAGE_M2 / math.pi)   # = 25 m
    r_px = r_m * sx
    sigma = r_px * 0.6   # sigma mais apertado → transição mais visível

    print(f"\n[{cfg['title']}]")
    print(f"  Imagem original: {SW}×{SH} px  |  Canvas: {W_canvas}×{H_canvas} px")
    print(f"  Piso (com padding): {fx1},{fy1} → {fx2},{fy2}")
    print(f"  Escala: {sx:.3f} px/m (x), {sy:.3f} px/m (y)")
    print(f"  Raio: {r_m:.1f} m = {r_px:.1f} px  |  sigma={sigma:.1f} px")
    print(f"  WAPs: {len(cfg['stars'])}")

    # Fontes
    try:
        font_sm   = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        font_bold = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    except:
        font_sm = font_bold = ImageFont.load_default()

    # WAP coords deslocadas pelo padding
    waps = [(x + PADDING, y + PADDING, i+1) for i, (x, y) in enumerate(cfg["stars"])]

    # ── Heatmap gaussiano ────────────────────────────────────────────────────
    heat = np.zeros((H_canvas, W_canvas), dtype=np.float64)

    for cx, cy, _ in waps:
        pad = int(r_px * 3.0)
        x0, x1 = max(0, cx-pad), min(W_canvas, cx+pad)
        y0, y1 = max(0, cy-pad), min(H_canvas, cy+pad)
        xs = np.arange(x0, x1); ys = np.arange(y0, y1)
        if len(xs) == 0 or len(ys) == 0: continue
        xx, yy = np.meshgrid(xs, ys)
        blob = np.exp(-((xx-cx)**2 + (yy-cy)**2) / (2*sigma**2))
        heat[y0:y1, x0:x1] = np.maximum(heat[y0:y1, x0:x1], blob)

    heat = np.clip(heat, 0, 1.0)

    # Máscara do piso (só colorir dentro dos limites)
    floor_mask = np.zeros((H_canvas, W_canvas), dtype=bool)
    floor_mask[fy1:fy2, fx1:fx2] = True

    # ── Colormap e composição ────────────────────────────────────────────────
    cmap = build_colormap()
    heat_rgba = apply_colormap(heat, floor_mask, cmap)
    heat_img  = Image.fromarray(heat_rgba, 'RGBA')

    # Canvas branco, planta centrada com padding
    canvas = Image.new("RGBA", (W_canvas, H_canvas), (245, 245, 248, 255))
    canvas.paste(src_pil.convert("RGBA"), (PADDING, PADDING))
    canvas = Image.alpha_composite(canvas, heat_img)

    # ── Linhas de ligação entre WAPs vizinhos ────────────────────────────────
    max_conn = 48 * sx   # ~48 m em px
    ll = Image.new("RGBA", (W_canvas, H_canvas), (0, 0, 0, 0))
    ld = ImageDraw.Draw(ll)
    for i, (cx1, cy1, _) in enumerate(waps):
        for cx2, cy2, _ in waps[i+1:]:
            if math.hypot(cx2-cx1, cy2-cy1) < max_conn:
                ld.line([(cx1, cy1), (cx2, cy2)],
                        fill=(255, 200, 0, 90), width=1)
    canvas = Image.alpha_composite(canvas, ll)

    # ── Símbolos dos WAPs ────────────────────────────────────────────────────
    sl = Image.new("RGBA", (W_canvas, H_canvas), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sl)
    for cx, cy, n in waps:
        draw_wap_symbol(sd, cx, cy, n, font_sm)
    canvas = Image.alpha_composite(canvas, sl)

    # ── Legenda (centrada verticalmente à direita da planta) ─────────────────
    img_final = canvas.convert("RGB")
    leg_x = SW + PADDING * 2 + 8
    leg_y = PADDING
    leg_w = LEGEND_WIDTH - 16
    draw_legend(img_final, leg_x, leg_y, leg_w, cmap,
                len(waps), r_m, COVERAGE_M2, font_bold, font_sm, cfg["title"])

    img_final.save(cfg["out"], dpi=(150, 150))
    print(f"  → Guardado: {cfg['out']}")


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    for key, cfg in FLOORS.items():
        generate_heatmap(cfg)
    print("\nConcluído!")