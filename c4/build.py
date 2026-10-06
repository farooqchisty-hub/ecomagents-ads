#!/usr/bin/env python3
"""Storyboard page for Ecom Agent OS concept 4, "The 2am Founder". Writes index.html next to this file."""
import html, os
e = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))

CAST = [
    ("cast_maya", "Maya, 31", "Founder of Northlane Candle Co. (fictional). Grey hoodie, messy bun, tortoiseshell glasses. The only character in every unit."),
    ("cast_strategist", "The Strategist, mid 40s", "Mustard cardigan, glasses on a beaded chain. First teammate to appear. One line."),
    ("cast_care", "Customer Care lead, late 20s", "Navy hoodie, headset around his neck. Second teammate. One line."),
    ("cast_operator", "The Operator, mid 50s", "Silver hair, grey beard, denim shirt. Sits at the head of the full table. Delivers the turn."),
]

# t0, t1, beat, unit, keyframe, picture, lines[(who, line, delivery)], graphics, sound, music
TL = [
    (0.0, 4.0, "HOOK", "U1", "k1_hook", "Extreme close-up. Maya at 2:07am, laptop light on her face, tabs reflected in her glasses, wall clock soft behind her.",
     [("Maya", "Who does all of this at two a.m.?  ...Me.", "flat, tired, half-laughing at herself")], "none", "native: room tone, laptop fan", "A1 late night: sparse felt piano and a low pad, enters under her line"),
    (4.0, 11.0, "SETUP", "U2", "k2_strategist", "She clicks a tab closed. Cut to over her shoulder: the Strategist is already sitting across the table, sketching ad layouts, and looks up.",
     [("Strategist", "Hooks are ready. Want the three strongest?", "warm, matter-of-fact, like it is a normal Tuesday"), ("Maya", "(no line, stares)", "")],
     "Label pops in free space above her head: CREATIVE STRATEGY", "native trackpad click as the tab closes (the event that summons her)", "A1 continues"),
    (11.0, 17.0, "BUILD", "U3", "k3_care", "She closes another tab. The Customer Care lead is in the chair right next to her, relaxed.",
     [("Care lead", "Seventeen refund tickets. Drafts are in your queue. You just approve.", "easygoing, reassuring, a little amused by her face")],
     "Label: CUSTOMER CARE", "native trackpad click", "A1 to A2: a soft pulse enters as he finishes"),
    (17.0, 23.0, "BUILD", "U4 a/b/c", "k4_filling", "Three hard cuts, 2s each, from the far end of the table: 4 teammates, then 9, then all 16. People are simply there on each cut; nobody morphs or appears mid-shot.",
     [], "Agent name cards snap in on each cut, in the empty space above the table, never over a face: Customer Voice, Offers & Bundles, Product Page, Purchase Recovery, Performance Marketing, Operator, and more", "none (decoration stays silent)", "A2 build: pulse and strings rise to the turn"),
    (23.0, 30.0, "TURN", "U5", "k5_full", "Wide, symmetrical. The full table, a low working murmur. Maya standing at the near end. The Operator at the head looks up.",
     [("Maya", "...Who are you people?", "stunned, small, almost a whisper"), ("Operator", "Your growth team. We just need your Brand Brain.", "dry, kind, unhurried")],
     "none", "native murmur, pages, keys", "A2 drops to a held chord under the Operator's line"),
    (30.0, 34.0, "PAYOFF", "U6", "k6_dawn", "Dawn. Maya wakes on the couch under a throw. The table is empty, chairs pushed in, her laptop glowing alone.",
     [("Maya", "(reads, quietly) Sixteen drafts.", "sleepy, slow smile")], "none", "native: birds, distant traffic", "A3 morning: warm open chord, light piano"),
    (34.0, 37.0, "IN-WORLD CTA", "U7", "k7_screen", "Over her shoulder to the laptop. The screen is replaced in post with the real product context: a chat workspace for Northlane with the Brand Brain files attached and finished drafts from the agents (ad hooks, refund replies, a recovery flow). She types: go with hooks 1 and 3.",
     [], "Screen comp (static camera, corner-pinned): chat workspace with Brand Brain chips and agent drafts. No fake dashboard: this is how the product actually runs.", "native typing", "A3 continues"),
    (37.0, 40.0, "OUTRO", "HF card", None, "End card built in HyperFrames, brand colors from ecomagents.ai.",
     [], "Ecom Agent OS. 16 growth agents. One Brand Brain. You approve what goes live.  ecomagents.ai  [price line per market]", "none", "A3 resolves through the card, no hard stop"),
]

