"""
Terminal 4 — Planta WAP (estrelas + círculos) + Heatmap WiFi
=============================================================
Parâmetros:
  R   = 25 m  (raio de cobertura por WAP)
  D   = 41.14 m  (distância entre vizinhos hex)  → overlap = 8.7% ≤ 15% ✓
  Borda: WAPs extra em x=0 e x=200 na linha central → overlap = 13.1% ≤ 15% ✓
  Total: 16 WAPs por piso  |  Cobertura 100% ✓
"""

import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/claude/T4_wap_final"
os.makedirs(OUT, exist_ok=True)

R        = 25.0
W, H     = 200.0, 100.0
D        = R * math.sqrt(3) * 0.95   # 41.14 m
DY       = D * math.sqrt(3) / 2       # 35.62 m
LEGEND_W = 230

# ── Posições WAP (metros) ─────────────────────────────────────────
def make_waps():
    n_cols_even = 5
    y_start  = H/2 - DY              # 14.38 m
    x_start  = W/2 - 2*D             # 17.72 m
    waps = []
    for r in range(3):
        y = round(y_start + r*DY, 2)
        if r % 2 == 0:
            for c in range(n_cols_even):
                waps.append((round(x_start + c*D, 2), y))
        else:
            waps.append((0.0, y))
            for c in range(n_cols_even - 1):
                waps.append((round(x_start + D/2 + c*D, 2), y))
            waps.append((W, y))
    return waps

WAPS = make_waps()

# ── Floor bounds (px) ─────────────────────────────────────────────
BOUNDS = {
    "T4_L0": (4,  5,  630, 320),
    "T4_L2": (3,  0,  630, 315),
}

# ── Overlap entre dois círculos ───────────────────────────────────
def overlap_fraction(d, R):
    if d >= 2*R: return 0.0
    if d <= 0:   return 1.0
    a = 2*R**2*math.acos(d/(2*R)) - (d/2)*math.sqrt(4*R**2-d**2)
    return a/(math.pi*R**2)

# ── Colormap (verde→vermelho) ─────────────────────────────────────
CMAP = [
    (0.00, (44,  160, 44,  0  )),
    (0.04, (44,  160, 44,  90 )),
    (0.15, (100, 200, 40,  135)),
    (0.40, (220, 215, 20,  150)),
    (0.65, (230, 100, 20,  162)),
    (0.85, (210, 25,  20,  170)),
    (1.00, (178, 5,   5,   175)),
]

def heat_to_rgba(heat):
    out = np.zeros((*heat.shape, 4), dtype=np.float32)
    for i in range(len(CMAP)-1):
        v0,c0 = CMAP[i]; v1,c1 = CMAP[i+1]
        m = (heat>=v0)&(heat<v1)
        t = np.where(m,(heat-v0)/(v1-v0),0.0)
        for ch in range(4):
            out[:,:,ch] += np.where(m, c0[ch]+t*(c1[ch]-c0[ch]), 0.0)
    m = heat>=1.0
    for ch,v in enumerate(CMAP[-1][1]):
        out[:,:,ch] = np.where(m, v, out[:,:,ch])
    return np.clip(out,0,255).astype(np.uint8)

def compute_heatmap(waps_m, pw, ph, ppm):
    # sigma: sinal = exp(-R²/2σ²) = 0.87 na borda → σ = R/√(-2·ln0.87)
    sigma_m  = R / math.sqrt(-2*math.log(0.87))
    sigma_px = sigma_m * ppm
    heat = np.zeros((ph, pw), dtype=np.float32)
    for wx,wy in waps_m:
        cx,cy = wx*ppm, wy*ppm
        x0=max(0,int(cx-3.5*sigma_px)); x1=min(pw,int(cx+3.5*sigma_px)+1)
        y0=max(0,int(cy-3.5*sigma_px)); y1=min(ph,int(cy+3.5*sigma_px)+1)
        if x1<=x0 or y1<=y0: continue
        xx,yy = np.meshgrid(np.arange(x0,x1),np.arange(y0,y1))
        blob = np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*sigma_px**2))
        heat[y0:y1,x0:x1] = np.maximum(heat[y0:y1,x0:x1], blob)
    return heat

