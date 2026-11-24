"""V01 · Tráiler «El Quisco no termina en la playa» · 1080×1920 · 30 fps · estilo V00.
Genera edicion/index.html (HyperFrames), voz.wav (frases colocadas) y subtitulos.json.
Uso: python build_v01.py  (desde esta carpeta)"""
import json, math, os, random, shutil, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))      # khiska-el-quisco/
E = os.path.join(HERE, "edicion"); A = os.path.join(E, "assets")
os.makedirs(A, exist_ok=True)
for f in ["cactus-khiska-una-flor.webp", "cactus-khiska-tres-flores.webp", "flor-capullo.webp", "flor-parcial.webp", "flor-abierta.webp",
          "logo-el-quisco.webp", "hero-fondo-isla-negra.webp", "hero-fondo-el-batro.webp", "territorio-las-petras.webp",
          "hero-fondo-mirador-neptuno.webp", "hero-fondo-caleta.webp", "sendero-ilustrado.webp"]:
    shutil.copy2(os.path.join(ROOT, "assets", "img", f), A)
for f in ["app-03-rutas.png", "app-04-ficha.png", "app-07-mi.png"]:
    shutil.copy2(os.path.join(ROOT, "_proyecto", "produccion", "capturas", f), A)
os.makedirs(os.path.join(A, "fonts"), exist_ok=True)
for f in ["rubik-latin-400-normal", "rubik-latin-500-normal", "rubik-latin-700-normal", "rubik-mono-one-latin-400-normal"]:
    shutil.copy2(os.path.join(ROOT, "assets", "fonts", f + ".woff2"), os.path.join(A, "fonts"))

# Sendero: recorte por luminancia (sin rectángulo)
from PIL import Image
a = np.asarray(Image.open(os.path.join(A, "sendero-ilustrado.webp")).convert("RGB")).astype(np.float32) / 255
bg = np.median(np.concatenate([a[:25].reshape(-1, 3), a[-25:].reshape(-1, 3)]), axis=0)
al = np.clip((np.max(np.clip((bg - a) / np.maximum(bg, 1e-3), 0, 1), axis=2) - 0.06) / 0.5, 0, 1)
w = a.shape[1]; al *= np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / 120, 0, 1)[None, :]
alx = np.maximum(al, 1e-3)[..., None]
Image.fromarray((np.dstack([np.clip((a - (1 - alx) * bg) / alx, 0, 1), al]) * 255).astype(np.uint8), "RGBA").save(os.path.join(A, "sendero.png"))

# Paleta y estilo de V00
CREAM, GREEN, INK, PINK, POLLEN = "#F8F5EC", "#3F6B3A", "#1E2A1D", "#C9506B", "#EFB93F"
NL = "\n"

# ── Escenas: (duración, texto en pantalla/voz) ──
ESC = [(3.2, "¿Creías que El Quisco era solo verano?"), (2.8, "El Quisco no termina en la playa."),
       (2.0, "Humedal El Batro"), (2.0, "Quebrada Las Petras"), (2.0, "Mirador Neptuno"), (2.0, "La caleta"),
       (3.3, "Y desde hoy, una forma nueva de recorrerlo."), (2.2, "Khiska es tu cactus."), (2.4, "Una ruta. Una flor."),
       (1.6, "Elige un lugar"), (1.7, "Revisa su ficha"), (2.3, "Mira tu cactus en Mi Khiska"),
       (1.9, "Pincha tu curiosidad."), (4.9, "¿Qué parte de El Quisco quieres descubrir?")]
VOZ_DIR = "voz-sandra"     # voz oficial; «voz» = Paulina (versión anterior)
VOZ_OFF = [0.35, 0.2, 0.25, 0.25, 0.25, 0.25, 0.2, 0.2, 0.2, 0.15, 0.15, 0.15, 0.15, 0.3]
def _dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
ESC = [(round(max(d, _dur(os.path.join(HERE, VOZ_DIR, f"{k + 1:02d}.wav")) + VOZ_OFF[k] + (0.25 if k < 13 else 0.25)), 2), t) for k, (d, t) in enumerate(ESC)]
T = [0.0]
for d, _ in ESC:
    T.append(round(T[-1] + d, 3))
DUR = T[-1]

