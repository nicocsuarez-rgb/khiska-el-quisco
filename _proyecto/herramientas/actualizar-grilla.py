# Actualiza la grilla de El Quisco: copys, audiencias por persona, destinos del portal/app,
# formatos producibles sin grabar, guiones de video y guía de estilo basada en el reel.
import openpyxl, copy
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

SRC = 'original.xlsx'
OUT = 'GRILLA_EL_QUISCO_KHISKA_v2.xlsx'
wb = openpyxl.load_workbook(SRC)
ws = wb['Grilla']

H = {c.value: c.column for c in ws[4]}
P_CAM, P_HAB, P_HEC, P_VAL, P_ROS = 'Camila (escapada)', 'Visitante habitual', 'Don Héctor (vecino mayor)', 'Vale (joven local)', 'Rosa (oficios)'
HT = '#ElQuisco #DondeLaNaturalezaTieneNombre'

# fila -> cambios. G = guion de video (hoja "Guiones de video"); Prod = cómo se produce
R = {
5:  dict(Formato='Reel manifiesto', Audiencia=P_CAM,
         Copy='¿Creías que El Quisco era solo verano? Detrás de su playa hay humedales, quebradas, oficios y relatos que todavía no conoces por su nombre. El Quisco lleva el nombre de un cactus que crece frente al mar. Pincha tu curiosidad.',
         CTA='Explora en el link de la bio', Destino='Portal · Inicio', KPI='Clics al portal',
         Prod='Video sin grabar: ilustraciones de los lugares + textos animados + música', G='V01'),
6:  dict(Audiencia=f'{P_HAB} · {P_HEC}',
         Copy='Mar, humedal, quebradas, memoria y sabores de caleta. El Quisco es mucho más que su playa de verano. ¿Cuál de estas dimensiones ya conoces y cuál te falta descubrir? Cuéntanos en los comentarios.',
         CTA='Comenta tu dimensión', Destino='Portal · Lugares', Estado='Listo',
         Prod='Carrusel 5 láminas (ya diseñado, 1080×1350)'),
7:  dict(Audiencia=f'{P_VAL} · {P_CAM}',
         Copy='Tres cosas que quizás no sabías de El Quisco: 1) se llama así por el quisco, un cactus de nuestra costa; 2) "quisco" viene del quechua y significa espina; 3) el Humedal El Batro es humedal urbano reconocido desde 2025. Hay más por descubrir.',
         CTA='Descubre más en el link', Destino='Portal · Lugares', KPI='Retención 3 s y reproducciones completas',
         Prod='Video sin grabar: 3 tarjetas con dato + fuente en pantalla', G='V02'),
8:  dict(Audiencia='Todas las personas',
         Copy='El Quisco se llama así por el quisco, el cactus de nuestra costa, y "quisco" viene del quechua: espina. De ahí nace Khiska, tu propio cactus: cada ruta que completas abre una de sus flores. Desliza y descubre cómo funciona.',
         CTA='Conoce Khiska', Destino='Portal · Khiska',
         Prod='Carrusel 5 láminas: origen del nombre → cactus → 1 ruta = 1 flor'),
9:  dict(Formato='Video ilustrado 1–2 min', Audiencia=f'{P_HAB} · {P_CAM}',
         Copy='Una comuna que lleva el nombre de una planta. En dos minutos te contamos de dónde viene el nombre de El Quisco: el cactus que crece frente al mar y la palabra quechua que significa espina. Con fuentes, para que lo cuentes tú también.',
         CTA='Ver más en el portal', Destino='Portal · Khiska', KPI='Tiempo de reproducción',
         Prod='Video sin grabar con narrador IA (no vecino) + ilustraciones + fuentes en pantalla', G='V03'),
10: dict(Audiencia=f'{P_HEC} · {P_VAL}',
         Copy='Hay lugares que solo conocen quienes viven aquí. ¿Qué rincón de El Quisco debería ser parte de una ruta Khiska? Déjalo en los comentarios o súmalo en «Propón un lugar» en nuestro portal.',
         CTA='Propón un lugar', Destino='Portal · Propón un lugar',
         Prod='Gráfica única con ilustración + pregunta'),
11: dict(Audiencia=f'{P_CAM} · {P_HAB}',
         Copy='¿Creías que El Quisco era solo verano? Ahora puedes explorarlo desde un solo lugar: eliges tu ruta sin crear cuenta ni descargar apps, cada ruta abre una flor en tu Khiska y tu Pasaporte guarda tu progreso. ¿Qué parte de El Quisco quieres descubrir?',
         CTA='Explora en el link de la bio', Destino='Portal · Inicio', KPI='Sesiones en el portal', Estado='Listo',
         Link='assets/video/reel-el-quisco-no-termina-en-la-playa.mp4',
         Prod='YA PRODUCIDO: reel de 38 s (es la referencia de estilo para todos los videos)', G='V00'),
12: dict(Formato='Video de pantalla', Audiencia=P_VAL,
         Copy='Así eliges una ruta en menos de un minuto: abres el portal, eliges lo que te da curiosidad, abres la ficha y listo. Sin crear cuenta.',
         CTA='Elige tu ruta', Destino='App · P3 Rutas', KPI='Clics a rutas',
         Prod='Grabación de pantalla de la app (P1→P3→P4) en marco de navegador', G='V04'),
13: dict(Audiencia='Todas las personas',
         Copy='¿Qué te gustaría descubrir primero en El Quisco? Acantilados y mar · Humedal y bosque nativo · Memoria y sabores. Tu respuesta nos ayuda a elegir la primera ruta.',
         CTA='Votar', Destino='Stories',
         Prod='Story con encuesta; opciones = las 3 dimensiones del portal'),
14: dict(Audiencia=f'{P_CAM} · {P_HAB}',
         Copy='No son lugares sueltos: son formas de recorrer El Quisco. Acantilados y mar profundo, humedal y bosque nativo, memoria y sabores. Elige la que te da más curiosidad. Guarda este post para tu próxima escapada.',
         CTA='Guárdalo y elige', Destino='Portal · Lugares',
         Prod='Carrusel 4 láminas con las ilustraciones de cada dimensión'),
15: dict(Audiencia=f'{P_HEC} · {P_ROS}',
         Copy='Ayúdanos a reconocer estos lugares. ¿Sabes cómo se llaman, qué historia tienen o quién los cuida? La memoria de quienes viven aquí es parte de cada ruta.',
         CTA='Comenta lo que sabes', Destino='Publicación',
         Prod='Álbum con las ilustraciones de lugares (sin afirmar datos)'),
16: dict(Formato='Short narrado', Audiencia=f'{P_HEC} · {P_CAM}',
         Copy='Este lugar también se entiende escuchando. El Humedal El Batro: un humedal urbano reconocido en 2025, donde la visita se hace con cuidado. Escúchalo antes de ir.',
         CTA='Conoce el humedal', Destino='Portal · Ficha El Batro', KPI='Retención',
         Prod='Video sin grabar: ilustración del humedal + narrador IA neutro + subtítulos', G='V05'),
17: dict(Audiencia=f'{P_CAM} · {P_VAL}',
         Copy='Una ruta. Una flor. En tu Khiska, cada ruta que completes abrirá una flor de tu cactus. ¿Cuántas flores vas a abrir?',
         CTA='Descubre cómo funciona', Destino='Portal · Khiska',
         Hashtags=f'{HT} #HazFlorecerTuKhiska #Khiska',
         Prod='Video sin grabar: capullo que se abre sobre el cactus (animación de estados)', G='V06'),
18: dict(Audiencia=f'{P_CAM} · {P_HAB}',
         Copy='Elige, prepara y comienza. 1) Elige tu ruta en el portal. 2) Revisa su ficha: puedes imprimirla. 3) Sal a vivirla. Cuando la completes, su flor se abre en tu Khiska.',
         CTA='Comienza tu ruta', Destino='App · P4 Ficha', KPI='Rutas iniciadas',
         Prod='Grabación de pantalla de la app (P3→P4→P5) con pasos numerados, igual que el reel', G='V07'),
19: dict(Audiencia=P_VAL,
         Copy='POV: elegiste no quedarte solo en la playa. Abres la ficha, sigues el sendero y El Quisco empieza a contarte su historia.',
         CTA='Elige tu ruta', Destino='App · P3 Rutas', KPI='Reproducciones completas',
         Prod='Video sin grabar: ilustraciones en primera persona + app en el celular', G='V08'),
20: dict(Audiencia=f'{P_HEC} · {P_CAM}',
         Copy='Antes de salir: revisa la ficha de tu ruta, lleva agua y ropa cómoda, mira el pronóstico, respeta los senderos y sigue el código del visitante Khiska. Si no tienes buena señal, imprime la ficha.',
         CTA='Prepara tu visita', Destino='App · P4 Ficha',
         Prod='Carrusel/guía con íconos de la campaña'),
21: dict(Objetivo='Mostrar Mi Khiska', Audiencia='Todas las personas',
         Copy='Tu recorrido también puede quedar guardado. En Mi Khiska ves tu cactus, las flores que abriste y lo que te falta. Y si prefieres papel, tienes el Pasaporte Khiska.',
         CTA='Mira Mi Khiska', Destino='App · P7 Mi Khiska', KPI='Visitas a Mi Khiska',
         Prod='Carrusel con capturas de Mi Khiska y el Pasaporte'),
22: dict(Objetivo='Mostrar el Pasaporte', Audiencia=f'{P_HEC} · {P_CAM}',
         Copy='Tu Pasaporte Khiska guarda cada ruta que completas: un sello por recorrido. En tu celular o en papel.',
         CTA='Ver Pasaporte', Destino='Portal · Khiska',
         Prod='Módulo del portal (paso 2 del plan)'),
23: dict(Audiencia='Todas las personas',
         Copy='¿Qué estás mirando? Pista: es un cactus de nuestra costa y le dio su nombre a esta comuna.',
         CTA='Responder', Destino='Stories',
         Prod='Story quiz con la ilustración del quisco'),
24: dict(Audiencia=f'{P_CAM} · {P_HEC}',
         Copy='El territorio también te puede hablar. En los puntos de la ruta, un código abre el relato del lugar. Escanear te acompaña; completar la ruta es lo que abre la flor de tu Khiska.',
         CTA='Mira cómo funciona', Destino='App · P5 En ruta', KPI='Visitas a P5',
         Prod='Video sin grabar: QR ilustrado → pantalla P5 de la app → flor', G='V09'),
25: dict(Audiencia=f'{P_HEC} · {P_CAM}',
         Copy='Te invitamos a vivir la primera ruta Khiska junto al equipo y vecinos de El Quisco. Inscríbete en el evento para recibir la fecha y el punto de encuentro.',
         CTA='Inscríbete', Destino='Portal · Agenda',
         Prod='Evento de Facebook. Publicar SOLO si la ruta piloto está confirmada con la municipalidad'),
26: dict(Formato='Video ilustrado 1–2 min', Nombre='“Cómo funciona una ruta Khiska, paso a paso”', Audiencia=f'{P_CAM} · {P_HAB}',
         Copy='Cómo funciona una ruta Khiska, paso a paso: eliges, preparas, recorres y abres tu flor. Todo desde el celular y sin crear cuenta.',
         CTA='Planifica tu visita', Destino='App · P3 Rutas', KPI='Tiempo de reproducción',
         Prod='Video sin grabar: recorrido completo por la app P1→P7 con narrador IA', G='V10'),
27: dict(Objetivo='Mostrar la experiencia completa', Formato='Carrusel ilustrado', Nombre='“El fin de semana de Camila”', Pilar='Experiencia y retorno', Audiencia=P_CAM,
         Copy='Camila quería una escapada fuera del verano. Abrió el portal, eligió una ruta, la recorrió y volvió con una flor nueva en su Khiska. ¿Y tú, qué vas a descubrir?',
         CTA='Haz tu ruta', Destino='Portal · Lugares',
         Prod='Carrusel 6 láminas: historia de Camila como personaje ilustrado (no testimonio real)'),
28: dict(Audiencia=P_VAL,
         Copy='Llegué con curiosidad, me fui con una flor. Una ruta, un recorrido completo, una flor nueva en mi Khiska.',
         CTA='Comienza tu ruta', Destino='App · P6 Completar',
         Prod='Video sin grabar: antes/después capullo → flor abierta, POV ilustrado', G='V11'),
29: dict(Audiencia=f'{P_ROS} · {P_CAM}',
         Copy='Una ruta también puede terminar en una mesa. En la caleta, el oficio de quienes salen al mar se convierte en sabor. Memoria y sabores: una de las formas de recorrer El Quisco.',
         CTA='Conoce Memoria y sabores', Destino='Portal · Ficha La caleta', KPI='Clics a la ficha',
         Prod='Post con la ilustración de la caleta (sin nombrar locales sin acuerdo)'),
30: dict(Objetivo='Anticipar el mes siguiente', Nombre='“Lo que viene en septiembre”', Audiencia=f'{P_HAB} · {P_HEC}',
         Copy='Agosto fue el mes de empezar a recorrer. En septiembre, El Quisco sigue: nuevas razones para volver fuera del verano, en la agenda del portal.',
         CTA='Ver agenda', Destino='Portal · Agenda', KPI='Visitas a la agenda',
         Prod='Gráfica con calendario ilustrado (sin cifras inventadas)'),
31: dict(Audiencia=f'{P_CAM} · {P_VAL}',
         Copy='Una ruta completada hace florecer tu Khiska. La flor no es un premio: es la memoria visible de lo que viviste en El Quisco.',
         CTA='Mira Mi Khiska', Destino='App · P7 Mi Khiska', KPI='Visitas a Mi Khiska',
         Hashtags=f'{HT} #HazFlorecerTuKhiska #Khiska',
         Prod='Video sin grabar: cactus con capullos → flor que se abre (cumple las 3 reglas de lenguaje)', G='V12'),
32: dict(Objetivo='Dar razones para volver', Formato='Carrusel', Nombre='“¿Por qué volver fuera del verano?”', Pilar='Experiencia y retorno', Audiencia=f'{P_HAB} · {P_CAM}',
         Copy='Hay lugares que se visitan una vez y otros a los que se vuelve. Fuera del verano, El Quisco tiene humedal, acantilados, memoria y sabores esperando. Y tu Khiska todavía tiene capullos por abrir.',
         CTA='Elige tu próxima ruta', Destino='App · P8 Próxima experiencia',
         Prod='Carrusel 4 láminas (reemplaza el testimonio: no inventamos testimonios)'),
33: dict(Audiencia=P_VAL,
         Copy='¿Qué ruta harías después? Si te gustó el mar, prueba la memoria; si te gustó el humedal, prueba los acantilados. Cada ruta abre una flor distinta.',
         CTA='Elige tu siguiente ruta', Destino='App · P8 Próxima experiencia',
         Prod='Video sin grabar: respuesta en texto sobre ilustraciones de las 3 dimensiones', G='V13'),
34: dict(Audiencia=f'{P_ROS} · {P_CAM}',
         Copy='Tu experiencia también puede encontrarse con el comercio local. Cuando un local se suma a Khiska, su beneficio aparece señalado junto a tu flor. Revisa en el portal cuáles están disponibles.',
         CTA='Revisa en el portal', Destino='Portal · Khiska', KPI='Clics',
         Prod='Carrusel. Publicar SOLO con acuerdos escritos con comercios'),
35: dict(Audiencia=f'{P_CAM} · {P_HAB}',
         Copy='Te queda una ruta por descubrir. Según las flores que ya abriste, te sugerimos tu próximo recorrido.',
         CTA='Ver próxima ruta', Destino='App · P8 Próxima experiencia',
         Prod='Pantalla P8 de la app'),
36: dict(Audiencia=f'{P_VAL} · {P_CAM}',
         Copy='Tu mirada también forma parte del destino. Comparte tu ruta con #HazFlorecerTuKhiska y una foto de tu cactus: podríamos publicarla en nuestra cuenta (siempre con tu permiso).',
         CTA='Comparte tu ruta', Destino='Instagram',
         Prod='Convocatoria UGC; solo se republica contenido real con autorización'),
37: dict(Formato='Video ilustrado 1–2 min', Nombre='“El Quisco por capas”', Audiencia=f'{P_HAB} · {P_HEC}',
         Copy='El Quisco por capas: acantilados y mar profundo, humedal y bosque nativo, memoria y sabores. Un recorrido ilustrado por lo que hace de El Quisco un lugar con nombre propio.',
         CTA='Explora el portal', Destino='Portal · Lugares', KPI='Tiempo de reproducción',
         Prod='Video sin grabar: las 6 ilustraciones de lugares + narrador IA + música', G='V14'),
38: dict(Audiencia=f'{P_HAB} · {P_HEC}',
         Copy='Septiembre todavía tiene rutas para ti. Revisa la agenda del mes en el portal y planifica tu escapada fuera del verano.',
         CTA='Ver agenda', Destino='Portal · Agenda',
         Prod='Gráfica con fondo de agenda (solo actividades confirmadas)'),
39: dict(Audiencia=P_VAL,
         Copy='Tres razones para volver a El Quisco: 1) una ruta nueva por recorrer; 2) una agenda que sigue fuera del verano; 3) un cactus que todavía tiene capullos por abrir.',
         CTA='Planifica tu regreso', Destino='Portal · Inicio',
         Prod='Video sin grabar: 3 tarjetas numeradas, mismo estilo que V02', G='V15'),
40: dict(Audiencia='Todas las personas',
         Copy='El jardín puede seguir creciendo. Cada ruta abre una flor distinta, y tu cactus todavía tiene capullos. ¿Qué parte de El Quisco quieres descubrir ahora?',
         CTA='Explora en el link de la bio', Destino='Portal · Inicio', KPI='Visitas recurrentes',
         Hashtags=f'{HT} #HazFlorecerTuKhiska #Khiska',
         Prod='Video sin grabar: cactus completo florecido + cierre de campaña', G='V16'),
41: dict(Audiencia=f'{P_CAM} · {P_HAB}',
         Copy='Tu experiencia hasta ahora: rutas recorridas, flores abiertas y sellos en tu Pasaporte. Lo que falta, también está aquí.',
         CTA='Sigue explorando', Destino='App · P7 Mi Khiska',
         Prod='Pantalla P7 de la app'),
42: dict(Audiencia='Todas las personas',
         Copy='¿Qué ruta te gustaría que se abriera después? Elige la próxima ruta, el tipo de contenido o el evento que te gustaría ver en El Quisco.',
         CTA='Responder encuesta', Destino='Stories',
         Prod='Story con encuesta (ya en diseño)'),
43: dict(Objetivo='Proyectar lo que viene', Nombre='“Lo que viene para Khiska”', Audiencia=f'{P_HEC} · {P_HAB}',
         Copy='Gracias a quienes recorrieron, propusieron lugares y compartieron su mirada. Lo que viene: más rutas, nuevos relatos y un Khiska que otras comunas también puedan vivir. El Quisco todavía tiene nombres por descubrir.',
         CTA='Sigue explorando', Destino='Portal · Inicio', KPI='Alcance',
         Prod='Carrusel con las fases futuras (sin cifras de resultados inventadas)'),
}

