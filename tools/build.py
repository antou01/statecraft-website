#!/usr/bin/env python3
"""Build the Statecraft Institute site into site/.

Run:  python3 tools/build.py
Edit the content in content/ (or through the site editor). Photos go in media/.
"""
import glob, html, json, math, os, re, shutil
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
E = html.escape

def load(name):
    with open(os.path.join(ROOT, 'content', name), encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

def front(path):
    s = open(path, encoding='utf-8').read()
    _, fm, body = s.split('---', 2)
    return yaml.safe_load(fm) or {}, body.strip()

def md(body):
    out = []
    for b in [b.strip() for b in body.split('\n\n') if b.strip()]:
        if re.match(r'^[*-] ', b):
            out.append('<ul>' + ''.join(f'<li>{E(l[2:].strip())}</li>' for l in b.split('\n') if l.strip()) + '</ul>')
        else:
            out.append(f'<p>{E(b)}</p>')
    return '\n'.join(out)

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# ---------------------------------------------------------------- assets
def slug_of(path):
    return os.path.splitext(os.path.basename(path))[0]

def photos(path, widths, square=False):
    """Resize a photo from media/ into site/assets/photos as WebP (no metadata). Returns the slug."""
    from PIL import Image, ImageOps
    src = os.path.join(ROOT, path); s = slug_of(path)
    out = os.path.join(SITE, 'assets/photos'); os.makedirs(out, exist_ok=True)
    targets = [os.path.join(out, f'{s}-{w}.webp') for w in widths]
    if all(os.path.exists(t) and os.path.getmtime(t) >= os.path.getmtime(src) for t in targets):
        return s
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    if square:
        side = min(im.size); im = ImageOps.fit(im, (side, side), centering=(0.5, 0.35))
    for w, t in zip(widths, targets):
        c = im.copy(); c.thumbnail((w, w * 2)); c.save(t, 'WEBP', quality=72, method=6)
    return s

def copy_art():
    out = os.path.join(SITE, 'assets/art'); os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(ROOT, 'media/art/*.svg')):
        shutil.copy2(f, out)

ART_AR = {}
def art(path, label, p, style=''):
    name = slug_of(path)
    if name not in ART_AR:
        m = re.search(r'viewBox="([^"]+)"', open(os.path.join(ROOT, 'media/art', name + '.svg')).read(500))
        _, _, w, h = map(float, m.group(1).split()); ART_AR[name] = w / h
    url = f'{p}assets/art/{name}.svg'
    role = f'role="img" aria-label="{E(label)}"' if label else 'aria-hidden="true"'
    return f'<div class="art" {role} style="-webkit-mask-image:url({url});mask-image:url({url});--ar:{ART_AR[name]:.3f};{style}"></div>'

# ---------------------------------------------------------------- shared parts
ABOUT = [('Who we are', 'about/who-we-are.html'), ('Board of Advisers', 'about/board-of-advisers.html'),
         ('International Advisers', 'about/international-advisers.html'), ('Allies', 'about/allies.html'), ('Team', 'about/team.html')]
TOP = [('Our work', 'index.html#work'), ('Field Diaries', 'field-diaries.html'), ('Articles', 'index.html#articles'), ('Events', 'events.html')]

def lockup(p, which):
    if which == 'header':
        return (f'<img class="logo-light" src="{p}assets/logo/lockup-white.svg" alt="Statecraft Institute for Climate and Development Policy" width="300" height="76">'
                f'<img class="logo-dark" src="{p}assets/logo/lockup-dark.svg" alt="Statecraft Institute for Climate and Development Policy" width="300" height="76">')
    return (f'<img class="logo-light" src="{p}assets/logo/lockup-purple.svg" alt="Statecraft Institute for Climate and Development Policy" width="600" height="152">'
            f'<img class="logo-dark" src="{p}assets/logo/lockup-dark.svg" alt="Statecraft Institute for Climate and Development Policy" width="600" height="152">')

