#!/usr/bin/env python3
"""Ecom Agent OS video ads: plan v2 (after Farooq's feedback on v1 of videos 1 and 2). Writes index.html here."""
import html, os
e = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
AUD = "D2C founders, ecommerce teams and performance marketers"
CRIT = ["Relevance", "Scroll stop", "Virality", "Creativity", "Catchiness", "Uniqueness"]

# ---------------------------------------------------------------- video 1
V1_HOOKS = [
    ("Your ChatGPT doesn't know your brand. That's why your ads sound like everyone else's.", [10, 9, 8, 8, 9, 8], "Names a pain every AI user has felt, and the demo is the fix. Winner."),
    ("This is what happens when your AI actually knows your brand.", [9, 8, 7, 7, 8, 7], "Clean curiosity line. Test variant B."),
    ("POV: you stopped writing ad briefs from scratch.", [8, 8, 8, 7, 8, 6], "Native creator format. Test variant C."),
    ("I gave my AI one product link.", [7, 6, 5, 5, 6, 5], "The v1 hook. Too flat: no pain, no audience, no tension."),
    ("Stop prompting. Start delegating.", [7, 6, 6, 6, 8, 5], "Catchy but abstract; doesn't say for whom."),
    ("Paste a product link. Get a creative team.", [8, 7, 6, 6, 8, 6], "Good line, better as the step 2 voiceover than the opener."),
    ("Every AI ad looks the same. Here's why yours don't have to.", [8, 8, 7, 7, 7, 6], "Close to the winner but softer."),
    ("Performance marketers: one link in, four ad concepts out.", [8, 7, 6, 6, 7, 6], "Strong for a performance-marketer-only cut."),
]
V1 = [
    ("0.0 to 3.2", "HOOK", "Your ChatGPT doesn't know your brand. That's why your ads sound like everyone else's.",
     "WHY YOUR AI ADS SOUND GENERIC", "A bland AI caption types itself (\"Elevate your space with our premium candle ✨\"), gets a red GENERIC stamp and is struck through.", "Built in HyperFrames", "Music enters on the stamp"),
    ("3.2 to 6.0", "WHO", "If you're a D2C founder, run an ecommerce store, or buy performance ads, here's the fix.",
     "For D2C founders · ecommerce teams · performance marketers", "Three audience chips snap in, one per role as it is spoken.", "Built in HyperFrames", ""),
    ("6.0 to 11.0", "STEP 1", "Step one: fill in your Brand Brain once. Products, customers, voice, offers, claims.",
     "STEP 1 · Brand Brain, 6 files", "The REAL Brand Brain folder recording from the landing page (01-BRAND-BRAIN: product-and-sku-truth, audience-and-voc, positioning-and-voice, offers-and-economics, claims-rights-policies, growth-learnings).", "site: brain-navigation-v3.mp4", ""),
    ("11.0 to 14.0", "STEP 2", "Step two: pick an agent and give it one product link.",
     "STEP 2 · Pick an agent", "Chat workspace: Brand Brain chips attach, the 10ROAS Static Ad Generator chip drops in, the product link is sent.", "c1 composition (existing)", ""),
    ("14.0 to 24.0", "PROOF", "It reads your brand, finds the objection customers actually have, writes four hooks, the briefs and the image prompts. Then it checks every claim against your facts.",
     "Reads · finds the objection · writes · checks claims", "Output streams; each lime highlight lands on the word the voice is saying (objection, hook 1, claims check).", "c1 composition, highlights re-timed to the VO", "Soft riser into the reveal"),
    ("24.0 to 29.0", "PAYOFF", "Run the prompts in your image tool, and you get ads like these.",
     "4 ad concepts · illustrative example", "The 4 library-template Northlane ads land in a 2x2 grid. Small label: Demo brand, illustrative example.", "libads n1 to n4", "Hit on the grid landing"),
    ("29.0 to 35.0", "SCALE + OFFER", "That's one agent. You get sixteen: research, offers, creative, Meta and Google, landing pages, retention and profit. All sixteen for ₹699, once.",
     "16 agents · ₹699 once · no subscription", "The landing page's bundle box shot (16 numbered agent books + Brand Brain, Setup Guides, Work Resources, 3 Bonuses) slides in; the 4 lanes Acquire 8, Convert 3, Retain 3, Operate 2 tick on.", "site: growth-agents-v4", ""),
    ("35.0 to 38.0", "CTA", "Works in ChatGPT, Claude and Codex. Get it at ecomagents dot ai.",
     "ecomagents.ai", "End card in the site palette, lime CTA pill.", "Built in HyperFrames", "Music resolves on the card"),
]

