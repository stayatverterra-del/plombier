#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renauva — générateur du site multi-pages.

    python3 build.py

Écrit les fichiers .html à la racine du dossier. Le header, le footer, la barre
mobile et l'overlay urgence sont partagés : on ne les édite qu'ici.
"""
import os, re, sys, datetime


ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://renauva.com"
TEL_H = "06 60 75 37 71"
TEL = "+33660753771"
WA = "33660753771"
MAIL = "touatiibrahim650@gmail.com"
V = "39"  # cache-busting des assets

TODAY = datetime.date.today().isoformat()

# ==========================================================================
# AVIS CLIENTS
# ==========================================================================
# ⚠️ NE METTRE ICI QUE DE VRAIS AVIS DE VRAIS CLIENTS.
#
# Publier des témoignages inventés est une pratique commerciale trompeuse
# (art. L121-2 et L121-4 11° du Code de la consommation) : jusqu'à 300 000 €
# d'amende et 2 ans d'emprisonnement, et la DGCCRF contrôle activement le
# secteur du bâtiment. Le risque est pour Brahim.
#
# Tant que cette liste est vide, la section « Avis » ne s'affiche pas du tout
# et aucun balisage de notation n'est envoyé à Google. C'est volontaire.
#
# Format d'une entrée (recopier tel quel en remplaçant le contenu) :
#   dict(prenom="Sophie L.",        # prénom + initiale, comme sur Google
#        lieu="Rangueil, Toulouse",  # quartier ou commune
#        note=5,                     # 1 à 5
#        date="2026-05",             # AAAA-MM
#        motif="Recherche de fuite", # étiquette courte
#        texte="Le texte de l'avis, mot pour mot, sans le réécrire.")
#
# Une fois les vrais avis collés ici : python3 build.py
AVIS = [
    # --- Plomberie / urgence ---
    dict(prenom="Laurent M.", lieu="Toulouse", note=5, date="2026-07", cat="plomberie",
         motif="Fuite d'eau",
         texte="Fuite d'eau découverte le dimanche matin. J'ai appelé Brahim en panique, il est "
               "arrivé en moins d'une heure. Diagnostic ultra rapide, devis clair, réparation faite "
               "sur-le-champ. Professionnel, efficace et sympathique. Je recommande sans hésiter !"),
    dict(prenom="Sophie Delorme", lieu="Toulouse", note=5, date="2026-06", cat="plomberie",
         motif="Chauffe-eau",
         texte="Mon chauffe-eau a lâché au pire moment, en plein hiver. Brahim a eu un créneau dès "
               "le lendemain, remplacement effectué proprement et rapidement. Tarif très honnête "
               "comparé aux autres devis. Vraiment satisfaite. Merci !"),
    dict(prenom="Thomas K.", lieu="Toulouse", note=5, date="2026-06", cat="plomberie",
         motif="Débouchage",
         texte="Débouchage de colonne en urgence. Brahim est intervenu en moins de deux heures, "
               "travail impeccable, chantier laissé propre. Ponctuel, professionnel et très "
               "sympathique. C'est bon de trouver un artisan aussi sérieux. Je le recommande !"),
    dict(prenom="Valérie Gent", lieu="Toulouse", note=5, date="2026-06", cat="plomberie",
         motif="Fuite sous évier",
         texte="Fuite sous l'évier détectée. Brahim a bien tout expliqué avant d'intervenir. "
               "Le travail était soigné, l'intervention rapide, et il a laissé la cuisine nickel. "
               "Très professionnel. Je referai appel à lui sans souci."),
    dict(prenom="Rémi Fontaine", lieu="Toulouse", note=5, date="2026-07", cat="plomberie",
         motif="Fuite &amp; contrôle",
         texte="Problème de fuite : Brahim a diagnostiqué, expliqué, réparé. Mais en plus, il a pris "
               "le temps de bien vérifier tout ce qui était autour pour éviter d'autres problèmes "
               "futurs. Professionnel attentif et vraiment de bon conseil. C'est rare !"),
    dict(prenom="Isabelle Gardin", lieu="Toulouse", note=5, date="2026-06", cat="plomberie",
         motif="Robinetterie &amp; tuyauterie",
         texte="Petit dépannage de robinetterie devenu gros projet, avec le remplacement d'une partie "
               "de la tuyauterie. Au lieu de me la faire à l'envers, Brahim a bien expliqué pourquoi "
               "c'était nécessaire et proposé une solution adaptée. Très honnête. C'est agréable !"),

    # --- Rénovation salle de bains ---
    dict(prenom="Marc Delaunay", lieu="Toulouse", note=5, date="2026-06", cat="sdb",
         motif="Rénovation complète",
         texte="Rénovation complète de notre salle de bains. Brahim nous a proposé des solutions "
               "adaptées à notre budget, du choix des matériaux à la pose. Le rendu est magnifique, "
               "les délais respectés, le chantier était propre tous les jours. Un vrai professionnel. "
               "Bravo !"),
    dict(prenom="Céline R.", lieu="Toulouse", note=5, date="2026-06", cat="sdb",
         motif="Transformation complète",
         texte="Notre vieille salle de bains a été complètement transformée. Brahim a su nous écouter, "
               "proposer un design moderne, et exécuter le travail avec beaucoup de soin. Plomberie, "
               "carrelage, meubles : il a géré tout seul, c'était un vrai gain de temps. Très "
               "satisfaits du résultat !"),
    dict(prenom="Damien T.", lieu="Toulouse", note=5, date="2026-07", cat="sdb",
         motif="Douche à l'italienne",
         texte="Installation d'une douche à l'italienne. Brahim a bien expliqué les étapes, le devis "
               "était détaillé. L'intervention s'est déroulée sans surprise, le travail était très "
               "soigné, et le résultat dépasse nos attentes. Professionnel de A à Z. Je recommande !"),
    dict(prenom="Sandrine Mercier", lieu="Toulouse", note=5, date="2026-06", cat="sdb",
         motif="Petite salle de bains",
         texte="Nous avions une petite salle de bains vétuste. Brahim a proposé une rénovation "
               "complète et bien pensée dans notre budget. Respect des délais, travail soigné, "
               "explications claires tout au long. Notre nouvelle salle de bains est magnifique. "
               "Merci Brahim !"),
    dict(prenom="Pascale Dubois", lieu="Toulouse", note=5, date="2026-06", cat="sdb",
         motif="Salle de bains &amp; plomberie",
         texte="Projet global : rénovation de la salle de bains, remplacement du chauffe-eau et "
               "nouvelle tuyauterie. Brahim a proposé un plan cohérent, clair et dans notre budget. "
               "Tout s'est déroulé sans accroc, travail très soigné. Notre salle de bains est "
               "maintenant moderne et fonctionnelle. Vraiment satisfaits !"),
    dict(prenom="Gabriel M.", lieu="Toulouse", note=5, date="2026-06", cat="sdb",
         motif="Appartement ancien",
         texte="Ancien appartement avec plomberie vieillissante. Nous avons confié la rénovation "
               "complète de la salle de bains et la remise aux normes de la tuyauterie à Brahim. "
               "Professionnel, efficace, respectueux du lieu. Le résultat est excellent. "
               "Je recommande vivement !"),

    # --- Rénovation cuisine ---
    dict(prenom="Philippe B.", lieu="Toulouse", note=5, date="2026-06", cat="cuisine",
         motif="Rénovation complète",
         texte="Rénovation complète de la cuisine : plomberie neuve, carrelage, meubles modernes. "
               "Brahim a géré tout seul du début à la fin. Très professionnel, ponctuel, travail "
               "impeccable. La cuisine est superbe et fonctionnelle. Je recommande à 100 %."),
    dict(prenom="Audrey Leclerc", lieu="Toulouse", note=5, date="2026-05", cat="cuisine",
         motif="Plan de travail &amp; robinetterie",
         texte="Remplacement complet du plan de travail et de la robinetterie. Brahim a bien écouté "
               "nos envies, proposé des matériaux de qualité, et le travail a été fait rapidement "
               "sans gêne. Très satisfaits. Merci pour cette belle cuisine !"),
    dict(prenom="Nicolas A.", lieu="Toulouse", note=5, date="2026-06", cat="cuisine",
         motif="Refonte complète",
         texte="Projet ambitieux : refonte complète de la cuisine. Brahim a su nous proposer les "
               "bonnes solutions, respecter le budget et les délais. Le résultat est à la hauteur de "
               "nos espérances. Artisan vraiment compétent et agréable à travailler avec."),
]

# Mettre à True UNIQUEMENT quand la fiche Google Business Profile existe
# et affiche réellement des avis. Ajoute le lien « Voir les avis Google ».
GOOGLE_AVIS_URL = ""   # ex. "https://g.page/r/XXXXXXXX/review"

# --------------------------------------------------------------------------
# FAITS À CONFIRMER PAR BRAHIM avant affichage.
# Chaque ligne est affichée seulement si elle est renseignée / à True.
# Laisser vide = la mention n'apparaît nulle part sur le site.
# --------------------------------------------------------------------------
NB_CLIENTS = ""          # ex. "120" → affiche « 120+ clients accompagnés ». Vide = masqué.
DELAI_MOYEN = ""         # ex. "48h" → affiche « Intervention sous 48h ». Vide = masqué.
DISPOS_LIMITEES = ""     # ex. "3" → affiche « 3 chantiers de rénovation par mois ». Vide = masqué.
CERTIFICATIONS = []      # ex. ["Quali'eau"] — uniquement des certifications réellement détenues.
MARQUES = []             # ex. ["Grohe", "Villeroy & Boch"] — marques réellement posées.


# ==========================================================================
# MULTILINGUE
# Le français est à la racine, l'anglais dans /en/.
# Les corps de page anglais sont dans content_en.py.
# ==========================================================================
LANGS = ["fr"]

I18N = {
    "fr": {
        "code": "fr", "locale": "fr_FR",
        "nav": [("plomberie.html", "Plomberie"), ("urgence.html", "Urgence"),
                ("renovation-salle-de-bains.html", "Salle de bains"),
                ("renovation-cuisine.html", "Cuisine"), ("contact.html", "Contact")],
        "drawer": [("index.html", "Accueil"), ("plomberie.html", "Plomberie &amp; dépannage"),
                   ("urgence.html", "Urgence 24h/24"),
                   ("renovation-salle-de-bains.html", "Rénovation salle de bains"),
                   ("renovation-cuisine.html", "Rénovation cuisine"),
                   ("zone-intervention.html", "Zone d'intervention"),
                   ("faq.html", "Questions fréquentes"), ("contact.html", "Contact &amp; devis")],
        "urgence_btn": "Urgence", "call": "M'appeler", "menu_open": "Ouvrir le menu",
        "cta_devis": "Devis gratuit",
        "menu_close": "Fermer le menu", "skip": "Aller au contenu",
        "dispo": "Disponible 24h/24, du lundi au samedi · Toulouse",
        "foot_services": "Plomberie", "foot_reno": "Rénovation", "foot_contact": "Contact",
        "foot_intro": ("Plombier à Toulouse : dépannage, recherche de fuite, débouchage et plomberie "
                       "générale. Également rénovation de cuisine et de salle de bains clé en main. "
                       "Artisan indépendant, plus de 7 ans d'expertise."),
        "foot_links_a": [("plomberie.html", "Dépannage &amp; plomberie générale"),
                         ("urgence.html", "Urgence fuite d'eau 24h/24"),
                         ("plomberie.html#prestations", "Recherche de fuite"),
                         ("plomberie.html#prestations", "Débouchage &amp; engorgement"),
                         ("plomberie.html#prestations", "Chauffe-eau")],
        "foot_links_b": [("renovation-salle-de-bains.html", "Salle de bains clé en main"),
                         ("renovation-cuisine.html", "Cuisine clé en main"),
                         ("contact.html", "Contact &amp; devis"),
                         ("zone-intervention.html", "Zone d'intervention"),
                         ("faq.html", "Questions fréquentes")],
        "foot_zone": "Toulouse &amp; agglomération<br>24h/24, du lundi au samedi",
        "foot_legal": ("mentions-legales.html", "Mentions légales", "confidentialite.html",
                       "Confidentialité", "Diagnostic et déplacement gratuits sur Toulouse."),
        "rights": "Tous droits réservés.",
        "by": "Conception et développement du site&nbsp;:",
        "mbar": ("Appeler", "WhatsApp", "Urgence"),
        "urg_title": "Ça fuit&nbsp;?<br>On coupe, on trouve, on répare.",
        "urg_eyebrow": "Mode urgence activé",
        "urg_steps": ["Fermez l'arrivée d'eau générale (robinet sous l'évier ou au compteur).",
                      "Coupez l'électricité si l'eau approche d'une prise ou d'un tableau.",
                      "Appelez-moi. Je vous guide au téléphone en attendant d'arriver."],
        "urg_call": "Appeler le", "urg_wa": "Envoyer une urgence sur WhatsApp",
        "urg_note": "Disponible 24h/24, du lundi au samedi, sur Toulouse et son agglomération.",
        "urg_wa_text": "",
        "wa_text": "",
        "pop_eyebrow": "Diagnostic professionnel gratuit",
        "pop_title": "Laissez votre numéro,<br>je vous rappelle.",
        "pop_lead": ("Deux champs, trente secondes. Le déplacement et le diagnostic sont offerts "
                     "sur Toulouse — vous n'avancez rien."),
        "pop_first": "Prénom", "pop_phone": "Téléphone", "pop_need": "Votre besoin",
        "pop_needs": ["Fuite d'eau / urgence", "Canalisation bouchée", "Chauffe-eau",
                      "Autre dépannage plomberie", "Rénovation salle de bains", "Rénovation cuisine"],
        "pop_rgpd": "J'accepte d'être recontacté par Renauva.",
        "pop_privacy": "Confidentialité", "pop_submit": "Être rappelé",
        "pop_alt": "Ou appelez tout de suite :",
    },
}

LANG = "fr"          # langue en cours de génération
T = I18N["fr"]       # raccourci vers les libellés


def url(slug, lang=None):
    """URL absolue d'une page."""
    return "/" + ("" if slug == "index.html" else slug)

# --------------------------------------------------------------------------
# NAVIGATION (héritée — remplacée par I18N ci-dessus)
# --------------------------------------------------------------------------
NAV = [
    ("plomberie.html", "Plomberie"),
    ("urgence.html", "Urgence"),
    ("renovation-salle-de-bains.html", "Salle de bains"),
    ("renovation-cuisine.html", "Cuisine"),
    ("contact.html", "Contact"),
]
DRAWER = [
    ("index.html", "Accueil"),
    ("plomberie.html", "Plomberie &amp; dépannage"),
    ("urgence.html", "Urgence 24h/24"),
    ("renovation-salle-de-bains.html", "Rénovation salle de bains"),
    ("renovation-cuisine.html", "Rénovation cuisine"),
    ("zone-intervention.html", "Zone d'intervention"),
    ("faq.html", "Questions fréquentes"),
    ("contact.html", "Contact &amp; devis"),
]

LOGO = ('<svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true">'
        '<path d="M20 3c6 6.6 11 12.2 11 18.1A11 11 0 0 1 9 21.1C9 15.2 14 9.6 20 3Z" fill="none" '
        'stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/>'
        '<path d="M15.5 21.6a4.5 4.5 0 0 0 4.5 4.5" fill="none" stroke="currentColor" '
        'stroke-width="2.4" stroke-linecap="round"/></svg>')

IC_PHONE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 2.5 9 7.2l-2 1.6a13.8 13.8 0 0 0 '
            '6.2 6.2l1.6-2 4.7 2.4-1 3.3a2 2 0 0 1-2.2 1.4C9.6 19.2 4.8 14.4 3.1 5.7A2 2 0 0 1 4.5 3.5Z" '
            'fill="currentColor"/></svg>')
IC_WA = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5.1-1.3A10 '
         '10 0 1 0 12 2Z" fill="none" stroke="currentColor" stroke-width="2"/></svg>')
IC_ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

