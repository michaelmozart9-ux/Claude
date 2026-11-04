// 3D phone showing the real Between Lessons screens (layout mirrors src/routes/plan.today.tsx).
// Plan data shown is ONLY the real example plan (src/data/example-plan.json, Week 1 Session 1).
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

const C = { bg: "#071220", fg: "#f6f3eb", card: "#0f1b2b", gold: "#dbb568", muted: "#aab2b8", pfg: "#081424", border: "rgba(246,243,235,0.13)", goldSoft: "rgba(219,181,104,0.12)", goldLine: "rgba(219,181,104,0.5)" };
const W = 720, H = 1530;
const F = (w, s) => `${w} ${s}px Geist, Inter, sans-serif`;
const MONO = (s) => `500 ${s}px "Geist Mono", Geist, monospace`;

export const SESSION = {
  eyebrow: "WEEK 1 · SESSION 1 OF 5",
  piece: "Debussy — Clair de Lune",
  section: "Opening theme (first page, up to first dynamic swell)",
  hands: "Left hand",
  tempo: "40% tempo · 36 BPM",
  bpm: 36,
  segments: [
    { name: "Warm-up", minutes: 5, instruction: "Slow broken-chord arpeggios in both hands, focusing on smooth wrist motion between low and mid-range positions." },
    { name: "Main work", minutes: 20, instruction: "Play left hand alone, very slowly, stopping before each position shift to look at and name the next landmark note." },
    { name: "Run-through", minutes: 5, instruction: "Play left hand alone straight through at the same slow tempo without stopping, even if shaky." },
  ],
  why: "Naming landmarks out loud forces your eyes and brain to register where the hand is going before it moves, which is the real fix for losing your place.",
  milestone: "Play the left hand alone for the opening theme with no hesitation, naming each landmark position out loud as you shift.",
};
export const SESSION3 = {
  eyebrow: "WEEK 1 · SESSION 3 OF 5",
  piece: "Debussy — Clair de Lune",
  section: "Opening theme, first 8 bars",
  hands: "Right hand",
  tempo: "50% tempo · 45 BPM",
  bpm: 45,
  segments: [
    { name: "Warm-up", minutes: 5, instruction: "Slow legato scale (Db major) focusing on even finger weight and singing tone." },
    { name: "Main work", minutes: 20, instruction: "Practice right-hand melody alone, shaping phrases with a slight swell toward the top note of each phrase, keeping tempo steady." },
    { name: "Run-through", minutes: 5, instruction: "Play right hand alone through the full 8 bars, listening for a singing legato line." },
  ],
  why: "Giving the melody dedicated attention now means it won't compete for focus once the left hand's landmarks are added back in.",
  milestone: SESSION.milestone,
};
export const WEEK1 = [
  ["Day 1", "Left hand", 40], ["Day 2", "Left hand", 40], ["Day 3", "Right hand", 50], ["Day 4", "Left hand", 45], ["Day 5", "Left hand", 50],
];