# ---------------------------------------------------------------- video 2
V2_HOOKS = [
    ("474 files. 16 growth agents. Here's what's actually inside.", [10, 9, 8, 8, 9, 8], "Specific numbers + the unboxing curiosity loop. Winner."),
    ("Don't buy another prompt pack until you see this folder.", [9, 9, 8, 8, 8, 8], "Contrarian, great scroll stop. Test variant B."),
    ("₹699 gets you this. Let me open it.", [9, 8, 8, 7, 8, 7], "Unboxing energy, price up front. Test variant C."),
    ("Your growth team, in one folder.", [7, 5, 5, 6, 7, 5], "The v1 headline. Fine as a tagline, too soft as a hook."),
    ("What ₹75,889 of growth work looks like in one folder.", [8, 7, 7, 7, 7, 7], "Strong, but the value number lands harder at the end."),
    ("D2C founders, here's everything inside a ₹699 growth team.", [8, 7, 6, 6, 7, 6], "Clear audience callout; kept as the line after the hook."),
]
V2 = [
    ("0.0 to 3.0", "HOOK", "474 files. Sixteen growth agents. Here's what's actually inside.",
     "WHAT'S INSIDE ECOM AGENT OS", "The bundle box shot punches in on the downbeat; 474 / 16 count up beside it.", "site: growth-agents-v4", "Drop 1: beat starts on frame 1"),
    ("3.0 to 5.5", "WHO", "Built for D2C founders, ecommerce teams and performance marketers.",
     "For D2C founders · ecommerce teams · performance marketers", "Audience chips snap on the beat.", "HyperFrames", ""),
    ("5.5 to 11.0", "01 AGENTS", "Sixteen agents, one per growth job. Customer research, offers, creative, Meta and Google, landing pages, recovery, retention, profit.",
     "01 · 16 growth agents", "The 16 current agent names cascade as folder rows, cut to the beat (designed from agents-data.js, so every name is current). A 1.5s insert of the real folder recording plays under a crop that hides the original-edition folder names.", "site: agents-navigation-v3 (cropped) + agents-data.js", "Kick on each row"),
    ("11.0 to 15.5", "02 BRAND BRAIN", "One Brand Brain. Six files your agents read first: products, audience, voice, offers, claims, learnings.",
     "02 · Brand Brain, 6 editable ledgers", "Real folder recording: 01-BRAND-BRAIN with its six CSVs, punch-in on the file names.", "site: brain-navigation-v3.mp4", ""),
    ("15.5 to 20.0", "03 INSIDE AN AGENT", "Every agent ships with instructions, prompts, workflows, examples and a review scorecard.",
     "03 · Inside every agent", "Real folder recording of one agent package, cropped to its sub-folders (agent, prompts, workflows, examples, review, evals). Title bar cropped out.", "site: examples-navigation-v3.mp4 (cropped)", ""),
    ("20.0 to 23.5", "04 SETUP", "Setup guides for ChatGPT, Claude, Codex, Hermes and OpenClaw.",
     "04 · 5 host setup guides", "Real recording of 04-HOST-PACKS, the five host folders.", "site: guides-navigation-v3.mp4", ""),
    ("23.5 to 28.5", "05 BONUSES", "Plus three bonuses: a 46-record retention vault, four profit workbooks and a 12-month promo calendar.",
     "05 · 3 operating bonuses", "Retention vault recording, then the three bonus renders (retention kit, workbooks, promotion calendar) whip in on the beat.", "site: bonuses-navigation-v3.mp4 + bonus images", "Build to the drop"),
    ("28.5 to 32.0", "PRICE", "Itemized at ₹75,889. Yours for ₹699. Once.",
     "₹75,889 itemized value → ₹699 once", "Strike-through, then ₹699 slams in exactly on the drop.", "HyperFrames", "DROP 2 on the slam"),
    ("32.0 to 35.0", "CTA", "No subscription. Works in ChatGPT, Claude and Codex. ecomagents dot ai.",
     "ecomagents.ai", "End card with the bundle box.", "HyperFrames", "Hook melody returns, rings out"),
]