WA_LINK = "https://wa.me/%s" % WA

# --------------------------------------------------------------------------
# SCHEMA.ORG — le bloc entreprise, partagé par toutes les pages
# --------------------------------------------------------------------------
BUSINESS = """{
      "@type": ["Plumber", "HomeAndConstructionBusiness", "LocalBusiness"],
      "@id": "%(site)s/#business",
      "name": "Renauva",
      "alternateName": "Renauva Plomberie Toulouse",
      "description": "Plombier à Toulouse : dépannage, recherche de fuite, débouchage, chauffe-eau et plomberie générale. Également rénovation de cuisine et de salle de bains clé en main. Diagnostic et déplacement gratuits, plus de 7 ans d'expertise, disponible 24h/24 du lundi au samedi.",
      "url": "%(site)s/",
      "telephone": "%(tel)s",
      "email": "%(mail)s",
      "image": "%(site)s/assets/video/hero-poster.jpg",
      "priceRange": "€€",
      "currenciesAccepted": "EUR",
      "founder": { "@type": "Person", "name": "Brahim Touati", "jobTitle": "Plombier" },
      "address": { "@type": "PostalAddress", "addressLocality": "Toulouse", "postalCode": "31000",
                   "addressRegion": "Occitanie", "addressCountry": "FR" },
      "geo": { "@type": "GeoCoordinates", "latitude": 43.604652, "longitude": 1.444209 },
      "areaServed": [
        { "@type": "City", "name": "Toulouse" },
        { "@type": "GeoCircle",
          "geoMidpoint": { "@type": "GeoCoordinates", "latitude": 43.604652, "longitude": 1.444209 },
          "geoRadius": "30000" }
      ],
      "openingHoursSpecification": [{ "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
        "opens": "00:00", "closes": "23:59" }],
      "hasOfferCatalog": {
        "@type": "OfferCatalog", "name": "Prestations Renauva",
        "itemListElement": [
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Dépannage plomberie en urgence", "areaServed": "Toulouse" } },
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Recherche de fuite d'eau", "areaServed": "Toulouse" } },
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Débouchage de canalisation", "areaServed": "Toulouse" } },
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Installation et remplacement de chauffe-eau", "areaServed": "Toulouse" } },
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Rénovation de salle de bains clé en main", "areaServed": "Toulouse" } },
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Rénovation de cuisine clé en main", "areaServed": "Toulouse" } }
        ]
      },
      "knowsLanguage": "fr",
      "slogan": "Diagnostic et déplacement gratuits à Toulouse"
    }""" % {"site": SITE, "tel": TEL, "mail": MAIL}


def breadcrumb(items):
    """items = [(nom, url_relative_ou_None)]"""
    els = []
    for i, (name, url) in enumerate(items, 1):
        el = '{ "@type": "ListItem", "position": %d, "name": "%s"' % (i, name)
        if url:
            el += ', "item": "%s/%s"' % (SITE, url)
        els.append(el + " }")
    return ('{ "@type": "BreadcrumbList", "@id": "#breadcrumb", "itemListElement": [\n      '
            + ",\n      ".join(els) + "\n    ] }")


def faq_schema(qa):
    els = []
    for q, a in qa:
        a_txt = re.sub(r"<[^>]+>", "", a).replace(" ", " ")
        a_txt = re.sub(r"\s+", " ", a_txt).strip().replace('"', "'")
        els.append('{ "@type": "Question", "name": "%s",\n        "acceptedAnswer": '
                   '{ "@type": "Answer", "text": "%s" } }' % (q.replace('"', "'"), a_txt))
    return '{ "@type": "FAQPage", "@id": "#faq", "mainEntity": [\n      ' + ",\n      ".join(els) + "\n    ] }"


def faq_html(qa, eyebrow="Questions fréquentes", title=None):
    items = "".join(
        '<details class="faq__i reveal"><summary>%s</summary><div>%s</div></details>' % (q, a)
        for q, a in qa)
    t = title or 'Ce qu\'on nous<br><span class="accent">demande le plus.</span>'
    return """
<section class="sec faq" id="faq">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal">%s</p>
      <h2 class="sec__title reveal">%s</h2>
    </header>
    <div class="faq__list">%s</div>
  </div>
</section>""" % (eyebrow, t, items)


CTA_FINAL = """
<section class="cta">
  <div class="wrap cta__in">
    <h2 class="reveal">Un problème d'eau ne s'arrange<br>jamais tout seul.</h2>
    <p class="reveal">Diagnostic gratuit, déplacement offert, devis clair. Vous ne risquez rien à décrocher.</p>
    <div class="cta__acts reveal">
      <a class="btn btn--light btn--lg" href="contact.html#rappel">Demander un diagnostic gratuit</a>
      <a class="btn btn--outline btn--lg" href="tel:__TEL__">__TELH__</a>
    </div>
  </div>
</section>"""

# Bandeau CTA réutilisable, inséré au milieu de l'accueil.
# `href` pointe vers le formulaire de la page contact (scroll direct via #rappel).
def cta_band(titre, sous, bouton):
    return ("""
<section class="ctaband">
  <div class="wrap ctaband__in reveal">
    <div>
      <h2 class="ctaband__t">%s</h2>
      <p class="ctaband__p">%s</p>
    </div>
    <a class="btn btn--blue btn--lg" href="contact.html#rappel">%s</a>
  </div>
</section>""" % (titre, sous, bouton))

def stars(n):
    full = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 3 6.9 7.5.7-5.6 5 1.6 7.4L12 18.3'
            ' 5.5 22l1.6-7.4-5.6-5 7.5-.7Z" fill="currentColor"/></svg>')
    return '<span class="stars" aria-label="%d étoiles sur 5">%s</span>' % (n, full * n)



def demande_avis():
    """Invite les clients à laisser un vrai avis. N'apparaît que si la fiche
    Google Business Profile existe (GOOGLE_AVIS_URL renseigné)."""
    if not GOOGLE_AVIS_URL:
        return ""
    return """
<section class="sec alt">
  <div class="wrap cta__in">
    <p class="eyebrow reveal" style="justify-content:center"><span class="idx">→</span> Vous êtes déjà client&nbsp;?</p>
    <h2 class="sec__title reveal">Votre avis aide<br><span class="accent">le prochain client.</span></h2>
    <p class="sec__lead reveal" style="margin-inline:auto">Deux minutes suffisent, et ça change
      tout pour un artisan indépendant.</p>
    <p class="reveal" style="margin-top:26px">
      <a class="btn btn--blue btn--lg" href="%s" target="_blank" rel="noopener">Laisser un avis Google</a></p>
  </div>
</section>""" % GOOGLE_AVIS_URL


MOIS_FR = {"01": "Janvier", "02": "Février", "03": "Mars", "04": "Avril", "05": "Mai",
           "06": "Juin", "07": "Juillet", "08": "Août", "09": "Septembre", "10": "Octobre",
           "11": "Novembre", "12": "Décembre"}


def date_lisible(d):
    """2026-06 -> « Juin 2026 ». Une date absolue ne périme pas, contrairement
    à « il y a 2 semaines » qui devient faux au bout d'un mois."""
    an, mois = d.split("-")
    return "%s %s" % (MOIS_FR.get(mois, mois), an)


def avis_section(cats=None, eyebrow=None, titre=None, limite=None, carrousel=False):
    """Section « avis ». Ne rend rien tant qu'aucun avis n'est saisi.
    `cats` filtre par type de chantier pour n'afficher que les avis pertinents
    sur chaque page."""
    lot = [a for a in AVIS if not cats or a.get("cat") in cats]
    if limite:
        lot = lot[:limite]
    if not lot:
        return demande_avis()

    eyebrow = eyebrow or "Avis clients"
    titre = titre or 'Ce qu\'en disent<br><span class="accent">les Toulousains.</span>'

    def carte(a):
        return """
      <figure class="avis__c reveal">
        %s
        <blockquote>%s</blockquote>
        <figcaption><b>%s</b><span>%s · %s</span><em>%s</em></figcaption>
      </figure>""" % (stars(a["note"]), a["texte"], a["prenom"], a["lieu"],
                      date_lisible(a["date"]), a["motif"])

    items = "".join(carte(a) for a in lot)
    if carrousel:
        # piste dupliquée : la boucle se referme sans saut visible
        items += "".join(carte(a) for a in lot)

    google = ('<p class="reveal" style="margin-top:32px;text-align:center">'
              '<a class="link-arrow" href="%s" target="_blank" rel="noopener">Voir tous les avis sur Google __ARROW__</a></p>'
              % GOOGLE_AVIS_URL) if GOOGLE_AVIS_URL else ""

    duree = max(28, len(lot) * 7)
    return """
<section class="sec avis%s" id="avis"%s>
  <div class="wrap">
    <header class="sec__head sec__head--center">
      <p class="eyebrow reveal"><span class="idx">→</span> %s</p>
      <h2 class="sec__title reveal">%s</h2>
    </header>
    <div class="avis__grid">%s</div>
    %s
  </div>
</section>""" % (" avis--carrousel" if carrousel else "",
                 ' style="--avis-duree:%ds"' % (duree * 2) if carrousel else "",
                 eyebrow, titre, items, google)


def avis_schema():
    """Balisage Review — uniquement si de vrais avis existent."""
    if not AVIS:
        return ""
    els = []
    for a in AVIS:
        els.append("""{ "@type": "Review", "itemReviewed": { "@id": "%s/#business" },
      "author": { "@type": "Person", "name": "%s" },
      "datePublished": "%s",
      "reviewRating": { "@type": "Rating", "ratingValue": %d, "bestRating": 5 },
      "reviewBody": "%s" }""" % (SITE, a["prenom"], a["date"], a["note"],
                                 a["texte"].replace('"', "'")))
    moy = sum(a["note"] for a in AVIS) / float(len(AVIS))
    els.append("""{ "@type": "AggregateRating", "itemReviewed": { "@id": "%s/#business" },
      "ratingValue": "%.1f", "reviewCount": %d, "bestRating": 5 }"""
               % (SITE, moy, len(AVIS)))
    return ",\n    ".join(els)


def credibilite():
    """Bandeau de réassurance. Chaque élément n'apparaît que s'il est vrai."""
    items = ['<li><b>Basé à Toulouse</b><span>Artisan local, pas une plateforme</span></li>',
             '<li><b>Plus de 7 ans d\'expertise</b><span>Plomberie et rénovation</span></li>',
             '<li><b>Diagnostic professionnel gratuit</b><span>Déplacement offert</span></li>']
    if DELAI_MOYEN:
        items.append('<li><b>Intervention sous %s</b><span>Délai moyen constaté</span></li>' % DELAI_MOYEN)
    if NB_CLIENTS:
        items.append('<li><b>%s+ clients accompagnés</b><span>Sur Toulouse et l\'agglomération</span></li>' % NB_CLIENTS)
    if CERTIFICATIONS:
        items.append('<li><b>%s</b><span>Certification détenue</span></li>' % " · ".join(CERTIFICATIONS))
    if MARQUES:
        items.append('<li><b>%s</b><span>Marques posées</span></li>' % " · ".join(MARQUES))
    if DISPOS_LIMITEES:
        items.append('<li><b>%s chantiers par mois</b><span>Agenda volontairement limité</span></li>' % DISPOS_LIMITEES)
    return '<section class="credib"><div class="wrap"><ul class="credib__list">%s</ul></div></section>' % "".join(items)



# --------------------------------------------------------------------------
# RÉSEAU — animation pilotée par le scroll
# Aucune dépendance : SVG + un peu de JavaScript natif. Le tracé se dessine
# et l'eau progresse dans le tuyau au fur et à mesure que la page défile.
# Réglages dans assets/js/app.js, section « RÉSEAU ».
# --------------------------------------------------------------------------
RESEAU = """
<section class="pipes" id="reseau" aria-labelledby="pipesTitle">
  <div class="pipes__rail">
    <div class="pipes__sticky">
      <div class="wrap pipes__in">

        <div class="pipes__head">
          <p class="eyebrow"><span class="idx">&rarr;</span> Le réseau, de la vanne au robinet</p>
          <h2 class="sec__title" id="pipesTitle">Ce qui se passe<br><span class="accent">dans vos murs.</span></h2>
          <p class="pipes__lead">Une installation qui fonctionne, c'est un parcours continu&nbsp;:
            arrivée, distribution, évacuation. Quand un seul point cède, c'est toute la ligne
            qui se manifeste — souvent là où vous ne l'attendiez pas.</p>

          <ol class="pipes__steps">
            <li data-at="0"><b>Arrivée fermée</b><span>Vanne générale, compteur, réducteur de pression.</span></li>
            <li data-at="1"><b>Mise en pression</b><span>Le réseau se remplit, les points faibles se révèlent.</span></li>
            <li data-at="2"><b>Distribution</b><span>Cuivre, PER ou multicouche jusqu'à chaque point d'eau.</span></li>
            <li data-at="3"><b>Débit rétabli</b><span>Pression stable, écoulement franc, aucune reprise à prévoir.</span></li>
          </ol>

          <p class="pipes__cta">
            <a class="btn btn--blue btn--lg" href="tel:__TEL__">__ICPH__ Faire vérifier mon installation</a>
          </p>
        </div>

        <div class="pipes__viz" aria-hidden="true">
          <svg viewBox="0 0 1100 600" preserveAspectRatio="xMidYMid meet" id="pipesSvg">
            <defs>
              <linearGradient id="pipeWater" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="#0B5FA5"/>
                <stop offset="55%" stop-color="#3AA0F5"/>
                <stop offset="100%" stop-color="#8FCBFF"/>
              </linearGradient>
              <filter id="pipeGlow" x="-30%" y="-30%" width="160%" height="160%">
                <feGaussianBlur stdDeviation="7" result="b"/>
                <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
              </filter>
            </defs>

            <g class="pipes__grid">
              <path d="M0 150 H1100 M0 300 H1100 M0 450 H1100" />
              <path d="M275 0 V600 M550 0 V600 M825 0 V600" />
            </g>

            <path class="pipes__shell" d="__TRACE__"/>
            <path class="pipes__draw"  d="__TRACE__" id="pipesDraw"/>
            <path class="pipes__flow"  d="__TRACE__" id="pipesFlow"/>

            <g id="pipesNodes" class="pipes__nodes">
              <circle cx="214" cy="254" r="9"/>
              <circle cx="516" cy="150" r="9"/>
              <circle cx="516" cy="452" r="9"/>
              <circle cx="826" cy="208" r="9"/>
            </g>

            <g class="pipes__valve" id="pipesValve">
              <circle cx="40" cy="300" r="21"/>
              <path d="M40 288 V312 M28 300 H52"/>
            </g>

            <g class="pipes__out" id="pipesOut">
              <path d="M1056 300 v34" />
              <circle class="drop" cx="1056" cy="362" r="6"/>
              <circle class="drop drop--2" cx="1056" cy="362" r="5"/>
            </g>
          </svg>

          <div class="pipes__gauge">
            <span class="pipes__gaugeBar"><i id="pipesGauge"></i></span>
            <b id="pipesPct">0&nbsp;%</b>
          </div>
        </div>

      </div>
    </div>
  </div>
</section>""".replace("__TRACE__", "M 40 300 H 168 C 196 300 214 282 214 254 V 150 C 214 122 232 104 260 104 H 470 C 498 104 516 122 516 150 V 452 C 516 480 534 498 562 498 H 780 C 808 498 826 480 826 452 V 208 C 826 180 844 162 872 162 H 1010 C 1038 162 1056 180 1056 208 V 300")


