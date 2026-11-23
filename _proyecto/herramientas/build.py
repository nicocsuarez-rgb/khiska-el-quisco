# Genera las páginas HTML estáticas del sitio (el resultado no requiere este script).
import json, os, html
OUT = '/home/claude/sitio-web/'
SITE = 'El Quisco · Experiencia Khiska'

DIM = {
    'acantilados': ('Acantilados y mar profundo', 'icono-rocas'),
    'humedal': ('Humedal y bosque nativo', 'icono-hoja'),
    'memoria': ('Memoria y sabores', 'icono-flor'),
}

T = [  # Territorios: solo datos con respaldo; el resto queda por confirmar
    dict(slug='el-batro', nombre='Humedal El Batro', dim='humedal', img='territorio-el-batro',
         alt='Ilustración en acuarela de un humedal costero con juncos y agua quieta, inspirada en El Batro',
         breve='Humedal urbano reconocido oficialmente en 2025. Cualquier visita debe respetar su protección.',
         que=['El Humedal Urbano El Batro fue reconocido por el Ministerio del Medio Ambiente el 29 de septiembre de 2025 (Res. Ex. 6.648), a solicitud del municipio de El Quisco.',
              'Ese reconocimiento es un dato del territorio, no la confirmación de una ruta: cualquier recorrido aquí debe acordarse con el municipio y respetar la protección del humedal.'],
         fuente='Fuente: Biblioteca del Congreso Nacional (Ley Chile), Res. Ex. 6.648 del MMA, 29/09/2025.'),
    dict(slug='las-petras', nombre='Quebrada Las Petras', dim='humedal', img='territorio-las-petras',
         alt='Ilustración en acuarela de una quebrada costera con vegetación y un sendero hacia el mar, inspirada en Las Petras',
         breve='Quebrada costera identificada como referente del territorio. Visita por validar.',
         que=['Quebrada costera que el equipo identificó como referente territorial de El Quisco.',
              'Todavía no hay un recorrido validado: no publicamos tiempos, accesos ni dificultad hasta confirmarlos en terreno.'],
         fuente=''),
    dict(slug='mirador-neptuno', nombre='Mirador Neptuno', dim='acantilados', img='territorio-mirador-neptuno',
         alt='Ilustración en acuarela de un mirador de madera sobre rocas costeras frente al mar, inspirada en el Mirador Neptuno',
         breve='Mirador costero identificado como referente del territorio. Visita por validar.',
         que=['Mirador costero que el equipo identificó como referente territorial de El Quisco.',
              'La información práctica de la visita se publicará cuando esté confirmada.'],
         fuente=''),
    dict(slug='punta-de-tralca', nombre='Punta de Tralca', dim='acantilados', img=None,
         alt='',
         breve='Sector costero de la comuna, mencionado en la identidad de El Quisco. Visita por validar.',
         que=['Punta de Tralca aparece junto a Isla Negra y El Totoral en la firma del logotipo comunal de El Quisco entregado al equipo.',
              'Aún no contamos con imagen ni con un recorrido validado para este sector.'],
         fuente='Fuente: logotipo de El Quisco incluido en la carpeta de recursos del proyecto.'),
    dict(slug='isla-negra', nombre='Isla Negra', dim='memoria', img='territorio-isla-negra',
         alt='Ilustración en acuarela de una costa rocosa con casas sobre la ladera, inspirada en Isla Negra',
         breve='Localidad de la comuna asociada al Litoral de los Poetas. Visita por validar.',
         que=['Isla Negra es parte de la comuna de El Quisco y se asocia al destino turístico Litoral de los Poetas.',
              'Los relatos y hitos de una posible ruta se definirán con actores locales antes de publicarse.'],
         fuente='Fuentes: logotipo comunal de El Quisco (carpeta de recursos) y chile.travel, citado en el Documento central del proyecto (8/11/2026).'),
    dict(slug='el-totoral', nombre='El Totoral', dim=None, img='territorio-el-totoral',
         alt='Ilustración en acuarela de un camino rural de tierra entre matorrales costeros, inspirada en El Totoral',
         breve='Sector rural de la comuna, mencionado en la identidad de El Quisco. Visita por validar.',
         que=['El Totoral aparece junto a Isla Negra y Punta de Tralca en la firma del logotipo comunal de El Quisco entregado al equipo.',
              'Su dimensión dentro de Khiska y el posible recorrido están por definir.'],
         fuente='Fuente: logotipo de El Quisco incluido en la carpeta de recursos del proyecto.'),
    dict(slug='caleta', nombre='La caleta', dim='memoria', img='territorio-caleta',
         alt='Ilustración en acuarela de una olla al fuego junto a casetas de pescadores frente al mar',
         breve='Oficios del mar y cocina de caleta como parte de la experiencia. Visita por validar.',
         que=['La caleta reúne oficios del mar y gastronomía de caleta, dos capas del territorio que la campaña quiere poner en valor.',
              'Los comercios, horarios y relatos asociados solo se publicarán con acuerdo de sus protagonistas.'],
         fuente=''),
]

