#!/usr/bin/env python3
"""Storyboards for concepts 5 (AI avatar value stack) and 6 (Go For Launch, cinematic harness).
Same playbook as the Box, Box, Brenda 60s storyboard: beats, how it's built, screenplay, music and sound
as prompted, motion graphics track, voice, keyframes + contact sheet, checks, cost, gate."""
import html, os
e = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))

STYLE = """
:root{--bg:#f4f1e8;--card:#fcfbf6;--ink:#16150f;--muted:#5d5d53;--line:#d2d1c5;--lime:#cdf13b;--olive:#455517}
@media (prefers-color-scheme:dark){:root{--bg:#121210;--card:#1b1b18;--ink:#eeece4;--muted:#a3a397;--line:#2f2f2a;--olive:#b8d36a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 'Hanken Grotesk',system-ui,sans-serif}
.wrap{max-width:1160px;margin:0 auto;padding:0 16px 70px}header{padding:38px 0 20px;border-bottom:1px solid var(--line)}
h1,h2,h3{font-family:'Bricolage Grotesque',sans-serif;letter-spacing:-.4px}h1{font-size:clamp(30px,5vw,48px);margin:6px 0}h2{font-size:25px;margin:42px 0 10px}h3{font-size:18px;margin:22px 0 6px}
.chip{display:inline-block;background:var(--lime);color:#16150f;font-size:11px;font-weight:700;letter-spacing:.4px;padding:3px 8px;border-radius:99px;margin-right:6px}
.m{color:var(--muted);font-size:13px}.toc a{color:var(--olive);font-weight:600;margin-right:14px;text-decoration:none}
.beats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}
.beat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}.beat b{display:block;font-family:'Bricolage Grotesque';font-size:17px;margin-bottom:4px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}.card h4{margin:0 0 6px}.card p{margin:0;font-size:14px}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--card)}table{border-collapse:collapse;width:100%;min-width:760px}
th{text-align:left;font-size:12px;color:var(--muted);padding:10px 12px;border-bottom:1px solid var(--line)}td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;font-size:14px}
td.t{white-space:nowrap}td img{width:92px;border-radius:8px;display:block}
.line{margin:0 0 4px}.line b{font-weight:700}.del{color:var(--muted);font-size:12px}
.contact{width:100%;border-radius:12px;border:1px solid var(--line);display:block}
.cast{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}.cast figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.cast img{width:100%;display:block}.cast figcaption{padding:10px 12px;font-size:13px}
ul{padding-left:18px}li{margin:4px 0}.gate{background:var(--card);border:2px solid var(--ink);border-radius:14px;padding:16px 18px;margin:36px 0 0}
"""

def page(title, chip, sub, beats, how, shots, music, mg, voice, cast, contact, checks, cost, gate, extra=""):
    bh = "".join(f"<div class='beat'><b>{e(a)}</b>{e(b)}</div>" for a, b in beats)
    hh = "".join(f"<div class='card'><h4>{e(a)}</h4><p>{e(b)}</p></div>" for a, b in how)
    rows = []
    for i, s in enumerate(shots, 1):
        t, beat, pic, cam, unit, lines, gfx, kf = s
        ls = "".join(f"<p class='line'><b>{e(w)}</b>: “{e(l)}” <span class='del'>({e(d)})</span></p>" for w, l, d in lines) or "<span class='m'>no dialogue</span>"
        img = f"<img src='{kf}' alt=''>" if kf else ""
        rows.append(f"<tr><td class='t'><b>{i}. {e(t)}s</b><br><span class='chip'>{e(beat)}</span></td><td>{img}</td><td>{e(pic)}<br><span class='m'>{e(cam)} · {e(unit)}</span></td><td>{ls}</td><td class='m'>{e(gfx)}</td></tr>")
    mh = "".join(f"<p><b>{e(a)}</b> {e(b)}</p>" for a, b in music)
    mgh = "".join(f"<tr><td class='t'>{e(a)}</td><td>{e(b)}</td><td class='m'>{e(c)}</td></tr>" for a, b, c in mg)
    ch = "".join(f"<figure><img loading='lazy' src='{s}' alt=''><figcaption><b>{e(n)}</b><br>{e(d)}</figcaption></figure>" for s, n, d in cast)
    words = sum(len(l.split()) for s in shots for _, l, _ in s[5])
    total = sum(c for _, c in cost)
    out = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Hanken+Grotesk:wght@400;600;700&display=swap" rel="stylesheet"><style>{STYLE}</style></head><body><div class="wrap">