UNITS = [
    ("U1 hook, 5s", "Maya alone. Refs: Maya card + K1. Short so the hook can be re-rolled cheaply."),
    ("U2 Strategist, 7s", "Refs: Maya, Strategist, K2. Single world, one camera setup."),
    ("U3 Care lead, 6s", "Refs: Maya, Care lead, K3."),
    ("U4 a/b/c, 3 x 4s", "First-frame inserts from three table states (4, 9, 16 people), 2s used from each. Hard cuts solve the people-appearing physics problem."),
    ("U5 turn, 7s", "Refs: all four cards + K5. Holds the only product term spoken (Brand Brain), so it is its own short unit."),
    ("U6 dawn, 5s", "Refs: Maya + K6."),
    ("U7 screen insert, 4s", "First frame K7, static camera so the screen comp tracks cleanly."),
]
SOUND = [
    ("Native first", "All speech, murmur, clicks, typing and ambience come from the generations themselves."),
    ("Added sounds: none planned", "The tab clicks are native and carry the story (each click summons a teammate). Name cards, the end card and the screen comp stay silent. Nothing ever sits on a brand word."),
    ("Music: one score, 3 sections", "A1 late night (0 to 11s), A2 build (11 to 30s), A3 morning (30 to 40s). Generated to the final cut, ducked under every line, carries through the outro."),
]
VOICE = [
    "Maya speaks in U1, U5 and U6: her isolated U1 vocal stem is passed as the voice reference into U5 and U6.",
    "Strategist, Care lead and Operator each have one line in one unit, so there is no cross-unit voice match to hold.",
    "Every speaker is on camera on their first line.",
    "No brand name is spoken. \"Brand Brain\" is plain English and gets checked on the vocal stem with two transcribers.",
]
RULES = [
    "One world, so plain cuts: no split screen or picture-in-picture.",
    "Exact-risk line (Brand Brain) lives in a short unit, re-rollable for about $2.",
    "Physics: teammates never materialize on camera; the table fills only across hard cuts.",
    "Fictional world: Northlane Candle Co., blank labels, no real logos. Every take gets frame-scanned for brand leaks.",
    "Graphics use the real agent names, in free space, never over a face.",
    "Honest product mechanic: the dawn screen shows a chat workspace with drafts waiting for review, which is how the product works. No invented dashboard, no results claims.",
    "Cast for North America, so it runs in global markets.",
]
COST = [
    ("Cast cards + keyframes (done)", 2.75),
    ("Seedance 2.5, 51s generated at about $0.27/s", 13.80),
    ("Music, 3 sections", 1.50),
    ("Transcription + stem QA", 0.50),
    ("Re-roll budget (about 1.5x on risky units)", 15.00),
]
RISKS = [
    "Checkout is INR only (Cashfree). The global cut needs a USD price before it runs in the US; until then the end card shows no price outside India.",
    "Keeping 16 faces consistent across the three fill cuts: only the 4 cast members must match; the other 12 just need to stay in their seats between cuts b and c.",
]

def kf(k):
    return f"<img loading='lazy' src='img/{k}.jpg' alt=''>" if k else "<div class='ph'>end card</div>"
rows = []
for t0, t1, beat, unit, k, pic, lines, mg, sfx, mus in TL:
    ls = "".join(f"<p><b>{e(w)}</b>: “{e(l)}”" + (f" <span class='m'>({e(d)})</span>" if d else "") + "</p>" for w, l, d in lines) or "<p class='m'>no dialogue</p>"
    rows.append(f"""<article class='beat'><div class='kf'>{kf(k)}</div><div class='bd'>
<div class='tc'><span class='t'>{t0:.0f} to {t1:.0f}s</span><span class='chip'>{e(beat)}</span><span class='chip u'>{e(unit)}</span></div>
<p class='pic'>{e(pic)}</p><div class='lines'>{ls}</div>
<dl><dt>Graphics</dt><dd>{e(mg)}</dd><dt>Sound</dt><dd>{e(sfx)}</dd><dt>Music</dt><dd>{e(mus)}</dd></dl></div></article>""")
cards = lambda xs: "".join(f"<div class='card'><h4>{e(a)}</h4><p>{e(b)}</p></div>" for a, b in xs)
cast = "".join(f"<figure class='cast'><img loading='lazy' src='img/{k}.jpg' alt=''><figcaption><b>{e(n)}</b><br>{e(d)}</figcaption></figure>" for k, n, d in CAST)
words = sum(len(l.split()) for r in TL for w, l, d in r[6] if not l.startswith("("))
total = sum(c for _, c in COST)