def head(title, desc, p):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#812f8e" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#141215" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{p}assets/logo/emblem-purple.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,400;0,600;0,700;0,800;1,600&display=swap">
<link rel="stylesheet" href="{p}assets/site.css">
</head>
<body>
<div class="weave" aria-hidden="true"></div><div class="weave-glow" aria-hidden="true"></div>
'''

def header(p, current):
    sub = ''.join(f'<li><a href="{p}{h}"{" aria-current=\"page\"" if n == current else ""}>{n}</a></li>' for n, h in ABOUT)
    top = ''.join(f'<li><a href="{p}{h}"{" aria-current=\"page\"" if n == current else ""}>{n}</a></li>' for n, h in TOP)
    return f'''<header class="site"><div class="wrap bar">
<a class="mini" href="{p}index.html" aria-label="Statecraft Institute, home">{lockup(p, "header")}</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="main" id="nav" aria-label="Main"><ul>
<li class="drop"><button class="sub" type="button" aria-expanded="false">About SICDP <span class="caret" aria-hidden="true"></span></button><ul>{sub}</ul></li>
{top}
<li class="menu-only"><button class="theme-btn" type="button">Dark mode</button></li>
</ul></nav>
<button class="theme-btn" type="button">Dark mode</button>
</div></header>
'''

def masthead(p, title=None, eyebrow=None):
    t = f'<h1 class="page-title">{E(title)}</h1>' if title else ''
    e = f'<p class="label eyebrow" style="margin-top:22px">{E(eyebrow)}</p>' if eyebrow else ''
    return f'<div class="masthead"><div class="wrap"><a class="lockup" href="{p}index.html" aria-label="Statecraft Institute, home">{lockup(p, "big")}</a>{e}{t}</div></div>'

def crest():
    d = 'M0 40' + ''.join(f' Q {x+60} {14 if (x//120)%2==0 else 34} {x+120} 24' for x in range(0, 1440, 120))
    top = 'M0 24' + ''.join(f' Q {x+60} {8 if (x//120)%2==0 else 40} {x+120} 24' for x in range(0, 1440, 120))
    return (f'<svg class="crest" viewBox="0 0 1440 48" preserveAspectRatio="none" aria-hidden="true">'
            f'<path class="fill" d="{top} V48 H0 Z"/><path class="stitch" d="{top}"/></svg>')

def footer(p):
    svg = {
      'mail': '<path d="M3 6h18v12H3z"/><path d="M3 7l9 6 9-6"/>',
      'phone': '<path d="M6 3h4l2 5-3 2a11 11 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 4 5a2 2 0 0 1 2-2z"/>',
      'facebook': '<path d="M14 21v-8h3l.5-3.5H14V7.5c0-1 .4-1.7 1.8-1.7h1.8V2.7A20 20 0 0 0 15 2.5c-2.6 0-4.3 1.6-4.3 4.5v2.5H8V13h2.7v8"/>',
      'instagram': '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".8"/>',
    }
    def li(key, col, text, label):
        return f'<li><span class="ic" style="--c:{col}"><svg viewBox="0 0 24 24" role="img" aria-label="{label}">{svg[key]}</svg></span><span class="copy">{E(text)}</span></li>'
    contact = li('mail', 'var(--coral)', 'thestatecraftinstitute@gmail.com', 'Email') + li('phone', 'var(--teal)', '+880 1812-267679', 'Phone')
    follow = li('facebook', 'var(--blue)', 'The Statecraft Institute', 'Facebook') + li('instagram', 'var(--saffron)', 'sicdp', 'Instagram')
    return f'''<footer class="site">{crest()}<div class="body">