function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function wrap(g, text, maxW) {
  const words = text.split(" "); const lines = []; let cur = "";
  for (const w of words) { const t = cur ? cur + " " + w : w; if (g.measureText(t).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t; }
  if (cur) lines.push(cur); return lines;
}
function para(g, text, x, y, maxW, lh, maxLines = 99) {
  let lines = wrap(g, text, maxW);
  if (lines.length > maxLines) { lines = lines.slice(0, maxLines); lines[maxLines - 1] = lines[maxLines - 1].replace(/\s+\S*$/, "") + "…"; }
  lines.forEach((l, i) => g.fillText(l, x, y + i * lh)); return lines.length * lh;
}
function spaced(g, text, x, y, sp) { let cx = x; for (const ch of text) { g.fillText(ch, cx, y); cx += g.measureText(ch).width + sp; } return cx - x; }
function check(g, x, y, s, on, col = C.pfg) {
  rr(g, x, y, s, s, 8); if (on) { g.fillStyle = C.gold; g.fill(); } g.strokeStyle = on ? C.gold : "rgba(246,243,235,0.3)"; g.lineWidth = 2.5; g.stroke();
  if (on) { g.strokeStyle = col; g.lineWidth = 4; g.lineCap = "round"; g.beginPath(); g.moveTo(x + s * 0.25, y + s * 0.52); g.lineTo(x + s * 0.43, y + s * 0.7); g.lineTo(x + s * 0.76, y + s * 0.32); g.stroke(); }
}
function btn(g, x, y, w, h, label, filled, size = 28) {
  rr(g, x, y, w, h, h / 2); if (filled) { g.fillStyle = C.gold; g.fill(); } else { g.strokeStyle = "rgba(246,243,235,0.25)"; g.lineWidth = 2; g.stroke(); }
  g.fillStyle = filled ? C.pfg : C.fg; g.font = F(600, size); g.textAlign = "center"; g.fillText(label, x + w / 2, y + h / 2 + size * 0.36); g.textAlign = "left";
}
function chip(g, x, y, text, gold, maxW) {
  g.font = F(500, 21); const lines = wrap(g, text, maxW - 36); const w = Math.max(...lines.map((l) => g.measureText(l).width)) + 36; const h = 22 + lines.length * 27;
  rr(g, x, y, w, h, lines.length > 1 ? 22 : h / 2); g.fillStyle = gold ? C.goldSoft : "rgba(7,18,32,0.6)"; g.fill(); g.strokeStyle = gold ? C.goldLine : C.border; g.lineWidth = 2; g.stroke();
  g.fillStyle = gold ? C.gold : C.muted; lines.forEach((l, i) => g.fillText(l, x + 18, y + 33 + i * 27)); return [w, h];
}
function playIcon(g, cx, cy, s, col) { g.fillStyle = col; g.beginPath(); g.moveTo(cx - s * 0.35, cy - s * 0.45); g.lineTo(cx + s * 0.5, cy); g.lineTo(cx - s * 0.35, cy + s * 0.45); g.closePath(); g.fill(); }

// Draws the full (tall) Today page. Returns layout anchors for taps.
function drawToday(g, st, PH) {
  const S = st.session === 3 ? SESSION3 : SESSION, X = 44, CW = W - 2 * X; const A = {};
  g.fillStyle = C.bg; g.fillRect(0, 0, W, PH);
  const grd = g.createRadialGradient(W * 0.5, 0, 10, W * 0.5, 0, 700); grd.addColorStop(0, "rgba(219,181,104,0.10)"); grd.addColorStop(1, "rgba(219,181,104,0)"); g.fillStyle = grd; g.fillRect(0, 0, W, 800);
  let y = 150;
  g.fillStyle = C.gold; g.beginPath(); g.arc(X + 12, y - 9, 10, 0, 7); g.fill();
  g.fillStyle = C.fg; g.font = F(600, 27); g.fillText("Between Lessons", X + 32, y);
  g.fillStyle = C.muted; g.font = F(400, 23); g.textAlign = "right"; g.fillText("← My plan", W - X, y); g.textAlign = "left";
  y = 245; g.fillStyle = C.gold; g.font = F(600, 18); spaced(g, S.eyebrow, X, y, 3.6);
  y = 312; g.fillStyle = C.fg; g.font = F(600, 54); y += para(g, S.piece, X, y, CW, 58) - 58;
  y += 42; let cx = X, rowH = 0;
  for (const [txt, gold] of [[S.section, false], [S.hands, false], [S.tempo, true]]) {
    g.font = F(500, 21); const est = Math.min(CW, g.measureText(txt).width + 36);
    if (cx + est > X + CW) { cx = X; y += rowH + 12; rowH = 0; }
    const [w, h] = chip(g, cx, y, txt, gold, CW); if (gold) A.tempoChip = [cx + w / 2, y + h / 2];
    cx += w + 12; rowH = Math.max(rowH, h);
  }
  y += rowH + 30;
  // metronome
  rr(g, X, y, CW, 132, 18); g.fillStyle = C.card; g.fill(); g.strokeStyle = C.border; g.lineWidth = 2; g.stroke();
  g.fillStyle = C.muted; g.font = F(500, 19); spaced(g, "METRONOME", X + 28, y + 42, 3);
  const bpm = st.bpm ?? S.bpm; g.fillStyle = C.fg; g.font = F(600, 46); g.fillText(String(bpm), X + 28, y + 100); const bw = g.measureText(String(bpm)).width;
  g.fillStyle = C.muted; g.font = F(500, 21); g.fillText("BPM", X + 36 + bw, y + 100);
  for (let i = 0; i < 4; i++) { const on = st.beat !== undefined && Math.floor(st.beat * 4) % 4 === i; g.fillStyle = on ? C.gold : "rgba(246,243,235,0.16)"; g.beginPath(); g.arc(X + 300 + i * 34, y + 86, on ? 11 : 8, 0, 7); g.fill(); }
  for (const [k, lab] of [[0, "−"], [1, "+"]]) { const bx = X + CW - 210 + k * 70; rr(g, bx, y + 40, 56, 56, 28); g.strokeStyle = "rgba(246,243,235,0.25)"; g.stroke(); g.fillStyle = C.fg; g.font = F(500, 34); g.textAlign = "center"; g.fillText(lab, bx + 28, y + 80); g.textAlign = "left"; }
  const pbx = X + CW - 70; g.fillStyle = C.gold; g.beginPath(); g.arc(pbx + 28, y + 68, 30, 0, 7); g.fill();
  if (st.beat !== undefined) { g.fillStyle = C.pfg; g.fillRect(pbx + 18, y + 54, 8, 28); g.fillRect(pbx + 31, y + 54, 8, 28); } else playIcon(g, pbx + 30, y + 68, 26, C.pfg);
  A.metro = [pbx + 28, y + 68];
  y += 132 + 26;
  // segments
  A.seg = [];
  S.segments.forEach((s, i) => {
    const on = st.ticks?.[i], run = st.hl === i;
    g.font = F(400, 21); const lines = wrap(g, s.instruction, CW - 170).slice(0, 3); const h = 92 + lines.length * 28;
    rr(g, X, y, CW, h, 14); g.fillStyle = run ? C.goldSoft : C.bg; g.fill(); g.strokeStyle = run ? C.gold : C.border; g.lineWidth = run ? 3 : 2; g.stroke();
    if (on && !run) { g.fillStyle = "rgba(7,18,32,0.35)"; g.fill(); }
    check(g, X + 24, y + 26, 38, on); A.seg.push([X + 43, y + 45]);
    g.fillStyle = C.fg; g.font = F(600, 28); g.fillText(s.name, X + 82, y + 54); const nw = g.measureText(s.name).width;
    g.fillStyle = C.muted; g.font = MONO(19); g.fillText(`· ${s.minutes} min`, X + 92 + nw, y + 54);
    const rem = run && st.remain !== undefined ? st.remain : on ? 0 : s.minutes * 60;
    g.font = MONO(24); g.fillStyle = run ? C.gold : C.muted; g.textAlign = "right"; g.fillText(`${Math.floor(rem / 60)}:${String(Math.floor(rem % 60)).padStart(2, "0")}`, X + CW - 92, y + 54); g.textAlign = "left";
    g.fillStyle = C.muted; g.font = F(400, 21); lines.forEach((l, k) => g.fillText(l, X + 82, y + 92 + k * 28));
    const bx = X + CW - 76, by = y + 22; rr(g, bx, by, 56, 56, 12); if (run) { g.fillStyle = C.gold; g.fill(); } else { g.strokeStyle = "rgba(246,243,235,0.25)"; g.lineWidth = 2; g.stroke(); }
    if (run) { g.fillStyle = C.pfg; g.fillRect(bx + 19, by + 16, 7, 24); g.fillRect(bx + 31, by + 16, 7, 24); } else playIcon(g, bx + 30, by + 28, 22, C.fg);
    A.seg[i].push(bx + 28, by + 28);
    y += h + 16;
  });
  y += 14; g.fillStyle = C.muted; g.font = `italic 400 21px Geist, Inter`; y += para(g, "Why: " + S.why, X, y + 20, CW, 30, 3) + 8;
  rr(g, X, y, CW, 150, 18); g.fillStyle = C.goldSoft; g.fill(); g.strokeStyle = C.goldLine; g.lineWidth = 2; g.stroke();
  g.fillStyle = C.gold; g.font = F(600, 22); g.fillText("This week's milestone ·", X + 64, y + 44);
  g.strokeStyle = C.gold; g.lineWidth = 3; g.beginPath(); g.arc(X + 34, y + 37, 12, 0, 7); g.stroke(); g.beginPath(); g.arc(X + 34, y + 37, 4, 0, 7); g.stroke();
  g.fillStyle = C.fg; g.font = F(400, 21); para(g, S.milestone, X + 64, y + 76, CW - 90, 29, 3);
  y += 150 + 36;
  if (st.phase === "checkin" || st.phase === "rated") {
    rr(g, X, y, CW, 470, 18); g.fillStyle = C.card; g.fill(); g.strokeStyle = C.border; g.lineWidth = 2; g.stroke();
    g.fillStyle = C.fg; g.font = F(600, 36); g.fillText("How did it go?", X + 28, y + 64);
    const R = [["😣", "Too hard", "hard"], ["👍", "Just right", "right"], ["😎", "Too easy", "easy"]]; const bw2 = (CW - 56 - 24) / 3; A.rate = {};
    R.forEach(([em, lab, key], i) => {
      const bx = X + 28 + i * (bw2 + 12), by = y + 96, sel = st.rating === key;
      rr(g, bx, by, bw2, 150, 14); g.fillStyle = sel ? "rgba(219,181,104,0.18)" : C.bg; g.fill(); g.strokeStyle = sel ? C.gold : C.border; g.lineWidth = sel ? 3 : 2; g.stroke();
      g.font = `52px "Noto Color Emoji"`; g.textAlign = "center"; g.fillText(em, bx + bw2 / 2, by + 74); g.fillStyle = C.fg; g.font = F(600, 22); g.fillText(lab, bx + bw2 / 2, by + 122); g.textAlign = "left";
      A.rate[key] = [bx + bw2 / 2, by + 75];
    });
    g.fillStyle = C.muted; g.font = F(600, 16); spaced(g, "WHAT BROKE? (OPTIONAL)", X + 28, y + 290, 2.6);
    rr(g, X + 28, y + 304, CW - 56, 62, 12); g.fillStyle = C.bg; g.fill(); g.strokeStyle = C.border; g.stroke(); g.fillStyle = "rgba(170,178,184,0.6)"; g.font = F(400, 20); g.fillText("e.g. left hand jumps in the middle section", X + 46, y + 343);
    btn(g, X + 28, y + 390, CW - 56, 62, "Save session", st.rating, 24); if (!st.rating) { g.fillStyle = "rgba(7,18,32,0.0)"; }
    A.save = [X + 28 + (CW - 56) / 2, y + 421];
    y += 470 + 30;
  } else {
    btn(g, X, y, CW, 84, "Finish session", true, 28); A.finish = [W / 2, y + 42]; y += 120;
  }
  return { A, end: y };
}

function drawSaved(g, st) {
  const X = 44, CW = W - 2 * X;
  g.fillStyle = C.bg; g.fillRect(0, 0, W, H);
  g.fillStyle = C.gold; g.beginPath(); g.arc(X + 12, 141, 10, 0, 7); g.fill(); g.fillStyle = C.fg; g.font = F(600, 27); g.fillText("Between Lessons", X + 32, 150);
  rr(g, X, 260, CW, 520, 22); g.fillStyle = C.card; g.fill(); g.strokeStyle = C.border; g.lineWidth = 2; g.stroke();
  g.fillStyle = C.gold; g.font = F(600, 18); spaced(g, "SESSION SAVED", X + 36, 334, 3.6);
  g.fillStyle = C.fg; g.font = F(600, 60); g.fillText("Nice work.", X + 36, 420);
  g.fillStyle = C.muted; g.font = F(400, 26);
  const change = st.change ?? 5;
  const txt = change === 0 ? "Next time on Debussy — Clair de Lune, the tempo stays as planned." : `Next time on Debussy — Clair de Lune, tempo goes ${change > 0 ? "up" : "down"} ${Math.abs(change)}% from the plan's target.`;
  para(g, txt, X + 36, 480, CW - 72, 38);
  btn(g, X + 36, 616, CW - 72, 70, "Next session", true, 26); btn(g, X + 36, 700, CW - 72, 64, "Back to my plan", false, 24);
  return { A: { next: [W / 2, 651] } };
}

function drawForm(g, st) {
  const X = 44, CW = W - 2 * X; const A = {};
  g.fillStyle = C.bg; g.fillRect(0, 0, W, H);
  g.fillStyle = C.gold; g.beginPath(); g.arc(X + 12, 141, 10, 0, 7); g.fill(); g.fillStyle = C.fg; g.font = F(600, 27); g.fillText("Between Lessons", X + 32, 150);
  const step = st.step ?? 1; rr(g, X, 210, CW, 8, 4); g.fillStyle = "rgba(246,243,235,0.12)"; g.fill(); rr(g, X, 210, CW * (step + 1) / 6, 8, 4); g.fillStyle = C.gold; g.fill();
  g.fillStyle = C.muted; g.font = F(500, 20); g.fillText(`Question ${step + 1} of 6`, X, 270);
  const Q = ["What grade are you working at?", "Which pieces do you want to learn?", "How many days a week can you practise?", "How long is each practice session?"];
  g.fillStyle = C.fg; g.font = F(600, 50); let y = 350 + para(g, Q[step], X, 350, CW, 56) + 20;
  const field = (label, val, yy, caret) => {
    g.fillStyle = C.muted; g.font = MONO(18); spaced(g, label.toUpperCase(), X, yy, 3);
    rr(g, X, yy + 18, CW, 84, 14); g.fillStyle = C.card; g.fill(); g.strokeStyle = caret ? C.gold : C.border; g.lineWidth = caret ? 3 : 2; g.stroke();
    g.fillStyle = val ? C.fg : "rgba(170,178,184,0.55)"; g.font = F(500, 30); g.fillText(val || "…", X + 26, yy + 72);
    if (caret) { const w = g.measureText(val || "").width; g.fillStyle = C.gold; g.fillRect(X + 28 + w, yy + 40, 3, 40); }
  };
  if (step === 0) {
    g.fillStyle = C.muted; g.font = MONO(18); spaced(g, "PIANO GRADE", X, y + 10, 3); const gw = (CW - 36) / 4;
    for (let i = 0; i < 8; i++) { const gx = X + (i % 4) * (gw + 12), gy = y + 36 + Math.floor(i / 4) * 96, sel = st.grade === i + 1; rr(g, gx, gy, gw, 80, 14); g.fillStyle = sel ? C.gold : C.card; g.fill(); g.strokeStyle = sel ? C.gold : C.border; g.lineWidth = 2; g.stroke(); g.fillStyle = sel ? C.pfg : C.fg; g.font = F(600, 24); g.textAlign = "center"; g.fillText(`Grade ${i + 1}`, gx + gw / 2, gy + 50); g.textAlign = "left"; if (!A.grades) A.grades = []; A.grades.push([gx + gw / 2, gy + 40]); }
  } else if (step === 1) {
    field("Composer 1", st.composer ?? "", y + 10, st.caret === "composer"); field("Title 1", st.title ?? "", y + 140, st.caret === "title");
  } else if (step === 2) {
    g.fillStyle = C.gold; g.font = F(600, 64); g.fillText(`${st.days ?? 5} days`, X, y + 90);
  } else if (step === 3) {
    [20, 30, 45, 60].forEach((m, i) => { const by = y + 10 + i * 100, sel = st.minutes === m; rr(g, X, by, CW, 84, 14); g.fillStyle = sel ? C.goldSoft : C.card; g.fill(); g.strokeStyle = sel ? C.gold : C.border; g.lineWidth = sel ? 3 : 2; g.stroke(); g.fillStyle = C.fg; g.font = F(500, 30); g.fillText(`${m} minutes`, X + 26, by + 54); });
  }
  btn(g, X, 1290, CW, 84, step === 5 ? "Build my plan" : "Next", true, 28); A.next = [W / 2, 1332];
  return { A };
}

function drawWeek(g, st) {
  const X = 44, CW = W - 2 * X; const A = { rows: [] };
  g.fillStyle = C.bg; g.fillRect(0, 0, W, H);
  g.fillStyle = C.gold; g.beginPath(); g.arc(X + 12, 141, 10, 0, 7); g.fill(); g.fillStyle = C.fg; g.font = F(600, 27); g.fillText("Between Lessons", X + 32, 150);
  g.fillStyle = C.fg; g.font = F(600, 50); g.fillText("Your 6-week roadmap", X, 270);
  const done = st.done ?? 0;
  g.fillStyle = C.gold; g.font = F(600, 30); g.fillText(String(done), X, 335); const dw = g.measureText(String(done)).width;
  g.fillStyle = C.muted; g.font = F(400, 22); g.fillText("sessions done · Week 1 of 6", X + dw + 12, 335);
  rr(g, X, 360, CW, 8, 4); g.fillStyle = "rgba(246,243,235,0.12)"; g.fill(); rr(g, X, 360, Math.max(8, CW * done / 30), 8, 4); g.fillStyle = C.gold; g.fill();
  g.fillStyle = C.gold; g.font = F(600, 18); spaced(g, "WEEK 1", X, 430, 3.6);
  let y = 452;
  WEEK1.forEach(([d, hands, pct], i) => {
    const isDone = done > i, next = done === i;
    rr(g, X, y, CW, 150, 16); g.fillStyle = next ? C.goldSoft : C.card; g.fill(); g.strokeStyle = next ? C.gold : C.border; g.lineWidth = next ? 3 : 2; g.stroke();
    g.fillStyle = C.muted; g.font = F(600, 17); spaced(g, d.toUpperCase(), X + 26, y + 40, 2.4);
    g.fillStyle = C.fg; g.font = F(600, 27); g.fillText("Debussy — Clair de Lune", X + 26, y + 82);
    g.fillStyle = C.muted; g.font = F(400, 21); g.fillText(`${hands} · ${pct}% tempo · 30 min`, X + 26, y + 120);
    if (isDone) { rr(g, X + CW - 140, y + 52, 116, 46, 23); g.fillStyle = C.goldSoft; g.fill(); g.strokeStyle = C.goldLine; g.lineWidth = 2; g.stroke(); g.fillStyle = C.gold; g.font = F(600, 21); g.textAlign = "center"; g.fillText("✓ Done", X + CW - 82, y + 83); g.textAlign = "left"; }
    else if (next) { rr(g, X + CW - 140, y + 50, 116, 50, 25); g.fillStyle = C.gold; g.fill(); g.fillStyle = C.pfg; g.font = F(600, 22); g.textAlign = "center"; g.fillText("Start", X + CW - 82, y + 83); g.textAlign = "left"; }
    A.rows.push([X + CW - 82, y + 75]); y += 166;
  });
  return { A };
}

function statusBar(g) {
  g.fillStyle = C.fg; g.font = F(600, 26); g.fillText("9:41", 70, 62);
  g.fillStyle = "#000"; rr(g, W / 2 - 100, 22, 200, 56, 28); g.fill();
  g.fillStyle = C.fg; for (let i = 0; i < 4; i++) g.fillRect(560 + i * 11, 58 - i * 6, 8, 8 + i * 6);
  rr(g, 612, 38, 46, 24, 6); g.strokeStyle = C.fg; g.lineWidth = 2; g.stroke(); g.fillRect(616, 42, 34, 16);
}

export function makePhone() {
  const group = new THREE.Group();
  const body = new THREE.Mesh(new RoundedBoxGeometry(1.06, 2.2, 0.1, 6, 0.13), new THREE.MeshStandardMaterial({ color: "#1b1c20", metalness: 0.85, roughness: 0.3 }));
  const frame = new THREE.Mesh(new RoundedBoxGeometry(1.085, 2.225, 0.085, 6, 0.14), new THREE.MeshStandardMaterial({ color: "#b8a27a", metalness: 1, roughness: 0.25 }));
  const canvas = document.createElement("canvas"); canvas.width = W; canvas.height = H; const g = canvas.getContext("2d");
  const page = document.createElement("canvas"); page.width = W; page.height = 2700; const pg = page.getContext("2d");
  const tex = new THREE.CanvasTexture(canvas); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.985, 0.985 * H / W), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false }));
  screen.position.z = 0.052;
  const back = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 1.9), new THREE.MeshStandardMaterial({ color: "#2a2b30", metalness: 0.6, roughness: 0.45 })); back.position.z = -0.052; back.rotation.y = Math.PI;
  const logo = new THREE.Mesh(new THREE.CircleGeometry(0.09, 40), new THREE.MeshStandardMaterial({ color: "#dbb568", metalness: 1, roughness: 0.2 })); logo.position.set(0, 0.25, -0.054); logo.rotation.y = Math.PI;
  for (const m of [frame, body, screen, back, logo]) { group.add(m); m.material.transparent = true; m.material.depthTest = false; }
  frame.renderOrder = 20; body.renderOrder = 21; back.renderOrder = 22; logo.renderOrder = 23; screen.renderOrder = 23;
  let lastKey = ""; let anchors = {};
  function draw(st) {
    const key = JSON.stringify(st); if (key === lastKey) return anchors; lastKey = key;
    let res;
    if (st.screen === "saved") res = drawSaved(g, st);
    else if (st.screen === "form") res = drawForm(g, st);
    else if (st.screen === "week") res = drawWeek(g, st);
    else {
      const r = drawToday(pg, st, page.height); res = r;
      const maxScroll = Math.max(0, r.end - H + 40); const sc = Math.min(maxScroll, st.scroll === "end" ? maxScroll : st.scroll ?? 0);
      g.drawImage(page, 0, sc, W, H, 0, 0, W, H);
      const A = {}; for (const [k, v] of Object.entries(r.A)) A[k] = Array.isArray(v) && typeof v[0] === "number" ? [v[0], v[1] - sc, ...v.slice(2).map((q, i) => (i % 2 ? q - sc : q))] : v;
      if (r.A.seg) A.seg = r.A.seg.map((s) => [s[0], s[1] - sc, s[2], s[3] - sc]);
      if (r.A.rate) { A.rate = {}; for (const [k, v] of Object.entries(r.A.rate)) A.rate[k] = [v[0], v[1] - sc]; }
      res = { A };
    }
    g.fillStyle = "rgba(7,18,32,0.92)"; g.fillRect(0, 0, W, 96); statusBar(g);
    if (st.tap) { const [x, y, age] = st.tap; const k = Math.min(1, age / 0.45); g.fillStyle = `rgba(255,255,255,${0.42 * (1 - k)})`; g.beginPath(); g.arc(x, y, 26 + 70 * k, 0, 7); g.fill(); g.fillStyle = `rgba(255,255,255,${0.55 * (1 - k)})`; g.beginPath(); g.arc(x, y, 22, 0, 7); g.fill(); }
    if (st.toast) { const [txt, a] = st.toast; g.globalAlpha = a; rr(g, 60, 1340, W - 120, 96, 48); g.fillStyle = C.gold; g.fill(); g.fillStyle = C.pfg; g.font = F(700, 30); g.textAlign = "center"; g.fillText(txt, W / 2, 1400); g.textAlign = "left"; g.globalAlpha = 1; }
    tex.needsUpdate = true; anchors = res.A; return anchors;
  }
  function setOpacity(o) { for (const m of [frame, body, screen, back, logo]) m.material.opacity = o; }
  // precompute anchors without displaying
  let aKey = "", aCache = {};
  function anchorsFor(st) { const k = JSON.stringify(st); if (k === aKey) return aCache; const a = draw(st); aKey = k; aCache = a; return a; }
  return { group, draw, setOpacity, anchorsFor, W, H };
}
