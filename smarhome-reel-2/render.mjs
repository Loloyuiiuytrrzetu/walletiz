// node render.mjs <fmt> frames <out pattern with %d> t1,t2,...  |  node render.mjs <fmt> video <out.mp4>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import http from 'http'; import fs from 'fs'; import path from 'path'; import { spawn } from 'child_process';
const [fmt, mode, outPath, times] = process.argv.slice(2);
const root = '/home/user/walletiz';
const types = { '.html':'text/html', '.css':'text/css', '.png':'image/png', '.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.woff2':'font/woff2' };
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); }); }).listen(0);
const port = srv.address().port;
const W = { '916':1080, '11':1080, '169':1920 }[fmt], H = { '916':1920, '11':1080, '169':1080 }[fmt];
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
p.on('pageerror', e => console.error('PAGEERR', e.message));
p.on('requestfailed', r => console.error('REQFAIL', r.url()));
p.on('response', r => { if (r.status() >= 400) console.error('HTTP', r.status(), r.url()); });
await p.goto(`http://localhost:${port}/smarhome-reel-2/ad.html?f=${fmt}`); await p.evaluate(() => window.ready);
if (mode === 'frames') {
  for (const [i, t] of times.split(',').entries()) { await p.evaluate(t => seek(t), +t); await p.waitForTimeout(40); await p.screenshot({ path: outPath.replace('%d', String(i).padStart(2,'0')) }); }
} else {
  const FPS = 30, N = 20 * FPS;
  const ff = spawn('ffmpeg', ['-loglevel','error','-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p',outPath], { stdio: ['pipe','inherit','inherit'] });
  for (let i = 0; i < N; i++) {
    await p.evaluate(t => seek(t), i / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 94 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) process.stdout.write(`${fmt} ${i}/${N}\n`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await b.close(); srv.close();
