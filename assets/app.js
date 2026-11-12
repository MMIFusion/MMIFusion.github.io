/* MMIFusion: progressive enhancement. Article links work without JavaScript. */
(() => {
  'use strict';
  const $ = (selector) => document.querySelector(selector);
  const menu = $('.menu-toggle');
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? '关闭导航' : '打开导航');
    $('#primary-nav').classList.toggle('open', open);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
      menu.click();
      menu.focus({preventScroll:true});
    }
  });
  document.addEventListener('pointerdown', event => {
    if (menu?.getAttribute('aria-expanded') === 'true' && !event.target.closest('.site-header')) menu.click();
  });
  let toastTimer;
  const toast = (message) => {
    (document.querySelector('dialog[open]') || document.body).append($('#toast'));
    $('#toast').textContent = message;
    $('#toast').classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 2800);
  };
  // One live region and timer across features, including modal dialogs.
  window.MMIFusionUI = {notify: toast};
  document.querySelectorAll('dialog').forEach(dialog => dialog.addEventListener('close', () => {
    if (dialog.contains($('#toast'))) {
      clearTimeout(toastTimer);
      $('#toast').classList.remove('visible');
      document.body.append($('#toast'));
    }
  }));
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const text = button.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        toast(`已复制：${text}`);
      } catch {
        // Keep the exact value accessible when clipboard permission is unavailable.
        window.prompt('请复制以下内容：', text);
      }
    });
  });

  const qrDialog = $('#wechat-dialog');
  if (qrDialog && typeof qrDialog.showModal === 'function') {
    let qrOpener;
    const closeQR = () => qrDialog.close();
    document.querySelectorAll('[data-qr-open]').forEach(link => {
      link.setAttribute('aria-haspopup', 'dialog');
      link.setAttribute('aria-controls', 'wechat-dialog');
      link.addEventListener('click', event => {
        // Keep normal link behavior for opening in another tab or without JS.
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        qrOpener = link;
        if (menu?.getAttribute('aria-expanded') === 'true') menu.click();
        qrDialog.showModal();
        document.documentElement.classList.add('qr-modal-open');
      });
    });
    qrDialog.querySelector('[data-qr-close]').addEventListener('click', closeQR);
    qrDialog.addEventListener('close', () => {
      document.documentElement.classList.remove('qr-modal-open');
      if (qrOpener?.getClientRects().length) qrOpener.focus({preventScroll:true});
      else menu?.focus({preventScroll:true});
    });
    qrDialog.addEventListener('click', event => {
      if (event.target !== qrDialog) return;
      const bounds = qrDialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) closeQR();
    });
  }

  const bookmarkKey = 'mmifusion-bookmarks-v1';
  let saved;
  try { const raw = JSON.parse(localStorage.getItem(bookmarkKey) || '[]'); saved = new Set(Array.isArray(raw) ? raw.filter(id => typeof id === 'string') : []); } catch { saved = new Set(); }
  const bookmarkButtons = [...document.querySelectorAll('[data-bookmark]')];
  const syncBookmarks = () => bookmarkButtons.forEach(button => {
    const active = saved.has(button.dataset.bookmark);
    button.setAttribute('aria-pressed', String(active));
    button.setAttribute('aria-label', active ? '取消收藏文章' : '收藏文章');
    button.innerHTML = active ? '★<span>已收藏</span>' : '☆<span>收藏</span>';
  });
  let onBookmarkChange = () => {};
  bookmarkButtons.forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.bookmark;
    if (saved.has(id)) saved.delete(id); else saved.add(id);
    try { localStorage.setItem(bookmarkKey, JSON.stringify([...saved])); }
    catch { toast('浏览器无法保存收藏，本次打开期间仍然可用'); }
    syncBookmarks(); onBookmarkChange();
  }));
  addEventListener('storage', event => {
    if (event.key === bookmarkKey) {
      try { const value = JSON.parse(event.newValue || '[]'); saved = new Set(Array.isArray(value) ? value.filter(id => typeof id === 'string') : []); syncBookmarks(); onBookmarkChange(); } catch { /* Keep last valid selection. */ }
    }
  });
  syncBookmarks();

  const collection = $('.collection');
  if (!collection) return;
  const rows = [...collection.querySelectorAll('[data-article-id]')];
  rows.forEach(row => {
    const wrap = row.querySelector('.article-stat-wrap');
    if (!wrap) return;
    const button = wrap.querySelector('.article-stat-toggle');
    button?.addEventListener('click', () => {
      const open = wrap.classList.toggle('stats-open');
      button.setAttribute('aria-expanded', String(open));
    });
    wrap.addEventListener('keydown', event => {
      if (event.key !== 'Escape') return;
      wrap.classList.add('stats-dismissed');
      wrap.classList.remove('stats-open');
      button?.setAttribute('aria-expanded', 'false');
    });
    wrap.querySelector('.article-title-link')?.addEventListener('mouseleave', () => wrap.classList.remove('stats-dismissed'));
    wrap.addEventListener('focusout', event => {
      if (!wrap.contains(event.relatedTarget)) wrap.classList.remove('stats-dismissed');
    });
  });
  const search = $('#article-search');
  const topic = $('#topic-filter');
  const venue = $('#venue-filter');
  const sort = $('#sort-order');
  const savedOnly = $('#saved-only');
  const buttons = [...collection.querySelectorAll('[data-section]')];
  let records, state, filtered;
  const pageSize = Number(collection.dataset.pageSize);
  const norm = (text) => String(text).normalize('NFKC').toLocaleLowerCase().replace(/\s+/g, ' ').trim();

  const loadState = () => {
    const params = new URLSearchParams(location.search);
    const validSection = buttons.some(button => button.dataset.section === params.get('section'));
    const validOption = (select, value) => select && [...select.options].some(option => option.value === value);
    return {
      query: params.get('q') || '',
      saved: params.get('saved') === '1',
      section: validSection ? params.get('section') : '',
      topic: validOption(topic, params.get('topic')) ? params.get('topic') : '',
      venue: validOption(venue, params.get('venue')) ? params.get('venue') : '',
      sort: params.get('sort') === 'oldest' ? 'oldest' : 'newest',
      page: Math.max(1, Number.parseInt(params.get('page'), 10) || 1),
    };
  };
  const syncControls = () => {
    if (search) search.value = state.query;
    if (savedOnly) savedOnly.checked = state.saved;
    if (topic) topic.value = state.topic;
    if (venue) venue.value = state.venue;
    if (sort) sort.value = state.sort;
    buttons.forEach(button => {
      const active = button.dataset.section === state.section;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
  };
  const saveState = () => {
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries({q:state.query,section:state.section,topic:state.topic,venue:state.venue})) {
      if (value) params.set(key, value);
    }
    if (state.saved) params.set('saved', '1');
    if (state.sort !== 'newest') params.set('sort', state.sort);
    if (state.page > 1) params.set('page', String(state.page));
    const suffix = params.toString();
    history.replaceState(null, '', location.pathname + (suffix ? `?${suffix}` : '') + location.hash);
  };
  const render = (updateURL = true) => {
    const terms = norm(state.query).split(' ').filter(Boolean);
    filtered = records.filter(({article, searchable}) =>
      (!state.saved || saved.has(article.id)) &&
      (!state.section || article.section === state.section) &&
      (!state.topic || article.topics.includes(state.topic)) &&
      (!state.venue || article.venue === state.venue) &&
      terms.every(term => searchable.includes(term))
    ).sort((a, b) => state.sort === 'oldest' ? a.article.date.localeCompare(b.article.date) : b.article.date.localeCompare(a.article.date));
    const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
    state.page = Math.min(state.page, totalPages);
    rows.forEach(row => { row.hidden = true; });
    const selected = filtered.slice((state.page - 1) * pageSize, state.page * pageSize);
    selected.forEach(({node}) => { node.hidden = false; $('#article-list').append(node); });
    $('#empty-results').hidden = filtered.length > 0;
    $('#empty-results h3').textContent = state.saved ? '当前筛选下暂无收藏' : '没有找到匹配的文章';
    $('#empty-results p').textContent = state.saved ? '点击文章旁的星标收藏，或清除其他筛选条件。收藏保存在当前浏览器。' : '试试方法名、研究方向，或缩短关键词。';
    $('#result-count').textContent = `共 ${filtered.length} 篇文章`;
    $('#pagination').hidden = filtered.length <= pageSize;
    $('#page-info').textContent = `${state.page} / ${totalPages}`;
    $('#prev-page').disabled = state.page === 1;
    $('#next-page').disabled = state.page === totalPages;
    syncControls();
    if (updateURL) saveState();
  };
  const reset = () => {
    state = {query:'',section:'',topic:'',venue:'',sort:'newest',page:1,saved:false};
    render();
  };
  fetch('data/articles.json').then(response => {
    if (!response.ok) throw new Error('Article data unavailable');
    return response.json();
  }).then(data => {
    const byId = new Map(data.articles.map(article => [article.id, article]));
    records = rows.map(node => {
      const article = byId.get(node.dataset.articleId);
      if (!article) throw new Error('Article index mismatch');
      return {node,article,searchable:norm([article.title,article.section,article.venue,...article.topics].join(' '))};
    });
    state = loadState();
    render();
    onBookmarkChange = () => render();
    savedOnly?.addEventListener('change', () => { state.saved = savedOnly.checked; state.page = 1; render(); });
    search?.addEventListener('input', () => { state.query = search.value; state.page = 1; render(); });
    topic?.addEventListener('change', () => { state.topic = topic.value; state.page = 1; render(); });
    venue?.addEventListener('change', () => { state.venue = venue.value; state.page = 1; render(); });
    sort?.addEventListener('change', () => { state.sort = sort.value; state.page = 1; render(); });
    buttons.forEach(button => button.addEventListener('click', () => { state.section = button.dataset.section; state.page = 1; render(); }));
    $('#reset-filters')?.addEventListener('click', reset);
    $('[data-reset]')?.addEventListener('click', reset);
    for (const [id, step] of [['prev-page', -1], ['next-page', 1]]) {
      $(`#${id}`).addEventListener('click', () => {
        state.page += step;
        render();
        $('.result-summary').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});
      });
    }
    addEventListener('popstate', () => { state = loadState(); render(false); });
    document.addEventListener('keydown', (event) => {
      if (event.key === '/' && !event.metaKey && !event.ctrlKey && !event.altKey && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName) && !document.activeElement?.isContentEditable) {
        event.preventDefault();
        search?.focus();
      }
    });
  }).catch(() => {
    // The server-rendered complete article archive remains readable.
    $('.collection-controls')?.setAttribute('hidden', '');
    $('#result-count').textContent = `共 ${rows.length} 篇文章 · 完整目录模式`;
    const message = document.createElement('p');
    message.className = 'small-note';
    message.textContent = '搜索暂时不可用，仍可浏览下方完整目录并点击阅读。刷新页面可重试。';
    $('.result-summary').after(message);
  });
})();
