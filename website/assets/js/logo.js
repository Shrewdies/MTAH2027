/* The Shrewdies: animated wordmark behaviour. Markup: _includes/logo.html. */
(function () {
  "use strict";

  var logos = Array.prototype.slice.call(document.querySelectorAll(".sh-logo"));
  if (!logos.length) return;

  var VB_W = 2175.545;
  var VB_H = 338.887;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  var spots = null;

  function rand(min, max) { return min + Math.random() * (max - min); }

  /* Glint positions: points on the letterforms, biased towards edges that face the light. */
  function sampleSpots(svg) {
    var ctx = document.createElement("canvas").getContext("2d");
    if (!ctx || typeof Path2D === "undefined") return [];
    var shapes = Array.prototype.map.call(svg.querySelectorAll("defs path"), function (p) {
      return new Path2D(p.getAttribute("d"));
    });
    function inside(x, y) {
      for (var i = 0; i < shapes.length; i++) if (ctx.isPointInPath(shapes[i], x, y)) return true;
      return false;
    }
    var out = [];
    for (var n = 0; n < 6000 && out.length < 160; n++) {
      var x = rand(8, VB_W - 8);
      var y = rand(4, VB_H - 8);
      if (!inside(x, y)) continue;
      var edge = !inside(x - 9, y - 12) || !inside(x + 9, y - 12);
      if (edge || Math.random() < 0.15) {
        out.push([(x / VB_W * 100).toFixed(2) + "%", (y / VB_H * 100).toFixed(2) + "%"]);
      }
    }
    return out;
  }

  function moveGlint(glint) {
    if (!spots || !spots.length) return;
    var s = spots[(Math.random() * spots.length) | 0];
    glint.style.left = s[0];
    glint.style.top = s[1];
  }

  var timing = {
    hero: { glint: [2.6, 4.2], wait: 1.6, sheen: null },
    header: { glint: [4.5, 7.5], wait: 0.6, sheen: [1, 6] },
    footer: { glint: [6, 9], wait: 1, sheen: [2, 10] }
  };

  function variantOf(logo) {
    var m = /sh-logo--(\w+)/.exec(logo.className);
    return m && timing[m[1]] ? m[1] : "header";
  }

  function setup(logo) {
    var t = timing[variantOf(logo)];
    if (t.sheen) logo.style.setProperty("--sh-sheen-delay", rand(t.sheen[0], t.sheen[1]).toFixed(2) + "s");
    var glints = logo.querySelectorAll(".sh-logo__glint");
    Array.prototype.forEach.call(glints, function (g, i) {
      var period = rand(t.glint[0], t.glint[1]);
      g.style.setProperty("--sh-glint-t", period.toFixed(2) + "s");
      g.style.setProperty("--sh-glint-delay", (t.wait + period * i / glints.length + rand(0, 0.5)).toFixed(2) + "s");
    });
    logo.addEventListener("animationiteration", function (e) {
      if (e.target.classList && e.target.classList.contains("sh-logo__glint")) moveGlint(e.target);
    });
  }

  /* Pause everything off-screen and in hidden tabs. */
  function syncPause(logo) {
    logo.classList.toggle("is-paused", document.hidden || logo.getAttribute("data-sh-view") === "0");
  }

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        e.target.setAttribute("data-sh-view", e.isIntersecting ? "1" : "0");
        syncPause(e.target);
      });
    }, { rootMargin: "80px 0px" });
    logos.forEach(function (l) { io.observe(l); });
  }
  document.addEventListener("visibilitychange", function () { logos.forEach(syncPause); });

  /* Hero light follows a fine pointer: rim light, extrusion, floodlight and a slight tilt. */
  function trackPointer() {
    var heroes = logos.filter(function (l) { return /sh-logo--hero/.test(l.className); });
    if (!heroes.length) return;
    var px = 0;
    var py = 0;
    var queued = false;
    var props = ["--sh-lx", "--sh-ly", "--sh-px", "--sh-py", "--sh-tx", "--sh-ty"];

    function clamp(v) { return v < -1 ? -1 : v > 1 ? 1 : v; }

    function frame() {
      queued = false;
      heroes.forEach(function (h) {
        if (h.classList.contains("is-paused")) return;
        var r = h.getBoundingClientRect();
        var dx = clamp((px - (r.left + r.width / 2)) / (r.width * 0.6));
        var dy = clamp((py - (r.top + r.height / 2)) / (r.height * 2.4));
        h.style.setProperty("--sh-lx", (dx * 0.9).toFixed(3));
        h.style.setProperty("--sh-ly", (-0.55 + dy * 0.45).toFixed(3));
        h.style.setProperty("--sh-px", dx.toFixed(3));
        h.style.setProperty("--sh-py", dy.toFixed(3));
        h.style.setProperty("--sh-tx", (dx * 5).toFixed(2));
        h.style.setProperty("--sh-ty", (-dy * 4).toFixed(2));
      });
    }

    window.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse" && e.pointerType !== "pen") return;
      px = e.clientX;
      py = e.clientY;
      if (!queued) { queued = true; requestAnimationFrame(frame); }
    }, { passive: true });

    document.addEventListener("mouseleave", function () {
      heroes.forEach(function (h) { props.forEach(function (p) { h.style.removeProperty(p); }); });
    });
  }

  if (reduced.matches) return;

  logos.forEach(setup);

  var schedule = window.requestIdleCallback || function (fn) { return setTimeout(fn, 200); };
  schedule(function () {
    var svg = logos[0].querySelector("svg");
    spots = svg ? sampleSpots(svg) : [];
  });

  if (finePointer.matches) trackPointer();
})();
