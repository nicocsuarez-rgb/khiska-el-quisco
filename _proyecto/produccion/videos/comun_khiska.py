"""Base común para V07 y V12 (estilo V00/V01): assets, voz por frase, subtítulos, cierre estándar y página HyperFrames."""
import json, math, os, random, shutil, subprocess
import numpy as np
from PIL import Image

VIDEOS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(VIDEOS, "..", "..", ".."))
CREAM, GREEN, INK, PINK, POLLEN = "#F8F5EC", "#3F6B3A", "#1E2A1D", "#C9506B", "#EFB93F"
SR = 48000
NL = "\n"
CIERRE = "¿Qué parte de El Quisco quieres descubrir? Explora en el link de la bio."


def preparar(here, imgs, capturas=()):
    a = os.path.join(here, "edicion", "assets"); os.makedirs(os.path.join(a, "fonts"), exist_ok=True)
    for f in set(imgs) | {"logo-el-quisco.webp", "flor-abierta.webp"}:
        shutil.copy2(os.path.join(ROOT, "assets", "img", f), a)
    for f in capturas:
        shutil.copy2(os.path.join(ROOT, "_proyecto", "produccion", "capturas", f), a)
    for f in ["rubik-latin-400-normal", "rubik-latin-500-normal", "rubik-latin-700-normal", "rubik-mono-one-latin-400-normal"]:
        shutil.copy2(os.path.join(ROOT, "assets", "fonts", f + ".woff2"), os.path.join(a, "fonts"))
    if "sendero-ilustrado.webp" in imgs:
        x = np.asarray(Image.open(os.path.join(a, "sendero-ilustrado.webp")).convert("RGB")).astype(np.float32) / 255
        bg = np.median(np.concatenate([x[:25].reshape(-1, 3), x[-25:].reshape(-1, 3)]), axis=0)
        al = np.clip((np.max(np.clip((bg - x) / np.maximum(bg, 1e-3), 0, 1), axis=2) - 0.06) / 0.5, 0, 1)
        w = x.shape[1]; al *= np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / 120, 0, 1)[None, :]
        alx = np.maximum(al, 1e-3)[..., None]
        Image.fromarray((np.dstack([np.clip((x - (1 - alx) * bg) / alx, 0, 1), al]) * 255).astype(np.uint8), "RGBA").save(os.path.join(a, "sendero.png"))
    return a


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)


def tiempos(here, minimos, off, pad=0.3, pad_final=0.3):
    """Duración de cada escena = máx(mínimo, voz + margen)."""
    n = len(minimos); T = [0.0]
    for k in range(n):
        v = dur(os.path.join(here, "voz-sandra", f"{k + 1:02d}.wav"))
        T.append(round(T[-1] + max(minimos[k], v + off[k] + (pad if k < n - 1 else pad_final)), 2))
    return T


