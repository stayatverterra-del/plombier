/**
 * Plombier — Worker unique : sert le site statique + l'API des demandes.
 *
 * Routing :
 *   - /api/lead   → réception d'une demande du formulaire (POST)
 *   - /api/leads  → consultation / màj / suppression (réservé, clé ADMIN_KEY)
 *   - tout le reste → fichiers statiques (env.ASSETS)
 *
 * Bindings attendus (wrangler.toml) :
 *   - DB        : base D1 « plombier-leads »
 *   - ASSETS    : fichiers statiques du site
 * Secret :
 *   - ADMIN_KEY : mot de passe du dashboard /suivi
 */

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

/* Filet de sécurité : garantit l'existence des tables même si les migrations
   n'ont pas tourné au déploiement. Exécuté une seule fois par isolate. */
let schemaPret = false;
async function ensureSchema(env) {
  if (schemaPret) return;
  await env.DB.batch([
    env.DB.prepare(
      `CREATE TABLE IF NOT EXISTS demandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, recu_le TEXT NOT NULL, source TEXT NOT NULL,
        statut TEXT NOT NULL DEFAULT 'À rappeler', score REAL, priorite TEXT, nom TEXT,
        telephone TEXT, secteur TEXT, km INTEGER, type_demande TEXT, urgence TEXT, budget TEXT,
        duree TEXT, logement TEXT, acces TEXT, proba INTEGER, estim_bas INTEGER, estim_haut INTEGER,
        message TEXT, nb_photos INTEGER DEFAULT 0, page TEXT, langue TEXT, adresse TEXT,
        disponibilite TEXT, urgence_2h INTEGER DEFAULT 0, email TEXT)`
    ),
    env.DB.prepare(
      `CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, demande_id INTEGER NOT NULL, nom TEXT,
        type_mime TEXT, donnees TEXT NOT NULL,
        FOREIGN KEY (demande_id) REFERENCES demandes(id))`
    ),
  ]);
  schemaPret = true;
}

const json = (obj, status = 200, extra = {}) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS, ...extra },
  });

const bad = () =>
  new Response('Clé invalide', { status: 401, headers: { 'Content-Type': 'text/plain' } });

function csvCell(v) {
  const s = v == null ? '' : String(v);
  return /[";\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

/* ------------------------------------------------------------------ */
/* Notification WhatsApp (best-effort, ne bloque jamais l'enregistrement) */
/* ------------------------------------------------------------------ */
async function notifieWhatsApp(env, d, id, origin) {
  const token = env.WHATSAPP_TOKEN;
  const phoneId = env.WHATSAPP_PHONE_NUMBER_ID;
  if (!token || !phoneId) return; // pas configuré : on ne fait rien.

  const dest = (env.WHATSAPP_RECIPIENT_NUMBER || '33686458557').replace(/[^0-9]/g, '');
  const type = d.type_demande || '';
  const urgent = d.urgence_2h || /urgence/i.test(type) || /urgence/i.test(d.urgence || '');
  const ligneUrg = urgent ? '🚨 URGENCE (< 2h)' : '🟢 Normal';

  const corps =
    '🚨 NOUVELLE DEMANDE D\'INTERVENTION\n\n' +
    '👤 CLIENT :\n' +
    '- Nom : ' + (d.nom || '—') + '\n' +
    '- Tél : ' + (d.telephone || '—') + '\n' +
    (d.email ? '- Email : ' + d.email + '\n' : '') +
    '- Adresse : ' + (d.adresse || d.secteur || '—') +
      (d.adresse && d.secteur ? ' (' + d.secteur + ')' : '') + '\n\n' +
    '⚡ URGENCE & DISPOS :\n' +
    '- Urgence : ' + ligneUrg + '\n' +
    '- Disponibilités : ' + (d.disponibilite || 'Non précisé') + '\n\n' +
    '🛠️ DÉTAILS DU PROJET :\n' +
    '- Type de demande : ' + (type || '—') + '\n' +
    '- Budget : ' + (d.budget || '—') + '\n' +
    '- Description du problème :\n"' + (d.message || '—') + '"\n\n' +
    '📁 MÉDIAS :\n' +
    '- ' + (Array.isArray(d.photos) && d.photos.length
      ? d.photos.length + ' photo(s) — voir sur ' + (origin || '') + '/suivi'
      : 'Aucun média joint');

  const url = 'https://graph.facebook.com/v21.0/' + phoneId + '/messages';
  const r = await fetch(url, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messaging_product: 'whatsapp',
      to: dest,
      type: 'text',
      text: { preview_url: true, body: corps },
    }),
  });
  if (!r.ok) console.error('WhatsApp KO', r.status, await r.text());
}

