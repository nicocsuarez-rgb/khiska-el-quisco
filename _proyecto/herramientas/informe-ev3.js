const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, AlignmentType, HeadingLevel,
  WidthType, ShadingType, BorderStyle, LevelFormat, PageBreak, Footer, PageNumber, TableLayoutType } = require('docx');
const sizeOf = (f) => { const { execSync } = require('child_process'); const o = execSync(`python3 -c "from PIL import Image;im=Image.open('${f}');print(im.size[0],im.size[1])"`).toString().trim().split(' '); return { w: +o[0], h: +o[1] }; };

const F = 'Calibri', VERDE = '34501F', ROSA = 'A8384A', GRIS = '4A4A42';
const W = 9360; // ancho útil carta con márgenes de 1"
const p = (text, o = {}) => new Paragraph({ spacing: { after: 140, line: 300 }, ...o.par, children: runs(text, o) });
function runs(text, o = {}) {
  // **negrita** simple
  return text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/).filter(Boolean).map(t => t.startsWith('**')
    ? new TextRun({ text: t.slice(2, -2), bold: true, font: F, size: o.size || 23, color: o.color })
    : (t.startsWith('*') && t.endsWith('*') && t.length > 2)
      ? new TextRun({ text: t.slice(1, -1), italics: true, font: F, size: o.size || 23, color: o.color })
      : new TextRun({ text: t, font: F, size: o.size || 23, italics: o.italics, color: o.color }));
}
const h1 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t })] });
const h2 = (t) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t })] });
const acto = (t) => new Paragraph({ spacing: { before: 0, after: 60 }, children: [new TextRun({ text: t.toUpperCase(), font: F, size: 19, bold: true, color: ROSA, characterSpacing: 40 })] });
const cita = (t) => new Paragraph({ spacing: { before: 120, after: 200, line: 300 }, indent: { left: 567 }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: 'EE7F8E', space: 12 } },
  children: [new TextRun({ text: t, font: F, size: 25, italics: true, color: VERDE })] });
const bullet = (t) => new Paragraph({ numbering: { reference: 'vinetas', level: 0 }, spacing: { after: 80, line: 290 }, children: runs(t) });
const brk = () => new Paragraph({ children: [new PageBreak()] });
const img = (f, ancho = W, cap) => {
  const s = sizeOf(f); const wpx = Math.round(ancho / 15); const hpx = Math.round(wpx * s.h / s.w);
  const out = [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: cap ? 40 : 160 },
    children: [new ImageRun({ type: 'jpg', data: fs.readFileSync(f), transformation: { width: wpx, height: hpx } })] })];
  if (cap) out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: cap, font: F, size: 19, italics: true, color: GRIS })] }));
  return out;
};
const borde = { style: BorderStyle.SINGLE, size: 4, color: 'D9D1BD' };
function tabla(cols, filas, opts = {}) {
  const total = cols.reduce((a, c) => a + c[1], 0);
  const anchos = cols.map(c => Math.round(c[1] / total * W));
  anchos[anchos.length - 1] += W - anchos.reduce((a, b) => a + b, 0);
  const celda = (t, i, head) => new TableCell({ width: { size: anchos[i], type: WidthType.DXA },
    borders: { top: borde, bottom: borde, left: borde, right: borde }, margins: { top: 80, bottom: 80, left: 110, right: 110 },
    shading: head ? { type: ShadingType.CLEAR, fill: '3F6B3A', color: 'auto' } : (opts.zebra && opts._r % 2 ? { type: ShadingType.CLEAR, fill: 'F8F5EC', color: 'auto' } : undefined),
    children: String(t).split('\n').map(l => new Paragraph({ spacing: { after: 30, line: 260 }, children: head
      ? [new TextRun({ text: l, bold: true, color: 'FFFFFF', font: F, size: 20 })]
      : runs(l, { size: 20 }) })) });
  const rows = [new TableRow({ tableHeader: true, children: cols.map((c, i) => celda(c[0], i, true)) })];
  filas.forEach((f, r) => { opts._r = r; rows.push(new TableRow({ cantSplit: true, children: f.map((t, i) => celda(t, i, false)) })); });
  return [new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: anchos, layout: TableLayoutType.FIXED, rows }), new Paragraph({ spacing: { after: 160 }, children: [] })];
}
function dosImg(a, b, capA, capB) {
  const cw = W / 2;
  const cell = (f, cap) => { const s = sizeOf(f); const wpx = Math.round((cw - 300) / 15); let hpx = Math.round(wpx * s.h / s.w); let w2 = wpx;
    if (hpx > 330) { hpx = 330; w2 = Math.round(330 * s.w / s.h); }
    return new TableCell({ width: { size: cw, type: WidthType.DXA }, borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({ type: 'jpg', data: fs.readFileSync(f), transformation: { width: w2, height: hpx } })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 60, after: 120 }, children: [new TextRun({ text: cap, font: F, size: 20, bold: true, color: VERDE })] })] }); };
  return [new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [cw, cw], layout: TableLayoutType.FIXED, rows: [new TableRow({ children: [cell(a, capA), cell(b, capB)] })] }), new Paragraph({ children: [] })];
}
const I = (n) => 'img/' + n;