def head(titulo, desc, R, path, extra=''):
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
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{R}assets/icons/favicon.png">
<link rel="apple-touch-icon" href="{R}assets/icons/apple-touch-icon.png">
<link rel="stylesheet" href="{R}css/styles.css">
{extra}</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido principal</a>
<p class="franja-aviso">Propuesta académica de Agencia C.C.C. Las rutas y el Pasaporte Khiska están en etapa de validación. <a href="{R}experiencia-khiska.html#estado">Qué está disponible</a></p>
'''

def header(R, actual):
    items = [('index.html', 'Inicio'), ('rutas.html', 'Rutas'), ('experiencia-khiska.html', 'Experiencia Khiska'),
             ('index.html#agenda', 'Agenda'), ('index.html#comunidad', 'Comunidad')]
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
      <a class="btn btn--chico" href="{R}experiencia-khiska.html#mi-khiska">Mi Khiska</a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu-principal"><span class="menu-toggle__barras"></span><span class="visually-hidden">Abrir menú</span></button>
    </div>
  </div>
</header>
'''

def footer(R):
    return f'''<div class="franja-color decorativa" aria-hidden="true"></div>
<footer class="pie">
  <div class="contenedor">
    <div class="pie__grid">
      <div>
        <img class="pie__logo" src="{R}assets/img/logo-el-quisco.webp" alt="El Quisco" width="190" height="78" loading="lazy">
        <p>El Quisco es el destino. Khiska es la experiencia que transforma la curiosidad en un recorrido.</p>
      </div>
      <div>
        <h2>Explora</h2>
        <ul>
          <li><a href="{R}rutas.html">Lugares y rutas</a></li>
          <li><a href="{R}experiencia-khiska.html">Experiencia Khiska</a></li>
          <li><a href="{R}index.html#agenda">Agenda</a></li>
          <li><a href="{R}index.html#propon">Propón un lugar</a></li>
        </ul>
      </div>
      <div>
        <h2>Redes</h2>
        <ul>
          <li>Instagram · Facebook · TikTok · YouTube</li>
          <li><span class="pendiente">Cuentas por confirmar</span></li>
        </ul>
      </div>
      <div>
        <h2>Contacto</h2>
        <ul>
          <li><span class="pendiente">Contacto pendiente</span></li>
          <li>Se publicará el canal oficial cuando el municipio u oficina de turismo lo confirme.</li>
        </ul>
      </div>
    </div>
    <div class="pie__legal">
      <p>Propuesta académica de Agencia C.C.C. (Fernanda Cruz, Benjamín Cerda y Nicolás Cáceres) · Taller de Estrategia y Planificación Digital MDC1106 · Duoc UC · <span data-anio>2026</span>.</p>
      <p>Las imágenes de lugares son ilustraciones inspiradas en el territorio, no fotografías. QR, recompensas, rutas y Wallet son demostraciones hasta que su funcionamiento esté validado. <a href="{R}privacidad.html">Uso y privacidad</a></p>
    </div>
  </div>
</footer>
<script src="{R}js/main.js" defer></script>
</body>
</html>
'''

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>\n'