# ---------------------------------------------------------------- video 3, 4
V3_HOOKS = [
    ("Your ChatGPT is a stranger to your brand. Let me fix that in thirty seconds.", [10, 8, 8, 8, 8, 8], "Pain + promise of speed. Winner."),
    ("If you run a Shopify brand, stop writing ad briefs from a blank ChatGPT.", [9, 7, 7, 6, 7, 6], "v1 line. Good audience callout, weaker tension. Kept as line 2."),
    ("Here's the ₹699 folder D2C founders keep asking me about.", [8, 8, 8, 7, 8, 7], "Social curiosity, but implies demand we can't show yet. Dropped."),
]
V3 = [
    ("0 to 3", "HOOK", "Your ChatGPT is a stranger to your brand. Let me fix that in thirty seconds.", "Presenter to camera, phone selfie framing."),
    ("3 to 7", "WHO", "If you're a D2C founder, an ecommerce team or a performance marketer, this is for you.", "Presenter; audience chips pop beside her."),
    ("7 to 14", "WHAT", "This is Ecom Agent OS. Sixteen growth agents, plus a Brand Brain that remembers your products, your voice and your offers.", "Cut to the bundle box and the Brand Brain folder recording; her voice continues."),
    ("14 to 22", "PROOF", "Give an agent one product link, and it writes the hooks, the briefs and the image prompts. You review everything before it goes live.", "Video 1's chat demo and ad grid as B-roll."),
    ("22 to 28", "OFFER", "All sixteen agents. ₹699, once. No subscription.", "Back on her face; ₹699 graphic."),
    ("28 to 31", "CTA", "Link's at ecomagents dot ai.", "End card."),
]
V4_NOTES = [
    "Script and storyboard stay as approved: https://farooqchisty-hub.github.io/ecomagents-ads/c4/",
    "Hook fix: a meme-style super on the first frame, \"Every D2C founder at 2am:\", so the audience is named before Maya speaks. Same super pattern for global: \"Every ecommerce founder at 2am:\".",
    "BLOCKER found in production: Replicate's Seedance 2.0 rejected every first frame showing a photoreal face as \"sensitive\" (error E005). Only the over-the-shoulder screen shot rendered. Fix: test the same keyframes on Veo 3.1 (on the same approved Replicate account, image-to-video with native dialogue), one unit first, before re-running all nine. Veo costs more per second, so the all-in estimate moves to about $30 to 45.",
]