<div class="wrap cols">
<div><img class="lock" src="{p}assets/logo/lockup-dark.svg" alt="Statecraft Institute for Climate and Development Policy" width="230" height="58">
<p class="motto" style="margin-top:14px">Instituta Firma, Res Publica Firma</p></div>
<div><h2>Contact</h2><ul class="contact">{contact}</ul></div>
<div><h2>Follow</h2><ul class="contact">{follow}</ul></div>
</div>
<div class="wrap fine">An independent, youth-led think tank in Bangladesh · Founded 8 June 2026 · sicdp.xyz</div>
</div></footer>
<script src="{p}assets/site.js" defer></script>
</body>
</html>
'''

def page(path, title, desc, current, body, p, mast_title=None, eyebrow=None):
    html_ = head(title, desc, p) + header(p, current) + masthead(p, mast_title, eyebrow) + '<main>' + body + '</main>' + footer(p)
    full = os.path.join(SITE, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(html_)

def photo_fig(item, p, link=None, viewer=False):
    s = photos(item['photo'], [480, 960, 1600])
    meta = f'{item["place"]} · {item["date"]}'
    img = (f'<div class="frame"><img src="{p}assets/photos/{s}-960.webp" srcset="{p}assets/photos/{s}-480.webp 480w, {p}assets/photos/{s}-960.webp 960w" '
           f'sizes="(max-width: 480px) 100vw, (max-width: 860px) 50vw, 380px" alt="{E(item["caption"])}" loading="lazy" decoding="async" width="960" height="720"></div>')
    cap = f'<figcaption>{E(item["caption"])}<span>{E(meta)}</span></figcaption>'
    if viewer:
        return (f'<figure><button type="button" data-full="{p}assets/photos/{s}-1600.webp" data-alt="{E(item["caption"])}" data-meta="{E(meta)}" '
                f'aria-label="Open photo: {E(item["caption"])}">{img}</button>{cap}</figure>')
    return f'<figure><a href="{link}">{img}</a>{cap}</figure>'

def articles():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'content/articles/*.md'))):
        meta, body = front(f)
        y, m = str(meta['written']).split('-')[:2]
        meta['when'] = f'Written {MONTHS[int(m)-1]} {y}'; meta['slug'] = slug_of(f); meta['body'] = body
        meta['first'] = re.split(r'(?<=[.?!])\s', body.split('\n\n')[0])[0]
        out.append(meta)
    return sorted(out, key=lambda a: str(a['written']), reverse=True)

def events():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'content/events/*.md'))):
        meta, body = front(f); meta['body'] = body; out.append(meta)
    return sorted(out, key=lambda e: str(e['date']), reverse=True)

def nice_date(d):
    d = str(d); y, m, dd = d.split('-'); return f'{int(dd)} {MONTHS[int(m)-1]} {y}'

# ---------------------------------------------------------------- home
def home():
    p = ''; H = load('home.yml'); F = load('field-diaries.yml')
    heroes = ''
    for k, h in enumerate(H['heroes']):
        s = photos(h['photo'], [768, 1280, 1920]); cap = f'{h["caption"]} · {h["place"]} · {h["date"]}'
        heroes += (f'<img class="{"show" if k == 0 else ""}" src="assets/photos/{s}-1280.webp" srcset="assets/photos/{s}-768.webp 768w, assets/photos/{s}-1280.webp 1280w, assets/photos/{s}-1920.webp 1920w" '
                   f'sizes="(max-width: 860px) 100vw, 600px" alt="{E(h["caption"])}" data-caption="{E(cap)}" width="1280" height="960" {"fetchpriority=high" if k == 0 else "loading=lazy"}>')
    first = H['heroes'][0]
    grid = ''.join(photo_fig(i, p, 'field-diaries.html') for i in F['photos'] if i.get('home'))
    arts = ''.join(f'<a class="article-card" href="articles/{a["slug"]}.html"><div class="thumb">{art(a["thumbnail"], "", p)}</div>'
                   f'<h3>{E(a["title"])}</h3><p>{E(a["first"])}</p><span class="label">{E(a["author"])} · {E(a["when"])}</span></a>' for a in articles())
    hazards = ''.join(f'<figure>{art("media/art/"+n+".svg", l, p)}<figcaption>{l}</figcaption></figure>' for n, l in
                      [('hazard-salinity', 'Coastal salinity'), ('hazard-erosion', 'Riverine erosion'), ('hazard-drought', 'Drought'), ('hazard-haor', 'Haor flash floods')])
    steps = ''.join(f'<li>{art("media/art/"+n+".svg", "", p)}<span>{l}</span></li>' for n, l in
                    [('lab-intake', 'Intake'), ('lab-casework', 'Active case work'), ('lab-review', 'After-action review'), ('lab-dispatch', 'Published dispatch')])
    coming = ''.join(f'<li><strong>{E(c["title"])}</strong><span class="label">{E(c["label"])}</span></li>' for c in H['coming_up'])
    rays = ''.join(f'<path class="s ray" style="--i:{i}" d="M{300+44*math.cos(math.radians(a)):.1f} {150-44*math.sin(math.radians(a)):.1f} L{300+60*math.cos(math.radians(a)):.1f} {150-60*math.sin(math.radians(a)):.1f}"/>'
                   for i, a in enumerate((15, 45, 70, 90, 110, 135, 165)))
    skyline = f'''<svg class="skyline" viewBox="0 0 600 190" role="img" aria-label="A small house with solar panels, a wind turbine and a building under a rising sun">
