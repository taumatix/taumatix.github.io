(function () {
  var root = document.documentElement;
  var forced = new URLSearchParams(location.search).get("theme");
  if (forced === "dark" || forced === "light") {
    root.setAttribute("data-theme", forced);
  } else {
    try {
      var saved = localStorage.getItem("theme");
      if (saved) root.setAttribute("data-theme", saved);
    } catch (e) {}
  }

  var btn = document.getElementById("theme");
  if (btn) {
    btn.addEventListener("click", function () {
      var dark = root.getAttribute("data-theme") === "dark" ||
        (!root.getAttribute("data-theme") && matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  // Refresh the baked-in version badges from the latest release; keep them on any failure.
  document.querySelectorAll("[data-repo]").forEach(function (card) {
    var el = card.querySelector("[data-version]");
    if (!el) return;
    fetch("https://api.github.com/repos/taumatix/" + card.dataset.repo + "/releases/latest")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { if (j && j.tag_name) el.textContent = j.tag_name; })
      .catch(function () {});
  });
})();
