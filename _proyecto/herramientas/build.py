# Genera las páginas del portal (modo presentación). Ejecutar desde la raíz del repo:
#   python3 _proyecto/herramientas/build.py
# Edita los textos aquí y vuelve a ejecutar. Los videos se editan en js/videos.js.
import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
SITE = 'El Quisco · Experiencia Khiska'

DIM = {
    'acantilados': ('Acantilados y mar profundo', 'icono-rocas'),
    'humedal': ('Humedal y bosque nativo', 'icono-hoja'),
    'memoria': ('Memoria y sabores', 'icono-flor'),
}

T = [
    dict(slug='el-batro', nombre='Humedal El Batro', dim='humedal', img='territorio-el-batro',
         alt='Ilustración en acuarela de un humedal costero con juncos y agua quieta, inspirada en El Batro',
         breve='Un humedal urbano protegido, a pasos de la costa.',
         que=['El Humedal Urbano El Batro fue reconocido por el Ministerio del Medio Ambiente el 29 de septiembre de 2025, a solicitud de la Municipalidad de El Quisco.',
              'Es un lugar para recorrer en silencio y con cuidado: aquí la naturaleza tiene nombre y también reglas.'],
         fuente='Fuente: Res. Ex. 6.648 del Ministerio del Medio Ambiente, 29/09/2025 (BCN, Ley Chile).'),
    dict(slug='las-petras', nombre='Quebrada Las Petras', dim='humedal', img='territorio-las-petras',
         alt='Ilustración en acuarela de una quebrada costera con vegetación y un sendero hacia el mar, inspirada en Las Petras',
         breve='Una quebrada costera donde la vegetación baja hasta el mar.',
         que=['Una de las quebradas de la costa de El Quisco, donde el verde baja hasta el mar.',
              'Es parte de la dimensión Humedal y bosque nativo: el El Quisco que no se ve desde la playa.'], fuente=''),
    dict(slug='mirador-neptuno', nombre='Mirador Neptuno', dim='acantilados', img='territorio-mirador-neptuno',
         alt='Ilustración en acuarela de un mirador de madera sobre rocas costeras frente al mar, inspirada en el Mirador Neptuno',
         breve='Un mirador sobre las rocas para mirar el Pacífico de frente.',
         que=['Un mirador costero sobre las rocas, frente al Pacífico.',
              'Es parte de la dimensión Acantilados y mar profundo.'], fuente=''),
    dict(slug='punta-de-tralca', nombre='Punta de Tralca', dim='acantilados', img='territorio-punta-de-tralca',
         alt='Ilustración en acuarela de un cactus costero sobre la roca',
         breve='Uno de los sectores costeros que forman la comuna.',
         que=['Punta de Tralca aparece junto a Isla Negra y El Totoral en la firma del logotipo de El Quisco: es uno de los nombres que forman la comuna.',
              'Es parte de la dimensión Acantilados y mar profundo.'], fuente=''),
    dict(slug='isla-negra', nombre='Isla Negra', dim='memoria', img='territorio-isla-negra',
         alt='Ilustración en acuarela de una costa rocosa con casas sobre la ladera, inspirada en Isla Negra',
         breve='Parte de la comuna y del Litoral de los Poetas.',
         que=['Isla Negra es parte de la comuna de El Quisco y del destino Litoral de los Poetas.',
              'Es parte de la dimensión Memoria y sabores: relatos, poesía y oficios del litoral.'],
         fuente='Fuente: chile.travel, Litoral de los Poetas.'),
    dict(slug='el-totoral', nombre='El Totoral', dim='humedal', img='territorio-el-totoral',
         alt='Ilustración en acuarela de un camino rural de tierra entre matorrales costeros, inspirada en El Totoral',
         breve='El lado rural de la comuna, entre caminos de tierra y matorral costero.',
         que=['El Totoral aparece junto a Isla Negra y Punta de Tralca en la firma del logotipo de El Quisco.',
              'Es el lado rural de la comuna: caminos de tierra y matorral costero.'], fuente=''),
    dict(slug='caleta', nombre='La caleta', dim='memoria', img='territorio-caleta',
         alt='Ilustración en acuarela de una olla al fuego junto a casetas de pescadores frente al mar',
         breve='Donde el oficio de quienes salen al mar se convierte en sabor.',
         que=['En la caleta, el oficio de quienes salen al mar se convierte en sabor.',
              'Es parte de la dimensión Memoria y sabores.'], fuente=''),
]