<defs><clipPath id="horizon"><rect x="0" y="0" width="600" height="150"/></clipPath></defs>
<g clip-path="url(#horizon)"><g class="sun"><circle class="s" cx="300" cy="150" r="34"/>{rays}</g></g>
<path class="s" d="M10 150 H590"/><path class="s d" d="M30 168 Q 120 160 210 168 T 390 168 T 570 168"/>
<g transform="translate(80 0)"><path class="s" d="M0 150 V112 L28 92 L56 112 V150"/><path class="s d" d="M10 104 L28 94 L46 104"/><path class="s" d="M20 150 V130 H34 V150"/></g>
<g transform="translate(205 0)"><path class="s" d="M30 150 L33 74 L36 150"/><g class="blades"><path class="s" d="M33 74 L33 40"/><path class="s" d="M33 74 L62 91"/><path class="s" d="M33 74 L4 91"/><circle class="s" cx="33" cy="74" r="3"/></g></g>
<g transform="translate(420 0)"><path class="s" d="M0 150 V78 H46 V150"/><path class="s d" d="M10 92 H36 M10 106 H36 M10 120 H36 M10 134 H36"/></g>
<g transform="translate(520 0)"><circle class="s" cx="14" cy="122" r="13"/><path class="s" d="M14 135 V150"/></g>
<g transform="translate(20 0)"><circle class="s" cx="14" cy="126" r="10"/><path class="s" d="M14 136 V150"/></g></svg>'''
    body = f'''
<section class="wrap" aria-label="Introduction"><div class="hero">
<div><p class="label eyebrow">{E(H["eyebrow"])}</p><p class="motto">{E(H["motto"])}</p><p class="lede">{E(H["lede"])}</p>
<div class="cta"><a class="btn solid" href="#work">Our work</a><a class="btn" href="field-diaries.html">Field Diaries</a></div></div>
<figure class="slides"><div class="holder"><div class="stage" data-seconds="{H.get("hero_seconds", 3)}">{heroes}</div></div>
<figcaption>{E(first["caption"])} · {E(first["place"])} · {E(first["date"])}</figcaption></figure>
</div></section>

