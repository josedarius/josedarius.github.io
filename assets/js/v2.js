/* MyCloudSME v2 — interactions & motion. Everything degrades gracefully. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- mobile menu ---- */
  var mb = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (mb && nav) {
    var setOpen = function (o) {
      nav.classList.toggle('open', o);
      mb.setAttribute('aria-expanded', o);
      mb.textContent = o ? 'Close' : 'Menu';
    };
    mb.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  }

  /* ---- header shadow on scroll + reading progress ---- */
  var hdr = document.querySelector('.hdr');
  var bar = document.createElement('div');
  bar.className = 'progress';
  if (hdr) hdr.appendChild(bar);
  var onScroll = function () {
    var y = window.scrollY || 0;
    if (hdr) hdr.classList.toggle('scrolled', y > 8);
    var h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- staggered children in grids ---- */
  var groups = '.caps,.why,.flow5,.ps,.bigstats,.benefits,.route-steps,.trio,.practices,.prob-grid,.cases,.case-row,.steps,.sheets,.offers,.svc,.prods,.paths,.std-list,.pillars-grid,.card-grid,.lifecycle-grid,.services-grid,.solutions-grid,.delivery-steps,.stat-row,.proof,.skills';
  document.querySelectorAll(groups).forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (c, i) {
      c.classList.add('rv');
      c.style.setProperty('--d', Math.min(i, 10) * 70 + 'ms');
    });
  });

  /* ---- count-up numbers (final value is already in the HTML) ---- */
  var countUp = function (el) {
    var m = el.textContent.match(/^(\D*)(\d+)(.*)$/);
    if (!m || reduce) return;
    var pre = m[1], end = parseInt(m[2], 10), post = m[3], t0 = null, dur = 1400;
    var step = function (t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + Math.round(end * e) + post;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  /* ---- reveal on scroll ---- */
  var els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in');
        e.target.querySelectorAll('[data-count], .proof b, .stat-row b, .metrics b, .bigstats b').forEach(countUp);
        if (e.target.hasAttribute('data-count')) countUp(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- pointer glow in dark sections + spotlight cards ---- */
  if (!reduce && window.matchMedia('(pointer: fine)').matches) {
    document.querySelectorAll('.grid-bg').forEach(function (s) {
      s.addEventListener('pointermove', function (e) {
        var r = s.getBoundingClientRect();
        s.style.setProperty('--gx', (e.clientX - r.left) + 'px');
        s.style.setProperty('--gy', (e.clientY - r.top) + 'px');
        s.classList.add('glow-on');
      });
      s.addEventListener('pointerleave', function () { s.classList.remove('glow-on'); });
    });
    var cards = '.offer,.prod,a.service-card,a.solution-card,.sheet';
    document.querySelectorAll(cards).forEach(function (c) {
      c.classList.add('spot');
      c.addEventListener('pointermove', function (e) {
        var r = c.getBoundingClientRect();
        c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        c.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
    /* subtle 3D tilt on the hero diagram */
    var dg = document.querySelector('.hero .diagram');
    var hero = document.querySelector('.hero');
    if (dg && hero) {
      hero.addEventListener('pointermove', function (e) {
        var r = hero.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        dg.style.transform = 'perspective(1200px) rotateY(' + (x * 6) + 'deg) rotateX(' + (-y * 6) + 'deg)';
      });
      hero.addEventListener('pointerleave', function () { dg.style.transform = ''; });
    }
  }


  /* ---- signature moment: hero verb typing, synced with the control-plane diagram ---- */
  var verb = document.getElementById('sw-verb');
  var cp = document.querySelector('.diagram.cp');
  if (verb && !reduce) {
    var words = ['planned', 'migrated', 'modernised', 'secured', 'optimised', 'operated'];
    var wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
    var setNode = function (i) {
      if (!cp) return;
      cp.querySelectorAll('[data-node]').forEach(function (n) { n.classList.toggle('on', +n.getAttribute('data-node') === i); });
    };
    (async function loop() {
      await wait(2400);
      for (var i = 0; ; i = (i + 1) % words.length) {
        verb.classList.add('typing');
        while (verb.textContent.length) { verb.textContent = verb.textContent.slice(0, -1); await wait(30); }
        setNode(i);
        var w = words[i];
        for (var k = 1; k <= w.length; k++) { verb.textContent = w.slice(0, k); await wait(60); }
        verb.classList.remove('typing');
        await wait(2600);
      }
    })();
  }


  /* ---- accessible tabs ---- */
  document.querySelectorAll('[data-tabs]').forEach(function (box) {
    var tabs = Array.prototype.slice.call(box.querySelectorAll('[role="tab"]'));
    var select = function (t, focus) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', on);
        x.tabIndex = on ? 0 : -1;
        var p = document.getElementById(x.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
      if (focus) t.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowDown' || k === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (k === 'ArrowUp' || k === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (k === 'Home') n = tabs[0];
        if (k === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
  });

  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();
})();