PERSONAS = [
    ('Vengo de escapada', 'Elige una ruta en minutos, sin crear cuenta, y prepárala antes de salir.', 'rutas.html', 'Ver rutas', 'icono-sendero'),
    ('Quiero volver fuera del verano', 'Cada mes tiene algo distinto. Revisa la agenda y tu próxima ruta.', '#agenda', 'Ver agenda', 'icono-calendario'),
    ('Prefiero leer con calma', 'Activa la lectura fácil: letra grande y menos elementos. Cada ficha se puede imprimir.', '#', 'Activar lectura fácil', 'icono-hoja'),
    ('Vivo en El Quisco', '¿Conoces un rincón que merece una ruta? Propónlo y súmalo a la experiencia.', '#propon', 'Propón un lugar', 'icono-ubicacion'),
    ('Tengo un oficio local', 'La caleta y sus oficios son parte de Memoria y sabores.', 'territorios/caleta.html', 'Ver la caleta', 'icono-flor'),
]

def head(titulo, desc, R, extra=''):
    return f'''<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#faf7ee">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CL">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{R}assets/img/og-el-quisco.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{R}assets/icons/favicon.png">
<link rel="apple-touch-icon" href="{R}assets/icons/apple-touch-icon.png">
<link rel="stylesheet" href="{R}css/styles.css">
{extra}</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido principal</a>
'''

def header(R, actual):
    items = [('index.html', 'Inicio'), ('rutas.html', 'Rutas'), ('index.html#mira', 'Videos'),
             ('experiencia-khiska.html', 'Khiska'), ('index.html#agenda', 'Agenda')]
    cur = ' aria-current="page"'
    li = ''.join(f'<li><a href="{R}{h}"{cur if h == actual else ""}>{t}</a></li>' for h, t in items)
    return f'''<header class="cabecera">
  <div class="contenedor cabecera__fila">
    <a class="marca" href="{R}index.html">
      <img src="{R}assets/icons/icono-flor.webp" alt="" width="30" height="30">
      <span>El Quisco<small>Experiencia Khiska</small></span>
    </a>
    <nav class="nav" aria-label="Principal">
      <ul class="nav__lista" id="menu-principal" data-abierto="false">{li}</ul>
    </nav>
    <div class="cabecera__acciones">
      <button class="btn-lectura" type="button" aria-pressed="false"><span aria-hidden="true">Aa</span><span class="texto-largo">Lectura fácil</span><span class="visually-hidden"> (modo de lectura fácil)</span></button>
      <a class="btn btn--chico" href="{R}app/index.html">Abrir la app</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu-principal"><span class="menu-toggle__barras"></span><span class="visually-hidden">Abrir menú</span></button>
    </div>
  </div>
</header>
'''

def footer(R):
    return f'''<div class="franja-color decorativa" aria-hidden="true"></div>
<footer class="pie">
  <div class="contenedor">
    <div class="pie__grid pie__grid--3">
      <div>
        <img class="pie__logo" src="{R}assets/img/logo-el-quisco.webp" alt="El Quisco" width="190" height="78" loading="lazy">
        <p>El Quisco es el destino. Khiska es la experiencia que transforma la curiosidad en un recorrido.</p>
      </div>
      <div>
        <h2>Explora</h2>
        <ul>
          <li><a href="{R}rutas.html">Lugares y rutas</a></li>
          <li><a href="{R}index.html#mira">Videos</a></li>
          <li><a href="{R}experiencia-khiska.html">Experiencia Khiska</a></li>
          <li><a href="{R}app/index.html">App Khiska</a></li>
        </ul>
      </div>
      <div>
        <h2>Participa</h2>
        <ul>
          <li><a href="{R}index.html#propon">Propón un lugar</a></li>
          <li><a href="{R}index.html#agenda">Agenda</a></li>
          <li><a href="{R}privacidad.html">Uso y privacidad</a></li>
        </ul>
      </div>
    </div>
    <p class="pie__legal">Proyecto académico de Agencia C.C.C. · Duoc UC · <span data-anio>2026</span></p>
  </div>
</footer>
<script src="{R}js/videos.js" defer></script>
<script src="{R}js/main.js" defer></script>
</body>
</html>
'''

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>\n'

