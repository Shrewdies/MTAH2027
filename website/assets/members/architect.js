/* Staged diagrams: [data-phases="n"] gains is-live, then is-p1..is-pn in turn, holds, and starts over at is-p1.
   data-step mirrors the caption that belongs to the current phase. Without this script the finished diagram shows. */
(function () {
  "use strict";
  var stages = document.querySelectorAll("[data-phases]");
  if (!stages.length || !("IntersectionObserver" in window)) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var root = document.documentElement;

  Array.prototype.forEach.call(stages, function (el) {
    var count = parseInt(el.getAttribute("data-phases"), 10);
    var steps = (el.getAttribute("data-phase-steps") || "").split(",");
    var tick = parseInt(el.getAttribute("data-phase-ms"), 10) || 1600;
    var hold = 3, at = 1, seen = false;

    function show(phase) {
      for (var i = 1; i <= count; i++) el.classList.toggle("is-p" + i, i <= phase);
      el.setAttribute("data-step", steps[phase - 1] || "");
    }

    el.classList.add("is-live");
    show(1);
    new IntersectionObserver(function (entries) { seen = entries[0].isIntersecting; }, { threshold: 0.2 }).observe(el);
    window.setInterval(function () {
      if (!seen || document.hidden || root.classList.contains("sh-motion-paused")) return;
      at = at % (count + hold) + 1;
      show(Math.min(at, count));
    }, tick);
  });
})();
