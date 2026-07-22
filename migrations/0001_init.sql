-- Plombier — stockage des demandes du site (créé automatiquement au déploiement).
CREATE TABLE IF NOT EXISTS demandes (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  recu_le       TEXT    NOT NULL,
  source        TEXT    NOT NULL,          -- formulaire | diagnostic | popup
  statut        TEXT    NOT NULL DEFAULT 'À rappeler',
  score         REAL,                      -- score de rentabilité /10
  priorite      TEXT,                      -- prioritaire | à évaluer | à planifier
  nom           TEXT,
  telephone     TEXT,
  secteur       TEXT,
  km            INTEGER,
  type_demande  TEXT,
  urgence       TEXT,
  budget        TEXT,
  duree         TEXT,
  logement      TEXT,
  acces         TEXT,
  proba         INTEGER,
  estim_bas     INTEGER,
  estim_haut    INTEGER,
  message       TEXT,
  nb_photos     INTEGER DEFAULT 0,
  page          TEXT,
  langue        TEXT,
  adresse       TEXT,
  disponibilite TEXT,                      -- Matin | Après-midi | Soir | N'importe quand
  urgence_2h    INTEGER DEFAULT 0,         -- 1 si le client demande une intervention sous 2h
  email         TEXT
);

CREATE TABLE IF NOT EXISTS photos (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  demande_id INTEGER NOT NULL,
  nom        TEXT,
  type_mime  TEXT,
  donnees    TEXT NOT NULL,               -- image en base64, redimensionnée côté client
  FOREIGN KEY (demande_id) REFERENCES demandes(id)
);

CREATE INDEX IF NOT EXISTS idx_demandes_date  ON demandes(recu_le DESC);
CREATE INDEX IF NOT EXISTS idx_demandes_score ON demandes(score DESC);
CREATE INDEX IF NOT EXISTS idx_photos_demande ON photos(demande_id);