def tarjeta(t, R, catalogo=False):
    dimtxt = DIM[t['dim']][0] if t['dim'] else 'Dimensión por confirmar'
    ficha = f'{R}territorios/{t["slug"]}.html'
    if t['img']:
        media = f'<div class="tarjeta__media"><img src="{R}assets/img/{t["img"]}-card.webp" alt="{t["alt"]}" width="640" height="357" loading="lazy"><span class="tarjeta__etiqueta">{dimtxt}</span></div>'
    else:
        media = f'<div class="tarjeta__media tarjeta__media--pendiente"><div><img src="{R}assets/icons/icono-ubicacion.webp" alt="" width="70" height="107"><span class="pendiente">Imagen pendiente</span></div><span class="tarjeta__etiqueta">{dimtxt}</span></div>'
    datos = ''
    if catalogo:
        datos = f'''<ul class="datos">
          <li><img src="{R}assets/icons/icono-reloj.webp" alt="" width="26" height="26"><strong>Duración:</strong> <span class="pendiente">Por confirmar</span></li>
          <li><img src="{R}assets/icons/icono-sendero.webp" alt="" width="26" height="26"><strong>Dificultad:</strong> <span class="pendiente">Por confirmar</span></li>
        </ul>'''
    pid = f'det-{t["slug"]}{"-c" if catalogo else ""}'
    return f'''<article class="tarjeta" data-dimension="{t["dim"] or "sin-dimension"}">
      {media}
      <div class="tarjeta__cuerpo">
        <h3><a href="{ficha}">{t["nombre"]}</a></h3>
        <p class="tarjeta__estado">Referente territorial · visita por validar</p>
        {datos}
        <div class="tarjeta__revelar">
          <button class="tarjeta__toggle" type="button" aria-expanded="false" aria-controls="{pid}">Ver descripción </button>
          <div class="tarjeta__detalle" id="{pid}" hidden>
            <p>{t["breve"]}</p>
            <a class="btn btn--chico btn--secundario" href="{ficha}">Ver ficha<span class="visually-hidden"> de {t["nombre"]}</span></a>
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

# ------------------------------------------------------------------ index
def index():
    R = ''
    desc = 'El Quisco no termina en la playa. Descubre humedales, miradores, memoria y sabores de caleta, y conoce Khiska: una ruta, una flor.'
    sch = ld({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": SITE, "inLanguage": "es-CL"},
        {"@type": "TouristDestination", "name": "El Quisco",
         "description": "Comuna costera de la Región de Valparaíso, Chile.",
         "containedInPlace": {"@type": "AdministrativeArea", "name": "Región de Valparaíso, Chile"},
         "includesAttraction": [{"@type": "TouristAttraction", "name": "Humedal Urbano El Batro"}]}]})
    destacados = [t for t in T if t['img']]
    cards = '\n'.join(tarjeta(t, R) for t in destacados)
    meses = ''
    for i, m in enumerate(['Julio · Despertar', 'Agosto · Recorrer', 'Septiembre · Florecer y volver']):
        meses += f'''<details class="mes"{" open" if i == 0 else ""}>
          <summary><img src="assets/icons/icono-calendario.webp" alt="" width="32" height="32">{m}</summary>
          <div class="mes__cuerpo">
            <p><span class="pendiente">Contenido pendiente</span></p>
            <p>Aún no hay actividades confirmadas para este mes. Solo publicaremos fecha, lugar y responsable cuando estén confirmados.</p>
          </div>
        </details>'''
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
          <a class="btn btn--secundario" href="#khiska">¿Cómo funciona Khiska?</a>
        </div>
      </div>
      <div class="hero__ilustracion">
        <img class="ilustracion" src="assets/img/cactus-khiska-tres-flores.webp" alt="Cactus ilustrado en acuarela con tres flores rosadas abiertas y capullos por abrir" width="900" height="710">
      </div>
    </div>
  </section>

  <div class="franja-color decorativa" aria-hidden="true"></div>

  <section class="seccion seccion--espinas" id="curiosidad" aria-labelledby="titulo-curiosidad">
    <div class="contenedor curiosidad">
      <div>
        <span class="rotulo rotulo--rosa">Paso opcional</span>
        <h2 class="curiosidad__titulo activacion" id="titulo-curiosidad">Pincha tu curiosidad.</h2>
        <p>¿Qué parte de El Quisco quieres descubrir? Elige una dimensión y te mostramos primero esos lugares.</p>
      </div>
      <div>
        {chips(R, "lista-panoramas", "resultado-panoramas", "enlace-catalogo", True, "Elige lo que te gustaría descubrir")}
        <p class="saltar-intereses"><a href="#panoramas" data-saltar>Prefiero ver todo</a></p>
      </div>
    </div>
  </section>

  <section class="seccion" id="panoramas" aria-labelledby="titulo-panoramas">
    <div class="contenedor">
      <div class="seccion__cabecera">
        <span class="rotulo">Panoramas y rutas</span>
        <h2 id="titulo-panoramas">Hay más por descubrir.</h2>
        <p>Estos lugares son referentes del territorio. Cada ruta, con sus hitos, tiempos y accesos, se publicará cuando esté validada en terreno.</p>
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
          <p>Khiska es la curiosidad hecha recorrido. Tu cactus registra lo que descubres: cada flor representa una ruta completa. No es una mascota ni un ranking: es tu registro personal.</p>
          <ol class="pasos">
            <li><span><strong>Explora una ruta.</strong> Elige un lugar y revisa su ficha antes de ir.</span></li>
            <li><span><strong>Completa la experiencia.</strong> Recorre los hitos definidos de esa ruta.</span></li>
            <li><span><strong>Haz florecer tu Khiska.</strong> Al completarla, su flor se abre en tu cactus.</span></li>
          </ol>
          <div class="hero__acciones">
            <a class="btn" href="experiencia-khiska.html">Prueba la demostración</a>
          </div>
        </div>
      </div>
      <ul class="estados" aria-label="Estados de una flor">
        <li class="estado"><img src="assets/img/flor-capullo.webp" alt="" width="360" height="404" loading="lazy"><strong>Capullo cerrado</strong><span>Ruta no iniciada</span></li>
        <li class="estado"><img src="assets/img/flor-parcial.webp" alt="" width="360" height="261" loading="lazy"><strong>Apertura parcial</strong><span>Ruta iniciada</span></li>
        <li class="estado"><img src="assets/img/flor-abierta.webp" alt="" width="360" height="261" loading="lazy"><strong>Flor abierta</strong><span>Una ruta completada</span></li>
        <li class="estado"><img src="assets/img/flor-beneficio.webp" alt="" width="360" height="339" loading="lazy"><strong>Beneficio señalado</strong><span>Solo si existe un acuerdo local confirmado</span></li>
      </ul>
    </div>
  </section>

  <section class="seccion" id="comunidad" aria-labelledby="titulo-comunidad">
    <div class="contenedor">
      <div class="seccion__cabecera">
        <span class="rotulo">Comunidad</span>
        <h2 id="titulo-comunidad">Cada ruta tiene algo que contar.</h2>
        <p>Las historias de El Quisco las cuentan sus vecinos, oficios y visitantes. Aquí se mostrarán publicaciones reales y podrás proponer lugares para futuras rutas.</p>
      </div>
      <div class="comunidad">
        <div class="ig">
          <div class="ig__cuenta">
            <img src="assets/img/avatar-cuenta.webp" alt="" width="52" height="52" loading="lazy">
            <div><strong>Cuenta turística de El Quisco</strong><span class="pendiente">Usuario por confirmar</span></div>
          </div>
          <div class="ig__marco">
            <p><strong>Última publicación de Instagram</strong><br>Este espacio mostrará la publicación más reciente de la cuenta oficial. La integración está pendiente de acceso y permisos.</p>
          </div>
        </div>
        <div id="propon">
          <form class="formulario" id="form-propuesta" novalidate data-endpoint="">
            <h3>Propón un lugar</h3>
            <p>¿Conoces un rincón de El Quisco que merezca una ruta? Cuéntanos. Las propuestas se revisan antes de considerarlas.</p>
            <div class="campo">
              <label for="lugar">Lugar <span class="req" aria-hidden="true">*</span><span class="visually-hidden">(obligatorio)</span></label>
              <input type="text" id="lugar" name="lugar" autocomplete="off" required aria-describedby="error-lugar">
              <p class="error" id="error-lugar" aria-live="polite"></p>
            </div>
            <div class="campo">
              <label for="motivo">¿Por qué vale la pena descubrirlo? <span class="req" aria-hidden="true">*</span><span class="visually-hidden">(obligatorio)</span></label>
              <textarea id="motivo" name="motivo" required aria-describedby="ayuda-motivo error-motivo"></textarea>
              <span class="ayuda" id="ayuda-motivo">Mínimo 20 caracteres. Puede ser una historia, un oficio o un paisaje.</span>
              <p class="error" id="error-motivo" aria-live="polite"></p>
            </div>
            <div class="campo">
              <label for="nombre">Tu nombre (opcional)</label>
              <input type="text" id="nombre" name="nombre" autocomplete="name">
            </div>
            <div class="campo">
              <label for="correo">Correo (opcional)</label>
              <input type="email" id="correo" name="correo" autocomplete="email" aria-describedby="ayuda-correo error-correo">
              <span class="ayuda" id="ayuda-correo">Solo si quieres que te contactemos sobre tu propuesta.</span>
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
      </div>
    </div>
  </section>

  <section class="seccion seccion--papel2" id="agenda" aria-labelledby="titulo-agenda">
    <div class="contenedor">
      <div class="seccion__cabecera">
        <span class="rotulo">Calendario</span>
        <h2 id="titulo-agenda">Razones para volver.</h2>
        <p>La agenda reúne actividades confirmadas del territorio, mes a mes.</p>
      </div>
      <div class="agenda">
        {meses}
      </div>
    </div>
  </section>
</main>
'''
    write('index.html', head('El Quisco: donde la naturaleza tiene nombre · Experiencia Khiska', desc, R, 'index.html', sch) + body + footer(R))

