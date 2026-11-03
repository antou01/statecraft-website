/* Statecraft Institute site behaviour. Small on purpose: no libraries. */
(function () {
  var doc = document.documentElement;
  doc.classList.remove('no-js');

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var conn = navigator.connection || {};
  var lite = conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '') || (navigator.deviceMemory && navigator.deviceMemory <= 2);
  if (lite) doc.classList.add('lite');

  /* Hero: one field photo per visit */
  var hero = document.querySelector('[data-heroes]');
  if (hero) {
    try {
      var list = JSON.parse(hero.getAttribute('data-heroes'));
      var pick = list[Math.floor(Math.random() * list.length)];
      var img = hero.querySelector('img'), cap = hero.querySelector('figcaption');
      var base = hero.getAttribute('data-base') || '';
      img.srcset = [768, 1280, 1920].map(function (w) { return base + pick.slug + '-' + w + '.webp ' + w + 'w'; }).join(', ');
      img.src = base + pick.slug + '-1280.webp';
      img.alt = pick.alt;
      cap.textContent = pick.caption;
    } catch (e) { /* keep the default photo */ }
  }

  /* Mobile menu */
  var btn = document.querySelector('.menu-btn'), nav = document.querySelector('nav.main');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  /* Seams sew themselves in when they reach the screen */
  var seams = document.querySelectorAll('.sew');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    seams.forEach(function (s) { io.observe(s); });
  } else { seams.forEach(function (s) { s.classList.add('in'); }); }

  /* Images show a sewing line until they load */
  document.querySelectorAll('.frame img').forEach(function (im) {
    if (im.complete) return;
    var f = im.parentNode; f.classList.add('loading');
    im.addEventListener('load', function () { f.classList.remove('loading'); });
    im.addEventListener('error', function () { f.classList.remove('loading'); });
  });

  /* Tap on header or footer: a seam flashes (phones) */
  ['header.site', 'footer.site'].forEach(function (sel) {
    var el = document.querySelector(sel); if (!el) return;
    el.addEventListener('pointerdown', function (ev) {
      if (ev.pointerType !== 'touch') return;
      el.classList.add('tap'); setTimeout(function () { el.classList.remove('tap'); }, 900);
    });
  });

  /* Page arrival: a stitch runs across under the header */
  if (!reduce && !lite) {
    var a = document.createElement('div'); a.className = 'arrive'; a.setAttribute('aria-hidden', 'true');
    document.body.appendChild(a); setTimeout(function () { a.remove(); }, 1100);
  }

  /* Desktop only: the weave brightens near the cursor, and a thread follows it over empty cloth */
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (!fine || reduce || lite) return;
  var cv = document.createElement('canvas'); cv.className = 'trail'; cv.setAttribute('aria-hidden', 'true');
  document.body.appendChild(cv);
  var ctx = cv.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2), pts = [], fade = 1, leftAt = 0, raf = 0;
  function size() { cv.width = innerWidth * dpr; cv.height = innerHeight * dpr; cv.style.width = innerWidth + 'px'; cv.style.height = innerHeight + 'px'; }
  size(); addEventListener('resize', size);
  var ink = function () { return getComputedStyle(doc).getPropertyValue('--ink').trim() || '#812f8e'; };
  var TEXT = 'p,h1,h2,h3,li,a,button,figcaption,blockquote,label,input,.label,.wordmark,nav';
  function draw() {
    raf = 0; ctx.clearRect(0, 0, cv.width, cv.height);
    if (leftAt) { fade = Math.max(0, 1 - (performance.now() - leftAt) / 1000); if (!fade) { pts = []; leftAt = 0; return; } }
    if (pts.length > 1) {
      ctx.save(); ctx.scale(dpr, dpr); ctx.globalAlpha = 0.75 * fade; ctx.strokeStyle = ink();
      ctx.lineWidth = 1.8; ctx.lineCap = 'round'; ctx.setLineDash([7, 6]);
      ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
      for (var i = 1; i < pts.length - 1; i++) {
        var mx = (pts[i][0] + pts[i + 1][0]) / 2, my = (pts[i][1] + pts[i + 1][1]) / 2;
        ctx.quadraticCurveTo(pts[i][0], pts[i][1], mx, my);
      }
      ctx.stroke(); ctx.restore();
    }
    if (leftAt) raf = requestAnimationFrame(draw);
  }
  function kick() { if (!raf) raf = requestAnimationFrame(draw); }
  addEventListener('pointermove', function (e) {
    doc.style.setProperty('--mx', e.clientX + 'px'); doc.style.setProperty('--my', e.clientY + 'px');
    var overText = e.target.closest && e.target.closest(TEXT);
    if (overText) { if (pts.length && !leftAt) leftAt = performance.now(); kick(); return; }
    if (leftAt) { leftAt = 0; fade = 1; pts = []; }
    var last = pts[pts.length - 1];
    if (!last || Math.hypot(e.clientX - last[0], e.clientY - last[1]) > 6) { pts.push([e.clientX, e.clientY]); if (pts.length > 90) pts.shift(); }
    kick();
  }, { passive: true });
  addEventListener('scroll', function () { pts = []; kick(); }, { passive: true });
  document.addEventListener('pointerleave', function () { if (pts.length) { leftAt = performance.now(); kick(); } });
})();