/* ------------------------------------------------------------------ */
/* POST /api/lead — réception d'une demande                            */
/* ------------------------------------------------------------------ */
async function receptionLead(request, env, ctx) {
  try {
    const d = await request.json();

    if (d.botcheck) return json({ success: true, ignored: true });
    if (!d.telephone && !d.nom) return json({ success: false, error: 'champs vides' }, 400);

    const num = (v) => {
      const n = parseFloat(String(v ?? '').replace(',', '.'));
      return Number.isFinite(n) ? n : null;
    };
    const txt = (v, max = 2000) => (v == null ? null : String(v).slice(0, max));

    const res = await env.DB.prepare(
      `INSERT INTO demandes
        (recu_le, source, score, priorite, nom, telephone, secteur, km, type_demande,
         urgence, budget, duree, logement, acces, proba, estim_bas, estim_haut,
         message, nb_photos, page, langue, adresse, disponibilite, urgence_2h, email)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
    ).bind(
      new Date().toISOString(),
      txt(d.source || 'formulaire', 30),
      num(d.score), txt(d.priorite, 40),
      txt(d.nom, 120), txt(d.telephone, 40), txt(d.secteur, 120), num(d.km),
      txt(d.type_demande, 120), txt(d.urgence, 80), txt(d.budget, 80), txt(d.duree, 60),
      txt(d.logement, 40), txt(d.acces, 40), num(d.proba),
      num(d.estim_bas), num(d.estim_haut),
      txt(d.message, 4000),
      Array.isArray(d.photos) ? d.photos.length : 0,
      txt(d.page, 300), txt(d.langue, 5),
      txt(d.adresse, 200), txt(d.disponibilite, 40), d.urgence_2h ? 1 : 0,
      txt(d.email, 160)
    ).run();

    const id = res.meta.last_row_id;

    if (Array.isArray(d.photos) && d.photos.length) {
      const stmt = env.DB.prepare(
        'INSERT INTO photos (demande_id, nom, type_mime, donnees) VALUES (?,?,?,?)'
      );
      await env.DB.batch(
        d.photos.slice(0, 3).map((p) =>
          stmt.bind(id, txt(p.nom, 200), txt(p.type, 40), String(p.donnees || '').slice(0, 900000))
        )
      );
    }

    const origin = new URL(request.url).origin;
    const notif = notifieWhatsApp(env, d, id, origin).catch((e) => console.error(e));
    if (ctx && ctx.waitUntil) ctx.waitUntil(notif);

    return json({ success: true, id });
  } catch (err) {
    return json({ success: false, error: String(err) }, 500);
  }
}

/* ------------------------------------------------------------------ */
/* /api/leads — consultation / màj / suppression (protégé ADMIN_KEY)   */
/* ------------------------------------------------------------------ */
async function listeLeads(request, env) {
  const url = new URL(request.url);
  if (url.searchParams.get('cle') !== env.ADMIN_KEY) return bad();

  const photoId = url.searchParams.get('photo');
  if (photoId) {
    const p = await env.DB.prepare('SELECT type_mime, donnees FROM photos WHERE id = ?')
      .bind(photoId).first();
    if (!p) return new Response('introuvable', { status: 404 });
    const bin = Uint8Array.from(atob(p.donnees), (c) => c.charCodeAt(0));
    return new Response(bin, {
      headers: { 'Content-Type': p.type_mime || 'image/jpeg', 'Cache-Control': 'private, max-age=3600' },
    });
  }

  const { results } = await env.DB.prepare(
    `SELECT d.*, (SELECT group_concat(id) FROM photos WHERE demande_id = d.id) AS photo_ids
       FROM demandes d ORDER BY d.recu_le DESC LIMIT 500`
  ).all();

  if (url.searchParams.get('format') === 'csv') {
    const cols = ['recu_le', 'statut', 'score', 'priorite', 'nom', 'telephone', 'email',
      'secteur', 'adresse', 'km', 'type_demande', 'urgence', 'urgence_2h', 'disponibilite',
      'budget', 'duree', 'logement', 'acces', 'proba',
      'estim_bas', 'estim_haut', 'message', 'nb_photos', 'source'];
    const entetes = ['Reçu le', 'Statut', 'Score /10', 'Priorité', 'Nom', 'Téléphone', 'E-mail',
      'Secteur', 'Adresse', 'Km', 'Type de demande', 'Urgence', 'Urgence <2h', 'Disponibilité',
      'Budget', 'Durée', 'Logement', 'Accès',
      'Proba 1re visite', 'Estim. basse', 'Estim. haute', 'Message', 'Photos', 'Source'];
    const lignes = [entetes.join(';')].concat(
      results.map((r) => cols.map((c) => csvCell(r[c])).join(';'))
    );
    return new Response('﻿' + lignes.join('\r\n'), {
      headers: {
        'Content-Type': 'text/csv;charset=utf-8',
        'Content-Disposition': 'attachment; filename="demandes-plombier.csv"',
      },
    });
  }

  return json({ demandes: results });
}

async function majStatut(request, env) {
  const url = new URL(request.url);
  if (url.searchParams.get('cle') !== env.ADMIN_KEY) return bad();
  const { id, statut } = await request.json();
  await env.DB.prepare('UPDATE demandes SET statut = ? WHERE id = ?')
    .bind(String(statut).slice(0, 40), id).run();
  return json({ success: true });
}

async function supprimeLeads(request, env) {
  const url = new URL(request.url);
  if (url.searchParams.get('cle') !== env.ADMIN_KEY) return bad();

  const body = await request.json().catch(() => ({}));
  const ids = (Array.isArray(body.ids) ? body.ids : [body.id])
    .map((n) => parseInt(n, 10))
    .filter((n) => Number.isInteger(n));
  if (!ids.length) return json({ success: false, error: 'aucun id' }, 400);

  const marks = ids.map(() => '?').join(',');
  await env.DB.batch([
    env.DB.prepare('DELETE FROM photos WHERE demande_id IN (' + marks + ')').bind(...ids),
    env.DB.prepare('DELETE FROM demandes WHERE id IN (' + marks + ')').bind(...ids),
  ]);
  return json({ success: true, deleted: ids.length });
}

/* ------------------------------------------------------------------ */
/* Entrée                                                              */
/* ------------------------------------------------------------------ */
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    if (path === '/api/lead') {
      if (method === 'OPTIONS') return new Response(null, { headers: CORS });
      if (method === 'POST') { await ensureSchema(env); return receptionLead(request, env, ctx); }
      return new Response('Méthode non autorisée', { status: 405, headers: CORS });
    }

    if (path === '/api/leads') {
      if (method === 'OPTIONS') return new Response(null, { headers: CORS });
      await ensureSchema(env);
      if (method === 'GET') return listeLeads(request, env);
      if (method === 'POST') return majStatut(request, env);
      if (method === 'DELETE') return supprimeLeads(request, env);
      return new Response('Méthode non autorisée', { status: 405, headers: CORS });
    }

    // Tout le reste : fichiers statiques du site.
    return env.ASSETS.fetch(request);
  },
};