# ------------------------------------------------------------------ catálogo
def rutas():
    R = ''
    desc = 'Lugares de El Quisco para descubrir más allá de la playa: humedales, miradores, memoria y sabores. Rutas en etapa de validación.'
    cards = '\n'.join(tarjeta(t, R, catalogo=True) for t in T)
    sch = ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "index.html"},
        {"@type": "ListItem", "position": 2, "name": "Lugares y rutas"}]})
    body = f'''{header(R, "rutas.html")}
<main id="contenido">
  <div class="contenedor">
    <nav class="migas" aria-label="Ruta de navegación"><ol><li><a href="index.html">Inicio</a></li><li aria-current="page">Lugares y rutas</li></ol></nav>
    <header class="cabecera-pagina">
      <span class="rotulo">Catálogo</span>
      <h1>Lugares y rutas de El Quisco</h1>
      <p class="estrecho">Elige por dimensión y abre la ficha de cada lugar. Hoy son referentes territoriales: los recorridos, tiempos y accesos se agregarán solo cuando estén validados.</p>
      <img class="cabecera-pagina__sendero ilustracion decorativa" src="assets/img/sendero-ilustrado.webp" alt="" width="2000" height="389">
    </header>
    {chips(R, "lista-catalogo", "resultado-catalogo", None, True, "Filtrar por dimensión")}
    <p class="resultado" id="resultado-catalogo" aria-live="polite"></p>
    <div class="grid-tarjetas" id="lista-catalogo">
{cards}
    </div>
    <div class="aviso aviso--cierre">
      <p><strong>¿Por qué no hay tiempos ni dificultad?</strong> Porque aún no se han medido en terreno. Preferimos mostrar “por confirmar” antes que inventar un dato que te haga planificar mal tu visita.</p>
    </div>
  </div>
</main>
'''
    write('rutas.html', head('Lugares y rutas · El Quisco · Experiencia Khiska', desc, R, 'rutas.html', sch) + body + footer(R))