# Columnas nuevas T, U
hdr_style = ws['S4']; body_style = ws['R5']
for col, title, width in [(20, 'Cómo se produce', 46), (21, 'Guion', 9)]:
    c = ws.cell(4, col, title)
    c.font = copy.copy(hdr_style.font); c.fill = copy.copy(hdr_style.fill); c.alignment = copy.copy(hdr_style.alignment); c.border = copy.copy(hdr_style.border)
    ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = width
key = {'Formato': 'Formato', 'Nombre': 'Nombre de la pieza', 'Copy': 'Copy', 'CTA': 'CTA', 'Destino': 'Destino', 'KPI': 'KPI',
       'Audiencia': 'Audiencia', 'Hashtags': 'Hashtags', 'Estado': 'Estado', 'Link': 'Link de archivo', 'Pilar': 'Pilar', 'Objetivo': 'Objetivo'}
for row, ch in R.items():
    for k, v in ch.items():
        if k in key: ws.cell(row, H[key[k]], v)
    for col, val in [(20, ch.get('Prod', '')), (21, ch.get('G', ''))]:
        c = ws.cell(row, col, val)
        c.font = copy.copy(body_style.font); c.alignment = copy.copy(body_style.alignment); c.border = copy.copy(body_style.border)
    s = ws.cell(row, H['Link de archivo']); s.font = copy.copy(body_style.font); s.alignment = copy.copy(body_style.alignment)