<section class="band on-dark" id="about" style="margin-top:clamp(40px,6vw,72px)"><div class="wrap split">
<div><h2>Who we are</h2><p class="intro" style="margin-top:18px">SICDP is an independent, youth-led think tank based in Dhaka, Bangladesh. We work at the intersection of climate governance and state capacity in South Asia.</p>
<p>We study why climate and digital governance fall short in practice, and we ground our answers in field evidence and institutional analysis.</p>
<div class="cta"><a class="btn" href="about/who-we-are.html">More about SICDP</a></div></div>
<div class="focus">
<div class="card saffron">{art("media/art/hazard-haor.svg", "", p)}<div><h3>Climate governance</h3><p>How plans for salinity, erosion, drought and floods hold up where people live with them.</p></div></div>
<div class="card teal">{art("media/art/stitch-circuit.svg", "", p)}<div><h3>Digital governance and state capacity</h3><p>Whether public institutions are ready for the technology they are asked to run.</p></div></div>
</div></div></section>

<section class="band on-lilac" id="work"><div class="wrap">
<div class="head"><h2>Our work</h2><p>Two programmes in the field now, and a paper series on the way.</p></div>
<div class="work">
<article class="programme coral"><header><h3>The C30 Agenda</h3><span class="chip">Field research</span></header>
<p>The C30 Agenda is SICDP's first major field research project. It audits where climate-related Sustainable Development Goal targets failed to deliver for climate-vulnerable communities and proposes climate priorities for the decade beyond 2030, grounded in direct field evidence from Bangladesh. Research teams work across four sites, each representing a distinct hazard: coastal salinity, riverine erosion, drought, and haor flash floods. Findings are qualitative-led, drawn from interviews and focus groups.</p>
<div class="hazards">{hazards}</div></article>
<article class="programme teal"><header><h3>The Adaptation Lab</h3><span class="chip">Applied research</span></header>
<p>The Adaptation Lab is the applied research arm of SICDP. It takes a single live case at a time and moves it through a structured cycle: intake, active case work, after-action review, and a published dispatch. A dual-wing design also supports an innovation and prototyping track. Each case must name a clear beneficiary, and the Lab documents what it learns so that practical adaptation lessons are shared openly with practitioners and policymakers.</p>
<ol class="steps">{steps}</ol></article>
<article class="programme saffron"><div class="papers">{art("media/art/papers.svg", "", p)}<div><header><h3>The Statecraft Papers</h3><span class="chip">Forthcoming</span></header>
<p>Our working paper series. Papers will be published openly here, on SSRN and on Zenodo.</p></div></div></article>
</div></div></section>

<section class="band on-blue" id="field"><div class="wrap">
<div class="head"><h2>Field Diaries</h2><p>{E(F["dates"])}. Eleven districts from Bagerhat to Mymensingh.</p></div>
<div class="photos">{grid}</div>
<p class="cta"><a class="btn" style="color:#fff;border-color:#fff" href="field-diaries.html">See the route and all photos</a></p>
</div></section>

<section class="band" id="articles"><div class="wrap">
<div class="head"><h2>Articles</h2><p class="muted">Short pieces by SICDP members. Views are the authors' own.</p></div>
<div class="articles">{arts}</div>
</div></section>

