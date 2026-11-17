/* The Shrewdies — small progressive enhancements. No dependencies. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---- Mobile navigation ---- */
  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (navToggle && nav) {
    var setNav = function (open) {
      navToggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    };
    navToggle.addEventListener("click", function () {
      setNav(navToggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { setNav(false); navToggle.focus(); }
    });
  }

  /* ---- Motion embeds: honour reduced motion, offer pause, load Lottie only when needed ---- */
  document.querySelectorAll("[data-motion]").forEach(function (fig) {
    var video = fig.querySelector("video[data-autoplay]");
    var lottieEl = fig.querySelector("[data-lottie]");
    var toggle = fig.querySelector(".motion__toggle");
    var player = null;

    function setPaused(paused) {
      if (!toggle) return;
      toggle.setAttribute("aria-pressed", String(paused));
      toggle.textContent = paused ? "Play" : "Pause";
    }

    if (video) {
      if (!reduceMotion.matches) {
        var p = video.play();
        if (p && p.catch) p.catch(function () { setPaused(true); });
        setPaused(false);
      } else {
        setPaused(true);
      }
      if (toggle) {
        toggle.hidden = false;
        toggle.addEventListener("click", function () {
          if (video.paused) { video.play(); setPaused(false); } else { video.pause(); setPaused(true); }
        });
      }
    }

    if (lottieEl) {
      loadLottie(function (lottie) {
        if (!lottie) { fig.classList.add("is-missing"); return; }
        player = lottie.loadAnimation({
          container: lottieEl, renderer: "svg", loop: true,
          autoplay: !reduceMotion.matches, path: lottieEl.getAttribute("data-lottie")
        });
        player.addEventListener("data_failed", function () { fig.classList.add("is-missing"); });
        if (toggle) {
          toggle.hidden = false;
          setPaused(reduceMotion.matches);
          toggle.addEventListener("click", function () {
            if (player.isPaused) { player.play(); setPaused(false); } else { player.pause(); setPaused(true); }
          });
        }
      });
    }
  });

  var lottieQueue = null;
  function loadLottie(cb) {
    if (window.lottie) return cb(window.lottie);
    if (lottieQueue) return lottieQueue.push(cb);
    lottieQueue = [cb];
    var s = document.createElement("script");
    s.src = "https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js";
    s.async = true;
    s.onload = function () { lottieQueue.forEach(function (fn) { fn(window.lottie); }); };
    s.onerror = function () { lottieQueue.forEach(function (fn) { fn(null); }); };
    document.head.appendChild(s);
  }

})();
