# Statecraft Institute website (SICDP): project context

Read this whole file before doing anything. Then read the files listed under "Repository layout".

## Who you are working with
- Hasanor Rahman (call him "Hasanor" or "হাছানুর"). Designer (Photoshop, Illustrator, InDesign, ~7 years), BSS student in Japanese Studies, University of Dhaka. Not a programmer and does not want to learn coding; you write all code.
- Talk to him in Bengali, short and clear. Never use em dashes. Explain technical steps in plain words.
- For any idea he shares, also give five short lenses: 10x this, What am I missing?, Steelman this, ELI5, Be brutal.
- Do not create extra docs or files unless he asks. Do not start building until the plan is discussed and he approves it.

## Confirmed by Hasanor (2 Nov 2026): use this as the source of truth for public copy
- Name: Statecraft Institute for Climate and Development Policy (SICDP). Final. (SICG is the old name; never use it publicly.)
- Who we are: SICDP is an independent, youth-led think tank based in Dhaka, Bangladesh. We work at the intersection of climate governance and state capacity in South Asia.
- Motto: "Instituta Firma, Res Publica Firma."
- What we try to do: We study why climate and digital governance fall short in practice, and we ground our answers in field evidence and institutional analysis.
- Programmes:
  - C30 Agenda: first major field research project. Audits where climate-related SDG targets failed to deliver and proposes climate priorities beyond 2030, based on fieldwork in four Bangladeshi sites facing salinity, riverbank erosion, drought and flash flooding.
  - The Adaptation Lab: applied research arm. Describe it in general terms only (the approved copy below). Do NOT name "Charting Displacement" or any specific case on the site (Hasanor, 3 Nov 2026).
  - The Statecraft Papers: planned working paper series. NOT yet launched.
- Approved programme copy for the site (Hasanor, 3 Nov 2026; use as written, English):
  - C30 Agenda: "The C30 Agenda is SICDP's first major field research project. It audits where climate-related Sustainable Development Goal targets failed to deliver for climate-vulnerable communities and proposes climate priorities for the decade beyond 2030, grounded in direct field evidence from Bangladesh. Research teams work across four sites, each representing a distinct hazard: coastal salinity, riverine erosion, drought, and haor flash floods. Findings are qualitative-led, drawn from interviews and focus groups."
  - The Adaptation Lab: "The Adaptation Lab is the applied research arm of SICDP. It takes a single live case at a time and moves it through a structured cycle: intake, active case work, after-action review, and a published dispatch. A dual-wing design also supports an innovation and prototyping track. Each case must name a clear beneficiary, and the Lab documents what it learns so that practical adaptation lessons are shared openly with practitioners and policymakers."
- Plans:
  - RDA Synergy Week 2027: proposed week-long programme with the Rural Development Academy (RDA), Bogura, 28 December 2026 to 2 January 2027. TEDx event, three-day Char Research Bootcamp for about 80 students from eight universities, and a policy symposium, then a synthesis phase producing a field report, a policy brief and working papers. SICDP organises, RDA hosts, its Char Development Research Centre advises. Status: proposed, not approved.
  - Publish working papers openly through the website, SSRN and Zenodo.
  - Publish policy briefs and op-eds ahead of a cross-border academic roundtable with Indian institutions, targeted for December 2026.
  - Build long-term partnerships with South Asian research institutions.
- Real invitation (received 2 Nov 2026): Bangladesh Climate Change Trust (BCCT, Ministry of Environment, Forest and Climate Change) invited SICDP (listed first in the distribution) to send a representative to a youth consultation ahead of COP31 on meaningful youth participation in Bangladesh's climate priorities. 5 Nov 2026, 11:00, BCCT conference room, Puraton Bon Bhaban, 101 Mohakhali, Dhaka, chaired by the BCCT Managing Director; about 65 attendees. Site wording rule: "invited to / took part in" only after attending; never "partner of BCCT". Do not publish the notice image itself.
- Contact: thestatecraftinstitute@gmail.com
- Implication for the site: there are no published outputs yet. Everything above under "Plans" must be labelled as proposed / planned / forthcoming.