MUSIC = [
    ("Video 1 (voice-led demo)", "Warm, catchy modern lo-fi house, 118 BPM, bright plucked synth hook you could hum, soft four-on-the-floor, ducked about 12 dB under the voice, a short riser into the ad reveal at 24s, resolves on the end card. Think a polished tech-creator explainer, not a corporate bed."),
    ("Video 2 (what's inside)", "Punchy, catchy electro-pop / house, 124 BPM, a vocal-chop or whistle hook in the first two bars, cuts land on the beat, drum fill into a hard drop exactly on the ₹699 slam at 28.5s, hook melody returns on the end card. Confident, not cheesy."),
    ("How it gets made", "ElevenLabs Music on the approved Replicate account, composed to the locked edit in sections so there are no restarts. I generate 3 options per video, you pick by ear on a review page before the final mix. The v1 synth bed is scrapped."),
]
VOICE = [
    "Videos 1 and 2 share one brand narrator: a young adult, confident, conversational creator voice (ElevenLabs v3), US English for the global cut.",
    "Optional India cut: the same script in an Indian English voice, since the price is in rupees. Same visuals, 1 extra VO pass, about $0.10.",
    "Product name read as \"EE-kom AY-jent oh-ESS\" and checked with two transcribers on the isolated voice, as with every brand word.",
    "Captions burned in, word-timed to the voice, 64px+ on a 1080 wide frame, kept out of the bottom 300px (Reels UI).",
]
RULES = [
    "Audience named in the first 5 seconds of every video: D2C founders, ecommerce teams, performance marketers.",
    "Every \"what's inside\" visual comes from the landing page's own recordings and renders. Nothing invented.",
    "The agent-folder recordings on the site show the original edition's folder names, which don't match today's 16 agents (the site discloses this). Video 2 only shows those clips cropped, and lists the current names as graphics. Best fix: send me the current zip and I record a fresh 60 second folder tour.",
    "No results claims: no ROAS, revenue or time-saved numbers. \"10ROAS\" appears only as the agent's name.",
    "Demo output in video 1 is labelled \"Demo brand, illustrative example\". No testimonials anywhere until real reviews exist.",
    "No third-party logos (Shopify, Meta, OpenAI and so on) in the ads; host names as plain text only, so nothing implies an endorsement.",
    "No em or en dashes on screen.",
]
COST = [
    ("Video 1: voiceover + 3 music options + re-render", "about $3"),
    ("Video 2: voiceover + 3 music options + render, 3 aspect ratios", "about $3"),
    ("Video 3: presenter identity re-roll (she reads older than 25 right now) + lip-synced clips", "about $8 to 12"),
    ("Video 4: Veo test unit, then 9 units + score", "about $30 to 45"),
    ("Spent so far", "about $7"),
]

def hooks_table(rows):
    head = "".join(f"<th>{c}</th>" for c in CRIT)
    out = []
    for i, (h, s, why) in enumerate(sorted(rows, key=lambda r: -sum(r[1]))):
        tot = sum(s)
        cls = " class='win'" if i == 0 else ""
        out.append(f"<tr{cls}><td class='hk'>{e(h)}<div class='m'>{e(why)}</div></td>" + "".join(f"<td class='n'>{x}</td>" for x in s) + f"<td class='n'><b>{tot}</b>/60</td></tr>")
    return f"<div class='tw'><table><tr><th>Hook</th>{head}<th>Total</th></tr>{''.join(out)}</table></div>"

def script_table(rows):
    out = []
    for t, beat, vo, ost, vis, asset, snd in rows:
        out.append(f"<tr><td class='t'><b>{e(t)}s</b><br><span class='chip'>{e(beat)}</span></td><td><p class='vo'>“{e(vo)}”</p></td><td><b>{e(ost)}</b><p class='m'>{e(vis)}</p></td><td class='m'>{e(asset)}{('<br><i>' + e(snd) + '</i>') if snd else ''}</td></tr>")
    return f"<div class='tw'><table><tr><th>Time</th><th>Voiceover</th><th>On screen · picture</th><th>Asset · sound</th></tr>{''.join(out)}</table></div>"

def v3_table(rows):
    return "<div class='tw'><table><tr><th>Time</th><th>Line</th><th>Picture</th></tr>" + "".join(
        f"<tr><td class='t'><b>{e(t)}s</b><br><span class='chip'>{e(b)}</span></td><td><p class='vo'>“{e(l)}”</p></td><td class='m'>{e(p)}</td></tr>" for t, b, l, p in rows) + "</table></div>"

