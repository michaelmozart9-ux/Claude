// Shared scene engine. Everything is a pure function of t, driven by videos/<v>/timing.json.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { FontLoader } from "three/addons/loaders/FontLoader.js";
import { TextGeometry } from "three/addons/geometries/TextGeometry.js";
import { makePhone } from "/lib/phone.js";

const V = new URLSearchParams(location.search).get("v");
const T = await (await fetch(`/videos/${V}/timing.json?` + Math.random())).json();
await Promise.all(["900 80px Inter", "800 40px Inter", "700 30px Inter", "600 30px Inter", "500 30px Inter", "600 30px Geist", "500 30px Geist", "400 30px Geist", "italic 400 30px Geist", "500 30px 'Geist Mono'", "64px 'Noto Color Emoji'"].map((f) => document.fonts.load(f, "Aa😣👍😎")));
const font3d = await new Promise((res) => new FontLoader().load("/node_modules/three/examples/fonts/helvetiker_bold.typeface.json", res));

const $ = (id) => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, k) => a + (b - a) * k;
const ease = (k) => 1 - Math.pow(1 - clamp(k), 3);
const easeIO = (k) => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
const back = (k) => { k = clamp(k); const c = 1.70158; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
const hash = (a, b) => { const s = Math.sin(a * 12.9898 + b * 78.233 + 0.123) * 43758.5453; return s - Math.floor(s); };
const EASES = { io: easeIO, o: ease, lin: (k) => clamp(k), back: back, cut: (k) => (k >= 1 ? 1 : 0) };

const DUR = T.duration;
const COL = { R: "#F2C46B", L: "#5FB4FF", X: "#FF3B3B", G: "#8D939C", W: "#FFFFFF", B: "#F7E3B0", P: "#C58CFF", N: "#5FE3A1" };
const hc = Object.fromEntries(Object.entries(COL).map(([k, v]) => [k, new THREE.Color(v)]));

// ---------- renderer / scene ----------
const QS = new URLSearchParams(location.search);
const RS = +(QS.get("rs") ?? T.rs ?? 1), AA = (QS.get("aa") ?? "1") === "1";
const renderer = new THREE.WebGLRenderer({ canvas: $("gl"), antialias: AA, preserveDrawingBuffer: true, powerPreference: "high-performance" });
renderer.setPixelRatio(1); renderer.setSize(Math.round(1080 * RS), Math.round(1920 * RS), false);
$("gl").style.width = "1080px"; $("gl").style.height = "1920px";
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = T.exposure ?? 1.1; renderer.outputColorSpace = THREE.SRGBColorSpace;
const BG = new THREE.Color(T.bg ?? "#0E0C0A");
const scene = new THREE.Scene(); scene.background = BG; scene.fog = new THREE.FogExp2(BG, T.fog ?? 0.028);
const camera = new THREE.PerspectiveCamera(T.fov ?? 45, 1080 / 1920, 0.05, 200); scene.add(camera);
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.45;
scene.add(new THREE.AmbientLight("#FFE9C9", 0.45));
const key = new THREE.DirectionalLight("#FFE2B0", 2.0); key.position.set(-4, 9, 10); scene.add(key);
const rim = new THREE.DirectionalLight("#E0A84B", 1.3); rim.position.set(5, 4, -6); scene.add(rim);
const fillL = new THREE.PointLight("#7CC4FF", 6, 18); fillL.position.set(-6, 3, 2); scene.add(fillL);

function softTex(size = 128, hard = 0.0) {
  const c = document.createElement("canvas"); c.width = c.height = size; const g = c.getContext("2d");
  const gr = g.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(hard || 0.25, "rgba(255,255,255,.55)"); gr.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = gr; g.fillRect(0, 0, size, size); const t = new THREE.CanvasTexture(c); return t;
}
const SOFT = softTex();

// back glow + floor
{
  const c = document.createElement("canvas"); c.width = c.height = 512; const g = c.getContext("2d");
  const gr = g.createRadialGradient(256, 256, 0, 256, 256, 256); gr.addColorStop(0, T.glow ?? "rgba(224,168,75,0.35)"); gr.addColorStop(0.5, "rgba(120,80,30,0.10)"); gr.addColorStop(1, "rgba(0,0,0,0)");
  g.fillStyle = gr; g.fillRect(0, 0, 512, 512);
  const m = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(c), transparent: true, depthWrite: false, fog: false }));
  m.position.set(0, 8, -28); scene.add(m);
}
const floor = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), new THREE.MeshLambertMaterial({ color: "#0b0907" }));
floor.rotation.x = -Math.PI / 2; floor.position.y = -0.25; floor.visible = !!T.floor; scene.add(floor);

// dust
const DUST = 260;
const dustG = new THREE.BufferGeometry(); const dustP = new Float32Array(DUST * 3); dustG.setAttribute("position", new THREE.BufferAttribute(dustP, 3));
const dust = new THREE.Points(dustG, new THREE.PointsMaterial({ size: 0.07, map: SOFT, color: "#E8C27A", transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending }));
scene.add(dust);

