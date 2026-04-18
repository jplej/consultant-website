(function () {
  var d = document.documentElement;
  if (localStorage.theme === "dark" || (!("theme" in localStorage) && matchMedia("(prefers-color-scheme:dark)").matches)) {
    d.classList.add("dark");
  }
})();