def tarjeta(t, R):
    dimtxt = DIM[t['dim']][0]
    ficha = f'{R}territorios/{t["slug"]}.html'
    pid = f'det-{t["slug"]}'
    return f'''<article class="tarjeta" data-dimension="{t["dim"]}">
      <div class="tarjeta__media"><img src="{R}assets/img/{t["img"]}-card.webp" alt="{t["alt"]}" width="640" height="357" loading="lazy"><span class="tarjeta__etiqueta">{dimtxt}</span></div>
      <div class="tarjeta__cuerpo">
        <h3><a href="{ficha}">{t["nombre"]}</a></h3>
        <p class="tarjeta__estado">{t["breve"]}</p>
        <div class="tarjeta__revelar">
          <button class="tarjeta__toggle" type="button" aria-expanded="false" aria-controls="{pid}">Ver más </button>
          <div class="tarjeta__detalle" id="{pid}" hidden>
            <p>{t["que"][0]}</p>
            <a class="btn btn--chico btn--secundario" href="{ficha}">Abrir ficha<span class="visually-hidden"> de {t["nombre"]}</span></a>
          </div>
        </div>
      </div>
    </article>'''

def chips(R, objetivo, resultado, enlace=None, recordar=False, leyenda=''):
    c = f'<button class="chip" type="button" data-dimension="todo" aria-pressed="true"><img src="{R}assets/icons/icono-sendero.webp" alt="" width="24" height="24">Ver todo</button>'
    for k, (n, ic) in DIM.items():
        c += f'<button class="chip" type="button" data-dimension="{k}" aria-pressed="false"><img src="{R}assets/icons/{ic}.webp" alt="" width="24" height="24">{n}</button>'
    attrs = f'data-filtro="{objetivo}" data-resultado="{resultado}"' + (f' data-enlace="{enlace}"' if enlace else '') + (' data-recordar' if recordar else '')
    return f'<fieldset class="chips" {attrs}><legend>{leyenda}</legend>{c}</fieldset>'

ESTADOS = '''<ul class="estados" aria-label="Cómo se abre una flor">
        <li class="estado"><img src="assets/img/flor-capullo.webp" alt="" width="360" height="404" loading="lazy"><strong>Capullo cerrado</strong><span>Ruta por descubrir</span></li>
        <li class="estado"><img src="assets/img/flor-parcial.webp" alt="" width="360" height="261" loading="lazy"><strong>Apertura parcial</strong><span>Ruta iniciada</span></li>
        <li class="estado"><img src="assets/img/flor-abierta.webp" alt="" width="360" height="261" loading="lazy"><strong>Flor abierta</strong><span>Ruta completada</span></li>
      </ul>'''