PROCESS = """
<section class="sec proc" id="processus">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal"><span class="idx">→</span> Comment ça se passe</p>
      <h2 class="sec__title reveal">Quatre étapes.<br><span class="accent">Aucune mauvaise surprise.</span></h2>
    </header>
    <ol class="proc__list">
      <li class="proc__i reveal"><span class="proc__n">1</span><h3>Vous appelez</h3>
        <p>Ou vous m'envoyez votre demande en 30 secondes par WhatsApp. Je rappelle vite : en plomberie,
          celui qui rappelle en premier est celui qui règle le problème.</p></li>
      <li class="proc__i reveal"><span class="proc__n">2</span><h3>Diagnostic gratuit sur place</h3>
        <p>Je me déplace chez vous, à Toulouse. J'ouvre, je teste, je localise. Vous ne payez ni le
          déplacement, ni le diagnostic.</p></li>
      <li class="proc__i reveal"><span class="proc__n">3</span><h3>Devis clair</h3>
        <p>Poste par poste, matériaux compris. Vous savez ce que vous payez et pourquoi, avant que
          le premier outil ne sorte.</p></li>
      <li class="proc__i reveal"><span class="proc__n">4</span><h3>Réparation rapide</h3>
        <p>Chantier tenu, pièce rendue propre. Plus d'odeurs, plus de problème d'évacuation.
          Le résultat, et vite.</p></li>
    </ol>
  </div>
</section>"""

TRUST = """
<section class="sec why" id="pourquoi">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal"><span class="idx">→</span> Pourquoi Renauva</p>
      <h2 class="sec__title reveal">Six raisons de<br><span class="accent">décrocher le téléphone.</span></h2>
    </header>
    <div class="why__grid">
      <article class="why__c why__c--hero reveal"><span class="why__n">01</span>
        <h3>Diagnostic professionnel <span class="accent">gratuit</span></h3>
        <p>Je me déplace chez vous, j'ouvre, je cherche, je comprends le problème et je vous dis ce qu'il
          faut faire. Sans engagement, sans facture surprise pour « être venu voir ».</p>
        <div class="why__glow" aria-hidden="true"></div></article>
      <article class="why__c reveal"><span class="why__n">02</span><h3>Déplacement offert</h3>
        <p>Zéro frais de déplacement sur Toulouse et son agglomération. Le devis commence à 0&nbsp;€.</p></article>
      <article class="why__c reveal"><span class="why__n">03</span><h3>Plus de 7 ans d'expertise</h3>
        <p>Plus de sept ans de dépannages, de fuites trouvées là où personne ne regardait, de chantiers
          livrés propres.</p></article>
      <article class="why__c reveal"><span class="why__n">04</span><h3>Rapide et efficace, 24h/24</h3>
        <p>Du lundi au samedi, une fuite n'attend pas l'ouverture des bureaux. Vous appelez, ça sonne,
          et ça se règle aujourd'hui plutôt que la semaine prochaine.</p></article>
      <article class="why__c reveal"><span class="why__n">05</span><h3>Un artisan, pas un standard</h3>
        <p>Vous m'avez au téléphone, et c'est moi qui viens. Aucun intermédiaire, aucun sous-traitant
          différent à chaque étape.</p></article>
    </div>
  </div>
</section>"""

ARTISAN = """
<section class="sec artisan" id="artisan">
  <div class="wrap artisan__in">
    <div class="artisan__photo reveal">
      <img src="assets/img/brahim.webp" alt="Brahim Touati, plombier à Toulouse, fondateur de Renauva"
           loading="lazy" width="800" height="1200">
    </div>
    <div class="artisan__txt">
      <p class="eyebrow reveal"><span class="idx">→</span> L'artisan</p>
      <h2 class="sec__title reveal">Brahim Touati.<br><span class="accent">Artisan plombier à Toulouse.</span></h2>
      <p class="reveal">Plombier-rénovateur indépendant basé à Toulouse, je mets plus de sept ans
        d'expertise au service de vos projets&nbsp;: plomberie, mais aussi rénovation complète
        de salle de bains et de cuisine.</p>
      <p class="reveal">Je travaille seul et j'interviens personnellement sur chacun de mes chantiers.
        Pas de sous-traitance, pas d'intermédiaire — vous me parlez directement, du premier appel
        à la fin des travaux.</p>
      <blockquote class="reveal">« J'annonce un prix ferme et un planning, et je m'y tiens.
        Pas de surprise en cours de route. »<cite>Brahim Touati, fondateur de Renauva</cite></blockquote>
      <div class="artisan__acts reveal">
        <a class="btn btn--blue" href="tel:__TEL__">__TELH__</a>
        <a class="btn btn--ghost" href="contact.html">Décrire mon problème</a>
      </div>
    </div>
  </div>
</section>

<section class="sec methode" id="methode">
  <div class="wrap">
    <header class="sec__head sec__head--center">
      <p class="eyebrow reveal"><span class="idx">→</span> Comment je travaille</p>
      <h2 class="sec__title reveal">Simple<br><span class="accent">et rigoureux.</span></h2>
    </header>
    <ol class="methode__grid">
      <li class="methode__c reveal"><span class="methode__n">01</span>
        <h3>Le constat d'abord</h3>
        <p>Je viens voir votre situation sans engagement. Je vous explique clairement ce que je
          constate, ce qui peut être fait, et pour quel résultat. Aucun frais.</p></li>
      <li class="methode__c reveal"><span class="methode__n">02</span>
        <h3>Transparence absolue</h3>
        <p>Avant de commencer, nous convenons ensemble du prix, du planning et du résultat attendu.
          Pas de surprise en cours de route.</p></li>
      <li class="methode__c reveal"><span class="methode__n">03</span>
        <h3>Un seul interlocuteur</h3>
        <p>C'est moi du début à la fin. Vous me posez vos questions, vous suivez l'avancement avec moi,
          vous m'appelez si besoin. Pas de tiers, pas de complications.</p></li>
      <li class="methode__c reveal"><span class="methode__n">04</span>
        <h3>Respect des délais</h3>
        <p>J'annonce un planning, je le tiens. Votre temps compte.</p></li>
    </ol>
    <p class="methode__sign reveal">Brahim Touati, artisan plombier à Toulouse</p>
  </div>
</section>"""

ZONE_LIST = ["Toulouse Centre", "Capitole", "Saint-Cyprien", "Les Carmes", "Compans", "Rangueil",
             "Côte Pavée", "Purpan", "Saint-Michel", "Minimes", "Croix-Daurade", "Lardenne",
             "Jean Jaurès", "Busca", "Blagnac", "Colomiers", "Tournefeuille", "Balma", "L'Union",
             "Ramonville", "Saint-Orens", "Cugnaux", "Portet-sur-Garonne", "Muret",
             "Plaisance-du-Touch", "Castanet-Tolosan", "Aucamville", "Fenouillet", "Launaguet",
             "Quint-Fonsegrives"]

ZONE_MAP = """<div class="zone__map">
        <svg viewBox="0 0 500 500" aria-hidden="true">
          <defs><radialGradient id="zg" cx="50%" cy="50%">
            <stop offset="0%" stop-color="#2E9BF0" stop-opacity=".38"/>
            <stop offset="70%" stop-color="#0B5FA5" stop-opacity=".10"/>
            <stop offset="100%" stop-color="#0B5FA5" stop-opacity="0"/></radialGradient></defs>
          <circle cx="250" cy="250" r="230" fill="url(#zg)"/>
          <circle class="zring" cx="250" cy="250" r="120" fill="none" stroke="#2E9BF0" stroke-opacity=".35" stroke-dasharray="3 7"/>
          <circle class="zring" cx="250" cy="250" r="180" fill="none" stroke="#2E9BF0" stroke-opacity=".25" stroke-dasharray="3 7"/>
          <circle class="zring" cx="250" cy="250" r="235" fill="none" stroke="#2E9BF0" stroke-opacity=".16" stroke-dasharray="3 7"/>
          <g><circle cx="250" cy="250" r="9" fill="#2E9BF0"/>
             <circle class="zpulse" cx="250" cy="250" r="9" fill="none" stroke="#2E9BF0" stroke-width="2"/></g>
        </svg>
        <span class="zone__core">Toulouse</span>
      </div>"""

ZONE_TEASER = """
<section class="sec zone zone--slim" id="zone">
  <div class="wrap">
    <div class="zone__wrap reveal">
      __MAP__
      <div class="zone__side">
        <p class="eyebrow"><span class="idx">→</span> Zone d'intervention</p>
        <h2>Toulouse <span class="accent">et toute l'agglomération.</span></h2>
        <p class="zone__lead">Déplacement gratuit dans un rayon d'environ 30&nbsp;km.
          Votre commune n'est pas listée&nbsp;? Appelez, elle y est sûrement.</p>
        <ul class="zone__list">__LIST__</ul>
        <p style="margin-top:18px"><a class="link-arrow" href="zone-intervention.html">Voir toute la zone __ARROW__</a></p>
      </div>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# SHELL
# --------------------------------------------------------------------------
def nav_html(active, slug_fr):
    """Barre de navigation + tiroir mobile."""
    t = I18N[LANG]
    links = "".join('<a href="%s"%s>%s</a>' % (u, ' class="is-on"' if u == active else "", lbl)
                    for u, lbl in t["nav"])
    drawer = "".join('<a href="%s"><span class="idx">%02d</span> %s</a>' % (u, i, lbl)
                     for i, (u, lbl) in enumerate(t["drawer"], 1))
    return """
<header class="nav" id="nav">
  <div class="nav__in">
    <a class="brand" href="%(home)s" aria-label="Renauva">%(logo)s<span class="brand__text">Renauva<em>.</em></span></a>
    <nav class="nav__links" aria-label="Navigation">%(links)s</nav>
    <div class="nav__cta">
      <button class="btn-urgence" data-urgence aria-haspopup="dialog"><span class="pulse"></span> %(urg)s</button>
      <a class="btn btn--sm btn--ghost nav__phone" href="tel:%(tel)s">%(icph)s<span>%(telh)s</span></a>
      <a class="btn btn--sm btn--blue nav__devis" href="contact.html#rappel">%(devis)s</a>
      <button class="burger" id="burger" aria-label="%(open)s" aria-expanded="false"><i></i><i></i></button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer" aria-hidden="true">
  <nav class="drawer__nav">%(drawer)s</nav>
  <div class="drawer__foot">
    <a class="btn btn--blue btn--full" href="contact.html#rappel">%(devis)s</a>
    <a class="btn btn--ghost btn--full" href="tel:%(tel)s">%(call)s</a>
    <a class="btn btn--ghost btn--full" href="%(wa)s" target="_blank" rel="noopener">WhatsApp</a>
    <p>%(dispo)s</p>
  </div>
</div>""" % {"logo": LOGO, "links": links, "drawer": drawer, "tel": TEL, "telh": TEL_H,
             "icph": IC_PHONE, "wa": "https://wa.me/%s" % WA,
             "home": url("index.html"), "urg": t["urgence_btn"], "call": t["call"],
             "open": t["menu_open"], "dispo": t["dispo"],
             "devis": t["cta_devis"]}


def footer_html():
    t = I18N[LANG]
    la = "".join('<a href="%s">%s</a>' % (u, l) for u, l in t["foot_links_a"])
    lb = "".join('<a href="%s">%s</a>' % (u, l) for u, l in t["foot_links_b"])
    ml, mlbl, cf, cflbl, note = t["foot_legal"]
    return """
<footer class="foot">
  <div class="wrap foot__in">
    <div class="foot__brand">
      <a class="brand" href="%(home)s">%(logo)s<span class="brand__text">Renauva<em>.</em></span></a>
      <p>%(intro)s</p>
    </div>
    <div class="foot__col"><h4>%(h1)s</h4>%(la)s</div>
    <div class="foot__col"><h4>%(h2)s</h4>%(lb)s</div>
    <div class="foot__col foot__col--contact"><h4>%(h3)s</h4>
      <a class="foot__big" href="tel:%(tel)s">%(telh)s</a>
      <a href="mailto:%(mail)s">%(mail)s</a>
      <a href="%(wa)s" target="_blank" rel="noopener">WhatsApp</a>
      <p>%(zone)s</p>
    </div>
  </div>
  <div class="wrap foot__bot">
    <p>© <span id="year">%(year)s</span> Renauva — Brahim Touati. %(rights)s</p>
    <p><a href="%(ml)s">%(mlbl)s</a> · <a href="%(cf)s">%(cflbl)s</a> · %(note)s</p>
    <p class="foot__by">%(by)s <a href="https://renauva.pages.dev" rel="author">Quentin Joubert</a></p>
  </div>
</footer>

<div class="mbar" id="mbar">
  <a class="mbar__b mbar__b--call" href="tel:%(tel)s">%(icph)s%(m1)s</a>
  <a class="mbar__b mbar__b--wa" href="%(wa)s" target="_blank" rel="noopener">%(icwa)s%(m2)s</a>
  <button class="mbar__b mbar__b--urg" data-urgence><span class="pulse"></span>%(m3)s</button>
</div>

<div class="urg" id="urg" role="dialog" aria-modal="true" aria-labelledby="urgTitle" aria-hidden="true">
  <div class="urg__bg"></div>
  <div class="urg__panel">
    <button class="urg__close" id="urgClose" aria-label="%(close)s">✕</button>
    <p class="urg__eyebrow"><span class="pulse"></span> %(ueye)s</p>
    <h2 id="urgTitle">%(utitle)s</h2>
    <ol class="urg__steps">%(usteps)s</ol>
    <a class="btn btn--red btn--lg btn--full" href="tel:%(tel)s">%(ucall)s %(telh)s</a>
    <a class="btn btn--ghost btn--full" href="https://wa.me/%(wanum)s?text=%(uwatext)s"
       target="_blank" rel="noopener">%(uwa)s</a>
    <p class="urg__note">%(unote)s</p>
  </div>
</div>

<div class="pop" id="pop" role="dialog" aria-modal="true" aria-labelledby="popTitle" aria-hidden="true">
  <div class="pop__bg" data-pop-close></div>
  <div class="pop__panel">
    <button class="pop__close" data-pop-close aria-label="%(close)s">✕</button>
    <p class="pop__eyebrow">%(peye)s</p>
    <h2 id="popTitle">%(ptitle)s</h2>
    <p class="pop__lead">%(plead)s</p>
    <form id="popForm" action="https://api.web3forms.com/submit" method="POST">
      <input type="hidden" name="access_key" value="VOTRE_CLE_WEB3FORMS">
      <input type="hidden" name="subject" value="Rappel demandé — pop-up site Renauva">
      <input type="hidden" name="from_name" value="Site Renauva (pop-up)">
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
      <div class="pop__row">
        <label class="f"><span>%(pfirst)s</span>
          <input type="text" name="nom" required autocomplete="given-name" placeholder="Marie"></label>
        <label class="f"><span>%(pphone)s</span>
          <input type="tel" name="telephone" required autocomplete="tel" inputmode="tel" placeholder="06 12 34 56 78"></label>
      </div>
      <label class="f"><span>%(pneed)s</span>
        <select name="projet" id="popProjet">%(pneeds)s</select></label>
      <label class="f f--check"><input type="checkbox" name="consentement" value="Oui" required>
        <span>%(prgpd)s <a href="%(cf)s">%(pprivacy)s</a>.</span></label>
      <button type="submit" class="btn btn--blue btn--lg btn--full" id="popSubmit">%(psubmit)s</button>
      <p class="f__note" id="popNote" role="status"></p>
    </form>
    <p class="pop__alt">%(palt)s <a href="tel:%(tel)s">%(telh)s</a></p>
  </div>