## Website decisions by Hasanor (3 Nov 2026): these override the background sections below
- Tagline: the Latin motto "Instituta Firma, Res Publica Firma" (as on the document cover) is the main tagline. Do NOT use "Southern Perspectives. Global Policy." or "Good governance is climate action".
- Do NOT use publicly: the "borrowed capacity / built capacity" thesis, the "Borrowed Capacity" and "Premature Automation" papers (personal work of the authors, unpublished, not SICDP work), the IIT Kharagpur roundtable, the Bengal Delta Conference, anything from `SICG.docx` (outdated draft). No funding page or funder names for now (no funding yet). No 3-month goals, no achievements timeline.
- Tone and scope: light site. Say what we work on, and note upcoming progress briefly. No heavy detail. Grows as work happens.
- RDA: may be mentioned only as forthcoming work with RDA (proposal is in process); no dates or programme details yet.
- Content we can publish: unpublished, original op-eds by SICDP people, published on the SICDP website under the SICDP banner; field photos and videos from the Oct 2026 trip.
- Team: everyone is willing to give photos. Build a profile for each member (photo + short About). Hasanor will send the team list. No advisers yet. Hasanor wants the Advisory Board section SHOWN with open seats (empty, honestly labelled, no fake names or faces), so prospective advisers can see where their name and photo will go and what they gain. A name goes in only after written consent.
- "Youth-led" can be up front.
- Language: English only.
- Colours: Shihab's navy dossier draft is not binding; design fresh in the brand.
- Domain and email: no funds, so use the .xyz domain (sicdp.xyz) and the Gmail address for now.
- Visual system (Hasanor's idea, 3 Nov 2026): nakshi kantha running stitch is THE unifying motif across the site: page background as a faint watermark weave (barely visible), section borders and dividers, text-box/card frames, profile frames, larger icons. Purple on white. Proposed guardrails (to confirm): stitch for frames, dividers and large illustrations; solid lines for body text and small UI icons (24px) so they stay legible; watermark very low opacity and never behind long text in a way that hurts contrast; built with CSS and one tiny SVG pattern so the site stays light.
- Motion wishes (Hasanor, 3 Nov 2026; details still open): hover on empty areas should feel like touching a kantha; loading shown as stitches being sewn; page-to-page transition with a stitch (and river wave) feel; river waves can combine with stitch. Must stay light and calm, not heavy on the eye. Proposed budget: no animation libraries, all interaction JS under ~5 KB, honour prefers-reduced-motion, never block content behind a loader, phone (no hover) needs its own answer.
- Motion decisions (Hasanor, 3 Nov 2026):
  - Desktop hover on empty areas and on images: stitches near the cursor become clearer + a light ripple + a thread trail behind the cursor that stays while the mouse is there, then fades. Only if it stays light.
  - Phone: section dividers stitch themselves on scroll; tap-to-reveal stitches in special places (header, footer).
  - No blocking loader. Hero lines stitch in within ~1 s on open; image/video placeholders show stitching while loading; stitch-in plays on every page.
  - Page transitions under 0.5 s, as fast as possible: stitch line sewn left to right for the programme "wings"; river-wave curtain and a one-time card shimmer for Team profiles, About, Contact; other places minimal.
  - Waves drawn as a running stitch: hero, footer, and as dividers between landing-page sections.
  - Illustrations gently animated (haor water rippling, tree drying under the sun, etc.): noticeable but never annoying.
  - Colour: purple only (no secondary colours for now).
  - Reduced-motion users: no movement, but keep a little feel (e.g. soft fades).
  - Dark mode (decided 3 Nov 2026): follow the device automatically, NO toggle button. Light device = white site; dark device = dark site. Dark background is a soft charcoal / iron black (not pure black), text light purple-white (#F4EDF6), links light purple, watermark even fainter. Emblem: purple version in light mode, full-colour version in dark mode; the emblem's elements must never change. Phone browser bar (Android status/address bar) should match the purple header (theme-color).
  - Trail: on PC long, following the mouse path, fades 1 s after the mouse leaves; on phone short (finger length). Nothing happens over text. Ripple only on images.
  - Illustration animation runs slowly while on screen, stops off screen; only one moving illustration on screen at a time. Hero: photos rotate one after another.
  - Low-end phones: drop images/animations where needed and just show the content.
  - Structure (to confirm): full home page with sections; menu items scroll to sections; About has its own entry; NO contact page or form, contact (email, phone) and social links sit in the footer; programmes and divisions are the "wings" with their own pages and the stitch transition.
  - Illustrations: Hasanor generated them in Google Flow from the prompts; he will send them as reference. Claude redraws them as clean, layered line-art SVG so they can be animated.
- More decisions (3 Nov 2026):
  - Section names: "From the field" is called "Field Diaries"; "Writing" is called "Write-ups" (op-eds shown as thumbnail cards).
  - Division pages: description of the division's work, member list, links to member profiles.
  - Photos: files named for the hero go to the hero (one random photo per visit with its place name, no slideshow); files named field trip, and unnamed ones, go to Field Diaries.
  - Emblem: tree gaps stay transparent (also in dark mode). Dark-mode header is charcoal (like YouTube).
  - All accounts (domain, Cloudflare, GitHub, YouTube) on the organisation Gmail. Domain sicdp.xyz not bought yet; buying now.
  - Phone 01812267679 is Shihab's; fine on the site. Op-eds are approved by Shihab.
  - Field video subjects gave consent. No Bengali on the site. No soft target date. Test device: Hasanor's low-cost Android.
- Answers to the open questions (3 Nov 2026):
  - Plan and purple brand: APPROVED as written (Shihab agreed). Building can start once the starter items arrive.
  - Launch: no fixed date.
  - Site maintainer: Shanto (Hasanor Rahman Shanto, i.e. Hasanor himself).
  - Motto: Latin only, no translation shown.
  - Advisory Board: four open seats, no names, no Founding Chair for now: Climate & Disaster Governance; Rural Development & Char Lands; Public Administration & Digital Governance; Foreign Adviser.
  - Prof. Abdullah-Al-Mamun: not approaching for now. Do not reference him on the site.
  - Team order: by division, following Hasanor's division chart (chart not yet received). Anyone in more than one division needs one primary division.
  - Founding date: 8 June 2026.
  - Contact: email + phone 01812267679 (as on the letterhead), no form.
  - Festival greetings: none for now.

## The organisation (background from internal documents)
- Name: Statecraft Institute for Climate and Development Policy (SICDP). Earlier name in some documents: Statecraft Institute for Climate & Governance (SICG).
- Youth-led policy think tank, Dhaka, founded 2026 by Md. Imam Hossain Shihab (Founder and Executive Director). Hasanor leads design in the Creative Studio and wants a leadership role.
- Core thesis: "borrowed capacity". Bangladesh outsources state functions (climate governance, digital services) to NGOs, donors and consultants. Goal: "built capacity". Vision line: "States that build, not borrow, the capacity to govern their own future." Tagline in an earlier draft: "Southern Perspectives. Global Policy."
- Two research tracks:
  1. Climate & Governance. Flagship: Field-to-Negotiation Research Program (field evidence turned into UNFCCC negotiation language; path toward COP youth delegations).
  2. Technology & State Capacity. Flagship: Digital Governance Research Program. Working paper "Premature Automation: Institutional Preconditions for AI-Enabled Public Services in South Asia" by Shihab and Shuaib Ahmed Araf (Dept. of Public Administration, DU). Four failure modes: opaque accountability, encoded exclusion, vendor dependency, administrative deskilling.
- Other programmes: The Adaptation Lab (Innovation Atlas, Prototype Pilots, The Last Mile, Recognition & Reach; first proposal on char erosion and land rights in Sirajganj, Bogura, Gaibandha); The C30 Agenda ("Field-Tested Climate Priorities, Beyond 2030"; sites Satkhira, Kurigram, Naogaon, Sunamganj).
- Events: RDA Synergy Week 2027 at the Rural Development Academy, Bogura, with its Char Development Research Centre (TEDxBogura, Char Research Bootcamp, Delta Futures Symposium; about 100 participants from 8 universities; proposal to RDA's Director General drafted, NOT yet approved). IIT Kharagpur cross-border roundtable, target Dec 2026 (faculty panel NOT confirmed). A Dhaka roundtable is planned.
- Publication imprint: The Statecraft Papers. Standard: "useful to someone making a decision".
- Structure: four divisions (Policy & Research, External Relations, Strategic Engagement, Creative Studio); Advisory Fellows and an advisory board of teachers planned.
- Field content: in Oct 2026 Hasanor and team did an 8-day trip Khulna to Moulvibazar (13 districts) recording short interviews on climate and development ("চায়ের কাপে বাংলাদেশ" / Voices from the Delta, Field Diary, Field Notes), including RDA Bogura experts.
- Hasanor's vision: a think tank that feels prestigious yet "ours" to ordinary Bangladeshis across religion and politics, rooted in the land, recognisable by colour and logo alone, relevant for 50 to 100 years.

## Repository layout
- `docs/internal/` SICDP internal documents. Key ones: `SICDP_External_v3.docx` (public positioning), `SICG.docx` (founding document: outputs, 13-platform digital strategy, funding strategy), Adaptation Lab and C30 documents, IIT Kharagpur roundtable plans, `4 months checklist.docx`, `statecraft-homepage.html` (Shihab's earlier homepage draft in a navy/paper/seal-red "dossier" style; it contains sample op-eds, placeholder metrics and calls the IIT roundtable "Confirmed": never publish any of that as real).
- `docs/proposals/` RDA Synergy Week proposal: original draft and the formatted version on the letterhead.
- `docs/field/` field trip plan and route (Oct 2026).
- `brand/logo/` `emblem-color-final.png`, `emblem-purple.png`, `emblem-black.png`, `lockup-horizontal-purple.png`, older drafts in `drafts/`. Ask Hasanor for vector (AI/SVG) logo files before final build.
- `brand/letterhead/` letterhead EPS, SVG (vector, text outlined), 300 dpi PNG, blank Word template.
- The repo is PRIVATE because `docs/` is internal. Never move internal documents into the public site output.

## Brand (designed by Hasanor)
- Emblem: a circle divided into organic sections by thin white gaps; the gaps form a hidden negative-space tree (built capacity growing from within). Sections: nakshi kantha running-stitch topographic contours (knowledge, research), silt and sand ripple bands (land), large leaves with vein cuts (nature), riverbank with tree, solar-roof house, wind turbine, multi-storey building and rising sun (people and development), river with a char island and small plain boat (water, climate risk). Deliberately avoids party-political symbols (no paddy sheaf, no canopy boat as a central symbol).
- Main colour: purple #812F8E (accents #5A1F66 / #6B2078, light tint #F4EDF6). Candidate secondary/data palette from the colour emblem: ochre #C48A3A, teal #1F6E6A, deep blue #2F5D7C, coral #D0634F, sage #8EA585, saffron #E3A93B. Final palette not decided.
- Logotype currently in a heavy condensed font (Gobold), three equal lines. Suggested direction (not final): "Statecraft" large in Newsreader, "INSTITUTE FOR CLIMATE AND DEVELOPMENT POLICY" small in Inter caps, IBM Plex Mono for labels and numbers; Bengali pairing Tiro Bangla + Noto Sans Bengali.
- Line-art kit planned from the emblem: horizon line, development skyline, leaf sprig, river with char and plain boat, nakshi stitch pattern, half sun, contact icons. Rule: max two motifs per design, lots of white space.
- Naming suggestion: people-facing "Statecraft", formal "Statecraft Institute", legal "Statecraft Institute for Climate and Development Policy (SICDP)". Not final.
- Open gap: the emblem shows climate and land well but nothing for the Technology & State Capacity track. Idea: a "stitched circuit" (circuit lines drawn as nakshi stitches).

## Website plan so far (not approved yet)
- Hosting decision: this private repo, deployed with Cloudflare Pages (free; private repos supported). Keep the public site in its own folder (for example `site/`) so only that folder is deployed.
- Domain: www.sicdp.xyz is printed on the letterhead. Concern: .xyz can look less serious and can hurt email deliverability; .org was suggested. Decide before buying. Set up an organisation email on the domain.
- Build approach: static site (plain HTML/CSS, or a simple static generator if it helps editing). Move to a CMS later only if many people need to publish without code.
- Draft sitemap: Home; About (mission, vision, borrowed vs built capacity, story, how we work); People (Leadership, Advisory Board, Team by division, Fellows later); Research (two tracks); Programs; Publications (The Statecraft Papers); Events (RDA Synergy Week, IIT Kharagpur, Dhaka roundtable); Field Notes (videos, photos, map archive idea); Get Involved; Contact. Footer: Partners, Support Us, Privacy Policy, Funding & Independence (no single donor above 40 percent, no agenda-distorting money), Research Ethics (consent for field recordings).
- Option: start with one strong landing page plus Contact, then grow.
- Image placeholders: hero 1920x1080, programme cards 1200x800, portraits 800x800 with consistent background and light, publication covers 1200x1600, events 1600x900, video thumbnails 1280x720. Use clearly marked empty placeholders, not stock photos.
- Mobile-first (most Bangladeshi visitors use phones), fast, accessible, SEO basics, analytics, Google Search Console.

## Hard rules
- Never invent content: no fake publications, metrics, testimonials, partners or "confirmed" events. Unbuilt things are labelled "Forthcoming".
- Do not list anyone on the Advisory Board or team without their written consent.
- Keep it non-partisan in words and images.
- The site must have a named maintainer and be easy to update.

## Open questions to ask Hasanor first
1. ~~Who will update the site~~ Answered: Shanto (Hasanor).
2. ~~Domain~~ Answered: .xyz + Gmail for now (3 Nov 2026).
3. One landing page first, or the full 8 to 10 page site? (He wants a light site.)
4. ~~Language~~ Answered: English only.
5. ~~Shihab's draft~~ Answered: start fresh; purple brand and plan approved.
6. ~~Deadline~~ Answered: no fixed date.
7. Team list, roles, photos and short bios (he will send). Advisers: none yet.
8. ~~Final organisation name~~ Answered: SICDP (2 Nov 2026).

## How to start a session
1. Read this file and the key documents in `docs/internal/`.
2. Summarise in Bengali what you understood; list gaps and contradictions you find.
3. Ask the open questions that are still unanswered.
4. Propose a short written plan (sitemap, phase 1 scope, tech, steps) and wait for approval.
5. Only then build in `site/`, show previews, and iterate on design with him.