ASSETS = [
    ("growth-agents-v4", "Bundle box shot", "Hero product visual: 16 numbered agent books + Brand Brain, Setup Guides, Work Resources, 3 Bonuses. Videos 1, 2, 3."),
    ("brain-navigation-v3", "Brand Brain folder (recording, 6.8s)", "Current. The six ledgers by name. Videos 1, 2, 3."),
    ("examples-navigation-v3", "Inside one agent (recording, 6.8s)", "Original-edition title bar; crop to the sub-folders. Video 2."),
    ("guides-navigation-v3", "Host packs (recording, 9.6s)", "ChatGPT, Claude, Codex, Hermes, OpenClaw folders. Video 2."),
    ("bonuses-navigation-v3", "Retention vault (recording, 9.2s)", "Current bonus files. Video 2."),
    ("agents-navigation-v3", "Agent folders (recording, 8.1s)", "Original-edition names: cropped insert only."),
    ("bonus-retention-vault", "Retention kit render", "Video 2 bonus beat."),
    ("bonus-growth-workbooks", "Profit workbooks render", "Video 2 bonus beat."),
    ("bonus-promotion-calendar", "Promotion calendar render", "Video 2 bonus beat."),
]
assets = "".join(f"<figure><img loading='lazy' src='img/{k}.jpg' alt=''><figcaption><b>{e(n)}</b><br>{e(d)}</figcaption></figure>" for k, n, d in ASSETS)
lst = lambda xs: "<ul>" + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>"
cards = lambda xs: "<div class='grid'>" + "".join(f"<div class='card'><h4>{e(a)}</h4><p>{e(b)}</p></div>" for a, b in xs) + "</div>"

