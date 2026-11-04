# Between Lessons shorts kit (64 videos)

Generates 1080×1920 falling-notes piano shorts for betweenlessons.org from one shared engine.

| Part | What it does |
|---|---|
| `gen/music.py` | Public-domain pieces (arranged from memory) + Grade 1 / 5 / 8 arrangers |
| `gen/formats.py` | 10 formats: grade comparison, 5 levels, guess the song, guess the grade, ❌ vs ✅ practice, tempo ladder, pedal comparison, 5 left hands, "easier than it sounds", one mistake |
| `gen/make.py` | The 64-video catalogue (posting order) → `videos/NN-slug/{audio.wav,timing.json}` |
| `engine/` | three.js scene + HTML overlays, driven only by `timing.json` |
| `render2.mjs`, `one.sh` | Playwright frame render → ffmpeg MP4 |
| `CAPTIONS.md` | Caption (with #ad), YouTube title and pieces for each video |

## Run
Set up as in the piano-shorts-video skill (npm deps, `wav/` piano samples, `python3 -m http.server 8765` in this folder), then:
```bash
python3 gen/make.py all
ls videos | xargs -P 3 -I{} ./one.sh {}
```
Only real product facts are shown (6-week plan, tempo targets, −5% on "Too hard", Day 1 free, the real Clair de Lune example plan on the phone screen). No reviews, stats or results.