// ---------- keyboard ----------
const LO = 33, HI = 88, WW = 0.30, KL = 1.5, BL = 0.95;
const isBlack = (m) => [1, 3, 6, 8, 10].includes(((m % 12) + 12) % 12);
const whiteIdx = (m) => { let n = 0; for (let k = LO; k < m; k++) if (!isBlack(k)) n++; return n; };
const C4X = whiteIdx(60);
const BOFF = { 1: -0.06, 3: 0.06, 6: -0.08, 8: 0, 10: 0.08 };
function keyX(m) { if (!isBlack(m)) return (whiteIdx(m) - C4X) * WW; return (whiteIdx(m - 1) - C4X) * WW + WW / 2 + BOFF[m % 12] * WW; }
const ALPHA = T.tilt ?? 0.42, VEL = T.speed ?? 2.4, SMAX = 18;
const HY = 0.2, HZ = -0.8;
const U = new THREE.Vector3(0, Math.cos(ALPHA), -Math.sin(ALPHA));
const QW = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), -ALPHA);
const kb = new THREE.Group(); scene.add(kb);
const keys = {};
const wGeo = new THREE.BoxGeometry(WW - 0.014, 0.16, KL); wGeo.translate(0, -0.08, KL / 2);
const bGeo = new THREE.BoxGeometry(0.17, 0.14, BL); bGeo.translate(0, -0.07, BL / 2);
for (let m = LO; m <= HI; m++) {
  const blk = isBlack(m);
  const mat = new THREE.MeshStandardMaterial({ color: blk ? "#121212" : "#F1ECE3", roughness: blk ? 0.32 : 0.38, metalness: blk ? 0.2 : 0.0, emissive: "#000", transparent: true });
  const mesh = new THREE.Mesh(blk ? bGeo : wGeo, mat); mesh.position.set(keyX(m), blk ? 0.27 : 0.16, -0.75); kb.add(mesh);
  keys[m] = { mesh, mat, base: new THREE.Color(blk ? "#121212" : "#F1ECE3"), blk, home: mesh.position.clone() };
}
const rail = new THREE.Mesh(new THREE.BoxGeometry((whiteIdx(HI) + 1) * WW + 0.3, 0.32, 0.12), new THREE.MeshStandardMaterial({ color: "#0d0b09", roughness: 0.4, metalness: 0.5, transparent: true }));
rail.position.set(((whiteIdx(LO) + whiteIdx(HI)) / 2 - C4X) * WW, 0.08, -0.86); kb.add(rail);
const hitLine = new THREE.Mesh(new THREE.BoxGeometry((whiteIdx(HI) + 1) * WW + 0.3, 0.025, 0.03), new THREE.MeshBasicMaterial({ color: "#F2C46B", toneMapped: false, transparent: true }));
hitLine.position.set(rail.position.x, HY, HZ - 0.01); kb.add(hitLine);
const hitGlow = new THREE.Mesh(new THREE.PlaneGeometry((whiteIdx(HI) + 1) * WW + 1.2, 0.7), new THREE.MeshBasicMaterial({ map: SOFT, color: "#F2C46B", transparent: true, opacity: 0.35, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }));
hitGlow.position.set(rail.position.x, HY + 0.05, HZ - 0.06); hitGlow.quaternion.copy(QW); kb.add(hitGlow);

// notes
const NOTES = (T.notes ?? []).map((n, i) => ({ ...n, i, hide: n.hide || n.m < LO || n.m > HI, x: keyX(clamp(n.m, LO, HI)), w: isBlack(n.m) ? 0.15 : WW * 0.82 }));
const SECS = Object.fromEntries((T.secs ?? []).map((s) => [s.id, s]));
const secOn = (sec, t) => { const s = SECS[sec]; return !s || (t >= s.t0 && t < s.t1); };
const NMAX = Math.max(1, NOTES.length);
const noteMesh = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({ toneMapped: false, transparent: true }), NMAX);
const haloMesh = new THREE.InstancedMesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: SOFT, transparent: true, opacity: 0.5, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }), NMAX);
noteMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage); haloMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
noteMesh.setColorAt(0, new THREE.Color()); haloMesh.setColorAt(0, new THREE.Color());
kb.add(noteMesh); kb.add(haloMesh);
const SPK = 2600;
const spkG = new THREE.BufferGeometry(); const spkP = new Float32Array(SPK * 3), spkC = new Float32Array(SPK * 3);
spkG.setAttribute("position", new THREE.BufferAttribute(spkP, 3)); spkG.setAttribute("color", new THREE.BufferAttribute(spkC, 3));
const sparks = new THREE.Points(spkG, new THREE.PointsMaterial({ size: 0.075, map: SOFT, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
kb.add(sparks);
const keyGlow = new THREE.InstancedMesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: SOFT, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false }), 64);
keyGlow.setColorAt(0, new THREE.Color()); kb.add(keyGlow);