page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ecom Agent OS Ad Plan</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Hanken+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f4f1e8;--card:#fcfbf6;--ink:#16150f;--muted:#5d5d53;--line:#d2d1c5;--lime:#cdf13b;--olive:#455517}}
@media (prefers-color-scheme:dark){{:root{{--bg:#121210;--card:#1b1b18;--ink:#eeece4;--muted:#a3a397;--line:#2f2f2a;--lime:#cdf13b;--olive:#b8d36a}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 'Hanken Grotesk',system-ui,sans-serif}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 16px}}header{{padding:40px 0 22px;border-bottom:1px solid var(--line)}}
h1,h2{{font-family:'Bricolage Grotesque',sans-serif;letter-spacing:-.5px}}h1{{font-size:clamp(30px,5vw,48px);margin:6px 0}}h2{{font-size:26px;margin:44px 0 10px}}h3{{margin:26px 0 8px;font-size:18px}}h4{{margin:0 0 6px}}
.chip{{display:inline-block;background:var(--lime);color:#16150f;font-size:11px;font-weight:700;letter-spacing:.4px;padding:3px 8px;border-radius:99px}}
.m{{color:var(--muted);font-size:13px;margin:4px 0 0}}.toc a{{color:var(--olive);margin-right:14px;font-weight:600;text-decoration:none}}
.tw{{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--card)}}table{{border-collapse:collapse;width:100%;min-width:720px}}
th{{text-align:left;font-size:12px;color:var(--muted);padding:10px 12px;border-bottom:1px solid var(--line)}}td{{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}}
td.n{{text-align:center;white-space:nowrap}}td.t{{white-space:nowrap}}td.hk{{min-width:320px}}tr.win td{{background:rgba(205,241,59,.22)}}
.vo{{margin:0;font-weight:600}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}}.card p{{margin:0;font-size:14px}}
.assets{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}}figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
figure img{{width:100%;height:150px;object-fit:cover;display:block;background:#222}}figcaption{{padding:10px 12px;font-size:13px}}
.fix{{background:var(--card);border:1px solid var(--line);border-left:0;border-radius:12px;padding:14px 16px}}.fix li{{margin:4px 0}}
.gate{{background:var(--card);border:2px solid var(--ink);border-radius:14px;padding:16px 18px;margin:36px 0 60px}}
</style></head><body>
<header><div class="wrap"><span class="chip">PLAN V2 · FOR APPROVAL</span>
<h1>Ecom Agent OS video ads</h1>
<p>Rewritten after your notes on videos 1 and 2. Every video now names who it is for in the first 5 seconds, carries a voiceover, opens on a scored hook, and is built from the landing page's own recordings and renders. Audience everywhere: {e(AUD)}.</p>
<div class="toc"><a href="#fb">Your notes</a><a href="#assets">Assets</a><a href="#v1">Video 1</a><a href="#v2">Video 2</a><a href="#v3">Video 3</a><a href="#v4">Video 4</a><a href="#music">Music & voice</a><a href="#rules">Rules</a><a href="#cost">Cost</a></div></div></header>
<div class="wrap">
<h2 id="fb">Your notes, and what changes</h2>
<div class="fix"><ul>
<li><b>Video 1 needs a voiceover narrating what's happening.</b> Added: a narrator walks through problem, step 1, step 2, proof, offer. Highlights are re-timed to land on the spoken word.</li>
<li><b>Say who it's for.</b> All four videos name D2C founders, ecommerce teams and performance marketers inside 5 seconds, spoken and on screen.</li>
<li><b>The hook is weak.</b> 8 hooks written for video 1 and 6 for video 2, scored on 6 criteria; the winner opens, the next two are A/B variants.</li>
<li><b>Video 2 should be a compilation of what's inside the files.</b> Rebuilt as a "what's inside" unboxing: agents, Brand Brain, inside an agent, setup guides, bonuses, then the price, all from the real folder recordings on the landing page.</li>
<li><b>Video 2 music is terrible.</b> Scrapped. New direction below; you pick from 3 options by ear before the mix.</li>
</ul></div>

<h2 id="assets">Landing page assets I'll use</h2><div class="assets">{assets}</div>

<h2 id="v1">Video 1 · "Generic AI" demo, 38s, voice-led</h2>
<p>Problem, fix in two steps, proof on screen, offer. The demo is the proof, the voice makes it make sense.</p>
<h3>Hooks, scored</h3>{hooks_table(V1_HOOKS)}
<h3>Script</h3>{script_table(V1)}
<p class="m">Deliverables: 9:16 master, 4:5, 1:1, plus hook variants B and C as separate files.</p>

<h2 id="v2">Video 2 · "What's inside", 35s, compilation</h2>
<p>An unboxing of the download, cut to the beat: every section of the bundle shown from its real folder recording, ending on the price drop.</p>
<h3>Hooks, scored</h3>{hooks_table(V2_HOOKS)}
<h3>Script</h3>{script_table(V2)}
<p class="m">Deliverables: 9:16, 4:5, 1:1, a 15s cutdown (hook, agents, brain, price, CTA) and a 6s price bumper.</p>

<h2 id="v3">Video 3 · Presenter, 31s</h2>
<p>An adult presenter (23 to 25) explaining the product, never posing as a customer. The first identity renders read 28 to 35, so she gets re-rolled younger-looking before any video spend.</p>
<h3>Hooks, scored</h3>{hooks_table(V3_HOOKS)}
<h3>Script</h3>{v3_table(V3)}

<h2 id="v4">Video 4 · The 2am Founder</h2>{lst(V4_NOTES)}

<h2 id="music">Music and voice</h2>{cards(MUSIC)}<h3>Voice</h3>{lst(VOICE)}
<h2 id="rules">Rules for all four</h2>{lst(RULES)}
<h2 id="cost">Cost</h2><div class="tw"><table><tr><th>Item</th><th>Estimate</th></tr>{''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in COST)}</table></div>

<div class="gate"><b>Decisions for you:</b><ol>
<li>Approve the scripts and the winning hooks (or swap in a variant).</li>
<li>Narrator: US English only, or also an Indian English cut?</li>
<li>Can you send the current bundle zip? A fresh 60s folder tour of today's 16 agents makes video 2 fully accurate.</li>
</ol></div>
</div></body></html>"""
assert "—" not in page and "–" not in page, "no em or en dashes"
open(os.path.join(HERE, "index.html"), "w").write(page)
print("ok")