<section class="band on-sun" id="coming"><div class="wrap coming">
<div><div class="head" style="margin-bottom:18px"><h2>Coming up</h2></div><ul>{coming}</ul>
<p class="cta"><a class="btn" style="color:var(--on-sun);border-color:var(--on-sun)" href="events.html">Events</a></p></div>
{skyline}
</div></section>
'''
    page('index.html', 'Statecraft Institute', 'Statecraft Institute for Climate and Development Policy (SICDP): an independent, youth-led think tank in Bangladesh working on climate governance and state capacity in South Asia.', '', body, p)

# ---------------------------------------------------------------- field diaries
ROUTE = ['Dhaka', 'Bagerhat', 'Khulna', 'Jashore', 'Benapole', 'Kotchandpur', 'Islamic University', 'Shilaidaha', 'Rooppur',
         'Natore', 'RDA, Bogura', 'Sariakandi', 'Madarganj', 'Jamalpur', 'Mymensingh']
LABEL = {'Dhaka': (9, 4, 'start'), 'Bagerhat': (9, 10, 'start'), 'Khulna': (-9, 4, 'end'), 'Jashore': (9, 4, 'start'),
         'Benapole': (-9, 9, 'end'), 'Kotchandpur': (-9, 4, 'end'), 'Islamic University': (9, 4, 'start'), 'Shilaidaha': (9, 2, 'start'),
         'Rooppur': (-9, 3, 'end'), 'Natore': (-9, 4, 'end'), 'RDA, Bogura': (-9, 4, 'end'), 'Sariakandi': (-6, -9, 'end'),
         'Madarganj': (0, 17, 'middle'), 'Jamalpur': (2, -10, 'start'), 'Mymensingh': (9, 4, 'start')}
DAYS = [('21 Oct', 'Dhaka', 'Night train from Kamalapur'),
        ('22 Oct', 'Khulna, Bagerhat, Jashore', 'Khulna University, the Sixty Dome Mosque, the Bhairab riverside'),
        ('23 Oct', 'Jashore, Jhenaidah', 'Benapole border, Mobarakganj, Kotchandpur and the Baluhar baor'),
        ('24 Oct', 'Jhenaidah, Kushtia, Pabna, Natore', 'Shailkupa and Islamic University, Lalon Shah shrine, Shilaidaha, Rooppur'),
        ('25 Oct', 'Bogura', 'Rural Development Academy'),
        ('26 Oct', 'Bogura, Jamalpur', 'Sariakandi ghat, across the Jamuna to Madarganj, Jamalpur'),
        ('27–28 Oct', 'Mymensingh', 'Bangladesh Agricultural University, the Brahmaputra bank, Trishal'),
        ('29 Oct', 'Dhaka', 'Back at Kamalapur after midnight')]

def field():
    p = ''; F = load('field-diaries.yml')
    geo = json.load(open(os.path.join(ROOT, 'tools/bangladesh-outline.json')))
    x0, y0, x1, y1 = geo['bbox']; pad = 12
    vb = f'{x0-pad:.0f} {y0-pad:.0f} {x1-x0+2*pad:.0f} {y1-y0+2*pad:.0f}'
    st = geo['stops']; route = 'M' + ' L'.join(f'{st[k][0]} {st[k][1]}' for k in ROUTE)
    dots = ''.join(f'<circle class="stop" style="--k:{i}" cx="{st[k][0]}" cy="{st[k][1]}" r="4"/>' for i, k in enumerate(ROUTE))
    labels = ''.join(f'<text style="--k:{i}" x="{st[k][0]+LABEL[k][0]}" y="{st[k][1]+LABEL[k][1]}" text-anchor="{LABEL[k][2]}">{E(k)}</text>' for i, k in enumerate(ROUTE))
    mapsvg = (f'<svg class="map" viewBox="{vb}" role="img" aria-label="Map of Bangladesh with the October 2026 route from Dhaka through Bagerhat, Khulna, Jashore, Kotchandpur, Kushtia, Rooppur, Bogura and Jamalpur to Mymensingh">'
              f'<defs><mask id="routemask" maskUnits="userSpaceOnUse"><path class="reveal" pathLength="1" d="{route}"/></mask></defs>'
              f'<path class="land" d="{geo["d"]}"/><path class="route" mask="url(#routemask)" d="{route}"/>{dots}{labels}</svg>')
    days = ''.join(f'<li><span class="label">{E(d)}</span><span><strong>{E(w)}</strong><br>{E(t)}</span></li>' for d, w, t in DAYS)
    groups = ''
    for place in dict.fromkeys(i['place'] for i in F['photos']):
        figs = ''.join(photo_fig(i, p, viewer=True) for i in F['photos'] if i['place'] == place)
        groups += f'<section class="stop-group"><h2>{E(place)}</h2><div class="photos">{figs}</div></section>'
    body = f'''
