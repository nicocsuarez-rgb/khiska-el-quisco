"""V12 · Una ruta completada hace florecer tu Khiska · 1080×1920 · ~20 s · voz Sandra. Uso: python build_v12.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from comun_khiska import *

preparar(HERE, ["cactus-khiska-una-flor.webp", "flor-capullo.webp", "flor-parcial.webp"], ["app-07-mi.png"])
TXT = ["Una ruta completada…", "…hace florecer tu Khiska.", "La flor no es un premio:", "es la memoria de lo que viviste.", "Guárdala en Mi Khiska.", CIERRE]
OFF = [0.3, 0.15, 0.2, 0.15, 0.2, 0.3]
T = tiempos(HERE, [2.4, 3.8, 2.4, 3.2, 3.2, 4.8], OFF, pad=0.25)
D = T[-1]
subs = voz_y_subs(HERE, T, OFF, TXT)
J = []; js = J.append

# 1-2 · el cactus está desde el inicio; la flor se abre lentamente
js(f'tl.set("#e1", {{ opacity: 1 }}, 0); tl.to("#e1", {{ opacity: 0, duration: 0.4 }}, {T[2] - 0.35:.3f});')
js('tl.fromTo("#c1", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.9, ease: "power2.out" }, 0);')
js('tl.fromTo("#t1", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.25);')
js(f'tl.to("#t1", {{ opacity: 0, y: -14, duration: 0.3 }}, {T[1] - 0.15:.3f});')
js(f'tl.fromTo("#t2", {{ opacity: 0, y: 20, scale: .95 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {T[1] + 0.1:.3f});')
a = T[1]
js(f'tl.set("#cap", {{ opacity: 1 }}, 0); tl.to("#cap", {{ opacity: 0, scale: 1.12, duration: 0.9, ease: "sine.inOut" }}, {a + 0.2:.3f});')
js(f'tl.fromTo("#par", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.9, ease: "sine.inOut" }}, {a + 0.2:.3f}); tl.to("#par", {{ opacity: 0, scale: 1.12, duration: 0.9, ease: "sine.inOut" }}, {a + 1.3:.3f});')
js(f'tl.fromTo("#glow1", {{ opacity: 0, scale: .6 }}, {{ opacity: 1, scale: 1.1, duration: 1.0 }}, {a + 1.3:.3f});')
# 3-4 · la flor grande: «La flor no es un premio: / es la memoria de lo que viviste.»
js(f'tl.set("#e3", {{ opacity: 1 }}, {T[2] - 0.35:.3f}); tl.set("#e3", {{ opacity: 0 }}, {T[4]:.3f});')
js(f'tl.fromTo("#flor", {{ opacity: 0, scale: .7 }}, {{ opacity: 1, scale: 1, duration: 0.8, ease: "power3.out" }}, {T[2] - 0.3:.3f});')
js(f'tl.fromTo("#flor", {{ rotation: 0 }}, {{ rotation: 8, duration: {T[4] - T[2] + 0.3:.3f}, ease: "none", immediateRender: false }}, {T[2] - 0.3:.3f});')
js(f'tl.fromTo("#glow3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.8 }}, {T[2] - 0.3:.3f});')
js(f'tl.fromTo("#t3 .card", {{ opacity: 0, y: -24, rotation: -3 }}, {{ opacity: 1, y: 0, rotation: -1, duration: 0.6, ease: "power3.out" }}, {T[2]:.3f});')
js(f'tl.fromTo("#t4", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {T[3]:.3f});')
js(f'tl.to("#e3", {{ opacity: 0, duration: 0.3 }}, {T[4] - 0.3:.3f});')
# 5 · Mi Khiska en la app
a, b = T[4], T[5]
js(f'tl.set("#d5", {{ opacity: 1 }}, {a:.3f}); tl.set("#d5", {{ opacity: 0 }}, {b:.3f});')
js(f'tl.fromTo("#d5 .phone", {{ opacity: 0, scale: .92, y: 40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {a:.3f});')
js(f'tl.fromTo("#d5 .shot", {{ y: 0 }}, {{ y: -80, duration: {b - a:.3f}, ease: "sine.inOut" }}, {a + 0.3:.3f});')
js(f'tl.fromTo("#d5 .pill", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {a + 0.05:.3f});')
js(f'tl.fromTo("#flash", {{ opacity: .6 }}, {{ opacity: 0, duration: 0.2, immediateRender: false }}, {a:.3f});')
J += cierre_js(T[5], D)
SH, SJ = subs_html_js(subs); J += SJ

css = f"""
    #c1 {{ position: absolute; left: 280px; top: 560px; width: 520px; height: 829px; }}
    #c1 img.base {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    #cap, #par {{ position: absolute; left: 24px; top: 336px; width: 206px; transform-origin: 50% 50%; }}
    #par {{ top: 372px; }}
    #glow1 {{ left: 170px; top: 760px; width: 480px; height: 480px; }}
    #t1, #t2 {{ position: absolute; left: 60px; right: 60px; top: 260px; text-align: center; }}
    #t1 {{ font-weight: 700; font-size: 84px; }}
    #t2 {{ font-family: "Rubik Mono One"; font-size: 62px; line-height: 1.15; color: {GREEN}; }}
    #flor {{ position: absolute; left: 240px; top: 600px; width: 600px; transform-origin: 50% 50%; }}
    #glow3 {{ left: 140px; top: 470px; width: 800px; height: 800px; }}
    #t3 {{ position: absolute; left: 0; right: 0; top: 250px; display: flex; justify-content: center; }}
    #t3 .card {{ width: 880px; height: 170px; display: flex; align-items: center; justify-content: center; }}
    #t3 .card span {{ position: relative; font-weight: 700; font-size: 68px; color: {INK}; }}
    #t4 {{ position: absolute; left: 70px; right: 70px; top: 1210px; text-align: center; font-weight: 700; font-size: 66px; line-height: 1.12; color: {GREEN}; }}
"""
body = f"""<div id="e1" class="vis"><div id="glow1" class="glow"></div>
      <div id="c1"><img class="base" src="assets/cactus-khiska-una-flor.webp" alt="" /><img id="cap" src="assets/flor-capullo.webp" alt="" style="opacity:0" /><img id="par" src="assets/flor-parcial.webp" alt="" style="opacity:0" /></div>
      <div id="t1">Una ruta completada…</div><div id="t2" style="opacity:0">…hace florecer<br>tu Khiska.</div></div>
    <div id="e3" class="vis"><div id="glow3" class="glow"></div><img id="flor" src="assets/flor-abierta.webp" alt="" />
      <div id="t3"><div class="card">{wobbly(880, 170, 12)}<span>La flor no es un premio:</span></div></div>
      <div id="t4" style="opacity:0">es la memoria de lo<br>que viviste.</div></div>
    <div id="d5" class="vis"><div class="pill"><b>Guárdala en Mi Khiska</b></div><div class="phone"><div class="screen"><img class="shot" src="assets/app-07-mi.png" alt="" /></div></div></div>
    <div id="flash"></div>
    {CIERRE_HTML}
    {NL.join(SH)}"""
pagina(HERE, D, css, body, J)
print(f"ok · {D} s · escenas {T}")