</div>""" % {
        "logo": LOGO, "home": url("index.html"), "intro": t["foot_intro"],
        "h1": t["foot_services"], "h2": t["foot_reno"], "h3": t["foot_contact"],
        "la": la, "lb": lb, "tel": TEL, "telh": TEL_H, "mail": MAIL,
        "wa": "https://wa.me/%s?text=%s" % (WA, t["wa_text"]), "wanum": WA,
        "zone": t["foot_zone"], "year": datetime.date.today().year, "rights": t["rights"],
        "ml": ml, "mlbl": mlbl, "cf": cf, "cflbl": cflbl, "note": note,
        "by": t["by"],
        "icph": IC_PHONE, "icwa": IC_WA,
        "m1": t["mbar"][0], "m2": t["mbar"][1], "m3": t["mbar"][2],
        "close": t["menu_close"],
        "ueye": t["urg_eyebrow"], "utitle": t["urg_title"],
        "usteps": "".join("<li><b>%d.</b> %s</li>" % (i, x) for i, x in enumerate(t["urg_steps"], 1)),
        "ucall": t["urg_call"], "uwa": t["urg_wa"], "unote": t["urg_note"],
        "uwatext": t["urg_wa_text"],
        "peye": t["pop_eyebrow"], "ptitle": t["pop_title"], "plead": t["pop_lead"],
        "pfirst": t["pop_first"], "pphone": t["pop_phone"], "pneed": t["pop_need"],
        "pneeds": "".join("<option>%s</option>" % x for x in t["pop_needs"]),
        "prgpd": t["pop_rgpd"], "pprivacy": t["pop_privacy"], "psubmit": t["pop_submit"],
        "palt": t["pop_alt"],
    }


SHELL = """<!DOCTYPE html>
<html lang="__LANGCODE__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta name="theme-color" content="#07090D">
<meta name="robots" content="__ROBOTS__">
<meta name="geo.region" content="FR-31"><meta name="geo.placename" content="Toulouse">
<link rel="canonical" href="__CANON__">
__ALT__

<meta property="og:type" content="website">
<meta property="og:locale" content="__LOCALE__">
<meta property="og:site_name" content="Renauva">
<meta property="og:url" content="__CANON__">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:image" content="__SITE__/assets/video/hero-poster.jpg">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
__PRELOAD__
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=__V__">

<script type="application/ld+json">
{ "@context": "https://schema.org", "@graph": [
    __BUSINESS__,
    { "@type": "WebSite", "@id": "__SITE__/#website", "url": "__SITE__/", "name": "Renauva",
      "inLanguage": "fr-FR", "publisher": { "@id": "__SITE__/#business" } }__SCHEMA__
] }
</script>
</head>
<body>

<div class="loader" id="loader" aria-hidden="true">
  <div class="loader__inner">
    <div class="loader__mark"><span>R</span></div>
    <div class="loader__word"><span>R</span><span>E</span><span>N</span><span>A</span><span>U</span><span>V</span><span>A</span></div>
    <div class="loader__bar"><i></i></div>
  </div>
</div>

<a class="skip" href="#main">Aller au contenu</a>
<div class="progress" id="progress" aria-hidden="true"></div>
__NAV__
<main id="main">
__BODY__
</main>
__FOOTER__
<script src="assets/js/app.js?v=__V__" defer></script>
</body>
</html>
"""


def render(slug, title, desc, body, schema="", robots="index, follow, max-image-preview:large",
           preload="", active=None):
    t = I18N[LANG]
    canon = SITE + url(slug)
    alt = ""

    extra = ",\n    " + schema if schema else ""
    html = (SHELL
            .replace("__TITLE__", title)
            .replace("__DESC__", desc)
            .replace("__ROBOTS__", robots)
            .replace("__CANON__", canon)
            .replace("__ALT__", alt)
            .replace("__LANGCODE__", t["code"])
            .replace("__LOCALE__", t["locale"])
            .replace("__PRELOAD__", preload)
            .replace("__BUSINESS__", BUSINESS)
            .replace("__SCHEMA__", extra)
            .replace("__NAV__", nav_html(active or slug, slug))
            .replace("__BODY__", body)
            .replace("__FOOTER__", footer_html())
            .replace("__SITE__", SITE)
            .replace("__V__", V))

    # srcset automatique : on ne sert jamais du 1600 px a un telephone.
    # Le slider avant/apres est exclu, son src est reecrit en JS.
    def _srcset(m):
        tag, sl = m.group(0), m.group(1)
        if "srcset" in tag or "ba__" in tag:
            return tag
        if not os.path.exists(os.path.join(ROOT, "assets", "img", sl + "-sm.webp")):
            return tag
        sizes = "100vw" if "phero__media" in tag else "(max-width:820px) 100vw, 50vw"
        return tag.replace('src="assets/img/%s.webp"' % sl,
                           'src="assets/img/%s.webp" srcset="assets/img/%s-sm.webp 800w, '
                           'assets/img/%s.webp 1600w" sizes="%s" decoding="async"' % (sl, sl, sl, sizes))
    html = re.sub(r'<img[^>]*src="assets/img/([a-z0-9\-]+)\.webp"[^>]*>', _srcset, html)

    # liens internes relatifs → absolus
    html = re.sub(r'href="([a-z0-9\-]+\.html)', lambda m: 'href="/' + m.group(1), html)

    # chemins d'assets en absolu
    html = html.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    html = html.replace('srcset="assets/', 'srcset="/assets/').replace(', assets/', ', /assets/')
    html = html.replace('data-before="assets/', 'data-before="/assets/')
    html = html.replace('data-after="assets/', 'data-after="/assets/')

    html = (html.replace("__TELH__", TEL_H).replace("__TEL__", TEL)
                .replace("__WA__", "https://wa.me/%s?text=%s" % (WA, t["wa_text"]))
                .replace("__ARROW__", IC_ARROW)
                .replace("__ICPH__", IC_PHONE).replace("__ICWA__", IC_WA))

    chemin = os.path.join(ROOT, slug)
    dossier = os.path.dirname(chemin)
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(html)
    return slug


def phero(eyebrow, h1, lead, img, alt, tone=""):
    """Bandeau de tête des pages intérieures."""
    return """
<section class="phero %s">
  <div class="phero__media"><img src="assets/img/%s" alt="%s" width="1600" height="1067" fetchpriority="high"></div>
  <div class="wrap phero__in">
    <p class="kicker reveal"><span class="dot"></span> %s</p>
    <h1 class="phero__title">%s</h1>
    <p class="phero__lead reveal">%s</p>
    <div class="phero__acts reveal">
      <a class="btn btn--blue btn--lg" href="tel:__TEL__">__ICPH__ Appeler maintenant</a>
      <a class="btn btn--glass btn--lg" href="contact.html">Demander un diagnostic gratuit</a>
    </div>
    <ul class="phero__proof reveal">
      <li>Diagnostic professionnel gratuit</li><li>Déplacement offert</li><li>Rapide et efficace</li><li>Plus de 7 ans d'expertise</li>
    </ul>
  </div>
</section>""" % (tone, img, alt, eyebrow, h1, lead)


def cards(items, cls="grid3"):
    out = []
    for it in items:
        n = it.get("n", "")
        link = it.get("link")
        inner = ('<span class="pcard__n">%s</span><h3>%s</h3><p>%s</p>' % (n, it["t"], it["d"]))
        if link:
            inner += '<span class="pcard__go">%s %s</span>' % (it.get("cta", "En savoir plus"), IC_ARROW)
            out.append('<a class="pcard reveal" href="%s">%s</a>' % (link, inner))
        else:
            out.append('<div class="pcard reveal">%s</div>' % inner)
    return '<div class="%s">%s</div>' % (cls, "".join(out))


# ==========================================================================
# PAGES
# ==========================================================================

HOME_HERO = """
<section class="hero" id="hero">
  <div class="hero__media">
    <video class="hero__video" id="heroVideo" autoplay muted loop playsinline preload="none"
           poster="assets/video/hero-poster.webp" aria-hidden="true" tabindex="-1"></video>
    <div class="hero__grade"></div>
    <div class="hero__grid" aria-hidden="true"></div>
  </div>
  <div class="hero__in">
    <p class="kicker reveal" data-d="0"><span class="dot"></span> Artisan à Toulouse · rapide et efficace</p>
    <h1 class="hero__title">
      <span class="line"><span>Rénovation cuisine</span></span>
      <span class="line"><span>&amp; salle de bains</span></span>
      <span class="line"><span class="accent">+ plomberie complète.</span></span>
    </h1>
    <p class="hero__sub reveal" data-d="120">
      À Toulouse, je prends les gros chantiers <strong>clé en main</strong> — cuisine, salle de bains,
      du démontage au dernier joint — et <strong>toute la plomberie</strong> : fuite, canalisation bouchée,
      chauffe-eau, robinetterie. <strong>Dépannage urgence 24h/24</strong>, du lundi au samedi.
    </p>
    <div class="hero__free reveal" data-d="200">
      <div class="free__duo">
        <p class="free__item"><span class="free__tick"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 13 4.5 4.5L19 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          <span>Diagnostic</span> <b>gratuit</b></p>
        <p class="free__item"><span class="free__tick"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 13 4.5 4.5L19 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          <span>Déplacement</span> <b>offert</b></p>
      </div>
      <p class="free__note">Il vient, il cherche, il trouve, il chiffre.
        <strong>Vous ne payez rien pour ça.</strong></p>
    </div>
    <div class="hero__actions reveal" data-d="280">
      <a class="btn btn--blue btn--lg" href="contact.html#rappel">Demander un diagnostic gratuit</a>
      <a class="btn btn--ghost btn--lg" href="tel:__TEL__">__ICPH__ Appeler maintenant</a>
      <button class="btn btn--red btn--lg" data-urgence><span class="pulse"></span> J'ai une urgence</button>
    </div>
    <button class="hero__cue" data-scroll="#services" aria-label="Défiler vers les services"><span></span> Découvrir</button>
  </div>
  <div class="hero__stats">
    <div><b data-count="7" data-suffix="+">0</b><i>ans d'expertise</i></div>
    <div><b>24<small>h<br>/24</small></b><i>du lundi au samedi</i></div>
    <div><b data-count="0" data-suffix="€">0</b><i>de frais de déplacement</i></div>
  </div>
</section>"""

MARQUEE = """
<div class="marquee" aria-hidden="true"><div class="marquee__track">%s</div></div>""" % (
    ("".join('<span>%s</span><i>◆</i>' % s for s in
             ["Recherche de fuite", "Débouchage", "Chauffe-eau", "Dépannage 24h/24",
              "Diagnostic gratuit", "Déplacement offert", "Plomberie complète",
              "Rénovation clé en main", "Toulouse &amp; agglomération"])) * 2)

BA_BLOCK = """
<section class="sec ba" id="realisations">
  <div class="wrap">
    <header class="sec__head sec__head--center">
      <p class="eyebrow reveal"><span class="idx">→</span> Réalisations</p>
      <h2 class="sec__title reveal">Glissez pour voir<br><span class="accent">la transformation.</span></h2>
      <p class="sec__lead reveal">Je ne fais pas que dépanner : je refais aussi des cuisines et des salles
        de bains entières. Attrapez la poignée et faites-la glisser.</p>
    </header>
    <div class="ba__stage reveal">
      <div class="ba__frame" id="baFrame">
        <img class="ba__after" id="baAfter" src="assets/img/sdb-07.webp" alt="Salle de bains après rénovation à Toulouse, faïence grise et vasque design" width="1600" height="1067">
        <div class="ba__beforeWrap" id="baBeforeWrap">
          <img class="ba__before" id="baBefore" src="assets/img/plomberie-04.webp" alt="Salle de bains avant rénovation, plomberie en cours de dépose" width="1600" height="1067">
        </div>
        <span class="ba__tag ba__tag--b">Avant</span><span class="ba__tag ba__tag--a">Après</span>
        <div class="ba__handle" id="baHandle" role="slider" tabindex="0" aria-label="Curseur avant / après"
             aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"><i></i><i></i></div>
      </div>
      <div class="ba__meta">
        <div class="ba__tabs" role="tablist">
          <button class="ba__tab is-on" role="tab" aria-selected="true"
            data-before="assets/img/plomberie-04.webp" data-after="assets/img/sdb-07.webp"
            data-title="Salle de bains — Toulouse Centre"
            data-info="Reprise complète des évacuations, faïence grise pleine hauteur, vasque suspendue."><span class="idx">01</span> Salle de bains</button>
          <button class="ba__tab" role="tab" aria-selected="false"
            data-before="assets/img/plomberie-03.webp" data-after="assets/img/cuisine-09.webp"
            data-title="Cuisine — Rangueil"
            data-info="Nouvelle arrivée d'eau, évacuation lave-vaisselle, plan de travail et pose complète."><span class="idx">02</span> Cuisine</button>
          <button class="ba__tab" role="tab" aria-selected="false"
            data-before="assets/img/plomberie-02.webp" data-after="assets/img/sdb-02.webp"
            data-title="Salle d'eau — Blagnac"
            data-info="Douche et baignoire, double vasque, ventilation reprise. Plus d'odeur de siphon."><span class="idx">03</span> Salle d'eau</button>
        </div>
        <div class="ba__txt">
          <h3 id="baTitle">Salle de bains — Toulouse Centre</h3>
          <p id="baInfo">Reprise complète des évacuations, faïence grise pleine hauteur, vasque suspendue.</p>
          <a class="link-arrow" href="contact.html">Demander le même résultat chez moi __ARROW__</a>
        </div>
      </div>
    </div>
  </div>
</section>"""


def gallery(slugs, alts, caps, wide=False, eager=0):
    """Galerie de grandes photos. srcset pour ne pas charger du 1600px sur un mobile."""
    figs = []
    for i, (sl, a, c) in enumerate(zip(slugs, alts, caps)):
        prio = ('fetchpriority="high"' if i < eager else 'loading="lazy"')
        figs.append(
            '<figure class="gal__i reveal">'
            '<img src="assets/img/%s.webp" '
            'srcset="assets/img/%s-sm.webp 800w, assets/img/%s.webp 1600w" '
            'sizes="%s" alt="%s" %s decoding="async" width="1600" height="1067">'
            '<figcaption>%s</figcaption></figure>'
            % (sl, sl, sl, "(max-width:820px) 100vw, (max-width:1280px) 50vw, %dpx"
               % (420 if wide else 620), a, prio, c))
    return '<div class="gal%s">%s</div>' % (" gal--wide" if wide else "", "".join(figs))


# ---------------- ACCUEIL ----------------
HOME_FAQ = [
    ("Le diagnostic est-il vraiment gratuit ?",
     "<p>Oui. Je me déplace chez vous à Toulouse, je cherche l'origine du problème et je vous remets un devis clair. Le diagnostic et le déplacement sont gratuits et sans engagement.</p>"),
    ("Vous ne faites que la recherche de fuite ?",
     "<p>Non, et c'est important : Renauva fait <strong>toute la plomberie</strong> — chauffe-eau, débouchage, robinetterie, WC, colonnes, évacuations, cuivre, PER, multicouche, création de réseau. La recherche de fuite n'est qu'une partie du métier.</p>"),
    ("Intervenez-vous en urgence ?",
     "<p>Oui, 24h/24 du lundi au samedi sur Toulouse et son agglomération pour les fuites, dégâts des eaux et engorgements. Appelez le 06 60 75 37 71.</p>"),
    ("Faites-vous aussi la rénovation complète ?",
     "<p>Oui, en clé en main : salle de bains et cuisine, de la dépose aux finitions, plomberie et carrelage compris. Un seul interlocuteur, aucun corps de métier à coordonner.</p>"),
]

HOME_BODY = (
    HOME_HERO + MARQUEE + credibilite() + """
<section class="sec services" id="services">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal"><span class="idx">→</span> Ce que fait Renauva</p>
      <h2 class="sec__title reveal">Les gros chantiers.<br><span class="accent">Et la panne du jour.</span></h2>
      <p class="sec__lead reveal">Une pièce à refaire entièrement ou une fuite à 22 h : c'est moi qui viens
        dans les deux cas, et je ne sous-traite rien. Le diagnostic est gratuit.</p>
    </header>
    __CARDS__
  </div>
