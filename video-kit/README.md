# Between Lessons video kit (rebuilt)

Short vertical videos (1080x1920, 30 fps) rendered from three.js, with real sampled piano audio.

## Setup (once)
```
npm install                      # three, Geist font, Salamander piano samples
pip install numpy soundfile pillow
python3 tools/make_samples.py    # decodes piano samples to assets/wav
python3 -m http.server 8765 &    # serve the kit root
```

## Make / render
```
python3 videos/batch1.py a1      # build audio.wav + timing.json (batch1: a1-a3, b1-b3; batch2: c-e; batch3: f-k)
node render.mjs a1-guess-classical test 0.3 2 4    # test stills -> videos/<v>/test
python3 tools/sheet.py videos/<v>/test sheet.jpg   # contact sheet
python3 tools/capcheck.py                          # flags captions that would wrap past 2 lines
echo a1-guess-classical >> logs/todo.txt; tools/worker.sh &   # full render + encode -> out/<v>.mp4
```

## Layout
- `lib/pianolib.py` piano rendering (Salamander Grand Piano, CC-BY 3.0, Alexander Holm), reverb, master
- `lib/sfx.py` synthesised sound effects + music bed
- `lib/music.py` public-domain arrangements (from memory: check by ear)
- `lib/reel.py` authoring API (notes, camera, captions, fx, phone, outro); `lib/fit.py` caption fitting
- `lib/formats.py`, `lib/formats2.py` the 11 video formats
- `lib/engine.js` scene engine (pure function of t), `lib/phone.js` real Today / check-in / roadmap / questionnaire screens
- `render.mjs` frame renderer (Playwright + CDP screenshots), `tools/worker.sh` render queue

Gotcha fixed this time: InstancedMesh/Points need `frustumCulled = false` or short notes and confetti vanish.
