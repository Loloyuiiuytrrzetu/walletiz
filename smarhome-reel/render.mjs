// node render.mjs <fmt> frames <out.png pattern> t1,t2,...   -> stills
// node render.mjs <fmt> video <out.mp4>                      -> 30fps silent video piped to ffmpeg
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import http from 'http'; import fs from 'fs'; import path from 'path'; import { spawn } from 'child_process';
const [fmt, mode, outPath, times] = process.argv.slice(2);
const root = path.resolve('.');
const types = { '.html': 'text/html', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.woff2': 'font/woff2' };
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0);
const port = srv.address().port;
const W = { '916': 1080, '11': 1080, '169': 1920 }[fmt], H = { '916': 1920, '11': 1080, '169': 1080 }[fmt];
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
p.on('pageerror', e => console.error('PAGEERR', e.message));
await p.goto(`http://localhost:${port}/comp.html?f=${fmt}`); await p.evaluate(() => window.ready);
if (mode === 'frames') {
  for (const [i, t] of times.split(',').entries()) { await p.evaluate(t => seek(t), +t); await p.waitForTimeout(60); await p.screenshot({ path: outPath.replace('%d', i) }); }
} else {
  const FPS = 30, N = 20 * FPS;
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', outPath], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < N; i++) {
    await p.evaluate(t => seek(t), i / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) process.stdout.write(`${fmt} ${i}/${N}\n`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await b.close(); srv.close();
