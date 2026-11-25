# Prompt: narrativa y sonido en el portal y la app

Pega esto en Claude Code sobre el repositorio `khiska-el-quisco`.

---

Lee `CLAUDE.md`, `_proyecto/contexto.md` y, sobre todo, **`_proyecto/sistema-khiska.md`**: es el documento base y manda sobre todo lo demás.
Vamos a hacer que el portal y la app cuenten la misma historia y tengan sonido. Trabaja paso a paso: primero muéstrame
el plan (qué cambias en cada página y pantalla) y espera mi visto bueno. No inventes datos, rutas, duraciones,
comercios ni voces.

## 1. Narrativa: la espina, el camino y la flor (portal y app)

- Organiza el portal en los **tres actos** del punto 1 de `sistema-khiska.md`, sin agregar más texto del necesario:
  - **La espina** (curiosidad): portada, "Pincha tu curiosidad", videos.
  - **El camino**: lugares, fichas, cómo preparar la visita.
  - **La flor**: Khiska, Mi Khiska, agenda y razones para volver.
  Usa un marcador visual sutil por acto (ícono de espina, sendero o flor de `assets/`) y una frase corta de transición entre actos.
- En la app, que el recorrido se sienta como el viaje de Camila por los tres actos: los títulos y las transiciones entre pantallas
  deben dejar claro en qué acto está la persona.
- La pantalla **"¡Florece!"** se renombra para cumplir la regla 3 de lenguaje (el que florece es el cactus, no la persona),
  por ejemplo "Tu flor se abrió". Revisa todos los textos con `_proyecto/guia-de-lenguaje.md`.
- La portada del portal y el inicio de la app deben poder explicarse en una frase: "Una espina que pincha tu curiosidad,
  un camino por El Quisco y una flor que guarda lo que viviste."

## 2. Sonido (punto 4 de `sistema-khiska.md`)

- Crea `assets/audio/` y `js/audios.js` (lista editable: `{ id, lugar, tipo: "paisaje" | "relato", titulo, archivo, transcripcion, credito }`).
- **Paisaje sonoro**: componente "Escucha este lugar" en cada ficha de `territorios/` y en la pantalla En ruta de la app.
- **Relatos en voz local**: el mismo componente, con transcripción desplegable y crédito "Voz de [nombre], [oficio]".
  Solo se muestran si el archivo existe y tiene transcripción y crédito. **Nunca** generes voces con IA para relatos de vecinos o pescadores.
- **Landing "Escucha El Quisco"** (`escucha.html`): es el destino del QR de los paraderos sonoros (acto 1). Un botón grande para
  escuchar el paisaje sonoro, una frase ("Esto también es El Quisco") y un CTA a lugares. Debe funcionar bien en celular y cargar rápido.
- El sonido de la flor al abrirse (app) se mantiene, con opción de silenciarlo.
- Accesibilidad: nada suena solo al cargar; controles con etiqueta, teclado y transcripción.
- Si todavía no hay archivos en `assets/audio/`, deja todo construido pero **oculto** (modo presentación: sin reproductores vacíos
  ni "próximamente"), y dime exactamente qué archivos necesitas y con qué nombre.

## 3. Cierre

- Revisa enlaces, consola sin errores y vista en celular (360 px).
- Actualiza `_proyecto/contexto.md` y `_proyecto/registro-de-decisiones.md`.
- Haz commit y push.
