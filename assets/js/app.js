/* =========================================================
   RENAUVA — app.js
   Aucune dépendance externe. Tout est natif (IO + rAF).
   ========================================================= */
(function () {
  'use strict';

  var TEL = '+33660753771';
  var WA = '33660753771';

  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };

  /* ---------- LIBELLÉS SELON LA LANGUE DE LA PAGE ----------
     Seule l'interface est traduite. Le dossier envoyé à Brahim reste en
     français : c'est lui qui le lit, quelle que soit la langue du visiteur. */
  var EN = document.documentElement.lang === 'en';
  var L = EN ? {
    step: function (a, b) { return 'Step ' + a + ' of ' + b; },
    next: 'Continue', last: 'See my summary', back: 'Back', done: 'Done',
    hot: 'Priority request', mid: 'Request to review', low: 'Request to schedule',
    urgentTitle: 'This is an emergency: calling is still the fastest.',
    readyTitle: 'Your file is ready.',
    rangeLabel: 'Indicative range',
    disc: 'Automatic estimate, materials and labour included. Only the free on-site ' +
          'assessment can produce a firm quote.',
    discNo: 'Brahim comes out, finds where the problem is coming from and gives you a clear ' +
            'quote. The assessment and the call-out stay free.',
    photo: 'photo', photos: 'photos', noPhoto: 'No photo', access: 'access',
    budgets: {
      dep: [['Under \u20ac150', 0.5], ['\u20ac150 \u2013 \u20ac300', 1.5], ['\u20ac300 \u2013 \u20ac700', 2.5],
            ['Over \u20ac700', 3], ['I do not know yet', 1.5]],
      reno: [['Under \u20ac5,000', 1.5], ['\u20ac5,000 \u2013 \u20ac10,000', 2.5], ['\u20ac10,000 \u2013 \u20ac20,000', 3],
             ['Over \u20ac20,000', 3], ['I do not know yet', 2]]
    },
    sending: 'Sending\u2026',
    sentOk: 'File sent. Brahim has everything he needs and will call you back shortly.',
    sentErr: 'Could not send. Use WhatsApp or call 06 60 75 37 71.',
    notWired: 'Email sending is not connected yet. Use WhatsApp or call 06 60 75 37 71.',
    formOk: 'Thank you for completing the form. Your request has been received — I will get back to you within the next 24 hours.',
    formErr: 'Could not send. Please call 06 60 75 37 71 or use WhatsApp.',
    filesMax: 'Maximum 3 photos \u2014 the extra ones will be ignored.'
  } : {
    step: function (a, b) { return '\u00c9tape ' + a + ' sur ' + b; },
    next: 'Continuer', last: 'Voir mon r\u00e9capitulatif', back: 'Retour', done: 'Termin\u00e9',
    hot: 'Demande prioritaire', mid: 'Demande \u00e0 \u00e9valuer', low: 'Demande \u00e0 planifier',
    urgentTitle: "C'est une urgence : l'appel reste le plus rapide.",
    readyTitle: 'Votre dossier est pr\u00eat.',
    rangeLabel: 'Fourchette indicative',
    disc: "Estimation automatique, mat\u00e9riaux et main d'\u0153uvre inclus. " +
          'Seul le diagnostic gratuit sur place permet un devis ferme.',
    discNo: "Je me d\u00e9place, je cherche l'origine du probl\u00e8me et je vous remets un devis clair. " +
            'Le diagnostic et le d\u00e9placement restent gratuits.',
    photo: 'photo', photos: 'photos', noPhoto: 'Sans photo', access: 'acc\u00e8s',
    budgets: {
      dep: [['Moins de 150 \u20ac', 0.5], ['150 \u20ac \u2013 300 \u20ac', 1.5], ['300 \u20ac \u2013 700 \u20ac', 2.5],
            ['Plus de 700 \u20ac', 3], ['Je ne sais pas encore', 1.5]],
      reno: [['Moins de 5 000 \u20ac', 1.5], ['5 000 \u20ac \u2013 10 000 \u20ac', 2.5], ['10 000 \u20ac \u2013 20 000 \u20ac', 3],
             ['Plus de 20 000 \u20ac', 3], ['Je ne sais pas encore', 2]]
    },
    sending: 'Envoi en cours\u2026',
    sentOk: "Dossier envoy\u00e9. Brahim a tout ce qu'il faut, il vous rappelle rapidement.",
    sentErr: 'Envoi impossible. Passez par WhatsApp ou appelez le 06 60 75 37 71.',
    notWired: "L'envoi par e-mail n'est pas encore reli\u00e9. Passez par WhatsApp ou appelez le 06 60 75 37 71.",
    formOk: "Merci d'avoir compl\u00e9t\u00e9 le formulaire. Votre demande a bien \u00e9t\u00e9 transmise, je vous recontacte dans les prochaines 24 heures.",
    formErr: 'Envoi impossible. Appelez le 06 60 75 37 71 ou \u00e9crivez sur WhatsApp.',
    filesMax: '3 photos maximum \u2014 les suivantes seront ignor\u00e9es.'
  };

  /* ═══════════════════════════════════════════════════════════
     ENREGISTREMENT DES DEMANDES
     Chaque envoi est écrit dans la base du site (Cloudflare D1) et
     consultable sur /suivi.html. Les photos sont redimensionnées ici,
     dans le navigateur, avant d'être transmises.
     Ce canal est indépendant de l'e-mail : si l'un tombe, l'autre passe.
  ═══════════════════════════════════════════════════════════ */
  var API_LEAD = '/api/lead';

  /* Réduit une photo à 1400 px de côté max et la convertit en JPEG.
     Une photo de téléphone passe ainsi de ~4 Mo à ~200 Ko. */
  function compresse(file) {
    return new Promise(function (resolve) {
      if (!/^image\//.test(file.type)) return resolve(null);
      var img = new Image(), url = URL.createObjectURL(file);
      img.onload = function () {
        URL.revokeObjectURL(url);
        var max = 1400;
        var w = img.width, h = img.height;
        if (w > max || h > max) {
          if (w > h) { h = Math.round(h * max / w); w = max; }
          else { w = Math.round(w * max / h); h = max; }
        }
        var cv = document.createElement('canvas');
        cv.width = w; cv.height = h;
        cv.getContext('2d').drawImage(img, 0, 0, w, h);
        var data = cv.toDataURL('image/jpeg', 0.72);
        resolve({ nom: file.name, type: 'image/jpeg', donnees: data.split(',')[1] });
      };
      img.onerror = function () { URL.revokeObjectURL(url); resolve(null); };
      img.src = url;
    });
  }

  function enregistre(payload, fichiers) {
    var liste = Array.prototype.slice.call(fichiers || []).slice(0, 3);
    return Promise.all(liste.map(compresse))
      .then(function (photos) {
        payload.photos = photos.filter(Boolean);
        payload.page = location.href;
        payload.langue = document.documentElement.lang;
        return fetch(API_LEAD, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
      })
      .then(function (r) { return r.ok; })
      .catch(function () { return false; });
  }

  /* ---------- LOADER ---------- */
  var loader = $('#loader');
  function killLoader() {
    if (!loader || loader.classList.contains('is-out')) return;
    loader.classList.add('is-out');
    document.body.classList.remove('is-locked');
    setTimeout(function () { loader.remove(); }, 700);
  }
  document.body.classList.add('is-locked');
  window.addEventListener('load', function () { setTimeout(killLoader, reduce ? 0 : 700); });
  setTimeout(killLoader, 3200); // filet de sécurité

  /* ---------- VIDEO HERO (source selon la largeur, chargée après le 1er paint) ---------- */
  (function () {
    var v = $('#heroVideo');
    if (!v || reduce) return;
    var save = navigator.connection && (navigator.connection.saveData ||
      /2g/.test(navigator.connection.effectiveType || ''));
    if (save) return;
    var src = (innerWidth > 900 && devicePixelRatio > 1) || innerWidth > 1400
      ? '/assets/video/hero-1080.mp4' : '/assets/video/hero-720.mp4';
    var start = function () {
      v.src = src;
      v.load();
      var p = v.play();
      if (p && p.catch) p.catch(function () {});
    };
    if (document.readyState === 'complete') start();
    else window.addEventListener('load', start);
  })();

  /* ---------- REVEALS AU SCROLL ---------- */
  (function () {
    var els = $$('.reveal, .proc__i');
    if (!('IntersectionObserver' in window) || reduce) {
      els.forEach(function (el) { el.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        var d = parseInt(el.dataset.d || 0, 10);
        if (!d) {
          var sibs = el.parentElement ? $$('.reveal', el.parentElement) : [];
          d = Math.min(sibs.indexOf(el), 5) * 80;
          if (d < 0) d = 0;
        }
        setTimeout(function () { el.classList.add('is-in'); }, d);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  })();

  /* ---------- COMPTEURS ---------- */
  (function () {
    var els = $$('[data-count]');
    if (!els.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, target = +el.dataset.count, suf = el.dataset.suffix || '',
            pre = el.dataset.prefix || '';
        // onglet en arrière-plan : rAF est gelé, on afficherait un chiffre figé à mi-course
        if (reduce || document.hidden) { el.textContent = pre + target + suf; io.unobserve(el); return; }
        // si l'onglet passe en arrière-plan pendant l'animation, on saute à la valeur finale
        document.addEventListener('visibilitychange', function fin() {
          if (document.hidden) { el.textContent = pre + target + suf; dur = 0; }
          document.removeEventListener('visibilitychange', fin);
        });
        var t0 = performance.now(), dur = 1100;
        (function tick(now) {
          var p = clamp((now - t0) / dur, 0, 1);
          el.textContent = pre + Math.round(target * (1 - Math.pow(1 - p, 3))) + suf;
          if (p < 1) requestAnimationFrame(tick);
        })(t0);
        io.unobserve(el);
      });
    }, { threshold: 0.5 });
    els.forEach(function (el) { io.observe(el); });
  })();

  /* ---------- NAV : sticky, auto-hide, progression, lien actif ---------- */
  (function () {
    var nav = $('#nav'), bar = $('#progress'), mbar = $('#mbar');
    var links = $$('.nav__links a');
    var last = 0, ticking = false;

    function frame() {
      var y = scrollY;
      var h = document.documentElement.scrollHeight - innerHeight;
      if (bar) bar.style.transform = 'scaleX(' + (h > 0 ? clamp(y / h, 0, 1) : 0) + ')';
      nav.classList.toggle('is-stuck', y > 40);
      nav.classList.toggle('is-hidden', y > 560 && y > last && !$('#drawer').classList.contains('is-open'));
      if (mbar) mbar.classList.toggle('is-on', y > 400);
      last = y;
      ticking = false;
    }
    addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(frame); }
    }, { passive: true });
    frame();

    // surlignage de l'ancre courante — uniquement pour les liens internes à la page
    var anchors = links.filter(function (a) { return a.getAttribute('href').charAt(0) === '#'; });
    if ('IntersectionObserver' in window && anchors.length) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          anchors.forEach(function (a) {
            a.classList.toggle('is-on', a.getAttribute('href') === '#' + e.target.id);
          });
        });
      }, { rootMargin: '-45% 0px -50% 0px' });
      anchors.forEach(function (a) {
        var s = document.getElementById(a.getAttribute('href').slice(1));
        if (s) io.observe(s);
      });
    }
  })();

  /* ---------- DRAWER MOBILE ---------- */
  (function () {
    var b = $('#burger'), d = $('#drawer');
    if (!b || !d) return;
    function set(open) {
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
      b.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
      d.classList.toggle('is-open', open);
      d.setAttribute('aria-hidden', open ? 'false' : 'true');
      document.body.classList.toggle('is-locked', open);
    }
    b.addEventListener('click', function () { set(!d.classList.contains('is-open')); });
    $$('a', d).forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  })();

  /* ---------- SCROLL DOUX (data-scroll) ---------- */
  $$('[data-scroll]').forEach(function (el) {
    el.addEventListener('click', function () {
      var t = $(el.dataset.scroll);
      if (t) t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    });
  });

  /* ---------- ARRIVÉE DEPUIS UN CTA : scroll doux vers la cible ----------
     Quand on arrive sur la page contact via un bouton (#rappel, #estimateur…),
     on repositionne en douceur sur la bonne section sans que l'utilisateur scrolle. */
  (function () {
    var hash = location.hash;
    if (!hash || hash.length < 2) return;
    var cible = document.getElementById(hash.slice(1));
    if (!cible) return;
    // Laisse le layout se poser (polices, images) avant de glisser vers la cible.
    addEventListener('load', function () {
      setTimeout(function () {
        cible.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
      }, 120);
    });
  })();

  /* ---------- PARALLAX HERO ---------- */
  (function () {
    var media = $('.hero__media'), hero = $('.hero');
    if (!media || !hero || reduce) return;
    var ticking = false;
    addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = scrollY;
        if (y < innerHeight * 1.2) media.style.transform = 'translate3d(0,' + (y * 0.22) + 'px,0) scale(' + (1 + y * 0.00008) + ')';
        ticking = false;
      });
    }, { passive: true });
  })();

  /* ---------- SIGNATURE : SLIDER AVANT / APRÈS ---------- */
  (function () {
    var frame = $('#baFrame'), wrap = $('#baBeforeWrap'), handle = $('#baHandle');
    if (!frame || !wrap || !handle) return;
    var pos = 50, dragging = false;

    function apply(p) {
      pos = clamp(p, 2, 98);
      wrap.style.clipPath = 'inset(0 ' + (100 - pos) + '% 0 0)';
      handle.style.left = pos + '%';
      handle.setAttribute('aria-valuenow', Math.round(pos));
    }
    function fromEvent(e) {
      var r = frame.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      apply((x / r.width) * 100);
    }
    function down(e) { dragging = true; frame.classList.add('is-drag'); fromEvent(e); }
    function move(e) { if (dragging) { fromEvent(e); if (e.cancelable && e.touches) e.preventDefault(); } }
    function up() { dragging = false; frame.classList.remove('is-drag'); }

    frame.addEventListener('mousedown', down);
    addEventListener('mousemove', move);
    addEventListener('mouseup', up);
    frame.addEventListener('touchstart', down, { passive: true });
    addEventListener('touchmove', move, { passive: false });
    addEventListener('touchend', up);
    handle.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { apply(pos - 4); e.preventDefault(); }
      if (e.key === 'ArrowRight') { apply(pos + 4); e.preventDefault(); }
    });

    apply(50);

    // démo automatique au premier passage dans le viewport
    if (!reduce && 'IntersectionObserver' in window) {
      var done = false;
      var io = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting || done) return;
        done = true; io.disconnect();
        var t0 = performance.now();
        (function tick(now) {
          if (dragging) return;
          var p = clamp((now - t0) / 2000, 0, 1);
          var e = p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
          apply(50 + Math.sin(e * Math.PI * 1.5) * 30);
          if (p < 1) requestAnimationFrame(tick); else apply(46);
        })(t0);
      }, { threshold: .45 });
      io.observe(frame);
    }

    // onglets projets
    var tabs = $$('.ba__tab'), before = $('#baBefore'), after = $('#baAfter');
    var title = $('#baTitle'), info = $('#baInfo');
    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        tabs.forEach(function (o) { o.classList.remove('is-on'); o.setAttribute('aria-selected', 'false'); });
        t.classList.add('is-on'); t.setAttribute('aria-selected', 'true');
        frame.style.opacity = '0';
        setTimeout(function () {
          before.src = t.dataset.before;
          after.src = t.dataset.after;
          title.textContent = t.dataset.title;
          info.textContent = t.dataset.info;
          frame.style.opacity = '1';
          apply(50);
        }, 220);
      });
    });
    frame.style.transition = 'opacity .22s ease';
  })();

  /* =========================================================
     PARCOURS DE DIAGNOSTIC
     Qualifie la demande, calcule un score de rentabilite (formule du
     cahier des charges) et prepare le dossier pour Brahim.
     Tout est calcule ici, dans le navigateur : aucun service externe.
     ========================================================= */
  var estimation = null;   // repris par le formulaire de rappel

  (function () {
    var box = $('#diagForm'); if (!box) return;

    // Distance approximative au centre de Toulouse, en km.
    var KM = {
      'Toulouse Centre': 0, 'Capitole': 0, 'Saint-Cyprien': 2, 'Les Carmes': 1, 'Compans': 2,
      'Rangueil': 4, 'Côte Pavée': 3, 'Purpan': 5, 'Saint-Michel': 2, 'Minimes': 3,
      'Croix-Daurade': 5, 'Lardenne': 6, 'Jean Jaurès': 1, 'Busca': 2,
      'Blagnac': 8, 'Colomiers': 11, 'Tournefeuille': 10, 'Balma': 7, "L'Union": 7,
      'Ramonville': 7, 'Saint-Orens': 9, 'Cugnaux': 10, 'Portet-sur-Garonne': 9,
      'Muret': 22, 'Plaisance-du-Touch': 14, 'Castanet-Tolosan': 12, 'Aucamville': 6,
      'Fenouillet': 10, 'Launaguet': 7, 'Quint-Fonsegrives': 9, 'Autre commune': 18
    };

    var BUDGETS = L.budgets;

    var steps = $$('.diag__step', box);
    var rail = $('#diagRail'), count = $('#diagCount');
    var next = $('#diagNext'), prev = $('#diagPrev'), nav = $('.diag__nav', box);
    var res = $('#diagRes'), photos = $('#diagPhotos'), thumbs = $('#diagThumbs');
    var i = 0, files = [];

    function fam() {
      var t = box.querySelector('input[name=type]:checked');
      return t ? t.dataset.fam : 'dep';
    }
    function actifs() {
      var f = fam();
      return steps.filter(function (st) { return !st.dataset.fam || st.dataset.fam === f; });
    }
    function checked(name) { return box.querySelector('input[name=' + name + ']:checked'); }

    function budgetOptions() {
      var wrap = $('#diagBudget'), list = BUDGETS[fam()];
      var courant = checked('budget');
      var garde = courant ? courant.value : null;
      wrap.innerHTML = list.map(function (b, k) {
        var sel = garde ? (b[0] === garde) : (k === 2);
        return '<label class="opt"><input type="radio" name="budget" value="' + b[0] +
               '" data-b="' + b[1] + '"' + (sel ? ' checked' : '') +
               '><span><b>' + b[0] + '</b></span></label>';
      }).join('');
      if (!wrap.querySelector('input:checked')) wrap.querySelector('input').checked = true;
    }

    function show(n) {
      var list = actifs();
      i = clamp(n, 0, list.length - 1);
      steps.forEach(function (st) { st.classList.remove('is-on'); });
      list[i].classList.add('is-on');
      if (list[i].dataset.step === 'budget') budgetOptions();
      rail.style.width = ((i + 1) / list.length * 100) + '%';
      count.textContent = L.step(i + 1, list.length);
      prev.hidden = i === 0;
      next.textContent = i === list.length - 1 ? L.last : L.next;
    }

    // photos : aperçu local, rien n'est envoyé avant validation
    if (photos) {
      photos.addEventListener('change', function () {
        files = Array.prototype.slice.call(photos.files).slice(0, 3);
        thumbs.innerHTML = '';
        files.forEach(function (f) {
          var img = document.createElement('img');
          img.alt = 'Aperçu de la photo ' + f.name;
          img.src = URL.createObjectURL(f);
          img.onload = function () { URL.revokeObjectURL(img.src); };
          thumbs.appendChild(img);
        });
      });
    }

    function nice(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }

    function calcule() {
      var t = checked('type'), f = fam();
      var b = checked('budget'), acc = checked('acces');
      var secteur = $('#diagSecteur').value;
      var km = KM[secteur] === undefined ? 12 : KM[secteur];
      var duree = +t.dataset.duree;

      // --- formule du cahier des charges ---
      var pUrg = f === 'reno' ? 2 : +checked('urgence').dataset.u;          // 0-3
      var pBud = +b.dataset.b;                                              // 0-3
      var pDur = f === 'reno' ? 2 : (duree < 1 ? 1 : duree <= 3 ? 2 : 1.5); // 0-2
      var pDis = km < 5 ? 1 : km <= 15 ? 0.6 : 0.2;                         // 0-1
      var proba = +t.dataset.proba * (+acc.dataset.acc) * (files.length ? 1 : 0.82);
      var score = Math.round((pUrg + pBud + pDur + pDis + proba) * 10) / 10;

      var d = {
        type: t.value, fam: f, score: score, proba: Math.round(proba * 100),
        urgence: f === 'reno' ? 'Projet de rénovation' : checked('urgence').value,
        budget: b.value, secteur: secteur, km: km,
        logement: checked('logement').value, acces: acc.value,
        duree: f === 'reno' ? 'plusieurs jours'
          : '≈ ' + Math.floor(duree) + ' h' + (duree % 1 ? ' ' + (duree % 1) * 60 : ''),
        photos: files.length,
        nom: $('#diagNom').value.trim(), tel: $('#diagTel').value.trim(),
        message: $('#diagMsg').value.trim()
      };

      if (f === 'reno') {
        var base = +t.dataset.base * (+checked('surface').dataset.mult) *
                   (+checked('finition').dataset.mult) + (+checked('depose').dataset.add);
        d.low = Math.round(base * 0.85 / 50) * 50;
        d.high = Math.round(base * 1.25 / 50) * 50;
        d.surface = checked('surface').value;
        d.finition = checked('finition').value;
        d.depose = checked('depose').value;
      }
      return d;
    }

    function pastille(sc) {
      if (sc >= 7) return ['🟢', L.hot, 'is-hot'];
      if (sc >= 5) return ['🟠', L.mid, 'is-mid'];
      return ['🔴', L.low, 'is-low'];
    }

    function dossier(d) {
      var p = pastille(d.score);
      var l = [];
      l.push(p[0] + ' ' + (d.urgence.indexOf('AUJOURD') === 0 ? 'URGENCE' : d.type.toUpperCase()) +
             ' | SCORE RENTABILITÉ : ' + d.score.toFixed(1) + '/10');
      l.push('');
      l.push('Client : ' + d.nom + ' | ' + d.tel);
      l.push('Secteur : ' + d.secteur + ' (~' + d.km + ' km du centre)');
      l.push('Type : ' + d.type);
      l.push('Urgence : ' + d.urgence);
      l.push('Budget annoncé : ' + d.budget);
      l.push('Durée estimée : ' + d.duree);
      l.push('Logement : ' + d.logement + ' — accès ' + d.acces.toLowerCase());
      l.push('Photos jointes : ' + (d.photos ? d.photos : 'aucune'));
      l.push('Probabilité 1re visite décisive : ' + d.proba + ' %');
      if (d.low) {
        l.push('Estimation site : ' + nice(d.low) + ' € – ' + nice(d.high) + ' €' +
               ' (' + d.surface + ', ' + d.finition + ', ' + d.depose.toLowerCase() + ')');
      }
      if (d.message) { l.push(''); l.push('Message du client : ' + d.message); }
      return l.join('\n');
    }

    function resume(d) {
      var l = ['Bonjour Renauva, demande via le site :',
               '• ' + d.type,
               '• Urgence : ' + d.urgence,
               '• Secteur : ' + d.secteur,
               '• Budget : ' + d.budget,
               '• ' + d.logement + ', accès ' + d.acces.toLowerCase()];
      if (d.low) l.push('• Estimation site : ' + nice(d.low) + ' € – ' + nice(d.high) + ' €');
      if (d.message) l.push('• ' + d.message);
      l.push('• ' + d.nom + ' — ' + d.tel);
      if (d.photos) l.push('(j\'ai ' + d.photos + ' photo' + (d.photos > 1 ? 's' : '') + ' à vous envoyer juste après)');
      return l.join('\n');
    }

    var courant = null;

    function termine() {
      var nom = $('#diagNom'), tel = $('#diagTel'), rgpd = $('#diagRgpd');
      if (!nom.value.trim() || !tel.value.trim() || !rgpd.checked) {
        [nom, tel, rgpd].forEach(function (el) {
          if (el.checkValidity && !el.checkValidity()) el.reportValidity();
        });
        return;
      }
      var d = courant = calcule();
      estimation = d.low ? { low: d.low, high: d.high, piece: d.type,
                             text: d.type + ' — ' + nice(d.low) + ' € à ' + nice(d.high) + ' €' } : null;

      var p = pastille(d.score);
      var pill = $('#diagPill');
      pill.textContent = p[0] + ' ' + p[1] + ' · ' + d.score.toFixed(1) + '/10';
      pill.className = 'diag__pill ' + p[2];

      $('#diagResTitle').textContent = d.urgence.indexOf('AUJOURD') === 0
        ? L.urgentTitle : L.readyTitle;

      $('#diagEstim').innerHTML = d.low
        ? '<p class="diag__resLabel">' + L.rangeLabel + '</p><p class="diag__amount">' +
          nice(d.low) + ' € <em>–</em> ' + nice(d.high) + ' €</p>' +
          '<p class="diag__disc">' + L.disc + '</p>'
        : '<p class="diag__disc">' + L.discNo + '</p>';

      var recap = $('#diagRecap');
      recap.innerHTML = '';
      [d.type, d.urgence, d.secteur, d.budget, d.logement + ' · ' + L.access + ' ' + d.acces.toLowerCase(),
       d.photos ? d.photos + ' ' + (d.photos > 1 ? L.photos : L.photo) : L.noPhoto
      ].forEach(function (v) {
        var li = document.createElement('li'); li.textContent = v; recap.appendChild(li);
      });

      $('#diagWa').href = 'https://wa.me/' + WA;
      $('#dmSubject').value = (d.score >= 7 ? '[PRIORITAIRE] ' : '') +
        (d.urgence.indexOf('AUJOURD') === 0 ? '[URGENCE] ' : '') +
        d.type + ' — ' + d.secteur + ' — score ' + d.score.toFixed(1) + '/10';
      $('#dmMessage').value = dossier(d);
      $('#dmNom').value = d.nom;
      $('#dmTel').value = d.tel;

      box.hidden = true; nav.hidden = true; res.hidden = false;
      rail.style.width = '100%';
      count.textContent = L.done;
      res.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    }

    next.addEventListener('click', function () {
      if (i === actifs().length - 1) { termine(); return; }
      show(i + 1);
    });
    prev.addEventListener('click', function () { show(i - 1); });
    $('#diagRestart').addEventListener('click', function () {
      res.hidden = true; box.hidden = false; nav.hidden = false; show(0);
    });

    $('#diagMail').addEventListener('click', function () {
      var form = $('#diagMailForm'), note = $('#diagNote'), btn = $('#diagMail');
      note.className = 'f__note';
      var key = form.querySelector('[name=access_key]').value;
      var mailPret = key && key.indexOf('VOTRE_CLE') !== 0;
      btn.disabled = true;
      var label = btn.textContent;
      btn.textContent = L.sending;
      var fd = new FormData(form);
      files.forEach(function (f, k) { fd.append('photo_' + (k + 1), f, f.name); });
      fd.append('page', location.href);

      var p = pastille(courant.score);
      var base = enregistre({
        source: 'diagnostic',
        score: courant.score, priorite: p[1],
        nom: courant.nom, telephone: courant.tel, secteur: courant.secteur, km: courant.km,
        type_demande: courant.type, urgence: courant.urgence, budget: courant.budget,
        duree: courant.duree, logement: courant.logement, acces: courant.acces,
        proba: courant.proba, estim_bas: courant.low || null, estim_haut: courant.high || null,
        message: courant.message
      }, files);
      var mail = mailPret
        ? fetch(form.action, { method: 'POST', body: fd })
            .then(function (r) { return r.json(); })
            .then(function (r) { return !!r.success; })
            .catch(function () { return false; })
        : Promise.resolve(false);

      Promise.all([base, mail]).then(function (res) {
        if (res[0] || res[1]) {
          note.className = 'f__note is-ok';
          note.textContent = L.sentOk;
        } else {
          note.className = 'f__note is-err';
          note.textContent = L.sentErr;
          btn.disabled = false;
        }
      }).finally(function () { btn.textContent = label; });
    });

    $$('input[name=type]', box).forEach(function (r) {
      r.addEventListener('change', function () { show(0); });
    });

    show(0);
  })();

  /* ---------- MODE URGENCE ---------- */
  (function () {
    var urg = $('#urg'); if (!urg) return;
    function set(open) {
      urg.classList.toggle('is-open', open);
      urg.setAttribute('aria-hidden', open ? 'false' : 'true');
      document.body.classList.toggle('is-locked', open);
      document.body.classList.toggle('urgence-mode', open);
      if (open) { var b = $('.btn--red', urg); if (b) b.focus(); }
    }
    $$('[data-urgence]').forEach(function (b) { b.addEventListener('click', function () { set(true); }); });
    $('#urgClose').addEventListener('click', function () { set(false); });
    $('.urg__bg', urg).addEventListener('click', function () { set(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
    // auto-ouverture si l'URL contient #urgence
    if (location.hash === '#urgence') setTimeout(function () { set(true); }, 900);
  })();

  /* ---------- FORMULAIRE ---------- */
  (function () {
    var form = $('#leadForm'); if (!form) return;
    var note = $('#fNote'), btn = $('#fSubmit'), files = $('#fPhotos'), filesTxt = $('#fFiles');

    if (files) {
      files.addEventListener('change', function () {
        var list = Array.prototype.slice.call(files.files);
        if (list.length > 3) { filesTxt.textContent = L.filesMax; }
        else if (list.length) { filesTxt.textContent = list.map(function (f) { return f.name; }).join(', '); }
        else { filesTxt.textContent = ''; }
      });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      note.className = 'f__note';
      note.textContent = '';

      if (!form.checkValidity()) { form.reportValidity(); return; }

      btn.disabled = true;
      var label = btn.textContent;
      btn.textContent = L.sending;

      var v = function (n) { var el = form.querySelector('[name=' + n + ']'); return el ? el.value : ''; };

      var bot = form.querySelector('[name=botcheck]');
      var urg = form.querySelector('[name=urgence_2h]');
      var msg = v('message');
      if (estimation) msg += (msg ? '\n\n' : '') + 'Estimation faite sur le site : ' + estimation.text;

      var payload = {
        source: 'formulaire',
        botcheck: bot && bot.checked ? 1 : 0,
        urgence_2h: urg && urg.checked ? 1 : 0,
        nom: v('nom'), telephone: v('telephone'), email: v('email'),
        secteur: v('secteur'), adresse: v('adresse'), disponibilite: v('disponibilite'),
        type_demande: v('projet'), budget: v('budget'), message: msg
      };

      enregistre(payload, files ? files.files : null).then(function (ok) {
        if (ok) {
          form.reset();
          if (filesTxt) filesTxt.textContent = '';
          note.className = 'f__note is-ok';
          note.textContent = L.formOk;
        } else {
          note.className = 'f__note is-err';
          note.textContent = L.formErr;
        }
      }).finally(function () { btn.disabled = false; btn.textContent = label; });
    });
  })();

  /* =========================================================
     RÉSEAU — animation pilotée par le scroll
     Le tracé se dessine puis l'eau y circule, en fonction de la
     position de la page. Aucune librairie : SVG + rAF.
     ========================================================= */
  (function () {
    var rail = $('.pipes__rail'); if (!rail) return;
    var draw = $('#pipesDraw'), flow = $('#pipesFlow');
    var valve = $('#pipesValve'), out = $('#pipesOut');
    var nodes = $$('#pipesNodes circle'), etapes = $$('.pipes__steps li');
    var gauge = $('#pipesGauge'), pct = $('#pipesPct');

    var lenDraw = draw.getTotalLength(), lenFlow = flow.getTotalLength();
    draw.style.strokeDasharray = lenDraw;
    flow.style.strokeDasharray = lenFlow;

    // Position des jonctions le long du tracé, pour les allumer au bon moment.
    // Calculé une seule fois, à la première apparition à l'écran : inutile de
    // faire ces relevés au chargement d'une section qu'on ne verra peut-être jamais.
    var seuils = null;
    function mesure() {
      seuils = nodes.map(function (n) {
        var cx = +n.getAttribute('cx'), cy = +n.getAttribute('cy'), best = 0, dmin = 1e9;
        for (var i = 0; i <= 120; i++) {
          var p = flow.getPointAtLength(lenFlow * i / 120);
          var d = (p.x - cx) * (p.x - cx) + (p.y - cy) * (p.y - cy);
          if (d < dmin) { dmin = d; best = i / 120; }
        }
        return best;
      });
    }

    function etat(p) {
      if (!seuils) mesure();
      // 0 → 0,45 : le tuyau se dessine. 0,25 → 1 : l'eau progresse.
      var dessine = clamp(p / 0.45, 0, 1);
      var eau = clamp((p - 0.25) / 0.7, 0, 1);

      draw.style.strokeDashoffset = lenDraw * (1 - dessine);
      flow.style.strokeDashoffset = lenFlow * (1 - eau);

      valve.classList.toggle('is-open', p > 0.12);
      out.classList.toggle('is-on', eau > 0.97);

      nodes.forEach(function (n, i) { n.classList.toggle('is-on', eau >= seuils[i] - 0.02); });

      var actif = p < 0.18 ? 0 : p < 0.42 ? 1 : p < 0.7 ? 2 : 3;
      etapes.forEach(function (li, i) { li.classList.toggle('is-live', i === actif); });

      var v = Math.round(eau * 100);
      gauge.style.width = v + '%';
      pct.textContent = v + ' %';
    }

    if (reduce) { etat(1); return; }

    var ticking = false, visible = false;
    function frame() {
      var r = rail.getBoundingClientRect();
      var course = r.height - innerHeight;
      var p = course > 0 ? clamp(-r.top / course, 0, 1) : 0;
      etat(p);
      ticking = false;
    }
    function onScroll() {
      if (!visible || ticking) return;
      ticking = true;
      requestAnimationFrame(frame);
    }
    addEventListener('scroll', onScroll, { passive: true });
    addEventListener('resize', frame);

    // On ne calcule rien tant que la section n'est pas à l'écran.
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) {
        visible = en[0].isIntersecting;
        if (visible) frame();
      }, { rootMargin: '120px 0px' }).observe(rail);
    } else { visible = true; }
    frame();
  })();

  /* ---------- POP-UP DE CAPTURE ---------- */
  (function () {
    var pop = $('#pop'); if (!pop) return;
    var KEY = 'renauva_pop';
    var JOURS = 7;            // on ne réaffiche pas avant 7 jours
    var DELAI = 26000;        // ou après 26 s de lecture
    var SCROLL = 0.5;         // ou à mi-page
    var shown = false, done = false;

    function seen() {
      try {
        var v = localStorage.getItem(KEY);
        return v && (Date.now() - +v) < JOURS * 864e5;
      } catch (e) { return false; }
    }
    function mark() { try { localStorage.setItem(KEY, Date.now()); } catch (e) {} }

    function open() {
      if (shown || seen() || done) return;
      // jamais par-dessus une urgence ou un menu ouvert
      if (document.body.classList.contains('is-locked')) return;
      shown = true; mark();
      pop.classList.add('is-open');
      pop.setAttribute('aria-hidden', 'false');
      var f = pop.querySelector('input[name=nom]');
      if (f) setTimeout(function () { f.focus(); }, 450);
    }
    function close() {
      pop.classList.remove('is-open');
      pop.setAttribute('aria-hidden', 'true');
    }

    $$('[data-pop-close]', pop).forEach(function (b) { b.addEventListener('click', close); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

    // déclencheurs
    var t = setTimeout(open, DELAI);
    addEventListener('scroll', function onScroll() {
      var h = document.documentElement.scrollHeight - innerHeight;
      if (h > 0 && scrollY / h > SCROLL) { removeEventListener('scroll', onScroll); open(); }
    }, { passive: true });
    // intention de sortie (desktop uniquement)
    if (!matchMedia('(pointer: coarse)').matches) {
      document.addEventListener('mouseout', function (e) {
        if (!e.relatedTarget && e.clientY <= 0) open();
      });
    }
    // inutile de relancer si la personne est déjà en train de nous contacter
    ['#leadForm', '#qualif', '.call'].forEach(function (sel) {
      var el = $(sel); if (!el || !('IntersectionObserver' in window)) return;
      new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) { done = true; clearTimeout(t); }
      }, { threshold: .3 }).observe(el);
    });

    // envoi
    var form = $('#popForm'), note = $('#popNote'), btn = $('#popSubmit');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      note.className = 'f__note';
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var key = form.querySelector('[name=access_key]').value;
      var mailPret = key && key.indexOf('VOTRE_CLE') !== 0;
      btn.disabled = true;
      var label = btn.textContent;
      btn.textContent = L.sending;
      var fd = new FormData(form);
      fd.append('page', location.href);
      var base = enregistre({
        source: 'popup',
        nom: (form.querySelector('[name=nom]') || {}).value || '',
        telephone: (form.querySelector('[name=telephone]') || {}).value || '',
        type_demande: (form.querySelector('[name=projet]') || {}).value || ''
      });
      var mail = mailPret
        ? fetch(form.action, { method: 'POST', body: fd })
            .then(function (r) { return r.json(); })
            .then(function (r) { return !!r.success; })
            .catch(function () { return false; })
        : Promise.resolve(false);

      Promise.all([base, mail]).then(function (res) {
        if (res[0] || res[1]) {
          form.reset();
          note.className = 'f__note is-ok';
          note.textContent = L.formOk;
          setTimeout(close, 2200);
        } else {
          note.className = 'f__note is-err';
          note.textContent = L.formErr;
        }
      }).finally(function () { btn.disabled = false; btn.textContent = label; });
    });
  })();

  /* ---------- DIVERS ---------- */
  var y = $('#year'); if (y) y.textContent = new Date().getFullYear();
})();
