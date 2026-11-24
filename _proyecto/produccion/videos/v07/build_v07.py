"""V07 · Elige, prepara y comienza · 1080×1920 · estilo V00/V01 · voz Sandra. Uso: python build_v07.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from comun_khiska import *

preparar(HERE, ["cactus-khiska-una-flor.webp", "flor-capullo.webp", "flor-parcial.webp", "sendero-ilustrado.webp"], ["app-03-rutas.png", "app-04-ficha.png"])
TXT = ["Elige, prepara y comienza.", "Así funciona Khiska, en tres pasos.", "Uno. Elige el lugar que te da curiosidad.",
       "Dos. Prepara: revisa su ficha, también imprimible.", "Tres. Comienza: tu flor empieza a abrirse.",
       "Una ruta completa, una flor. Haz florecer tu Khiska.", CIERRE]
OFF = [0.3, 0.2, 0.25, 0.25, 0.25, 0.3, 0.3]
T = tiempos(HERE, [3.0, 2.6, 3.8, 4.2, 4.0, 4.2, 4.8], OFF)
D = T[-1]
subs = voz_y_subs(HERE, T, OFF, TXT)
J = []; js = J.append
def vis(sel, a, b): js(f'tl.set("{sel}", {{ opacity: 1 }}, {a:.3f}); tl.set("{sel}", {{ opacity: 0 }}, {b:.3f});')

# 1-2 · gancho y «así funciona»
vis("#e1", 0, T[2])
js('tl.fromTo("#c-mini", { opacity: 0, y: 40, scale: .94 }, { opacity: 1, y: 0, scale: 1, duration: 1.0, ease: "power2.out" }, 0.05);')
for k, t in enumerate([0.3, 0.55, 0.75, 0.95]):
    js(f'tl.fromTo("#g{k}", {{ opacity: 0, y: 26 }}, {{ opacity: 1, y: 0, duration: 0.55, ease: "power3.out" }}, {t});')
js('tl.to("#gline", { attr: { "stroke-dashoffset": 0 }, duration: 0.8, ease: "power2.inOut" }, 1.5);')
js(f'tl.to(["#gancho", "#gline"], {{ opacity: 0, y: -40, duration: 0.4, ease: "power2.in" }}, {T[1] - 0.35:.3f});')
js(f'tl.to("#c-mini", {{ y: -120, scale: .8, duration: 0.7, ease: "power2.inOut" }}, {T[1]:.3f});')
js(f'tl.fromTo("#asi .card", {{ opacity: 0, y: 30, rotation: 3 }}, {{ opacity: 1, y: 0, rotation: 1, duration: 0.7, ease: "power3.out" }}, {T[1] + 0.1:.3f});')
js(f'tl.to("#e1", {{ opacity: 0, duration: 0.3 }}, {T[2] - 0.3:.3f});')
# 3-4 · pasos con la app
for k, (i, shot) in enumerate([(2, "d0"), (3, "d1")]):
    a, b = T[i], T[i + 1]
    vis(f"#{shot}", a, b)
    js(f'tl.fromTo("#{shot} .phone", {{ opacity: 0, scale: .92, y: 40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {a:.3f});')
    js(f'tl.fromTo("#{shot} .shot", {{ y: 0 }}, {{ y: {-180 if k == 0 else -140}, duration: {b - a:.3f}, ease: "sine.inOut" }}, {a + 0.3:.3f});')
    js(f'tl.fromTo("#{shot} .pill", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {a + 0.05:.3f});')
    js(f'tl.fromTo("#flash", {{ opacity: .6 }}, {{ opacity: 0, duration: 0.2, immediateRender: false }}, {a:.3f});')
# 5 · comienza: sendero + capullo → parcial
a, b = T[4], T[5]
vis("#e5", a, b)
js(f'tl.fromTo("#e5 .pill", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {a + 0.05:.3f});')
js(f'tl.fromTo("#sendero img", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 2.0, ease: "power2.inOut" }}, {a + 0.2:.3f});')
js(f'tl.fromTo("#f5a", {{ opacity: 0, scale: .7 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {a + 0.4:.3f});')
t_ab = a + 0.25 + 2.0
js(f'tl.to("#f5a", {{ opacity: 0, scale: 1.08, duration: 0.6 }}, {t_ab:.3f});')
js(f'tl.fromTo("#f5b", {{ opacity: 0, scale: .9 }}, {{ opacity: 1, scale: 1, duration: 0.7, ease: "back.out(1.5)" }}, {t_ab:.3f});')
js(f'tl.fromTo("#glow5", {{ opacity: 0, scale: .7 }}, {{ opacity: 1, scale: 1.1, duration: 0.6 }}, {t_ab:.3f});')
# 6 · cactus con la flor que se abre + «Haz florecer tu Khiska»
a, b = T[5], T[6]
vis("#e6", a, b)
js(f'tl.fromTo("#c6", {{ clipPath: "inset(100% 0% 0% 0%)", y: 50 }}, {{ clipPath: "inset(0% 0% 0% 0%)", y: 0, duration: 1.1, ease: "power2.out" }}, {a:.3f});')
js(f'tl.fromTo("#t6a", {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {a + 0.2:.3f});')
js(f'tl.set("#cap6", {{ opacity: 1 }}, {a:.3f}); tl.to("#cap6", {{ opacity: 0, scale: 1.15, duration: 0.5 }}, {a + 1.4:.3f});')
js(f'tl.fromTo("#par6", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {a + 1.4:.3f}); tl.to("#par6", {{ opacity: 0, scale: 1.15, duration: 0.5 }}, {a + 2.1:.3f});')
js(f'tl.fromTo("#glow6", {{ opacity: 0, scale: .6 }}, {{ opacity: 1, scale: 1.15, duration: 0.6 }}, {a + 2.1:.3f}); tl.to("#glow6", {{ opacity: .4, scale: 1, duration: 0.8 }}, {a + 2.7:.3f});')
t_haz = subs[5]["start"] + 1.75
js(f'tl.fromTo("#t6b", {{ opacity: 0, y: 20, scale: .95 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {t_haz:.3f});')
# 7 · cierre
J += cierre_js(T[6], D)
SH, SJ = subs_html_js(subs); J += SJ

G = "Elige, prepara y comienza.".split()
css = f"""
    #c-mini {{ position: absolute; left: 400px; top: 330px; width: 280px; transform-origin: 50% 100%; }}
    #gancho {{ position: absolute; left: 80px; right: 80px; top: 860px; text-align: center; font-weight: 700; font-size: 96px; line-height: 1.08; }}
    #gancho span {{ display: inline-block; }}
    #gline {{ position: absolute; left: 270px; top: 1100px; width: 540px; height: 40px; overflow: visible; }}
    #asi {{ position: absolute; left: 0; right: 0; top: 880px; display: flex; justify-content: center; }}
    #asi .card {{ width: 900px; height: 210px; display: flex; align-items: center; justify-content: center; text-align: center; }}
    #asi .card span {{ position: relative; font-weight: 700; font-size: 62px; line-height: 1.1; color: {GREEN}; }}
    #sendero {{ position: absolute; left: 0; right: 0; top: 960px; height: 420px; }}
    #sendero img {{ width: 1080px; height: 210px; margin-top: 100px; transform: scale(1.6); transform-origin: 50% 50%; }}
    #f5a {{ position: absolute; left: 380px; top: 480px; width: 320px; }}
    #f5b {{ position: absolute; left: 350px; top: 560px; width: 380px; }}
    #glow5 {{ left: 240px; top: 380px; width: 600px; height: 600px; }}
    #c6 {{ position: absolute; left: 310px; top: 520px; width: 460px; height: 733px; }}
    #c6 img.base {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    #cap6, #par6 {{ position: absolute; left: 22px; top: 300px; width: 180px; transform-origin: 50% 50%; }}
    #par6 {{ top: 330px; }}
    #glow6 {{ left: 180px; top: 700px; width: 460px; height: 460px; }}
    #t6a {{ position: absolute; left: 60px; right: 60px; top: 230px; text-align: center; font-weight: 700; font-size: 74px; line-height: 1.1; }}
    #t6b {{ position: absolute; left: 60px; right: 60px; top: 1290px; text-align: center; font-family: "Rubik Mono One"; font-size: 54px; line-height: 1.15; color: {GREEN}; }}