</section>""".replace("__CARDS__", cards([
        {"n": "01", "t": "Rénovation salle de bains",
         "d": "Clé en main : plomberie, évacuations, douche à l'italienne, carrelage, meubles, "
              "sèche-serviettes, ventilation, finitions. Une seule entreprise du début à la fin.",
         "link": "renovation-salle-de-bains.html", "cta": "Voir la rénovation"},
        {"n": "02", "t": "Rénovation cuisine",
         "d": "Clé en main : arrivées et évacuations, raccordement lave-vaisselle, pose des meubles, "
              "plan de travail, crédence, électroménager. Vous ne coordonnez personne.",
         "link": "renovation-cuisine.html", "cta": "Voir la rénovation"},
        {"n": "03", "t": "Recherche de fuite &amp; urgence 24h/24",
         "d": "Fuite visible ou encastrée sous dalle, dégât des eaux, WC bouché, plus d'eau chaude. "
              "On coupe, on localise, on répare — sans attendre l'ouverture des bureaux.",
         "link": "urgence.html", "cta": "Que faire tout de suite"},
        {"n": "04", "t": "Débouchage &amp; dégorgement",
         "d": "Évier, douche, WC, colonne de copropriété, hydrocurage. L'intervention la plus demandée : "
              "on débouche, puis on traite la cause.",
         "link": "plomberie.html", "cta": "Voir les prestations"},
        {"n": "05", "t": "Chauffe-eau &amp; robinetterie",
         "d": "Panne, entartrage, groupe de sécurité, remplacement de ballon, mitigeurs thermostatiques, "
              "robinets d'arrêt, flexibles.",
         "link": "plomberie.html", "cta": "Voir les prestations"},
        {"n": "06", "t": "Sanitaires &amp; canalisations",
         "d": "Pose de baignoire, douche, WC suspendu, adaptation PMR. Remplacement de canalisation, "
              "passage cuivre vers PER ou multicouche.",
         "link": "plomberie.html", "cta": "Voir les prestations"},
    ]))
    + cta_band("Un projet ou une panne&nbsp;? Parlons-en.",
               "Diagnostic et déplacement gratuits. Je vous rappelle avec un devis clair.",
               "Demander un diagnostic gratuit")
    + TRUST + avis_section(limite=3, carrousel=True) + PROCESS + BA_BLOCK + ARTISAN
    + ZONE_TEASER.replace("__MAP__", ZONE_MAP).replace(
        "__LIST__", "".join("<li>%s</li>" % z for z in ZONE_LIST[:20]))
    + cta_band("Vous êtes dans ma zone d'intervention&nbsp;?",
               "Toulouse et 30&nbsp;km alentour, du lundi au samedi. Laissez-moi vos coordonnées.",
               "Être rappelé rapidement")
    + faq_html(HOME_FAQ) + CTA_FINAL
)

# ---------------- PLOMBERIE ----------------
PLOMB_FAQ = [
    ("Combien coûte une intervention de plomberie à Toulouse ?",
     "<p>Le déplacement et le diagnostic sont gratuits, donc le devis part de 0 €. Ensuite tout dépend de la panne : un débouchage simple n'a rien à voir avec le remplacement d'un chauffe-eau. Je chiffre sur place, poste par poste, avant de commencer.</p>"),
    ("Comment se passe une recherche de fuite ?",
     "<p>Je localise l'origine de la fuite en limitant la casse : contrôle des arrivées et des évacuations, mise en pression, inspection des points sensibles. L'objectif est de trouver sans démolir la moitié de la pièce, puis de réparer dans la foulée.</p>"),
    ("Mes canalisations sentent mauvais, c'est grave ?",
     "<p>Une odeur d'égout vient presque toujours d'un siphon désamorcé, d'une ventilation de chute bouchée ou d'une évacuation mal pentée. C'est réparable, et durablement — pas avec un produit versé dans le siphon tous les mois.</p>"),
    ("Travaillez-vous le cuivre, le PER et le multicouche ?",
     "<p>Oui, les trois, en réparation comme en création de réseau complet. Le choix du matériau se fait selon l'existant, l'accès et la durée de vie attendue.</p>"),
    ("Intervenez-vous en appartement et en copropriété ?",
     "<p>Oui. Appartements, maisons, colonnes montantes et parties privatives. Pour les parties communes, il faut l'accord du syndic : Je vous dis sur place ce qui relève de vous et ce qui relève de la copropriété.</p>"),
]

PLOMB_BODY = (
    phero("Plomberie · Toulouse &amp; agglomération",
          "Plombier à Toulouse&nbsp;:<br><span class=\"accent\">dépannage et plomberie générale.</span>",
          "Recherche de fuite, débouchage, chauffe-eau, robinetterie, évacuations, création de réseau. "
          "Je fais <strong>toute la plomberie</strong> — et le diagnostic est gratuit.",
          "plomberie-01.webp",
          "Plombier soudant des tuyaux en cuivre lors d'une intervention à Toulouse")
    + credibilite()
    + """
<section class="sec" id="prestations">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal"><span class="idx">→</span> Prestations</p>
      <h2 class="sec__title reveal">Tout ce qui touche<br><span class="accent">à l'eau chez vous.</span></h2>
      <p class="sec__lead reveal">Beaucoup de plombiers se limitent à une spécialité. J'interviens sur
        l'ensemble du réseau, de la vanne d'arrivée au dernier siphon.</p>
    </header>
    __CARDS__
  </div>
</section>""".replace("__CARDS__", cards([
        {"n": "01", "t": "Recherche de fuite",
         "d": "Localisation de l'origine avec le minimum de casse : arrivées, évacuations, murs, sols, chauffage. Puis réparation dans la foulée."},
        {"n": "02", "t": "Débouchage &amp; engorgement",
         "d": "Évier, douche, baignoire, WC, colonne. On débouche, et surtout on identifie pourquoi ça se bouchait."},
        {"n": "03", "t": "Chauffe-eau &amp; ballon",
         "d": "Panne, fuite, entartrage, groupe de sécurité, remplacement complet, mise en service. Électrique et thermodynamique."},
        {"n": "04", "t": "Robinetterie &amp; mitigeurs",
         "d": "Remplacement, réparation, mitigeurs thermostatiques, robinets d'arrêt, flexibles, cartouches."},
        {"n": "05", "t": "WC &amp; sanitaires",
         "d": "WC suspendus et classiques, bâti-support, mécanisme de chasse, lavabos, vasques, receveurs."},
        {"n": "06", "t": "Évacuations &amp; colonnes",
         "d": "Reprise de pentes, remplacement de descentes, ventilation de chute, siphons qui se désamorcent, odeurs."},
        {"n": "07", "t": "Création de réseau",
         "d": "Cuivre, PER, multicouche. Nouvelle arrivée, nouvelle évacuation, déplacement de point d'eau, alimentation lave-linge ou lave-vaisselle."},
        {"n": "08", "t": "Dégât des eaux",
         "d": "Coupure, recherche de l'origine, réparation, et un compte rendu clair pour votre dossier d'assurance."},
    ], "grid4"))
    + """
<section class="sec split">
  <div class="wrap split__in">
    <div class="split__txt">
      <p class="eyebrow reveal"><span class="idx">→</span> Ce que ça règle vraiment</p>
      <h2 class="sec__title reveal">Plus d'odeurs.<br><span class="accent">Plus d'eau qui stagne.</span></h2>
      <p class="reveal">Les clients qui appellent Renauva veulent deux choses, et toujours les mêmes :
        <strong>que le problème disparaisse</strong>, et <strong>que ça aille vite</strong>. Pas une explication
        technique de vingt minutes, pas un rendez-vous dans trois semaines.</p>
      <p class="reveal">C'est pour ça que je ne me contente pas de faire partir le symptôme.
        Une évacuation qui sent, un siphon qui se vide, un écoulement qui traîne : il remonte à la cause
        pour que vous n'ayez pas à rappeler dans deux mois.</p>
      <ul class="ticks reveal">
        <li>Diagnostic gratuit sur place, sans engagement</li>
        <li>Devis clair poste par poste avant toute intervention</li>
        <li>Réparation durable, pas un rustine qui tiendra trois semaines</li>
        <li>Chantier laissé propre</li>
      </ul>
      <div class="artisan__acts reveal">
        <a class="btn btn--blue btn--lg" href="tel:__TEL__">__ICPH__ __TELH__</a>
        <a class="btn btn--ghost btn--lg" href="contact.html">Demander un diagnostic</a>
      </div>
    </div>
    <div class="split__img reveal">
      <img src="assets/img/plomberie-02.webp" alt="Main gantée serrant un raccord de plomberie avec une clé à molette"
           loading="lazy" width="1600" height="1067">
    </div>
  </div>
</section>"""
    + RESEAU
    + PROCESS
    + """
<section class="sec alt" id="urgence-teaser">
  <div class="wrap cta__in">
    <p class="eyebrow reveal" style="justify-content:center"><span class="pulse"></span> Ça fuit maintenant ?</p>
    <h2 class="sec__title reveal">Une urgence ne se planifie pas.</h2>
    <p class="sec__lead reveal" style="margin-inline:auto">Fuite, dégât des eaux, WC bouché un dimanche :
      voici les trois gestes à faire avant même que j'arrive.</p>
    <p class="reveal" style="margin-top:24px"><a class="btn btn--red btn--lg" href="urgence.html">Voir la page urgence</a></p>
  </div>
</section>"""
    + avis_section(cats=['plomberie'])
    + faq_html(PLOMB_FAQ, "Questions fréquentes — plomberie",
               'Les questions qu\'on nous<br><span class="accent">pose au téléphone.</span>')
    + CTA_FINAL
)

# ---------------- URGENCE ----------------
URG_FAQ = [
    ("Vous intervenez vraiment la nuit ?",
     "<p>Renauva est joignable 24h/24 du lundi au samedi. Selon l'heure et le secteur, je vous dis tout de suite si je peux passer dans la foulée ou au plus tôt le lendemain matin — et je vous guide au téléphone en attendant.</p>"),
    ("Le déplacement en urgence est-il payant ?",
     "<p>Non. Le déplacement et le diagnostic restent gratuits, y compris en urgence. Vous ne payez que la réparation, après un devis annoncé.</p>"),
    ("Que faire avant votre arrivée ?",
     "<p>Fermez l'arrivée d'eau générale, coupez l'électricité si l'eau approche d'une prise ou du tableau, épongez et déplacez ce qui craint l'eau. Puis appelez : je vous dis quoi faire pendant que je me mets en route.</p>"),
    ("Je ne trouve pas ma vanne d'arrêt, que faire ?",
     "<p>Appelez quand même. Elle est le plus souvent sous l'évier, dans les WC, dans un placard technique ou au compteur en pied d'immeuble. Je vous guide au téléphone pour la trouver.</p>"),
    ("C'est un dégât des eaux, dois-je prévenir mon assurance ?",
     "<p>Oui, déclarez dans les cinq jours ouvrés. Je vous remets une facture et un descriptif clair de l'origine de la fuite : c'est exactement ce que votre assureur demande.</p>"),
]

URG_BODY = (
    phero("Urgence · 24h/24, du lundi au samedi",
          "Urgence plomberie<br><span class=\"accent\">à Toulouse.</span>",
          "Fuite d'eau, dégât des eaux, canalisation bouchée, chauffe-eau hors service. "
          "On coupe, on localise, on répare. <strong>Déplacement et diagnostic gratuits</strong>, même en urgence.",
          "plomberie-04.webp",
          "Intervention d'urgence de plomberie sur un lavabo à Toulouse", "phero--urg")
    + credibilite()
    + """
<section class="sec" id="gestes">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal"><span class="pulse"></span> À faire tout de suite</p>
      <h2 class="sec__title reveal">Trois gestes<br><span class="accent">avant qu'il arrive.</span></h2>
      <p class="sec__lead reveal">Chaque minute compte : ce sont ces trois réflexes qui font la différence
        entre une flaque et un plafond à refaire.</p>
    </header>
    <ol class="steps">
      <li class="reveal"><span class="steps__n">1</span><h3>Coupez l'eau</h3>
        <p>Vanne d'arrêt générale : sous l'évier, dans les WC, dans le placard technique ou au compteur.
          Fermez-la à fond. Si vous ne la trouvez pas, appelez, on vous guide.</p></li>
      <li class="reveal"><span class="steps__n">2</span><h3>Coupez le courant si besoin</h3>
        <p>Si l'eau approche d'une prise, d'un luminaire ou du tableau électrique, coupez le disjoncteur
          général avant de toucher quoi que ce soit.</p></li>
      <li class="reveal"><span class="steps__n">3</span><h3>Appelez-moi</h3>
        <p>Décrivez-moi ce que vous voyez et d'où ça vient. Je vous dis quoi faire en attendant et je me mets
          en route. Le diagnostic reste gratuit.</p></li>
    </ol>
    <div class="urgcall reveal">
      <p>Ne perdez pas de temps à remplir un formulaire.</p>
      <a class="btn btn--red btn--lg" href="tel:__TEL__">__ICPH__ Appeler le __TELH__</a>
      <a class="btn btn--wa btn--lg" href="https://wa.me/33660753771" target="_blank" rel="noopener">__ICWA__ Urgence sur WhatsApp</a>
    </div>
  </div>
</section>

<section class="sec alt" id="cas">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal"><span class="idx">→</span> Ce qu'on traite en urgence</p>
      <h2 class="sec__title reveal">Si c'est là-dedans,<br><span class="accent">ça n'attend pas demain.</span></h2>
    </header>
    __CARDS__
  </div>
</section>""".replace("__CARDS__", cards([
        {"n": "01", "t": "Fuite d'eau",
         "d": "Sous un évier, dans un mur, au plafond, sur une colonne. Coupure, localisation, réparation."},
        {"n": "02", "t": "Dégât des eaux",
         "d": "Chez vous ou chez le voisin. Origine identifiée, réparation, et un descriptif clair pour l'assurance."},
        {"n": "03", "t": "Canalisation bouchée",
         "d": "WC, évier ou douche qui refoulent. Débouchage puis traitement de la cause, pas juste du symptôme."},
        {"n": "04", "t": "Chauffe-eau en panne",
         "d": "Plus d'eau chaude, fuite au groupe de sécurité, cuve percée. Réparation ou remplacement rapide."},
        {"n": "05", "t": "Rupture de canalisation",
         "d": "Gel, corrosion, choc. Mise en sécurité immédiate puis remplacement de la portion touchée."},
        {"n": "06", "t": "Odeurs d'égout",
         "d": "Siphon désamorcé, ventilation bouchée, évacuation mal pentée. On remonte jusqu'à la cause."},
    ], "grid3"))
    + """
<section class="sec split">
  <div class="wrap split__in">
    <div class="split__txt">
      <p class="eyebrow reveal"><span class="idx">→</span> Pourquoi appeler Renauva</p>
      <h2 class="sec__title reveal">Vous parlez<br><span class="accent">directement à l'artisan.</span></h2>
      <p class="reveal">Pas de plateforme téléphonique, pas de mise en relation avec un inconnu qui facture
        le déplacement avant même d'avoir regardé. Vous appelez, je réponds, et c'est moi qui viens.</p>
      <ul class="ticks reveal">
        <li>Déplacement et diagnostic gratuits, y compris en urgence</li>
        <li>Prix annoncé avant intervention, pas après</li>
        <li>Plus de 7 ans d'expertise sur Toulouse</li>
        <li>Conseils au téléphone immédiatement, avant même d'arriver</li>
      </ul>
      <div class="artisan__acts reveal">
        <a class="btn btn--red btn--lg" href="tel:__TEL__">__ICPH__ __TELH__</a>
      </div>
    </div>
    <div class="split__img reveal">
      <img src="assets/img/plomberie-03.webp" alt="Plombier resserrant un robinet d'arrêt sous un lavabo"
           loading="lazy" width="1600" height="1067">
    </div>
  </div>
