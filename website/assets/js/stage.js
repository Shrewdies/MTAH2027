/* The Shrewdies — background stage: pause control, hidden-tab pause, gentle pointer parallax. */
(function () {
  "use strict";

  var stage = document.querySelector("[data-stage]");
  if (!stage) return;

  var root = document.documentElement;
  var toggle = document.querySelector("[data-motion-toggle]");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  var KEY = "sh-motion";
  var userPaused = false;
  try { userPaused = localStorage.getItem(KEY) === "paused"; } catch (e) { /* storage unavailable */ }

  function apply() {
    stage.classList.toggle("is-paused", userPaused || document.hidden);
    root.classList.toggle("sh-motion-paused", userPaused);
    if (toggle) {
      toggle.hidden = reduce.matches;
      toggle.setAttribute("aria-pressed", String(userPaused));
      var label = toggle.querySelector("[data-motion-label]");
      if (label) label.textContent = userPaused ? "Play background motion" : "Pause background motion";
    }
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      userPaused = !userPaused;
      try { localStorage.setItem(KEY, userPaused ? "paused" : "playing"); } catch (e) { /* not remembered */ }
      apply();
    });
  }
  document.addEventListener("visibilitychange", apply);
  if (reduce.addEventListener) reduce.addEventListener("change", apply);
  apply();

  /* Parallax: layers shift a few pixels with the pointer. */
  var layers = stage.querySelectorAll("[data-depth]");
  if (!layers.length || !finePointer.matches) return;
  var tx = 0, ty = 0, queued = false;
  function render() {
    queued = false;
    if (reduce.matches || userPaused) return;
    for (var i = 0; i < layers.length; i++) {
      var d = Number(layers[i].getAttribute("data-depth")) || 1;
      layers[i].style.setProperty("--px", (tx * d * 10).toFixed(1) + "px");
      layers[i].style.setProperty("--py", (ty * d * 8).toFixed(1) + "px");
    }
  }
  window.addEventListener("pointermove", function (e) {
    tx = e.clientX / window.innerWidth - 0.5;
    ty = e.clientY / window.innerHeight - 0.5;
    if (!queued) { queued = true; window.requestAnimationFrame(render); }
  }, { passive: true });
})();