// zones (highlight a key range on the wall)
const ZONES = (T.zones ?? []).map((z) => {
  const x0 = keyX(z.lo) - WW * 0.55, x1 = keyX(z.hi) + WW * 0.55; const h = z.h ?? 9;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, h), new THREE.MeshBasicMaterial({ color: z.col ?? "#F2C46B", transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
  m.quaternion.copy(QW); const c = new THREE.Vector3((x0 + x1) / 2, HY, HZ - 0.02).addScaledVector(U, h / 2); m.position.copy(c); kb.add(m);
  const e = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(x1 - x0, h)), new THREE.LineBasicMaterial({ color: z.col ?? "#F2C46B", transparent: true, opacity: 0, toneMapped: false }));
  e.quaternion.copy(QW); e.position.copy(c); kb.add(e);
  return { ...z, m, e };
});

// ---------- camera-space fx ----------
const camSpace = new THREE.Group(); camera.add(camSpace);
const FOVT = Math.tan(((T.fov ?? 45) * Math.PI) / 360);
const pyToWorld = (py, d) => (0.5 - py / 1920) * 2 * d * FOVT;
const pxToWorld = (px, d) => (px / 1080 - 0.5) * 2 * d * FOVT * (1080 / 1920);
const FX = T.fx ?? [];
const CONF = FX.filter((f) => f.type === "confetti"), SHARD = FX.filter((f) => f.type === "shards");
const CMAX = 420;
const confMesh = new THREE.InstancedMesh(new THREE.PlaneGeometry(0.085, 0.05), new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, toneMapped: false, transparent: true, depthTest: false }), CMAX);
confMesh.renderOrder = 30; confMesh.setColorAt(0, new THREE.Color()); camSpace.add(confMesh);
const triG = new THREE.BufferGeometry(); triG.setAttribute("position", new THREE.BufferAttribute(new Float32Array([0, 0.09, 0, -0.07, -0.05, 0, 0.08, -0.04, 0]), 3)); triG.computeVertexNormals();
const shardMesh = new THREE.InstancedMesh(triG, new THREE.MeshBasicMaterial({ side: THREE.DoubleSide, toneMapped: false, depthTest: false, transparent: true }), CMAX);
shardMesh.renderOrder = 30; shardMesh.setColorAt(0, new THREE.Color()); camSpace.add(shardMesh);
const CONF_COLS = ["#F2C46B", "#FFFFFF", "#FF5C7A", "#5FB4FF", "#5FE3A1", "#F7E3B0"].map((c) => new THREE.Color(c));
const RINGS = FX.filter((f) => f.type === "ring").map((f) => { const m = new THREE.Mesh(new THREE.TorusGeometry(1, 0.018, 8, 120), new THREE.MeshBasicMaterial({ color: f.col ?? "#F2C46B", transparent: true, blending: THREE.AdditiveBlending, depthTest: false, toneMapped: false })); m.renderOrder = 29; camSpace.add(m); return { f, m }; });
const dimmer = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshBasicMaterial({ color: BG, transparent: true, opacity: 0, depthWrite: false, depthTest: false }));
dimmer.renderOrder = 15; dimmer.position.z = -13; camSpace.add(dimmer);

// 3D text slams
const SLAMS = (T.slams ?? []).map((s) => {
  const size = s.size ?? 1.0;
  const geo = new TextGeometry(s.text, { font: font3d, size, height: size * 0.3, depth: size * 0.3, curveSegments: 6, bevelEnabled: true, bevelThickness: size * 0.05, bevelSize: size * 0.03, bevelSegments: 3 });
  geo.computeBoundingBox(); const bb = geo.boundingBox; geo.translate(-(bb.max.x + bb.min.x) / 2, -(bb.max.y + bb.min.y) / 2, -(bb.max.z + bb.min.z) / 2);
  const col = new THREE.Color(s.col === "red" ? "#E8302C" : s.col === "white" ? "#E9E4DA" : s.col === "blue" ? "#4E9FEA" : s.col === "green" ? "#3FCB86" : "#D99A2B");
  const mat = new THREE.MeshStandardMaterial({ color: col, metalness: s.col === "white" ? 0.1 : 0.6, roughness: 0.3, emissive: col, emissiveIntensity: 0, transparent: true, depthTest: false, toneMapped: false });
  const mesh = new THREE.Mesh(geo, mat); mesh.renderOrder = 25; camSpace.add(mesh);
  const d = s.z ?? 7; const width = bb.max.x - bb.min.x; const maxW = 2 * d * FOVT * (1080 / 1920) * 0.86;
  return { s, mesh, mat, d, fit: Math.min(1, maxW / width) };
});

