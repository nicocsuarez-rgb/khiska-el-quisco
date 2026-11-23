/* El Quisco · Experiencia Khiska — interacciones
   Sin dependencias. Todo funciona abriendo index.html localmente. */
(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.add("js");

  /* Almacenamiento seguro: puede fallar en modo privado o con datos bloqueados */
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* sin persistencia */ } },
    del: function (k) { try { window.localStorage.removeItem(k); } catch (e) { /* nada */ } }
  };

  /* ---------- Año en el pie ---------- */
  document.querySelectorAll("[data-anio]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Menú móvil ---------- */
  var toggle = document.querySelector(".menu-toggle");
  var lista = document.getElementById("menu-principal");
  if (toggle && lista) {
    var cerrar = function () { toggle.setAttribute("aria-expanded", "false"); lista.setAttribute("data-abierto", "false"); };
    toggle.addEventListener("click", function () {
      var abierto = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!abierto));
      lista.setAttribute("data-abierto", String(!abierto));
      if (!abierto) { var primero = lista.querySelector("a"); if (primero) primero.focus(); }
    });
    lista.addEventListener("click", function (e) { if (e.target.closest("a")) cerrar(); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") { cerrar(); toggle.focus(); }
    });
    window.matchMedia("(min-width: 941px)").addEventListener("change", function (m) { if (m.matches) cerrar(); });
  }

  /* ---------- Modo lectura fácil (P9) ---------- */
  var btnLectura = document.querySelector(".btn-lectura");
  var aplicarLectura = function (activo) {
    doc.classList.toggle("lectura-facil", activo);
    if (btnLectura) btnLectura.setAttribute("aria-pressed", String(activo));
  };
  aplicarLectura(store.get("khiska-lectura-facil") === "1");
  if (btnLectura) {
    btnLectura.addEventListener("click", function () {
      var activo = !doc.classList.contains("lectura-facil");
      aplicarLectura(activo);
      store.set("khiska-lectura-facil", activo ? "1" : "0");
    });
  }

  /* ---------- Tarjetas: revelar descripción con clic, toque o teclado ---------- */
  document.querySelectorAll(".tarjeta__toggle").forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute("aria-controls"));
    if (!panel) return;
    btn.addEventListener("click", function () {
      var abierto = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!abierto));
      panel.hidden = abierto;
      btn.firstChild.textContent = abierto ? "Ver descripción " : "Ocultar descripción ";
    });
  });

  /* ---------- Filtro por dimensión (P2 y P3) ---------- */
  document.querySelectorAll("[data-filtro]").forEach(function (grupo) {
    var objetivo = document.getElementById(grupo.getAttribute("data-filtro"));
    if (!objetivo) return;
    var chips = grupo.querySelectorAll(".chip[data-dimension]");
    var vivo = document.getElementById(grupo.getAttribute("data-resultado"));
    var enlace = document.getElementById(grupo.getAttribute("data-enlace"));

    var aplicar = function (dim, guardar) {
      var visibles = 0;
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.getAttribute("data-dimension") === dim)); });
      objetivo.querySelectorAll(".tarjeta").forEach(function (t) {
        var dims = (t.getAttribute("data-dimension") || "").split(" ");
        var ver = dim === "todo" || dims.indexOf(dim) !== -1;
        t.hidden = !ver;
        if (ver) visibles++;
      });
      if (vivo) vivo.textContent = visibles === 1 ? "Se muestra 1 lugar." : "Se muestran " + visibles + " lugares.";
      if (enlace) enlace.setAttribute("href", dim === "todo" ? "rutas.html" : "rutas.html?dimension=" + encodeURIComponent(dim));
      if (guardar) store.set("khiska-interes", dim);
    };

    chips.forEach(function (c) {
      c.addEventListener("click", function () { aplicar(c.getAttribute("data-dimension"), true); });
    });

    var inicial = "todo";
    var param = new URLSearchParams(window.location.search).get("dimension");
    var validas = Array.prototype.map.call(chips, function (c) { return c.getAttribute("data-dimension"); });
    if (param && validas.indexOf(param) !== -1) inicial = param;
    else if (grupo.hasAttribute("data-recordar") && validas.indexOf(store.get("khiska-interes")) !== -1) inicial = store.get("khiska-interes");
    aplicar(inicial, false);
  });

  /* Saltar la pregunta de intereses */
  document.querySelectorAll("[data-saltar]").forEach(function (a) {
    a.addEventListener("click", function () { store.del("khiska-interes"); });
  });

  /* ---------- Imprimir ficha ---------- */
  document.querySelectorAll("[data-imprimir]").forEach(function (b) {
    b.addEventListener("click", function () { window.print(); });
  });

  /* ---------- Formulario "Propón un lugar" (P10) ---------- */
  var form = document.getElementById("form-propuesta");
  if (form) {
    var estado = document.getElementById("form-estado");
    var copiar = document.getElementById("copiar-propuesta");
    var reglas = {
      lugar: function (v) { return v.trim().length >= 3 ? "" : "Escribe el nombre del lugar (mínimo 3 caracteres)."; },
      motivo: function (v) { return v.trim().length >= 20 ? "" : "Cuéntanos un poco más: mínimo 20 caracteres."; },
      correo: function (v) { return !v.trim() || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? "" : "Revisa el formato del correo (ejemplo: nombre@correo.cl)."; },
      consentimiento: function (v, el) { return el.checked ? "" : "Necesitamos tu autorización para revisar la propuesta."; }
    };
    var validar = function (el) {
      var regla = reglas[el.name];
      if (!regla) return true;
      var msg = regla(el.value, el);
      var err = document.getElementById("error-" + el.name);
      el.setAttribute("aria-invalid", msg ? "true" : "false");
      if (err) err.textContent = msg;
      return !msg;
    };
    Object.keys(reglas).forEach(function (n) {
      var el = form.elements[n];
      if (!el) return;
      el.addEventListener("blur", function () { if (el.value || el.type === "checkbox") validar(el); });
      el.addEventListener("input", function () { if (el.getAttribute("aria-invalid") === "true") validar(el); });
      el.addEventListener("change", function () { if (el.type === "checkbox") validar(el); });
    });

    var textoPropuesta = function () {
      return "Propuesta de lugar para Khiska\n" +
        "Lugar: " + form.elements.lugar.value.trim() + "\n" +
        "Por qué: " + form.elements.motivo.value.trim() + "\n" +
        (form.elements.nombre.value.trim() ? "Nombre: " + form.elements.nombre.value.trim() + "\n" : "") +
        (form.elements.correo.value.trim() ? "Correo: " + form.elements.correo.value.trim() + "\n" : "");
    };
    var mostrar = function (tipo, html) {
      estado.className = "estado-form estado-form--" + tipo;
      estado.innerHTML = html;
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true, primero = null;
      Object.keys(reglas).forEach(function (n) {
        var el = form.elements[n];
        if (el && !validar(el)) { ok = false; if (!primero) primero = el; }
      });
      if (!ok) {
        mostrar("error", "Hay campos por revisar. Corrígelos y vuelve a intentarlo.");
        primero.focus();
        return;
      }
      var endpoint = form.getAttribute("data-endpoint");
      if (!endpoint) {
        /* Sin servicio configurado: no se simula un envío exitoso */
        mostrar("info", "<strong>Tu propuesta está completa, pero no se ha enviado.</strong> El servicio de recepción aún no está configurado en este sitio. Puedes copiar el texto para guardarlo o compartirlo.");
        if (copiar) copiar.hidden = false;
        return;
      }
      var boton = form.querySelector("[type=submit]");
      boton.disabled = true;
      mostrar("info", "Enviando…");
      fetch(endpoint, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          mostrar("exito", "<strong>¡Gracias!</strong> Recibimos tu propuesta. El equipo la revisará antes de considerarla para una ruta futura.");
          form.reset();
        })
        .catch(function () {
          mostrar("error", "No pudimos enviar tu propuesta. Revisa tu conexión e inténtalo otra vez.");
          if (copiar) copiar.hidden = false;
        })
        .then(function () { boton.disabled = false; });
    });

    if (copiar) {
      copiar.addEventListener("click", function () {
        var texto = textoPropuesta();
        var listo = function () { mostrar("exito", "Texto copiado al portapapeles."); };
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(texto).then(listo, function () { window.prompt("Copia el texto:", texto); });
        } else {
          window.prompt("Copia el texto de tu propuesta:", texto);
        }
      });
    }
  }

  /* ---------- Demostración Mi Khiska (P6, P7, P8) ---------- */
  var jardin = document.getElementById("jardin-demo");
  if (jardin) {
    var base = jardin.getAttribute("data-base") || "";
    var ESTADOS = {
      capullo: { img: "assets/img/flor-capullo.webp", texto: "Capullo cerrado · ruta no iniciada", accion: "Iniciar ruta (demo)" },
      parcial: { img: "assets/img/flor-parcial.webp", texto: "Apertura parcial · ruta iniciada", accion: "Completar ruta (demo)" },
      abierta: { img: "assets/img/flor-abierta.webp", texto: "Flor abierta · ruta completada", accion: "Reiniciar (demo)" }
    };
    var ORDEN = ["capullo", "parcial", "abierta"];
    var parcelas = jardin.querySelectorAll(".parcela");
    var resumen = document.getElementById("demo-resumen");
    var siguiente = document.getElementById("demo-siguiente");
    var sonido = document.getElementById("demo-sonido");
    var guardado = {};
    try { guardado = JSON.parse(store.get("khiska-demo") || "{}") || {}; } catch (e) { guardado = {}; }

    var tono = function () {
      if (!sonido || !sonido.checked) return;
      try {
        var Ctx = window.AudioContext || window.webkitAudioContext;
        var ctx = new Ctx(), t = ctx.currentTime;
        [523.25, 659.25, 783.99].forEach(function (f, i) {
          var o = ctx.createOscillator(), g = ctx.createGain();
          o.type = "sine"; o.frequency.value = f;
          g.gain.setValueAtTime(0, t + i * .09);
          g.gain.linearRampToValueAtTime(.08, t + i * .09 + .02);
          g.gain.exponentialRampToValueAtTime(.0001, t + i * .09 + .6);
          o.connect(g); g.connect(ctx.destination); o.start(t + i * .09); o.stop(t + i * .09 + .65);
        });
        if (navigator.vibrate) navigator.vibrate(40);
      } catch (e) { /* audio no disponible */ }
    };

    var pintar = function (p, est, animar) {
      var d = ESTADOS[est];
      var img = p.querySelector(".parcela__flor img");
      p.setAttribute("data-estado", est);
      if (!animar) p.classList.add("sin-animar");
      img.src = base + d.img;
      p.querySelector(".parcela__estado").textContent = d.texto;
      var b = p.querySelector("button");
      b.textContent = d.accion;
      b.setAttribute("aria-label", d.accion + ": " + p.querySelector("h3").textContent);
    };

    var actualizar = function () {
      var total = parcelas.length, hechas = 0, iniciadas = 0;
      parcelas.forEach(function (p) {
        var e = p.getAttribute("data-estado");
        if (e === "abierta") hechas++;
        if (e === "parcial") iniciadas++;
      });
      var faltan = total - hechas;
      resumen.textContent = "Flores abiertas: " + hechas + " de " + total + ". " +
        (iniciadas ? "Rutas en curso: " + iniciadas + ". " : "") +
        (faltan === 0 ? "Completaste todas las rutas de la demostración." : "Te " + (faltan === 1 ? "queda 1 ruta" : "quedan " + faltan + " rutas") + " por descubrir.");
      if (siguiente) siguiente.hidden = hechas === 0;
    };

    parcelas.forEach(function (p) {
      var id = p.getAttribute("data-ruta");
      var est = ORDEN.indexOf(guardado[id]) !== -1 ? guardado[id] : "capullo";
      pintar(p, est, false);
      p.querySelector("button").addEventListener("click", function () {
        var actual = p.getAttribute("data-estado");
        var nuevo = ORDEN[(ORDEN.indexOf(actual) + 1) % ORDEN.length];
        p.classList.remove("sin-animar");
        pintar(p, nuevo, true);
        if (nuevo === "abierta") tono();
        guardado[id] = nuevo;
        store.set("khiska-demo", JSON.stringify(guardado));
        actualizar();
      });
    });

    var reset = document.getElementById("demo-reiniciar");
    if (reset) reset.addEventListener("click", function () {
      guardado = {};
      store.del("khiska-demo");
      parcelas.forEach(function (p) { pintar(p, "capullo", false); });
      actualizar();
      resumen.focus();
    });
    actualizar();
  }
})();
