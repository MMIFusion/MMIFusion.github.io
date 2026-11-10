/* Original implementation. Input: 8-bit RGBA, transparent pixels over white. */
(function (root) {
  'use strict';
  function evaluate(rgba, width, height) {
    if (!Number.isInteger(width) || !Number.isInteger(height) || width < 1 || height < 1 || rgba.length !== width * height * 4) throw new Error('Invalid image dimensions');
    const n = width * height, gray = new Uint8Array(n), hist = new Uint32Array(256);
    let sum = 0, squares = 0, dx = 0, dy = 0;
    for (let i = 0; i < n; i++) {
      const j = i * 4, alpha = rgba[j + 3] / 255;
      const value = Math.floor(0.299 * (rgba[j] * alpha + 255 * (1 - alpha)) + 0.587 * (rgba[j + 1] * alpha + 255 * (1 - alpha)) + 0.114 * (rgba[j + 2] * alpha + 255 * (1 - alpha)) + 0.5);
      gray[i] = value; hist[value]++; sum += value; squares += value * value;
      if (i % width) dx += (value - gray[i - 1]) ** 2;
      if (i >= width) dy += (value - gray[i - width]) ** 2;
    }
    let en = 0;
    for (const count of hist) if (count) { const p = count / n; en -= p * Math.log2(p); }
    return {en, sd: Math.sqrt(Math.max(0, squares / n - (sum / n) ** 2)), sf: Math.sqrt((width > 1 ? dx / (height * (width - 1)) : 0) + (height > 1 ? dy / (width * (height - 1)) : 0))};
  }
  root.FusionMetrics = {evaluate};
  if (typeof module === 'object' && module.exports) module.exports = {evaluate};
})(typeof window === 'object' ? window : globalThis);