// cards (display-list canvases)
const CARDS = (T.cards ?? []).map((c) => {
  const px = c.px ?? 220; const cw = Math.round(c.w * px), ch = Math.round(c.h * px);
  const cv = document.createElement("canvas"); cv.width = cw; cv.height = ch; const g = cv.getContext("2d");
  g.beginPath(); g.roundRect(3, 3, cw - 6, ch - 6, (c.radius ?? 0.12) * px); g.fillStyle = c.bg ?? "rgba(20,17,14,0.94)"; g.fill();
  if (c.border) { g.lineWidth = c.bw ?? 5; g.strokeStyle = c.border; g.stroke(); }
  for (const it of c.items ?? []) {
    if (it.t === "rect") { g.beginPath(); g.roundRect(it.x * px, it.y * px, it.w * px, it.h * px, (it.r ?? 0) * px); g.fillStyle = it.color; g.fill(); if (it.stroke) { g.lineWidth = it.lw ?? 3; g.strokeStyle = it.stroke; g.stroke(); } }
    else if (it.t === "text") { g.font = `${it.weight ?? 700} ${Math.round(it.size * px)}px ${it.font ?? "Inter"}`; g.fillStyle = it.color ?? "#fff"; g.textAlign = it.align ?? "left"; g.textBaseline = "alphabetic"; if (it.ls) g.letterSpacing = it.ls + "px"; g.fillText(it.text, it.x * px, it.y * px); g.letterSpacing = "0px"; }
    else if (it.t === "circle") { g.beginPath(); g.arc(it.x * px, it.y * px, it.r * px, 0, 7); if (it.color) { g.fillStyle = it.color; g.fill(); } if (it.stroke) { g.lineWidth = it.lw ?? 3; g.strokeStyle = it.stroke; g.stroke(); } }
  }
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, toneMapped: false, depthTest: c.space !== "cam", side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(c.w, c.h), mat); if (c.space === "cam") { mesh.renderOrder = 18; camSpace.add(mesh); } else scene.add(mesh);
  return { c, mesh, mat };
});
function keyed(keys, t) {
  if (!keys || !keys.length) return null;
  if (t <= keys[0].t) return keys[0];
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i], b = keys[i + 1];
    if (t < b.t) { const k = (EASES[b.e ?? "io"] ?? easeIO)((t - a.t) / (b.t - a.t)); const o = {}; for (const f of ["p", "r", "l"]) if (a[f] && b[f]) o[f] = a[f].map((v, j) => lerp(v, b[f][j], k)); for (const f of ["s", "o", "v"]) if (a[f] !== undefined && b[f] !== undefined) o[f] = lerp(a[f], b[f], k); return o; }
  }
  return keys[keys.length - 1];
}

// phone
const phone = makePhone(); camSpace.add(phone.group); phone.group.visible = false;
const PH = T.phone;

// ---------- HTML elements ----------
const stage = $("stage");
const ELS = (T.els ?? []).map((e, i) => {
  const o = document.createElement("div"); o.className = "el"; o.style.cssText = `top:${e.y ?? 140}px;` + (e.style ?? "");
  const inn = document.createElement("div"); inn.className = "in " + (e.cls ?? "cap"); o.appendChild(inn);
  if (e.type === "timer") inn.innerHTML = `<svg viewBox="0 0 220 220"><circle cx="110" cy="110" r="96" fill="rgba(0,0,0,.45)" stroke="rgba(255,255,255,.15)" stroke-width="14"/><circle class="arc" cx="110" cy="110" r="96" fill="none" stroke="#F2C46B" stroke-width="14" stroke-linecap="round" transform="rotate(-90 110 110)" stroke-dasharray="603" stroke-dashoffset="0"/></svg><div class="n"></div>`;
  else inn.innerHTML = e.html ?? "";
  o.style.display = "none"; stage.insertBefore(o, $("flash")); return { e, o, inn, last: "" };
});

function uiEl(E, t) {
  const e = E.e; const tin = e.din ?? (e.in === "slam" ? 0.22 : 0.28), tout = e.dout ?? 0.18;
  if (t < e.t0 || t >= e.t1 + (e.out === "none" ? 0 : tout)) { if (E.o.style.display !== "none") E.o.style.display = "none"; return; }
  if (E.o.style.display !== "flex") E.o.style.display = "flex";
  const a = t - e.t0; let op = 1, sc = 1, ty = 0, tx = 0, rot = 0;
  const kin = clamp(a / tin);
  switch (e.in ?? "pop") {
    case "pop": sc = lerp(0.6, 1, back(kin)); op = clamp(a / 0.12); break;
    case "fade": op = ease(kin); break;
    case "up": ty = lerp(60, 0, ease(kin)); op = ease(kin); break;
    case "down": ty = lerp(-60, 0, ease(kin)); op = ease(kin); break;
    case "left": tx = lerp(-700, 0, ease(kin)); op = clamp(a / 0.1); break;
    case "right": tx = lerp(700, 0, ease(kin)); op = clamp(a / 0.1); break;
    case "slam": sc = lerp(2.3, 1, ease(kin)); op = clamp(a / 0.08); break;
    case "spin": sc = lerp(0.2, 1, back(kin)); rot = lerp(-25, 0, ease(kin)); op = clamp(a / 0.1); break;
    default: break;
  }
  if (t >= e.t1) { const ko = clamp((t - e.t1) / tout); if (e.out === "pop") { sc *= lerp(1, 0.7, ko); } if (e.out === "upout") ty -= 80 * ko; op *= 1 - ko; }
  if (e.pulse) { const p = Math.max(0, Math.sin((t - e.t0) * Math.PI * 2 * e.pulse)); sc *= 1 + 0.035 * p; }
  if (e.shake) { const s = e.shake * Math.exp(-a * 6); tx += s * Math.sin(a * 90); }
  E.inn.style.opacity = op.toFixed(3); E.inn.style.transform = `translate(${tx.toFixed(1)}px,${ty.toFixed(1)}px) scale(${sc.toFixed(4)}) rotate(${rot.toFixed(2)}deg)`;
  if (e.count) { const c = e.count; const k = easeIO((t - c.t0) / Math.max(0.001, c.t1 - c.t0)); const v = lerp(c.from, c.to, k); const txt = (c.fmt ?? "{v}").replace("{v}", v.toFixed(c.dec ?? 0)); if (txt !== E.last) { E.inn.innerHTML = txt; E.last = txt; } }
  if (e.type === "timer") { const k = clamp(a / (e.t1 - e.t0)); E.inn.querySelector(".arc").setAttribute("stroke-dashoffset", (603 * k).toFixed(1)); const n = String(Math.max(1, Math.ceil(e.n * (1 - k)))); if (n !== E.last) { E.inn.querySelector(".n").textContent = n; E.last = n; } }
  if (e.width) { const w = e.width; const k = easeIO((t - w.t0) / Math.max(0.001, w.t1 - w.t0)); const bar = E.inn.querySelector(".fill"); if (bar) bar.style.width = lerp(w.from, w.to, k).toFixed(1) + "%"; }
}

