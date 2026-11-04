// node render2.mjs <videoDir> test t1 t2 ...  |  node render2.mjs <videoDir> full   (env START/END)
import { chromium } from "playwright";
import fs from "node:fs";
const [dir, mode, ...rest] = process.argv.slice(2);
const timing = JSON.parse(fs.readFileSync(`${dir}/timing.json`, "utf8"));
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium", args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
const errs = []; p.on("pageerror", (e) => errs.push(e.message)); p.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
await p.addInitScript(`window.__TIMING__ = ${JSON.stringify(timing)};`);
await p.goto(`http://127.0.0.1:8765/engine/index.html`);
await p.waitForFunction(() => window.__ready, null, { timeout: 120000 }); await p.evaluate(() => window.__ready);
const st = await p.$("#stage");
const shot = async (t, path, type) => { await p.evaluate((t) => window.render(t), t); await st.screenshot(type === "jpeg" ? { path, type: "jpeg", quality: 92 } : { path }); };
if (mode === "test") { for (const t of rest.map(Number)) await shot(t, `${dir}/test-${t}.jpg`, "jpeg"); }
else {
  fs.mkdirSync(`${dir}/frames`, { recursive: true }); const n = Math.ceil(timing.duration * timing.fps), i0 = +(process.env.START || 0), i1 = Math.min(n, +(process.env.END || n));
  for (let i = i0; i < i1; i++) await shot(i / timing.fps, `${dir}/frames/${String(i).padStart(4, "0")}.jpg`, "jpeg");
}
if (errs.length) console.log("errors", JSON.stringify(errs.slice(0, 5)));
await b.close();
