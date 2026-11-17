/* Member pages and hubs: reveal on scroll and count-up numbers. Content is complete without it. */
(function () {
  "use strict";
  var root = document.querySelector("[data-member], [data-why]");
  if (!root || !("IntersectionObserver" in window)) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  root.classList.add("mb-anim");

  function countUp(el) {
    var end = parseInt(el.getAttribute("data-count"), 10);
    if (!(end > 0)) return;
    var from = end >= 1000 ? end - 40 : 0;
    var start = Date.now(), dur = Math.min(1600, 700 + end * 60);
    el.textContent = from;
    (function step() {
      var p = Math.min((Date.now() - start) / dur, 1);
      el.textContent = Math.round(from + (end - from) * (1 - Math.pow(1 - p, 3)));
      if (p < 1) setTimeout(step, 30);
    })();
  }

  var targets = root.querySelectorAll(".mb-stats, [data-reveal-item], [data-reveal-group], [data-timeline]");
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-in");
      entry.target.querySelectorAll("[data-count]").forEach(countUp);
      io.unobserve(entry.target);
    });
  }, { threshold: 0.18, rootMargin: "0px 0px -6% 0px" });
  targets.forEach(function (t) { io.observe(t); });
})();
