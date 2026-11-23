# Khiska · El Quisco — instrucciones para Claude Code

Proyecto universitario de **Agencia C.C.C.** (Fernanda Cruz, Benjamín Cerda y Nicolás Cáceres),
Publicidad, Duoc UC Viña del Mar. Campaña **"El Quisco: donde la naturaleza tiene nombre"** y
**Experiencia Khiska**. Este repositorio es lo que se muestra en el **examen transversal**.

Trabajamos como compañeros, paso a paso: antes de un cambio grande, resume lo que entendiste y
espera confirmación. Responde en español de Chile, claro y cercano.

## Qué hay en el repositorio

| Carpeta / archivo | Qué es | ¿Se publica? |
|---|---|---|
| `index.html`, `rutas.html`, `experiencia-khiska.html`, `territorios/`, `privacidad.html` | **Portal** para el visitante | Sí (GitHub Pages) |
| `css/styles.css`, `js/main.js`, `assets/` | Estilos, interacciones, ilustraciones, íconos y fuentes Rubik | Sí |
| `app/index.html` | **App Khiska** (Mi Khiska, pantallas P1–P10). Un solo archivo con imágenes incrustadas | Sí |
| `equipo/dossier.html` | **Dossier** de respaldo (datos con fuente, journey, personas, aliados, riesgos) | Sí, pero **nunca enlazado desde el menú del portal** |
| `_proyecto/` | Registro de decisiones, guía de lenguaje, herramientas | No (Jekyll ignora carpetas con `_`) |

El portal se abre con doble clic en `index.html`; no necesita servidor.
Las páginas de `territorios/` se generaron con `_proyecto/herramientas/build.py`; hoy se editan directo en el HTML.

## Objetivo actual

El sitio es un **portal**: el lugar donde se **ve, reproduce, encuentra y desde donde se redirige** a todo
el contenido de la Experiencia Khiska (lugares, la experiencia, videos y reels, agenda, redes).
Sitio y app deben sentirse como **una sola experiencia**.

## Modo presentación (obligatorio)

Todo lo visible se ve como **producto terminado**:
- Nada de notas de producción, instrucciones, etiquetas "pendiente/por confirmar", "demo" ni tablas de estado.
- **Pero nunca inventar datos.** Si un dato no existe (duración, dificultad, horarios, contacto, comercios),
  **se omite el campo**, no se rellena ni se marca.
- Se mantiene una sola línea de crédito en el pie: "Proyecto académico de Agencia C.C.C. · Duoc UC".
  Evita que el portal parezca el sitio oficial de la Municipalidad (usa su logo).

## Reglas de Khiska

- **Una flor = una ruta completa e individual.** No es un hito ni una etapa.
- Estados de la flor: capullo cerrado (no iniciada) → apertura parcial (iniciada) → flor abierta (completada)
  → beneficio señalado (solo con acuerdo local confirmado).
- No afirmar plataforma operativa, comercios adheridos, canjes, Wallet ni validación con usuarios.
- Los lugares (El Batro, Las Petras, Mirador Neptuno, Isla Negra, Punta de Tralca, El Totoral, la caleta)
  son **referentes**, no rutas confirmadas: sin recorridos, duraciones ni dificultades inventadas.
- Origen del nombre: solo con las fuentes citadas en `equipo/dossier.html`.
- La marca se escribe **Khiska**.
- Dossier y portal son productos distintos.

## Lenguaje: "Haz florecer tu Khiska"

Se mantiene la frase, con tres reglas (ver `_proyecto/guia-de-lenguaje.md`):
1. Siempre junto a la imagen del cactus o la flor; nunca como texto aislado.
2. Siempre después de que se entienda que Khiska es un cactus.
3. "Florecer" nunca se dirige a la persona (no "hazte florecer", "florece con nosotros").

## Identidad visual

- Tipografía: Rubik (texto), Rubik Mono One (titulares de activación). Archivos locales en `assets/fonts/`.
- Paleta botánica: verde `#55763A`, rosa `#EE7F8E`, salvia `#A7BE9F`, tinta `#1E1E1E`, fondo papel `#FAF7EE`.
- Paleta vibrante El Quisco (solo acentos): `#00A8E8 #ABCC59 #FFD000 #ED9E00 #C95028`.
- Ilustración botánica artesanal, acuarela + tinta fina. Nada 3D, infantil ni íconos corporativos genéricos.
- Logo de El Quisco original: no redibujar ni alterar.
- Tono: cercano, evocador y claro. "La poesía invita. La información orienta."

## Calidad

- HTML semántico, accesible (WCAG 2.2 AA), responsive desde 360 px, sin scroll horizontal.
- Sin dependencias externas innecesarias; rutas relativas.
- Antes de dar algo por terminado: revisar enlaces, consola sin errores y vista en celular.
