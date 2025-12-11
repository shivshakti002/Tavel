document.addEventListener("DOMContentLoaded", () => {
  // footer year
  const y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // menu toggle
  const menuBtn = document.getElementById("menuBtn");
  const nav = document.getElementById("nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", () => {
      nav.style.display = nav.style.display === "block" ? "" : "block";
    });
  }

  // show success message if flash present (server redirects)
  // (no extra logic needed since server flashes & reloads page)
});
