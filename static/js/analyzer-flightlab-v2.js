/* CONFIGDOCTOR FPV Flight Lab v2 — progressive enhancements only. */
(function () {
  'use strict';

  function boot() {
    var shell = document.querySelector('.analyzer-shell');
    if (!shell) return;

    var form = document.getElementById('aForm');
    var byId = function (id) { return document.getElementById(id); };
    var read = function (id, fallback) {
      var el = byId(id);
      return el && el.value !== '' ? el.value : (fallback || '—');
    };
    var clean = function (value) {
      return String(value == null ? '' : value).replace(/\s+/g, ' ').trim();
    };

    function updateSnapshot() {
      var frame = read('fSz', '5.0');
      var prop = read('fPrV', read('fPr', '5.0'));
      var pitch = read('fPtV', read('fPt', '4.0'));
      var weight = read('fWtV', read('fWt', '720'));
      var battery = read('battSel', '4S');
      var style = read('fSt', 'freestyle');
      var kv = read('fKv', '');
      var styleLabels = { freestyle: 'Freestyle', racing: 'Racing', longrange: 'Long Range' };
      var values = {
        flightlabFrame: clean(frame) + '"',
        flightlabProp: clean(prop) + '" / ' + clean(pitch),
        flightlabBattery: clean(battery),
        flightlabStyle: styleLabels[style] || clean(style),
        flightlabWeight: clean(weight) + ' g',
        flightlabMotor: kv ? clean(kv) + ' KV' : 'KV auto'
      };
      Object.keys(values).forEach(function (id) {
        var target = byId(id);
        if (target) target.textContent = values[id];
      });
    }

    if (form) {
      form.addEventListener('input', updateSnapshot, true);
      form.addEventListener('change', updateSnapshot, true);
      form.addEventListener('click', function (event) {
        if (event.target.closest('.sz,.bp,.sc,.bfv')) {
          window.requestAnimationFrame(updateSnapshot);
          window.setTimeout(updateSnapshot, 80);
        }
      });
      form.addEventListener('submit', function () {
        var button = byId('btnA');
        if (button) {
          button.classList.add('is-processing');
          button.setAttribute('aria-busy', 'true');
        }
      });
      updateSnapshot();
    }

    /* First-flight checklist: saved locally on this device; never sent to the server. */
    var checks = Array.prototype.slice.call(document.querySelectorAll('[data-flight-check]'));
    var count = byId('flightlabCheckCount');
    var storageKey = 'configdoctor.flightlab.checklist.v2';

    function readSaved() {
      try {
        var saved = JSON.parse(window.localStorage.getItem(storageKey) || '{}');
        return saved && typeof saved === 'object' ? saved : {};
      } catch (error) { return {}; }
    }
    function saveChecks() {
      var state = {};
      checks.forEach(function (item) {
        state[item.getAttribute('data-flight-check')] = !!item.checked;
      });
      try { window.localStorage.setItem(storageKey, JSON.stringify(state)); } catch (error) { /* storage is optional */ }
      updateCheckCount();
    }
    function updateCheckCount() {
      if (!count) return;
      var done = checks.filter(function (item) { return item.checked; }).length;
      count.textContent = done + '/' + checks.length + ' DONE';
      count.setAttribute('aria-label', done + ' of ' + checks.length + ' checks complete');
    }
    var saved = readSaved();
    checks.forEach(function (item) {
      var key = item.getAttribute('data-flight-check');
      if (Object.prototype.hasOwnProperty.call(saved, key)) item.checked = !!saved[key];
      item.addEventListener('change', saveChecks);
    });
    updateCheckCount();

    var reset = byId('flightlabChecklistReset');
    if (reset) reset.addEventListener('click', function () {
      checks.forEach(function (item) { item.checked = false; });
      saveChecks();
    });

    var results = byId('analyzer-results');
    if (results && shell.getAttribute('data-mobile-view') === 'results') {
      results.classList.add('flightlab-animate');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot, { once: true });
  } else {
    boot();
  }
})();
