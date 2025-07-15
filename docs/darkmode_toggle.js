document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;
  const toggle = document.getElementById("dark-toggle");
  const theme = localStorage.getItem("theme") || "light";
  if (theme === "dark") body.classList.add("dark");

  toggle.addEventListener("click", () => {
    body.classList.toggle("dark");
    localStorage.setItem("theme", body.classList.contains("dark") ? "dark" : "light");
  });
});