</section>"""
    + avis_section(cats=['plomberie'], limite=3,
                   eyebrow='Avis clients',
                   titre='Ils ont appelé<br><span class=\'accent\'>en urgence.</span>')
    + faq_html(URG_FAQ, "Questions fréquentes — urgence",
               'Ce qu\'il faut savoir<br><span class="accent">quand ça coule.</span>')
    + CTA_FINAL
)

# ---------------- RÉNOVATION SDB ----------------
SDB_FAQ = [
    ("Combien coûte une rénovation de salle de bains à Toulouse ?",
     "<p>Ça dépend de la surface, de l'état de l'existant et du niveau de finition. L'estimateur du site donne une fourchette indicative en 30 secondes, et le diagnostic gratuit sur place débouche sur un devis ferme.</p>"),
    ("Combien de temps dure le chantier ?",
     "<p>Une salle de bains complète prend en général d'une à deux semaines selon la surface, la dépose et les délais de livraison des matériaux. Je vous donne un planning au devis, et je m'y tiens.</p>"),
    ("Gérez-vous aussi le carrelage et les meubles ?",
     "<p>Oui, c'est tout l'intérêt du clé en main : plomberie, évacuations, carrelage, faïence, meubles, sanitaires et finitions. Vous n'avez aucun autre artisan à coordonner.</p>"),
    ("Peut-on remplacer une baignoire par une douche à l'italienne ?",
     "<p>Oui, c'est une des demandes les plus fréquentes. La faisabilité dépend surtout de la hauteur disponible pour l'évacuation. Je vérifie ça gratuitement lors du diagnostic.</p>"),
    ("Puis-je acheter moi-même les meubles et les sanitaires ?",
     "<p>Oui. Je peux tout fournir ou poser ce que vous avez choisi. Dans ce cas je vous dis avant l'achat si le modèle est compatible avec l'existant.</p>"),
]

SDB_BODY = (
    phero("Rénovation · Toulouse &amp; agglomération",
          "Rénovation de salle de bains<br><span class=\"accent\">clé en main à Toulouse.</span>",
          "Douche à l'italienne, baignoire, double vasque, faïence pleine hauteur et reprise complète "
          "des évacuations. Un seul artisan, de la dépose au dernier joint.",
          "sdb-06.webp", "Salle de bains rénovée à Toulouse avec accents bois et vasque suspendue")
    + """
<section class="sec alt">
  <div class="wrap">
    <header class="sec__head sec__head--center">
      <p class="eyebrow reveal"><span class="idx">→</span> Le résultat, tout de suite</p>
      <h2 class="sec__title reveal">Voilà la pièce<br><span class="accent">qu'on vous rend.</span></h2>
      <p class="sec__lead reveal">Faïence pleine hauteur, douche de plain-pied, évacuations reprises :
        le niveau de finition se décide avec vous, gratuitement, lors du diagnostic.</p>
    </header>
    __GAL__
  </div>
</section>""".replace("__GAL__", gallery(
        ["sdb-04", "sdb-02", "sdb-01", "sdb-06", "sdb-03", "sdb-05"],
        ["Salle de bains rénovée à Toulouse avec douche à l'italienne et double vasque",
         "Salle de bains avec baignoire îlot, douche et double vasque bois",
         "Salle de bains avec double vasque et miroirs suspendus",
         "Salle de bains rénovée avec accents bois et vasque design",
         "Salle de bains avec baignoire et vasque sur meuble",
         "Salle de bains carrelage gris pleine hauteur et sanitaires blancs"],
        ["Douche à l'italienne", "Baignoire &amp; douche", "Double vasque",
         "Accents bois", "Baignoire", "Faïence pleine hauteur"], eager=2))
    + credibilite()

    + """
<section class="sec">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal"><span class="idx">→</span> Ce qui est compris</p>
      <h2 class="sec__title reveal">Vous ne coordonnez<br><span class="accent">personne.</span></h2>
      <p class="sec__lead reveal">Pas de plombier le lundi, de carreleur le jeudi et de menuisier « la semaine
        prochaine ». Je fais tout, dans l'ordre, sans temps mort.</p>
    </header>
    __CARDS__
  </div>
</section>""".replace("__CARDS__", cards([
        {"n": "01", "t": "Dépose complète", "d": "Démontage de l'existant, évacuation des gravats, protection du reste du logement."},
        {"n": "02", "t": "Plomberie &amp; évacuations", "d": "Reprise des arrivées, des évacuations et des pentes. C'est là que se jouent les odeurs et l'écoulement."},
        {"n": "03", "t": "Douche à l'italienne", "d": "Receveur extra-plat ou douche de plain-pied, étanchéité soignée, paroi sur mesure."},
        {"n": "04", "t": "Carrelage &amp; faïence", "d": "Sol et murs, pleine hauteur si vous voulez, joints réguliers et coupes propres."},
        {"n": "05", "t": "Meubles &amp; sanitaires", "d": "Vasque simple ou double, WC suspendu, robinetterie thermostatique, miroirs et rangements."},
        {"n": "06", "t": "Ventilation &amp; finitions", "d": "VMC reprise, peinture, plinthes, joints silicone. La pièce est rendue finie et propre."},
    ], "grid3"))

    + """
<section class="sec split">
  <div class="wrap split__in">
    <div class="split__txt">
      <p class="eyebrow reveal"><span class="idx">→</span> Budget</p>
      <h2 class="sec__title reveal">Une fourchette,<br><span class="accent">en 30 secondes.</span></h2>
      <p class="reveal">Quatre questions et vous savez dans quel ordre de grandeur vous vous situez, avant même
        de décrocher le téléphone. C'est indicatif — le prix ferme sort du diagnostic gratuit sur place.</p>
      <div class="artisan__acts reveal">
        <a class="btn btn--blue btn--lg" href="contact.html#estimateur">Estimer mon budget</a>
        <a class="btn btn--ghost btn--lg" href="tel:__TEL__">__TELH__</a>
      </div>
    </div>
    <div class="split__img reveal">
      <img src="assets/img/sdb-04.webp" alt="Salle de bains moderne avec douche à l'italienne et double vasque"
           loading="lazy" width="1600" height="1067">
    </div>
  </div>
</section>"""
    + PROCESS
    + avis_section(cats=['sdb'])
    + faq_html(SDB_FAQ, "Questions fréquentes — salle de bains",
               'Avant de vous lancer,<br><span class="accent">vous vous demandez…</span>')
    + CTA_FINAL
)

# ---------------- RÉNOVATION CUISINE ----------------
CUIS_FAQ = [
    ("Combien coûte une rénovation de cuisine à Toulouse ?",
     "<p>Le budget dépend surtout des meubles et du plan de travail, puis de l'ampleur des reprises de plomberie et d'électricité. L'estimateur du site donne une fourchette indicative, le diagnostic gratuit donne le prix ferme.</p>"),
    ("Posez-vous les cuisines achetées en magasin ?",
     "<p>Oui. Cuisine en kit ou sur mesure, je m'occupe de la dépose, des raccordements, de la pose des meubles, du plan de travail et de l'électroménager.</p>"),
    ("Peut-on déplacer l'évier ou le lave-vaisselle ?",
     "<p>Oui, à condition de pouvoir créer une évacuation avec une pente correcte. C'est justement ce que je vérifie lors du diagnostic gratuit, avant que vous ne commandiez quoi que ce soit.</p>"),
    ("Combien de temps sans cuisine ?",
     "<p>Comptez en général de quelques jours à deux semaines selon l'ampleur. Le planning est annoncé au devis, et l'eau est rétablie chaque soir quand c'est possible.</p>"),
    ("Faites-vous aussi la crédence et le plan de travail ?",
     "<p>Oui : crédence carrelée ou en panneau, plan de travail découpé et posé, joints et finitions comprises.</p>"),
]

CUIS_BODY = (
    phero("Rénovation · Toulouse &amp; agglomération",
          "Rénovation de cuisine<br><span class=\"accent\">clé en main à Toulouse.</span>",
          "Arrivées d'eau, évacuations, raccordement lave-vaisselle, pose des meubles, plan de travail "
          "et crédence. De la cuisine des années 80 à une cuisine que vous avez envie de montrer.",
          "cuisine-03.webp", "Cuisine moderne rénovée à Toulouse avec îlot central et tabourets")
    + """
<section class="sec alt">
  <div class="wrap">
    <header class="sec__head sec__head--center">
      <p class="eyebrow reveal"><span class="idx">→</span> Le résultat, tout de suite</p>
      <h2 class="sec__title reveal">Voilà la cuisine<br><span class="accent">qu'on vous rend.</span></h2>
      <p class="sec__lead reveal">Plan de travail, crédence, raccordements invisibles :
        tout se décide avec vous, gratuitement, lors du diagnostic.</p>
    </header>
    __GAL__
  </div>
</section>""".replace("__GAL__", gallery(
        ["cuisine-03", "cuisine-01", "cuisine-10", "cuisine-06",
         "cuisine-09", "cuisine-05", "cuisine-07", "cuisine-02"],
        ["Cuisine rénovée à Toulouse avec îlot central et tabourets",
         "Cuisine claire avec plan de travail en marbre",
         "Cuisine à meubles blancs et plan de travail noir",
         "Cuisine contemporaine avec crédence en carreaux métro",
         "Cuisine avec plan de travail en marbre et robinetterie design",
         "Cuisine ouverte avec îlot et comptoir",
         "Cuisine avec plan de travail en bois massif",
         "Cuisine moderne à façades blanches"],
        ["Îlot central", "Plan marbre", "Bicolore", "Crédence métro",
         "Marbre", "Cuisine ouverte", "Plan bois", "Façades blanches"], eager=2))
    + credibilite()

    + """
<section class="sec">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal"><span class="idx">→</span> Ce qui est compris</p>
      <h2 class="sec__title reveal">De la dépose<br><span class="accent">au dernier joint.</span></h2>
      <p class="sec__lead reveal">Une cuisine, c'est d'abord de la plomberie : c'est là que les mauvaises
        surprises arrivent, et c'est justement mon métier.</p>
    </header>
    __CARDS__
  </div>
</section>""".replace("__CARDS__", cards([
        {"n": "01", "t": "Dépose de l'ancienne cuisine", "d": "Démontage, débranchement, évacuation. Le chantier commence propre."},
        {"n": "02", "t": "Arrivées &amp; évacuations", "d": "Eau chaude, eau froide, évacuation évier et lave-vaisselle, déplacement de point d'eau si besoin."},
        {"n": "03", "t": "Pose des meubles", "d": "Caissons alignés et de niveau, portes réglées, socles et corniches ajustés."},
        {"n": "04", "t": "Plan de travail", "d": "Découpe, pose, encastrement de l'évier et de la plaque, joints étanches."},
        {"n": "05", "t": "Crédence", "d": "Carrelage, carreaux métro ou panneau. Coupes nettes autour des prises."},
        {"n": "06", "t": "Électroménager", "d": "Raccordement et mise en service du lave-vaisselle, du four, de la plaque et de la hotte."},
    ], "grid3"))

    + """
<section class="sec split">
  <div class="wrap split__in">
    <div class="split__txt">
      <p class="eyebrow reveal"><span class="idx">→</span> Budget</p>
      <h2 class="sec__title reveal">Savoir où vous allez,<br><span class="accent">avant de commander.</span></h2>
      <p class="reveal">Beaucoup de cuisines sont achetées avant de savoir si l'évacuation peut être déplacée.
        Faites l'inverse : estimation en 30 secondes, puis diagnostic gratuit sur place, puis commande.</p>
      <div class="artisan__acts reveal">
        <a class="btn btn--blue btn--lg" href="contact.html#estimateur">Estimer mon budget</a>
        <a class="btn btn--ghost btn--lg" href="tel:__TEL__">__TELH__</a>
      </div>
    </div>
    <div class="split__img reveal">
      <img src="assets/img/cuisine-09.webp" alt="Cuisine rénovée avec plan de travail en marbre à Toulouse"
           loading="lazy" width="1600" height="1067">
    </div>
  </div>
</section>"""
    + PROCESS
    + avis_section(cats=['cuisine'])
    + faq_html(CUIS_FAQ, "Questions fréquentes — cuisine",
               'Avant de commander<br><span class="accent">votre cuisine…</span>')
    + CTA_FINAL
)

# ---------------- ZONE ----------------
ZONE_BODY = (
    phero("Zone d'intervention",
          "Toulouse<br><span class=\"accent\">et toute l'agglomération.</span>",
          "Déplacement gratuit dans un rayon d'environ 30&nbsp;km autour de Toulouse. "
          "Votre commune n'est pas listée&nbsp;? Appelez, elle y est sûrement.",
          "cuisine-08.webp", "Vue d'une cuisine rénovée près de Toulouse")
    + ("""
<section class="sec">
  <div class="wrap">
    <div class="zone__wrap reveal">
      __MAP__
      <div>
        <h2 class="sec__title reveal" style="font-size:clamp(26px,3.2vw,40px)">Quartiers de Toulouse</h2>
        <ul class="zone__list">__L1__</ul>
        <h2 class="sec__title reveal" style="font-size:clamp(26px,3.2vw,40px);margin-top:34px">Communes de l'agglomération</h2>
        <ul class="zone__list">__L2__</ul>
      </div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    <header class="sec__head">
      <p class="eyebrow reveal"><span class="idx">→</span> Intervenir vite, c'est d'abord être près</p>
      <h2 class="sec__title reveal">Un artisan local,<br><span class="accent">pas une plateforme.</span></h2>
    </header>
    <div class="sec__lead reveal" style="max-width:70ch">
      <p>Renauva est basé à Toulouse et n'intervient que sur Toulouse et sa périphérie immédiate.
        Ce n'est pas une limite commerciale, c'est ce qui permet de passer <strong>le jour même</strong>
        sur une fuite au lieu de vous donner rendez-vous la semaine suivante.</p>
      <p>Que vous soyez en appartement haussmannien au Capitole, en maison de brique à la Côte Pavée,
        en résidence récente à Blagnac ou en pavillon à Tournefeuille, les problèmes ne sont pas les mêmes :
        colonnes anciennes en fonte d'un côté, PER et multicouche de l'autre. Plus de sept ans sur le secteur,
        ça veut dire connaître les deux.</p>
      <p><strong>Le déplacement est gratuit partout dans cette zone</strong>, urgence comprise.</p>
    </div>
  </div>
