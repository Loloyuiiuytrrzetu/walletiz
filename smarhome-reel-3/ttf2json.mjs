import opentype from 'opentype.js';
import fs from 'fs';
const font = opentype.parse(fs.readFileSync('ArchivoBlack.ttf').buffer.slice(0));
const round = x => Math.round(x * 100) / 100;
const scale = (100000) / ((font.unitsPerEm || 2048) * 72);
const glyphs = {};
const chars = "ROSÄNMAÄabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ²·.,!?'’-éèàêç&ÉÀ€%m";
for (const ch of new Set(chars)) {
  const g = font.charToGlyph(ch); if (!g) continue;
  const token = { ha: round(g.advanceWidth * scale), x_min: round((g.xMin || 0) * scale), x_max: round((g.xMax || 0) * scale), o: '' };
  for (const c of g.path.commands) {
    if (c.type.toLowerCase() === 'c') c.type = 'b';
    token.o += c.type.toLowerCase() + ' ';
    if (c.x !== undefined && c.y !== undefined) token.o += round(c.x * scale) + ' ' + round(c.y * scale) + ' ';
    if (c.x1 !== undefined && c.y1 !== undefined) token.o += round(c.x1 * scale) + ' ' + round(c.y1 * scale) + ' ';
    if (c.x2 !== undefined && c.y2 !== undefined) token.o += round(c.x2 * scale) + ' ' + round(c.y2 * scale) + ' ';
  }
  glyphs[ch] = token;
}
const out = { glyphs, familyName: font.getEnglishName('fullName'), ascender: round(font.ascender * scale), descender: round(font.descender * scale),
  underlinePosition: font.tables.post.underlinePosition, underlineThickness: font.tables.post.underlineThickness,
  boundingBox: { xMin: font.tables.head.xMin, xMax: font.tables.head.xMax, yMin: font.tables.head.yMin, yMax: font.tables.head.yMax },
  resolution: 1000, original_font_information: font.tables.name };
fs.writeFileSync('archivo.typeface.json', JSON.stringify(out));
console.log(Object.keys(glyphs).length);