def voz_y_subs(here, T, off, textos):
    D = T[-1]; voz = np.zeros(int(D * SR) + SR, np.float32); subs = []
    for k, txt in enumerate(textos):
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", os.path.join(here, "voz-sandra", f"{k + 1:02d}.wav"), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32); i = int((T[k] + off[k]) * SR); voz[i:i + len(x)] += x
        subs.append({"text": txt, "start": round(T[k] + off[k], 3), "end": round(min(T[k + 1], T[k] + off[k] + len(x) / SR + 0.3), 3)})
    voz[:int(D * SR)].astype(np.float32).tofile(os.path.join(here, "_v.f32"))
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", os.path.join(here, "_v.f32"), "-ac", "2", "-c:a", "pcm_s24le",
                    os.path.join(here, "audio48k.wav")], check=True)
    os.remove(os.path.join(here, "_v.f32"))
    json.dump({"duration": D, "fps": 30, "segments": [[0, D]], "words": []}, open(os.path.join(here, "words.json"), "w"))
    json.dump(subs, open(os.path.join(here, "subtitulos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return subs


def wobbly(w, h, seed, step=34, amp=1.6, r=14):
    rnd = random.Random(seed); pts = []
    def edge(x0, y0, x1, y1):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
        for k in range(n):
            t = k / n; pts.append((x0 + (x1 - x0) * t + rnd.uniform(-amp, amp), y0 + (y1 - y0) * t + rnd.uniform(-amp, amp)))
    m = 3
    edge(m + r, m, w - m - r, m); edge(w - m, m + r, w - m, h - m - r); edge(w - m - r, h - m, m + r, h - m); edge(m, h - m - r, m, m + r)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return f'<svg class="ink" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><path d="{d}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/></svg>'


PAPER = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 .45  0 0 0 0 .40  0 0 0 0 .30  0 0 0 .55 0'/></filter>"
         "<rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")

CSS_BASE = f"""
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: {CREAM}; }}
    #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {CREAM}; font-family: "Rubik", sans-serif; color: {INK}; }}
    .paper {{ position: absolute; inset: 0; background-image: url("{PAPER}"); opacity: .22; mix-blend-mode: multiply; }}
    .vis {{ opacity: 0; }}
    .ink {{ position: absolute; inset: 0; overflow: visible; }}
    .card {{ position: relative; background: #FBF8F1; box-shadow: 0 16px 30px -18px rgba(30,42,29,.45); border-radius: 14px; }}
    .pill {{ position: absolute; left: 0; right: 0; top: 150px; margin: 0 auto; width: max-content; max-width: 960px; background: {GREEN}; color: {CREAM};
             padding: 20px 46px 24px; border-radius: 40px; box-shadow: 0 18px 36px -18px rgba(30,42,29,.6); text-align: center; z-index: 2; }}
    .pill b {{ display: block; font-weight: 700; font-size: 52px; line-height: 1.1; }}
    .pill span {{ display: block; font-weight: 400; font-size: 36px; margin-top: 4px; }}
    .phone {{ position: absolute; left: 280px; top: 360px; width: 520px; height: 1110px; border-radius: 64px; background: {INK}; padding: 14px;
              box-shadow: 0 40px 80px -30px rgba(30,42,29,.6); }}
    .screen {{ width: 100%; height: 100%; border-radius: 52px; overflow: hidden; background: #fff; }}
    .shot {{ width: 100%; display: block; }}
    #flash {{ position: absolute; inset: 0; background: #FFFDF6; opacity: 0; }}
    .glow {{ position: absolute; border-radius: 50%; background: radial-gradient(circle, rgba(239,185,63,.55) 0%, rgba(239,185,63,.16) 45%, transparent 70%); opacity: 0; }}
    #cierre {{ position: absolute; inset: 0; }}
    #logo {{ position: absolute; left: 160px; top: 300px; width: 760px; }}
    #o-flor {{ position: absolute; left: 380px; top: 660px; width: 320px; }}
    #o-t {{ position: absolute; left: 90px; right: 90px; top: 1000px; text-align: center; font-family: "Young Serif", serif; font-size: 80px; line-height: 1.12; }}
    #btn {{ position: absolute; left: 0; right: 0; top: 1330px; display: flex; justify-content: center; }}
    #btn div {{ font-family: "Rubik Mono One", sans-serif; font-size: 38px; color: {CREAM}; background: {PINK}; padding: 30px 46px 32px; border-radius: 999px;
                box-shadow: 0 20px 40px -18px rgba(201,80,107,.7); }}
    .sub {{ position: absolute; left: 70px; right: 70px; top: 1540px; display: flex; justify-content: center; opacity: 0; text-align: center; }}
    .sub span {{ font-weight: 500; font-size: 40px; line-height: 1.25; background: rgba(255,253,246,.92); padding: 8px 22px 11px; border-radius: 12px; }}
"""
CIERRE_HTML = """<div id="cierre" class="vis">
      <img id="logo" src="assets/logo-el-quisco.webp" alt="El Quisco" />
      <img id="o-flor" src="assets/flor-abierta.webp" alt="" />
      <div id="o-t">¿Qué parte de El Quisco quieres descubrir?</div>
      <div id="btn"><div id="btn-in">EXPLORA EN EL LINK DE LA BIO</div></div>
    </div>"""


def cierre_js(t0, D):
    return [f'tl.set("#cierre", {{ opacity: 1 }}, {t0 - 0.05:.3f});',
            f'tl.fromTo("#logo", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }}, {t0:.3f});',
            f'tl.fromTo("#o-flor", {{ opacity: 0, scale: .6, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 1.0, ease: "back.out(1.4)" }}, {t0 + 0.3:.3f});',
            f'tl.fromTo("#o-t", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }}, {t0 + 0.5:.3f});',
            f'tl.fromTo("#btn", {{ opacity: 0, y: 30, scale: .9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "back.out(1.7)" }}, {t0 + 1.4:.3f});',
            f'tl.to("#btn-in", {{ scale: 1.05, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {t0 + 2.2:.3f});']


def subs_html_js(subs):
    h, j = [], []
    for k, s in enumerate(subs):
        h.append(f'<div id="s{k}" class="sub"><span>{s["text"]}</span></div>')
        j.append(f'tl.set("#s{k}", {{ opacity: 1 }}, {s["start"]:.3f}); tl.set("#s{k}", {{ opacity: 0 }}, {s["end"]:.3f});')
    return h, j


def pagina(here, D, css, body, js):
    fonts = "".join(f'@font-face {{ font-family: "{fam}"; src: url("assets/fonts/{f}.woff2") format("woff2"); font-weight: {w}; }}\n    '
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
    {fonts}{CSS_BASE}{css}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
    <div class="paper"></div>
    {body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {(NL + "    ").join(js)}
    window.__timelines["main"] = tl;
  </script>
</body>
</html>
"""
    open(os.path.join(here, "edicion", "index.html"), "w", encoding="utf-8", newline="\n").write(page)