</section>"""
        .replace("__MAP__", ZONE_MAP)
        .replace("__L1__", "".join("<li>%s</li>" % z for z in ZONE_LIST[:14]))
        .replace("__L2__", "".join("<li>%s</li>" % z for z in ZONE_LIST[14:])))
    + CTA_FINAL
)


# ==========================================================================
# PARCOURS DE DIAGNOSTIC — qualification + score de rentabilité
# Le calcul est fait en JavaScript (assets/js/app.js), de façon déterministe :
# formule urgence + budget + durée + distance + probabilité, comme au cahier
# des charges. Aucun appel externe, aucune donnée envoyée sans validation.
# ==========================================================================
DIAG_SECTION = """
<section class="sec diag" id="diagnostic">
  <div class="wrap">
    <header class="sec__head sec__head--center">
      <p class="eyebrow reveal"><span class="idx">&rarr;</span> Diagnostic express</p>
      <h2 class="sec__title reveal">D&eacute;crivez votre probl&egrave;me.<br><span class="accent">Je saurai tout avant d&#39;arriver.</span></h2>
      <p class="sec__lead reveal">Quelques questions, vos photos, et c&#39;est r&eacute;gl&eacute;. Vous obtenez une estimation
        imm&eacute;diate, et je re&ccedil;ois un dossier complet &mdash; je ne vous rappellerai pas pour vous demander
        ce que vous venez d&#39;&eacute;crire.</p>
    </header>

    <div class="diag__box reveal">
      <div class="diag__rail" aria-hidden="true"><i id="diagRail"></i></div>
      <p class="diag__count" id="diagCount">&Eacute;tape 1</p>

      <form id="diagForm" novalidate>

        <div class="diag__step is-on" data-step="type">
          <p class="diag__q">De quoi s&#39;agit-il&nbsp;?</p>
          <div class="opts opts--3">
            <label class="opt"><input type="radio" name="type" value="Fuite d&#39;eau / d&eacute;g&acirc;t des eaux" data-fam="dep" data-duree="1.5" data-proba=".85" checked><span><b>Fuite d&#39;eau</b><i>Visible, encastr&eacute;e ou d&eacute;g&acirc;t des eaux</i></span></label>
            <label class="opt"><input type="radio" name="type" value="Canalisation bouch&eacute;e" data-fam="dep" data-duree="1" data-proba=".9"><span><b>Canalisation bouch&eacute;e</b><i>&Eacute;vier, douche, WC, colonne</i></span></label>
            <label class="opt"><input type="radio" name="type" value="Chauffe-eau" data-fam="dep" data-duree="2.5" data-proba=".8"><span><b>Chauffe-eau</b><i>Panne, fuite, remplacement</i></span></label>
            <label class="opt"><input type="radio" name="type" value="Robinetterie / sanitaire" data-fam="dep" data-duree="1.5" data-proba=".88"><span><b>Robinetterie</b><i>Mitigeur, WC, vasque, flexible</i></span></label>
            <label class="opt"><input type="radio" name="type" value="R&eacute;novation salle de bains" data-fam="reno" data-base="6500" data-duree="8" data-proba=".95"><span><b>R&eacute;novation salle de bains</b><i>Cl&eacute; en main</i></span></label>
            <label class="opt"><input type="radio" name="type" value="R&eacute;novation cuisine" data-fam="reno" data-base="7500" data-duree="8" data-proba=".95"><span><b>R&eacute;novation cuisine</b><i>Cl&eacute; en main</i></span></label>
          </div>
        </div>

        <div class="diag__step" data-step="urgence" data-fam="dep">
          <p class="diag__q">C&#39;est pour quand&nbsp;?</p>
          <div class="opts opts--3">
            <label class="opt"><input type="radio" name="urgence" value="AUJOURD&#39;HUI &mdash; urgence" data-u="3" checked><span><b>Aujourd&#39;hui</b><i>&Ccedil;a coule, &ccedil;a d&eacute;borde, c&#39;est bloquant</i></span></label>
            <label class="opt"><input type="radio" name="urgence" value="Cette semaine" data-u="2"><span><b>Cette semaine</b><i>G&ecirc;nant mais pas critique</i></span></label>
            <label class="opt"><input type="radio" name="urgence" value="Projet &agrave; planifier" data-u="1"><span><b>&Agrave; planifier</b><i>Quand &ccedil;a vous arrange</i></span></label>
          </div>
        </div>

        <div class="diag__step" data-step="surface" data-fam="reno">
          <p class="diag__q">Quelle surface&nbsp;?</p>
          <div class="opts opts--4">
            <label class="opt"><input type="radio" name="surface" value="Moins de 4 m&sup2;" data-mult=".8" checked><span><b>&lt; 4 m&sup2;</b><i>Petite pi&egrave;ce</i></span></label>
            <label class="opt"><input type="radio" name="surface" value="4 &agrave; 7 m&sup2;" data-mult="1"><span><b>4 &ndash; 7 m&sup2;</b><i>Standard</i></span></label>
            <label class="opt"><input type="radio" name="surface" value="7 &agrave; 12 m&sup2;" data-mult="1.45"><span><b>7 &ndash; 12 m&sup2;</b><i>Grande pi&egrave;ce</i></span></label>
            <label class="opt"><input type="radio" name="surface" value="Plus de 12 m&sup2;" data-mult="1.9"><span><b>&gt; 12 m&sup2;</b><i>Tr&egrave;s grande</i></span></label>
          </div>
        </div>

        <div class="diag__step" data-step="finition" data-fam="reno">
          <p class="diag__q">Quel niveau de finition&nbsp;?</p>
          <div class="opts opts--3">
            <label class="opt"><input type="radio" name="finition" value="Essentiel" data-mult=".85" checked><span><b>Essentiel</b><i>Propre, solide, sans superflu</i></span></label>
            <label class="opt"><input type="radio" name="finition" value="Confort" data-mult="1.15"><span><b>Confort</b><i>Beaux mat&eacute;riaux, douche italienne</i></span></label>
            <label class="opt"><input type="radio" name="finition" value="Premium" data-mult="1.55"><span><b>Premium</b><i>Sur-mesure, haut de gamme</i></span></label>
          </div>
        </div>

        <div class="diag__step" data-step="depose" data-fam="reno">
          <p class="diag__q">L&#39;existant est-il &agrave; d&eacute;poser&nbsp;?</p>
          <div class="opts opts--3">
            <label class="opt"><input type="radio" name="depose" value="Tout est &agrave; casser" data-add="1400" checked><span><b>Tout est &agrave; casser</b><i>D&eacute;pose compl&egrave;te + &eacute;vacuation</i></span></label>
            <label class="opt"><input type="radio" name="depose" value="Partiellement" data-add="600"><span><b>Partiellement</b><i>On garde une partie</i></span></label>
            <label class="opt"><input type="radio" name="depose" value="Rien &agrave; d&eacute;poser" data-add="0"><span><b>Rien &agrave; d&eacute;poser</b><i>Pi&egrave;ce d&eacute;j&agrave; nue</i></span></label>
          </div>
        </div>

        <div class="diag__step" data-step="secteur">
          <p class="diag__q">O&ugrave; &ecirc;tes-vous&nbsp;?</p>
          <label class="f"><span>Quartier ou commune</span>
            <select id="diagSecteur">__SECTEURS__</select>
            <em class="f__hint">Le d&eacute;placement est gratuit partout dans cette zone.</em></label>
          <p class="diag__sub">Type de logement</p>
          <div class="opts opts--2">
            <label class="opt"><input type="radio" name="logement" value="Maison" checked><span><b>Maison</b><i>Acc&egrave;s direct</i></span></label>
            <label class="opt"><input type="radio" name="logement" value="Appartement"><span><b>Appartement</b><i>Immeuble, &eacute;tage</i></span></label>
          </div>
          <p class="diag__sub">L&#39;acc&egrave;s est-il facile&nbsp;?</p>
          <div class="opts opts--3">
            <label class="opt"><input type="radio" name="acces" value="Facile" data-acc="1" checked><span><b>Facile</b><i>Stationnement, plain-pied</i></span></label>
            <label class="opt"><input type="radio" name="acces" value="Normal" data-acc=".93"><span><b>Normal</b><i>Ascenseur, rue passante</i></span></label>
            <label class="opt"><input type="radio" name="acces" value="Difficile" data-acc=".82"><span><b>Difficile</b><i>Sans ascenseur, acc&egrave;s &eacute;troit</i></span></label>
          </div>
        </div>

        <div class="diag__step" data-step="budget">
          <p class="diag__q">Quel budget avez-vous en t&ecirc;te&nbsp;?</p>
          <p class="diag__note">Personne ne vous tiendra &agrave; ce chiffre. &Ccedil;a sert &agrave; venir avec la bonne solution
            et les bonnes pi&egrave;ces d&egrave;s la premi&egrave;re visite.</p>
          <div class="opts opts--3" id="diagBudget"></div>
        </div>

        <div class="diag__step" data-step="coords">
          <p class="diag__q">O&ugrave; puis-je vous rappeler&nbsp;?</p>
          <div class="f__row">
            <label class="f"><span>Pr&eacute;nom et nom *</span>
              <input type="text" id="diagNom" required autocomplete="name" placeholder="Marie Dupont"></label>
            <label class="f"><span>T&eacute;l&eacute;phone *</span>
              <input type="tel" id="diagTel" required autocomplete="tel" inputmode="tel" placeholder="06 12 34 56 78"></label>
          </div>
          <label class="f"><span>Un d&eacute;tail &agrave; ajouter&nbsp;? (facultatif)</span>
            <textarea id="diagMsg" rows="3" placeholder="Ex : &ccedil;a coule sous l&#39;&eacute;vier depuis hier soir."></textarea></label>
          <label class="f f--check"><input type="checkbox" id="diagRgpd" required>
            <span>J&#39;accepte d&#39;&ecirc;tre recontact&eacute; par Renauva.
              <a href="confidentialite.html">Politique de confidentialit&eacute;</a>.</span></label>
        </div>

        <div class="diag__nav">
          <button type="button" class="btn btn--ghost" id="diagPrev" hidden>Retour</button>
          <button type="button" class="btn btn--blue btn--lg" id="diagNext">Continuer</button>
        </div>
      </form>

      <div class="diag__res" id="diagRes" hidden>
        <div class="diag__resHead">
          <span class="diag__pill" id="diagPill"></span>
          <h3 id="diagResTitle">Votre dossier est pr&ecirc;t.</h3>
        </div>
        <div class="diag__estim" id="diagEstim"></div>
        <ul class="diag__recap" id="diagRecap"></ul>
        <div class="diag__send">
          <a class="btn btn--wa btn--lg btn--full" id="diagWa" href="#" target="_blank" rel="noopener">__ICWA__ Envoyer sur WhatsApp</a>
          <button type="button" class="btn btn--blue btn--lg btn--full" id="diagMail">Envoyer par e-mail</button>
          <a class="btn btn--ghost btn--full" href="tel:__TEL__">__ICPH__ Ou appeler le __TELH__</a>
        </div>
        <p class="f__note" id="diagNote" role="status"></p>
        <button type="button" class="link-arrow" id="diagRestart">Recommencer</button>
      </div>

      <form id="diagMailForm" action="https://api.web3forms.com/submit" method="POST"
            enctype="multipart/form-data" hidden>
        <input type="hidden" name="access_key" value="VOTRE_CLE_WEB3FORMS">
        <input type="hidden" name="subject" id="dmSubject" value="Nouvelle demande &mdash; site Renauva">
        <input type="hidden" name="from_name" value="Site Renauva">
        <input type="hidden" name="message" id="dmMessage">
        <input type="hidden" name="nom" id="dmNom">
        <input type="hidden" name="telephone" id="dmTel">
        <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
      </form>
    </div>
  </div>
</section>""".replace("__SECTEURS__",
    "".join('<option value="%s">%s</option>' % (z, z) for z in ZONE_LIST)
    + '<option value="Autre commune">Autre commune</option>')

# ---------------- CONTACT ----------------
CONTACT_BODY = (
    phero("Contact · Devis gratuit",
          "Parlons de votre problème.<br><span class=\"accent\">Le diagnostic est offert.</span>",
          "Le plus rapide reste l'appel : je réponds moi-même. Sinon, laissez-moi vos coordonnées, "
          "je vous rappelle.",
          "plomberie-02.webp", "Plombier serrant un raccord lors d'une intervention à Toulouse")

    # --- 1. L'APPEL, en tête et sur toute la largeur ---
    + """
<section class="callbar" id="appeler">
  <div class="wrap callbar__in">
    <div class="callbar__left">
      <p class="callbar__label"><span class="pulse"></span> Le plus rapide</p>
      <a class="callbar__num" href="tel:__TEL__">__TELH__</a>
      <p class="callbar__sub">24h/24, du lundi au samedi · Toulouse &amp; agglomération ·
        déplacement et diagnostic gratuits</p>
    </div>
    <div class="callbar__acts">
      <a class="btn btn--blue btn--lg" href="tel:__TEL__">__ICPH__ Appeler</a>
      <a class="btn btn--wa" href="__WA__" target="_blank" rel="noopener">__ICWA__ WhatsApp</a>
      <button class="btn btn--ghost" data-urgence><span class="pulse"></span> Urgence</button>
    </div>
  </div>
</section>"""

    # --- 2. LE FORMULAIRE, pleine largeur ---
    + """
<section class="sec lead" id="rappel">
  <div class="wrap">
    <header class="sec__head sec__head--center">
      <p class="eyebrow reveal"><span class="idx">→</span> Demande de rappel</p>
      <h2 class="sec__title reveal">Pas le temps d'appeler&nbsp;?<br><span class="accent">Je vous rappelle.</span></h2>
      <p class="sec__lead reveal">Cinq champs, trente secondes. Joignez des photos si vous en avez&nbsp;:
        j'arrive avec la bonne pièce dès la première visite.</p>
    </header>

    <form id="leadForm" class="lead__form reveal">
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">

      <div class="lead__grid">
        <label class="f"><span>Nom et prénom *</span>
          <input type="text" name="nom" required autocomplete="name" placeholder="Marie Dupont"></label>
        <label class="f"><span>Téléphone *</span>
          <input type="tel" name="telephone" required autocomplete="tel" inputmode="tel" placeholder="06 12 34 56 78"></label>
        <label class="f"><span>E-mail *</span>
          <input type="email" name="email" required autocomplete="email" inputmode="email" placeholder="marie.dupont@email.com"></label>
        <label class="f"><span>Quartier / commune *</span>
          <input type="text" name="secteur" required placeholder="Rangueil, Toulouse"></label>
        <label class="f"><span>Adresse compl&egrave;te (facultatif)</span>
          <input type="text" name="adresse" autocomplete="street-address" placeholder="12 rue des Lilas, 31400 Toulouse"></label>
        <label class="f"><span>Vos disponibilit&eacute;s</span>
          <select name="disponibilite" id="fDispo">
            <option value="N&#39;importe quand">N&#39;importe quand</option>
            <option value="Matin">Matin</option>
            <option value="Apr&egrave;s-midi">Apr&egrave;s-midi</option>
            <option value="Soir">Soir</option>
          </select></label>

        <label class="f"><span>Type de demande *</span>
          <select name="projet" id="fProjet" required>
            <option value="Plomberie / dépannage">Plomberie / dépannage</option>
            <option value="Urgence fuite d'eau">Urgence fuite d'eau</option>
            <option value="Recherche de fuite">Recherche de fuite</option>
            <option value="Débouchage / engorgement">Débouchage / engorgement</option>
            <option value="Chauffe-eau">Chauffe-eau</option>
            <option value="Rénovation salle de bains">Rénovation salle de bains</option>
            <option value="Rénovation cuisine">Rénovation cuisine</option>
            <option value="Autre">Autre</option>
          </select></label>
        <label class="f"><span>Budget approximatif *</span>
          <select name="budget" id="fBudget" required>
            <option value="">Sélectionnez une fourchette</option>
            <option>Dépannage — moins de 500 €</option>
            <option>500 € – 2 000 €</option>
            <option>2 000 € – 5 000 €</option>
            <option>5 000 € – 10 000 €</option>
            <option>10 000 € – 20 000 €</option>
            <option>Plus de 20 000 €</option>
            <option>Je ne sais pas encore</option>
          </select></label>
        <label class="f f--file"><span>Photos (facultatif)</span>
          <input type="file" name="photos" id="fPhotos" accept="image/jpeg,image/png,image/heic,image/heif,image/webp" multiple>
          <span class="f__drop"><b>Choisir des photos</b> <i>Jusqu&#39;&agrave; 3 &middot; depuis votre galerie</i></span>
          <em class="f__hint" id="fFiles"></em></label>
      </div>

      <label class="f f--wide"><span>Décrivez votre problème</span>
        <textarea name="message" id="fMessage" rows="4"
          placeholder="Ex : fuite sous l'évier de la cuisine depuis hier, l'eau coule dans le meuble."></textarea></label>

      <label class="f--urgence"><input type="checkbox" name="urgence_2h" value="1" id="fUrg2h">
        <span><b>&#128680; C&#39;est urgent</b> — j&#39;ai besoin d&#39;une intervention sous 2h.
        <i>&Agrave; cocher seulement en cas de v&eacute;ritable urgence (fuite active, d&eacute;g&acirc;t en cours).</i></span></label>

      <div class="lead__foot">
        <label class="f f--check"><input type="checkbox" name="consentement" value="Oui" required>
          <span>J'accepte d'être recontacté par Renauva.
            <a href="confidentialite.html">Politique de confidentialité</a>.</span></label>
        <button type="submit" class="btn btn--blue btn--lg" id="fSubmit">Me rappeler</button>
      </div>
      <p class="f__note" id="fNote" role="status"></p>
    </form>
  </div>
