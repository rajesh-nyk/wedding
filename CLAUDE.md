# Rajesh & Chinmayee — wedding website (handover notes)

Live site: https://blessed4life.in (Cloudflare Workers static assets, see `wrangler.jsonc`).
The live site is served from `wedding/website-3/`. Websites 1 and 2 in `wedding/` are older versions; leave them alone.

## Rules Rajesh has set (follow every time)
- **Never push to `main` unless Rajesh says "push to prod".** Pushing to `main` deploys blessed4life.in automatically.
  Work on the `test` branch; show changes locally (run a local server and let him open it on his phone over Wi-Fi) before anything goes live.
- He is very serious about small details. Check every change on phone (iPhone SE 375×667, iPhone 390×844, 430×932),
  iPad (820×1180) and laptop (1280×680, 1470×800 = his MacBook, 1920×1080) **in Safari and Chrome** before showing it.
- Text must never touch or overlap photos, cards, the garland, Ganesha or the travelling wheel. No text escaping decorative borders. No horizontal overflow.
- Backgrounds: dark AMOLED gradients. Colours must blend between sections (no visible seams).
- Hover effects only on real mouse devices `(hover:hover) and (pointer:fine)`; never let hover create square boxes or push things out of frame (Safari clipping bugs).
- No extra explanatory text he didn't ask for. Explain changes to him in plain language, no jargon.
- Transitions must be smooth and continuous. He loved the current scroll **velocity** (calm, capped ~1.15 screens/sec) — keep it.
- He rejected: gold-dust particles ("cheap"), incense-smoke transitions ("ugly"). Don't bring them back.

## Facts
- Rajesh (from Bhubaneswar) & Chinmayee (from Sambalpur). Nirbandha 27 Jan 2027 Sambalpur · Bahaghara 26 Feb 2027 Sambalpur · Reception 3 Mar 2027 Bhubaneswar.
- Contact in footer: rajeshnayakabcd@gmail.com, instagram.com/genhu_____1509

## How `index.html` works
Single file. Scroll-driven scenes: each `<section class="scene" data-scene="key">` has a sticky `.stage`; the loop computes progress `p` (0..1)
and calls `U[key](p, el)`. Helpers: `seg(p,a,b)`, `eo`, `eio`, `eback`, `lerp`, `cl`. Some scenes overlap the previous one
(`margin-top:-100svh`, flagged `ov` in the scene table) and stay hidden until the previous scene finishes.
Scene order: hero (Konark wheel) → bless (diya → ray → aura → lines → Ganesha) → moments (Our Story photos) → events + 3 ceremony cards
(nb, bh, rc) → knot (Hata Ganthi) → sapt (Saptapadi) → rit (ritual cards + Kaudi Khela game) → sky (sunset → night, credits in footer).

Key systems:
- `VS` — cinematic scroll: wheel/touch/keys set a target; page travels to it at a capped speed. `autoTo(y, ms)` glides the page.
- `GLP` — WebGL "molten gold" handover: embers rise and the diya is forged at the end of the hero.
- `G3D` / `G3` — WebGL renderer for the 3D Ganesha (`ganesha-mesh.json` + `g-base-2k.jpg` phones / `g-base-4k.jpg` laptops).
  Falls back to the painted `ganesha.webp` if WebGL is missing or Reduce Motion is on.
- Interactions: hold-to-light diya (`DY`), drag hands together for Hata Ganthi (`KG`), tap footprints (Saptapadi), Kaudi Khela game.
- `LITE` mode for slow phones; `RM` = prefers-reduced-motion; PWA via `sw.js` (bump cache name `V` on each release) + `manifest.webmanifest`.

## In progress when handed over
- **3D Ganesha camera move** (his request): shot 1 from beneath the seat (screen filled with the cream underside) → shot 2 low close-up
  beside the raised hand/trunk → shot 3 full front view. Keyframes `K` in the `G3` block. Works on phone sizes; the last change
  (camera closer on wide laptop screens so shot 1 has no black corners) is **not yet checked**. Not yet shown to Rajesh.
- He hasn't yet approved the 3D Ganesha, the camera move, or the diya forging for prod. Everything on `test` after `main` is unapproved.
- 3D pipeline: original Meshy model was 165 MB / 3.5M triangles (too big for GitHub; Rajesh has it). `tools/ganesha-3d/decimate.py`
  reduced it to ~212k triangles keeping texture seams; `smooth_and_pack.py` smooths normals and packs JSON. Meshy's metal/roughness map
  is noisy, so the shader ignores it and detects gold from the colour. With proper tools available (e.g. gltf-transform + meshoptimizer,
  three.js), a better-quality pipeline is welcome.
- Check Meshy licence terms for his plan (free plan may require attribution).

## Checks
`tools/checks/*.py` are Playwright scripts (serve `wedding/website-3` on localhost:8822 first; they expect Chrome at /usr/bin/google-chrome — adjust paths).
`bounds.py` scans every screen at 7 sizes for overflow and text escaping boxes; the others test the diya, knot drag, Saptapadi, Kaudi Khela,
ceremony handovers and the 3D Ganesha.
