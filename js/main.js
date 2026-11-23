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

  /* Botón "Activar lectura fácil" de la sección Para ti */
  document.querySelectorAll("[data-activar-lectura]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      if (!doc.classList.contains("lectura-facil") && btnLectura) btnLectura.click();
      window.scrollTo(0, 0);
    });
  });

  /* ---------- Videos (js/videos.js) ---------- */
  var listaVideos = document.getElementById("lista-videos");
  if (listaVideos && Array.isArray(window.KHISKA_VIDEOS) && window.KHISKA_VIDEOS.length) {
    var esc = function (t) { return String(t || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
    listaVideos.innerHTML = window.KHISKA_VIDEOS.map(function (v, i) {
      var clase = "video-card" + (i === 0 ? " video-card--destacado" : "");
      var poster = v.poster ? ' poster="' + esc(v.poster) + '"' : "";
      var medio = v.archivo
        ? '<video controls playsinline preload="metadata"' + poster + '><source src="' + esc(v.archivo) + '" type="video/mp4"></video>'
        : '<a class="video-card__enlace" href="' + esc(v.enlace) + '" target="_blank" rel="noopener">' +
          (v.poster ? '<img src="' + esc(v.poster) + '" alt="" loading="lazy">' : "") + '<span class="video-card__play" aria-hidden="true">▶</span><span class="visually-hidden">Ver video: ' + esc(v.titulo) + ' (se abre en otra pestaña)</span></a>';
      return '<figure class="' + clase + '">' + medio + '<figcaption><strong>' + esc(v.titulo) + "</strong></figcaption></figure>";
    }).join("");
  }

  /* ---------- Tarjetas: revelar descripción con clic, toque o teclado ---------- */
  document.querySelectorAll(".tarjeta__toggle").forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute("aria-controls"));
    if (!panel) return;
    btn.addEventListener("click", function () {
      var abierto = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!abierto));
      panel.hidden = abierto;
      btn.firstChild.textContent = abierto ? "Ver más " : "Ver menos ";
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
        mostrar("exito", "<strong>¡Gracias!</strong> Tu propuesta está lista. Copia el texto para compartirla con el equipo.");
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

  /* ---------- Portada animada: video de fondo, paralaje y pausa ---------- */
  var hero = document.querySelector(".hero");
  if (hero) {
    var quieto = window.matchMedia("(prefers-reduced-motion: reduce)");
    var fondo = hero.querySelector(".hero__fondo");
    var cactus = hero.querySelector(".hero__cactus");
    var pausa = hero.querySelector(".hero__pausa");
    var video = null;
    var cfg = window.KHISKA_FONDO || {};
    var ahorro = navigator.connection && navigator.connection.saveData;

    if (fondo && cfg.video && !quieto.matches && !ahorro) {
      video = document.createElement("video");
      video.className = "hero__video";
      video.muted = true; video.loop = true; video.playsInline = true; video.autoplay = true;
      video.setAttribute("muted", ""); video.setAttribute("playsinline", "");
      if (cfg.poster) video.poster = cfg.poster;
      video.src = cfg.video;
      video.addEventListener("canplay", function () { hero.classList.add("hero--con-video"); }, { once: true });
      video.addEventListener("error", function () { video.remove(); video = null; hero.classList.remove("hero--con-video"); });
      fondo.appendChild(video);
    }

    if (pausa) {
      pausa.addEventListener("click", function () {
        var pausado = !hero.classList.contains("hero--pausado");
        hero.classList.toggle("hero--pausado", pausado);
        pausa.setAttribute("aria-pressed", String(pausado));
        pausa.textContent = pausado ? "Reanudar movimiento" : "Pausar movimiento";
        if (video) { if (pausado) video.pause(); else video.play().catch(function () {}); }
      });
    }

    /* Paralaje suave: el fondo baja más lento que el contenido */
    var pendiente = false;
    var moverPortada = function () {
      pendiente = false;
      var y = window.scrollY;
      if (y > window.innerHeight * 1.2) return;
      if (fondo) fondo.style.transform = "translate3d(0," + (y * 0.3).toFixed(1) + "px,0)";
      if (cactus) cactus.style.translate = "0 " + (y * 0.12).toFixed(1) + "px";
    };
    window.addEventListener("scroll", function () {
      if (quieto.matches || pendiente) return;
      pendiente = true;
      window.requestAnimationFrame(moverPortada);
    }, { passive: true });
  }

  /* ---------- Lluvia de flores: premio y huevo de pascua ----------
     window.KhiskaLluvia() se puede llamar desde cualquier logro. */
  var base = (document.currentScript && document.currentScript.src || "").replace(/js\/main\.js.*$/, "");
  var lluviaDeFlores = function (cantidad) {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return 0;
    cantidad = cantidad || (window.innerWidth < 600 ? 45 : 80);
    var capa = document.createElement("div");
    capa.className = "lluvia";
    capa.setAttribute("aria-hidden", "true");
    var alto = window.innerHeight, ancho = window.innerWidth, maximo = 0;
    for (var i = 0; i < cantidad; i++) {
      var img = document.createElement("img");
      img.src = base + "assets/img/" + (Math.random() < .72 ? "flor-abierta.webp" : "flor-parcial.webp");
      img.alt = "";
      var tam = 26 + Math.random() * 48;
      img.style.width = tam + "px";
      capa.appendChild(img);
      var x = Math.random() * ancho, deriva = (Math.random() - .5) * 220;
      var giro = (Math.random() < .5 ? -1 : 1) * (180 + Math.random() * 360);
      var dur = 2600 + Math.random() * 2200, espera = Math.random() * 1300;
      maximo = Math.max(maximo, dur + espera);
      img.animate([
        { transform: "translate(" + x + "px," + (-tam - 20) + "px) rotate(0deg)", opacity: 1 },
        { transform: "translate(" + (x + deriva * .6) + "px," + (alto * .5) + "px) rotate(" + giro * .5 + "deg)", opacity: 1, offset: .5 },
        { transform: "translate(" + (x + deriva) + "px," + (alto + 40) + "px) rotate(" + giro + "deg)", opacity: .85 }
      ], { duration: dur, delay: espera, easing: "cubic-bezier(.35,.1,.55,1)", fill: "both" });
    }
    document.body.appendChild(capa);
    setTimeout(function () { capa.remove(); }, maximo + 200);
    return maximo;
  };
  window.KhiskaLluvia = lluviaDeFlores;

  /* Pinchar a Khiska en la portada: llueven flores y te lleva a "Pincha tu curiosidad" */
  var cactusPortada = document.querySelector("[data-pinchar]");
  if (cactusPortada) {
    cactusPortada.addEventListener("click", function (e) {
      var destino = document.querySelector(cactusPortada.getAttribute("href"));
      var dura = lluviaDeFlores();
      if (!dura || !destino) return;
      e.preventDefault();
      if (cactusPortada.classList.contains("pinchado")) return;
      cactusPortada.classList.add("pinchado");
      setTimeout(function () {
        cactusPortada.classList.remove("pinchado");
        var titulo = destino.querySelector("h2") || destino;
        titulo.setAttribute("tabindex", "-1");
        destino.scrollIntoView({ behavior: "smooth", block: "start" });
        titulo.focus({ preventScroll: true });
      }, 1900);
    });
  }

  /* ---------- Movimiento al bajar: todo va apareciendo ---------- */
  var sinMovimiento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var cabecera = document.querySelector(".cabecera");
  var barra = document.createElement("div");
  barra.className = "avance"; barra.setAttribute("aria-hidden", "true");
  document.body.appendChild(barra);
  var marcoPendiente = false;
  var alBajar = function () {
    marcoPendiente = false;
    var y = window.scrollY, total = document.documentElement.scrollHeight - window.innerHeight;
    if (cabecera) cabecera.classList.toggle("cabecera--compacta", y > 30);
    barra.style.setProperty("--avance", total > 0 ? Math.min(1, y / total).toFixed(4) : 0);
  };
  window.addEventListener("scroll", function () {
    if (!marcoPendiente) { marcoPendiente = true; window.requestAnimationFrame(alBajar); }
  }, { passive: true });
  alBajar();

  if (!sinMovimiento && "IntersectionObserver" in window) {
    /* [selector, variante]: los hijos de un mismo grupo aparecen en cascada */
    var grupos = [
      [".personas-grid > *, .grid-tarjetas > *, .videos > *, .estados > *, .agenda > *, .pie__grid > *", ""],
      [".pasos > li, .formulario > .campo, .formulario > .acciones", "izq"],
      [".seccion__cabecera, .cabecera-pagina > *, .ficha-hero > *, .ficha-cuerpo > *, .curiosidad > *, .comunidad > *, .pasaporte > *, .seccion > .contenedor > .aviso", ""],
      [".khiska__ilustracion, .ficha-hero__media, .propon__img, .estado-form", "zoom"],
      [".khiska > div:not(.khiska__ilustracion)", "der"]
    ];
    var marcados = [];
    grupos.forEach(function (g) {
      document.querySelectorAll(g[0]).forEach(function (el) {
        if (el.closest(".hero") || el.classList.contains("revelar") || el.closest(".revelar")) return;
        var hermanos = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
        el.classList.add("revelar");
        if (g[1]) el.classList.add("revelar--" + g[1]);
        el.style.setProperty("--i", Math.min(hermanos, 5));
        marcados.push(el);
      });
    });
    var vigia = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.add("visible");
        vigia.unobserve(el);
        /* Terminado el efecto, el elemento vuelve a su comportamiento normal */
        setTimeout(function () {
          el.classList.remove("revelar", "visible", "revelar--zoom", "revelar--izq", "revelar--der");
          el.style.removeProperty("--i");
        }, 900 + Math.min(5, +el.style.getPropertyValue("--i") || 0) * 90);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    marcados.forEach(function (el) { vigia.observe(el); });
    /* Si algo queda oculto (impresión, saltos con ancla), se muestra igual */
    window.addEventListener("beforeprint", function () { marcados.forEach(function (el) { el.classList.add("visible"); }); });
  }
})();
