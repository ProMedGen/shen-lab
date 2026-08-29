// Specimen clips marked data-loop play silently on a loop while they are on
// screen. They keep preload="none", so nothing is fetched until a clip is
// actually scrolled to -- a visitor who never reaches the Organoids section
// never downloads it. Pausing off-screen clips keeps decode off the CPU.
(() => {
  const clips = document.querySelectorAll("video[data-loop]");
  if (!clips.length) return;

  // Honouring reduced-motion here rather than in CSS keeps the poster frame
  // and the controls, so the clip is still available on demand.
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  if (typeof IntersectionObserver !== "function") return;

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const video = entry.target;
        if (entry.isIntersecting) {
          // A play() rejection is expected when a browser or power-saving mode
          // declines autoplay; the poster and controls remain, so there is
          // nothing to recover from.
          video.play().catch(() => {});
        } else if (!video.paused) {
          video.pause();
        }
      }
    },
    { rootMargin: "100px 0px", threshold: 0.25 },
  );

  clips.forEach((clip) => observer.observe(clip));
})();

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