# ------------------------------------------------------------------ fichas
def fichas():
    R = '../'
    for t in T:
        dimtxt = DIM[t['dim']][0] if t['dim'] else 'Dimensión por confirmar'
        desc = f'{t["nombre"]}, El Quisco: referente territorial de la Experiencia Khiska. {t["breve"]}'
        if t['img']:
            media = f'<figure class="ficha-hero__media"><img src="../assets/img/{t["img"]}.webp" alt="{t["alt"]}" width="1200" height="670"><figcaption>Ilustración inspirada en el lugar; no es una fotografía.</figcaption></figure>'
        else:
            media = f'<figure class="ficha-hero__media tarjeta__media--pendiente media-pendiente"><div><img src="../assets/icons/icono-ubicacion.webp" alt="" width="80" height="122"><span class="pendiente">Imagen pendiente</span></div></figure>'
        que = ''.join(f'<p>{p}</p>' for p in t['que'])
        fuente = f'<p class="fuente">{t["fuente"]}</p>' if t['fuente'] else ''
        filas = [('icono-ubicacion', 'Hitos de la ruta'), ('icono-reloj', 'Duración'), ('icono-sendero', 'Dificultad'),
                 ('icono-hoja', 'Recomendaciones'), ('icono-rocas', 'Condiciones de acceso')]
        tabla = ''.join(f'<tr><th scope="row"><img src="../assets/icons/{i}.webp" alt="" width="22" height="22">{n}</th><td><span class="pendiente">Por confirmar</span></td></tr>' for i, n in filas)
        sch = ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "../index.html"},
            {"@type": "ListItem", "position": 2, "name": "Lugares y rutas", "item": "../rutas.html"},
            {"@type": "ListItem", "position": 3, "name": t['nombre']}]})
        body = f'''{header(R, "")}
<main id="contenido">
  <div class="contenedor">
    <nav class="migas" aria-label="Ruta de navegación"><ol><li><a href="../index.html">Inicio</a></li><li><a href="../rutas.html">Lugares y rutas</a></li><li aria-current="page">{t["nombre"]}</li></ol></nav>
    <div class="ficha-hero">
      <div>
        <span class="rotulo">{dimtxt}</span>
        <h1>{t["nombre"]}</h1>
        <p><span class="demo-sello">Referente territorial · visita por validar</span></p>
        <p class="hero__bajada">{t["breve"]}</p>
      </div>
      {media}
    </div>
    <div class="ficha-cuerpo pb-4">
      <div>
        <h2>Qué sabemos</h2>
        {que}
        {fuente}
        <h2 class="mt-2">Ficha práctica</h2>
        <table class="tabla-ficha">
          <caption class="visually-hidden">Información práctica de {t["nombre"]}</caption>
          <tbody>{tabla}</tbody>
        </table>
        <p class="fuente mt-1">Sin tiempos ni accesos inventados: estos datos se completarán después de validar el recorrido.</p>
      </div>
      <aside>
        <div class="caja">
          <h2 class="h-caja">¿Y la flor de esta ruta?</h2>
          <p>Podrás comenzar la experiencia y abrir su flor cuando el recorrido y su forma de validación estén definidos.</p>
          <div class="acciones">
            <a class="btn" href="../experiencia-khiska.html">Ver cómo funciona Khiska</a>
          </div>
        </div>
        <div class="caja no-imprimir">
          <h2 class="h-caja">Lleva esta ficha</h2>
          <p>Imprímela o guárdala como PDF para revisarla sin conexión.</p>
          <div class="acciones">
            <button class="btn btn--secundario" type="button" data-imprimir>Imprimir ficha</button>
            <a class="btn btn--secundario" href="../rutas.html">Volver al catálogo</a>
          </div>
        </div>
      </aside>
    </div>
  </div>
</main>
'''
        write(f'territorios/{t["slug"]}.html', head(f'{t["nombre"]} · Lugares de El Quisco · Experiencia Khiska', desc, R, '', sch) + body + footer(R))

