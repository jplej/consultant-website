document.addEventListener("DOMContentLoaded", function () {
  var btn = document.getElementById("theme-toggle");
  if (!btn) return;
  btn.addEventListener("click", function () {
    var d = document.documentElement;
    d.classList.toggle("dark");
    localStorage.theme = d.classList.contains("dark") ? "dark" : "light";
  });
});
