#!/usr/bin/env python3
"""Build the Statecraft Institute site into site/.

Run:  python3 tools/build.py
Content lives in content/ (write-ups) and in the lists below (photos, captions).
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
E = html.escape

# ---------------------------------------------------------------- content
HEROES = [
    ('hero-jamuna-buffaloes', 'Buffaloes on a char in the Jamuna', 'Sariakandi, Bogura · 26 October 2026'),
    ('hero-kotchandpur-burning', 'Waste burning beside homes and farmland', 'Kotchandpur, Jhenaidah · 23 October 2026'),
    ('hero-bau-paddy', 'Paddy fields and power lines', 'Bangladesh Agricultural University, Mymensingh · October 2026'),
    ('hero-sariakandi-boats', 'Boats moored at the Jamuna ghat', 'Sariakandi, Bogura · 26 October 2026'),
    ('hero-rda-palms', 'An egret takes off on a road lined with betel-nut palms', 'Rural Development Academy, Bogura · October 2026'),
]
# stop key, photo slug, caption, date
FIELD = [
    ('Kotchandpur', 'kotchandpur-tea-stall', 'A roadside tea stall', '23 Oct'),
    ('Islamic University', 'iu-village-interview', 'Recording an interview in a village', '24 Oct'),
    ('Islamic University', 'iu-tea-stall', 'Tea and talk at a village stall', '24 Oct'),
    ('Islamic University', 'iu-buffalo-cart', 'A buffalo cart on a village road', '24 Oct'),
    ('Shilaidaha', 'shilaidaha-fields', 'The team in the paddy fields', '24 Oct'),
    ('Rooppur', 'rooppur', 'Rooppur at dusk, seen from the road', '24 Oct'),
    ('RDA, Bogura', 'rda-working-session', 'An evening working session', '25 Oct'),
    ('Sariakandi', 'sariakandi-ghat-boat', 'A boat at the ghat', '26 Oct'),
    ('Sariakandi', 'jamuna-crossing', 'Crossing the Jamuna by boat', '26 Oct'),
    ('Sariakandi', 'jamuna-boat-ride', 'On the Jamuna crossing', '26 Oct'),
    ('Sariakandi', 'jamuna-sandbar', 'People on a sandbar mid-river', '26 Oct'),
    ('Sariakandi', 'jamuna-char', 'A low char on the Jamuna', '26 Oct'),
    ('Madarganj', 'madarganj-elephant', 'An elephant on the road', '26 Oct'),
    ('Madarganj', 'madarganj-van', 'A battery van on the Madarganj road', '26 Oct'),
    ('Mymensingh', 'mymensingh-village-night', 'A village home at night', '27 Oct'),
]
HOME_FIELD = ['kotchandpur-tea-stall', 'iu-village-interview', 'shilaidaha-fields', 'rooppur', 'rda-working-session', 'jamuna-crossing']
PLACE = {  # stop key -> public place name, district
    'Kotchandpur': 'Kotchandpur, Jhenaidah', 'Islamic University': 'Near Islamic University, Kushtia',
    'Shilaidaha': 'Shilaidaha, Kushtia', 'Rooppur': 'Rooppur, Ishwardi, Pabna', 'RDA, Bogura': 'Rural Development Academy, Bogura',
    'Sariakandi': 'Jamuna river, Sariakandi, Bogura', 'Madarganj': 'Madarganj, Jamalpur', 'Mymensingh': 'Near Bangladesh Agricultural University, Mymensingh',
}
ROUTE = ['Dhaka', 'Bagerhat', 'Khulna', 'Jashore', 'Benapole', 'Kotchandpur', 'Islamic University', 'Shilaidaha', 'Rooppur',
         'Natore', 'RDA, Bogura', 'Sariakandi', 'Madarganj', 'Jamalpur', 'Mymensingh']
LABEL = {  # dx, dy, anchor
    'Dhaka': (9, 4, 'start'), 'Bagerhat': (9, 10, 'start'), 'Khulna': (-9, 4, 'end'), 'Jashore': (9, 4, 'start'),
    'Benapole': (-9, 9, 'end'), 'Kotchandpur': (-9, 4, 'end'), 'Islamic University': (9, 4, 'start'), 'Shilaidaha': (9, 2, 'start'),
    'Rooppur': (-9, 3, 'end'), 'Natore': (-9, 4, 'end'), 'RDA, Bogura': (-9, 4, 'end'), 'Sariakandi': (-6, -9, 'end'),
    'Madarganj': (0, 17, 'middle'), 'Jamalpur': (2, -10, 'start'), 'Mymensingh': (9, 4, 'start'),
}
DAYS = [
    ('21 Oct', 'Dhaka', 'Night train from Kamalapur'),
    ('22 Oct', 'Khulna, Bagerhat, Jashore', 'Khulna University, the Sixty Dome Mosque, the Bhairab riverside'),
    ('23 Oct', 'Jashore, Jhenaidah', 'Benapole border, Mobarakganj, Kotchandpur and the Baluhar baor'),
    ('24 Oct', 'Kushtia, Pabna, Natore', 'Islamic University, Lalon Shah shrine, Shilaidaha, Rooppur'),
    ('25 Oct', 'Bogura', 'Rural Development Academy'),
    ('26 Oct', 'Bogura, Jamalpur', 'Sariakandi ghat, across the Jamuna to Madarganj, Jamalpur'),
    ('27–28 Oct', 'Mymensingh', 'Bangladesh Agricultural University, the Brahmaputra bank, Trishal'),
    ('29 Oct', 'Dhaka', 'Back at Kamalapur after midnight'),
]
WRITEUPS = [
    ('is-bangladesh-ready-to-automate', 'thumb-automate', 'A traffic light with an AI camera, a motorbike and an auto-rickshaw at a Dhaka intersection'),
    ('tarl', 'thumb-tarl', 'Children in a small group learning with flashcards'),
    ('never-skilling', 'thumb-neverskilling', 'A thread running from a pencil towards a laptop, cut halfway'),
]
MONTHS = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July',
          '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

# ---------------------------------------------------------------- helpers
ART_VB = {}
for f in os.listdir(os.path.join(SITE, 'assets/art')):
    if f.endswith('.svg') and f != 'weave.svg':
        s = open(os.path.join(SITE, 'assets/art', f)).read(400)
        m = re.search(r'viewBox="([^"]+)"', s)
        if m:
            _, _, w, h = map(float, m.group(1).split()); ART_VB[f[:-4]] = w / h

def art(name, label, p, extra=''):
    url = f'{p}assets/art/{name}.svg'
    role = f'role="img" aria-label="{E(label)}"' if label else 'aria-hidden="true"'
    return (f'<div class="art {extra}" {role} style="-webkit-mask-image:url({url});mask-image:url({url});'
            f'--ar:{ART_VB.get(name, 1):.3f}"></div>')

def seam(cls=''):
    d = 'M0 12' + ''.join(f' Q {x+50} {2 if (x//100)%2==0 else 22} {x+100} 12' for x in range(0, 1200, 100))
    return f'<svg class="seam sew {cls}" viewBox="0 0 1200 24" preserveAspectRatio="none" aria-hidden="true"><path d="{d}"/></svg>'

def head(title, desc, p):
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#812f8e" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#141215" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{p}assets/logo/emblem-purple.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&family=Oswald:wght@500&family=Source+Sans+3:wght@400;600&display=swap">
<link rel="stylesheet" href="{p}assets/site.css">
</head>
<body>
<div class="weave" aria-hidden="true"></div>
'''

def header(p, current):
    items = [('About', f'{p}index.html#about'), ('Our work', f'{p}index.html#work'), ('Field Diaries', f'{p}field-diaries.html'),
             ('Write-ups', f'{p}index.html#writeups'), ('Team', f'{p}index.html#team')]
    lis = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if n == current else ""}>{n}</a></li>' for n, h in items)
    return f'''<header class="site"><div class="wrap bar">
<a class="brand" href="{p}index.html" aria-label="Statecraft Institute, home">
<picture><source srcset="{p}assets/logo/emblem-color.svg" media="(prefers-color-scheme: dark)"><img src="{p}assets/logo/emblem-white.svg" alt="" width="46" height="46"></picture>
<span class="wordmark">Statecraft Institute<small>for Climate and Development Policy</small></span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="main" id="nav" aria-label="Main"><ul>{lis}</ul></nav>
</div></header>
'''

def footer(p):
    return f'''<footer class="site">
{seam()}
<div class="wrap cols">
<div><a class="brand" href="{p}index.html"><picture><source srcset="{p}assets/logo/emblem-color.svg" media="(prefers-color-scheme: dark)"><img src="{p}assets/logo/emblem-white.svg" alt="" width="46" height="46"></picture>
<span class="wordmark">Statecraft Institute<small>for Climate and Development Policy</small></span></a>
<p class="motto">Instituta Firma, Res Publica Firma</p></div>
<div><h2>Contact</h2><p class="copy">thestatecraftinstitute@gmail.com</p><p class="copy">+880 1812-267679</p><p>Dhaka, Bangladesh</p></div>
<div><h2>Follow</h2><p>Facebook: The Statecraft Institute</p><p>Instagram: sicdp</p></div>
</div>
<div class="wrap fine">An independent, youth-led think tank · Founded 8 June 2026 · sicdp.xyz</div>
</footer>
<script src="{p}assets/site.js" defer></script>
</body>
</html>
'''

def photo(slug, caption, meta, p, sizes='(max-width: 480px) 100vw, (max-width: 860px) 50vw, 360px'):
    return (f'<figure><div class="frame"><img src="{p}assets/photos/{slug}-960.webp" '
            f'srcset="{p}assets/photos/{slug}-480.webp 480w, {p}assets/photos/{slug}-960.webp 960w" sizes="{sizes}" '
            f'alt="{E(caption)}" loading="lazy" decoding="async" width="960" height="720"></div>'
            f'<figcaption>{E(caption)}<span class="label">{E(meta)}</span></figcaption></figure>')

def read_writeup(slug):
    s = open(os.path.join(ROOT, 'content/write-ups', slug + '.md'), encoding='utf-8').read()
    fm, body = s.split('---', 2)[1:]
    meta = dict(re.findall(r'^(\w+):\s*"(.*)"\s*$', fm, re.M))
    y, m = meta['written'].split('-')
    meta['when'] = f'Written {MONTHS[m]} {y}'
    blocks = [b.strip() for b in body.strip().split('\n\n') if b.strip()]
    out = []
    for b in blocks:
        if b.startswith('* '):
            out.append('<ul>' + ''.join(f'<li>{E(l[2:].strip())}</li>' for l in b.split('\n') if l.strip()) + '</ul>')
        else:
            out.append(f'<p>{E(b)}</p>')
    first = re.split(r'(?<=[.?!])\s', blocks[0])[0]
    return meta, '\n'.join(out), first

def write(path, text):
    full = os.path.join(SITE, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(text)

# ---------------------------------------------------------------- home
def home():
    p = ''
    h0 = HEROES[0]
    heroes = json.dumps([{'slug': s, 'alt': a, 'caption': f'{a} · {c}'} for s, a, c in HEROES])
    byslug = {f[1]: f for f in FIELD}
    grid = ''.join(photo(s, byslug[s][2], f'{PLACE[byslug[s][0]]} · {byslug[s][3]} 2026', p) for s in HOME_FIELD)
    wu = ''
    for slug, thumb, alt in WRITEUPS:
        meta, _, first = read_writeup(slug)
        wu += (f'<a class="writeup stitched" href="write-ups/{slug}.html"><div class="thumb">{art(thumb, alt, p)}</div>'
               f'<h3>{E(meta["title"])}</h3><p>{E(first)}</p><span class="label">{E(meta["author"])} · {E(meta["when"])}</span></a>')
    hazards = ''.join(f'<figure>{art(n, l, p)}<figcaption>{l}</figcaption></figure>' for n, l in
                      [('hazard-salinity', 'Coastal salinity'), ('hazard-erosion', 'Riverine erosion'), ('hazard-drought', 'Drought'), ('hazard-haor', 'Haor flash floods')])
    steps = ''.join(f'<li>{art(n, "", p)}<span>{l}</span></li>' for n, l in
                    [('lab-intake', 'Intake'), ('lab-casework', 'Active case work'), ('lab-review', 'After-action review'), ('lab-dispatch', 'Published dispatch')])
    seats = ''.join(f'<div class="seat stitched open">{art("seat", "", p)}<h3>{t}</h3><p>Seat open</p></div>' for t in
                    ['Climate &amp; Disaster Governance', 'Rural Development &amp; Char Lands', 'Public Administration &amp; Digital Governance', 'Foreign Adviser'])
    team = ''.join(f'<div class="seat stitched open">{art("seat", "", p)}<h3>Profile in preparation</h3><p>Team member</p></div>' for _ in range(4))
    rays = ''.join(f'<path class="s ray" style="--i:{i}" d="M{300+44*__import__("math").cos(a):.1f} {150-44*__import__("math").sin(a):.1f} L{300+60*__import__("math").cos(a):.1f} {150-60*__import__("math").sin(a):.1f}"/>'
                   for i, a in enumerate([__import__('math').radians(d) for d in (15, 45, 70, 90, 110, 135, 165)]))
    skyline = f'''<svg class="skyline decor" viewBox="0 0 600 190" role="img" aria-label="A small house with solar panels, a wind turbine and a building under a rising sun">
<defs><clipPath id="horizon"><rect x="0" y="0" width="600" height="150"/></clipPath></defs>
<g clip-path="url(#horizon)"><g class="sun"><circle class="s" cx="300" cy="150" r="34"/>{rays}</g></g>
<path class="s" d="M10 150 H590"/>
<path class="s d" d="M30 168 Q 120 160 210 168 T 390 168 T 570 168"/>
<g transform="translate(80 0)"><path class="s" d="M0 150 V112 L28 92 L56 112 V150"/><path class="s" d="M6 108 L28 92 L50 108"/><path class="s d" d="M10 104 L28 94 L46 104"/><path class="s" d="M20 150 V130 H34 V150"/></g>
<g transform="translate(205 0)"><path class="s" d="M30 150 L33 74 L36 150"/><g class="blades"><path class="s" d="M33 74 L33 40"/><path class="s" d="M33 74 L62 91"/><path class="s" d="M33 74 L4 91"/><circle class="s" cx="33" cy="74" r="3"/></g></g>
<g transform="translate(420 0)"><path class="s" d="M0 150 V78 H46 V150"/><path class="s d" d="M10 92 H36 M10 106 H36 M10 120 H36 M10 134 H36"/></g>
<g transform="translate(520 0)"><circle class="s" cx="14" cy="122" r="13"/><path class="s" d="M14 135 V150"/></g>
<g transform="translate(20 0)"><circle class="s" cx="14" cy="126" r="10"/><path class="s" d="M14 136 V150"/></g>
</svg>'''
    body = f'''{head("Statecraft Institute", "Statecraft Institute for Climate and Development Policy (SICDP): an independent, youth-led think tank in Dhaka working on climate governance and state capacity in South Asia.", p)}{header(p, "")}
<main>
<section class="hero"><div class="wrap grid">
<div>
<p class="label">Independent · Youth-led · Dhaka, Bangladesh</p>
<h1 style="margin-top:14px">Statecraft Institute<span>for Climate and Development Policy</span></h1>
<p class="motto">Instituta Firma, Res Publica Firma</p>
<p class="lede">We work at the intersection of climate governance and state capacity in South Asia.</p>
<div class="cta"><a class="btn solid" href="#work">Our work</a><a class="btn" href="field-diaries.html">Field Diaries</a></div>
</div>
<figure class="stitched" data-heroes='{E(heroes)}' data-base="assets/photos/">
<img src="assets/photos/{h0[0]}-1280.webp" srcset="assets/photos/{h0[0]}-768.webp 768w, assets/photos/{h0[0]}-1280.webp 1280w, assets/photos/{h0[0]}-1920.webp 1920w" sizes="(max-width: 820px) 100vw, 600px" alt="{E(h0[1])}" width="1280" height="960" fetchpriority="high">
<figcaption>{E(h0[1])} · {E(h0[2])}</figcaption></figure>
</div>
<div class="wrap" style="margin-top:34px">{seam()}</div></section>

<section class="block" id="about"><div class="wrap">
<div class="block-head"><h2>Who we are</h2></div>
<div class="prose"><p>SICDP is an independent, youth-led think tank based in Dhaka, Bangladesh. We work at the intersection of climate governance and state capacity in South Asia.</p>
<p>We study why climate and digital governance fall short in practice, and we ground our answers in field evidence and institutional analysis.</p></div>
<div class="focus">
<div class="card stitched">{art("hazard-haor", "", p)}<div><h3>Climate governance</h3><p>How plans for salinity, erosion, drought and floods hold up where people live with them.</p></div></div>
<div class="card stitched">{art("stitch-circuit", "", p)}<div><h3>Digital governance and state capacity</h3><p>Whether public institutions are ready for the technology they are asked to run.</p></div></div>
</div></div></section>

<section class="block" id="work" style="background:var(--tint)"><div class="wrap">
<div class="block-head"><h2>Our work</h2><p>Two programmes in the field now, and a paper series on the way.</p></div>
<div class="work">
<article class="programme stitched"><header><h3>The C30 Agenda</h3><span class="status">Field research</span></header>
<p>The C30 Agenda is SICDP's first major field research project. It audits where climate-related Sustainable Development Goal targets failed to deliver for climate-vulnerable communities and proposes climate priorities for the decade beyond 2030, grounded in direct field evidence from Bangladesh. Research teams work across four sites, each representing a distinct hazard: coastal salinity, riverine erosion, drought, and haor flash floods. Findings are qualitative-led, drawn from interviews and focus groups.</p>
<div class="hazards">{hazards}</div></article>
<article class="programme stitched"><header><h3>The Adaptation Lab</h3><span class="status">Applied research</span></header>
<p>The Adaptation Lab is the applied research arm of SICDP. It takes a single live case at a time and moves it through a structured cycle: intake, active case work, after-action review, and a published dispatch. A dual-wing design also supports an innovation and prototyping track. Each case must name a clear beneficiary, and the Lab documents what it learns so that practical adaptation lessons are shared openly with practitioners and policymakers.</p>
<ol class="steps">{steps}</ol></article>
<article class="programme stitched open"><div class="papers">{art("papers", "", p)}<div><header><h3>The Statecraft Papers</h3><span class="status">Forthcoming</span></header>
<p>Our working paper series. Papers will be published openly here, on SSRN and on Zenodo.</p></div></div></article>
</div></div></section>

<section class="block" id="field"><div class="wrap">
<div class="block-head"><h2>Field Diaries</h2><p>Eight days, eleven districts, from Bagerhat to Mymensingh. October 2026.</p></div>
<div class="photos">{grid}</div>
<p class="more"><a class="btn" href="field-diaries.html">See the route and all photos</a></p>
</div></section>

<section class="block" id="writeups" style="background:var(--tint)"><div class="wrap">
<div class="block-head"><h2>Write-ups</h2><p>Short pieces by SICDP members. Views are the authors' own.</p></div>
<div class="writeups">{wu}</div>
</div></section>

<section class="block" id="coming"><div class="wrap coming">
<div><div class="block-head" style="margin-bottom:18px"><h2>Coming up</h2></div>
<ul><li><strong>Work with the Rural Development Academy, Bogura</strong><span class="label">Forthcoming</span></li>
<li><strong>The first Statecraft Papers</strong><span class="label">Forthcoming</span></li></ul></div>
{skyline}
</div></section>

<section class="block" id="team" style="background:var(--tint)"><div class="wrap">
<div class="block-head"><h2>Team</h2><p>Profiles are being prepared and will appear here.</p></div>
<div class="people">{team}</div>
</div></section>

<section class="block" id="advisory"><div class="wrap">
<div class="block-head"><h2>Advisory Board</h2><p>We are forming our advisory board. Each seat stays open until the right person agrees to join.</p></div>
<div class="people">{seats}</div>
</div></section>
</main>
{footer(p)}'''
    write('index.html', body)

# ---------------------------------------------------------------- field diaries
def field():
    p = ''
    geo = json.load(open(os.path.join(ROOT, 'tools/bangladesh-outline.json')))
    x0, y0, x1, y1 = geo['bbox']; pad = 12
    vb = f'{x0-pad:.0f} {y0-pad:.0f} {x1-x0+2*pad:.0f} {y1-y0+2*pad:.0f}'
    st = geo['stops']
    route = 'M' + ' L'.join(f'{st[k][0]} {st[k][1]}' for k in ROUTE)
    dots = ''.join(f'<circle class="stop" cx="{st[k][0]}" cy="{st[k][1]}" r="4"/>' for k in ROUTE)
    labels = ''.join(f'<text x="{st[k][0]+LABEL[k][0]}" y="{st[k][1]+LABEL[k][1]}" text-anchor="{LABEL[k][2]}">{E(k)}</text>' for k in ROUTE)
    mapsvg = (f'<svg class="map" viewBox="{vb}" role="img" aria-label="Map of Bangladesh with the October 2026 route from Dhaka to Bagerhat, Khulna, Jashore, Kotchandpur, Kushtia, Rooppur, Bogura, Jamalpur and Mymensingh">'
              f'<path class="land" d="{geo["d"]}"/><g class="sew-route"><path class="route" d="{route}"/></g>{dots}{labels}</svg>')
    days = ''.join(f'<li><span class="label">{E(d)}</span><span><strong>{E(w)}</strong><br>{E(t)}</span></li>' for d, w, t in DAYS)
    groups = ''
    for stop in dict.fromkeys(f[0] for f in FIELD):
        figs = ''.join(photo(s, c, f'{d} 2026', p) for k, s, c, d in FIELD if k == stop)
        groups += f'<section class="stop-group"><h2>{E(PLACE[stop])}</h2><div class="photos" style="margin-top:14px">{figs}</div></section>'
    body = f'''{head("Field Diaries · Statecraft Institute", "Photos and route from SICDP's October 2026 field trip across eleven districts of Bangladesh.", p)}{header(p, "Field Diaries")}
<main>
<section class="block"><div class="wrap">
<p class="label">21 to 29 October 2026</p>
<h1 style="font-size:clamp(2.1rem,4.6vw,3.3rem);margin-top:10px">Field Diaries</h1>
<div class="diary-top" style="margin-top:28px">
<div class="sew">{mapsvg}</div>
<div><p class="lede" style="margin-top:0">Eight days on trains, buses, CNGs and a boat across the Jamuna. About 1,100 km through eleven districts, recording short interviews on climate and development.</p>
<ul class="days">{days}</ul></div>
</div>
<div style="margin-top:40px">{seam()}</div>
<div style="margin-top:36px">{groups}</div>
</div></section>
</main>
{footer(p)}'''
    write('field-diaries.html', body)

# ---------------------------------------------------------------- write-ups
def writeups():
    p = '../'
    for slug, thumb, alt in WRITEUPS:
        meta, body_html, _ = read_writeup(slug)
        page = f'''{head(meta["title"] + " · Statecraft Institute", meta["title"] + ", a write-up by " + meta["author"] + ".", p)}{header(p, "Write-ups")}
<main class="calm"><article class="op wrap">
<p class="label"><a href="{p}index.html#writeups">Write-ups</a></p>
<h1 style="margin-top:12px">{E(meta["title"])}</h1>
<p class="by label">{E(meta["author"])} · {E(meta["when"])}</p>
<div class="thumb">{art(thumb, alt, p)}</div>
<div class="body">{body_html}</div>
<p class="disclaimer">Views are the author's own and do not necessarily reflect those of SICDP. Sources will be added.</p>
</article></main>
{footer(p)}'''
        write(f'write-ups/{slug}.html', page)

if __name__ == '__main__':
    home(); field(); writeups(); print('built')
