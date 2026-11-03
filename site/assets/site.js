/* Statecraft Institute site behaviour. Small on purpose: no libraries. */
(function () {
  var doc = document.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var conn = navigator.connection || {};
  var lite = conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '') || (navigator.deviceMemory && navigator.deviceMemory <= 2);
  if (lite) doc.classList.add('lite');

  /* Dark mode test button (remembered on this device) */
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var saved = store('sicdp-theme'); if (saved) doc.setAttribute('data-theme', saved);
  function isDark() { var t = doc.getAttribute('data-theme'); return t ? t === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; }
  function label() { document.querySelectorAll('.theme-btn').forEach(function (b) { b.textContent = isDark() ? 'Light mode' : 'Dark mode'; }); }
  document.querySelectorAll('.theme-btn').forEach(function (b) {
    b.addEventListener('click', function () { var t = isDark() ? 'light' : 'dark'; doc.setAttribute('data-theme', t); store('sicdp-theme', t); label(); });
  });
  label();

  /* Big logo shrinks gradually into the header as the page scrolls */
  var mast = document.querySelector('.masthead .lockup');
  if (!mast) doc.classList.add('no-masthead');
  else {
    var ticking = false, span = function () { return Math.max(120, mast.offsetHeight + 40); };
    var upd = function () { ticking = false; var p = Math.min(1, Math.max(0, scrollY / span())); doc.style.setProperty('--p', p.toFixed(3)); };
    addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  }
  /* Pages open at the top (the Field Diaries map must come first) */
  if (!location.hash) { try { history.scrollRestoration = 'manual'; } catch (e) {} scrollTo(0, 0); }

  /* Menu: phone toggle and the About dropdown */
  var btn = document.querySelector('.menu-btn'), nav = document.querySelector('nav.main');
  if (btn && nav) btn.addEventListener('click', function () { var o = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); });
  document.querySelectorAll('.drop > button').forEach(function (b) {
    b.addEventListener('click', function () { var d = b.parentNode, o = d.classList.toggle('open'); b.setAttribute('aria-expanded', o ? 'true' : 'false'); });
  });
  document.addEventListener('click', function (e) { document.querySelectorAll('.drop.open').forEach(function (d) { if (!d.contains(e.target) && innerWidth > 900) d.classList.remove('open'); }); });

  /* Hero photos change every few seconds */
  var stage = document.querySelector('.slides .stage');
  if (stage) {
    var imgs = stage.querySelectorAll('img'), cap = document.querySelector('.slides figcaption'), i = 0, paused = false;
    var secs = parseFloat(stage.getAttribute('data-seconds')) || 3;
    if (imgs.length > 1 && !reduce) {
      stage.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') paused = true; });
      stage.addEventListener('pointerleave', function () { paused = false; });
      setInterval(function () {
        if (paused || document.hidden) return;
        var next = (i + 1) % imgs.length, n = imgs[next];
        if (!n.complete) { n.loading = 'eager'; return; }            /* wait until the next photo has loaded */
        imgs[i].classList.remove('show'); n.classList.add('show'); i = next;
        cap.textContent = n.getAttribute('data-caption');
        var after = imgs[(i + 1) % imgs.length]; after.loading = 'eager';
      }, secs * 1000);
    }
  }

  /* Images show a sewing line while loading */
  document.querySelectorAll('.frame img').forEach(function (im) {
    if (im.complete) return; var f = im.parentNode; f.classList.add('loading');
    var done = function () { f.classList.remove('loading'); }; im.addEventListener('load', done); im.addEventListener('error', done);
  });

  /* Photo viewer on the Field Diaries page: caption, place, date and time sit inside the stitched frame */
  var dlg = document.querySelector('dialog.viewer');
  if (dlg) {
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-full]')), cur = 0;
    var vImg = dlg.querySelector('img');
    var set = function (sel, v) { var el = dlg.querySelector(sel); el.textContent = v || ''; el.parentNode.hidden = !v; };
    function show(k) {
      cur = (k + items.length) % items.length; var it = items[cur];
      vImg.src = it.getAttribute('data-full'); vImg.alt = it.getAttribute('data-alt');
      dlg.querySelector('.over strong').textContent = it.getAttribute('data-alt');
      set('.v-place', it.getAttribute('data-place')); set('.v-date', it.getAttribute('data-date')); set('.v-time', it.getAttribute('data-time'));
      var nx = items[(cur + 1) % items.length]; (new Image()).src = nx.getAttribute('data-full');   /* preload the next photo */
    }
    items.forEach(function (it, k) { it.addEventListener('click', function () { show(k); dlg.showModal(); }); });
    dlg.querySelector('.prev').addEventListener('click', function () { show(cur - 1); });
    dlg.querySelector('.next').addEventListener('click', function () { show(cur + 1); });
    dlg.querySelector('.close').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') show(cur - 1); if (e.key === 'ArrowRight') show(cur + 1); });
    var sx = null;
    vImg.addEventListener('pointerdown', function (e) { sx = e.clientX; });
    vImg.addEventListener('pointerup', function (e) { if (sx === null) return; var dx = e.clientX - sx; sx = null; if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1)); });
  }

  /* Video: load the player only when someone presses play */
  document.querySelectorAll('.video[data-yt]').forEach(function (v) {
    v.querySelector('button').addEventListener('click', function () {
      var f = document.createElement('iframe'); f.src = 'https://www.youtube-nocookie.com/embed/' + v.getAttribute('data-yt') + '?autoplay=1';
      f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true; f.title = v.getAttribute('data-title') || 'Video';
      v.innerHTML = ''; v.appendChild(f);
    });
  });

  /* Tap on header or footer: a seam flashes */
  ['header.site', 'footer.site'].forEach(function (sel) {
    var el = document.querySelector(sel); if (!el) return;
    el.addEventListener('pointerdown', function (ev) { if (ev.pointerType !== 'touch') return; el.classList.add('tap'); setTimeout(function () { el.classList.remove('tap'); }, 900); });
  });

  /* Page arrival: a stitch runs across under the header */
  if (!reduce && !lite) { var a = document.createElement('div'); a.className = 'arrive'; a.setAttribute('aria-hidden', 'true'); document.body.appendChild(a); setTimeout(function () { a.remove(); }, 1100); }

  /* The weave glows under the cursor, or under a finger on empty cloth */
  if (reduce || lite) return;
  var glow = document.querySelector('.weave-glow'); if (!glow) return;
  var TEXT = 'p,h1,h2,h3,li,a,button,figcaption,label,input,img,nav,.art,svg';
  var off = 0;
  function at(x, y) { doc.style.setProperty('--mx', x + 'px'); doc.style.setProperty('--my', y + 'px'); glow.classList.add('on'); clearTimeout(off); }
  function fade(ms) { clearTimeout(off); off = setTimeout(function () { glow.classList.remove('on'); }, ms); }
  addEventListener('pointermove', function (e) {
    if (e.pointerType === 'mouse') { at(e.clientX, e.clientY); fade(1000); }
    else if (e.buttons && !(e.target.closest && e.target.closest(TEXT))) { at(e.clientX, e.clientY); }
  }, { passive: true });
  addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse' && !(e.target.closest && e.target.closest(TEXT))) at(e.clientX, e.clientY); }, { passive: true });
  addEventListener('pointerup', function (e) { if (e.pointerType !== 'mouse') fade(700); }, { passive: true });
  addEventListener('pointercancel', function () { fade(700); }, { passive: true });
})();