page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>The 2am Founder</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f6f4ef;--ink:#16181d;--muted:#6b6f78;--line:#e2ded5;--card:#fff;--acc:#2440c9;--chip:#eceaf6}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111215;--ink:#ecebe7;--muted:#9a9ea8;--line:#2a2c31;--card:#1a1b1f;--acc:#8ea2ff;--chip:#24263a}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Inter,system-ui,sans-serif}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 16px}}header{{padding:40px 0 24px;border-bottom:1px solid var(--line)}}
h1{{font-size:clamp(28px,5vw,44px);margin:8px 0;letter-spacing:-.5px}}h2{{margin:40px 0 14px;font-size:22px}}h4{{margin:0 0 6px}}
.chip{{display:inline-block;background:var(--chip);color:var(--acc);font-size:11px;font-weight:700;letter-spacing:.4px;padding:3px 8px;border-radius:99px;margin-right:6px}}
.chip.u{{background:transparent;border:1px solid var(--line);color:var(--muted)}}.m{{color:var(--muted);font-size:13px}}
.toc a{{color:var(--acc);margin-right:14px;font-size:14px;text-decoration:none}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}}.card p{{margin:0;font-size:14px}}
.castrow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}}.cast{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}.cast img{{width:100%;display:block}}.cast figcaption{{padding:10px 12px;font-size:13px}}
.beat{{display:grid;grid-template-columns:220px 1fr;gap:16px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:12px}}
.kf img,.ph{{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:10px;display:block}}.ph{{display:grid;place-items:center;background:var(--chip);color:var(--muted)}}
.tc{{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-bottom:6px}}.t{{font-weight:700;margin-right:6px}}.pic{{margin:4px 0 8px}}.lines p{{margin:4px 0}}
dl{{display:grid;grid-template-columns:80px 1fr;gap:4px 10px;margin:10px 0 0;font-size:13px}}dt{{color:var(--muted)}}dd{{margin:0}}
table{{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden}}td{{border-bottom:1px solid var(--line);padding:9px 12px}}td:last-child{{text-align:right;white-space:nowrap}}
ul{{padding-left:18px}}li{{margin:4px 0}}.gate{{background:var(--card);border:2px solid var(--acc);border-radius:14px;padding:16px;margin:32px 0 60px}}
@media (max-width:640px){{.beat{{grid-template-columns:1fr}}.kf img,.ph{{max-width:260px}}}}
</style></head><body>
<header><div class="wrap"><span class="chip">Storyboard for approval</span><span class="chip">Ecom Agent OS · concept 4</span>
<h1>The 2am Founder</h1>
<p>A founder alone at 2am closes her tabs one by one, and each closed tab leaves a teammate at her table until all 16 seats are full. At dawn the table is empty, but the drafts are real and waiting for her review. 40s, 9:16 master, North American cast for global use. {words} words of dialogue.</p>
<div class="toc"><a href="#cast">Cast</a><a href="#tl">Timeline</a><a href="#gen">Generation</a><a href="#sound">Sound</a><a href="#rules">Rules</a><a href="#cost">Cost</a></div></div></header>
<div class="wrap">
<h2 id="cast">Cast</h2><div class="castrow">{cast}</div>
<h2 id="tl">Timeline</h2>{''.join(rows)}
<h2 id="gen">Generation plan <span class="m">Seedance 2.5, generated without music</span></h2><div class="grid">{cards(UNITS)}</div>
<h2 id="sound">Sound and music</h2><div class="grid">{cards(SOUND)}</div>
<h2>Voice</h2><ul>{''.join(f'<li>{e(v)}</li>' for v in VOICE)}</ul>
<h2 id="rules">Principles applied</h2><ul>{''.join(f'<li>{e(v)}</li>' for v in RULES)}</ul>
<h2>Risks</h2><ul>{''.join(f'<li>{e(v)}</li>' for v in RISKS)}</ul>
<h2 id="cost">Cost</h2><table>{''.join(f'<tr><td>{e(a)}</td><td>${c:.2f}</td></tr>' for a, c in COST)}<tr><td><b>Total, all in</b></td><td><b>about ${total:.0f}</b></td></tr></table>
<div class="gate"><b>Gate:</b> nothing past the keyframes has been spent. Approve this storyboard (or mark changes) and production starts: 7 units, the score, then a review cut.</div>
</div></body></html>"""
assert "—" not in page and "–" not in page, "no em or en dashes"
open(os.path.join(HERE, "index.html"), "w").write(page)
print(os.path.join(HERE, "index.html"))
