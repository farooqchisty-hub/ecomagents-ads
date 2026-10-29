# v5 motion style test (WS + EA reels)

A style test for approval, not the re-cut. Screenplay, narration, timing and on-screen words are the v3 ones:
captions are parsed word for word (text, page breaks, word times, key words) from the approved `v3/mg/compositions/v3-*.html`,
and every UI string comes from the v3 replica code.

## Files
- `style/01..08_*.png`: 8 style frames, 1080x1920, lossless snapshots of the real compositions (re-shoot: `tools/style_frames.sh`).
  01 WS hook, 02 WS dashboard with tracked box, 03 WS count + byline chips, 04 WS "₹1 / AD" + 5X, 05 EA angles lifted out of ChatGPT,
  06 EA Pawfull ad lands, 07 EA retention flow, 08 WS end card.
- `test_ws.mp4` (20.27 s: hook H1 + body 1, narration ws2_h1 at 0.300 s, ws2_b1 at 5.980 s, as in assembly.json, no music) and `test_ws_115.mp4`.
- `test_ea.mp4` (7.43 s: EA-2 body 2, ea2_b2 placed at -0.014 s as in assembly.json) and `test_ea_115.mp4`.
- `mg/`: the HyperFrames project. `v5lib.py` (design system, captions), `build_ws.py`, `build_ea.py`, `build_sf.py` (style-frame scenes),
  `entry/<name>/` one root per test. Rebuild: `PYTHONDONTWRITEBYTECODE=1 python3 build_ws.py` (etc.), render with
  `npx hyperframes render entry/test_ws -o renders/test_ws_silent.mp4 --quality delivery`, then `python3 ../tools/mix.py`.
- `tools/track_tour.py`: measures the real tour, writes `mg/assets/tour/tour_track.json` + `plate.jpg`.
- `tools/qa_boxes.py`, `tools/static_scan.py`: the QA below. Results in `qa/`.

## Design system
- **World:** one dark "vault" per product (WS deep green on near-black, EA warm olive on near-black). Real library ads float in it at depth.
  The hook flies through it, the body window sits inside it, so the cut is one forward camera move, not a new slide.
- **Type:** Anton for the hook and price slabs (extruded, layered shadow, lines on separate z planes so they parallax), the hero numeral
  "1,169" is filled with the real library ads. Geist 800 (WS) / Inter 800 (EA) for captions and numbers; Playfair italic only for "the".
  Count-ups are odometer reels, not flicker. Captions: words blur in per page, light up on the voice, key words get a marker wiped under them.