# ------------------------------------------------------------------ Khiska
def khiska():
    R = ''
    desc = 'Cómo funciona Khiska: una ruta, una flor. Prueba la demostración del cactus y conoce el Pasaporte Khiska, en etapa de validación.'
    parcelas = ''.join(f'''<li class="parcela" data-ruta="demo-{l.lower()}" data-estado="capullo">
            <div class="parcela__flor"><img src="assets/img/flor-capullo.webp" alt="" width="360" height="404"></div>
            <h3>Ruta de ejemplo {l}</h3>
            <p class="parcela__estado">Capullo cerrado · ruta no iniciada</p>
            <button class="btn btn--chico" type="button">Iniciar ruta (demo)</button>
          </li>''' for l in 'ABCD')
    body = f'''{header(R, "experiencia-khiska.html")}
<main id="contenido">
  <div class="contenedor">
    <nav class="migas" aria-label="Ruta de navegación"><ol><li><a href="index.html">Inicio</a></li><li aria-current="page">Experiencia Khiska</li></ol></nav>
    <header class="cabecera-pagina khiska">
      <div>
        <span class="rotulo">Experiencia Khiska</span>
        <h1>La curiosidad hecha recorrido.</h1>
        <p class="hero__bajada">No inventamos otro mundo: te invitamos a descubrir el que existe. Khiska registra lo que vives en El Quisco con un cactus personal.</p>
        <p><strong>Explora una ruta. Completa la experiencia. Haz florecer tu Khiska.</strong></p>
      </div>
      <div class="khiska__ilustracion"><img class="ilustracion" src="assets/img/cactus-khiska-florecido.webp" alt="Cactus ilustrado con todas sus flores rosadas abiertas" width="900" height="685"></div>
    </header>
  </div>

  <section class="seccion seccion--espinas" id="mi-khiska" aria-labelledby="titulo-demo">
    <div class="contenedor">
      <div class="demo">
        <div class="demo__cabecera">
          <div>
            <span class="demo-sello">Demostración del prototipo</span>
            <h2 id="titulo-demo" class="mt-1">Mi Khiska</h2>
            <p class="estrecho">Simula cómo cambia tu cactus. Las rutas son de ejemplo: no corresponden a recorridos reales y el avance solo se guarda en este navegador.</p>
          </div>
          <div class="demo__controles">
            <label class="switch"><input type="checkbox" id="demo-sonido"> Sonido al florecer</label>
            <button class="btn btn--chico btn--secundario" type="button" id="demo-reiniciar">Reiniciar demostración</button>
          </div>
        </div>
        <ul class="jardin" id="jardin-demo" data-base="">
          {parcelas}
        </ul>
        <p class="demo__resumen" id="demo-resumen" tabindex="-1" aria-live="polite"></p>
        <div class="siguiente aviso" id="demo-siguiente" hidden>
          <p><strong>Tu próxima experiencia.</strong> Cada flor es una ruta distinta. Revisa los lugares y elige qué descubrir en tu próxima visita. <a href="rutas.html">Ver lugares</a></p>
        </div>
      </div>
    </div>
  </section>

  <section class="seccion" aria-labelledby="titulo-estados">
    <div class="contenedor">
      <div class="seccion__cabecera">
        <span class="rotulo">Sistema de florecimiento</span>
        <h2 id="titulo-estados">Cada flor mantiene su lugar.</h2>
        <p>Una flor equivale a una ruta completa e individual. Varias flores no son etapas de una misma ruta.</p>
      </div>
      <ul class="estados">
        <li class="estado"><img src="assets/img/flor-capullo.webp" alt="" width="360" height="404" loading="lazy"><strong>Capullo cerrado</strong><span>Ruta no iniciada</span></li>
        <li class="estado"><img src="assets/img/flor-parcial.webp" alt="" width="360" height="261" loading="lazy"><strong>Apertura parcial</strong><span>Ruta iniciada y aún no completada</span></li>
        <li class="estado"><img src="assets/img/flor-abierta.webp" alt="" width="360" height="261" loading="lazy"><strong>Flor abierta</strong><span>Ruta completada según el método de validación definido</span></li>
        <li class="estado"><img src="assets/img/flor-beneficio.webp" alt="" width="360" height="339" loading="lazy"><strong>Beneficio señalado</strong><span>Solo si existe un acuerdo local. La flor sigue abierta después de un canje.</span></li>
      </ul>
    </div>
  </section>

  <section class="seccion seccion--papel2" id="pasaporte" aria-labelledby="titulo-pasaporte">
    <div class="contenedor pasaporte">
      <img src="assets/img/pasaporte-khiska.webp" alt="Tarjeta vertical ilustrada del Pasaporte Khiska con un cactus en flor, espacio para código QR y progreso de rutas" width="600" height="894" loading="lazy">
      <div>
        <span class="rotulo">Pasaporte Khiska</span>
        <h2 id="titulo-pasaporte">Tu progreso es privado.</h2>
        <p>El Pasaporte conecta tu perfil con la experiencia en terreno: muestra las rutas completadas y lo que te queda por descubrir. Sin rankings ni comparaciones.</p>
        <p>También se propone una versión en papel para quienes no usan smartphone.</p>
        <p><span class="pendiente">En diseño</span></p>
        <img class="ilustracion decorativa sello-mini" src="assets/img/sello-ruta-completada.webp" alt="" width="140" height="140" loading="lazy">
      </div>
    </div>
  </section>

  <section class="seccion" id="estado" aria-labelledby="titulo-estado">
    <div class="contenedor estrecho">
      <span class="rotulo">Transparencia</span>
      <h2 id="titulo-estado">Qué está disponible hoy</h2>
      <table class="tabla-ficha">
        <caption class="visually-hidden">Estado de cada componente de Khiska</caption>
        <tbody>
          <tr><th scope="row">Lugares y fichas</th><td>Disponibles como referentes territoriales. Rutas por validar.</td></tr>
          <tr><th scope="row">Cactus Mi Khiska</th><td>Demostración con rutas de ejemplo.</td></tr>
          <tr><th scope="row">Registro de usuario</th><td><span class="pendiente">No disponible</span> Las rutas se pueden consultar sin registrarse.</td></tr>
          <tr><th scope="row">QR en hitos y validación de ruta</th><td><span class="pendiente">Por definir</span> Escanear un QR no equivale a completar una ruta.</td></tr>
          <tr><th scope="row">Beneficios y comercios</th><td><span class="pendiente">Sin acuerdos</span> Solo se publicarán con acuerdos confirmados.</td></tr>
          <tr><th scope="row">Apple Wallet / Google Wallet</th><td><span class="pendiente">Proyectado</span> No operativo.</td></tr>
        </tbody>
      </table>
      <p class="mt-2"><a class="btn" href="rutas.html">Descubre las rutas</a></p>
    </div>
  </section>
</main>
'''
    write('experiencia-khiska.html', head('Experiencia Khiska: una ruta, una flor · El Quisco', desc, R, '', '') + body + footer(R))

