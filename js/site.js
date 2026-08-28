(() => {
  const button = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-bar");
  if (!button || !nav) return;
  button.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    button.setAttribute("aria-expanded", String(open));
  });
})();