"""
body = f"""<div id="e1" class="vis">
      <img id="c-mini" src="assets/cactus-khiska-una-flor.webp" alt="" />
      <div id="gancho">{" ".join(f'<span id="g{k}">{w}</span>' for k, w in enumerate(G))}</div>
      <svg id="gline" viewBox="0 0 540 40"><path id="gline" d="M6,24 C120,10 240,34 360,18 C430,10 490,22 534,16" fill="none" stroke="{POLLEN}" stroke-width="9" stroke-linecap="round" stroke-dasharray="560" stroke-dashoffset="560"/></svg>
      <div id="asi"><div class="card vis" style="opacity:0">{wobbly(900, 210, 3)}<span>Así funciona Khiska,<br>en tres pasos.</span></div></div>
    </div>
    <div id="d0" class="vis"><div class="pill"><b>1. Elige</b><span>El lugar que te da curiosidad</span></div><div class="phone"><div class="screen"><img class="shot" src="assets/app-03-rutas.png" alt="" /></div></div></div>
    <div id="d1" class="vis"><div class="pill"><b>2. Prepara</b><span>Revisa su ficha, también imprimible</span></div><div class="phone"><div class="screen"><img class="shot" src="assets/app-04-ficha.png" alt="" /></div></div></div>
    <div id="e5" class="vis"><div class="pill"><b>3. Comienza</b><span>Tu flor empieza a abrirse</span></div>
      <div id="glow5" class="glow"></div><img id="f5a" src="assets/flor-capullo.webp" alt="" /><img id="f5b" class="vis" src="assets/flor-parcial.webp" alt="" />
      <div id="sendero"><img src="assets/sendero.png" alt="" /></div></div>
    <div id="e6" class="vis"><div id="glow6" class="glow"></div>
      <div id="c6"><img class="base" src="assets/cactus-khiska-una-flor.webp" alt="" /><img id="cap6" class="vis" src="assets/flor-capullo.webp" alt="" /><img id="par6" src="assets/flor-parcial.webp" alt="" style="opacity:0" /></div>
      <div id="t6a">Una ruta completa,<br>una flor.</div><div id="t6b" style="opacity:0">Haz florecer<br>tu Khiska.</div></div>
    <div id="flash"></div>
    {CIERRE_HTML}
    {NL.join(SH)}"""
J.insert(0, 'tl.set("#asi .card", { opacity: 0 }, 0);')
pagina(HERE, D, css, body, J)
print(f"ok · {D} s · escenas {T}")
