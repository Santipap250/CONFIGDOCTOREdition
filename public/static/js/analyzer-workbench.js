/* Mobile workbench navigation for the Drone Analyzer.
   Progressive enhancement only: the traditional form submission remains unchanged. */
(function () {
  'use strict';

  var shell = document.querySelector('.analyzer-shell');
  if (!shell) return;

  var tabs = Array.prototype.slice.call(shell.querySelectorAll('[data-analyzer-view]'));
  var setup = document.getElementById('analyzer-setup');
  var results = document.getElementById('analyzer-results');
  var dockButton = document.getElementById('analyzerMobileSubmit');
  var media = window.matchMedia ? window.matchMedia('(max-width: 760px)') : null;
  var current = shell.getAttribute('data-mobile-view') || 'setup';

  function setView(view, moveFocus) {
    if (view !== 'setup' && view !== 'results') return;
    current = view;
    shell.setAttribute('data-mobile-view', view);
    tabs.forEach(function (tab) {
      var selected = tab.getAttribute('data-analyzer-view') === view;
      tab.setAttribute('aria-selected', selected ? 'true' : 'false');
      tab.setAttribute('tabindex', selected ? '0' : '-1');
    });
    if (moveFocus && media && media.matches) {
      var target = view === 'setup' ? setup : results;
      if (target) {
        var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      }
    }
  }

  function syncViewport() {
    var mobile = !!(media && media.matches);
    shell.classList.toggle('is-mobile-enhanced', mobile);
    if (!mobile) {
      tabs.forEach(function (tab) { tab.removeAttribute('tabindex'); });
    } else {
      setView(current, false);
    }
  }

  tabs.forEach(function (tab, index) {
    tab.addEventListener('click', function () {
      setView(tab.getAttribute('data-analyzer-view'), true);
    });
    tab.addEventListener('keydown', function (event) {
      var next = index;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      tabs[next].focus();
      setView(tabs[next].getAttribute('data-analyzer-view'), false);
    });
  });

  if (dockButton) {
    dockButton.addEventListener('click', function () {
      var form = document.getElementById('aForm');
      if (!form) return;
      if (typeof form.requestSubmit === 'function') form.requestSubmit();
      else form.submit();
    });
  }

  syncViewport();
  if (media) {
    if (typeof media.addEventListener === 'function') media.addEventListener('change', syncViewport);
    else if (typeof media.addListener === 'function') media.addListener(syncViewport);
  }
})();
