/**
 * josh.js — Josh AI shared utilities
 * Loaded as a regular (non-module) script on every page.
 * Handles active nav highlighting only.
 * The wxO chat init lives inline in chat.html to guarantee it always runs.
 */

(function () {
  "use strict";

  // Highlight the correct nav link based on current page filename
  var path = window.location.pathname;
  var page = path.substring(path.lastIndexOf("/") + 1) || "index.html";

  document.querySelectorAll(".topbar-nav a").forEach(function (link) {
    var href = link.getAttribute("href") || "";
    var linkPage = href.substring(href.lastIndexOf("/") + 1);
    if (linkPage === page) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });
})();