ws.cell(2, 1).value = ('Cómo usarla: una fila por publicación. Escribe la fecha como 15/07/2027; Día, Mes y Fase se calculan solos. '
                       'Audiencia = nuestras personas (Camila, visitante habitual, Don Héctor, Vale, Rosa). Destino = sección del portal o pantalla de la app. '
                       'Los videos tienen su guion en la pestaña "Guiones de video" y siguen la pestaña "Estilo de video".')

# ---------- Estilos para hojas nuevas ----------
VERDE = PatternFill('solid', fgColor='FF3F6B3A'); PAPEL = PatternFill('solid', fgColor='FFF8F5EC')
F_T = Font(name='Arial', size=15, bold=True, color='FF1E2A1D'); F_H = Font(name='Arial', size=10, bold=True, color='FFFFFFFF')
F_B = Font(name='Arial', size=10, color='FF1E2A1D'); F_BB = Font(name='Arial', size=10, bold=True, color='FF1E2A1D')
thin = Side(style='thin', color='FFD9D1BD'); BRD = Border(top=thin, bottom=thin, left=thin, right=thin)
WRAP = Alignment(wrap_text=True, vertical='top')

def tabla(sh, titulo, sub, cols, filas, fila0=4):
    sh['A1'] = titulo; sh['A1'].font = F_T
    sh['A2'] = sub; sh['A2'].font = Font(name='Arial', size=10, italic=True, color='FF4B5A48')
    for i, (n, w) in enumerate(cols, 1):
        c = sh.cell(fila0, i, n); c.font = F_H; c.fill = VERDE; c.alignment = WRAP
        sh.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    for r, fila in enumerate(filas, fila0 + 1):
        for i, v in enumerate(fila, 1):
            c = sh.cell(r, i, v); c.font = F_BB if i == 1 else F_B; c.alignment = WRAP; c.border = BRD
    sh.freeze_panes = sh.cell(fila0 + 1, 2)
    sh.sheet_view.showGridLines = False