def index():
    R = ''
    desc = 'El Quisco no termina en la playa. Descubre humedales, miradores, memoria y sabores de caleta, mira los videos de la campaña y conoce Khiska: una ruta, una flor.'
    sch = ld({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": SITE, "inLanguage": "es-CL"},
        {"@type": "TouristDestination", "name": "El Quisco", "description": "Comuna costera de la Región de Valparaíso, Chile.",
         "includesAttraction": [{"@type": "TouristAttraction", "name": "Humedal Urbano El Batro"}]}]})
    cards = '\n'.join(tarjeta(t, R) for t in T)
    personas = ''.join(f'''<li class="persona-card">
          <img src="assets/icons/{ic}.webp" alt="" width="44" height="44">
          <h3>{titulo}</h3><p>{texto}</p>
          <a class="btn btn--chico btn--secundario" href="{href}"{' data-activar-lectura' if 'lectura' in cta else ''}>{cta}</a>
        </li>''' for titulo, texto, href, cta, ic in PERSONAS)
    fases = [('Julio', 'Despertar', 'El Quisco no termina en la playa. Un mes para mirar la comuna con otros ojos y elegir qué descubrir primero.'),
             ('Agosto', 'Recorrer', 'Elige, prepara y comienza: el mes para salir a hacer tu primera ruta.'),
             ('Septiembre', 'Florecer y volver', 'Con la primavera, una razón para volver: tu cactus todavía tiene capullos por abrir.')]
    agenda = ''.join(f'''<details class="mes"{" open" if i == 0 else ""}>
          <summary><img src="assets/icons/icono-calendario.webp" alt="" width="32" height="32">{m} · {f}</summary>
          <div class="mes__cuerpo"><p>{d}</p></div>
        </details>''' for i, (m, f, d) in enumerate(fases))
    body = f'''{header(R, "index.html")}
<main id="contenido">
  <section class="hero" aria-labelledby="titulo-hero">
    <div class="contenedor hero__grid">
      <div>
        <img class="hero__logo" src="assets/img/logo-el-quisco.webp" alt="El Quisco" width="900" height="370" fetchpriority="high">
        <h1 id="titulo-hero">Donde la naturaleza tiene nombre.</h1>
        <p class="hero__bajada">El Quisco no termina en la playa. Hay humedales, miradores, memoria y sabores que se descubren por capas.</p>
        <div class="hero__acciones">
          <a class="btn" href="rutas.html">Descubre las rutas</a>
          <a class="btn btn--secundario" href="#mira">Mira el video</a>
        </div>
      </div>
      <div class="hero__ilustracion">
        <img class="ilustracion" src="assets/img/cactus-khiska-tres-flores.webp" alt="Cactus ilustrado en acuarela con tres flores rosadas abiertas y capullos por abrir" width="900" height="710">
      </div>
    </div>
  </section>

  <div class="franja-color decorativa" aria-hidden="true"></div>

  <section class="seccion" id="para-ti" aria-labelledby="titulo-para-ti">
    <div class="contenedor">
      <div class="seccion__cabecera">
        <span class="rotulo">Para ti</span>
        <h2 id="titulo-para-ti">¿Cómo quieres vivir El Quisco?</h2>
      </div>
      <ul class="personas-grid">{personas}</ul>
    </div>
  </section>

  <section class="seccion seccion--papel2" id="mira" aria-labelledby="titulo-mira">
    <div class="contenedor">
      <div class="seccion__cabecera">
        <span class="rotulo rotulo--rosa">Mira</span>
        <h2 id="titulo-mira">El Quisco en movimiento</h2>
        <p>Los videos de la campaña, en un solo lugar.</p>
      </div>
      <div class="videos" id="lista-videos" data-base="">
        <figure class="video-card video-card--destacado">
          <video controls playsinline preload="metadata" poster="assets/video/poster-v00.jpg" width="540" height="960">
            <source src="assets/video/v00-el-quisco-desde-un-solo-lugar.mp4" type="video/mp4">
          </video>
          <figcaption><strong>Ahora El Quisco se puede explorar desde un solo lugar</strong></figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="seccion seccion--espinas" id="curiosidad" aria-labelledby="titulo-curiosidad">
    <div class="contenedor curiosidad">
      <div>
        <h2 class="curiosidad__titulo activacion" id="titulo-curiosidad">Pincha tu curiosidad.</h2>
        <p>¿Qué parte de El Quisco quieres descubrir? Elige una dimensión y te mostramos primero esos lugares.</p>
      </div>
      <div>
        {chips(R, "lista-panoramas", "resultado-panoramas", "enlace-catalogo", True, "Elige lo que te gustaría descubrir")}
      </div>
    </div>
  </section>

  <section class="seccion" id="panoramas" aria-labelledby="titulo-panoramas">
    <div class="contenedor">
      <div class="seccion__cabecera">
        <span class="rotulo">Lugares</span>
        <h2 id="titulo-panoramas">Hay más por descubrir.</h2>
        <p>Siete lugares, tres formas de recorrer El Quisco.</p>
      </div>
      <p class="resultado" id="resultado-panoramas" aria-live="polite"></p>
      <div class="grid-tarjetas" id="lista-panoramas">
{cards}
      </div>
      <p class="mt-2"><a class="btn" id="enlace-catalogo" href="rutas.html">Ver todos los lugares</a></p>
    </div>
  </section>

  <section class="seccion seccion--papel2" id="khiska" aria-labelledby="titulo-khiska">
    <div class="contenedor">
      <div class="khiska">
        <div class="khiska__ilustracion">
          <img class="ilustracion" src="assets/img/cactus-khiska-una-flor.webp" alt="Cactus ilustrado con una flor abierta y capullos cerrados en sus brazos" width="458" height="730" loading="lazy">
        </div>
        <div>
          <span class="rotulo">Experiencia Khiska</span>
          <h2 class="lema activacion" id="titulo-khiska">Una ruta.<br>Una flor.</h2>
          <p>Khiska es tu cactus. Cada ruta que completas en El Quisco abre una de sus flores y suma un sello a tu Pasaporte. No es un ranking: es el registro de lo que viviste.</p>
          <ol class="pasos">
            <li><span><strong>Explora una ruta.</strong> Elige un lugar y revisa su ficha antes de ir.</span></li>
            <li><span><strong>Completa la experiencia.</strong> Recorre la ruta de principio a fin.</span></li>
            <li><span><strong>Haz florecer tu Khiska.</strong> Al completarla, su flor se abre en tu cactus.</span></li>
          </ol>
          <div class="hero__acciones">
            <a class="btn" href="app/index.html">Abrir la app Khiska</a>
            <a class="btn btn--secundario" href="experiencia-khiska.html">Cómo funciona</a>
          </div>
        </div>
      </div>
      {ESTADOS}
    </div>
  </section>

  <section class="seccion" id="propon" aria-labelledby="titulo-propon">
    <div class="contenedor comunidad">
      <div>
        <span class="rotulo">Comunidad</span>
        <h2 id="titulo-propon">Cada ruta tiene algo que contar.</h2>
        <p>Las historias de El Quisco las cuentan sus vecinos, sus oficios y quienes lo visitan. ¿Conoces un rincón que merece una ruta?</p>
        <img class="ilustracion decorativa propon__img" src="assets/img/sello-ruta-completada.webp" alt="" width="220" height="220" loading="lazy">
      </div>
      <form class="formulario" id="form-propuesta" novalidate data-endpoint="">
        <h3>Propón un lugar</h3>
        <div class="campo">
          <label for="lugar">Lugar <span class="req" aria-hidden="true">*</span><span class="visually-hidden">(obligatorio)</span></label>
          <input type="text" id="lugar" name="lugar" autocomplete="off" required aria-describedby="error-lugar">
          <p class="error" id="error-lugar" aria-live="polite"></p>
        </div>
        <div class="campo">
          <label for="motivo">¿Por qué vale la pena descubrirlo? <span class="req" aria-hidden="true">*</span><span class="visually-hidden">(obligatorio)</span></label>
          <textarea id="motivo" name="motivo" required aria-describedby="ayuda-motivo error-motivo"></textarea>
          <span class="ayuda" id="ayuda-motivo">Una historia, un oficio o un paisaje.</span>
          <p class="error" id="error-motivo" aria-live="polite"></p>
        </div>
        <div class="campo">
          <label for="nombre">Tu nombre (opcional)</label>
          <input type="text" id="nombre" name="nombre" autocomplete="name">
        </div>
        <div class="campo">
          <label for="correo">Correo (opcional)</label>
          <input type="email" id="correo" name="correo" autocomplete="email" aria-describedby="error-correo">
          <p class="error" id="error-correo" aria-live="polite"></p>
        </div>
        <div class="campo campo--check">
          <input type="checkbox" id="consentimiento" name="consentimiento" required aria-describedby="error-consentimiento">
          <label for="consentimiento">Autorizo que el equipo revise esta propuesta. <a href="privacidad.html">Uso y privacidad</a></label>
        </div>
        <p class="error" id="error-consentimiento" aria-live="polite"></p>
        <div class="acciones">
          <button class="btn" type="submit">Enviar propuesta</button>
          <button class="btn btn--secundario" type="button" id="copiar-propuesta" hidden>Copiar texto</button>
        </div>
        <div class="estado-form" id="form-estado" role="status" aria-live="polite"></div>
      </form>
    </div>
  </section>

  <section class="seccion seccion--papel2" id="agenda" aria-labelledby="titulo-agenda">
    <div class="contenedor">
      <div class="seccion__cabecera">
        <span class="rotulo">Agenda</span>
        <h2 id="titulo-agenda">Razones para volver.</h2>
        <p>Tres meses para descubrir El Quisco fuera del verano.</p>
      </div>
      <div class="agenda">{agenda}</div>
    </div>
  </section>
</main>
'''
    write('index.html', head('El Quisco: donde la naturaleza tiene nombre · Experiencia Khiska', desc, R, sch) + body + footer(R))