// ---------- per frame ----------
const _m = new THREE.Matrix4(), _p = new THREE.Vector3(), _s = new THREE.Vector3(), _q = new THREE.Quaternion(), _c = new THREE.Color(), _e = new THREE.Euler();
const CAM = T.cam ?? [{ t: 0, p: [0, 3.2, 9.5], l: [0, 2.4, -0.8] }];
function camAt(t) {
  const k = keyed(CAM, t); camera.position.set(...k.p); const l = new THREE.Vector3(...k.l);
  const dr = T.drift ?? 1; camera.position.x += 0.06 * dr * Math.sin(0.37 * t); camera.position.y += 0.045 * dr * Math.sin(0.29 * t + 1);
  for (const f of FX) if (f.type === "shake" && t >= f.t && t < f.t + 1.2) { const a = (f.a ?? 0.16) * Math.exp(-(t - f.t) * 7); camera.position.x += a * Math.sin(95 * t); camera.position.y += a * Math.cos(81 * t); l.x += a * 0.5 * Math.sin(77 * t); }
  camera.lookAt(l); if (k.r) camera.rotation.z += k.r[2] ?? 0;
}
function seg(list, t, fade = 0.25) { let v = 0; for (const d of list ?? []) { if (t >= d.t0 - fade && t < d.t1 + fade) { const a = clamp((t - d.t0 + fade) / fade), b = clamp((d.t1 + fade - t) / fade); v = Math.max(v, (d.v ?? 1) * Math.min(a, b)); } } return v; }

