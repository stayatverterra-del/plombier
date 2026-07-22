#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renauva — publication sur Cloudflare Pages.

    python3 publish.py            # construit puis déploie
    python3 publish.py --dry      # construit dist/ sans déployer

Ne publie QUE les fichiers destinés aux visiteurs. Le code source (build.py,
publish.py) et la documentation interne (README.md) restent en local : ils
contiennent des notes de travail qui n'ont rien à faire en ligne.
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
PROJET = "renauva"

# Tout ce qui n'est pas listé ici ne part pas en ligne.
FICHIERS = ["robots.txt", "sitemap.xml", "_headers", "_redirects", "suivi.html"]
DOSSIERS = ["assets", "en", "functions"]


def main():
    dry = "--dry" in sys.argv

    print("→ génération des pages")
    subprocess.run([sys.executable, os.path.join(ROOT, "build.py")], check=True, cwd=ROOT)

    print("→ préparation de dist/")
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    for f in pages:
        shutil.copy2(os.path.join(ROOT, f), DIST)
    pages += sorted("en/" + f for f in os.listdir(os.path.join(ROOT, "en"))
                    if f.endswith(".html"))
    for f in FICHIERS:
        src = os.path.join(ROOT, f)
        if os.path.exists(src):
            shutil.copy2(src, DIST)
    for d in DOSSIERS:
        shutil.copytree(os.path.join(ROOT, d), os.path.join(DIST, d))

    total = sum(os.path.getsize(os.path.join(p, f))
                for p, _, fs in os.walk(DIST) for f in fs)
    nb = sum(len(fs) for _, _, fs in os.walk(DIST))
    print("   %d pages, %d fichiers, %.1f Mo" % (len(pages), nb, total / 1048576.0))

    # garde-fou : rien d'interne ne doit se retrouver dans dist/
    interdits = [f for f in os.listdir(DIST)
                 if f in ("build.py", "publish.py", "README.md") or f.endswith(".py")]
    if interdits:
        sys.exit("✘ fichiers internes dans dist/ : %s" % interdits)

    if dry:
        print("→ --dry : rien n'a été déployé. Contenu prêt dans dist/")
        return

    print("→ déploiement sur Cloudflare Pages")
    # wrangler.toml fournit le binding D1 : on déploie sans passer le dossier en argument
    subprocess.run(["npx", "--yes", "wrangler@latest", "pages", "deploy",
                    "--branch=main", "--commit-dirty=true"],
                   check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