# ---------- Estilo de video ----------
est = wb.create_sheet('Estilo de video')
tabla(est, 'Estilo de video · basado en el reel ya producido',
      'Referencia: assets/video/reel-el-quisco-no-termina-en-la-playa.mp4 (38 s). Todos los videos nuevos se ven y suenan como él.',
      [('Elemento', 22), ('Cómo es en el reel', 62), ('Regla para los videos nuevos', 62)],
      [
       ('Formato', '1080×1920, 38 s, vertical.', 'Reels/TikTok/Shorts: 1080×1920, 20–40 s. YouTube ilustrado: 1920×1080, 1–2 min.'),
       ('Fondo', 'Papel liso claro, sin texturas fuertes.', 'Siempre fondo papel (#FAF7EE / #F3EEE1). Nada de fotos de stock ni fondos oscuros.'),
       ('Apertura (0–3 s)', 'Pequeño cactus ilustrado + pregunta: "¿Creías que El Quisco era solo verano?", con subrayado amarillo a mano.', 'Abrir siempre con una pregunta o dato que pinche la curiosidad, + una ilustración de la campaña. Máx. 8 palabras.'),
       ('Cuerpo', 'Pantallas reales del sitio dentro de una ventana de navegador con sombra suave. Rótulo tipo etiqueta de papel arriba.', 'Mostrar el portal o la app reales (capturas o grabación de pantalla) en el mismo marco. Nunca pantallas inventadas.'),
       ('Pasos', 'Numerados: "1. Elige tu ruta · Sin crear cuenta ni apps", "2. Una ruta, una flor", "3. Tu Pasaporte · Progreso privado, sin rankings".', 'Máximo 3 pasos por video, numerados, con titular corto + subtítulo de 4–6 palabras.'),
       ('Flor', 'Estados capullo → apertura parcial → flor abierta como íconos bajo la pantalla.', 'Usar siempre las ilustraciones oficiales de los estados. Una flor = una ruta.'),
       ('Cierre', 'Logo El Quisco + flor abierta + "¿Qué parte de El Quisco quieres descubrir?" + botón rosa "EXPLORA EN EL LINK DE LA BIO".', 'Mismo cierre en todos los videos (2–3 s). En YouTube: "Explora en el portal" + URL.'),
       ('Tipografía', 'Rubik bold para titulares, Rubik Mono One en el botón/rótulos, serif en la pregunta final.', 'Igual. Textos en pantalla grandes y legibles en celular.'),
       ('Audio', 'Música instrumental suave, sin voz.', 'Música instrumental. Si hay narración: voz IA neutra de narrador, con subtítulos. Nunca presentarla como un vecino o testimonio real.'),
       ('Ritmo', 'Cortes y fundidos suaves; cada pantalla 2–4 s.', 'Sin efectos 3D, zooms bruscos ni transiciones llamativas.'),
       ('Lenguaje', 'Cercano y claro: pregunta → cómo funciona → invitación.', '"Haz florecer tu Khiska" solo con el cactus en pantalla; "florecer" nunca dirigido a la persona. No mostrar rótulos de "demo" en piezas de campaña.'),
       ('Datos', '—', 'Todo dato en pantalla lleva su fuente pequeña abajo (ej. "Fuente: RAE"). Si no hay fuente, no va.'),
      ])

