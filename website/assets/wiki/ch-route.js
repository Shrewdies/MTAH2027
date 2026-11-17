/* The reading route (Challenges). On screens without hover, play a tile's diagram while the tile is in view.
   Hover and keyboard focus are handled in CSS; reduced motion and the site's pause button keep everything still. */
(function () {
  "use strict";
  var tiles = document.querySelectorAll("[data-ch-tile]");
  if (!tiles.length || !("IntersectionObserver" in window) || !window.matchMedia) return;
  var noHover = window.matchMedia("(hover: none)");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!noHover.matches || reduce.matches) return;

  var watch = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      entry.target.classList.toggle("is-live", entry.isIntersecting && entry.intersectionRatio >= 0.6);
    });
  }, { threshold: [0, 0.6, 1], rootMargin: "-12% 0px -12% 0px" });
  tiles.forEach(function (tile) { watch.observe(tile); });
})();