<header><span class="chip">STORYBOARD · FOR APPROVAL</span><span class="chip">{e(chip)}</span><h1>{e(title)}</h1><p>{e(sub)} {words} words of dialogue.</p>
<div class="toc"><a href="#story">Story</a><a href="#how">How it's built</a><a href="#screen">Screenplay</a><a href="#music">Music and sound</a><a href="#mg">Motion graphics</a><a href="#kf">Keyframes</a><a href="#checks">Checks</a><a href="#cost">Cost</a></div></header>
<h2 id="story">The story in beats</h2><div class="beats">{bh}</div>
<h2 id="how">How it's built</h2><div class="grid">{hh}</div>
{extra}
<h2 id="screen">Screenplay <span class="m">{len(shots)} shots</span></h2>
<div class="tw"><table><tr><th>Time · beat</th><th>Frame</th><th>Picture · camera · unit</th><th>Dialogue (delivery)</th><th>Motion graphics · added sound</th></tr>{''.join(rows)}</table></div>
<h2 id="music">Music and sound, as prompted</h2>{mh}
<h2 id="mg">Motion graphics track</h2><p class="m">Anchored to the spoken word; never stacked; clear of faces.</p>
<div class="tw"><table><tr><th>At</th><th>Cue</th><th>Lands on</th></tr>{mgh}</table></div>
<h2>Voice</h2><ul>{''.join(f'<li>{e(v)}</li>' for v in voice)}</ul>
<h2 id="kf">Cast and keyframes</h2><div class="cast">{ch}</div>
<h3>Contact sheet</h3><img class="contact" src="{contact}" alt="contact sheet">
<h2 id="checks">Checks before you see it</h2><ul>{''.join(f'<li>{e(v)}</li>' for v in checks)}</ul>
<h2 id="cost">Cost</h2><div class="tw"><table><tr><th>Item</th><th>Cost</th></tr>{''.join(f'<tr><td>{e(a)}</td><td>${c:.2f}</td></tr>' for a, c in cost)}<tr><td><b>Total</b></td><td><b>about ${total:.0f}</b></td></tr></table></div>
<div class="gate"><b>Gate:</b> {e(gate)}</div></div></body></html>"""
    assert "—" not in out and "–" not in out, title
    return out

# ============================================================== CONCEPT 6
C6_BEATS = [
    ("Hook", "Black Friday, two minutes out. A launch control room, sixteen consoles, total silence."),
    ("Setup", "Riley, the founder, is Flight: \"Go, no-go for launch.\""),
    ("Build", "Seven stations call in, each with what their agent got ready: objections, hooks, bundles, checkout, recovery, care, profit."),
    ("Turn", "Walt: the Brand Brain is loaded, every station reads from the same page. Riley: \"Then it's my call.\""),
    ("Payoff", "She presses the key. Three, two, one. Store is live. First order."),
    ("Button", "\"What did this crew cost?\" \"Less than your lunch.\""),
    ("CTA", "Your launch crew. 16 agents, one Brand Brain, ₹699 once. You give the final go."),
]
C6_HOW = [
    ("Why mission control", "A go/no-go poll is a genre device that lets seven agents each say what they did in one line, so the product's range is shown, not listed. The founder keeps the final go, which is how the product works: agents prepare, you approve."),
    ("Generation", "Veo 3.1 image-to-video on the approved Replicate account (Seedance blocks photoreal faces). 15 units from 14 keyframes, 4 to 8 s each, native dialogue, generated without music."),
    ("One world", "Single location, so plain cuts; no split screen. The poll is a rhythm of matched medium shots, one per console, each cut on the word \"go\"."),
    ("Graphics", "Console labels (CUSTOMER VOICE, CREATIVE, OFFERS…) and the countdown clock are added in HyperFrames, because generated screens can't hold legible text. Every screen in the plates is abstract and blank."),
    ("Brand words", "The product name is never spoken; it lands on the end card. \"Brand Brain\" is plain English and gets a transcriber check on the isolated voice."),
    ("Fictional world", "Halden Outdoor Co., a made-up outdoor gear brand. No real logos; every frame is scanned for leaks."),
]
U = lambda n, d: f"unit {n}, {d}s"
C6_SHOTS = [
    ("0.0 to 3.5", "hook", "The dark launch control room, 16 consoles glowing, the big wall screen deep blue.", "wide from the back, slow push in", U("A", 6), [("PA (off)", "T-minus two minutes to Black Friday.", "calm, clinical, NASA flat")], "Countdown clock T-02:00 top band; super 'Black Friday. 2 minutes out.' · room hum", "../c6/kf/k01_room.jpg"),
    ("3.5 to 7.5", "setup", "Riley at the flight director desk on the top tier, headset on, scanning the room.", "medium close, locked", U("B", 6), [("Riley", "All stations, this is Flight. Go, no-go for launch.", "steady, low, in command")], "Label FLIGHT · RILEY, FOUNDER", "../c6/kf/k02_riley.jpg"),
    ("7.5 to 10.5", "build", "Mustard-cardigan controller turns to her mic.", "medium, locked", U("C1", 4), [("Customer Voice", "Customer Voice, go. Every ad answers the sizing question.", "crisp, confident")], "Console label CUSTOMER VOICE · tick on 'go'", "../c6/kf/k03_ctrl1.jpg"),
    ("10.5 to 13.5", "build", "Navy-hoodie controller leans into his mic.", "medium, locked", U("C2", 4), [("Creative", "Creative, go. Twelve hooks, in our customers' own words.", "quick, a little cocky")], "CREATIVE · 12 HOOKS", "../c6/kf/k04_ctrl2.jpg"),
    ("13.5 to 16.5", "build", "Black-turtleneck controller, a crisp nod.", "medium, locked", U("C3", 4), [("Offers", "Offers, go. Bundle priced to protect margin.", "precise")], "OFFERS · BUNDLE", "../c6/kf/k05_ctrl3.jpg"),
    ("16.5 to 19.5", "build", "Olive-overshirt controller sits up.", "medium, locked", U("C4", 4), [("Landing Page", "Landing page, go. Checkout friction, fixed.", "matter-of-fact")], "LANDING PAGE · CHECKOUT", "../c6/kf/k06_ctrl4.jpg"),
    ("19.5 to 22.5", "build", "Burgundy-sweater controller, hand on the mic boom.", "medium, locked", U("C5", 4), [("Recovery", "Recovery, go. Email, SMS and WhatsApp, armed.", "energetic")], "RECOVERY · 3 CHANNELS", "../c6/kf/k07_ctrl5.jpg"),
    ("22.5 to 25.0", "build", "Denim-jacket controller, a quick thumbs up.", "medium, locked", U("C6", 4), [("Care", "Care, go. Shipping replies, drafted.", "relaxed")], "CARE · REPLIES", "../c6/kf/k08_ctrl6.jpg"),
    ("25.0 to 28.5", "build", "White-shirt controller, glasses on.", "medium, locked", U("C7", 4), [("Profit", "Profit, go. Break-even ROAS is two point one.", "precise, dry")], "PROFIT · BREAK-EVEN 2.1", "../c6/kf/k09_ctrl7.jpg"),
    ("28.5 to 34.0", "turn", "Walt at the central console, the printed Brand Brain binder open beside him.", "medium, slow push", U("D", 6), [("Walt", "Brand Brain's loaded. Every station is reading from the same page.", "unhurried, dry warmth")], "BRAND BRAIN · 6 FILES · LOADED", "../c6/kf/k10_walt.jpg"),
    ("34.0 to 39.5", "turn", "Riley looks over the room, takes a breath.", "medium close, slow push", U("E", 6), [("Riley", "Then it's my call.", "quiet"), ("Riley", "We are go for launch.", "firm, rising")], "none · score drops to a held note", "../c6/kf/k02_riley.jpg"),
    ("39.5 to 41.5", "payoff", "Her hand presses the lime backlit key.", "extreme close insert", U("F", 4), [], "added: deep key clunk (the decision must register)", "../c6/kf/k11_key.jpg"),
    ("41.5 to 47.0", "payoff", "The wall screen floods lime, the room silhouetted, people rising.", "wide from the floor", U("G", 6), [("PA (off)", "Three. Two. One. Store is live.", "calm, then a hint of relief")], "STORE LIVE on the wall band · score lifts on 'live'", "../c6/kf/k12_wall.jpg"),
    ("47.0 to 51.0", "payoff", "Quiet relief, fist bumps; Riley smiles and slips her headset off.", "medium wide", U("H", 4), [], "First order toast 'Halden · order #1' · added: one soft order chime", "../c6/kf/k13_react.jpg"),
    ("51.0 to 56.0", "button", "The navy-hoodie kid leans to Walt and whispers.", "two-shot, locked", U("I", 6), [("Creative", "What did this crew cost?", "whisper"), ("Walt", "Less than your lunch.", "dry, tiny smile")], "none", "../c6/kf/k14_button.jpg"),
    ("56.0 to 61.0", "CTA", "End card: the bundle box shot on ink.", "HyperFrames", "graphics", [], "Your launch crew. 16 growth agents · One Brand Brain · ₹699 once · You give the final go · ecomagents.ai", ""),
]
C6_MUSIC = [
    ("0 to 7.5 s:", "cold open on a low pulse at 120 bpm with a ticking-clock motif, one tick per beat, under the PA line; room hum and console beeps native."),
    ("7.5 to 28.5 s:", "the poll: each \"go\" adds a layer (kick, then bass, then strings, then hats), so the room's readiness is heard building; the score ducks under every line and swells between them."),
    ("28.5 to 39.5 s:", "the tick stops on Walt; a suspended held pad; it thins to almost nothing on \"Then it's my call.\""),
    ("39.5 to 47 s:", "the key clunk lands on silence; a riser under the countdown; on \"live\" the full score opens into a warm, anthemic lift."),
    ("47 to 61 s:", "the lift resolves to a warm groove under the button, one final hit on the end card that rings out. One continuous ElevenLabs piece composed to the locked cut, in three sections, never restarting."),
    ("Added sounds (only what must register):", "the key clunk and one order chime. Console labels, the countdown and the end card stay silent."),
]
C6_MG = [
    ("0.2s", "Countdown clock T-02:00, top band, ticking down", "the PA line"),
    ("3.6s", "Lower label FLIGHT · RILEY, FOUNDER", "her first word"),
    ("7.6 to 25.1s", "Console label per station, slides in from the left edge, clear of faces", "each station's name"),
    ("8 to 28s", "Readiness bar 'GO 1/7 … 7/7', top right, one segment lights per 'go'", "each 'go'"),
    ("28.8s", "BRAND BRAIN · 6 FILES · LOADED chip beside the binder", "'Brand Brain'"),
    ("43.5s", "STORE LIVE band across the top of the lime wall", "'live'"),
    ("47.6s", "Order toast 'Halden · order #1'", "the chime"),
    ("56.0s", "End card", "after the button"),
]
C6_VOICE = [
    "Riley speaks in units B and E. Veo has no voice reference, so I generate 2 takes of each and keep the closest pair; if they still differ, unit E's line is re-voiced with ElevenLabs voice changer matched to B.",
    "Walt speaks in D and I: same approach.",
    "Each controller speaks once, on camera, in their own unit, so no cross-unit match is needed.",
    "The PA is off camera, so its lines can be re-spaced in the edit; on-camera lines are never re-timed.",
]
C6_CHECKS = [
    "Two takes for the speaking units; every take transcribed; \"Brand Brain\", \"ROAS\" and \"WhatsApp\" checked on the isolated voice.",
    "Frame scan every second for real brands on screens, warped hands on the key, faces drifting between the poll shots.",
    "Claims: no results numbers about the product. \"Break-even ROAS is two point one\" is the fictional store's own number. No testimonials.",
    "Runtime 61 s with the end card, loudness about -14 LUFS, share copy under 30 MB.",
]

# ============================================================== CONCEPT 5
C5_BEATS = [
    ("Hook", "\"Before you pay for one more AI tool, look at this.\" Eight subscriptions stack up to $468 a month."),
    ("Who", "D2C founders, ecommerce teams, performance marketers."),
    ("What", "Ecom Agent OS: 16 agents inside ChatGPT, Claude or Codex, plus a Brand Brain (real folder recording)."),
    ("What they do", "Animated agent cards, one per job, timed to his words."),
    ("Value", "$5,616 a year in single-job tools vs ₹699 once."),
    ("Bonuses", "Retention vault, profit workbooks, promo calendar (the site's mockups), and the swipe file free with any add-on."),
    ("CTA", "16 agents, one Brand Brain, ₹699 once, ecomagents.ai."),
]
C5_HOW = [
    ("Presenter", "Jay, a new adult presenter (about 28), so this doesn't look like the video 3 presenter. Face shots are lip-synced with OmniHuman 1.5 on Replicate (the model that won the video 3 test) from ElevenLabs v3 voice."),
    ("Edit", "HyperFrames: presenter full-frame on the hook, audience and CTA; a circular picture-in-picture of him over the product sections, so his face never leaves for long."),
    ("Real product", "Every product visual is from the landing page: the bundle box render, the Brand Brain and bonus folder recordings, the three bonus mockups and the swipe-file gift mockup."),
    ("Animations", "Price stack cascade and counter, agent ability cards that flip on the spoken verb, a value table that totals, a strike-through VS card, bonus whip-ins, a FREE sticker slam."),
    ("Value math, honestly", "Eight tool categories at entry monthly prices (Oct 2026), shown as categories, never brand names, with a footnote: some tools do more in places, and the agents run on the viewer's own AI plan."),
    ("Length", "About 57 s, voice-driven."),
]
C5_SHOTS = [
    ("0.0 to 3.0", "hook", "Jay to camera, hand up like he's stopping you.", "selfie, chest up", "lip-sync 1", [("Jay", "Before you pay for one more AI tool, look at this.", "knowing, a little conspiratorial")], "Subscription cards cascade down the right side, prices in red", "frames/f01.jpg"),
    ("3.0 to 7.0", "hook", "Same, the stack completes.", "selfie", "lip-sync 1", [("Jay", "Eight single-job AI tools. Four hundred and sixty-eight dollars. Every month.", "deadpan, counting it out")], "Counter ticks to $468/mo · added: register tick on the total", "frames/f01.jpg"),
    ("7.0 to 11.5", "who", "Jay, gesturing to the chips.", "selfie", "lip-sync 1", [("Jay", "If you run a D2C brand, an ecommerce team or ad accounts, there's a cheaper way.", "direct")], "Audience chips D2C founders / Ecommerce teams / Performance marketers", "frames/f02.jpg"),
    ("11.5 to 15.0", "what", "Bundle box render, Jay in a circle bottom left.", "graphic + PiP", "lip-sync 2", [("Jay", "Ecom Agent OS. Sixteen growth agents that work inside ChatGPT, Claude or Codex,", "warm, explaining")], "16 agents + a Brand Brain headline", "frames/f03.jpg"),
    ("15.0 to 18.5", "what", "The real Brand Brain folder recording, punch in on the six files.", "screen recording + PiP", "lip-sync 2", [("Jay", "plus a Brand Brain they all read first.", "warm")], "Six ledger chips pop: Products, Audience, Voice, Offers, Claims, Learnings", "frames/f04.jpg"),
    ("18.5 to 25.5", "what they do", "Agent ability cards (acquire lane), each flips on its verb.", "graphic", "voice continues", [("Jay", "They mine your reviews for objections, track competitor ads, write static ads and UGC scripts, read your Meta and Google numbers,", "brisk, listing")], "6 cards: Customer Voice, Competitor Tracker, Static Ad Generator, UGC Video, Performance Marketing, SEO/GEO", "frames/f05.jpg"),
    ("25.5 to 32.5", "what they do", "Second card set (convert, retain, operate).", "graphic", "voice continues", [("Jay", "price bundles around your margin, find checkout friction, draft recovery on email, SMS and WhatsApp, and reconcile your real profit.", "brisk, landing it")], "6 cards: Offers, Landing Pages CRO, Recovery, Repeat Purchase, Profit, Care", "frames/f06.jpg"),
    ("32.5 to 36.0", "value", "The tool table, rows fill, total lands.", "graphic", "voice continues", [("Jay", "Those tools add up to over five and a half thousand dollars a year.", "matter-of-fact")], "Table of 8 categories → Every month $468 · footnote", "frames/f07.jpg"),
    ("36.0 to 39.5", "value", "VS card: $5,616 struck through vs ₹699 once.", "graphic", "voice continues", [("Jay", "This is six hundred and ninety-nine rupees. Once.", "slow, letting it land")], "Strike on $5,616 · ₹699 slams · added: one low hit on the slam", "frames/f08.jpg"),
    ("39.5 to 45.0", "bonuses", "Three bonus mockups whip in; Jay PiP.", "graphic + PiP", "lip-sync 3", [("Jay", "You also get three bonuses: a retention vault, profit workbooks and a twelve-month promo calendar.", "upbeat")], "Retention vault / Profit workbooks / 12-month promo calendar · ₹5,997 value", "frames/f09.jpg"),
    ("45.0 to 49.0", "bonuses", "The swipe-file gift mockup, FREE sticker slams.", "graphic", "voice continues", [("Jay", "Add any add-on at checkout, and the Meta ads swipe file is free.", "light, a little sly")], "FREE sticker + 'with any add-on at checkout'", "frames/f10.jpg"),
    ("49.0 to 54.0", "CTA", "Jay to camera, pointing down.", "selfie", "lip-sync 4", [("Jay", "Sixteen agents, one Brand Brain, six ninety-nine once. It's at ecomagents dot ai.", "warm, clear")], "₹699 once sticker", "frames/f11.jpg"),
    ("54.0 to 57.5", "end", "End card on ink: bundle box, price, URL.", "graphic", "", [], "16 growth agents · ₹699 once · 3 bonuses · ecomagents.ai", "frames/f12.jpg"),
]
C5_MUSIC = [
    ("Bed:", "catchy, bright creator-economy pop house around 120 bpm, a hummable plucked hook, ducked about 12 dB under his voice. 3 options generated after the voice is locked; you pick by ear."),
    ("Shape:", "light open under the hook so the voice owns it; a lift as the agent cards start; a breath before the value VS; the hook melody returns on the end card."),
    ("Added sounds (only what must register):", "a register tick when the $468 total lands and one low hit on the ₹699 slam. Card flips, chips and wipes stay silent."),
]
C5_MG = [
    ("0.3 to 6.5s", "Subscription stack: 8 category cards with red prices cascade, counter to $468/mo", "'one more AI tool' to 'every month'"),
    ("7.6s", "Audience chips, one per role", "each role word"),
    ("11.6s", "16 agents + a Brand Brain headline over the bundle render", "'Ecom Agent OS'"),
    ("15.2s", "Brand Brain recording, 6 ledger chips", "'Brand Brain'"),
    ("18.6 to 32.4s", "12 agent ability cards, 2 sets of 6, each flips on its verb", "each verb"),
    ("32.6s", "Tool table rows fill, total $468", "'add up'"),
    ("36.1s", "VS card, strike on $5,616, ₹699 slam", "'six hundred and ninety-nine'"),
    ("39.6s", "Bonus mockups whip in, ₹5,997 value line", "'three bonuses'"),
    ("45.2s", "Swipe file gift + FREE sticker + condition line", "'free'"),
    ("49.2s", "₹699 once sticker beside him", "'six ninety-nine'"),
]
C5_VOICE = [
    "Jay: ElevenLabs v3, a young adult US male voice different from the video 1 narrator, so the ads don't sound like one person. 2 voice candidates rendered on line 1; you pick.",
    "All lines rendered first, word timings measured, then the face clips are lip-synced to those exact files, so the edit is driven by the real voice.",
    "Product name read as \"EE-kom AY-jent oh-ESS\", checked with two transcribers on the voice file.",
]
C5_CHECKS = [
    "Value math: every price is an entry monthly plan from the tool's own pricing (sources below), shown as a category. Footnote on screen. You confirm you're comfortable with the comparison before production.",
    "Swipe file is stated as free with any add-on, which is the site's actual condition. The bonuses are stated as included, which matches the site.",
    "No results claims; the 1,000-orders playbook add-on is deliberately left out because its title reads as a results promise.",
    "Lip sync checked on close mouth crops per clip; blink and eye-closure check (the video 3 weak spot).",
]
C5_SOURCES = [
    ("AI ad copywriter $49", "Jasper Creator, monthly", "https://www.toolradar.com/tools/jasper-ai/pricing"),
    ("Static ad generator $39", "AdCreative.ai Starter, monthly", "https://www.hackceleration.com/labs/adcreativeai-pricing"),
    ("UGC video ad tool $99", "Creatify Pro, monthly", "https://www.creatify.ai/pricing"),
    ("Competitor ad library $59", "Foreplay Basic, monthly", "https://creatify.ai/blog/foreplay-pricing-(2026)-plans-credits-and-what-you-ll-actually-pay"),
    ("SEO content briefs $99", "Surfer Essential, monthly", "https://www.eesel.ai/blog/surfer-seo-pricing"),
    ("Landing page CRO audit $49", "ConvertRocket.ai, monthly", "https://aitoolscoop.com/tool/convertrocket-ai/"),
    ("Profit analytics $35", "TrueProfit Basic, monthly", "https://apps.shopify.com/trueprofit"),
    ("AI support replies $39", "Tidio Lyro, 50 conversations", "https://www.dragapp.com/blog/tidio-pricing/"),
]
c5_extra = ("<h2>The value stack, sourced</h2><p class='m'>Shown in the ad as categories only. Left out on purpose: creator databases and enterprise creative analytics, where the tool does work the agents can't.</p>"
            "<div class='tw'><table><tr><th>Category in the ad</th><th>Price basis</th><th>Source</th></tr>"
            + "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td><a href='{c}'>{e(c.split('/')[2])}</a></td></tr>" for a, b, c in C5_SOURCES)
            + "<tr><td><b>Total $468 / month, $5,616 / year</b></td><td>vs ₹699 once (about $8)</td><td></td></tr></table></div>")

os.makedirs(os.path.join(HERE, "..", "c6"), exist_ok=True)
open(os.path.join(HERE, "c6.html"), "w").write(page(
    "Go For Launch", "Concept 6 · cinematic harness",
    "Black Friday, two minutes out. A launch control room runs a go/no-go poll where every station is one of the agents, and the founder gives the final go. 61 s, 9:16, North American cast.",
    C6_BEATS, C6_HOW, C6_SHOTS, C6_MUSIC, C6_MG, C6_VOICE,
    [("../c6/kf/cast_riley.jpg", "Riley, 34", "Founder of Halden Outdoor Co. (fictional), Flight. Speaks in B and E."),
     ("../c6/kf/cast_walt.jpg", "Walt, early 60s", "Operations lead at the central console; the Brand Brain binder. Speaks in D and I."),
     ("../c6/kf/cast_crew.jpg", "The crew", "Seven speaking controllers, one line each; the rest fill the room.")],
    "../c6/contact.jpg", C6_CHECKS,
    [("Cast cards + 14 keyframes (done)", 4.25), ("Veo 3.1, 15 units, 72 s at 720p (estimate $0.40/s)", 28.80), ("Re-roll budget (2 takes on speaking units)", 14.00), ("Score, 3 options", 1.20), ("Transcription checks", 0.20)],
    "nothing past the keyframes has been spent. Approve, mark changes, or swap a station's line, and production starts with unit B (Riley) as the voice test."))
open(os.path.join(HERE, "c5.html"), "w").write(page(
    "Before One More Tool", "Concept 5 · AI avatar + value stack",
    "An AI presenter breaks down what eight single-job AI tools cost against a ₹699 one-time bundle, shows what the 16 agents actually do with animated cards over the real folder recordings, then the bonuses and the free swipe file. About 57 s, 9:16.",
    C5_BEATS, C5_HOW, C5_SHOTS, C5_MUSIC, C5_MG, C5_VOICE,
    [("../c5/kf/cast_jay.jpg", "Jay, about 28", "Presenter, never a customer. Olive overshirt, home studio.")],
    "../c5/contact.jpg", C5_CHECKS,
    [("Presenter identity + 3 keyframes (done)", 1.00), ("Voice, 9 lines + 2 candidates", 0.25), ("OmniHuman 1.5 lip-sync, about 30 s of face", 6.00), ("Re-roll budget", 4.00), ("Music, 3 options", 1.20), ("Transcription checks", 0.10)],
    "nothing past the keyframes has been spent. Approve the script and the value comparison (or change the categories), and I record the voice first.",
    extra=c5_extra))
print("ok")