function updateKeyboard(t) {
  // explode
  let ex = null; for (const f of FX) if (f.type === "explode" && t >= f.t0 && t < (f.t1 ?? 99) + 0.7) ex = f;
  const kbo = T.kb ? (keyed(T.kb, t).o ?? 1) : 1;
  kb.visible = kbo > 0.01;
  for (const m in keys) { const K = keys[m]; K.mat.opacity = kbo; K.mesh.position.copy(K.home); K.mesh.rotation.set(0, 0, 0); K.mat.color.copy(K.base); K.mat.emissive.setRGB(0, 0, 0); }
  rail.material.opacity = kbo; hitLine.material.opacity = kbo; hitGlow.material.opacity = 0.35 * kbo;
  if (ex) {
    let a = t - ex.t0; const ret = ex.t1 ?? 99;
    if (t > ret) a = (ret - ex.t0) * (1 - easeIO((t - ret) / 0.65));
    for (const m in keys) {
      const K = keys[m], i = +m; const vx = (hash(i, 1) - 0.5) * 7, vy = 2.5 + hash(i, 2) * 5, vz = 1.5 + hash(i, 3) * 5;
      const dd = (1 - Math.exp(-1.4 * a)) / 1.4;
      K.mesh.position.set(K.home.x + vx * dd, K.home.y + vy * dd - 1.2 * a * a * (t <= ret ? 1 : 0.3), K.home.z + vz * dd);
      K.mesh.rotation.set((hash(i, 4) - 0.5) * 9 * dd, (hash(i, 5) - 0.5) * 9 * dd, (hash(i, 6) - 0.5) * 9 * dd);
      K.mat.emissive.set("#FF2A2A").multiplyScalar(0.6 * Math.exp(-a * 2));
    }
  }
  // notes + key presses
  let n = 0, s = 0, g = 0; const pressed = {};
  for (const N of NOTES) {
    if (ex || !secOn(N.sec, t) || N.hide) continue;
    const s0 = (N.t - t) * VEL, s1 = s0 + N.d * VEL;
    if (s1 > 0 && s0 < SMAX) {
      const a0 = Math.max(0, s0), a1 = Math.min(SMAX, s1), len = a1 - a0;
      if (len > 0.005) {
        _p.set(N.x, HY, HZ).addScaledVector(U, a0 + len / 2); _s.set(N.w, len, 0.07); _m.compose(_p, QW, _s); noteMesh.setMatrixAt(n, _m);
        const near = clamp(1 - s0 / 9); _c.copy(hc[N.h] ?? hc.R).multiplyScalar(0.55 + 0.6 * near); if (s0 <= 0) _c.multiplyScalar(1.35); noteMesh.setColorAt(n, _c);
        _p.addScaledVector(new THREE.Vector3(0, Math.sin(ALPHA), Math.cos(ALPHA)), 0.02); _s.set(N.w * 2.6, len + 0.5, 1); _m.compose(_p, QW, _s); haloMesh.setMatrixAt(n, _m); _c.copy(hc[N.h] ?? hc.R).multiplyScalar(0.28 + 0.3 * near); haloMesh.setColorAt(n, _c);
        n++;
      }
    }
    const end = Math.max(N.t + N.d, N.pe ? Math.min(N.pe, SECS[N.sec]?.t1 ?? 999) : 0);
    if (t >= N.t && t < end) { const held = t < N.t + N.d; const p = pressed[N.m]; const age = t - N.t; if (!p || (held && !p.held)) pressed[N.m] = { h: N.h, held, age, v: N.v ?? 0.7 }; }
    // sparks
    const age = t - N.t;
    if (age >= 0 && age < 0.6) {
      const cnt = N.h === "X" ? 18 : 10; const col = hc[N.h] ?? hc.R;
      for (let k = 0; k < cnt && s < SPK; k++) {
        const life = 0.32 + 0.3 * hash(N.i, k); if (age > life) continue;
        const vx = (hash(N.i, k + 50) - 0.5) * 1.8, vy = 1.0 + 2.4 * hash(N.i, k + 90), vz = 0.3 + (hash(N.i, k + 130) - 0.3) * 1.2;
        spkP[s * 3] = N.x + vx * age; spkP[s * 3 + 1] = HY + 0.05 + vy * age - 4.2 * age * age; spkP[s * 3 + 2] = HZ + 0.05 + vz * age;
        const f = 1 - age / life; spkC[s * 3] = col.r * f * 1.4; spkC[s * 3 + 1] = col.g * f * 1.4; spkC[s * 3 + 2] = col.b * f * 1.4; s++;
      }
    }
  }
  noteMesh.count = n; haloMesh.count = n; noteMesh.instanceMatrix.needsUpdate = true; haloMesh.instanceMatrix.needsUpdate = true;
  if (noteMesh.instanceColor) noteMesh.instanceColor.needsUpdate = true; if (haloMesh.instanceColor) haloMesh.instanceColor.needsUpdate = true;
  spkG.setDrawRange(0, s); spkG.attributes.position.needsUpdate = true; spkG.attributes.color.needsUpdate = true;
  for (const m in pressed) {
    const K = keys[m]; if (!K) continue; const P = pressed[m]; const col = hc[P.h] ?? hc.R;
    if (P.held) { K.mesh.rotation.x = 0.055 * clamp(P.age / 0.03); K.mat.color.copy(K.base).lerp(col, K.blk ? 0.75 : 0.6); K.mat.emissive.copy(col).multiplyScalar(K.blk ? 0.55 : 0.35); }
    else { K.mat.color.copy(K.base).lerp(col, 0.25); K.mat.emissive.copy(col).multiplyScalar(0.12); }
    if (g < 64) { _p.set(K.home.x, HY + 0.06, HZ + 0.06); const pulse = P.held ? 1.0 + 0.6 * Math.exp(-P.age * 8) : 0.5; _s.set((K.blk ? 0.5 : 0.75) * pulse, 0.9 * pulse, 1); _m.compose(_p, QW, _s); keyGlow.setMatrixAt(g, _m); _c.copy(col).multiplyScalar(P.held ? 0.9 : 0.35); keyGlow.setColorAt(g, _c); g++; }
  }
  keyGlow.count = g; keyGlow.instanceMatrix.needsUpdate = true; if (keyGlow.instanceColor) keyGlow.instanceColor.needsUpdate = true;
  for (const Z of ZONES) { const v = seg([Z], t, 0.2); Z.m.material.opacity = 0.12 * v; Z.e.material.opacity = 0.9 * v; }
}

