# Prompt para producir los videos en Claude Code

Copia y pega esto en una sesión de Claude Code sobre este repositorio, cambiando el número de guion.

---

Lee `CLAUDE.md` y `_proyecto/contexto.md`. Abre `_proyecto/fuentes/grilla-contenidos.xlsx`,
pestañas **Estilo de video** y **Guiones de video**, y produce el video **V01** (cambia por V07 o V12).

Reglas:
- Referencia obligatoria: `assets/video/reel-el-quisco-no-termina-en-la-playa.mp4` (V00). Mismo fondo papel,
  tipografía Rubik / Rubik Mono One, pantallas reales del portal y de la app en marco de navegador,
  pasos numerados y el mismo cierre (logo + flor + "¿Qué parte de El Quisco quieres descubrir?" +
  botón rosa "EXPLORA EN EL LINK DE LA BIO").
- Usa solo las ilustraciones de `assets/img/`, el logo de `assets/img/logo-el-quisco.webp` y capturas
  reales de `index.html`, `rutas.html` y `app/index.html` (toma las capturas con Playwright).
- Audio: voz IA que lee el mismo texto que aparece en pantalla + música instrumental suave.
- 1080×1920, 30 fps, H.264, entre 20 y 40 s. Guarda en `assets/video/` con un nombre descriptivo.
- Antes de renderizar, muéstrame el guion escena por escena con los textos y la duración, y espera mi visto bueno.
- Al terminar, revisa cuadros del video y avísame qué quedó y qué falta (por ejemplo, la voz).
