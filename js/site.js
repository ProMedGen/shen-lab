(() => {
  const header = document.querySelector(".site-header");
  const button = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-bar");

  // The sticky header offsets every in-page anchor jump. CSS carries a
  // per-breakpoint fallback; measuring the real height keeps the offset correct
  // after webfonts land or if the header content changes.
  if (header) {
    const syncHeaderHeight = () => {
      const h = Math.round(header.getBoundingClientRect().height);
      document.documentElement.style.setProperty("--header-h", `${h}px`);
    };
    syncHeaderHeight();
    if (typeof ResizeObserver === "function") {
      new ResizeObserver(syncHeaderHeight).observe(header);
    } else {
      window.addEventListener("resize", syncHeaderHeight);
    }
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(syncHeaderHeight);
    }
  }

  if (!button || !nav) return;

  const setOpen = (open) => {
    nav.classList.toggle("open", open);
    button.setAttribute("aria-expanded", String(open));
  };

  button.addEventListener("click", () => setOpen(!nav.classList.contains("open")));

  // Escape closes the menu and returns focus to the toggle, so keyboard users
  // are not trapped inside an open panel.
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && nav.classList.contains("open")) {
      setOpen(false);
      button.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (!nav.classList.contains("open")) return;
    if (nav.contains(event.target) || button.contains(event.target)) return;
    setOpen(false);
  });

  // Same-page anchors do not reload, so the panel has to be closed by hand.
  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) setOpen(false);
  });
})();
