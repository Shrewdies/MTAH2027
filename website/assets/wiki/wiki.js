/* The Shrewdies — wiki pages: motif and glyph pausing, page contents, scrollable tables, count-up stats, hub filter and search. No dependencies. */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var canWatch = "IntersectionObserver" in window;
  function each(list, fn) { Array.prototype.forEach.call(list, fn); }
  function still() { return reduce.matches || root.classList.contains("sh-motion-paused"); }
  function words(text) { return text.toLowerCase().split(/\s+/).filter(Boolean); }
  function matches(el, terms) {
    var haystack = el.getAttribute("data-search") || "";
    return terms.every(function (term) { return haystack.indexOf(term) > -1; });
  }

  /* ---- Motifs animate only while on screen; card glyphs only while in view ---- */
  var motifs = document.querySelectorAll("[data-wk-motif]");
  var glyphs = document.querySelectorAll("[data-wk-glyph]");
  if (canWatch) {
    var motifWatch = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { entry.target.classList.toggle("is-offscreen", !entry.isIntersecting); });
    }, { rootMargin: "120px" });
    each(motifs, function (motif) { motifWatch.observe(motif); });
    var glyphWatch = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) { entry.target.classList.toggle("is-inview", entry.isIntersecting); });
    });
    each(glyphs, function (holder) { glyphWatch.observe(holder); });
  }

  /* ---- Long pages get an "On this page" list beside the text ---- */
  var toc = document.querySelector("[data-wk-toc]");
  if (toc) {
    var heads = toc.parentNode.querySelectorAll(".wk-prose > h2[id]");
    if (heads.length >= 2) {
      var tocList = toc.querySelector("ol");
      each(heads, function (head) {
        var item = document.createElement("li");
        var link = document.createElement("a");
        link.href = "#" + head.id;
        link.textContent = head.textContent;
        item.appendChild(link);
        tocList.appendChild(item);
      });
      toc.hidden = false;
      toc.parentNode.classList.add("has-toc");
    }
  }

  /* ---- Tables scroll inside their own region ---- */
  var wraps = [];
  each(document.querySelectorAll(".wk-prose table"), function (table) {
    if (table.closest(".table-wrap")) return;
    var wrap = document.createElement("div");
    wrap.className = "table-wrap";
    wrap.style.setProperty("--cols", table.rows.length ? table.rows[0].cells.length : 2);
    table.parentNode.insertBefore(wrap, table);
    wrap.appendChild(table);
    wraps.push(wrap);
  });
  function markScrollable() {
    wraps.forEach(function (wrap) {
      if (wrap.scrollWidth > wrap.clientWidth + 1) {
        wrap.tabIndex = 0;
        wrap.setAttribute("role", "region");
        wrap.setAttribute("aria-label", "Table, scrolls sideways");
      } else {
        wrap.removeAttribute("tabindex");
        wrap.removeAttribute("role");
        wrap.removeAttribute("aria-label");
      }
    });
  }
  if (wraps.length) {
    markScrollable();
    var resizeQueued = false;
    window.addEventListener("resize", function () {
      if (resizeQueued) return;
      resizeQueued = true;
      window.requestAnimationFrame(function () { resizeQueued = false; markScrollable(); });
    });
  }

  /* ---- Stats count up once, when first seen ---- */
  function countUp(el) {
    var text = el.textContent;
    var parts = text.match(/^(\D*)(\d[\d,]*(?:\.\d+)?)([\s\S]*)$/);
    if (!parts) return;
    var target = parseFloat(parts[2].replace(/,/g, ""));
    var decimals = (parts[2].split(".")[1] || "").length;
    var grouped = parts[2].indexOf(",") > -1;
    var started = Date.now();
    function frame() {
      var p = Math.min((Date.now() - started) / 1100, 1);
      var value = (target * (1 - Math.pow(1 - p, 3))).toFixed(decimals);
      if (grouped) value = value.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      el.textContent = p < 1 ? parts[1] + value + parts[3] : text;
      if (p < 1) window.requestAnimationFrame(frame);
    }
    window.requestAnimationFrame(frame);
    window.setTimeout(function () { el.textContent = text; }, 1600);
  }
  var counters = document.querySelectorAll("[data-wk-count]");
  if (counters.length && canWatch && !still()) {
    var countWatch = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        countWatch.unobserve(entry.target);
        countUp(entry.target);
      });
    }, { threshold: 0.6 });
    each(counters, function (counter) { countWatch.observe(counter); });
  }

  /* ---- Families hub: "find a page" filters one list of links as you type ---- */
  var find = document.querySelector("[data-wk-find]");
  if (find) {
    var findInput = find.querySelector("[data-wk-search]");
    var findOut = find.querySelector("[data-wk-out]");
    var findAll = find.querySelector("details");
    var findItems = find.querySelectorAll("[data-wk-find-item]");
    var openedBySearch = false;
    var search = function () {
      var terms = words(findInput.value);
      var shown = 0;
      each(findItems, function (item) {
        item.hidden = !matches(item, terms);
        if (!item.hidden) shown += 1;
      });
      findOut.hidden = !terms.length;
      findOut.textContent = !terms.length ? "" : shown ? shown + (shown === 1 ? " page" : " pages") : "No page matches";
      if (terms.length && !findAll.open) { findAll.open = true; openedBySearch = true; }
      if (!terms.length && openedBySearch) { findAll.open = false; openedBySearch = false; }
    };
    findInput.addEventListener("input", search);
    findInput.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && findInput.value) { findInput.value = ""; search(); }
    });
    find.querySelector("[data-wk-search-box]").hidden = false;
  }

  /* ---- List hub: group chips and a text box filter the cards ---- */
  var list = document.querySelector("[data-wk-list]");
  var bar = list && list.querySelector("[data-wk-filter]");
  var cards = list ? list.querySelectorAll("[data-wk-card]") : [];
  if (bar && cards.length) {
    var sections = list.querySelectorAll("[data-wk-group-section]");
    var chips = list.querySelectorAll("[data-wk-group]");
    var input = list.querySelector("[data-wk-search]");
    var out = list.querySelector("[data-wk-out]");
    var empty = list.querySelector("[data-wk-empty]");
    var group = "";
    var apply = function () {
      var terms = words(input.value);
      var shown = 0;
      each(cards, function (card) {
        var match = (!group || card.getAttribute("data-group") === group) && matches(card, terms);
        card.hidden = !match;
        if (match) shown += 1;
      });
      each(sections, function (section) {
        section.hidden = !section.querySelector("[data-wk-card]:not([hidden])");
      });
      each(chips, function (chip) {
        var active = chip.getAttribute("data-wk-group") === group;
        chip.classList.toggle("is-active", active);
        chip.setAttribute("aria-pressed", String(active));
      });
      var filtered = shown !== cards.length;
      out.hidden = !filtered;
      out.textContent = filtered ? shown + " of " + cards.length : "";
      empty.hidden = shown > 0;
    };
    each(chips, function (chip) {
      chip.setAttribute("role", "button");
      chip.addEventListener("click", function (event) {
        event.preventDefault();
        group = chip.getAttribute("data-wk-group");
        apply();
      });
      chip.addEventListener("keydown", function (event) {
        if (event.key === " ") { event.preventDefault(); chip.click(); }
      });
    });
    input.addEventListener("input", apply);
    input.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && input.value) { input.value = ""; apply(); }
    });
    list.querySelector("[data-wk-reset]").addEventListener("click", function () {
      group = "";
      input.value = "";
      apply();
      input.focus();
    });
    bar.hidden = false;
    list.querySelector("[data-wk-search-box]").hidden = false;
    apply();
  }
})();