def rutas():
    R = ''
    desc = 'Lugares de El Quisco para descubrir más allá de la playa: humedal, acantilados, memoria y sabores de caleta.'
    cards = '\n'.join(tarjeta(t, R) for t in T)
    body = f'''{header(R, "rutas.html")}
<main id="contenido">
  <div class="contenedor">
    <nav class="migas" aria-label="Ruta de navegación"><ol><li><a href="index.html">Inicio</a></li><li aria-current="page">Lugares y rutas</li></ol></nav>
    <header class="cabecera-pagina">
      <span class="rotulo">Lugares</span>
      <h1>Lugares y rutas de El Quisco</h1>
      <p class="estrecho">Elige por dimensión y abre la ficha de cada lugar. Cada ruta que completes abre una flor en tu Khiska.</p>
      <img class="cabecera-pagina__sendero ilustracion decorativa" src="assets/img/sendero-ilustrado.webp" alt="" width="2000" height="389">
    </header>
    {chips(R, "lista-catalogo", "resultado-catalogo", None, True, "Filtrar por dimensión")}
    <p class="resultado" id="resultado-catalogo" aria-live="polite"></p>
    <div class="grid-tarjetas pb-4" id="lista-catalogo">
{cards}
    </div>
  </div>
</main>
'''
    write('rutas.html', head('Lugares y rutas · El Quisco · Experiencia Khiska', desc, R) + body + footer(R))

