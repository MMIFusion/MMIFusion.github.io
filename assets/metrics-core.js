/* Original implementation. Input: 8-bit RGBA, transparent pixels over white. */
(function (root) {
  'use strict';
  function evaluate(rgba, width, height) {
    if (!Number.isInteger(width) || !Number.isInteger(height) || width < 1 || height < 1 || rgba.length !== width * height * 4) throw new Error('Invalid image dimensions');
    const n = width * height, previousRow = new Uint8Array(width), hist = new Uint32Array(256);
    let sum = 0, squares = 0, dx = 0, dy = 0, left = 0;
    for (let i = 0; i < n; i++) {
      const j = i * 4, alpha = rgba[j + 3] / 255;
      const value = Math.floor(0.299 * (rgba[j] * alpha + 255 * (1 - alpha)) + 0.587 * (rgba[j + 1] * alpha + 255 * (1 - alpha)) + 0.114 * (rgba[j + 2] * alpha + 255 * (1 - alpha)) + 0.5);
      const column = i % width; hist[value]++; sum += value; squares += value * value;
      if (column) dx += (value - left) ** 2;
      if (i >= width) dy += (value - previousRow[column]) ** 2;
      previousRow[column] = value;
      left = value;
    }
    let en = 0;
    for (const count of hist) if (count) { const p = count / n; en -= p * Math.log2(p); }
    return {en, sd: Math.sqrt(Math.max(0, squares / n - (sum / n) ** 2)), sf: Math.sqrt((width > 1 ? dx / (height * (width - 1)) : 0) + (height > 1 ? dy / (width * (height - 1)) : 0))};
  }
  function evaluateImage(canvas, image) {
    const context = canvas.getContext('2d', {willReadFrequently:true});
    context.drawImage(image, 0, 0);
    return evaluate(context.getImageData(0, 0, canvas.width, canvas.height).data, canvas.width, canvas.height);
  }

  root.FusionMetrics = {evaluate, evaluateImage};
  if (typeof DedicatedWorkerGlobalScope !== 'undefined' && root instanceof DedicatedWorkerGlobalScope) {
    root.onmessage = ({data: image}) => {
      try {
        const surface = new OffscreenCanvas(image.width, image.height);
        root.postMessage(evaluateImage(surface, image));
      } finally {
        image.close();
      }
    };
  }
  if (typeof module === 'object' && module.exports) module.exports = {evaluate};
})(typeof window === 'object' ? window : globalThis);
