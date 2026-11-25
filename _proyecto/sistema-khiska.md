# Sistema Khiska · documento base

Fuente única para el informe de Innovación (EV3 Miranda), el informe de Medios, el portal, la app, los videos y todo lo físico.
Si algo no calza con este documento, se corrige el otro material, no este (salvo acuerdo del equipo).

## 1. La narrativa: la espina, el camino y la flor

"Quisco" viene del quechua *espina* (fuentes en el dossier). De ahí sale la historia que une todo:

| Acto | Símbolo | Qué le pasa a la persona | Fase de campaña | Frase |
|---|---|---|---|---|
| **1. La espina** | Espina | Algo la pincha: descubre que El Quisco no termina en la playa | **Despertar** (julio) | "Pincha tu curiosidad." |
| **2. El camino** | Sendero | La curiosidad se vuelve una ruta concreta: elige, prepara, recorre | **Recorrer** (agosto) | "Elige, prepara y comienza." |
| **3. La flor** | Flor | Lo vivido queda como memoria visible y razón para volver | **Florecer y volver** (septiembre) | "Una ruta completada hace florecer tu Khiska." |

La protagonista es **Camila** (persona principal). Cada pieza, pantalla y soporte pertenece a uno de los tres actos.

## 2. Públicos: una sola lista

El informe de Medios usó segmentos y el de estrategia usó personas. Son los mismos públicos:

| Segmento (Medios) | Persona | Acto donde más actúa |
|---|---|---|
| Escapista urbano (fuera de El Quisco) | **Camila** antes de viajar | 1. La espina |
| Explorador experiencial (en El Quisco) | **Camila** en destino · **Vale** | 2. El camino |
| Familias y excursionistas culturales | **Visitante habitual / segunda vivienda** · **Don Héctor** | 2 y 3 |
| Comunidad y actores locales | **Rosa** (oficios) · **Vale** · **Don Héctor** | Validan y cuentan el territorio |

## 3. Puntos de contacto por acto (phygital)

| Acto | Físico | Digital | Sonido |
|---|---|---|---|
| **1. La espina** | **Paraderos y Metro sonoros** (Santiago y Valparaíso): mupi con el sonido real de El Quisco contra el ruido de la ciudad + QR | Reels/TikTok (V01 tráiler, V00), landing **"Escucha El Quisco"** a la que lleva el QR del paradero | **Paisaje sonoro**: mar en las rocas, aves de quebrada y humedal, brisa |
| **2. El camino** | Señalética con QR en los hitos, ficha imprimible, Pasaporte de papel, Punto Khiska | Portal (lugares y fichas), app: rutas, ficha, en ruta | **Relatos en voz local**: pescadores de la caleta, vecinos y oficios, con transcripción |
| **3. La flor** | Sello en el Pasaporte, **cartel fotográfico con RA** (cactus con una flor por ruta completada) | App: la flor se abre, Mi Khiska, próxima experiencia, agenda | **Sonido de la flor al abrirse** (con opción de silenciarlo) |

Reglas que no cambian: una flor = una ruta completa · escanear un QR acompaña, no completa · sin rankings · sin registro para consultar · beneficios y comercios solo con acuerdo escrito.

## 4. Identidad sonora

- **Qué suena:** sonidos reales de El Quisco grabados en terreno y voces reales de la comunidad. Nunca voces de IA presentadas como vecinos o pescadores.
- **Narrador:** en los videos se usa la voz IA "Sandra" como narradora de la campaña (no se presenta como persona del lugar).
- **Producción de audios** (responsable sugerida: Fernanda, que es de El Quisco):
  1. Paisaje sonoro: 1–2 min por lugar (mar en Punta de Tralca, aves en El Batro y Las Petras, caleta), temprano y sin viento fuerte, celular + micrófono con cortaviento.
  2. Relatos: 3 a 5 personas (pescador/a de la caleta, vecino/a mayor, oficio local). Pauta: ¿qué es este lugar para usted?, un recuerdo, qué debería saber quien lo visita. Editar a 60–90 s.
  3. **Autorización firmada** de uso de voz y nombre, y **transcripción** de cada relato (accesibilidad y lectura fácil).
  4. Archivos en `assets/audio/` (mp3, 128 kbps) y registro en `js/audios.js`.
