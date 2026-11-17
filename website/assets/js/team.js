/* Team page: kit cards (tilt, light, flip, entrance, profile links). */
(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var canHover = window.matchMedia("(hover: hover) and (pointer: fine)");

  /* Tilt and light follow the pointer; the card flips away from the side the pointer came from.
     Keyboard focus flips it, the button or a tap toggles it, and focus leaving flips it back. */
  var cards = document.querySelectorAll("[data-kit-card]");
  var keyboardMode = false;
  document.addEventListener("keydown", function (e) { if (e.key === "Tab") keyboardMode = true; });
  document.addEventListener("pointerdown", function () { keyboardMode = false; });

  cards.forEach(function (card) {
    var btn = card.querySelector(".kit-card__flip");
    var frame = 0;

    function setFlipped(on) {
      card.classList.toggle("is-flipped", on);
      if (btn) btn.setAttribute("aria-pressed", String(on));
    }

    function track(e) {
      var r = card.getBoundingClientRect();
      var x = Math.min(Math.max((e.clientX - r.left) / r.width, 0), 1);
      var y = Math.min(Math.max((e.clientY - r.top) / r.height, 0), 1);
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(function () {
        card.style.setProperty("--ry", ((x - 0.5) * 16).toFixed(2) + "deg");
        card.style.setProperty("--rx", ((0.5 - y) * 12).toFixed(2) + "deg");
        card.style.setProperty("--mx", (x * 100).toFixed(1) + "%");
        card.style.setProperty("--my", (y * 100).toFixed(1) + "%");
        card.style.setProperty("--px", ((x - 0.5) * 2).toFixed(3));
        card.style.setProperty("--py", ((y - 0.5) * 2).toFixed(3));
      });
    }

    function reset() {
      cancelAnimationFrame(frame);
      card.classList.remove("is-tracking");
      ["--rx", "--ry", "--px", "--py"].forEach(function (p) { card.style.removeProperty(p); });
      card.style.setProperty("--lit", "0");
    }

    card.addEventListener("pointerenter", function (e) {
      if (e.pointerType !== "mouse") return;
      var r = card.getBoundingClientRect();
      card.style.setProperty("--flip", e.clientX < r.left + r.width / 2 ? "180deg" : "-180deg");
      if (reduceMotion.matches || !canHover.matches) return;
      card.classList.add("is-tracking");
      card.style.setProperty("--lit", "1");
      track(e);
    });
    card.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse" || reduceMotion.matches || !canHover.matches) return;
      track(e);
    });
    card.addEventListener("pointerleave", reset);

    /* The shirt and the photo both link to the profile. Without hover, the first tap flips the card
       and the back's links navigate. */
    card.addEventListener("click", function (e) {
      if (e.target.closest(".kit-card__flip")) return;
      var link = e.target.closest("a");
      if (link && !link.hasAttribute("data-kit-front")) return;
      /* Safari reports no pointer type on click events: a hover-capable device then counts as a mouse. */
      var byMouse = e.pointerType ? e.pointerType === "mouse" : canHover.matches;
      if (byMouse && canHover.matches) return;
      if (link && card.classList.contains("is-flipped")) return;
      if (link) e.preventDefault();
      setFlipped(link ? true : !card.classList.contains("is-flipped"));
    });
    if (btn) btn.addEventListener("click", function () { setFlipped(!card.classList.contains("is-flipped")); });

    card.addEventListener("focusin", function () { if (keyboardMode) setFlipped(true); });
    card.addEventListener("focusout", function (e) {
      /* A tapped shirt link drops focus by itself once its face is hidden; only focus that really leaves flips the card back. */
      if (e.target.hasAttribute("data-kit-front")) return;
      if (!card.contains(e.relatedTarget)) setFlipped(false);
    });
  });

  if (cards.length && "IntersectionObserver" in window && !reduceMotion.matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-in"); io.unobserve(entry.target); }
      });
    }, { threshold: 0.01 });
    cards.forEach(function (c) { c.setAttribute("data-reveal", ""); io.observe(c); });
  }
})();
