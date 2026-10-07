// node render.mjs frames out%d.png t1,t2   |   node render.mjs video out.mp4 [start end]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import http from 'http'; import fs from 'fs'; import path from 'path'; import { spawn } from 'child_process';
const [mode, outPath, arg3, arg4] = process.argv.slice(2);
const root = path.resolve('.');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.hdr': 'application/octet-stream' };
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0);
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', e => console.error('PAGEERR', e.message)); p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.error('console', m.text().slice(0, 200)); });
await p.goto(`http://localhost:${srv.address().port}/scene.html`);
await p.waitForFunction(() => window.ready === true, null, { timeout: 180000 });
await p.waitForTimeout(300);
const t0 = Date.now();
if (mode === 'frames') {
  for (const [i, t] of arg3.split(',').entries()) { await p.evaluate(t => seek(t), +t); await p.screenshot({ path: outPath.replace('%d', i) }); }
} else {
  const FPS = 30, a = +(arg3 || 0), z = +(arg4 || 20);
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', outPath], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = Math.round(a * FPS); i < Math.round(z * FPS); i++) {
    await p.evaluate(t => seek(t), i / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 94 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 30 === 0) console.log('frame', i, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
console.log('done in', ((Date.now() - t0) / 1000).toFixed(1), 's');
await b.close(); srv.close();