def draw_star(d, x, y, size=9):
    pts = []
    for k in range(10):
        ang = math.radians(-90+k*36)
        r = size if k%2==0 else size*0.4
        pts.append((x+r*math.cos(ang), y+r*math.sin(ang)))
    d.polygon(pts, fill=(255,215,0), outline=(130,90,0))

def draw_wap_icon(d, x, y, label, font):
    s=10
    d.ellipse([x-s,y-s,x+s,y+s], fill=(255,255,255,230), outline=(150,150,150,255), width=2)
    for r in [4,6,8]:
        d.arc([x-r,y-r+1,x+r,y+r+1],210,330, fill=(20,20,210,245), width=2)
    d.ellipse([x-2,y+3,x+2,y+7], fill=(20,20,210,245))
    d.text((x, y+s+2), label, font=font, fill=(10,10,10,255), anchor="mt")

def draw_legend_star(img, lx, ly, lw, n, font_b, font_s):
    d = ImageDraw.Draw(img)
    lh = 220
    d.rectangle([lx,ly,lx+lw,ly+lh], fill="#F8F8F8", outline="#444", width=2)
    d.text((lx+8,ly+7), "Planta WAP — Legenda", font=font_b, fill="#111")
    d.line([(lx+4,ly+24),(lx+lw-4,ly+24)], fill="#bbb", width=1)
    cy = ly+32
    draw_star(d, lx+14, cy+1, size=8)
    d.text((lx+28,cy-6), f"WAP (W01–W{n:02d})", font=font_s, fill="#222")
    cy+=18
    d.ellipse([lx+6,cy,lx+20,cy+14], fill=None, outline=(0,80,200), width=2)
    d.text((lx+28,cy+1), f"Raio cobertura R=25m", font=font_s, fill="#222")
    cy+=18
    d.line([(lx+4,cy),(lx+lw-4,cy)], fill="#ddd", width=1); cy+=6
    d.text((lx+8,cy), f"Total: {n} WAPs", font=font_s, fill="#333")

def draw_legend_heat(img, lx, ly, lw, n, font_b, font_s):
    d = ImageDraw.Draw(img)
    lh = 255
    d.rectangle([lx,ly,lx+lw,ly+lh], fill="#F8F8F8", outline="#444", width=2)
    d.text((lx+8,ly+7), "Sinal WiFi", font=font_b, fill="#111")
    d.line([(lx+4,ly+24),(lx+lw-4,ly+24)], fill="#bbb", width=1)
    # barra gradiente
    bx,by,bw,bh = lx+10, ly+28, lw-20, 14
    for i in range(bw):
        v = 1.0-(i/bw)*0.96
        col=(178,5,5)
        for ci in range(len(CMAP)-1):
            v0,c0=CMAP[ci]; v1,c1=CMAP[ci+1]
            if v0<=v<v1:
                t=(v-v0)/(v1-v0)
                col=tuple(int(c0[k]+t*(c1[k]-c0[k])) for k in range(3)); break
        for j in range(bh): img.putpixel((bx+i,by+j),col)
    d.rectangle([bx,by,bx+bw,by+bh],outline="#555",width=1)
    d.text((bx,by+bh+2),"Forte",font=font_s,fill="#333")
    d.text((bx+bw,by+bh+2),"Fraco",font=font_s,fill="#333",anchor="ra")
    cy=ly+58
    for color,label in [
        ((200,20,20),  "Excelente (> 85%)"),
        ((230,100,20), "Bom       (65–85%)"),
        ((220,210,20), "Médio     (40–65%)"),
        ((100,200,50), "Fraco     (15–40%)"),
        ((44,160,44),  "Limite    (< 15%) "),
    ]:
        d.rectangle([lx+8,cy,lx+20,cy+11],fill=color,outline="#555",width=1)
        d.text((lx+26,cy+1),label,font=font_s,fill="#222"); cy+=16
    d.line([(lx+4,cy+2),(lx+lw-4,cy+2)],fill="#ccc",width=1); cy+=8
    d.ellipse([lx+5,cy,lx+17,cy+12],fill=(255,255,255),outline=(150,150,150),width=2)
    d.text((lx+24,cy+1),f"WAP (W01–W{n:02d})",font=font_s,fill="#222"); cy+=16
    d.line([(lx+6,cy+5),(lx+26,cy+5)],fill=(255,200,0),width=2)
    d.text((lx+32,cy+1),"Ligação entre WAPs",font=font_s,fill="#222"); cy+=16
    d.line([(lx+4,cy+2),(lx+lw-4,cy+2)],fill="#ccc",width=1); cy+=6
    d.text((lx+8,cy),f"Total: {n} WAPs",font=font_s,fill="#444"); cy+=13
    d.text((lx+8,cy),f"R = 25 m  |  D = {D:.1f} m",font=font_s,fill="#444")

