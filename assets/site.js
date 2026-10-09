/* ══════════════════════════════════════════════════════════════════════════
   GCFPAD — shared behaviour. Seven pages, one file.

   Deliberately small and dependency-free: the sticky nav, the mobile drawer,
   the scroll reveal, and the inquiry form. Nothing here needs a build step and
   nothing is loaded from a CDN, so the site keeps working on a slow connection
   and cannot break because somebody else's server went down.
   ══════════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  /* ─── THE NAV ─────────────────────────────────────────────────────────
     Transparent over a hero, solid once you have scrolled past it. Pages with
     no hero start solid, otherwise the first screen has white links on a
     white background and the menu disappears. */
  var nav = document.querySelector('.nav');
  var hero = document.querySelector('.hero, .phero');

  function onScroll() {
    if (!nav) return;
    var trigger = hero ? Math.min(hero.offsetHeight - 90, 420) : 0;
    var solid = window.scrollY > trigger || !hero;
    nav.classList.toggle('solid', solid);
    nav.classList.toggle('over-hero', !solid);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);

  /* ─── MOBILE DRAWER ──────────────────────────────────────────────────── */
  var burger = document.querySelector('.burger');
  var drawer = document.querySelector('.drawer');
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove('open');
    if (burger) { burger.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
    document.body.style.overflow = '';
  }
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = !drawer.classList.contains('open');
      drawer.classList.toggle('open', open);
      burger.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      /* Locking the body is what stops the page scrolling underneath the
         menu on iOS, which otherwise feels broken. */
      document.body.style.overflow = open ? 'hidden' : '';
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') closeDrawer();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeDrawer();
    });
    /* A drawer left open while the window grows to desktop width becomes an
       invisible sheet over the whole page. */
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) closeDrawer();
    });
  }

  /* ─── SCROLL REVEAL ──────────────────────────────────────────────────
     The brief asked for subtle entrance animations and explicitly warned
     against excessive animation, so: one fade-and-rise, staggered inside a
     group, and it runs once.

     ⛔ If IntersectionObserver is missing, everything is shown immediately.
     An animation that fails must never leave the page blank. */
  var items = [].slice.call(document.querySelectorAll('.rv'));
  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var d = parseInt(el.getAttribute('data-d') || '0', 10);
        setTimeout(function () { el.classList.add('in'); }, d);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    items.forEach(function (el) { io.observe(el); });
    /* Anything already on screen at load should not wait for a scroll that
       may never come on a short page. */
    window.addEventListener('load', function () {
      items.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight) el.classList.add('in');
      });
    });
  }

  /* ─── THE INQUIRY FORM ───────────────────────────────────────────────
     🚨 A contact form that validates nicely and quietly posts into nothing is
     worse than no form: the visitor believes they have been in touch. So the
     endpoint is named here in one place, and if it is not set the form says
     so in plain language instead of pretending.

     ENDPOINT is filled in when the inbox is agreed. Until then the button
     offers the inquiry over WhatsApp, which is a channel that genuinely
     reaches someone. */
  var ENDPOINT = '';                       /* e.g. 'https://api.example.org/api/contact' */
  var WHATSAPP = '';                       /* e.g. '50912345678' - digits only, no + */

  var form = document.getElementById('inquiry');
  if (form) {
    var box = form.querySelector('.form-msg');
    var btn = form.querySelector('button[type=submit]');

    function say(kind, text) {
      if (!box) return;
      box.className = 'form-msg show ' + kind;
      box.textContent = text;
      box.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    function mark(field, bad) {
      var w = field.closest('.field');
      if (w) w.classList.toggle('bad', !!bad);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = {};
      var bad = null;
      ['name', 'organization', 'email', 'country', 'interest', 'message'].forEach(function (k) {
        var el = form.elements[k];
        if (!el) return;
        var v = (el.value || '').trim();
        data[k] = v;
        var required = (k === 'name' || k === 'email' || k === 'message');
        var looksEmail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
        var ok = required ? (k === 'email' ? looksEmail : v.length > 1) : true;
        mark(el, !ok);
        if (!ok && !bad) bad = el;
      });
      if (bad) {
        say('bad', 'Please complete the highlighted fields before sending.');
        bad.focus();
        return;
      }

      if (!ENDPOINT) {
        if (WHATSAPP) {
          var txt = 'GCFPAD inquiry\n\nName: ' + data.name +
                    '\nOrganization: ' + (data.organization || '-') +
                    '\nEmail: ' + data.email +
                    '\nCountry: ' + (data.country || '-') +
                    '\nArea of interest: ' + (data.interest || '-') +
                    '\n\n' + data.message;
          window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(txt), '_blank');
          say('good', 'Opening WhatsApp with your inquiry. Press send there and we will come back to you.');
          return;
        }
        say('bad', 'This form is not connected to an inbox yet, so nothing would reach us. ' +
                   'Please use the contact details on this page in the meantime.');
        return;
      }

      btn.disabled = true;
      var label = btn.textContent;
      btn.textContent = 'Sending...';
      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (r) {
        return r.json().catch(function () { return {}; });
      }).then(function (j) {
        if (j && j.ok) {
          form.reset();
          say('good', 'Thank you. Your inquiry has been received and someone will be in touch.');
        } else {
          say('bad', (j && j.error) || 'Your inquiry could not be sent. Please try again shortly.');
        }
      }).catch(function () {
        say('bad', 'Your inquiry could not be sent - the connection failed. Please try again shortly.');
      }).then(function () {
        btn.disabled = false;
        btn.textContent = label;
      });
    });
  }

  /* ─── FOOTER YEAR ───────────────────────────────────────────────────── */
  var y = document.getElementById('yr');
  if (y) y.textContent = new Date().getFullYear();
})();
