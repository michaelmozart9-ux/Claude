// node render.mjs <video> test 0.3 2 4 ...   |   node render.mjs <video> full   (env START, END, STEP, PORT)
import { createRequire } from "module"; const require = createRequire(import.meta.url); const { chromium } = require("playwright");
import fs from "fs";
const [, , name, mode, ...rest] = process.argv;
const PORT = process.env.PORT || 8765;
const dir = `videos/${name}`;
const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--disable-gpu-vsync"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on("pageerror", (e) => console.error("PAGEERROR", e.message));
page.on("console", (m) => { if (m.type() === "error") console.error("CONSOLE", m.text()); });
await page.goto(`http://localhost:${PORT}/index.html?v=${name}`);
await page.waitForFunction(() => window.__ready !== undefined, null, { timeout: 120000 });
await page.evaluate(() => window.__ready);
const cdp = await page.context().newCDPSession(page);
async function shot(t, file) {
  await page.evaluate((tt) => window.render(tt), t);
  const { data } = await cdp.send("Page.captureScreenshot", { format: "jpeg", quality: 92, optimizeForSpeed: true });
  fs.writeFileSync(file, Buffer.from(data, "base64"));
}
if (mode === "test") {
  fs.mkdirSync(`${dir}/test`, { recursive: true });
  for (const f of fs.readdirSync(`${dir}/test`)) fs.unlinkSync(`${dir}/test/${f}`);
  for (const s of rest) { const t = parseFloat(s); await shot(t, `${dir}/test/t_${t.toFixed(2).padStart(6, "0")}.jpg`); }
  console.log("test frames:", rest.length);
} else {
  const dur = await page.evaluate(() => window.__DUR); const fps = await page.evaluate(() => window.__FPS);
  const N = Math.round(dur * fps); const start = +(process.env.START || 0), end = +(process.env.END || N), step = +(process.env.STEP || 1);
  fs.mkdirSync(`${dir}/frames`, { recursive: true });
  const t0 = Date.now();
  for (let f = start; f < end; f += step) {
    await shot(f / fps, `${dir}/frames/${String(f).padStart(4, "0")}.jpg`);
    if (f % 150 === 0) console.log(`${name} frame ${f}/${N} ${((Date.now() - t0) / 1000 / Math.max(1, (f - start) / step + 1)).toFixed(2)}s/f`);
  }
  console.log(`${name} done ${N} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
await browser.close();