</section>"""

)

# ---------------- FAQ ----------------
ALL_FAQ = HOME_FAQ[:1] + PLOMB_FAQ + URG_FAQ + SDB_FAQ[:3] + CUIS_FAQ[:2] + [
    ("Quelle est votre zone d'intervention ?",
     "<p>Toulouse intra-muros et toute l'agglomération : Blagnac, Colomiers, Tournefeuille, Balma, Ramonville, Cugnaux, L'Union, Saint-Orens, Portet-sur-Garonne, Muret et alentours. Le déplacement est gratuit dans toute cette zone.</p>"),
    ("Comment vous payer ?",
     "<p>À la fin de l'intervention, sur facture. Pour les chantiers de rénovation, un acompte est demandé à la commande et le solde à la réception, selon l'échéancier indiqué sur le devis.</p>"),
]

FAQ_BODY = (
    phero("Questions fréquentes",
          "Tout ce qu'on nous<br><span class=\"accent\">demande au téléphone.</span>",
          "Diagnostic, urgences, délais, budget, zone d'intervention. Si votre question n'est pas là, "
          "appelez : la réponse prend deux minutes.",
          "plomberie-01.webp", "Plombier au travail sur des tuyaux en cuivre à Toulouse")
    + faq_html(ALL_FAQ, "Toutes les questions",
               'Diagnostic, urgence,<br><span class="accent">délais et budget.</span>')
    + CTA_FINAL
)

# ---------------- LÉGAL ----------------
LEGAL_HEAD = """
<section class="sec legal">
  <div class="wrap">
    <a class="link-arrow" href="index.html" style="margin-bottom:26px;display:inline-flex">← Retour à l'accueil</a>
"""

MENTIONS_BODY = LEGAL_HEAD + """
    <h1 class="sec__title">Mentions légales</h1>
    <p>Dernière mise à jour : __TODAY__.</p>
    <h2>Éditeur du site</h2>
    <ul>
      <li><strong>Renauva</strong> — entreprise individuelle</li>
      <li>Responsable de la publication : <strong>Brahim Touati</strong></li>
      <li>Activité : plomberie générale, dépannage et recherche de fuite, rénovation de cuisine et de salle de bains</li>
      <li>Adresse : Toulouse (31), France</li>
      <li>Téléphone : <a href="tel:__TEL__">__TELH__</a></li>
      <li>Email : <a href="mailto:touatiibrahim650@gmail.com">touatiibrahim650@gmail.com</a></li>
      <li>SIRET : <em>à compléter</em></li>
      <li>N° TVA intracommunautaire : <em>à compléter (ou « TVA non applicable, art. 293 B du CGI »)</em></li>
      <li>Assurance responsabilité civile professionnelle / décennale : <em>à compléter</em></li>
    </ul>
    <p class="todo">À compléter une fois l'entreprise immatriculée : SIRET, régime de TVA, coordonnées de
      l'assurance décennale. Ces informations sont obligatoires pour un artisan du bâtiment.</p>
    <h2>Hébergement</h2>
    <p>Le site est hébergé par <em>[nom et coordonnées de l'hébergeur, à renseigner après mise en ligne]</em>.</p>
    <h2>Propriété intellectuelle</h2>
    <p>L'ensemble du contenu de ce site (structure, textes, mise en page, code) est la propriété de Renauva.
      Toute reproduction, même partielle, est interdite sans autorisation écrite préalable.</p>
    <p>Les photographies et vidéos d'illustration sont utilisées sous licence commerciale Envato Elements.</p>
    <h2>Devis et prestations</h2>
    <p>Le diagnostic sur place et le déplacement sont gratuits sur Toulouse et son agglomération.
      Les estimations fournies par l'outil d'estimation en ligne sont purement indicatives et n'ont
      aucune valeur contractuelle. Seul un devis écrit signé engage Renauva.</p>
    <h2>Données personnelles</h2>
    <p>Voir la <a href="confidentialite.html">politique de confidentialité</a>.</p>
    <h2>Litiges</h2>
    <p>Le présent site est soumis au droit français. À défaut de résolution amiable, les tribunaux
      compétents sont ceux du ressort de Toulouse.</p>
    <p style="margin-top:40px"><a class="btn btn--blue" href="index.html">Retour au site</a></p>
  </div>
</section>"""

CONF_BODY = LEGAL_HEAD + """
    <h1 class="sec__title">Politique de confidentialité</h1>
    <p>Dernière mise à jour : __TODAY__.</p>
    <h2>Responsable du traitement</h2>
    <p><strong>Renauva</strong> — Brahim Touati, Toulouse (31).
      Contact : <a href="mailto:touatiibrahim650@gmail.com">touatiibrahim650@gmail.com</a> —
      <a href="tel:__TEL__">__TELH__</a>.</p>
    <h2>Données collectées</h2>
    <p>Le site ne collecte aucune donnée à votre insu. Les seules données traitées sont celles que vous
      saisissez volontairement dans le formulaire de contact :</p>
    <ul>
      <li>nom et prénom ;</li><li>numéro de téléphone ;</li><li>quartier ou commune ;</li>
      <li>type de demande et budget approximatif ;</li><li>description libre de votre problème ;</li>
      <li>photos éventuellement jointes.</li>
    </ul>
    <p>Si vous passez par WhatsApp, l'échange est soumis à la politique de confidentialité de WhatsApp
      (Meta Platforms Ireland Ltd.). Le site se contente de pré-remplir un message ; aucune donnée
      n'est stockée par Renauva à ce stade.</p>
    <h2>Finalité et base légale</h2>
    <p>Ces données servent uniquement à vous recontacter, à préparer le diagnostic gratuit et à établir un devis.
      La base légale est votre <strong>consentement</strong>, recueilli par la case à cocher du formulaire,
      ainsi que l'exécution de mesures précontractuelles à votre demande.</p>
    <h2>Destinataires</h2>
    <p>Vos données sont transmises à Brahim Touati (Renauva) par email et enregistrées dans un tableur privé
      servant au suivi des demandes. Le service technique d'acheminement des formulaires (Web3Forms) agit
      comme sous-traitant. Aucune donnée n'est vendue, louée ni transmise à des fins publicitaires.</p>
    <h2>Durée de conservation</h2>
    <p>Les demandes non converties sont conservées 12 mois maximum. Les données liées à une intervention
      réalisée sont conservées le temps des obligations légales et comptables applicables (jusqu'à 10 ans).</p>
    <h2>Vos droits</h2>
    <p>Conformément au RGPD, vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation,
      d'opposition et de portabilité. Pour l'exercer, écrivez à
      <a href="mailto:touatiibrahim650@gmail.com">touatiibrahim650@gmail.com</a>. Réponse sous un mois.
      Vous pouvez aussi saisir la <a href="https://www.cnil.fr" target="_blank" rel="noopener">CNIL</a>.</p>
    <h2>Cookies</h2>
    <p>Ce site n'utilise <strong>aucun cookie de suivi, aucun traceur publicitaire et aucun outil d'analyse
      comportementale</strong>. Aucune bannière de consentement n'est donc nécessaire. Les polices sont
      chargées depuis Google Fonts, ce qui implique une connexion à un serveur Google transmettant votre
      adresse IP ; elles peuvent être auto-hébergées (voir le README).</p>
    <h2>Sécurité</h2>
    <p>Le site est servi en HTTPS. Les données transmises via le formulaire circulent chiffrées.</p>
    <p style="margin-top:40px"><a class="btn btn--blue" href="index.html">Retour au site</a></p>
  </div>
</section>"""


def service_schema(name, desc, url):
    return """{ "@type": "Service", "@id": "%s/%s#service", "name": "%s", "description": "%s",
      "serviceType": "%s", "provider": { "@id": "%s/#business" },
      "areaServed": { "@type": "City", "name": "Toulouse" },
      "url": "%s/%s" }""" % (SITE, url, name, desc, name, SITE, SITE, url)



# ---------------- 404 ----------------
NOTFOUND_BODY = """
<section class="sec legal" style="padding-top:170px;text-align:center">
  <div class="wrap">
    <p class="eyebrow" style="justify-content:center">Erreur 404</p>
    <h1 class="sec__title">Cette page n&#39;existe pas.<br><span class="accent">Le probl&egrave;me, lui, existe toujours.</span></h1>
    <p class="sec__lead" style="margin-inline:auto">Le lien est peut-&ecirc;tre ancien ou mal recopi&eacute;.
      Voici o&ugrave; aller &mdash; et si &ccedil;a fuit maintenant, le plus rapide reste l&#39;appel.</p>
    <div class="cta__acts" style="margin-top:30px">
      <a class="btn btn--blue btn--lg" href="tel:__TEL__">__ICPH__ __TELH__</a>
      <a class="btn btn--ghost btn--lg" href="index.html">Retour &agrave; l&#39;accueil</a>
    </div>
    <div class="grid3" style="margin-top:clamp(40px,5vw,70px);text-align:left">
      <a class="pcard" href="urgence.html"><span class="pcard__n">01</span><h3>Urgence 24h/24</h3>
        <p>Fuite, d&eacute;g&acirc;t des eaux, canalisation bouch&eacute;e.</p></a>
      <a class="pcard" href="plomberie.html"><span class="pcard__n">02</span><h3>Plomberie</h3>
        <p>Recherche de fuite, d&eacute;bouchage, chauffe-eau, robinetterie.</p></a>
      <a class="pcard" href="contact.html"><span class="pcard__n">03</span><h3>Diagnostic gratuit</h3>
        <p>D&eacute;crivez votre probl&egrave;me, je vous rappelle.</p></a>
    </div>
  </div>
</section>"""

# ==========================================================================
# BUILD
# ==========================================================================
PAGES = [
    dict(slug="index.html",
         title="Plombier Toulouse — Dépannage, recherche de fuite | Renauva",
         desc="Plombier à Toulouse : dépannage, recherche de fuite, débouchage, chauffe-eau et plomberie générale. Diagnostic professionnel gratuit, plus de 7 ans d'expertise, 24h/24 du lundi au samedi. 06 60 75 37 71.",
         body=HOME_BODY,
         preload='<link rel="preload" as="image" href="assets/video/hero-poster.webp" fetchpriority="high">',
         schema=faq_schema(HOME_FAQ)),

    dict(slug="plomberie.html",
         title="Plomberie à Toulouse — Dépannage & recherche de fuite | Renauva",
         desc="Plomberie générale à Toulouse : recherche de fuite, débouchage, chauffe-eau, robinetterie, WC, évacuations, création de réseau. Diagnostic et déplacement gratuits. Appelez le 06 60 75 37 71.",
         body=PLOMB_BODY,
         schema=(service_schema("Plomberie générale et dépannage",
                                "Recherche de fuite, débouchage, chauffe-eau, robinetterie, WC, évacuations et création de réseau à Toulouse.",
                                "plomberie.html")
                 + ",\n    " + breadcrumb([("Accueil", "index.html"), ("Plomberie", None)])
                 + ",\n    " + faq_schema(PLOMB_FAQ))),

    dict(slug="urgence.html",
         title="Urgence plomberie Toulouse — Fuite d'eau 24h/24 | Renauva",
         desc="Urgence plombier à Toulouse : fuite d'eau, dégât des eaux, canalisation bouchée, chauffe-eau en panne. Disponible 24h/24 du lundi au samedi, déplacement et diagnostic gratuits. 06 60 75 37 71.",
         body=URG_BODY,
         schema=(service_schema("Dépannage plomberie en urgence",
                                "Intervention d'urgence 24h/24 du lundi au samedi à Toulouse pour fuite d'eau, dégât des eaux et canalisation bouchée.",
                                "urgence.html")
                 + ",\n    " + breadcrumb([("Accueil", "index.html"), ("Urgence", None)])
                 + ",\n    " + faq_schema(URG_FAQ))),

    dict(slug="renovation-salle-de-bains.html",
         title="Rénovation salle de bains Toulouse — clé en main | Renauva",
         desc="Rénovation complète de salle de bains à Toulouse : douche à l'italienne, carrelage, meubles, évacuations. Clé en main par un seul artisan. Diagnostic professionnel gratuit, plus de 7 ans d'expertise.",
         body=SDB_BODY,
         schema=(service_schema("Rénovation de salle de bains clé en main",
                                "Rénovation complète de salle de bains à Toulouse : dépose, plomberie, carrelage, meubles et finitions.",
                                "renovation-salle-de-bains.html")
                 + ",\n    " + breadcrumb([("Accueil", "index.html"), ("Rénovation salle de bains", None)])
                 + ",\n    " + faq_schema(SDB_FAQ))),

    dict(slug="renovation-cuisine.html",
         title="Rénovation cuisine Toulouse — clé en main | Renauva",
         desc="Rénovation de cuisine à Toulouse : arrivées d'eau, évacuations, pose des meubles, plan de travail, crédence et électroménager. Clé en main, diagnostic gratuit, déplacement offert.",
         body=CUIS_BODY,
         schema=(service_schema("Rénovation de cuisine clé en main",
                                "Rénovation complète de cuisine à Toulouse : plomberie, pose de meubles, plan de travail, crédence et électroménager.",
                                "renovation-cuisine.html")
                 + ",\n    " + breadcrumb([("Accueil", "index.html"), ("Rénovation cuisine", None)])
                 + ",\n    " + faq_schema(CUIS_FAQ))),

    dict(slug="zone-intervention.html",
         title="Zone d'intervention — plombier Toulouse et agglomération | Renauva",
         desc="Renauva intervient à Toulouse et dans toute l'agglomération : Blagnac, Colomiers, Tournefeuille, Balma, Ramonville, Cugnaux, Muret. Déplacement gratuit dans un rayon de 30 km.",
         body=ZONE_BODY,
         schema=breadcrumb([("Accueil", "index.html"), ("Zone d'intervention", None)])),

    dict(slug="contact.html",
         title="Contact & devis gratuit — plombier Toulouse | Renauva",
         desc="Contactez Renauva à Toulouse : appel direct, WhatsApp ou formulaire avec photos. Estimateur de budget en 30 secondes. Diagnostic et déplacement gratuits.",
         body=CONTACT_BODY,
         schema=breadcrumb([("Accueil", "index.html"), ("Contact", None)])),

    dict(slug="faq.html",
         title="Questions fréquentes — plombier Toulouse | Renauva",
         desc="Diagnostic gratuit, urgences 24h/24, délais, budget, zone d'intervention : toutes les réponses sur les prestations de plomberie et de rénovation Renauva à Toulouse.",
         body=FAQ_BODY,
         schema=(faq_schema(ALL_FAQ) + ",\n    "
                 + breadcrumb([("Accueil", "index.html"), ("Questions fréquentes", None)]))),

    dict(slug="mentions-legales.html", title="Mentions légales — Renauva Toulouse",
         desc="Mentions légales du site Renauva — Brahim Touati, plomberie et rénovation à Toulouse.",
         body=MENTIONS_BODY, robots="noindex, follow"),

    dict(slug="404.html", title="Page introuvable — Renauva Toulouse",
         desc="Cette page n'existe pas. Retrouvez les prestations de plomberie et de rénovation Renauva à Toulouse.",
         body=NOTFOUND_BODY, robots="noindex, follow"),

    dict(slug="confidentialite.html", title="Politique de confidentialité — Renauva Toulouse",
         desc="Politique de confidentialité et traitement des données personnelles du site Renauva, plomberie et rénovation à Toulouse.",
         body=CONF_BODY, robots="noindex, follow"),
]

SITEMAP_PRIO = {"index.html": "1.0", "plomberie.html": "0.9", "urgence.html": "0.9",
                "renovation-salle-de-bains.html": "0.8", "renovation-cuisine.html": "0.8",
                "contact.html": "0.7", "zone-intervention.html": "0.6", "faq.html": "0.5"}


def main():
    global LANG, T
    ecrites = []

    for pg in PAGES:
        kw = {k: v for k, v in pg.items() if k != "slug"}
        kw["body"] = kw["body"].replace("__TODAY__", TODAY)
        ecrites.append(render(pg["slug"], **kw))

    # sitemap
    urls = []
    for slug, prio in SITEMAP_PRIO.items():
        urls.append(
            "  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>"
            % (SITE, url(slug, "fr"), TODAY, prio))
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + "\n".join(urls) + "\n</urlset>\n")

    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)

    print("%d pages générées :" % len(ecrites))
    for w in ecrites:
        print("  ✓", w)
    print("  ✓ sitemap.xml\n  ✓ robots.txt")


if __name__ == "__main__":
    main()
