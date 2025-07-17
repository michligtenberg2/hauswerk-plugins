document.addEventListener("DOMContentLoaded", () => {
  const root = document.documentElement;
  const toggle = document.getElementById("dark-toggle");
  const theme = localStorage.getItem("theme") || "light";
  if (theme === "dark") root.classList.add("dark");

  if (toggle) {
    toggle.addEventListener("click", () => {
      root.classList.toggle("dark");
      localStorage.setItem("theme", root.classList.contains("dark") ? "dark" : "light");
    });
  }
});

