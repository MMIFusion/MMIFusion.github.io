/* Browser-only tools: directories, calendar, image statistics, contribution drafts. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const norm = s => String(s).normalize('NFKC').toLowerCase().trim();
  const notify = message => window.MMIFusionUI.notify(message);
  const copy = async text => { try { await navigator.clipboard.writeText(text); notify('已复制'); } catch { window.prompt('请复制以下内容：', text); } };
  $$('[data-copy-link]').forEach(el => el.addEventListener('click', () => copy(new URL(el.dataset.copyLink, location.href).href)));

  const upcoming = $('#calendar-upcoming'), refreshDirectories = [];
  if (upcoming) upcoming.checked = new URLSearchParams(location.search).get('upcoming') === '1';
  const calendarEvents = $$('[data-calendar-event]').map(node => ({node,event:JSON.parse(node.dataset.calendarEvent)}));
  const refreshEvents = () => {
    const now = new Date();
    calendarEvents.forEach(record => {
      record.status = window.MMIFusionCalendar.status(record.event,now);
      const {node,event,status} = record;
      node.classList.toggle('event-ended',status.ended);
      node.classList.toggle('event-imminent',status.imminent);
      if (node.classList.contains('event-row')) node.hidden = !!upcoming?.checked && status.ended;
      const counter = node.querySelector('[data-countdown]');
      if (counter) {
        const minutes = Math.floor(Math.max(0,status.remaining) / 60000), hours = Math.floor(minutes / 60);
        counter.textContent = status.ended ? '已截止' : minutes === 0 ? '不足 1 分钟' : `${Math.floor(hours / 24)} 天 ${hours % 24} 时 ${minutes % 60} 分`;
        counter.classList.toggle('expired',status.ended);
      }
      const dateLabel = node.querySelector('.date-only');
      if (dateLabel) dateLabel.textContent = status.ended ? '日期已过' : '按官方日期显示';
      const note = node.querySelector('small');
      if (note && node.classList.contains('deadline-teaser') && event.kind === 'deadline') note.textContent = status.imminent ? '72 小时内截止 · 请留足上传时间' : '距离截止 · 实时更新';
    });
    const teasers = calendarEvents.filter(({node}) => node.classList.contains('deadline-teaser'));
    const selected = teasers.filter(r => !r.status.ended).sort((a,b) => a.status.order-b.status.order).slice(0,3);
    const selectedNodes = selected.map(r => r.node);
    teasers.forEach(({node}) => {node.hidden = !selectedNodes.includes(node);});
    const displayed = $$('.deadline-teaser').filter(node => !node.hidden);
    // Avoid detaching a focused link on each timer tick when its order is unchanged.
    if (displayed.some((node,index) => node !== selectedNodes[index])) {
      selectedNodes.forEach(node => $('.deadline-strip').append(node));
    }
    if ($('.deadline-empty')) $('.deadline-empty').hidden = selected.length > 0;
  };
  refreshEvents();

  $$('[data-directory]').forEach(directory => {
    const cards = [...directory.querySelectorAll('[data-directory-card]')];
    const search = directory.querySelector('[data-card-search]');
    const selects = [...directory.querySelectorAll('[data-card-filter]')];
    const params = new URLSearchParams(location.search);
    const paginated = directory.dataset.directory === 'venues';
    const pageSize = 12;
    let page = Math.max(1, Math.floor(Number(params.get('page')) || 1));
    let initialVenueHash = paginated ? location.hash.slice(1) : '';
    search.value = params.get('q') || '';
    selects.forEach(select => { const value = params.get(select.dataset.cardFilter); if ([...select.options].some(o => o.value === value)) select.value = value; });
    const render = (save = true) => {
      const terms = norm(search.value).split(/\s+/).filter(Boolean);
      const matches = [];
      cards.forEach(card => {
        const available = !upcoming?.checked || directory.dataset.directory !== 'calendar' || card.dataset.reference === 'true' || card.dataset.pending === 'true' || [...card.querySelectorAll('.event-row')].some(row => !row.hidden);
        const show = available && terms.every(t => norm(card.dataset.search).includes(t)) && selects.every(s => !s.value || JSON.parse(card.dataset[s.dataset.cardFilter]).includes(s.value));
        card.hidden = !show; if (show) matches.push(card);
      });
      const count = matches.length;
      if (paginated) {
        const targetIndex = matches.findIndex(card => card.id === initialVenueHash);
        if (targetIndex >= 0) page = Math.floor(targetIndex / pageSize) + 1;
        initialVenueHash = '';
        const pages = Math.max(1, Math.ceil(count / pageSize));
        page = Math.min(page, pages);
        matches.forEach((card, index) => { card.hidden = index < (page - 1) * pageSize || index >= page * pageSize; });
        directory.querySelectorAll('[data-venue-pagination]').forEach(nav => {
          nav.hidden = count <= pageSize;
          nav.querySelector('[data-venue-page-label]').textContent = `第 ${page} / ${pages} 页 · 每页 ${pageSize} 项`;
          nav.querySelector('[data-venue-prev]').disabled = page <= 1;
          nav.querySelector('[data-venue-next]').disabled = page >= pages;
        });
      }
      const countLabel = directory.querySelector('.directory-count'), countText = `显示 ${count} / ${cards.length} 项`;
      if (countLabel.textContent !== countText) countLabel.textContent = countText;
      directory.querySelector('.directory-empty').hidden = count > 0;
      if (directory.dataset.directory === 'calendar') {
        const visible = calendarEvents.filter(({node}) => !node.hidden && !node.closest('.conference-card').hidden);
        const pending = cards.filter(card => !card.hidden && card.dataset.pending === 'true').length;
        const summary = `显示 ${visible.length} 个已公布节点 · ${visible.filter(r => !r.status.ended).length} 个未结束${pending ? ` · ${pending} 场待补充日程` : ''}`;
        if ($('#calendar-event-summary').textContent !== summary) $('#calendar-event-summary').textContent = summary;
      }
      if (save) {
        const query = new URLSearchParams();
        if (search.value) query.set('q', search.value);
        selects.forEach(s => { if (s.value) query.set(s.dataset.cardFilter, s.value); });
        if (upcoming?.checked) query.set('upcoming','1');
        if (paginated && page > 1) query.set('page', page);
        history.replaceState(null, '', location.pathname + (query.size ? '?' + query : '') + location.hash);
      }
    };
    search.addEventListener('input', () => {page = 1; render();});
    selects.forEach(s => s.addEventListener('change', () => {page = 1; render();}));
    directory.querySelectorAll('[data-card-reset]').forEach(b => b.addEventListener('click', () => { page = 1; search.value = ''; selects.forEach(s => s.value = ''); if (upcoming) {upcoming.checked=false;refreshEvents();} render(); }));
    if (paginated) {
      directory.querySelectorAll('[data-venue-prev], [data-venue-next]').forEach(button => button.addEventListener('click', () => {
        page += button.hasAttribute('data-venue-next') ? 1 : -1;
        render();
        const top = directory.querySelector('[data-venue-pagination]');
        top.focus({preventScroll:true});
        top.scrollIntoView({block:'start',behavior:document.documentElement.dataset.motion === 'off' ? 'instant' : 'smooth'});
      }));
    }
    if (directory.dataset.directory === 'calendar') {
      upcoming.addEventListener('change', () => {refreshEvents();render();});
      refreshDirectories.push(() => render(false));
    }
    render(false);
    if (directory.dataset.directory === 'calendar') {
      const shortcuts = [...directory.querySelectorAll('[data-conference-jump]')];
      const revealConference = (hash, scroll = true) => {
        let target;
        try { target = document.getElementById(decodeURIComponent(hash.slice(1))); } catch { return; }
        const card = target?.closest('.conference-card');
        if (!card || !directory.contains(card)) return;
        // A shortcut must still work after search, filtering or hiding ended nodes.
        if (card.hidden || target.hidden || card.querySelector('.event-row[hidden]')) {
          search.value = ''; selects.forEach(select => { select.value = ''; });
          upcoming.checked = false; refreshEvents(); render();
        }
        shortcuts.forEach(link => {
          if (link.hash === '#' + card.id) link.setAttribute('aria-current','location');
          else link.removeAttribute('aria-current');
        });
        cards.forEach(item => item.classList.toggle('conference-current',item === card));
        if (scroll) {
          card.focus({preventScroll:true});
          target.scrollIntoView({block:'start',behavior:document.documentElement.dataset.motion === 'off' ? 'instant' : 'smooth'});
        }
      };
      shortcuts.forEach(link => link.addEventListener('click', event => {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        revealConference(link.hash);
        if (location.hash !== link.hash) history.pushState(null,'',location.pathname + location.search + link.hash);
      }));
      addEventListener('hashchange', () => revealConference(location.hash));
      if (location.hash) requestAnimationFrame(() => revealConference(location.hash));
    }
  });

  const refreshCalendar = () => {refreshEvents();refreshDirectories.forEach(render => render());};
  if (calendarEvents.length) {
    setInterval(refreshCalendar,30000);
    document.addEventListener('visibilitychange', () => {if (!document.hidden) refreshCalendar();});
  }
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
    const syncCompare = () => {
      $('.comparison-bar').classList.toggle('has-selection', selected().length > 0);
      $('#compare-open').disabled = selected().length < 2;
      $('#compare-clear').disabled = selected().length === 0;
      $('#compare-count').textContent = selected().length ? `已选择 ${selected().length} 项 · 可对比 2–3 项` : '选择 2–3 个会议期刊进行对比';
      $('#compare-selection').textContent = selected().map(c => c.closest('.venue-card').querySelector('h2').textContent).join(' / ');
    };
    compare.forEach(c => c.addEventListener('change', () => {
      if (selected().length > 3) {c.checked=false;notify('一次最多对比 3 项，请先取消已选项目。');}
      syncCompare();
    }));
    $('#compare-clear').addEventListener('click', () => {compare.forEach(c => {c.checked=false;});syncCompare();});
    syncCompare();
    $('#compare-open').addEventListener('click', () => {
      const container = $('#compare-content'); container.replaceChildren();
      selected().forEach(c => {
        const original = c.closest('.venue-card'), clone = original.cloneNode(true);
        clone.hidden = false; clone.removeAttribute('id'); clone.removeAttribute('data-directory-card'); clone.querySelector('.compare-check').remove();
        container.append(clone);
      });
      dialog.showModal();
      document.documentElement.classList.add('compare-modal-open');
    });
    dialog.addEventListener('close', () => {
      document.documentElement.classList.remove('compare-modal-open');
      $('#compare-open').focus({preventScroll:true});
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
    const params = new URLSearchParams(location.search);
    const type = form.elements.type, initial = params.get('type');
    if ([...type.options].some(o => o.value === initial)) type.value = initial;
    const source = form.elements.source;
    const descriptionHint = form.elements.description.placeholder;
    const syncResourceHint = () => {
      form.elements.description.placeholder = type.value === '数据集'
        ? '请附全部论文作者（按原文顺序）、团队与机构、输入模态、任务、规模、划分、开放状态、使用许可及示例图来源。'
        : descriptionHint;
    };
    type.addEventListener('change',syncResourceHint);syncResourceHint();
    for (const key of ['title','source']) {
      if (params.has(key)) form.elements[key].value = params.get(key).slice(0,form.elements[key].maxLength);
    }
    if (initial === '内容勘误' && params.has('source')) {
      form.elements.description.placeholder = '请说明哪里有误、建议如何修改；如有新的官方说明，请一并附上链接。';
      $('#submission-help').textContent = '已带入反馈页面或原始来源，请补充需要更正的内容。';
    }
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
      const preview = $('#submission-text');
      if (matchMedia('(max-width: 900px)').matches) {
        preview.scrollIntoView({behavior:document.documentElement.dataset.motion === 'off' ? 'instant' : 'smooth',block:'center'});
      }
      preview.focus({preventScroll:true});
    });
    $('#submission-copy').addEventListener('click', () => copy($('#submission-text').value));
  }
})();