# ---------- Guiones de video ----------
gs = wb.create_sheet('Guiones de video')
G = [
 ('V00', '15/07/2027', 'Instagram · Reel', '“Ahora El Quisco se puede explorar desde un solo lugar”', '38 s',
  '¿Creías que El Quisco era solo verano?',
  'Portal en navegador → "Pincha tu curiosidad" → 1. Elige tu ruta · Sin crear cuenta ni apps → 2. Una ruta, una flor (estados) → 3. Tu Pasaporte · Progreso privado, sin rankings',
  'Logo + flor + ¿Qué parte de El Quisco quieres descubrir? + EXPLORA EN EL LINK DE LA BIO', 'Música', 'Ya producido', 'Listo'),
 ('V01', '01/07/2027', 'Instagram · Reel manifiesto', '“El Quisco no termina en la playa”', '30 s',
  '¿Creías que El Quisco era solo verano?',
  'Playa ilustrada se "desliza" y aparecen por capas: humedal (El Batro) → quebrada (Las Petras) → mirador (Neptuno) → caleta. Cartel en cada una: "Humedal", "Quebrada", "Mirador", "Caleta". Luego: cactus quisco + "El Quisco lleva el nombre de un cactus" → "Pincha tu curiosidad."',
  'Cierre estándar', 'Música', 'assets/img/territorio-*.webp, cactus-khiska-tres-flores.webp, logo-el-quisco.webp', 'Por producir'),
 ('V02', '05/07/2027', 'TikTok', '“Tres cosas que quizás no sabías de El Quisco”', '20 s',
  'Tres cosas que quizás no sabías de El Quisco',
  '1. Se llama así por un cactus: el quisco (ilustración del cactus). 2. "Quisco" viene del quechua y significa espina (Fuente: RAE, entrada «quisca»). 3. El Humedal El Batro es humedal urbano reconocido desde 2025 (Fuente: MMA, Res. Ex. 6.648).',
  'Hay más por descubrir + cierre estándar', 'Música', 'cactus-nativo/ilustraciones, territorio-el-batro.webp', 'Por producir'),
 ('V03', '10/07/2027', 'YouTube', '“Una tierra con nombre propio”', '1:30 min (16:9)',
  'Una comuna que lleva el nombre de una planta.',
  'Narrador IA: el quisco (Echinopsis chiloensis) en la costa → la palabra: quichca (1608), quisca (Lenz), kiska, khiska → "espina" → de ahí Khiska: tu cactus → una ruta, una flor → invitación al portal. Fuentes en pantalla en cada dato.',
  'Explora en el portal + URL', 'Narrador IA + música + subtítulos', 'Dossier (sección Origen) como guion de fuentes', 'Por producir'),
 ('V04', '17/07/2027', 'TikTok', '“Así eliges una ruta en menos de un minuto”', '25 s',
  'Así eliges una ruta en menos de un minuto',
  'Grabación real de la app: P1 Inicio → P2 intereses (toque) → P3 Rutas → P4 Ficha. Contador en pantalla 0:00 → 0:45. Pasos: 1. Elige lo que te da curiosidad · 2. Abre la ficha · 3. Listo, sin crear cuenta.',
  'Cierre estándar', 'Música', 'app/index.html', 'Por producir'),
 ('V05', '26/07/2027', 'YouTube Shorts', '“Este lugar también se entiende escuchando”', '30 s',
  'Este lugar también se entiende escuchando.',
  'Ilustración del humedal con leve movimiento → narrador IA: humedal urbano reconocido en 2025; se visita con cuidado; respeta los senderos. Subtítulos grandes.',
  'Conoce el humedal en el portal + cierre', 'Narrador IA + sonido ambiente', 'territorio-el-batro.webp', 'Por producir'),
 ('V06', '29/07/2027', 'Instagram · Reel teaser', '“Tu curiosidad puede hacer florecer una experiencia”', '15 s',
  'Una ruta. Una flor.',
  'Cactus con capullos → un capullo pasa a apertura parcial → flor abierta. Texto: "En tu Khiska, cada ruta completada abre una flor." → "¿Cuántas flores vas a abrir?"',
  'Cierre estándar', 'Música', 'flor-capullo/parcial/abierta.webp, cactus-khiska-una-flor.webp', 'Por producir'),
 ('V07', '01/08/2027', 'Instagram · Reel tutorial', '“Elige, prepara y comienza”', '30 s',
  'Elige, prepara y comienza.',
  'Mismo formato que V00: 1. Elige · catálogo de rutas → 2. Prepara · ficha imprimible → 3. Comienza · pantalla En ruta. Final: cactus con flor abriéndose + "Haz florecer tu Khiska".',
  'Cierre estándar', 'Música', 'app P3, P4, P5', 'Por producir'),
 ('V08', '03/08/2027', 'TikTok · POV', '“POV: elegiste no quedarte solo en la playa”', '20 s',
  'POV: elegiste no quedarte solo en la playa',
  'Mano ilustrada con celular mostrando la ficha → ilustración de sendero hacia la quebrada → "El Quisco empieza a contarte su historia".',
  'Cierre estándar', 'Música', 'sendero-ilustrado.webp, territorio-las-petras.webp', 'Por producir'),
 ('V09', '15/08/2027', 'Instagram · Reel', '“El territorio también te puede hablar”', '25 s',
  'El territorio también te puede hablar.',
  'Ilustración de un punto con código → pantalla P5 En ruta con relato → texto: "Escanear te acompaña" → "Completar la ruta abre tu flor" + flor.',
  'Cierre estándar', 'Música', 'app P5, icono-ubicacion.webp', 'Por producir'),
 ('V10', '19/08/2027', 'YouTube', '“Cómo funciona una ruta Khiska, paso a paso”', '1:30 min (16:9)',
  'Cómo funciona una ruta Khiska',
  'Narrador IA guía la app completa: P1 → P2 → P3 → P4 (imprimir) → P5 → P6 flor → P7 Mi Khiska → P9 lectura fácil (para quien lo necesite).',
  'Explora en el portal + URL', 'Narrador IA + música + subtítulos', 'app/index.html', 'Por producir'),
 ('V11', '24/08/2027', 'TikTok · Transformación', '“Llegué con curiosidad, me fui con una flor”', '15 s',
  'Llegué con curiosidad…',
  'Antes: capullo cerrado ("Llegué con curiosidad") → corte → Después: flor abierta en el cactus ("…me fui con una flor").',
  'Cierre estándar', 'Música', 'flor-capullo.webp, flor-abierta.webp', 'Por producir'),
 ('V12', '01/09/2027', 'Instagram · Reel', '“Una ruta completada hace florecer tu Khiska”', '20 s',
  'Una ruta completada…',
  'Cactus en pantalla desde el inicio → la flor se abre lentamente → "…hace florecer tu Khiska." → "La flor no es un premio: es la memoria de lo que viviste." → Mi Khiska en la app.',
  'Cierre estándar', 'Música', 'cactus-khiska-una-flor.webp, flor-*.webp, app P7', 'Por producir'),
 ('V13', '05/09/2027', 'TikTok · Respuesta', '“¿Qué ruta harías después?”', '20 s',
  '¿Qué ruta harías después?',
  'Burbuja de pregunta → 3 tarjetas: "¿Te gustó el mar? → Memoria y sabores", "¿Te gustó el humedal? → Acantilados", "¿Te gustó la caleta? → Humedal". Cada ruta abre una flor distinta.',
  'Cierre estándar', 'Música', 'ilustraciones de dimensiones', 'Por producir'),
 ('V14', '15/09/2027', 'YouTube', '“El Quisco por capas”', '2 min (16:9)',
  'El Quisco por capas',
  'Narrador IA recorre las 3 dimensiones con las 6 ilustraciones de lugares; solo datos con fuente (El Batro 2025, Litoral de los Poetas).',
  'Explora en el portal + URL', 'Narrador IA + música + subtítulos', 'territorio-*.webp', 'Por producir'),
 ('V15', '19/09/2027', 'TikTok', '“Tres razones para volver a El Quisco”', '20 s',
  'Tres razones para volver',
  'Mismo formato que V02: 1. Una ruta nueva por recorrer · 2. Una agenda fuera del verano · 3. Un cactus con capullos por abrir.',
  'Cierre estándar', 'Música', 'fondo-agenda.webp, cactus', 'Por producir'),
 ('V16', '22/09/2027', 'Instagram · Reel cierre', '“El jardín puede seguir creciendo”', '25 s',
  'El jardín puede seguir creciendo.',
  'Cactus con una flor → se suman flores (cada una = una ruta) → cactus completo florecido → "Tu cactus todavía tiene capullos".',
  'Cierre estándar con: "¿Qué parte de El Quisco quieres descubrir ahora?"', 'Música', 'cactus-khiska-florecido.webp', 'Por producir'),
]
tabla(gs, 'Guiones de video', 'Todos siguen la pestaña "Estilo de video". "Cierre estándar" = logo + flor + ¿Qué parte de El Quisco quieres descubrir? + EXPLORA EN EL LINK DE LA BIO.',
      [('Guion', 7), ('Fecha', 11), ('Canal', 18), ('Pieza', 30), ('Duración', 11), ('Gancho (0–3 s)', 28), ('Escenas y textos en pantalla', 70), ('Cierre', 30), ('Audio', 20), ('Recursos', 30), ('Estado', 12)],
      G)

wb.active = wb.sheetnames.index('Grilla')
wb.save(OUT)
print(wb.sheetnames)