def fichas():
    R = '../'
    for t in T:
        dimtxt = DIM[t['dim']][0]
        que = ''.join(f'<p>{p}</p>' for p in t['que'])
        fuente = f'<p class="fuente">{t["fuente"]}</p>' if t['fuente'] else ''
        sch = ld({"@context": "https://schema.org", "@type": "TouristAttraction", "name": t['nombre'],
                  "containedInPlace": {"@type": "City", "name": "El Quisco"}})
        body = f'''{header(R, "")}
<main id="contenido">
  <div class="contenedor">
    <nav class="migas" aria-label="Ruta de navegación"><ol><li><a href="../index.html">Inicio</a></li><li><a href="../rutas.html">Lugares y rutas</a></li><li aria-current="page">{t["nombre"]}</li></ol></nav>
    <div class="ficha-hero">
      <div>
        <span class="rotulo">{dimtxt}</span>
        <h1>{t["nombre"]}</h1>
        <p class="hero__bajada">{t["breve"]}</p>
      </div>
      <figure class="ficha-hero__media"><img src="../assets/img/{t["img"]}.webp" alt="{t["alt"]}" width="1200" height="670"><figcaption>Ilustración de la campaña.</figcaption></figure>
    </div>
    <div class="ficha-cuerpo pb-4">
      <div>
        <h2>El lugar</h2>
        {que}
        {fuente}
        <h2 class="mt-2">Antes de ir</h2>
        <ul class="lista-cuidado">
          <li>Revisa el pronóstico y lleva agua.</li>
          <li>Sigue los senderos y lleva tu basura de vuelta.</li>
          <li>Observa la flora y la fauna sin intervenirlas.</li>
        </ul>
      </div>
      <aside>
        <div class="caja">
          <img class="ilustracion caja__flor" src="../assets/img/flor-abierta.webp" alt="" width="120" height="87">
          <h2 class="h-caja">Una ruta. Una flor.</h2>
          <p>Cuando completas una ruta, su flor se abre en tu Khiska.</p>
          <div class="acciones"><a class="btn" href="../app/index.html">Abrir la app Khiska</a></div>
        </div>
        <div class="caja no-imprimir">
          <h2 class="h-caja">Lleva esta ficha</h2>
          <p>Imprímela o guárdala como PDF.</p>
          <div class="acciones">
            <button class="btn btn--secundario" type="button" data-imprimir>Imprimir ficha</button>
            <a class="btn btn--secundario" href="../rutas.html">Volver a lugares</a>
          </div>
        </div>
      </aside>
    </div>
  </div>
</main>
'''
        write(f'territorios/{t["slug"]}.html', head(f'{t["nombre"]} · El Quisco · Experiencia Khiska', f'{t["nombre"]}, El Quisco. {t["breve"]}', R, sch) + body + footer(R))

