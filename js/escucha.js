/* "Escucha este lugar": reproductor de paisajes sonoros y relatos en voz local.
   Lee window.KHISKA_AUDIOS (js/audios.js). Nada suena solo: siempre lo inicia la persona.
   Cada audio aparece solo si su archivo carga; un relato además necesita transcripción y crédito.
   Si no hay ninguno válido, el contenedor sigue oculto (modo presentación).

   Uso: KhiskaEscucha.montar(elemento, { lugar: "el-batro", base: "../", grande: false, titulo: "Escucha este lugar" }) */
(function () {
  "use strict";
  var sonando = null;

  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function tiempo(s) { s = Math.max(0, Math.floor(s || 0)); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); }
  function valido(a) {
    if (!a || !a.archivo || !a.titulo) return false;
    if (a.tipo === "relato") return !!(String(a.transcripcion || "").trim() && String(a.credito || "").trim());
    return a.tipo === "paisaje";
  }
  var ICONO_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>';
  var ICONO_PAUSA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z" fill="currentColor"/></svg>';

  function item(a, base, grande) {
    var li = document.createElement("li");
    li.className = "escucha__item escucha__item--" + a.tipo + (grande ? " escucha__item--grande" : "");
    li.hidden = true;
    var credito = a.tipo === "relato" ? '<p class="escucha__credito">Voz de ' + esc(a.credito) + "</p>" : (a.credito ? '<p class="escucha__credito">' + esc(a.credito) + "</p>" : "");
    li.innerHTML =
      '<button class="escucha__play" type="button" aria-label="Escuchar: ' + esc(a.titulo) + '">' + ICONO_PLAY + "</button>" +
      '<div class="escucha__cuerpo"><p class="escucha__titulo">' + esc(a.titulo) + "</p>" + credito +
      '<div class="escucha__avance"><input class="escucha__barra" type="range" min="0" max="100" step="0.1" value="0" aria-label="Avance de ' + esc(a.titulo) + '"><span class="escucha__tiempo">0:00</span></div>' +
      (String(a.transcripcion || "").trim() ? '<details class="escucha__transcripcion"><summary>Leer la transcripción</summary><p>' + esc(a.transcripcion) + "</p></details>" : "") +
      "</div>";
    var audio = new Audio();
    audio.preload = "metadata";
    var boton = li.querySelector(".escucha__play"), barra = li.querySelector(".escucha__barra"), reloj = li.querySelector(".escucha__tiempo");
    var pintar = function () {
      var p = !audio.paused;
      boton.innerHTML = p ? ICONO_PAUSA : ICONO_PLAY;
      boton.setAttribute("aria-label", (p ? "Pausar: " : "Escuchar: ") + a.titulo);
      li.classList.toggle("escucha__item--sonando", p);
    };
    audio.addEventListener("loadedmetadata", function () {
      li.hidden = false;
      reloj.textContent = tiempo(audio.duration);
      var cont = li.closest("[data-escucha]");
      if (cont) cont.hidden = false;
    });
    audio.addEventListener("timeupdate", function () {
      if (audio.duration) barra.value = audio.currentTime / audio.duration * 100;
      reloj.textContent = tiempo(audio.paused && !audio.currentTime ? audio.duration : audio.currentTime);
    });
    audio.addEventListener("play", function () { if (sonando && sonando !== audio) sonando.pause(); sonando = audio; pintar(); });
    audio.addEventListener("pause", pintar);
    audio.addEventListener("ended", function () { audio.currentTime = 0; pintar(); });
    boton.addEventListener("click", function () { if (audio.paused) audio.play().catch(function () {}); else audio.pause(); });
    barra.addEventListener("input", function () { if (audio.duration) audio.currentTime = barra.value / 100 * audio.duration; });
    audio.src = base + a.archivo;
    return li;
  }

  function montar(cont, op) {
    op = op || {};
    var lista = (window.KHISKA_AUDIOS || []).filter(function (a) { return a.lugar === op.lugar && valido(a); });
    cont.hidden = true;
    if (!lista.length) return;
    /* Primero el paisaje sonoro, después los relatos */
    lista.sort(function (a, b) { return (a.tipo === "relato") - (b.tipo === "relato"); });
    if (!op.sinTitulo) {
      var h = document.createElement("h2");
      h.className = "escucha__encabezado";
      h.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 10v4M8 7v10M12 4v16M16 7v10M20 10v4" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>' + esc(op.titulo || "Escucha este lugar");
      cont.appendChild(h);
    }
    var ul = document.createElement("ul");
    ul.className = "escucha__lista";
    lista.forEach(function (a) { ul.appendChild(item(a, op.base || "", op.grande)); });
    cont.appendChild(ul);
  }

  window.KhiskaEscucha = { montar: montar, detener: function () { if (sonando) sonando.pause(); } };
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-escucha]").forEach(function (c) {
      if (c.hasAttribute("data-escucha-manual")) return;
      montar(c, { lugar: c.getAttribute("data-escucha"), base: c.getAttribute("data-base") || "", grande: c.hasAttribute("data-grande"), sinTitulo: c.hasAttribute("data-sin-titulo") });
    });
  });
})();