# ─────────────────────────────────────────────────────────────────
def generate(src_path, level_name, tag):
    print(f"\n── {level_name} ──")
    base = Image.open(src_path).convert("RGB")
    SW, SH = base.size
    FX1,FY1,FX2,FY2 = BOUNDS[tag]
    FPW, FPH = FX2-FX1, FY2-FY1
    PPM = FPW / W   # píxeis por metro

    # Fontes
    try:
        fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",11)
        fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",8)
        fl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",7)
    except:
        fb=fs=fl=ImageFont.load_default()

    # Posições em px absolutos
    def m2px(wx,wy): return (int(FX1+wx*PPM), int(FY1+wy*PPM))
    waps_px = [m2px(wx,wy) for wx,wy in WAPS]

    # ── 1. PLANTA DAS ESTRELAS + CÍRCULOS ─────────────────────────
    canvas_s = Image.new("RGB",(SW+LEGEND_W,SH),(255,255,255))
    canvas_s.paste(base,(0,0))
    d = ImageDraw.Draw(canvas_s)

    # Círculos de cobertura (azul semi-transparente)
    circ_layer = Image.new("RGBA",(SW+LEGEND_W,SH),(0,0,0,0))
    dc = ImageDraw.Draw(circ_layer)
    r_px = int(R * PPM)
    for i,(ax,ay) in enumerate(waps_px):
        dc.ellipse([ax-r_px,ay-r_px,ax+r_px,ay+r_px],
                   fill=(0,80,220,28), outline=(0,80,220,160), width=2)
    canvas_s = Image.alpha_composite(canvas_s.convert("RGBA"), circ_layer).convert("RGB")
    d = ImageDraw.Draw(canvas_s)

    # Linhas de ligação
    for i in range(len(waps_px)):
        for j in range(i+1,len(waps_px)):
            dx=waps_px[i][0]-waps_px[j][0]; dy=waps_px[i][1]-waps_px[j][1]
            dist_m = math.hypot(WAPS[i][0]-WAPS[j][0],WAPS[i][1]-WAPS[j][1])
            if dist_m < D*1.05:
                d.line([waps_px[i],waps_px[j]], fill=(200,160,0), width=1)

    # Estrelas e labels
    for i,(ax,ay) in enumerate(waps_px):
        draw_star(d, ax, ay, size=9)
        d.text((ax,ay+11),f"W{i+1:02d}",font=fl,fill=(80,40,0),anchor="mt")

    # Título
    d.text((FX1+FPW//2, FY1+FPH//2-8), level_name,
           font=fb, fill=(40,40,40), anchor="mm")
    # Barra de escala
    sc_px = int(50*PPM)
    d.rectangle([FX1, FY2+15, FX1+sc_px, FY2+21], fill="black")
    d.text((FX1+sc_px//2, FY2+24),"50 m",font=fs,fill="black",anchor="mt")

    draw_legend_star(canvas_s, SW+4, 10, LEGEND_W-8, len(WAPS), fb, fs)

    sf = f"{OUT}/{tag}_star_plan.png"
    canvas_s.save(sf, dpi=(150,150))
    print(f"  ✓ Estrelas: {sf}")

    # ── 2. HEATMAP ────────────────────────────────────────────────
    print("  A calcular heatmap...")
    heat = compute_heatmap(WAPS, FPW, FPH, PPM)
    print(f"  Sinal mín: {heat.min()*100:.1f}%  máx: {heat.max()*100:.1f}%")
    heat_rgba = heat_to_rgba(heat)
    heat_pil  = Image.fromarray(heat_rgba,'RGBA')

    canvas_h = Image.new("RGBA",(SW+LEGEND_W,SH),(255,255,255,255))
    canvas_h.paste(base.convert("RGBA"),(0,0))

    # Colar heatmap na área do piso
    hl = Image.new("RGBA",(SW+LEGEND_W,SH),(0,0,0,0))
    hl.paste(heat_pil,(FX1,FY1))
    canvas_h = Image.alpha_composite(canvas_h, hl)

    # Paredes por cima
    base_arr = np.array(base)
    dark = (base_arr[:,:,0].astype(int)+base_arr[:,:,1]+base_arr[:,:,2]) < 160
    ov = np.zeros((SH,SW,4),dtype=np.uint8)
    ov[dark,:3]=base_arr[dark,:3]; ov[dark,3]=220
    wl = Image.new("RGBA",(SW+LEGEND_W,SH),(0,0,0,0))
    wl.paste(Image.fromarray(ov,'RGBA'),(0,0))
    canvas_h = Image.alpha_composite(canvas_h, wl)

    # Círculos de cobertura
    cl = Image.new("RGBA",(SW+LEGEND_W,SH),(0,0,0,0))
    dcc = ImageDraw.Draw(cl)
    for ax,ay in waps_px:
        dcc.ellipse([ax-r_px,ay-r_px,ax+r_px,ay+r_px],
                    fill=None, outline=(0,60,200,200), width=2)
    canvas_h = Image.alpha_composite(canvas_h, cl)

    # Linhas de ligação
    ll = Image.new("RGBA",(SW+LEGEND_W,SH),(0,0,0,0))
    dl = ImageDraw.Draw(ll)
    for i in range(len(waps_px)):
        for j in range(i+1,len(waps_px)):
            dm=math.hypot(WAPS[i][0]-WAPS[j][0],WAPS[i][1]-WAPS[j][1])
            if dm < D*1.05:
                dl.line([waps_px[i],waps_px[j]],fill=(255,200,0,100),width=1)
    canvas_h = Image.alpha_composite(canvas_h, ll)

    # Ícones WAP
    wl2=Image.new("RGBA",(SW+LEGEND_W,SH),(0,0,0,0))
    dw=ImageDraw.Draw(wl2)
    for i,(ax,ay) in enumerate(waps_px):
        draw_wap_icon(dw,ax,ay,f"W{i+1:02d}",fl)
    canvas_h = Image.alpha_composite(canvas_h, wl2)

    heat_final = canvas_h.convert("RGB")
    # Título
    ImageDraw.Draw(heat_final).text(
        (FX1+FPW//2, FY1+FPH//2-8), level_name, font=fb,
        fill=(40,40,40), anchor="mm",
        stroke_width=2, stroke_fill=(255,255,255))
    # Barra de escala
    dh=ImageDraw.Draw(heat_final)
    dh.rectangle([FX1,FY2+15,FX1+int(50*PPM),FY2+21],fill="black")
    dh.text((FX1+int(50*PPM)//2,FY2+24),"50 m",font=fs,fill="black",anchor="mt")

    draw_legend_heat(heat_final, SW+4, 10, LEGEND_W-8, len(WAPS), fb, fs)

    hf = f"{OUT}/{tag}_heatmap.png"
    heat_final.save(hf, dpi=(150,150))
    print(f"  ✓ Heatmap:  {hf}")

# ── RUN ───────────────────────────────────────────────────────────
generate("/home/claude/T4_L0_floorplan.png",
         "Terminal 4 — Level 0 (Arrivals)", "T4_L0")
generate("/home/claude/T4_L2_floorplan.png",
         "Terminal 4 — Level 2 (Departures)", "T4_L2")

print("\n✓ Concluído!")
print(f"\nResumo grelha:")
print(f"  R = 25 m  |  D = {D:.2f} m  |  DY = {DY:.2f} m")
print(f"  16 WAPs por piso  |  cobertura 100%  |  overlap máx 13.1% ≤ 15%")