def khiska():
    R = ''
    desc = 'Khiska: una ruta, una flor. Tu cactus registra lo que descubres en El Quisco y tu Pasaporte guarda cada ruta completada.'
    body = f'''{header(R, "experiencia-khiska.html")}
<main id="contenido">
  <div class="contenedor">
    <nav class="migas" aria-label="Ruta de navegación"><ol><li><a href="index.html">Inicio</a></li><li aria-current="page">Experiencia Khiska</li></ol></nav>
    <header class="cabecera-pagina khiska">
      <div>
        <span class="rotulo">Experiencia Khiska</span>
        <h1>La curiosidad hecha recorrido.</h1>
        <p class="hero__bajada">No inventamos otro mundo: te invitamos a descubrir el que existe. Khiska es tu cactus, y registra lo que vives en El Quisco.</p>
        <div class="hero__acciones"><a class="btn" href="app/index.html">Abrir la app Khiska</a></div>
      </div>
      <div class="khiska__ilustracion"><img class="ilustracion" src="assets/img/cactus-khiska-florecido.webp" alt="Cactus ilustrado con todas sus flores rosadas abiertas" width="900" height="685"></div>
    </header>
  </div>

  <section class="seccion seccion--espinas" aria-labelledby="titulo-pasos">
    <div class="contenedor">
      <div class="seccion__cabecera">
        <h2 class="lema activacion" id="titulo-pasos">Una ruta.<br>Una flor.</h2>
        <p>Cada flor es una ruta completa. Varias flores no son etapas de un mismo camino: son lugares distintos que ya viviste.</p>
      </div>
      <ol class="pasos pasos--grandes">
        <li><span><strong>Explora una ruta.</strong> Elige por lo que te da curiosidad, sin crear cuenta.</span></li>
        <li><span><strong>Completa la experiencia.</strong> Prepárala con su ficha y recórrela de principio a fin.</span></li>
        <li><span><strong>Haz florecer tu Khiska.</strong> Al terminar, su flor se abre en tu cactus.</span></li>
      </ol>
      {ESTADOS}
    </div>
  </section>

  <section class="seccion seccion--papel2" id="pasaporte" aria-labelledby="titulo-pasaporte">
    <div class="contenedor pasaporte">
      <img src="assets/img/pasaporte-khiska.webp" alt="Tarjeta vertical ilustrada del Pasaporte Khiska con un cactus en flor, código y progreso de rutas" width="600" height="894" loading="lazy">
      <div>
        <span class="rotulo">Pasaporte Khiska</span>
        <h2 id="titulo-pasaporte">Tu progreso es tuyo.</h2>
        <p>El Pasaporte guarda cada ruta que completas: un sello por recorrido. Sin rankings ni comparaciones.</p>
        <p>Existe en el celular y en papel, para que nadie quede fuera por no usar smartphone.</p>
        <img class="ilustracion decorativa sello-mini" src="assets/img/sello-ruta-completada.webp" alt="" width="140" height="140" loading="lazy">
      </div>
    </div>
  </section>

  <section class="seccion" aria-labelledby="titulo-app">
    <div class="contenedor estrecho centrado">
      <h2 id="titulo-app">Mi Khiska, en tu mano</h2>
      <p>En la app ves tu cactus, las flores que abriste y tu próxima ruta. También tiene lectura fácil.</p>
      <div class="hero__acciones centrado"><a class="btn" href="app/index.html">Abrir la app Khiska</a><a class="btn btn--secundario" href="rutas.html">Ver lugares</a></div>
    </div>
  </section>
</main>
'''
    write('experiencia-khiska.html', head('Experiencia Khiska: una ruta, una flor · El Quisco', desc, R) + body + footer(R))

def privacidad():
    R = ''
    body = f'''{header(R, "")}
<main id="contenido">
  <div class="contenedor estrecho pb-4">
    <nav class="migas" aria-label="Ruta de navegación"><ol><li><a href="index.html">Inicio</a></li><li aria-current="page">Uso y privacidad</li></ol></nav>
    <header class="cabecera-pagina"><h1>Uso y privacidad</h1></header>
    <h2>Lo que guarda este sitio</h2>
    <p>El sitio no usa cookies ni analítica. Solo guarda en tu navegador si activaste la lectura fácil y qué dimensión elegiste. Esa información no sale de tu dispositivo.</p>
    <h2>Propón un lugar</h2>
    <p>Las propuestas se usan solo para considerar nuevas rutas. Pedimos lo mínimo: el lugar y por qué vale la pena. Tu nombre y correo son opcionales.</p>
    <h2>Imágenes</h2>
    <p>Las imágenes de lugares son ilustraciones de la campaña.</p>
  </div>
</main>
'''
    write('privacidad.html', head('Uso y privacidad · El Quisco · Experiencia Khiska', 'Uso y privacidad del portal El Quisco · Experiencia Khiska.', R) + body + footer(R))

def write(path, s):
    with open(OUT + path, 'w', encoding='utf-8') as f: f.write(s)
    print('ok', path)

index(); rutas(); fichas(); khiska(); privacidad()
