/* Browser-only tools: directories, calendar, image statistics, contribution drafts. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const norm = s => String(s).normalize('NFKC').toLowerCase().trim();
  const notify = message => { const el = $('#toast'); el.textContent = message; el.classList.add('visible'); setTimeout(() => el.classList.remove('visible'), 3000); };
  const copy = async text => { try { await navigator.clipboard.writeText(text); notify('已复制'); } catch { window.prompt('请复制以下内容：', text); } };
  $$('[data-copy-link]').forEach(el => el.addEventListener('click', () => copy(new URL(el.dataset.copyLink, location.href).href)));

  $$('[data-directory]').forEach(directory => {
    const cards = [...directory.querySelectorAll('[data-directory-card]')];
    const search = directory.querySelector('[data-card-search]');
    const selects = [...directory.querySelectorAll('[data-card-filter]')];
    const params = new URLSearchParams(location.search);
    search.value = params.get('q') || '';
    selects.forEach(select => { const value = params.get(select.dataset.cardFilter); if ([...select.options].some(o => o.value === value)) select.value = value; });
    const render = (save = true) => {
      const terms = norm(search.value).split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(card => {
        const show = terms.every(t => norm(card.dataset.search).includes(t)) && selects.every(s => !s.value || JSON.parse(card.dataset[s.dataset.cardFilter]).includes(s.value));
        card.hidden = !show; if (show) count++;
      });
      directory.querySelector('.directory-count').textContent = `显示 ${count} / ${cards.length} 项`;
      directory.querySelector('.directory-empty').hidden = count > 0;
      if (save) {
        const query = new URLSearchParams();
        if (search.value) query.set('q', search.value);
        selects.forEach(s => { if (s.value) query.set(s.dataset.cardFilter, s.value); });
        history.replaceState(null, '', location.pathname + (query.size ? '?' + query : '') + location.hash);
      }
    };
    search.addEventListener('input', () => render());
    selects.forEach(s => s.addEventListener('change', () => render()));
    directory.querySelectorAll('[data-card-reset]').forEach(b => b.addEventListener('click', () => { search.value = ''; selects.forEach(s => s.value = ''); render(); }));
    render(false);
  });

  const countdown = () => $$('[data-countdown]').forEach(el => {
    const delta = new Date(el.dataset.countdown).getTime() - Date.now();
    if (delta <= 0) { el.textContent = '已截止'; el.classList.add('expired'); return; }
    const minutes = Math.floor(delta / 60000), hours = Math.floor(minutes / 60), days = Math.floor(hours / 24);
    el.textContent = `${days} 天 ${hours % 24} 时 ${minutes % 60} 分`;
  });
  countdown(); if ($('[data-countdown]')) setInterval(countdown, 30000);
  const timezone = $('#calendar-timezone');
  if (timezone) {
    const renderTimes = () => $$('[data-local-time]').forEach(el => {
      const zone = timezone.value === 'local' ? Intl.DateTimeFormat().resolvedOptions().timeZone : timezone.value;
      const parts = new Intl.DateTimeFormat('zh-CN', {timeZone:zone, year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit', hourCycle:'h23'}).format(new Date(el.dataset.localTime));
      el.dateTime = el.dataset.localTime; el.textContent = parts + ' · ' + zone;
    });
    timezone.addEventListener('change', renderTimes); renderTimes();
  }

  const compare = $$('[data-compare]');
  if (compare.length) {
    const dialog = $('#compare-dialog'), selected = () => compare.filter(c => c.checked);
    compare.forEach(c => c.addEventListener('change', () => {
      $('#compare-open').disabled = selected().length < 2;
      $('#compare-count').textContent = selected().length ? `已选择 ${selected().length} 项 · 可对比 2–3 项` : '选择 2–3 个会议期刊进行对比';
    }));
    $('#compare-open').addEventListener('click', () => {
      const container = $('#compare-content'); container.replaceChildren();
      selected().forEach(c => {
        const original = c.closest('.venue-card'), clone = original.cloneNode(true);
        clone.hidden = false; clone.removeAttribute('data-directory-card'); clone.querySelector('.compare-check').remove();
        container.append(clone);
      });
      dialog.showModal();
    });
    dialog.querySelector('[data-close-dialog]').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
  }

  const lab = $('#metric-lab');
  if (lab) {
    const canvas = $('#metric-canvas'), ctx = canvas.getContext('2d', {willReadFrequently:true});
    const message = $('#metric-message'), exporter = $('#metric-export');
    let latest, sequence = 0;
    const calculate = name => {
      latest = {name, width:canvas.width, height:canvas.height, ...window.FusionMetrics.evaluate(ctx.getImageData(0, 0, canvas.width, canvas.height).data, canvas.width, canvas.height)};
      ['en', 'sd', 'sf'].forEach(k => $('#metric-' + k).textContent = latest[k].toFixed(4));
      $('#metric-image-info').textContent = `${name} · ${canvas.width} × ${canvas.height} px`;
      exporter.disabled = false; message.textContent = '已完成 · 结果仅描述本图的统计特性';
    };
    const sample = kind => {
      sequence++; canvas.width = 256; canvas.height = 192;
      const frame = ctx.createImageData(256, 192);
      for (let y = 0; y < 192; y++) for (let x = 0; x < 256; x++) {
        const i = (y * 256 + x) * 4;
        const value = kind === 'flat' ? 128 : kind === 'checker' ? ((Math.floor(x / 16) + Math.floor(y / 16)) % 2) * 255 : x;
        frame.data[i] = frame.data[i+1] = frame.data[i+2] = value; frame.data[i+3] = 255;
      }
      ctx.putImageData(frame, 0, 0); calculate({flat:'纯灰示例', checker:'棋盘示例', gradient:'渐变示例'}[kind]);
      $$('[data-metric-sample]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.metricSample === kind)));
      $('#metric-file').value = '';
    };
    $$('[data-metric-sample]').forEach(b => b.addEventListener('click', () => sample(b.dataset.metricSample)));
    $('#metric-file').addEventListener('change', async event => {
      const file = event.target.files[0]; if (!file) return;
      const token = ++sequence;
      if (file.size > 20 * 1024 * 1024 || !/^image\/(png|jpeg|webp|bmp|x-ms-bmp)$/.test(file.type)) { message.textContent = '请选择不超过 20 MB 的 PNG、JPEG、WebP 或 BMP 图片；当前结果未改变。'; return; }
      const url = URL.createObjectURL(file), img = new Image(); message.textContent = '正在本地读取图片…';
      try {
        img.src = url; await img.decode(); if (token !== sequence) return;
        if (img.naturalWidth * img.naturalHeight > 16000000) throw new Error('图片超过 1600 万像素，请裁剪后重试');
        canvas.width = img.naturalWidth; canvas.height = img.naturalHeight; ctx.drawImage(img, 0, 0);
        calculate(file.name); $$('[data-metric-sample]').forEach(b => b.setAttribute('aria-pressed', 'false'));
      } catch (error) { if (token === sequence) message.textContent = (error.message.startsWith('图片超过') ? error.message : '无法解码这张图片，请换一张图片重试') + '；当前结果未改变。'; }
      finally { URL.revokeObjectURL(url); }
    });
    exporter.addEventListener('click', () => {
      if (!latest) return;
      // Guard spreadsheet formula interpretation when a filename begins with an operator.
      const safeName = /^[=+@\-\t\r\n]/.test(latest.name) ? "'" + latest.name : latest.name;
      const cell = value => '"' + String(value).replaceAll('"', '""') + '"';
      const csv = '\uFEFF' + ['image,width,height,EN_bits,SD,SF', [safeName, latest.width, latest.height, latest.en, latest.sd, latest.sf].map(cell).join(',')].join('\r\n');
      const url = URL.createObjectURL(new Blob([csv], {type:'text/csv;charset=utf-8'}));
      const a = document.createElement('a'); a.href = url; a.download = 'mmifusion-metrics.csv'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
    sample('gradient');
  }

  const form = $('#contribution-form');
  if (form) {
    const type = form.elements.type, initial = new URLSearchParams(location.search).get('type');
    if ([...type.options].some(o => o.value === initial)) type.value = initial;
    const source = form.elements.source;
    source.addEventListener('input', () => source.setCustomValidity(''));
    form.addEventListener('input', () => {
      $('#submission-actions').hidden = true;
      $('#submission-help').textContent = '内容已修改，请重新生成投稿预览。';
    });
    form.addEventListener('submit', event => {
      event.preventDefault();
      let url; try { url = new URL(source.value); } catch { return; }
      if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password) { source.setCustomValidity('请输入不含账号密码的 http 或 https 官方链接'); source.reportValidity(); return; }
      const title = form.elements.title.value.trim(), description = form.elements.description.value.trim();
      if (!title || !description) { notify('请填写名称与简介'); return; }
      const text = `资源类型：${type.value}\n名称：${title}\n官方来源：${url.href}\n\n简介与补充信息：\n${description}\n\n通过多模态信息融合主站整理`;
      $('#submission-text').value = text; $('#submission-text').hidden = false; $('#submission-actions').hidden = false;
      $('#submission-help').textContent = '草稿已生成。请检查来源与内容，再复制或继续提交。';
      $('#submission-github').href = 'https://github.com/MMIFusion/MMIFusion.github.io/issues/new?' + new URLSearchParams({title:`[${type.value}] ${title}`, body:text});
    });
    $('#submission-copy').addEventListener('click', () => copy($('#submission-text').value));
  }
})();
