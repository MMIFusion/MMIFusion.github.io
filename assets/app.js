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
    if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') menu.click();
  });
  let toastTimer;
  const toast = (message) => {
    $('#toast').textContent = message;
    $('#toast').classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 2800);
  };
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

  const collection = $('.collection');
  if (!collection) return;
  const rows = [...collection.querySelectorAll('[data-article-id]')];
  const search = $('#article-search');
  const topic = $('#topic-filter');
  const venue = $('#venue-filter');
  const sort = $('#sort-order');
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
      section: validSection ? params.get('section') : '',
      topic: validOption(topic, params.get('topic')) ? params.get('topic') : '',
      venue: validOption(venue, params.get('venue')) ? params.get('venue') : '',
      sort: params.get('sort') === 'oldest' ? 'oldest' : 'newest',
      page: Math.max(1, Number.parseInt(params.get('page'), 10) || 1),
    };
  };
  const syncControls = () => {
    if (search) search.value = state.query;
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
    if (state.sort !== 'newest') params.set('sort', state.sort);
    if (state.page > 1) params.set('page', String(state.page));
    const suffix = params.toString();
    history.replaceState(null, '', location.pathname + (suffix ? `?${suffix}` : '') + location.hash);
  };
  const render = (updateURL = true) => {
    const terms = norm(state.query).split(' ').filter(Boolean);
    filtered = records.filter(({article, searchable}) =>
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
    $('#result-count').textContent = `共 ${filtered.length} 篇文章`;
    $('#pagination').hidden = filtered.length <= pageSize;
    $('#page-info').textContent = `${state.page} / ${totalPages}`;
    $('#prev-page').disabled = state.page === 1;
    $('#next-page').disabled = state.page === totalPages;
    syncControls();
    if (updateURL) saveState();
  };
  const reset = () => {
    state = {query:'',section:'',topic:'',venue:'',sort:'newest',page:1};
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