# Voz: cada frase en su escena
SR = 48000
voz = np.zeros(int(DUR * SR) + SR, np.float32)
subs = []
for k in range(len(ESC)):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", os.path.join(HERE, VOZ_DIR, f"{k + 1:02d}.wav"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32)
    i = int((T[k] + VOZ_OFF[k]) * SR)
    voz[i:i + len(x)] += x
    txt = ESC[k][1] if k < 13 else "¿Qué parte de El Quisco quieres descubrir? Explora en el link de la bio."
    subs.append({"text": txt, "start": round(T[k] + VOZ_OFF[k], 3), "end": round(min(T[k + 1], T[k] + VOZ_OFF[k] + len(x) / SR + 0.3), 3)})
voz = voz[:int(DUR * SR)]
voz.astype(np.float32).tofile(os.path.join(HERE, "_v.f32"))
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", os.path.join(HERE, "_v.f32"),
                "-ac", "2", "-c:a", "pcm_s24le", os.path.join(HERE, "audio48k.wav")], check=True)
os.remove(os.path.join(HERE, "_v.f32"))
json.dump({"duration": DUR, "fps": 30, "segments": [[0, DUR]], "words": []}, open(os.path.join(HERE, "words.json"), "w"))
json.dump(subs, open(os.path.join(HERE, "subtitulos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def wobbly(w, h, seed, step=34, amp=1.6, r=14):
    rnd = random.Random(seed); pts = []
    def edge(x0, y0, x1, y1):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
        for k in range(n):
            t = k / n
            pts.append((x0 + (x1 - x0) * t + rnd.uniform(-amp, amp), y0 + (y1 - y0) * t + rnd.uniform(-amp, amp)))
    m = 3
    edge(m + r, m, w - m - r, m); edge(w - m, m + r, w - m, h - m - r); edge(w - m - r, h - m, m + r, h - m); edge(m, h - m - r, m, m + r)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return f'<svg class="ink" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><path d="{d}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/></svg>'


PAPER = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 .45  0 0 0 0 .40  0 0 0 0 .30  0 0 0 .55 0'/></filter>"
         "<rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")

J = []
js = J.append
def vis(sel, a, b):
    js(f'tl.set("{sel}", {{ opacity: 1 }}, {a:.3f}); tl.set("{sel}", {{ opacity: 0 }}, {b:.3f});')

# 1 · gancho
vis("#e1", 0, T[1])
js('tl.fromTo("#e1-cactus", { opacity: 0, y: 40, scale: .94 }, { opacity: 1, y: 0, scale: 1, duration: 1.0, ease: "power2.out" }, 0.05);')
for k, t in enumerate([0.35, 0.55, 0.72, 0.85, 1.05, 1.22, 1.4]):
    js(f'tl.fromTo("#q{k}", {{ opacity: 0, y: 26 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }}, {t});')
js('tl.to("#qline", { attr: { "stroke-dashoffset": 0 }, duration: 0.8, ease: "power2.inOut" }, 1.9);')
js(f'tl.to("#e1", {{ opacity: 0, y: -80, duration: 0.5, ease: "power2.in" }}, {T[1] - 0.45:.3f});')

# 2-6 · postal de la costa que se abre por capas
CAPAS = [("hero-fondo-isla-negra", None), ("hero-fondo-el-batro", "Humedal El Batro"), ("territorio-las-petras", "Quebrada Las Petras"),
         ("hero-fondo-mirador-neptuno", "Mirador Neptuno"), ("hero-fondo-caleta", "La caleta")]
vis("#t2", T[1] + 0.05, T[2] + 0.1)
js(f'tl.fromTo("#t2 .card", {{ opacity: 0, y: -30, rotation: -3 }}, {{ opacity: 1, y: 0, rotation: -1.2, duration: 0.7, ease: "power3.out" }}, {T[1] + 0.05:.3f});')
js(f'tl.to("#t2 .card", {{ opacity: 0, y: -20, duration: 0.3, ease: "power2.in" }}, {T[2] - 0.2:.3f});')
for k, (img, name) in enumerate(CAPAS):
    a, b = T[1 + k], T[2 + k]
    rot = [-1.5, 1.6, -1.8, 1.4, -1.2][k]
    vis(f"#c{k}", a, T[6] + 0.9)
    js(f'tl.fromTo("#c{k} .post", {{ y: {1300 if k else 160}, rotation: {rot * 4}, opacity: {1 if k else 0} }}, {{ y: 0, rotation: {rot}, opacity: 1, duration: {0.75 if k else 0.8}, ease: "power3.out" }}, {a:.3f});')
    js(f'tl.fromTo("#c{k} .ph img", {{ scale: 1 }}, {{ scale: 1.06, duration: {b - a + 0.6:.3f}, ease: "none" }}, {a:.3f});')
    if name:
        js(f'tl.fromTo("#c{k} .tag", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {a + 0.3:.3f});')
        js(f'tl.to("#c{k} .tag", {{ opacity: 0, duration: 0.25 }}, {b - 0.1:.3f});')
    # cuando entra la siguiente capa, esta se corre hacia arriba y queda detrás (pila de papeles)
    if k < len(CAPAS) - 1:
        js(f'tl.to("#c{k} .post", {{ y: {-150 - 18 * (4 - k)}, scale: {0.86 - 0.02 * (4 - k):.2f}, rotation: {rot * 2.2}, duration: 0.7, ease: "power2.inOut" }}, {b:.3f});')
# 7 · las capas se apilan y suben; se dibuja el sendero
js(f'tl.to("#c4 .post", {{ y: -190, scale: .84, duration: 0.7, ease: "power2.inOut" }}, {T[6]:.3f});')
js(f'tl.to(["#c0", "#c1", "#c2", "#c3", "#c4"], {{ y: -260, opacity: 0, duration: 0.6, ease: "power2.in" }}, {T[6] + 0.4:.3f});')
vis("#e7", T[6], T[7] + 0.4)
js(f'tl.fromTo("#t7 .card", {{ opacity: 0, y: -30, rotation: 2 }}, {{ opacity: 1, y: 0, rotation: .8, duration: 0.7, ease: "power3.out" }}, {T[6] + 0.15:.3f});')
js(f'tl.fromTo("#sendero img", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 2.2, ease: "power2.inOut" }}, {T[6] + 0.5:.3f});')
js(f'tl.to("#e7", {{ opacity: 0, duration: 0.4 }}, {T[7]:.3f});')
# 8-9 · cactus Khiska y la flor
vis("#e8", T[7], T[9] + 0.3)
js(f'tl.fromTo("#tres", {{ clipPath: "inset(100% 0% 0% 0%)", y: 60 }}, {{ clipPath: "inset(0% 0% 0% 0%)", y: 0, duration: 1.3, ease: "power2.out" }}, {T[7]:.3f});')
js(f'tl.fromTo("#t8", {{ opacity: 0, y: -24 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {T[7] + 0.15:.3f});')
js(f'tl.to("#t8", {{ opacity: 0, y: -16, duration: 0.3 }}, {T[8] - 0.1:.3f});')
js(f'tl.to("#tres", {{ y: -230, scale: .7, duration: 0.8, ease: "power2.inOut" }}, {T[8]:.3f});')
js(f'tl.fromTo("#t9", {{ opacity: 0, y: -24 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {T[8] + 0.1:.3f});')
for k, d in enumerate((0.35, 0.95, 1.55)):
    js(f'tl.fromTo("#st{k}", {{ opacity: 0, y: 30, scale: .85 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, {T[8] + d:.3f});')
for k, d in enumerate((0.7, 1.3)):
    js(f'tl.fromTo("#ar{k}", {{ opacity: 0, x: -12 }}, {{ opacity: 1, x: 0, duration: 0.3 }}, {T[8] + d:.3f});')
js(f'tl.to("#e8", {{ opacity: 0, duration: 0.3 }}, {T[9] - 0.05:.3f});')
# 10-12 · destellos de la app en marco de celular
for k in range(3):
    a, b = T[9 + k], T[10 + k]
    vis(f"#d{k}", a, b)
    js(f'tl.fromTo("#d{k} .phone", {{ opacity: 0, scale: .92, y: 40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {a:.3f});')
    js(f'tl.fromTo("#d{k} .shot", {{ y: 0 }}, {{ y: -60, duration: {b - a:.3f}, ease: "none" }}, {a:.3f});')
    js(f'tl.fromTo("#d{k} .pill", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, {a + 0.05:.3f});')
    js(f'tl.fromTo("#flash", {{ opacity: .6 }}, {{ opacity: 0, duration: 0.2, immediateRender: false }}, {a:.3f});')
# 13 · Pincha tu curiosidad
vis("#e13", T[12], T[13])
js(f'tl.fromTo("#t13", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {T[12] + 0.05:.3f});')
for k, d in enumerate((0.25, 0.7, 1.15)):
    js(f'tl.fromTo("#p{k}", {{ opacity: .9, scale: .2 }}, {{ opacity: 0, scale: 2.6, duration: 1.0, ease: "power2.out" }}, {T[12] + d:.3f});')
js(f'tl.fromTo("#chispa", {{ opacity: 0, scale: .3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {T[12] + 0.25:.3f});')
# 14 · cierre estándar (igual que V00)
vis("#e14", T[13] - 0.05, DUR + 1)
js(f'tl.fromTo("#logo", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }}, {T[13]:.3f});')
js(f'tl.fromTo("#o-flor", {{ opacity: 0, scale: .6, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 1.0, ease: "back.out(1.4)" }}, {T[13] + 0.3:.3f});')
js(f'tl.fromTo("#o-t", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }}, {T[13] + 0.5:.3f});')
js(f'tl.fromTo("#btn", {{ opacity: 0, y: 30, scale: .9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "back.out(1.7)" }}, {T[13] + 1.4:.3f});')
js(f'tl.to("#btn-in", {{ scale: 1.05, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {T[13] + 2.2:.3f});')
# subtítulos
SUBH = []
for k, s in enumerate(subs):
    SUBH.append(f'<div id="s{k}" class="sub"><span>{s["text"]}</span></div>')
    js(f'tl.set("#s{k}", {{ opacity: 1 }}, {s["start"]:.3f}); tl.set("#s{k}", {{ opacity: 0 }}, {s["end"]:.3f});')

Q = "¿Creías que El Quisco era solo verano?".split()
QH = " ".join(f'<span id="q{k}">{w}</span>' for k, w in enumerate(Q))
def post(k, img):
    return (f'<div id="c{k}" class="layer vis"><div class="post"><div class="ph"><img src="assets/{img}.webp" alt="" /></div></div>'
            + (f'<div class="tag"><div class="card">{wobbly(620, 120, 10 + k)}<span>{CAPAS[k][1]}</span></div></div>' if CAPAS[k][1] else "") + '</div>')
def phone(k, shot, label):
    return f'<div id="d{k}" class="vis"><div class="pill">{label}</div><div class="phone"><div class="screen"><img class="shot" src="assets/{shot}" alt="" /></div></div></div>'

FONTS = "".join(f'@font-face {{ font-family: "{fam}"; src: url("assets/fonts/{f}.woff2") format("woff2"); font-weight: {w}; }}\n    '
                for fam, f, w in [("Rubik", "rubik-latin-400-normal", 400), ("Rubik", "rubik-latin-500-normal", 500),
                                  ("Rubik", "rubik-latin-700-normal", 700), ("Rubik Mono One", "rubik-mono-one-latin-400-normal", 400)])
page = f"""<!doctype html>
<html lang="es" data-resolution="portrait">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, height=1920" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Young+Serif&display=block" />
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    {FONTS}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {CREAM}; }}
    #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {CREAM}; font-family: "Rubik", sans-serif; color: {INK}; }}
    .paper {{ position: absolute; inset: 0; background-image: url("{PAPER}"); opacity: .22; mix-blend-mode: multiply; }}
    .vis {{ opacity: 0; }}
    .ink {{ position: absolute; inset: 0; overflow: visible; }}
    .card {{ position: relative; background: #FBF8F1; box-shadow: 0 16px 30px -18px rgba(30,42,29,.45); border-radius: 14px; }}
    .layer {{ position: absolute; left: 0; right: 0; top: 0; bottom: 0; }}
    #e1-cactus {{ position: absolute; left: 400px; top: 330px; width: 280px; }}
    #q {{ position: absolute; left: 90px; right: 90px; top: 860px; text-align: center; font-weight: 700; font-size: 92px; line-height: 1.08; }}
    #q span {{ display: inline-block; }}
    #qline {{ position: absolute; left: 270px; top: 1205px; width: 540px; height: 40px; overflow: visible; }}
    #t2 {{ position: absolute; left: 0; right: 0; top: 280px; display: flex; justify-content: center; }}
    #t2 .card, #t7 .card {{ width: 900px; padding: 34px 50px 40px; text-align: center; }}
    #t2 .card span, #t7 .card span {{ position: relative; font-weight: 700; font-size: 62px; line-height: 1.1; color: {GREEN}; }}
    .post {{ position: absolute; left: 70px; top: 620px; width: 940px; padding: 18px; background: #FFFDF6; border: 3px solid {INK}; border-radius: 18px;
             box-shadow: 0 30px 60px -28px rgba(30,42,29,.55); transform-origin: 50% 40%; }}
    .ph {{ width: 898px; height: 520px; overflow: hidden; border-radius: 10px; }}
    .ph img {{ width: 100%; height: 100%; object-fit: cover; display: block; transform-origin: 50% 50%; }}
    .tag {{ position: absolute; left: 0; right: 0; top: 1230px; display: flex; justify-content: center; }}
    .tag .card {{ width: 620px; height: 120px; display: flex; align-items: center; justify-content: center; transform: rotate(-1deg); }}
    .tag span {{ position: relative; font-weight: 700; font-size: 58px; color: {GREEN}; }}
    #t7 {{ position: absolute; left: 0; right: 0; top: 330px; display: flex; justify-content: center; }}
    #sendero {{ position: absolute; left: 0; right: 0; top: 820px; height: 420px; }}
    #sendero img {{ width: 1080px; height: 210px; margin-top: 100px; transform: scale(1.6); transform-origin: 50% 50%; }}
    #tres {{ position: absolute; left: 150px; top: 560px; width: 780px; transform-origin: 50% 100%; }}
    #t8, #t9 {{ position: absolute; left: 60px; right: 60px; top: 300px; text-align: center; }}
    #t8 {{ font-weight: 700; font-size: 86px; }}
    #t9 {{ font-family: "Rubik Mono One"; font-size: 70px; line-height: 1.12; }}
    #states {{ position: absolute; left: 60px; right: 60px; top: 1060px; display: flex; justify-content: space-between; align-items: flex-start; }}
    .st {{ width: 290px; text-align: center; }}
    .st img {{ width: 250px; height: 220px; object-fit: contain; display: block; margin: 0 auto; }}
    .st p {{ font-weight: 500; font-size: 34px; margin-top: 8px; }}
    .arrow {{ font-size: 56px; color: {PINK}; margin-top: 80px; font-weight: 500; }}
    .pill {{ position: absolute; left: 0; right: 0; top: 190px; margin: 0 auto; width: max-content; background: {GREEN}; color: {CREAM}; font-weight: 500;
             font-size: 46px; padding: 22px 46px 24px; border-radius: 999px; box-shadow: 0 18px 36px -18px rgba(30,42,29,.6); z-index: 2; }}
    .phone {{ position: absolute; left: 280px; top: 320px; width: 520px; height: 1110px; border-radius: 64px; background: {INK}; padding: 14px;
              box-shadow: 0 40px 80px -30px rgba(30,42,29,.6); }}
    .screen {{ width: 100%; height: 100%; border-radius: 52px; overflow: hidden; background: #fff; }}
    .shot {{ width: 100%; display: block; }}
    #flash {{ position: absolute; inset: 0; background: #FFFDF6; opacity: 0; }}
    #t13 {{ position: absolute; left: 60px; right: 60px; top: 760px; text-align: center; font-family: "Rubik Mono One"; font-size: 84px; line-height: 1.12; }}
    .pulso {{ position: absolute; left: 540px; top: 1160px; width: 140px; height: 140px; margin: -70px 0 0 -70px; border-radius: 50%; border: 6px solid {POLLEN}; }}
    #chispa {{ position: absolute; left: 540px; top: 1160px; width: 40px; height: 40px; margin: -20px 0 0 -20px; border-radius: 50%; background: {POLLEN}; box-shadow: 0 0 34px 12px rgba(239,185,63,.55); }}
    #e14 {{ position: absolute; inset: 0; }}
    #logo {{ position: absolute; left: 160px; top: 300px; width: 760px; }}
    #o-flor {{ position: absolute; left: 380px; top: 660px; width: 320px; }}
    #o-t {{ position: absolute; left: 90px; right: 90px; top: 1000px; text-align: center; font-family: "Young Serif", serif; font-size: 80px; line-height: 1.12; }}
    #btn {{ position: absolute; left: 0; right: 0; top: 1330px; display: flex; justify-content: center; }}
    #btn div {{ font-family: "Rubik Mono One", sans-serif; font-size: 38px; color: {CREAM}; background: {PINK}; padding: 30px 46px 32px; border-radius: 999px;
                box-shadow: 0 20px 40px -18px rgba(201,80,107,.7); }}
    .sub {{ position: absolute; left: 70px; right: 70px; top: 1500px; display: flex; justify-content: center; opacity: 0; text-align: center; }}
    .sub span {{ font-weight: 500; font-size: 40px; line-height: 1.25; background: rgba(255,253,246,.92); padding: 8px 22px 11px; border-radius: 12px; }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
    <div class="paper"></div>
    <div id="e1" class="vis">
      <img id="e1-cactus" src="assets/cactus-khiska-una-flor.webp" alt="" />
      <div id="q">{QH}</div>
      <svg id="qline" viewBox="0 0 540 40"><path id="qline" d="M6,24 C120,10 240,34 360,18 C430,10 490,22 534,16" fill="none" stroke="{POLLEN}" stroke-width="9" stroke-linecap="round" stroke-dasharray="560" stroke-dashoffset="560"/></svg>
    </div>
    <div id="t2" class="vis"><div class="card">{wobbly(900, 200, 1)}<span>El Quisco no termina<br>en la playa.</span></div></div>
    {NL.join(post(k, img) for k, (img, _) in enumerate(CAPAS))}
    <div id="e7" class="vis"><div id="t7"><div class="card">{wobbly(900, 220, 7)}<span>Y desde hoy, una forma nueva de recorrerlo.</span></div></div>
      <div id="sendero"><img src="assets/sendero.png" alt="" /></div></div>
    <div id="e8" class="vis">
      <img id="tres" src="assets/cactus-khiska-tres-flores.webp" alt="" />
      <div id="t8">Khiska es tu cactus.</div>
      <div id="t9">Una ruta.<br>Una flor.</div>
      <div id="states">
        <div id="st0" class="st vis"><img src="assets/flor-capullo.webp" alt="" /><p>Capullo</p></div>
        <div id="ar0" class="arrow vis">→</div>
        <div id="st1" class="st vis"><img src="assets/flor-parcial.webp" alt="" /><p>Apertura parcial</p></div>
        <div id="ar1" class="arrow vis">→</div>
        <div id="st2" class="st vis"><img src="assets/flor-abierta.webp" alt="" /><p>Flor abierta</p></div>
      </div>
    </div>
    {phone(0, "app-03-rutas.png", "1. Elige un lugar")}
    {phone(1, "app-04-ficha.png", "2. Revisa su ficha")}
    {phone(2, "app-07-mi.png", "3. Mira tu cactus en Mi Khiska")}
    <div id="flash"></div>
    <div id="e13" class="vis"><div id="t13">Pincha tu<br>curiosidad.</div><div id="p0" class="pulso"></div><div id="p1" class="pulso"></div><div id="p2" class="pulso"></div><div id="chispa"></div></div>
    <div id="e14" class="vis">
      <img id="logo" src="assets/logo-el-quisco.webp" alt="El Quisco" />
      <img id="o-flor" src="assets/flor-abierta.webp" alt="" />
      <div id="o-t">¿Qué parte de El Quisco quieres descubrir?</div>
      <div id="btn"><div id="btn-in">EXPLORA EN EL LINK DE LA BIO</div></div>
    </div>
    {NL.join(SUBH)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.set("#t8, #t9", {{ opacity: 0 }}, 0);
    {(NL + "    ").join(J)}
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
"""
open(os.path.join(E, "index.html"), "w", encoding="utf-8", newline="\n").write(page)
print(f"ok · {DUR} s · escenas {T}")