function updateFx(t) {
  // confetti
  let c = 0;
  for (let ei = 0; ei < CONF.length; ei++) {
    const f = CONF[ei]; const a = t - f.t; if (a < 0 || a > 3.2) continue; const d = 6; const oy = pyToWorld(f.y ?? 760, d), ox = pxToWorld(f.x ?? 540, d); const N = Math.min(f.n ?? 220, CMAX - c);
    for (let j = 0; j < N; j++) {
      const vx = (hash(ei * 7 + 1, j) - 0.5) * 7.5, vy = 1.5 + 5.5 * hash(ei * 7 + 2, j), vz = (hash(ei * 7 + 3, j) - 0.5) * 3; const dr = (1 - Math.exp(-1.7 * a)) / 1.7;
      _p.set(ox + vx * dr, oy + vy * dr - 1.4 * a * a, -d + vz * dr); _e.set(a * 9 * hash(j, 4), a * 7 * hash(j, 5), a * 5); _q.setFromEuler(_e);
      const life = 2.2 + hash(j, 6); const sc = a > life ? 0 : 1 - Math.pow(a / life, 6); _s.set(sc, sc, sc); _m.compose(_p, _q, _s); confMesh.setMatrixAt(c, _m); confMesh.setColorAt(c, CONF_COLS[j % CONF_COLS.length]); c++;
    }
  }
  confMesh.count = c; confMesh.instanceMatrix.needsUpdate = true; if (confMesh.instanceColor) confMesh.instanceColor.needsUpdate = true;
  let sh = 0;
  for (let ei = 0; ei < SHARD.length; ei++) {
    const f = SHARD[ei]; const a = t - f.t; if (a < 0 || a > 2.5) continue; const d = 6; const oy = pyToWorld(f.y ?? 1100, d), ox = pxToWorld(f.x ?? 540, d); const N = Math.min(f.n ?? 140, CMAX - sh);
    for (let j = 0; j < N; j++) {
      const ang = hash(ei + 11, j) * Math.PI * 2, sp = 2 + 6 * hash(ei + 12, j); const dr = (1 - Math.exp(-2.2 * a)) / 2.2;
      _p.set(ox + Math.cos(ang) * sp * dr, oy + Math.sin(ang) * sp * dr - 2.2 * a * a, -d + (hash(j, 9) - 0.5) * 2 * dr); _e.set(a * 12 * hash(j, 4), a * 10 * hash(j, 5), a * 8); _q.setFromEuler(_e);
      const sc = (0.6 + hash(j, 8)) * Math.max(0, 1 - a / 2.2); _s.set(sc, sc, sc); _m.compose(_p, _q, _s); shardMesh.setMatrixAt(sh, _m); _c.set(j % 3 ? "#FF3B3B" : "#7A1010"); shardMesh.setColorAt(sh, _c); sh++;
    }
  }
  shardMesh.count = sh; shardMesh.instanceMatrix.needsUpdate = true; if (shardMesh.instanceColor) shardMesh.instanceColor.needsUpdate = true;
  for (const R of RINGS) { const a = t - R.f.t; if (a < 0 || a > 0.6) { R.m.visible = false; continue; } R.m.visible = true; const d = 6; R.m.position.set(pxToWorld(R.f.x ?? 540, d), pyToWorld(R.f.y ?? 760, d), -d); const k = ease(a / 0.6); R.m.scale.setScalar(0.25 + (R.f.s ?? 1.8) * 0.7 * k); R.m.material.opacity = (1 - k) * 0.8; }
  // slams
  for (const S of SLAMS) {
    const s = S.s; const a = t - s.t0; const out = s.t1 ?? 99;
    if (a < 0 || t > out + 0.3) { S.mesh.visible = false; continue; } S.mesh.visible = true;
    const k = clamp(a / (s.dur ?? 0.42)); const sc = lerp(s.from ?? 1.9, 1, back(k)) * S.fit * (s.scale ?? 1);
    let op = clamp(a / 0.1); if (t > out) op *= 1 - clamp((t - out) / 0.3);
    const y = pyToWorld(s.y ?? 760, S.d), x = pxToWorld(s.x ?? 540, S.d);
    S.mesh.position.set(x, y + (t > out ? 0.6 * clamp((t - out) / 0.3) : 0), -S.d + lerp(3.2, 0, ease(k)));
    S.mesh.rotation.set(lerp(-0.9, 0, back(k)) + 0.04 * Math.sin(t * 1.3), (s.spin ? lerp(-Math.PI * 2, 0, ease(k)) : 0) + 0.12 * Math.sin(t * 0.9), 0);
    S.mesh.scale.setScalar(sc); S.mat.opacity = op; S.mat.emissiveIntensity = (s.col === "white" ? 0.05 : 0.22) + 0.9 * Math.exp(-a * 3);
  }
  // cards
  for (const C of CARDS) { const k = keyed(C.c.keys, t); if (!k || (k.o ?? 1) <= 0.001) { C.mesh.visible = false; continue; } C.mesh.visible = true; C.mesh.position.set(...k.p); if (C.c.space === "cam") C.mesh.renderOrder = 16 + Math.max(0, Math.round((12 + k.p[2]) * 4)); if (k.r) C.mesh.rotation.set(...k.r); C.mesh.scale.setScalar(k.s ?? 1); C.mat.opacity = k.o ?? 1; }
  dimmer.material.opacity = seg(T.dim, t, 0.3) * 0.92;
  // flashes
  let fl = 0, rd = 0; for (const f of FX) { if (f.type === "flash" && t >= f.t && t < f.t + (f.dur ?? 0.35)) fl = Math.max(fl, (f.a ?? 0.4) * (1 - (t - f.t) / (f.dur ?? 0.35))); if (f.type === "redflash" && t >= f.t && t < f.t + (f.dur ?? 0.5)) rd = Math.max(rd, (f.a ?? 0.7) * (1 - (t - f.t) / (f.dur ?? 0.5))); }
  $("flash").style.opacity = fl.toFixed(3); $("red").style.opacity = rd.toFixed(3);
  const hz = seg(T.haze, t, 0.4); $("haze").style.opacity = hz.toFixed(3); $("haze").style.backdropFilter = hz > 0.01 ? `blur(${(hz * (T.hazeBlur ?? 9)).toFixed(1)}px)` : "none";
  scene.fog.density = (T.fog ?? 0.028) * (1 + 2.5 * hz);
}

