# Régénère catalogue.js, les pages de partage /produit/NNN/, sitemap.xml et robots.txt
# Usage : python3 build.py   (à relancer après avoir ajouté des photos ou changé un prix)
import json, os, html
SITE = "https://VOTRE-DOMAINE.com"   # <-- remplacer par l'adresse réelle du site (sans / final)
D = os.path.dirname(os.path.abspath(__file__))
cats = json.load(open(os.path.join(D, 'catalogue.json'), encoding='utf-8'))
open(os.path.join(D, 'catalogue.js'), 'w', encoding='utf-8').write('const CATS=' + json.dumps(cats, ensure_ascii=False, separators=(',', ':')) + ';')
fmt = lambda n: f"{n:,}".replace(',', '\u00a0') + ' F'
urls = [SITE + '/']
for c in cats:
    for s in c['subs']:
        for p in s['products']:
            for i in p['items']:
                n = f"{i['n']:03d}"
                img = f"img/produit-{n}.jpg" if os.path.exists(os.path.join(D, 'img', f"produit-{n}.jpg")) else "img/apercu-partage.jpg"
                t = p['name'] + (' — ' + i['d'] if i['d'] else '')
                title = html.escape(f"{t} — {fmt(i['p'])} | Purement Made in France")
                desc = html.escape(f"{fmt(i['p'])}. {p['desc']} Commandez sur WhatsApp.")
                url = f"{SITE}/produit/{n}"
                os.makedirs(os.path.join(D, 'produit', n), exist_ok=True)
                open(os.path.join(D, 'produit', n, 'index.html'), 'w', encoding='utf-8').write(f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<meta property="og:type" content="product"><meta property="og:site_name" content="Purement Made in France"><meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/{img}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE}/{img}">
<link rel="icon" href="/img/favicon.png"><meta name="theme-color" content="#12239E">
<script>location.replace("/#p{n}")</script></head><body><p><a href="/#p{n}">Voir {html.escape(t)}</a></p></body></html>''')
                urls.append(url)
open(os.path.join(D, 'sitemap.xml'), 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc></url>' for u in urls) + '</urlset>')
open(os.path.join(D, 'robots.txt'), 'w').write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
import re
ix=open(os.path.join(D,'index.html'),encoding='utf-8').read()
ix=re.sub(r'content="[^"]*/img/apercu-partage\.jpg"',f'content="{SITE}/img/apercu-partage.jpg"',ix)
open(os.path.join(D,'index.html'),'w',encoding='utf-8').write(ix)
print(len(urls) - 1, 'pages article générées')
