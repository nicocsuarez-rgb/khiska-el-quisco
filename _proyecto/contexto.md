# Contexto del proyecto Khiska · El Quisco

Léelo antes de cualquier tarea grande. Resume todo lo trabajado en el proyecto de claude.ai hasta el 23/11/2026.
Las fuentes completas están en `_proyecto/fuentes/` (la propuesta final es `propuesta-final.md`).

## Estado

- **EP3 de Taller de Estrategia (prof. Daniel Palomero):** entregada el 16/11/2026, nota **6,8**.
- **Lo que viene:** examen transversal de cuatro ramos (Taller de Estrategia y Planificación Digital,
  Innovación Digital, Community Manager y Marketing de Influencers, Estrategia de Medios Aplicada).
  La presentación del examen debe hacer referencia directa al **portal** y a la **app**, porque cada una
  responde a nuestros tipos de consumidor.
- Las pautas del examen no están en este repositorio: pedirlas al equipo antes de afirmar exigencias de un ramo.

## La campaña en una página

- **Problema:** la comunicación de El Quisco muestra lugares, pero no enseña a vivirlos.
- **Insight:** "La curiosidad por El Quisco ya existe; lo que falta es un siguiente paso claro y una razón
  para volver fuera del verano." (Ocupación Litoral de los Poetas: 66,6% en febrero → 30,9% en invierno, Sernatur 2025.)
- **Concepto:** "El Quisco: donde la naturaleza tiene nombre." Invitación: "Pincha tu curiosidad."
  Instrucción: "Explora una ruta. Completa la experiencia. Haz florecer tu Khiska."
- **Khiska:** sistema phygital. Cada persona tiene un cactus; cada ruta completada abre una flor y suma un sello
  al Pasaporte (digital o de papel).
- **Fases (jul–sep):** Despertar ("El Quisco no termina en la playa") → Recorrer ("Elige, prepara y comienza")
  → Florecer y volver ("Una ruta completada hace florecer tu Khiska").
- **Canales:** Instagram (17), Facebook (9), TikTok (6), YouTube (4), sitio web (3 módulos). 39 contenidos, 8 pagados, $360.000 en pauta.
  Todos llevan al sitio. Grilla completa en `fuentes/grilla-contenidos.xlsx`.
- **Presupuesto:** $2.032.000 (producción $1.672.000 + pauta $360.000). Proyección ROAS 14,5 / ROI 157% es **simulación**.

## Nuestros consumidores y dónde los responde el portal y la app

| Persona | Quién es | Lo que necesita | Dónde se responde |
|---|---|---|---|
| **Camila** (principal) | Visitante de escapada, fin de semana fuera del verano | Saber qué hacer, cuánto toma y cómo empezar, sin crear cuenta | Portal: lugares, fichas, videos. App: P1 Inicio → P3 Rutas → P4 Ficha (máx. 2 toques) → P5 En ruta → P6 Completar → P7 Mi Khiska |
| **Visitante habitual / segunda vivienda** | Ya conoce la playa | Una razón para venir en invierno | Portal: agenda, "Tu próxima experiencia". App: P8 |
| **Don Héctor** | Vecino mayor (25,1% de la comuna tiene 65+) | Leer sin esfuerzo, no perderse | Modo lectura fácil en portal y app (P9), ficha imprimible, Pasaporte de papel |
| **Vale** | Joven local | Participar rápido, sentir que su aporte cuenta | "Pincha tu curiosidad" / intereses (P2), "Propón un lugar" (P10), redes |
| **Rosa** | Oficio y comercio local | Ser visible para quien ya recorre | Dimensión "Memoria y sabores", la caleta; beneficios solo con acuerdo |

Pantallas de la app (P1–P10): Inicio · ¿Qué te gustaría descubrir? · Rutas · Ficha · En ruta · Completar ·
Mi Khiska · Tu próxima experiencia · Lectura fácil · Propón un lugar. La app tiene un **modo prueba**
(registra tareas, toques, tiempo y dudas) que se usó solo dentro del equipo.

## Plan de mejora acordado (23/11/2026)

1. **Montaje** en GitHub + Claude Code. ✔
2. **Portal:** ✔ (23/11) entrada por persona ("¿Cómo quieres vivir El Quisco?"), sección de videos **Mira** (`js/videos.js`), lugares, Khiska, Propón un lugar y agenda. El sitio pasa a ser el lugar donde se ve, reproduce, encuentra y redirige a todo el contenido
   (lugares, Khiska, **videos**, agenda, redes). Organizarlo por lo que necesita cada persona.
3. **App:** integrarla con la identidad del portal, para que se sientan como una sola experiencia.
4. **Pulido para el examen:** modo presentación (ver `CLAUDE.md`).
5. **Publicación:** GitHub Pages, https://nicocsuarez-rgb.github.io/khiska-el-quisco/ (activo).

## Videos

- Hay **un video listo**: `assets/video/v00-el-quisco-desde-un-solo-lugar.mp4` (38 s, 1080×1920),
  doblado por Benjamín con IA.
- Los demás videos de la grilla **no están producidos**. El equipo quiere generarlos **sin grabar**
  (texto, ilustraciones, capturas del portal y la app, voz con IA), como el reel.
- **Grilla v2 (23/11/2026):** `fuentes/grilla-contenidos.xlsx` con audiencias por persona, destinos del portal/app,
  columna "Cómo se produce", pestaña **Estilo de video** (basada en el reel) y **Guiones de video** V00–V16.
  El reel existente es **V00** (15/07, "Ahora El Quisco se puede explorar desde un solo lugar").
- **Grilla v3:** 41 piezas, tráiler V01 el 01/07, reel existente V00 el 15/07. **Videos prioritarios para el portal:**
  V01 tráiler, V00 (listo), V07 "Elige, prepara y comienza", V12 "Una ruta completada hace florecer tu Khiska".
  Prompt listo en `_proyecto/prompts/producir-videos.md`.
- El reel V00 tiene **voz IA que lee el mismo texto en pantalla** + música (lo hizo Benjamín).
- **Influencer (Community Manager):** Francisco "Chapu" Puelles, actor y deportista outdoor (escalada y trekking; Meganoticias, 2022).
  Según Fernanda tiene casa en El Quisco y va a escalar. Su hostal "La Tabla" en El Quisco **ya cerró**: no mencionarlo.
  Es una **propuesta académica: no se le contacta.** Se presenta como el influencer ideal, con guion y storyboard ilustrado
  (sin su imagen ni su voz), piezas V17 y V18 de la grilla. Si el proyecto avanza, se le invitaría a grabar.
- El dossier es privado (`_proyecto/dossier.html`).
- Regla: no fabricar testimonios ni "vecinos" con voz de IA presentados como reales. Las piezas de
  testimonio/UGC de la grilla necesitan personas reales o cambiar de formato.

## Pendientes conocidos

- Cuenta oficial de Instagram por confirmar (la propuesta menciona `@miodestinoelquisco`; una historia muestra `destinoelquisco`).
- Botón "Leer la propuesta completa" del dossier apunta a un artifact privado de claude.ai.
- Confirmar con Fernanda y Benjamín la regla de "Haz florecer tu Khiska".