function updatePhone(t) {
  if (!PH || t < PH.t0) { phone.group.visible = false; return; }
  phone.group.visible = true;
  const a = t - PH.t0; const k = back(a / 0.95), k2 = ease(a / 0.95);
  const rest = PH.rest ?? [0, -0.2, -3.9];
  let x = rest[0], y = lerp(-6, rest[1], k), z = rest[2];
  const lift = PH.lift; if (lift !== undefined && t > lift) { const kl = easeIO((t - lift) / 0.6); y += 0.28 * kl; z -= 1.1 * kl; }
  if (PH.t1 && t > PH.t1) { const ko = easeIO((t - PH.t1) / 0.5); y -= 6 * ko; }
  phone.group.position.set(x, y + 0.04 * Math.sin(t * 2.1), z);
  phone.group.rotation.set(lerp(0.6, 0.0, k2) + 0.03 * Math.sin(t * 1.3), lerp(-Math.PI * 2, 0, k2) + 0.08 * Math.sin(t * 0.8), 0.02 * Math.sin(t * 1.1));
  // state
  const st = { screen: "today" }; let tapT = null, tapXY = null;
  for (const s of PH.steps ?? []) if (t >= s.t) Object.assign(st, s.set ?? {});
  for (const tp of PH.taps ?? []) if (t >= tp.t && t < tp.t + 0.45) { tapT = tp.t; tapXY = tp.at; }
  if (st.metroT0 !== undefined && st.bpm && t >= st.metroT0) st.beat = (((t - st.metroT0) * st.bpm) / 60) % 1;
  if (st.countdown) { const [t0, from] = st.countdown; st.remain = Math.max(0, from - (t - t0) * (st.speedup ?? 1)); delete st.countdown; }
  if (st.scrollTo) { const [t0, t1, a0, a1] = st.scrollTo; st.scroll = Math.round(lerp(a0, a1, easeIO((t - t0) / (t1 - t0)))); delete st.scrollTo; }
  if (st.toastAt) { const ta = t - st.toastAt[0]; st.toast = ta >= 0 ? [st.toastAt[1], clamp(ta / 0.2) * (1 - clamp((ta - 1.6) / 0.3))] : null; if (!st.toast || st.toast[1] <= 0) delete st.toast; delete st.toastAt; }
  delete st.t; delete st.metroT0;
  let anchors = phone.anchorsFor({ ...st, tap: null });
  if (tapT !== null) { const p = resolveAnchor(tapXY, anchors); if (p) st.tap = [p[0], p[1], +(t - tapT).toFixed(2)]; }
  phone.draw(st);
}
function resolveAnchor(at, A) {
  if (Array.isArray(at)) return at;
  const path = at.split("."); let v = A; for (const p of path) v = v?.[p]; return Array.isArray(v) ? v : null;
}

function updateDust(t) {
  for (let i = 0; i < DUST; i++) {
    const x = (hash(i, 1) - 0.5) * 24, z = -2 - hash(i, 2) * 16, y0 = hash(i, 3) * 12 - 1;
    dustP[i * 3] = x + 0.3 * Math.sin(t * 0.3 + i); dustP[i * 3 + 1] = ((y0 + t * (0.12 + 0.1 * hash(i, 4))) % 12) - 1; dustP[i * 3 + 2] = z;
  }
  dustG.attributes.position.needsUpdate = true;
}

window.render = function (t) {
  camAt(t); updateDust(t); updateKeyboard(t); updateFx(t); updatePhone(t);
  renderer.render(scene, camera);
  for (const E of ELS) uiEl(E, t);
};
window.__dbg = () => ({ n: noteMesh.count, notes: NOTES.length, hidden: NOTES.filter((q) => q.hide).length, first: NOTES.slice(0, 3).map((q) => [q.m, q.t, q.d, q.sec, q.hide]) });
scene.traverse((o) => { if (o.isInstancedMesh || o.isPoints) o.frustumCulled = false; });
camera.traverse((o) => { if (o.isInstancedMesh || o.isPoints) o.frustumCulled = false; });
window.__DUR = DUR; window.__FPS = T.fps ?? 30;
window.__ready = (async () => { window.render(0); return true; })();
