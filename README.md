# Plombier — site + formulaire + dashboard de leads

Site vitrine pour artisan plombier/rénovateur, avec formulaire de contact et
dashboard de suivi des demandes sur `/suivi`. Tout est dans **un seul Worker
Cloudflare** : le site, l'API et la base de données.

---

## 🚀 Déployer sur son propre compte Cloudflare (1 clic)

[![Deploy to Cloudflare](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/quentinjoubert44-code/plombier)

**En cliquant sur ce bouton, Cloudflare fait TOUT tout seul :**

1. Demande de se connecter à **votre** compte Cloudflare (et de connecter GitHub).
2. Copie ce projet dans votre GitHub.
3. **Crée la base de données** (D1) automatiquement.
4. **Crée les tables** automatiquement.
5. Vous demande **un seul truc : un mot de passe** pour le dashboard `/suivi`
   (champ `ADMIN_KEY`). Choisissez-en un long et gardez-le.
6. Déploie le site + le formulaire + le dashboard.

À la fin, tout fonctionne sur votre compte, avec une base vide prête à recevoir
les vraies demandes. **Rien d'autre à régler.**

> Le dashboard s'ouvre sur `votre-site.workers.dev/suivi` — tapez le mot de passe
> choisi à l'étape 5 pour voir les demandes.

---

## Ce que contient le projet

```
plombier/
├── src/index.js           LE WORKER : sert le site + l'API des demandes
├── build.py               source du site (génère les .html) — Python, zéro dépendance
├── index.html, contact.html, suivi.html, …   pages du site (générées)
├── assets/                CSS, JS, images, vidéos
├── migrations/            création automatique des tables (D1)
├── wrangler.toml          config Cloudflare
├── package.json           scripts de déploiement
├── _headers, _redirects   cache, sécurité, redirections
└── .assetsignore          fichiers non servis publiquement (code source)
```

> ⚠️ **Ne jamais éditer les `.html` à la main** : ils sont régénérés par
> `build.py`. Pour changer le contenu du site :
> ```bash
> python3 build.py
> ```

---

## Mettre à jour le site plus tard

Une fois déployé via le bouton, chaque `git push` sur le dépôt redéploie
automatiquement (Cloudflare est relié à GitHub). Cycle de travail :

```bash
# modifier build.py ou assets/, puis :
python3 build.py
git add -A
git commit -m "Description du changement"
git push
```

Pour déployer à la main sans passer par GitHub :

```bash
npm install
npm run deploy      # applique les migrations puis déploie le Worker
```

---

## Changer le mot de passe du dashboard

Le mot de passe (`ADMIN_KEY`) n'est **jamais** dans le code : c'est un secret
Cloudflare. Pour le changer :

```bash
npx wrangler secret put ADMIN_KEY
```

Ou dans le dashboard Cloudflare → le Worker → **Settings → Variables and Secrets**.

---

## Notes techniques

- **Architecture** : un Worker (`src/index.js`) sert les fichiers statiques via
  le binding `ASSETS`, et intercepte `/api/lead` (réception) et `/api/leads`
  (consultation, protégée par `ADMIN_KEY`).
- **Base de données** : Cloudflare D1 (SQLite), binding `DB`. Les tables sont
  créées par les migrations **et** par un filet de sécurité au premier appel API.
- **Notification WhatsApp** (optionnelle) : renseignez les secrets
  `WHATSAPP_TOKEN` et `WHATSAPP_PHONE_NUMBER_ID` pour recevoir chaque demande
  par WhatsApp. Sans eux, tout marche, sans notification.
