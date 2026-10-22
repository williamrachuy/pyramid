# Pyramid

A four-player card game of courts, royals and gems, in which the table is an unfolded pyramid: pair every shared corner and the four faces close. The rules are in [RULES.md](RULES.md).

This repository is the source. The playable build lives on the website at [adividiardi.com/pyramid](https://www.adividiardi.com/pyramid/), copied from `web/`.

## Layout

| Path | What it is |
|---|---|
| `web/engine.js` | The rules engine: pure functions over plain JSON states, seeded and deterministic |
| `web/ai.js` | The three AI houses (Architect, Hoarder, Usurper) at four levels |
| `web/viz.js` | The live 3D pyramid (a hand-rolled canvas renderer) |
| `web/ui.js`, `web/index.html`, `web/style.css` | The table: glass, animations, input |
| `web/audio.js` | Procedural sound (Web Audio, no files) |
| `tests/engine.test.js` | Rules tests plus AI self-play |
| `tools/sync-to-site.sh` | Copies `web/` into the website checkout |
| `legacy/` | The original Python prototype |

## Run

No build step. Serve `web/` and open it:

```sh
python3 -m http.server -d web 8000   # then open http://localhost:8000
node tests/engine.test.js            # rules tests and AI self-play
```

## Publish to the website

```sh
tools/sync-to-site.sh ../williamrachuy.github.io
```

Then commit the site repo's `pyramid/` folder.