const children = [
  // ---------- Portada ----------
  new Paragraph({ spacing: { before: 2400, after: 120 }, children: [new TextRun({ text: 'KHISKA', font: F, size: 72, bold: true, color: VERDE, characterSpacing: 80 })] }),
  new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: 'El Quisco: donde la naturaleza tiene nombre', font: F, size: 36, color: VERDE })] }),
  new Paragraph({ spacing: { after: 600 }, children: [new TextRun({ text: 'Pincha tu curiosidad.', font: F, size: 28, italics: true, color: ROSA })] }),
  p('**Evaluación Parcial 3 · Innovación Digital**'),
  p('Prototipo, estrategia digital de lanzamiento y viabilidad'),
  p('Agencia C.C.C. · Fernanda Cruz, Benjamín Cerda y Nicolás Cáceres'),
  p('Publicidad · Duoc UC, sede Viña del Mar · Noviembre de 2026'),
  brk(),

  // ---------- Antes de empezar ----------
  acto('Antes de empezar'),
  h1('Una palabra que pincha'),
  p('Todo empezó con una pregunta que parece simple: ¿por qué El Quisco se llama así? La respuesta nos cambió el proyecto.'),
  p('Según la propia Municipalidad, la comuna debe su nombre al **quisco**, el cactus columnar que crece frente al mar en nuestra costa (*Echinopsis chiloensis*). Y la palabra quisco viene del quechua. Aparece como *quichca* en el vocabulario de Diego González Holguín de 1608 y en el Diccionario de la lengua española, en la entrada «quisca»; como *quisca* en el diccionario de voces chilenas de Rodolfo Lenz; como *kiska* en el quechua cusqueño, y como *khiska* o *khichka* en el quechua boliviano. Todas significan lo mismo: **espina**.'),
  p('Ahí entendimos que El Quisco no es una metáfora: lleva, literalmente, el nombre de su naturaleza. Y de esa espina nació **Khiska**, la forma con que escribimos nuestra marca, inspirada en una de las variantes de esa palabra.'),
  cita('Una espina que pincha tu curiosidad, un camino por El Quisco y una flor que guarda lo que viviste.'),
  p('Esa frase es la historia completa de nuestro proyecto, y la contamos en tres actos. Cada parte de este informe, cada pantalla de la app, cada pieza de la campaña y cada soporte en la calle pertenece a uno de ellos:'),
  ...tabla([['Acto', 18], ['Qué le pasa a la persona', 42], ['Fase de la campaña', 20], ['Frase', 30]], [
    ['**1. La espina**', 'Algo la pincha: descubre que El Quisco no termina en la playa.', 'Despertar (julio)', 'Pincha tu curiosidad.'],
    ['**2. El camino**', 'La curiosidad se vuelve una ruta concreta: elige, prepara y recorre.', 'Recorrer (agosto)', 'Elige, prepara y comienza.'],
    ['**3. La flor**', 'Lo vivido queda como memoria visible y como razón para volver.', 'Florecer y volver (septiembre)', 'Una ruta completada hace florecer tu Khiska.'],
  ], { zebra: true }),
  p('La protagonista de esta historia tiene nombre: **Camila**, una visitante que planea una escapada de fin de semana a El Quisco fuera del verano. La acompañaremos en todo el informe.'),
  brk(),

  // ---------- Acto 1 ----------
  acto('Acto 1 · La espina'),
  h1('Lo que descubrimos'),
  h2('Diagnóstico e insight clave'),
  p('El Quisco se llena en febrero y se vacía en invierno. En 2025, la ocupación de alojamientos del Litoral de los Poetas fue de **66,6%** a mediados de febrero y cayó a **30,9%** en las vacaciones de invierno, según Sernatur. Esa caída fue nuestro punto de partida.'),
  ...tabla([['Dato', 38], ['Cifra', 37], ['Fuente', 25]], [
    ['Población de El Quisco', '18.971 habitantes (+18,9% vs. 2017)', 'Censo 2024, INE (BCN 2026)'],
    ['Personas de 65 años o más', '25,1% en la comuna; 14% en el país', 'Censo 2024, INE'],
    ['Ocupación de alojamientos, Litoral de los Poetas', '66,6% en febrero; 30,9% en invierno', 'Sernatur, 2025'],
    ['Empresas de alojamiento y comidas', '296 de 1.701 empresas de la comuna', 'SII 2024 (BCN 2026)'],
    ['Humedal Urbano El Batro', 'Reconocido por el Ministerio del Medio Ambiente', 'Res. Ex. 6.648, 29/09/2025'],
  ], { zebra: true }),
  p('Mirando las redes y los sitios de la comuna nos dimos cuenta de algo injusto: casi todos conocen El Quisco, pero casi nadie lo conoce de verdad. La comunicación muestra lugares, pero no enseña a vivirlos. Una foto del humedal despierta interés, pero no dice qué recorrer, cómo prepararse, cómo guardar lo vivido ni por qué volver en julio.'),
  cita('La curiosidad por El Quisco ya existe; lo que falta es un siguiente paso claro y una razón para volver fuera del verano.'),
  p('Ese es nuestro insight. La segunda mitad la confirman los datos de ocupación. La primera la vamos a medir nosotros desde la primera fase de la campaña, con la encuesta de Stories y con conversaciones breves con visitantes y vecinos.'),

  h2('Categoría y comunidad'),
  p('Khiska compite en la categoría de **turismo de experiencias y pasaportes turísticos**: propuestas que convierten la visita en un recorrido con registro y motivo para volver. Es una categoría viva en Chile. El Servicio Nacional del Patrimonio Cultural lleva su Pasaporte Patrimonial al Día del Patrimonio 2026, y la Corporación Regional de Turismo de Valparaíso usó un pasaporte para el Mundial Sub-20 de 2025. Lo que nadie ha hecho es un pasaporte que nazca del nombre del propio territorio y que una lo digital con lo físico.'),
  p('Diseñamos para cuatro públicos, y a cada uno le pusimos cara. Así quedan conectados con los segmentos que trabajamos en Estrategia de Medios:'),
  ...tabla([['Persona', 20], ['Segmento', 24], ['Lo que necesita', 34], ['Cómo vive lo digital', 22]], [
    ['**Camila** (principal)', 'Escapista urbano y explorador experiencial', 'Saber qué hacer, cuánto toma y cómo empezar, sin crear una cuenta', 'Instagram, TikTok, celular siempre a mano'],
    ['**Visitante habitual**', 'Familias y segunda vivienda', 'Una razón para venir fuera del verano', 'Facebook, sitio web, agenda'],
    ['**Don Héctor**', 'Comunidad: vecino mayor', 'Leer sin esfuerzo y no perderse en menús', 'Uso básico del celular; prefiere papel'],
    ['**Vale**', 'Comunidad: joven local', 'Participar rápido y sentir que su aporte cuenta', 'Nativa digital, Stories y TikTok'],
    ['**Rosa**', 'Oficios y comercio local', 'Ser visible para quien ya está recorriendo', 'WhatsApp e Instagram de su negocio'],
  ], { zebra: true }),
  p('Sobre cómo se conectan: en Chile hay **19,1 millones de usuarios de internet (95,6%)**, y en el último mes el 84,9% usó Instagram, el 80,1% Facebook, el 69,0% YouTube y el 68,8% TikTok (DataReportal, Digital 2027 Chile). El 99,1% de los hogares con internet tiene smartphone, pero el 13,8% de las personas de 60 años o más nunca ha usado internet (Subtel, XII Encuesta de Acceso y Usos de Internet). En una comuna donde uno de cada cuatro vecinos tiene más de 65 años, ese último dato nos obligó a pensar en algo que no fuera solo digital.'),
  p('No existen datos de comportamiento digital medidos solo en El Quisco. Por eso la primera fase de la campaña incluye nuestra propia medición: encuesta en Stories, comentarios y lugares propuestos por la comunidad.'),
  brk(),

  // ---------- Acto 2 ----------
  acto('Acto 2 · El camino'),
  h1('Cómo llegamos a Khiska'),
  h2('Proceso creativo: del papel a la pantalla'),
  p('Antes de abrir cualquier programa, dibujamos. Con plumones y lápices de colores imaginamos cómo tenía que verse la página: el logo de El Quisco arriba, un menú transparente, la frase "Donde la naturaleza tiene nombre", un cactus que te invitaba a "pinchar tu curiosidad" y, en una esquina, un guiño que todavía nos hace reír: **"Sácate la espina"**.'),
  ...img(I('bocetos-conjunto.jpg'), W, 'Nuestros bocetos a mano: la portada, la Experiencia Khiska como un cactus donde cada flor es una ruta, y la agenda de eventos.'),
  p('En el cactus dibujado ya estaba la idea central: **cada flor es una ruta**. En otra hoja apareció la agenda de "eventos programados", las fotos de las experiencias de la gente y los enlaces a las redes de destinoelquisco y de la Municipalidad. Mucho de eso llegó al producto final; otras ideas las filtramos con datos y con lo que fuimos aprendiendo:'),
  ...tabla([['Idea inicial (boceto)', 30], ['Lo que decidimos', 30], ['Por qué', 40]], [
    ['Registro, login y guardar ruta en Wallet', 'Consultar rutas **sin registro** y sin descargar apps; Wallet como fase futura', 'El primer paso tiene que ser fácil. Pedir cuenta antes de mostrar valor espanta a Camila.'],
    ['Solo una experiencia digital', '**Phygital**: QR en el lugar y Pasaporte de papel', '25,1% de la comuna tiene 65 o más; 13,8% de los mayores de 60 nunca usó internet.'],
    ['Ranking de quienes más recorren', '**Progreso privado**, sin rankings', 'La flor es memoria personal, no competencia.'],
    ['Escanear el QR completa la ruta', 'El QR **acompaña**; completar la ruta abre la flor', 'Una flor tiene que significar algo vivido, no una foto a un cartel.'],
    ['Publicaciones de Instagram con comentarios', 'Sección **Mira** con los videos de la campaña', 'Mostrar contenido propio y controlado, sin depender de permisos de terceros.'],
    ['Escribir "khishka"', 'La marca se escribe **Khiska**', 'Una grafía más simple de leer y recordar, registrada entre las variantes.'],
    ['"Haz florecer tu Khiska" suelto', 'Siempre junto al cactus; el que florece es el cactus, nunca la persona', 'Un profesor nos advirtió un posible doble sentido. Lo resolvimos con reglas de uso.'],
  ], { zebra: true }),
  p('También usamos inteligencia artificial como compañera de trabajo: Perplexity para buscar datos actuales con fuente, IA de imágenes para la base de las ilustraciones botánicas ("cactus artesanal con una sola flor rosada", "sello circular artesanal para una ruta completada") y Claude para ordenar los documentos y construir el sitio y la app a partir de nuestros bocetos, el brandbook y la carpeta de recursos. Las decisiones creativas y estratégicas fueron siempre nuestras, y nos pusimos una regla: la IA no inventa datos, testimonios ni rutas.'),

  h2('Así lo soñamos, así quedó'),
  p('Lo que más nos enorgullece es que el producto final se parece a lo que dibujamos. No es una plantilla: viene de nosotros.'),
  ...dosImg(I('boceto-portada.jpg'), I('web-portada.jpg'), 'Así lo soñamos', 'Así quedó'),
  ...dosImg(I('boceto-cactus.jpg'), I('app-mi.jpg'), 'El cactus: cada flor, una ruta', 'Mi Khiska en la app'),
  ...dosImg(I('boceto-eventos.jpg'), I('web-agenda.jpg'), 'Eventos programados', 'La agenda del portal'),

  h2('El prototipo: portal, app y videos'),
  p('Nuestro soporte troncal tiene tres piezas que funcionan como una sola experiencia, publicadas y navegables:'),
  bullet('**El portal** (nicocsuarez-rgb.github.io/khiska-el-quisco): reúne los lugares, la Experiencia Khiska, los videos de la campaña y la agenda. Su entrada pregunta "¿Cómo quieres vivir El Quisco?" y ofrece un camino distinto para cada persona.'),
  bullet('**La app Khiska**: el viaje de Camila en el celular, desde la curiosidad hasta la flor. Inicio, intereses, rutas, ficha, en ruta, la flor que se abre, Mi Khiska, próxima experiencia, agenda y "Propón un lugar".'),
  bullet('**Los videos**: el tráiler de campaña y tres reels con la misma voz y el mismo lenguaje visual, que viven en la sección Mira del portal.'),
  ...dosImg(I('web-para-ti.jpg'), I('web-mira.jpg'), 'Una entrada por persona', 'Mira: los videos de la campaña'),
  ...dosImg(I('app-inicio.jpg'), I('app-rutas.jpg'), 'App: el inicio', 'App: elige tu próxima ruta'),
  p('**Nuestra propuesta de valor:** para quien quiere conocer El Quisco más allá del verano, Khiska convierte la curiosidad en una ruta concreta y deja una flor como memoria de lo vivido, sin descargar apps ni crear una cuenta.'),
  p('La pauta de la asignatura pide que un prototipo cumpla cinco criterios de inmersión. Así los cumple Khiska:'),
  ...tabla([['Criterio', 20], ['Cómo lo cumple Khiska', 80]], [
    ['**Multisensorial**', 'La flor se abre con sonido y vibración (que se pueden silenciar). En los hitos, los relatos en voz de pescadores y vecinos hacen que el lugar se escuche, no solo se vea.'],
    ['**Interactiva**', 'La persona elige por intereses, abre fichas, imprime, avanza por la ruta y ve cambiar su cactus.'],
    ['**Participativa**', '"Propón un lugar" permite que la comunidad sugiera rutas futuras. Vale y Rosa no son espectadoras: aportan.'],
    ['**Sin fricciones**', 'Dos toques desde el inicio hasta la ficha, sin registro, con modo de lectura fácil para Don Héctor y versión imprimible para los tramos sin señal.'],
    ['**Narrativa**', 'Todo el flujo cuenta la misma historia: la espina que pincha la curiosidad, el camino que se recorre y la flor que queda.'],
  ], { zebra: true }),

  h2('Por qué esta tecnología'),
  ...tabla([['Elegimos', 30], ['Porque', 70]], [
    ['**Web app que se abre con un QR**, sin descarga', 'El 99,1% de los hogares con internet tiene smartphone; abrir un enlace es un gesto que todos ya conocen. Una app descargable sería una barrera en el primer paso.'],
    ['**Pasaporte de papel** y ficha imprimible', 'Uno de cada cuatro vecinos tiene 65 años o más, y hay tramos costeros con poca señal.'],
    ['**Lectura fácil**', 'Texto grande y menos elementos para que Don Héctor también pueda usarla.'],
    ['**Hosting en GitHub Pages**', 'Costo $0, publicación inmediata y un código que otras comunas podrían reutilizar.'],
    ['**Realidad aumentada en el navegador** (WebAR)', 'Permite la foto con el cactus florecido sin instalar nada, con librerías de código abierto.'],
  ], { zebra: true }),
  brk(),

  // ---------- Acto 3 ----------
  acto('Acto 3 · La flor'),
  h1('Lanzamiento, alianzas y viabilidad'),
  h2('Estrategia digital de lanzamiento'),
  p('La campaña dura tres meses y cada mes es un acto de la historia. Primero cambiamos la mirada, después enseñamos a recorrer y al final damos una razón para volver.'),
  ...tabla([['Acto', 16], ['En la calle', 30], ['En lo digital', 30], ['Lo que suena', 24]], [
    ['**1. La espina**\nJulio', '**Paraderos y Metro sonoros** en Santiago y Valparaíso: en medio del ruido de la ciudad, el mupi deja escuchar el mar de El Quisco. Un QR lleva a "Escucha El Quisco".', 'Tráiler de campaña, reels y TikTok; carrusel "¿Qué dimensión de El Quisco conoces?"; encuesta en Stories.', 'Paisaje sonoro real: el mar en las rocas, las aves de quebrada y humedal, la brisa.'],
    ['**2. El camino**\nAgosto', 'Señalética con QR en los hitos, ficha imprimible, Pasaporte de papel y Punto Khiska.', 'Portal y app: catálogo, fichas, en ruta. Reel tutorial "Elige, prepara y comienza".', 'Relatos en voz de pescadores de la caleta, vecinos y oficios, con transcripción.'],
    ['**3. La flor**\nSeptiembre', 'Sello en el Pasaporte y **cartel fotográfico con realidad aumentada** junto al letrero de El Quisco.', 'La flor se abre en la app, Mi Khiska, próxima experiencia y agenda. Reel "Una ruta completada hace florecer tu Khiska".', 'El sonido de la flor al abrirse.'],
  ]),
  p('**El cartel con realidad aumentada.** Junto a las letras de El Quisco instalaremos un cartel con un código QR. Al escanearlo, se abre directamente la cámara del celular en el navegador y, detrás de las letras reales, aparecen cactus quisco: tienen una flor abierta por cada ruta que esa persona completó, y capullos por cada ruta que le falta. La foto que se lleva es única, porque muestra su propio recorrido, y es también una invitación a volver hasta ver el cactus completo. Es la escena final de la historia de Camila.'),
  p('**Una identidad que suena.** Lo sonoro recorre los tres actos: el mar que irrumpe en el paradero, la voz de un pescador que cuenta su caleta en el hito y la flor que suena al abrirse. Para lograrlo grabaremos en terreno con un celular y un micrófono de solapa. Primero el paisaje sonoro de cada lugar, temprano y sin viento. Después de tres a cinco relatos de vecinos, pescadores y oficios, de 60 a 90 segundos, cada uno con autorización firmada para usar su voz y su nombre, y con transcripción para que también los pueda leer quien lo necesite. Nunca usaremos voces artificiales haciéndose pasar por vecinos.'),

  h2('Alianzas estratégicas'),
  p('Elegimos una alianza principal que respalda toda la experiencia y una por cada dimensión de El Quisco. Así, las alianzas también cuentan la historia:'),
  ...tabla([['Rol', 18], ['Aliado', 24], ['Qué aporta', 32], ['Respaldo', 26]], [
    ['**Patrocinio**', 'destinoelquisco', 'La voz del turismo de la comuna: legitimidad, audiencia y un canal oficial para Khiska.', 'Su cuenta de Instagram y destinoelquisco.cl'],
    ['**Rostro**', 'Francisco "Chapu" Puelles (propuesta)', 'Una voz conocida del mundo outdoor que conecta con Vale y Camila.', 'Se dedica a actividades de escalada y trekking (Meganoticias)'],
    ['**Humedal y bosque nativo**', 'Defensa El Batro y Comité Ambiental Comunal', 'Cuidan el humedal y validan cómo visitarlo sin dañarlo.', 'Su impulso llevó al reconocimiento del humedal (expediente MMA 2024–2025)'],
    ['**Acantilados y mar profundo**', 'Comunidad de escalada de Punta de Tralca', 'Relatos y contenido de uno de los sectores de escalada más antiguos del litoral.', 'Sector equipado desde los años ochenta (theCrag)'],
    ['**Memoria y sabores**', 'Casa Museo Isla Negra (Fundación Pablo Neruda)', 'Validación cultural y relatos del Litoral de los Poetas.', 'Destino Litoral de los Poetas (chile.travel)'],
    ['**Financiamiento**', 'Gobierno Regional de Valparaíso', 'Fondos FIC-R, FRPD y 8% para las fases siguientes.', 'Programas regionales de turismo sostenible (2026)'],
  ], { zebra: true }),
  p('Al Chapu lo planteamos como el rostro ideal, sin haberlo contactado: si el proyecto avanza con la municipalidad, lo invitaríamos a grabar sus propias piezas con nuestro guion.'),

  h2('Viabilidad: tiempos, recursos y costos'),
  p('Khiska crece por fases, y cada fase avanza solo cuando se cumple su condición, no por calendario. Así la municipalidad nunca se compromete con más de lo que puede sostener.'),
  ...tabla([['Fase', 18], ['Qué incluye', 52], ['Condición para avanzar', 30]], [
    ['**0. Hoy**', 'Campaña, portal y app funcionando, videos producidos.', 'Presentación a la municipalidad y a destinoelquisco.'],
    ['**1. Ruta piloto**', 'Una ruta con hitos QR, relatos de vecinos, Pasaporte de papel y cartel con RA.', 'Ruta y forma de completarla acordadas con la municipalidad.'],
    ['**2. Más rutas**', 'Nuevas rutas, beneficios con comercios locales y registro real.', 'Piloto evaluado y acuerdos escritos con comercios.'],
    ['**3. Modelo para otras comunas**', 'Kit Khiska: marca, plantilla de ficha, criterios y código del sitio.', 'Resultados de la fase 2.'],
  ], { zebra: true }),
  p('La campaña de tres meses cuesta **$2.032.000** antes de impuestos: $1.672.000 en producción y gestión, y $360.000 en pauta en Meta y TikTok. Para la Fase 1 hicimos una estimación con precios públicos de proveedores chilenos de noviembre de 2026:'),
  ...tabla([['Ítem', 30], ['Supuesto', 32], ['Referencia', 22], ['Total', 16]], [
    ['Hosting del portal y la app', 'GitHub Pages', 'Gratuito', '$0'],
    ['Dominio .cl (1 año)', 'NIC Chile', '$9.940 + IVA', '$11.829'],
    ['Señalética con QR', '6 letreros trovicel 5 mm doble cara', 'Desde $14.000 c/u (PapelPrint)', '$84.000'],
    ['Pasaporte Khiska de papel', '100 unidades, tríptico full color', '$1.172 c/u (Macprint)', '$117.150'],
    ['Micrófono para relatos', 'Boya BY-M1 Pro II', '$40.990 (Paris.cl)', '$40.990'],
    ['Gráfica del cartel con RA', 'Trovicel impreso, 1 m²', '$10.080 (Macprint)', '$10.080'],
    ['Realidad aumentada', 'Librería de código abierto', 'Sin licencia', '$0'],
    ['**Total Fase 1**', '', '', '**$264.049**'],
  ], { zebra: true }),
  p('La estructura del cartel, la instalación y los permisos los consideramos como aporte en especie del municipio. Los paraderos sonoros se cotizan directamente con el operador de vía pública. Con estas cifras, una ruta piloto cabe con holgura en los fondos regionales disponibles, como el Fondo 8% del Gobierno Regional de Valparaíso.'),

  h2('Riesgos y cómo los cuidamos'),
  ...tabla([['Riesgo', 30], ['Prob.', 10], ['Impacto', 11], ['Cómo lo mitigamos', 49]], [
    ['Vecinos mayores quedan fuera', 'Alta', 'Alto', 'Pasaporte de papel, lectura fácil, Punto Khiska presencial y talleres.'],
    ['Invitar a rutas que aún no están listas', 'Alta', 'Alto', 'Lanzar solo con la ruta piloto definida; fichas solo con datos confirmados.'],
    ['Validación de ruta poco confiable', 'Alta', 'Medio', 'Método simple: código al final, sello presencial o ambos.'],
    ['Presión sobre el Humedal El Batro', 'Media', 'Alto', 'Código del visitante y criterios acordados con la municipalidad, el Ministerio del Medio Ambiente y Defensa El Batro.'],
    ['Beneficios comerciales sin respaldo', 'Media', 'Alto', 'Comunicarlos solo con acuerdo escrito.'],
    ['Sin señal en algunos tramos', 'Media', 'Medio', 'Ficha imprimible y Pasaporte de papel.'],
    ['Información desactualizada', 'Media', 'Medio', 'Un responsable municipal y revisión mensual.'],
    ['Datos personales de usuarios', 'Media', 'Medio', 'Consulta sin registro; pedir solo lo mínimo.'],
    ['Daño o robo de señalética y QR', 'Media', 'Bajo', 'Hitos de bajo costo y fácil reposición; el QR también va en el Pasaporte.'],
    ['Caída del sitio', 'Baja', 'Medio', 'Hosting estático y gratuito, con copia del código en GitHub.'],
    ['Audios sin autorización', 'Baja', 'Alto', 'Autorización firmada de voz y nombre antes de publicar cualquier relato.'],
  ], { zebra: true }),
  brk(),

  // ---------- Cierre ----------
  acto('Epílogo'),
  h1('Hay más El Quisco por descubrir'),
  p('Empezamos el semestre pensando en una campaña y terminamos diseñando una forma de recorrer El Quisco. Khiska es nuestra apuesta: un sistema simple, bonito y cuidadoso con el territorio, que conecta a quien visita con quienes viven ahí, y que da una razón real para volver.'),
  p('Camila llegó con curiosidad. Siguió un camino. Se fue con una flor. Y su cactus todavía tiene capullos.'),
  cita('El Quisco lleva el nombre de una espina. Nosotros solo queremos que pinche tu curiosidad.'),

  h2('Fuentes'),
  ...['Biblioteca del Congreso Nacional (BCN), Reporte comunal El Quisco 2026: Censo 2024 (INE) y empresas (SII).',
    'Sernatur, ocupación de alojamientos en vacaciones de verano e invierno, Litoral de los Poetas, 2025.',
    'Subtel, XII Encuesta de Acceso, Usos y Usuarios de Internet, 2025.',
    'DataReportal, Digital 2027: Chile, 2026.',
    'Ministerio del Medio Ambiente, Res. Ex. 6.648 que reconoce el Humedal Urbano El Batro, 29/09/2025; expediente de solicitud, 2024–2025.',
    'Real Academia Española, Diccionario de la lengua española, entrada «quisca».',
    'Rodolfo Lenz, Diccionario etimológico de las voces chilenas derivadas de lenguas indígenas americanas (1904–1910).',
    'Teófilo Laime Ajacopa, Diccionario bilingüe Iskay simipi yuyayk\'ancha, La Paz, 2007.',
    'Municipalidad de El Quisco, Informe Final PLADETUR (2025), y destinoelquisco.cl.',
    'Meganoticias, nota sobre Francisco Puelles, 07/12/2022 · theCrag, sector de escalada Punta de Tralca · chile.travel, Litoral de los Poetas.',
    'Precios de referencia: NIC Chile (vía simplo.cl), PapelPrint, Macprint y Paris.cl, noviembre de 2026.',
  ].map(t => new Paragraph({ numbering: { reference: 'vinetas', level: 0 }, spacing: { after: 60 }, children: [new TextRun({ text: t, font: F, size: 19, color: GRIS })] })),
];

const doc = new Document({
  creator: 'Agencia C.C.C.', title: 'Khiska · Informe EV3 Innovación Digital',
  styles: {
    default: { document: { run: { font: F, size: 23 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: F, size: 40, bold: true, color: VERDE }, paragraph: { spacing: { before: 120, after: 200 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: F, size: 28, bold: true, color: VERDE }, paragraph: { spacing: { before: 320, after: 120 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: 'vinetas', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Khiska · Agencia C.C.C.   ', font: F, size: 18, color: GRIS }), new TextRun({ children: [PageNumber.CURRENT], font: F, size: 18, color: GRIS })] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync('Informe_EV3_Khiska_El_Quisco.docx', b); console.log('ok'); });