def privacidad():
    R = ''
    desc = 'Uso y privacidad del sitio El Quisco · Experiencia Khiska: qué datos se guardan en tu navegador y qué no recopilamos.'
    body = f'''{header(R, "")}
<main id="contenido">
  <div class="contenedor estrecho pb-4">
    <nav class="migas" aria-label="Ruta de navegación"><ol><li><a href="index.html">Inicio</a></li><li aria-current="page">Uso y privacidad</li></ol></nav>
    <header class="cabecera-pagina"><h1>Uso y privacidad</h1><p>Última revisión: noviembre de 2026.</p></header>
    <h2>Qué guarda este sitio</h2>
    <p>El sitio no usa cookies, analítica ni servicios externos. Solo guarda en tu propio navegador (almacenamiento local):</p>
    <ul>
      <li>Si activaste el modo de lectura fácil.</li>
      <li>La dimensión que elegiste en “Pincha tu curiosidad”.</li>
      <li>El avance de la demostración de Mi Khiska.</li>
    </ul>
    <p>Esa información no sale de tu dispositivo. Puedes borrarla limpiando los datos del sitio en tu navegador o con el botón “Reiniciar demostración”.</p>
    <h2>Formulario “Propón un lugar”</h2>
    <p>Por ahora el formulario <strong>no envía información</strong>: el servicio de recepción aún no está configurado. Cuando se habilite, esta página indicará quién recibe las propuestas, para qué se usan y cómo pedir su eliminación.</p>
    <p><span class="pendiente">Responsable del tratamiento por confirmar</span></p>
    <h2>Contenido</h2>
    <p>Las imágenes de lugares son ilustraciones inspiradas en el territorio. Las rutas, el Pasaporte, los QR, los beneficios y Wallet son propuestas en validación.</p>
  </div>
</main>
'''
    write('privacidad.html', head('Uso y privacidad · El Quisco · Experiencia Khiska', desc, R, '', '') + body + footer(R))

def write(path, s):
    with open(OUT + path, 'w', encoding='utf-8') as f: f.write(s)
    print('ok', path)

index(); rutas(); fichas(); khiska(); privacidad()