- **Colour roles:** void, key light, accent (WS mint #71D793, EA lime #CDF13B), hot yellow #FFE14D only for "steal / price / highlight box",
  red only for the hook numeral. UI replicas keep their own colours.
- **Depth and light:** perspective 1500 to 1900 px, max 7 deg off face-on while text is read (hard cap 12 deg), soft key light, travelling
  light beam, gloss sweeps when something lands, window reflection, blurred background layers, film grain, vignette. DOF for "not chosen".
- **Camera:** always moving under the voice (orbit 1 deg/s, dollies, framing moves that follow the action), lands face-on for reading moments.
- **Transition grammar:** forward dolly carries across hook/body; objects carry across (message flies from composer to chat, angle cards lift
  out of the chat and drop back, the ad lifts out as the hero); highlight boxes ride the page; whips only on exits. No crossfades between worlds.
- **Timing rules:** arrivals expo.out 0.35 to 0.8 s, exits power3.in and shorter, moves power3.inOut 0.6 to 0.8 s, word stagger 35 ms,
  nothing still for more than 1 s (measured), every event keyed to a word stamp. Judged at 1.15x as well.

## Highlight boxes (the bug)
v3 drew one fixed band at guessed coordinates while the tour scrolled under it, so it never matched a card.
v5 measures the tour: per-frame scroll offset by template matching (match >= 0.98 on every moving frame), the page stitched from the
tour's own frames, ad rectangles found with a sub-pixel edge search, then checked back against each real tour stop:

| tour stop | t (s) | scroll px | ad rects in tour frame px (x0, y0, x1, y1), columns 1/2/3 |
|---|---|---|---|
| 1 | 0.27 | 0 | (295.5, 317.5, 623.5, 645.5) (638.5, 317.5, 965.5, 645.5) (980.5, 317.5, 1308.5, 645.5) |
| 2 | 1.47 | 813 | same columns, y 71.5 to 399.5 |
| 3 | 2.93 | 1381 | same columns, y 71.5 to 399.5 |
| 4 | 4.53 | 1968 | same columns, y 71.5 to 399.5 |
| 5 | 6.00 | 2554 | same columns, y 71.5 to 399.5 |

Worst deviation between the model and the edges measured directly in the tour frames: 1 source px (0.8 screen px). All 105 tour frames from 0 to 6.93 s are
in `tour_track.json`. The box (8 page px padding, 4 px stroke, radius 15 = ad radius + padding, corner brackets, spotlight dim outside)
lives in the same layer as the page, so it cannot drift: it moves between ads with the scroll in one shared ease.
Why a stitched plate and not the mp4 itself: the capture has 7.5 distinct frames per second and jumps up to 468 px per frame, so it
judders and any box would judder with it. The plate is the tour's own pixels, re-driven at 30 fps through the tour's own five stops.

QA on the render (`qa/boxes.txt`, `qa/boxes/box_crops.jpg`, a still every 0.5 s from 9.5 to 20.0 s): every landed frame shows the same gap on
all four sides, 6.5 to 7.5 px (design 6.7 px), 8.5 px during the final push (x1.24 zoom, expected 8.3). Frames that differ are mid-move or
the 0.4 s chip pulse; the dark ad (r4c2) has no measurable edge, the crops show it boxed correctly.

## What changed vs v3, and why
- Small UI box at the top of a black frame -> the UI is a lit surface in a world, larger, with a camera that follows the story.
- Flat Anton hook on a static tile wall -> extruded type on z planes, ad-filled numeral, flight through the real ads, rays on "₹1".
- Number flicker count -> odometer reels. Chips popping -> chips dropping out of the window with the box pulsing on each.
- EA: whole window at 0.9 scale with tiny text -> camera reads the UI for you (sidebar, composer, chat, angles), the three angles lift out
  readable at 25+ px, the pick racks focus, the ad becomes the hero. Paste is a paste (instant, select flash), not typing.
- Captions: same words and timing, now blur-in pages + marker key words.
- Fixed: black frames at every v3 cut (5.9, 20.3, 33.8 s in WS-2_H1) do not exist here; longest still run 0.13 s (v3 had 1.43 s).

## Rebuilding the 11 cuts with it
Stays: screenplay, `v3/vo/*.mp3`, `timing_v3.json` word stamps, `assembly.json` placements, caption text and timing (parsed, never retyped),
replica markup (ChatGPT, Mailflow), library ads, bonus mockups, presenter keyframes, the assemble step (plus the v4 music remix).
Changes: every scene stage moves to the v5 system.
- WS-2 (H1, H4) + WS-1 (H1, H2, H3): hooks -> `ws_hook` pattern per hook line set; body 1 -> `ws-b1` as tested; body 2 (filter + template dialog,
  tour 7 to 15.8 s) -> same tracking job on those frames (search field and Copy JSON prompt boxes still to measure), ChatGPT send with the
  carry-across; body 3 (result + before/after + meter) -> hero lift like EA; body 4 -> `sf-ws-offer`; body 5 -> `sf-ws-end`.
- EA-2 (H2, H4, H5) + EA-1 (H1, H4, H5): hooks -> same hook system in lime; body 1 (16 agents grid) -> grid as a 3D board in the vault;
  body 2 -> `ea-b2` as tested; body 3 -> `sf-ea-ret` world (ChatGPT map, Mailflow builder, flows list); body 4 -> grid light-up + approve stamp;
  body 5 -> EA end card in the `sf-ws-end` layout with 3 bonuses.
- EA-1 / WS-1 presenter cuts keep the presenter plates; the stages behind and beside them get the same world and camera.

## Honest limits of this test
- No music (as asked). Finals still need the peppy bed from `v4/tools/remix_v4.py` and sparse SFX.
- No AI video clips (no paid generation). The standing rule mixes a few in as hero beats; this test is motion graphics only.
- EA ad hero is full size for 1.0 s before the narration ends (1.4 s visible in all), 0.9 s at 1.15x: under the 1.2 s reading rule.
  In the full cut it should carry 0.4 s into the next beat.
- At 1.15x the box stations hold about 1.7 s each; fine, but the "1,169" reel roll is quick.
- Style frames 04, 07, 08 come from look-only scenes (motion sketched, not finished).
- The hook sticker whips across the caption for about 0.3 s on the exit.
- `hyperframes check` layout errors are intentional overlaps (odometer digits off-reel, fog and dim layers over the UI, the lifted deck over
  the chat); there are no runtime or motion errors.
