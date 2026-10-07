// Captures real Smar Home UI (smarhome.fr) as layered PNGs + layout JSON.
// Usage: node capture.mjs desktop|mobile
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const mode = process.argv[2] || 'desktop';
const cfg = mode === 'mobile' ? { viewport: { width: 430, height: 932 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true }
                              : { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 };
const out = `assets/ui/${mode}`; fs.mkdirSync(out, { recursive: true });
const L = { viewport: cfg.viewport, dpr: cfg.deviceScaleFactor };
const b = await chromium.launch();
const ctx = await b.newContext(cfg);
const p = await ctx.newPage();
const box = async (loc) => { const r = await loc.boundingBox(); return r && { x: r.x, y: r.y, w: r.width, h: r.height }; };
const shot = async (name, loc, opts = {}, pad = 0) => {
  if (!pad) { await loc.screenshot({ path: `${out}/${name}.png`, ...opts }); L[name] = await box(loc); return; }
  await loc.scrollIntoViewIfNeeded().catch(() => {});
  const r = await box(loc); const c = { x: Math.max(0, r.x - 2), y: r.y + 1, width: r.w + pad, height: r.h - 1 };
  await p.screenshot({ path: `${out}/${name}.png`, clip: c, ...opts }); L[name] = { x: c.x, y: c.y, w: c.width, h: c.height };
};
const CLEAR = `html,body,#root,main,body>div,.bg-background{background-color:transparent!important}`;
const css = (s) => p.addStyleTag({ content: s });
const settle = (ms = 1200) => p.waitForTimeout(ms);
const reveal = async () => { const h = await p.evaluate(() => document.body.scrollHeight); for (let y = 0; y < h; y += 300) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(120); } };

// ---------- HOME ----------
await p.goto('https://smarhome.fr/', { waitUntil: 'networkidle' });
await settle(3000);
await p.screenshot({ path: `${out}/hero-full.png` });
const chatBtn = p.getByRole('button', { name: 'Ouvrir le chat' });
L.chatBtn = await box(chatBtn);
// Chat: real click, real panel, real typing
await chatBtn.click(); await settle(1500);
await p.screenshot({ path: `${out}/chat-open.png` });
const panel = p.locator('text=Assistant Smar Home').locator('xpath=ancestor::div[contains(@class,"fixed") or contains(@class,"absolute")][1]');
L.chatPanel = await box(panel);
const input = p.getByPlaceholder(/Posez votre question/);
L.chatInput = await box(input);
await input.click(); await input.pressSequentially('Quels sont vos délais de livraison ?', { delay: 20 }); await settle(400);
await p.screenshot({ path: `${out}/chat-typed.png` });
L.chatSend = await box(p.locator('button[type=submit], button[aria-label*="nvoyer"]').last());
await p.goto('https://smarhome.fr/', { waitUntil: 'networkidle' }); await settle(3000);

