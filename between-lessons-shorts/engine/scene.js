// Generic falling-notes engine. Everything is driven by window.__TIMING__ (written by gen/make.py).
// window.render(t) is a pure function of t.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
await Promise.all(["900 80px Inter", "800 40px Inter", "700 30px Inter", "900 80px Inter", "700 30px Cormorant", "40px 'Noto Color Emoji'"].map((f) => document.fonts.load(f, "AÄřé❌✅")));
const T = window.__TIMING__, UI = T.ui, EV = T.ev || {}, NOTES = T.notes, SECS = T.secs, SEC = Object.fromEntries(SECS.map((s) => [s.id, s]));
const $ = (id) => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, k) => a + (b - a) * k, ease = (k) => 1 - Math.pow(1 - clamp(k), 3);
const easeIO = (k) => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
const back = (k) => { k = clamp(k); const c = 1.70158; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
const v3 = (x, y, z) => new THREE.Vector3(x, y, z);
let seed = 5; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
const RES = T.res || 720;
const END_Q = UI.endq_t, LT = UI.lt;

const renderer = new THREE.WebGLRenderer({ canvas: $("gl"), antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(RES, Math.round(RES * 16 / 9), false);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.1; renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.localClippingEnabled = true;
const scene = new THREE.Scene(); scene.background = new THREE.Color("#0E0C0A"); scene.fog = new THREE.FogExp2("#0E0C0A", 0.028);
const camera = new THREE.PerspectiveCamera(45, 1080 / 1920, 0.05, 120);
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.5;
scene.add(new THREE.AmbientLight("#FFE9C9", 0.55));
const keyL = new THREE.DirectionalLight("#FFE2B0", 2.4); keyL.position.set(-3, 9, 8); scene.add(keyL);
const rimL = new THREE.DirectionalLight("#E0A84B", 1.4); rimL.position.set(4, 4, -6); scene.add(rimL);
const glowL = new THREE.PointLight("#E0A84B", 0, 6, 1.5); glowL.position.set(0, 0.8, 0.6); scene.add(glowL);

// ---------- keyboard C2..C6
const NW = 29, KW = 0.235, KL = 1.5, X0 = -((NW - 1) * KW) / 2, HIT = 0.16, NZ = -0.86, V = 5.2;
const DEG = { 0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6 };
const isWhite = (m) => DEG[(m - 36) % 12] !== undefined;
const wIdx = (m) => Math.floor((m - 36) / 12) * 7 + DEG[(m - 36) % 12];
const laneX = (m) => (isWhite(m) ? X0 + wIdx(m) * KW : X0 + wIdx(m - 1) * KW + KW / 2);
const keys = {}, kb = new THREE.Group(); scene.add(kb);
for (let m = 36; m <= 84; m++) {
  const w = isWhite(m), mat = new THREE.MeshStandardMaterial({ color: w ? "#F1E9D6" : "#15100C", roughness: w ? 0.28 : 0.22, metalness: w ? 0 : 0.15, emissive: "#E0A84B", emissiveIntensity: 0 });
  const k = new THREE.Mesh(new THREE.BoxGeometry(w ? KW - 0.014 : 0.135, 0.12, w ? KL : 0.95), mat); k.position.set(laneX(m), w ? 0.06 : 0.17, w ? 0 : -0.275); kb.add(k);
  keys[m] = { k, p0: k.position.clone(), vel: v3((rnd() - 0.5) * 7, 2.5 + rnd() * 6, 1.5 + rnd() * 4), spin: v3((rnd() - 0.5) * 9, (rnd() - 0.5) * 9, (rnd() - 0.5) * 9) };
}
const W = NW * KW + 0.6;
const body = new THREE.Mesh(new THREE.BoxGeometry(W, 0.5, 2.4), new THREE.MeshStandardMaterial({ color: "#241C15", roughness: 0.45, metalness: 0.2 })); body.position.set(0, -0.25, -0.3); scene.add(body);
const hitM = new THREE.MeshStandardMaterial({ color: "#E0A84B", emissive: "#F2B84B", emissiveIntensity: 1, metalness: 0.5, roughness: 0.3 });
const hitLine = new THREE.Mesh(new THREE.BoxGeometry(W - 0.2, 0.035, 0.035), hitM); hitLine.position.set(0, HIT, NZ + 0.07); scene.add(hitLine);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: "#0B0907", roughness: 0.95 })); floor.rotation.x = -Math.PI / 2; floor.position.y = -0.5; scene.add(floor);
{
  const c = document.createElement("canvas"); c.width = 1024; c.height = 2048; const g = c.getContext("2d");
  const gr = g.createLinearGradient(0, 0, 0, 2048); gr.addColorStop(0, "rgba(30,24,18,0)"); gr.addColorStop(0.5, "rgba(30,24,18,.75)"); gr.addColorStop(1, "rgba(36,28,20,1)"); g.fillStyle = gr; g.fillRect(0, 0, 1024, 2048);
  for (let m = 36; m <= 84; m += 12) { const x = ((laneX(m) - KW / 2 + W / 2) / W) * 1024; const lg = g.createLinearGradient(0, 0, 0, 2048); lg.addColorStop(0, "rgba(224,168,75,0)"); lg.addColorStop(1, "rgba(224,168,75,.22)"); g.fillStyle = lg; g.fillRect(x - 1.5, 0, 3, 2048); }
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
  const p = new THREE.Mesh(new THREE.PlaneGeometry(W, 14), new THREE.MeshBasicMaterial({ map: tx, transparent: true, depthWrite: false })); p.position.set(0, 7, NZ - 0.25); scene.add(p);
}
// ---------- notes
const COL = { R: new THREE.Color("#F2B84B"), L: new THREE.Color("#A99BFF"), X: new THREE.Color("#FF3B3B") };
const clip = new THREE.Plane(new THREE.Vector3(0, 1, 0), -HIT), geoCache = {}, matCache = {};
const noteObjs = NOTES.map((n) => {
  const w = isWhite(n.m) ? 0.2 : 0.13, len = Math.max(0.12, n.d * V - 0.04), key = `${w}|${len.toFixed(2)}`;
  geoCache[key] = geoCache[key] || new RoundedBoxGeometry(w, len, 0.12, 2, Math.min(0.045, len / 2 - 0.005));
  const mesh = new THREE.Mesh(geoCache[key], new THREE.MeshStandardMaterial({ color: COL[n.h], emissive: COL[n.h], emissiveIntensity: 0.45, roughness: 0.35, clippingPlanes: [clip] }));
  mesh.visible = false; scene.add(mesh); return { n, mesh, len, x: laneX(n.m), z: NZ + (isWhite(n.m) ? 0 : 0.04) };
});
const active = (n, t) => { const s = SEC[n.sec]; return s && t >= s.start && t < s.end; };
// ---------- particles
const dotTex = (() => { const c = document.createElement("canvas"); c.width = c.height = 64; const g = c.getContext("2d"); const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.3, "rgba(255,255,255,.55)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); })();
function pool(n, size) { const pos = new Float32Array(n * 3), col = new Float32Array(n * 3), geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(pos, 3)); geo.setAttribute("color", new THREE.BufferAttribute(col, 3)); const pts = new THREE.Points(geo, new THREE.PointsMaterial({ map: dotTex, size, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })); pts.frustumCulled = false; scene.add(pts); return { pos, col, geo }; }
const SPK = 8, MAXN = Math.min(NOTES.length, 400), sparks = pool(MAXN * SPK, 0.09), glows = pool(MAXN, 1.25);
const sparkSeed = NOTES.map(() => Array.from({ length: SPK }, () => [(rnd() - 0.5) * 1.6, 1.4 + rnd() * 2.6, rnd() * 0.9, 0.35 + rnd() * 0.5]));
const NP = 220, dustP = new Float32Array(NP * 3), dustS = Array.from({ length: NP }, () => [(rnd() - 0.5) * 12, rnd() * 13, (rnd() - 0.5) * 10 - 1, 0.05 + rnd() * 0.12, rnd() * 6.28]);
const dustG = new THREE.BufferGeometry(); dustG.setAttribute("position", new THREE.BufferAttribute(dustP, 3));
scene.add(new THREE.Points(dustG, new THREE.PointsMaterial({ map: dotTex, size: 0.06, transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending, color: "#FFE2A8" })));
// snow (optional)
let snowG = null, snowS = [];
if (T.snow) { const N = 420; snowS = Array.from({ length: N }, () => [(rnd() - 0.5) * 16, rnd() * 16, (rnd() - 0.5) * 12 + 1, 0.4 + rnd() * 0.7, rnd() * 6.28]); snowG = new THREE.BufferGeometry(); snowG.setAttribute("position", new THREE.BufferAttribute(new Float32Array(N * 3), 3)); const sp = new THREE.Points(snowG, new THREE.PointsMaterial({ map: dotTex, size: 0.2, transparent: true, opacity: 0.8, depthWrite: false, color: "#FFF6E6", fog: false })); sp.frustumCulled = false; scene.add(sp); }
// confetti
const CN = 260, confM = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.11, 0.07), new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, fog: false }), CN); confM.frustumCulled = false; scene.add(confM);
const confS = Array.from({ length: CN }, () => [(rnd() - 0.5) * 9, 5 + rnd() * 8, (rnd() - 0.5) * 5 + 2, rnd() * 9, rnd() * 9, rnd() * 9]);
const CPAL = ["#E0A84B", "#F5EEDC", "#A99BFF", "#F2B84B", "#FF8A5B"].map((c) => new THREE.Color(c)); for (let i = 0; i < CN; i++) confM.setColorAt(i, CPAL[i % CPAL.length]);
const dmy = new THREE.Object3D();
// shockwave ring
const ring = new THREE.Mesh(new THREE.TorusGeometry(1, 0.05, 8, 80), new THREE.MeshBasicMaterial({ color: "#FFB347", transparent: true, opacity: 0, fog: false })); ring.rotation.x = Math.PI / 2; ring.position.set(0, 0.4, -0.2); scene.add(ring);