<section class="wrap"><p class="label eyebrow">{E(F["dates"])}</p>
<div class="diary-top" style="margin-top:18px"><div>{mapsvg}</div>
<div><p class="lede" style="margin-top:0;max-width:44ch">{E(F["intro"])}</p><ul class="days">{days}</ul></div></div></section>
<section class="band" style="padding-top:48px"><div class="wrap">{groups}</div></section>
<dialog class="viewer" aria-label="Photo viewer"><div class="pane"><img src="" alt=""><div class="cap"></div>
<div class="nav"><button class="prev" type="button">Previous</button><button class="close" type="button">Close</button><button class="next" type="button">Next</button></div></div></dialog>
'''
    page('field-diaries.html', 'Field Diaries · Statecraft Institute', "Photos and route from SICDP's October 2026 field trip across eleven districts of Bangladesh.", 'Field Diaries', body, p, 'Field Diaries')

# ---------------------------------------------------------------- articles
def article_pages():
    p = '../'
    for a in articles():
        body = f'''<article class="op wrap"><p class="label"><a href="{p}index.html#articles">Articles</a></p>
<h1 style="margin-top:12px;font-size:clamp(2rem,4.6vw,3rem);color:var(--ink-deep)">{E(a["title"])}</h1>
<p class="by label">{E(a["author"])} · {E(a["when"])}</p>
<div class="thumb">{art(a["thumbnail"], "", p)}</div>
<div class="body">{md(a["body"])}</div>
<p class="disclaimer">Views are the author's own and do not necessarily reflect those of SICDP. Sources will be added.</p></article>'''
        page(f'articles/{a["slug"]}.html', a['title'] + ' · Statecraft Institute', f'{a["title"]}, an article by {a["author"]}.', 'Articles', body, p)

# ---------------------------------------------------------------- events
def events_page():
    p = ''; items = ''
    for ev in events():
        ph = ''
        if ev.get('photo'):
            s = photos(ev['photo'], [480, 960]); ph = f'<img src="assets/photos/{s}-960.webp" alt="{E(ev["title"])}" style="border-radius:14px;aspect-ratio:4/3;object-fit:cover;width:100%">'
        else:
            ph = '<div class="photo-slot">Photo from the event will go here</div>'
        note = f'<p class="placeholder" style="margin-top:14px">{E(ev["body"])}</p>' if ev['body'].startswith('PREVIEW NOTE') else md(ev['body'])
        items += f'''<article class="event"><div><p class="label when">{nice_date(ev["date"])} · {E(ev["place"])}</p>
<h2 style="margin-top:10px;font-size:clamp(1.5rem,3vw,2.1rem);color:var(--ink-deep)">{E(ev["title"])}</h2>
<p style="margin-top:12px">{E(ev["summary"])}</p><p class="muted" style="margin-top:10px">Convened by {E(ev["convened_by"])}</p>{note}</div>{ph}</article>'''
    body = f'<section class="band" style="padding-top:28px"><div class="wrap" style="display:grid;gap:22px">{items}</div></section>'
    page('events.html', 'Events · Statecraft Institute', 'Events SICDP has organised or taken part in.', 'Events', body, p, 'Events')