// Transparent hero layers (real rendered text, background removed)
await css(CLEAR + ` #top>div.absolute.inset-0{visibility:hidden!important} #top>div.absolute.bottom-8{display:none!important} button[aria-label="Ouvrir le chat"]{visibility:hidden!important} header{background:transparent!important;backdrop-filter:none!important} #top .text-gradient-gold{padding-right:.14em}`);
await settle(300);
await p.screenshot({ path: `${out}/hero-text-layer.png`, omitBackground: true });
const words = p.locator('#top h1 > span');
const n = await words.count();
for (let i = 0; i < n; i++) {
  // isolate one word (others hidden) so descenders/italic overhang aren't clipped by neighbours
  await p.evaluate(i => document.querySelectorAll('#top h1 > span').forEach((s, j) => s.style.visibility = j === i ? 'visible' : 'hidden'), i);
  const r = await box(words.nth(i)); const c = { x: Math.max(0, r.x - 10), y: r.y - r.h * 0.15, width: r.w + 50, height: r.h * 1.45 };
  await p.screenshot({ path: `${out}/hero-w${i}.png`, clip: c, omitBackground: true }); L[`hero-w${i}`] = { x: c.x, y: c.y, w: c.width, h: c.height };
}
await p.evaluate(() => document.querySelectorAll('#top h1 > span').forEach(s => s.style.visibility = ''));
L.heroWords = n;
await shot('hero-eyebrow', p.locator('#top span.inline-flex').first(), { omitBackground: true });
const header = p.locator('header').first();
await shot('header', header, { omitBackground: true });
await shot('header-logo', header.getByRole('link', { name: /SMAR/ }).first(), { omitBackground: true });
const contactBtn = header.getByRole('link', { name: 'Nous contacter' });
if (await contactBtn.isVisible()) await shot('btn-contact', contactBtn, { omitBackground: true });
if (mode === 'desktop') {
  await shot('nav', header.locator('nav').first(), { omitBackground: true });
  await shot('lang', header.getByRole('button', { name: 'FR' }).locator('xpath=..'), { omitBackground: true });
}
// Remaining sections (reveal-on-scroll first)
await css(CLEAR + `header{visibility:hidden!important} .animate-marquee{animation:none!important}`);
await reveal(); await settle(800);
const adv = p.locator('#avantages .grid > div');
const na = await adv.count();
for (let i = 0; i < Math.min(na, 4); i++) { await adv.nth(i).scrollIntoViewIfNeeded(); await settle(500); await shot(`adv-${i + 1}`, adv.nth(i), { omitBackground: true }); }
const sol = p.locator('#solution .grid > div');
for (let i = 0; i < Math.min(await sol.count(), 6); i++) await shot(`sol-${i + 1}`, sol.nth(i), { omitBackground: true });
const zones = p.locator('#zones .animate-marquee > div > span:first-child');
for (let i = 0; i < 7; i++) { await zones.nth(i).scrollIntoViewIfNeeded().catch(() => {}); await shot(`zone-${i + 1}`, zones.nth(i), { omitBackground: true }, 16).catch(e => console.log('zone', i, e.message)); }
const star = p.locator('#zones .animate-marquee span.text-primary').first();
await shot('zone-star', star, { omitBackground: true });
const devis = p.getByRole('link', { name: 'Demander un devis' }).first();
await devis.scrollIntoViewIfNeeded(); await settle(600);
await shot('btn-devis', devis, { omitBackground: true });
await shot('card-rosan', devis.locator('xpath=ancestor::div[contains(@class,"rounded")][last()]'), { omitBackground: true }).catch(e => console.log('card', e.message));
const flogo = p.locator('footer img, section.border-t img').last();
await flogo.scrollIntoViewIfNeeded(); await settle(600);
await shot('footer-logo', flogo.locator('xpath=..'), { omitBackground: true });

// ---------- MODELES ----------
await p.goto('https://smarhome.fr/modeles', { waitUntil: 'networkidle' }); await settle(1500);
await css(`header{visibility:hidden!important} button[aria-label="Ouvrir le chat"]{visibility:hidden!important}`);
await reveal(); await settle(600);
const rosan = p.locator('#rosan');
await rosan.scrollIntoViewIfNeeded(); await settle(800);
const b18 = rosan.getByRole('button', { name: /^18 m² Studio/ }), b37 = rosan.getByRole('button', { name: /^37 m² T2/ });
await shot('rosan-18', rosan);
L.rosan_b18 = await box(b18); L.rosan_b37 = await box(b37);
await b37.hover(); await settle(500); await shot('rosan-37-hover', rosan);
await b37.click(); await p.mouse.move(0, 0); await settle(1500); await shot('rosan-37', rosan);
L.rosan_b37_after = await box(b37);
const planBtn = rosan.getByRole('button', { name: /^Plan / }).first();
await planBtn.scrollIntoViewIfNeeded(); await settle(600);
L.planBtn = await box(planBtn);
await p.screenshot({ path: `${out}/lb-before.png` });
await planBtn.hover(); await settle(500);
await p.screenshot({ path: `${out}/lb-hover.png` });
await planBtn.click(); await settle(1500);
await p.screenshot({ path: `${out}/lb-open.png` });
fs.writeFileSync(`${out}/layout.json`, JSON.stringify(L, null, 1));
await b.close();
console.log('done', mode);