- Mientras no existan grabaciones reales, el sitio y la app no muestran reproductores de relatos.

## 5. Alianzas

| Rol | Aliado | Aporta | Respaldo (fecha) |
|---|---|---|---|
| Patrocinio / paraguas | **destinoelquisco** (cuenta de turismo de la comuna) | Legitimidad, audiencia, canal oficial | Por confirmar quién la administra (municipio o privado) |
| Rostro (propuesta, sin contacto) | **Francisco "Chapu" Puelles** | Voz outdoor y aventura | Meganoticias (2022) |
| Humedal y bosque nativo | **Defensa El Batro / Comité Ambiental Comunal El Quisco** | Validación ambiental, cuidado del humedal | Expediente MMA 2024–2025; Res. Ex. 6.648 (29/09/2025) |
| Acantilados y mar profundo | **Comunidad de escalada de Punta de Tralca** | Ruta de roca, relatos, contenido | theCrag (buscar fuente 2025–2026) |
| Memoria y sabores | **Casa Museo Isla Negra (Fundación Pablo Neruda)** | Validación cultural y relatos | chile.travel (buscar fuente 2025–2026) |
| Financiamiento | Gobierno Regional de Valparaíso (FIC-R, FRPD, Fondo 8%) | Fases 1–3 | G5 Noticias (28/07/2026) |

## 6. Costos de la Fase 1 (ruta piloto) · estimación con precios de referencia

Simulación hecha con precios públicos de proveedores chilenos (noviembre 2026). No son cotizaciones formales.

| Ítem | Supuesto | Precio de referencia | Total estimado |
|---|---|---|---|
| Hosting portal y app | GitHub Pages | $0 | $0 |
| Dominio .cl (1 año) | NIC Chile | $9.940 + IVA | $11.829 |
| Señalética QR en hitos | 6 letreros trovicel 5 mm doble cara (1 ruta) | desde $14.000 c/u (PapelPrint) | $84.000 |
| Pasaporte Khiska de papel | 100 unidades formato tríptico, full color | $1.172 c/u en 100 u (Macprint, tríptico) | $117.150 |
| Micrófono para relatos y paisaje sonoro | Boya BY-M1 Pro II | $40.990 (Paris.cl) | $40.990 |
| Cartel fotográfico RA (estructura + gráfica) | Trovicel impreso, 1 m² | $10.080/m² (Macprint) + estructura con el municipio | $10.080 + estructura |
| WebAR | Librería de código abierto (MindAR / AR.js), desarrollo del equipo | $0 en licencias | $0 |
| Paraderos y Metro sonoros | Mupi + audio direccional | Requiere cotización con el operador de vía pública | Por cotizar |
| **Total Fase 1 sin vía pública** | | | **≈ $264.049 + estructura** |

Instalación, permisos y estructuras: aporte en especie del municipio.

## 7. Correcciones al informe de Medios (para el examen)

- "7 territorios **o rutas**" → **7 lugares en 3 dimensiones**; las rutas se definen con el municipio.
- Públicos → usar la tabla del punto 2 (segmento + persona).
- "Comercios adheridos", "entrega de beneficios" → **solo con acuerdo escrito**.
- "Dossier Khiska" como medio para la comunidad → el dossier es interno; cambiar por **kit para aliados**.
- "Descarga o registro inicial en el Pasaporte" → **sin descarga ni registro para consultar rutas**.
- Agregar la **capa sonora** a toda la arquitectura (no solo paraderos): relatos en hitos y sonido de la flor.
- Etiquetar cada soporte con su **acto** (espina, camino, flor).