// ---------- camera
function curSec(t) { let s = SECS[0]; for (const x of SECS) if (t >= x.start) s = x; return s; }
function pose(type, k, t) {
  let p = v3(0, 7.6, 15.2), l = v3(0, 4.75, -0.6);
  switch (type) {
    case "hook": { const e = easeIO(k); p = v3(lerp(2.2, 0.6, e), lerp(3.2, 5.6, e), lerp(9.0, 12.6, e)); l = v3(lerp(1.6, 0.3, e), lerp(2.2, 3.4, e), -0.6); break; }
    case "hookL": { const e = easeIO(k); p = v3(lerp(-2.2, -0.6, e), lerp(3.2, 5.6, e), lerp(9.0, 12.6, e)); l = v3(lerp(-1.6, -0.3, e), lerp(2.2, 3.4, e), -0.6); break; }
    case "wide": p.x += 0.5 * Math.sin(k * 2.2); break;
    case "push": { const e = easeIO(k); p.z -= 1.6 * e; p.y -= 0.6 * e; break; }
    case "close": { const e = easeIO(k); p = v3(1.1 * Math.sin(e * 3.3), lerp(6.6, 5.2, e), lerp(14.2, 12.4, e)); l = v3(0.35 * Math.sin(e * 3.3), lerp(4.5, 4.1, e), -0.6); break; }
    case "left": { const e = easeIO(k); p = v3(lerp(-1.8, -1.0, e), 6.2, lerp(12.8, 12.0, e)); l = v3(-1.1, 4.0, -0.6); break; }
    case "right": { const e = easeIO(k); p = v3(lerp(1.8, 1.0, e), 6.2, lerp(12.8, 12.0, e)); l = v3(1.1, 4.0, -0.6); break; }
    case "low": { const e = easeIO(k); p = v3(lerp(-0.8, 0.8, e), 3.6, lerp(11.2, 10.4, e)); l = v3(0, 3.1, -0.6); break; }
    case "orbit": { const a = lerp(-0.35, 0.35, easeIO(k)); p = v3(15.2 * Math.sin(a), 7.2, 15.2 * Math.cos(a)); break; }
    case "far": p = v3(0, 8.4, 17.0); l = v3(0, 5.2, -0.6); break;
  }
  return [p, l];
}
function cam(t) {
  const s = curSec(t), k = clamp((t - s.start) / Math.max(0.01, s.end - s.start));
  let [p, l] = pose(s.cam || "wide", s.cam === "hook" || s.cam === "hookL" ? clamp((t - s.start) / 1.9) : k, t);
  if (END_Q && t > END_Q - 0.95) { const pb = easeIO((t - (END_Q - 0.95)) / 2.2); p.lerp(v3(0, 8.0, 16.2), pb); l.lerp(v3(0, 5.0, -0.6), pb); }
  for (const c of EV.shake || []) if (t > c && t < c + 0.7) { const a = 0.16 * Math.exp(-(t - c) * 7); p.x += a * Math.sin(t * 95); p.y += a * Math.cos(t * 81); }
  camera.position.copy(p); camera.lookAt(l);
}
// ---------- overlay
const meter = [...document.querySelectorAll("#meter i")], setH = (el, h) => { if (el.__h !== h) { el.innerHTML = h; el.__h = h; } };
const fadeWin = (t, a, b, fi = 0.25, fo = 0.2) => clamp((t - a) / fi) * clamp((b - t) / fo);
function ui(t) {
  const s = curSec(t), k = t - s.start, endShown = END_Q && t >= END_Q - 0.1;
  const slams = (EV.slams || []).filter((x) => t >= x.t && t < x.end), slam = slams[slams.length - 1];
  // hook
  const hk = UI.hook_end ? fadeWin(t, -1, UI.hook_end, 0.01, 0.15) : 0; $("hook").style.opacity = hk; setH($("hook"), UI.hook || "");
  $("hook").style.transform = `scale(${lerp(1.06, 1, ease(t / 0.4)).toFixed(3)})`;
  // caption / sub / tag
  const cOn = s.cap && !slam && !endShown && t >= (UI.hook_end || 0) ? 1 : 0;
  setH($("cap"), s.cap || ""); $("cap").style.opacity = cOn * clamp(k / 0.15); $("cap").style.transform = `scale(${lerp(1.12, 1, ease(k / 0.3)).toFixed(3)})`;
  setH($("sub"), s.sub || ""); $("sub").style.opacity = (s.sub && !slam && !endShown ? 1 : 0) * clamp((k - 0.3) / 0.25);
  setH($("tag").firstChild, s.tag || ""); $("tag").style.opacity = (s.tag && !slam && !endShown ? 1 : 0) * clamp((k - 0.15) / 0.2);
  $("tag").style.transform = `scale(${lerp(1.3, 1, back(k / 0.3)).toFixed(3)})`;
  // card
  const gEl = $("card");
  if (!s.card || slam || t < (UI.hook_end || 0)) gEl.style.opacity = 0;
  else {
    const c = s.card; gEl.style.opacity = END_Q ? clamp((END_Q - 0.1 - t) / 0.3) : 1;
    setH(gEl.querySelector(".lab"), c.lab || "");
    const num = gEl.querySelector(".num"); setH(num, c.big || ""); const L = String(c.big || "").replace(/<[^>]+>/g, "").length; const cls = "num" + (L > 6 ? " small" : L > 4 ? " mid" : ""); if (num.className !== cls) num.className = cls;
    num.style.transform = `scale(${lerp(1.45, 1, ease(k / 0.3)).toFixed(3)})`;
    $("meter").style.display = c.meter ? "flex" : "none";
    meter.forEach((el, i) => { const on = c.meter && i < c.meter && k > 0.15 + i * 0.06 ? "on" : ""; if (el.className !== on) el.className = on; });
    setH($("desc"), c.desc || ""); $("desc").style.opacity = clamp((k - 0.35) / 0.25);
    setH($("small"), c.small || ""); $("small").style.opacity = clamp((k - 0.5) / 0.25);
  }
  // timers
  let tm = null; for (const x of EV.timers || []) if (t >= x[0] && t < x[1]) tm = x;
  if (tm) { const d = tm[1] - tm[0], a = t - tm[0], left = Math.ceil(d - a - 1e-6); $("timer").style.opacity = clamp(a / 0.15) * clamp((d - a) / 0.1 + 0.2);
    $("ring").setAttribute("stroke-dashoffset", (703.7 * clamp(a / d)).toFixed(1)); setH($("timer").querySelector(".n"), String(Math.max(1, left)));
    const fr = a - Math.floor(a); $("timer").querySelector(".n").style.transform = `scale(${lerp(1.35, 1, ease(fr / 0.25)).toFixed(3)})`; }
  else $("timer").style.opacity = 0;
  // slam
  if (slam) { const a = t - slam.t; setH($("slam"), slam.text); { const lg = slam.text.replace(/<[^>]+>/g, "").length > 15; if ($("slam").classList.contains("long") !== lg) $("slam").classList.toggle("long", lg); } setH($("slamsub"), slam.sub || ""); $("slam").style.opacity = clamp(a / 0.08) * clamp((slam.end - t) / 0.15);
    $("slam").style.transform = `scale(${lerp(1.9, 1, back(a / 0.35)).toFixed(3)}) rotate(${lerp(-6, 0, ease(a / 0.35)).toFixed(2)}deg)`;
    $("slamsub").style.opacity = clamp((a - 0.35) / 0.2) * clamp((slam.end - t) / 0.15); }
  else { $("slam").style.opacity = 0; $("slamsub").style.opacity = 0; }
  // end
  setH($("endq"), UI.endq || ""); setH($("end2"), UI.end2 || "");
  const ek = END_Q ? ease((t - END_Q) / 0.35) : 0; $("endq").style.opacity = ek; $("endq").style.transform = `scale(${lerp(0.9, 1, ek).toFixed(3)})`;
  const k2 = END_Q ? ease((t - END_Q - 0.6) / 0.35) : 0; $("end2").style.opacity = k2; $("end2").style.transform = `translateY(${lerp(30, 0, k2).toFixed(1)}px)`;
  const lk = LT ? ease((t - LT) / 0.4) : 0; $("lt").style.opacity = lk; $("lt").style.transform = `translateY(${lerp(40, 0, lk).toFixed(1)}px)`;
  // phone
  if (UI.phone) { const a = t - UI.phone; const pk = a < 0 ? 0 : 1; $("phone").style.opacity = pk;
    const y = lerp(1500, 0, back(a / 0.7)), r = lerp(-14, 0, ease(a / 0.7)); $("phone").style.transform = `translateY(${y.toFixed(1)}px) rotate(${r.toFixed(2)}deg)`;
    const beat = (Math.max(0, a) * 36 / 60) % 1; $("pdot").style.opacity = (0.35 + 0.65 * Math.exp(-beat * 6)).toFixed(3); $("pdot").style.transform = `scale(${(1 + 0.35 * Math.exp(-beat * 8)).toFixed(3)})`; }
  const dimT = UI.phone ? Math.min(UI.phone, END_Q || 1e9) : END_Q;
  $("dim").style.opacity = dimT ? (0.5 * ease((t - dimT) / 0.6)).toFixed(3) : 0;
  $("mark").style.opacity = 0.75 * clamp((t - 1.5) / 0.5) * (LT ? 1 - clamp((t - LT) / 0.3) : 1);
  $("ai").style.opacity = LT ? 0.9 * clamp((t - LT) / 0.4) : 0;
  let fl = 0; for (const c of EV.flash || []) if (t >= c && t < c + 0.2) fl = Math.max(fl, 0.32 * (1 - (t - c) / 0.2)); $("flash").style.opacity = fl.toFixed(3);
  let rd = 0; for (const c of EV.red || []) if (t >= c && t < c + 0.7) rd = Math.max(rd, Math.exp(-(t - c) * 4)); $("red").style.opacity = rd.toFixed(3);
}
// ---------- explosion
function explodeK(t) { for (const [a, b] of EV.explode || []) if (t >= a && t < b) { const out = ease((t - a) / 0.6), back_ = easeIO((t - (b - 0.9)) / 0.9); return out * (1 - back_); } return 0; }
// ---------- per-frame
window.render = function (t) {
  cam(t);
  const keyLv = {}, keyCol = {}; let si = 0, gi = 0, best = 0, bestX = 0;
  for (let i = 0; i < noteObjs.length; i++) {
    const o = noteObjs[i], n = o.n, on = active(n, t), bottom = HIT + (n.t - t) * V;
    o.mesh.visible = on && bottom < 14 && bottom + o.len > HIT;
    if (o.mesh.visible) { o.mesh.position.set(o.x, bottom + o.len / 2, o.z); o.mesh.material.emissiveIntensity = t >= n.t && t < n.t + n.d ? 1.35 : 0.45; }
    const a = t - n.t;
    if (on && a >= 0 && a < n.rel - n.t + 1.2) {
      const held = n.rel - n.t, lv = a < n.d ? 1 : a < held ? 0.55 : 0.55 * Math.exp(-(a - held) / 0.18);
      if (lv > (keyLv[n.m] || 0)) { keyLv[n.m] = lv; keyCol[n.m] = n.h; }
      if (lv > best) { best = lv; bestX = o.x; }
      const gl = lv * (a < 0.12 ? 1.5 - a * 4 : 1) * 0.85 * (0.6 + 0.4 * n.v);
      if (gl > 0.02 && gi < MAXN) { glows.pos.set([o.x, HIT + 0.08, o.z + 0.12], gi * 3); const c = COL[n.h]; glows.col.set([c.r * gl, c.g * gl, c.b * gl], gi * 3); gi++; }
      if (a < 0.9 && si < MAXN * SPK - SPK) for (const [vx, vy, vz, life] of sparkSeed[i]) { if (a > life) continue; const f = (1 - a / life) * (0.5 + 0.5 * n.v), c = COL[n.h]; sparks.pos.set([o.x + vx * a, HIT + vy * a - 4.2 * a * a, o.z + 0.1 + vz * a], si * 3); sparks.col.set([c.r * f + 0.25 * f, c.g * f + 0.2 * f, c.b * f + 0.1 * f], si * 3); si++; }
    }
  }
  for (const [pl, cnt] of [[sparks, si], [glows, gi]]) { pl.geo.setDrawRange(0, cnt); pl.geo.attributes.position.needsUpdate = true; pl.geo.attributes.color.needsUpdate = true; }
  const ex = explodeK(t);
  for (const m in keys) { const { k, p0, vel, spin } = keys[m], lv = keyLv[m] || 0; k.material.emissive.copy(COL[keyCol[m] || "R"]); k.material.emissiveIntensity = 0.9 * lv + (ex > 0 ? 0.6 * ex : 0);
    k.position.set(p0.x + vel.x * ex * 0.55, p0.y - 0.04 * lv + vel.y * ex * 0.55, p0.z + vel.z * ex * 0.55); k.rotation.set(spin.x * ex, spin.y * ex, spin.z * ex); }
  hitLine.visible = ex < 0.05;
  // shockwave
  let rw = 0, ra = 0; for (const [a] of EV.explode || []) if (t >= a && t < a + 1) { ra = t - a; rw = 1; }
  ring.material.opacity = rw ? 0.9 * (1 - ra) : 0; ring.scale.setScalar(0.5 + ra * 9);
  glowL.intensity = 10 * best + 30 * ex; glowL.position.x = bestX; hitM.emissiveIntensity = 0.9 + 0.8 * best;
  for (let i = 0; i < NP; i++) { const [x0, y0, z0, sp, ph] = dustS[i]; dustP[i * 3] = x0 + 0.2 * Math.sin(t * 0.5 + ph); dustP[i * 3 + 1] = (y0 + sp * t) % 13; dustP[i * 3 + 2] = z0; }
  dustG.attributes.position.needsUpdate = true;
  if (snowG) { const P = snowG.attributes.position.array; for (let i = 0; i < snowS.length; i++) { const [x0, y0, z0, sp, ph] = snowS[i]; P[i * 3] = x0 + 0.4 * Math.sin(t * 0.7 + ph); P[i * 3 + 1] = 15 - ((15 - y0 + sp * t) % 16); P[i * 3 + 2] = z0; } snowG.attributes.position.needsUpdate = true; }
  // confetti
  let cb = null; for (const c of EV.confetti || []) if (t >= c && t < c + 3.2) cb = c;
  confM.visible = cb !== null;
  if (cb !== null) { const a = t - cb, dr = (1 - Math.exp(-1.6 * a)) / 1.6;
    for (let i = 0; i < CN; i++) { const [vx, vy, vz, rx, ry, rz] = confS[i]; dmy.position.set(vx * dr, 3.2 + vy * dr - 1.6 * a * a, vz * dr); dmy.rotation.set(rx * a, ry * a, rz * a); dmy.scale.setScalar(clamp((3.2 - a) / 0.5)); dmy.updateMatrix(); confM.setMatrixAt(i, dmy.matrix); }
    confM.instanceMatrix.needsUpdate = true; }
  renderer.render(scene, camera); ui(t);
};
window.__ready = (async () => { window.render(0); return true; })();
