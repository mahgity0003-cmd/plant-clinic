(function () {
  "use strict";
  var cfg = window.SITE_CONFIG || {};

  /* مقصد QR از فایل site-config.js خوانده می‌شود */
  document.querySelectorAll("[data-qr-link]").forEach(function (a) {
    if (cfg.qrTarget) a.setAttribute("href", cfg.qrTarget);
  });

  /* کپی شماره تماس */
  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;top:0;right:0;opacity:0";
    document.body.appendChild(ta);
    ta.select();
    ta.setSelectionRange(0, text.length);
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
    return ok;
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(function () { return true; })
        .catch(function () { return fallbackCopy(text); });
    }
    return Promise.resolve(fallbackCopy(text));
  }

  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    var msg = btn.parentElement.querySelector(".copy-msg");
    var timer;
    btn.addEventListener("click", function () {
      var value = (btn.getAttribute("data-copy") || "").replace(/\s+/g, "");
      copyText(value).then(function (ok) {
        if (!msg) return;
        msg.textContent = ok ? "کپی شد!" : "کپی نشد؛ شماره را انتخاب کنید";
        msg.classList.add("show");
        clearTimeout(timer);
        timer = setTimeout(function () { msg.classList.remove("show"); }, 2200);
      });
    });
  });
})();
