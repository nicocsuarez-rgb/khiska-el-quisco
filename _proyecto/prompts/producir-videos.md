# Prompt: producir 3 videos (V01, V07, V12) con la skill de reels

Pega esto en Claude Code sobre el repositorio `khiska-el-quisco`.

---

Vamos a producir 3 videos de la campaña con la skill de edición de reels. Antes de hacer nada:

1. Lee `CLAUDE.md`, `_proyecto/contexto.md` y `_proyecto/guia-de-lenguaje.md`.
2. Abre `_proyecto/fuentes/grilla-contenidos.xlsx`, pestañas **Guiones de video** y **Estilo de video**: ahí están el guion y las reglas de V01, V07 y V12.
3. Mira cuadro a cuadro y escucha `assets/video/v00-el-quisco-desde-un-solo-lugar.mp4`. Es la referencia obligatoria de estilo, ritmo y voz.

## Los 3 videos

| Guion | Pieza | Duración | Qué cuenta |
|---|---|---|---|
| **V01** | Tráiler de campaña: El Quisco no termina en la playa | 30–35 s | Presentación de la campaña. Pregunta de apertura → la playa ilustrada se abre por capas (humedal, quebrada, mirador, caleta, un cartel por lugar) → "y desde hoy, una forma nueva de recorrerlo" → cactus Khiska → "Una ruta. Una flor." → destellos del portal y la app → "Pincha tu curiosidad." |
| **V07** | Elige, prepara y comienza | 25–30 s | Tutorial con la app real: 1. Elige (catálogo de rutas) · 2. Prepara (ficha, se puede imprimir) · 3. Comienza (en ruta). Final: el cactus con una flor que se abre + "Haz florecer tu Khiska". |
| **V12** | Una ruta completada hace florecer tu Khiska | 20 s | El cactus está en pantalla desde el inicio → una flor se abre lentamente → "La flor no es un premio: es la memoria de lo que viviste." → Mi Khiska en la app. |

## Reglas (no negociables)

- **Igual que V00:** fondo papel, Rubik / Rubik Mono One, pantallas reales dentro de un marco de navegador o de celular, pasos numerados, máximo 8 palabras por cartel, y el mismo cierre: logo El Quisco + flor + "¿Qué parte de El Quisco quieres descubrir?" + botón rosa "EXPLORA EN EL LINK DE LA BIO".
- **Voz:** la misma lógica de V00, una voz IA que lee el texto en pantalla, más música instrumental suave y subtítulos. Si la skill no puede generar voz, entrega la versión con música y subtítulos y avísame.
- **Solo materiales del proyecto:** ilustraciones de `assets/img/` (lugares `territorio-*.webp`, cactus, `flor-capullo/parcial/abierta.webp`, sello, pasaporte), logo `assets/img/logo-el-quisco.webp`, y capturas o grabaciones de pantalla **actuales** del portal (`index.html`, `rutas.html`) y de la app (`app/index.html`), hechas con Playwright. Nada de stock ni pantallas inventadas.
- **Lenguaje:** "Haz florecer tu Khiska" solo con el cactus en pantalla, y "florecer" nunca dirigido a la persona. Sin "demo" ni "prototipo" en pantalla. No mostrar rutas con duración, dificultad ni comercios.
- **Técnico:** 1080×1920, 30 fps, H.264 + AAC, menos de 25 MB cada uno.

## Dónde va cada cosa

```
_proyecto/produccion/videos/v01/   ← guion final, capturas, audio y proyecto de edición (no se publica)
_proyecto/produccion/videos/v07/
_proyecto/produccion/videos/v12/
assets/video/v01-trailer.mp4             + assets/video/poster-v01.jpg
assets/video/v07-elige-prepara-comienza.mp4 + assets/video/poster-v07.jpg
assets/video/v12-haz-florecer-tu-khiska.mp4 + assets/video/poster-v12.jpg
```

Al terminar cada video:
- Agrégalo a `js/videos.js` en este orden: V01 primero (destacado), luego V00, V07 y V12.
- En la grilla, pestaña **Producción**, cambia su estado a "Listo" y escribe la ruta del archivo.
- Suma una línea en `_proyecto/registro-de-decisiones.md` y actualiza la sección Videos de `_proyecto/contexto.md`.

## Si trabajas con esta carpeta en el Mac (sin GitHub)

- Las capturas actuales de la app y del portal ya están en `_proyecto/produccion/capturas/` (celular, 1170×2532).
  Para escenas que no estén ahí, abre `index.html` o `app/index.html` en el navegador y graba o captura la pantalla.
  Para "En ruta" y la flor que se abre, usa las ilustraciones `assets/img/flor-capullo.webp`, `flor-parcial.webp` y `flor-abierta.webp`.
- No hay commit ni push: deja los videos y pósters en `assets/video/` y actualiza `js/videos.js` dentro de esta carpeta.
  Nicolás los sube después al repositorio.
- Si no puedes editar el Excel de la grilla, anota los cambios en `_proyecto/produccion/videos/cambios.md`.

## Cómo trabajamos

Uno a la vez, partiendo por **V01**. Antes de renderizar, muéstrame el guion escena por escena (tiempo, imagen, texto en pantalla y lo que dice la voz) y espera mi visto bueno. Después de renderizar, revisa cuadros del video, dime qué quedó y qué mejorarías, y espera mi visto bueno antes de seguir con el siguiente. Al final, si estás en el repositorio, haz commit y push.