# ---------------------------------------------------------------- about pages
def about_pages():
    p = '../'; A = load('advisers.yml'); L = load('allies.yml')
    who = f'''<section class="band" style="padding-top:28px"><div class="wrap prose">
<p class="intro">SICDP is an independent, youth-led think tank based in Dhaka, Bangladesh. We work at the intersection of climate governance and state capacity in South Asia.</p>
<p>We study why climate and digital governance fall short in practice, and we ground our answers in field evidence and institutional analysis.</p>
<h2 style="margin-top:36px">Our motto</h2><p><em>Instituta Firma, Res Publica Firma.</em></p>
<h2 style="margin-top:36px">Our story</h2><p class="placeholder">Placeholder: a short story of how SICDP started on 8 June 2026 will go here.</p>
<h2 style="margin-top:36px">How we work</h2><p class="placeholder">Placeholder: how we choose research questions, work in the field and publish openly.</p>
</div></section>'''
    page('about/who-we-are.html', 'Who we are · Statecraft Institute', 'Who SICDP is and what it does.', 'Who we are', who, p, 'Who we are')

    def seats(lst):
        out = ''
        for s in lst:
            if s.get('name'):
                ph = photos(s['photo'], [400, 800], square=True) if s.get('photo') else None
                img = f'<img src="{p}assets/photos/{ph}-400.webp" alt="{E(s["name"])}" style="width:120px;height:120px;border-radius:50%;margin:0 auto 14px;object-fit:cover">' if ph else art('media/art/seat.svg', '', p)
                out += f'<div class="seat">{img}<h3>{E(s["name"])}</h3><p>{E(s.get("role", ""))}</p><p class="label" style="margin-top:8px">{E(s["seat"])}</p></div>'
            else:
                out += f'<div class="seat">{art("media/art/seat.svg", "", p)}<h3>{E(s["seat"])}</h3><p>Seat open</p></div>'
        return out
    intro = '<p class="muted" style="max-width:60ch;margin-bottom:26px">We are forming our advisory board. Each seat stays open until the right person agrees to join.</p>'
    page('about/board-of-advisers.html', 'Board of Advisers · Statecraft Institute', 'SICDP Board of Advisers.', 'Board of Advisers',
         f'<section class="band" style="padding-top:28px"><div class="wrap">{intro}<div class="people">{seats(A["board"])}</div></div></section>', p, 'Board of Advisers')
    page('about/international-advisers.html', 'International Advisers · Statecraft Institute', 'SICDP International Advisers.', 'International Advisers',
         f'<section class="band" style="padding-top:28px"><div class="wrap">{intro}<div class="people">{seats(A["international"])}</div></div></section>', p, 'International Advisers')

    slots = ''.join(f'<div class="slot">{E(a["name"])}</div>' for a in L.get('allies') or [])
    slots += ''.join('<div class="slot">Partner to be announced</div>' for _ in range(int(L.get('open_slots', 0))))
    page('about/allies.html', 'Allies · Statecraft Institute', 'Organisations SICDP works with.', 'Allies',
         f'<section class="band" style="padding-top:28px"><div class="wrap"><p class="intro" style="margin-bottom:28px">{E(L["intro"])}</p><div class="people">{slots}</div></div></section>', p, 'Allies')

    members = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'content/team/*.md'))):
        if f.endswith('README.md'): continue
        meta, about = front(f); meta['about'] = about
        if meta.get('consent'): members.append(meta)
    if members:
        cards = ''
        for m in sorted(members, key=lambda m: (str(m.get('division', '')), m.get('order', 99))):
            ph = photos(m['photo'], [400, 800], square=True) if m.get('photo') else None
            img = f'<img src="{p}assets/photos/{ph}-400.webp" alt="{E(m["name"])}" style="width:120px;height:120px;border-radius:50%;margin:0 auto 14px;object-fit:cover">' if ph else art('media/art/seat.svg', '', p)
            cards += f'<div class="seat">{img}<h3>{E(m["name"])}</h3><p>{E(m.get("role", ""))}</p><p class="label" style="margin-top:8px">{E(m.get("division", ""))}</p></div>'
    else:
        cards = ''.join(f'<div class="seat">{art("media/art/seat.svg", "", p)}<h3>Profile in preparation</h3><p>Team member</p></div>' for _ in range(4))
    team = f'''<section class="band" style="padding-top:28px"><div class="wrap">
<h2 style="font-size:1.6rem">How SICDP is organised</h2><p class="placeholder" style="margin:14px 0 36px">Placeholder: the organisational structure chart will go here.</p>
<div class="people">{cards}</div></div></section>'''
    page('about/team.html', 'Team · Statecraft Institute', 'The people of SICDP.', 'Team', team, p, 'Team')

if __name__ == '__main__':
    copy_art(); home(); field(); article_pages(); events_page(); about_pages(); print('built')
