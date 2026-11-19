(() => {
  const page = document.querySelector('.landing-page');
  if (!page || !('IntersectionObserver' in window)) return;

  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (motionPreference.matches) return;

  const targets = Array.from(page.querySelectorAll(
    '.elite-signal-strip, .quick-grid > .quick-card, .catalog-section .tool-group, .saved-section, .resource-row > a'
  ));
  if (!targets.length) return;

  const observer = new IntersectionObserver((entries, activeObserver) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-motion-visible');
      activeObserver.unobserve(entry.target);
    });
  }, {
    root: null,
    rootMargin: '0px 0px -40px 0px',
    threshold: 0.12,
  });

  targets.forEach((target, index) => {
    target.classList.add('motion-ready');
    target.style.setProperty('--motion-stagger', String(index % 4));
    observer.observe(target);
  });
})();
