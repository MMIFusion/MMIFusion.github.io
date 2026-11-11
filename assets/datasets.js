/* Progressive enhancement: the complete resource archive is already in the HTML. */
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const library = $('[data-dataset-catalog]');
  if (!library) return;
  const dialog = $('#dataset-dialog'), root = document.documentElement;
  if (typeof dialog.showModal !== 'function') return;
  const search = $('#dataset-search'), task = $('#dataset-task'), sort = $('#dataset-sort');
  const categories = [...document.querySelectorAll('[data-dataset-category]')];
  const norm = text => String(text).normalize('NFKC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
  const records = [...document.querySelectorAll('[data-dataset-id]')].map(node => ({
    node, id:node.dataset.datasetId, name:node.dataset.name, title:node.dataset.title,
    category:node.dataset.category, task:node.dataset.task, year:Number(node.dataset.year),
    order:Number(node.dataset.order), searchable:norm(node.dataset.search)
  }));
  const byId = new Map(records.map(record => [record.id,record]));
  const pageSize = 12;
  const readState = () => {
    const params = new URLSearchParams(location.search), category = params.get('category') || '';
    const selectedCategory = categories.some(b => b.dataset.datasetCategory === category) ? category : '';
    const selectedTask = params.get('task') || '';
    return {q:params.get('q') || '', category:selectedCategory,
      task:records.some(r => r.task === selectedTask && (!selectedCategory || r.category === selectedCategory)) ? selectedTask : '',
      sort:['name','year'].includes(params.get('sort')) ? params.get('sort') : 'source',
      page:Math.min(Math.ceil(records.length/pageSize),Math.max(1,Number.parseInt(params.get('page'),10)||1))};
  };
  let state = readState();
  const saveState = () => {
    const params = new URLSearchParams();
    for (const key of ['q','category','task']) if (state[key]) params.set(key,state[key]);
    if (state.sort !== 'source') params.set('sort',state.sort);
    if (state.page > 1) params.set('page',state.page);
    history.replaceState(history.state,'',location.pathname+(params.size?'?'+params:'')+location.hash);
  };
  const syncControls = () => {
    search.value = state.q; sort.value = state.sort;
    const tasks = [...new Set(records.filter(r => !state.category || r.category === state.category).map(r => r.task))];
    if (!tasks.includes(state.task)) state.task = '';
    task.replaceChildren(new Option('全部任务',''),...tasks.map(value => new Option(value,value)));
    task.value = state.task;
    categories.forEach(button => button.setAttribute('aria-pressed',String(button.dataset.datasetCategory === state.category)));
  };
  const render = (save = true) => {
    const terms = norm(state.q).split(' ').filter(Boolean);
    const matches = records.filter(r => (!state.category || r.category === state.category) && (!state.task || r.task === state.task) && terms.every(term => r.searchable.includes(term)));
    matches.sort((a,b) => state.sort === 'name' ? a.name.localeCompare(b.name,'en',{numeric:true}) || a.order-b.order : state.sort === 'year' ? b.year-a.year || a.order-b.order : a.order-b.order);
    state.page = Math.min(state.page,Math.max(1,Math.ceil(matches.length/pageSize)));
    const visible = matches.slice(0,state.page*pageSize), nodes = new Set(visible.map(r => r.node));
    records.forEach(({node}) => {node.hidden = !nodes.has(node);});
    const displayed = [...$('#dataset-results').children].filter(node => !node.hidden);
    if (displayed.some((node,index) => node !== visible[index].node)) {
      visible.forEach(({node}) => $('#dataset-results').append(node));
    }
    $('#dataset-empty').hidden = matches.length > 0;
    $('#dataset-result-count').textContent = `找到 ${matches.length} 项资源 / ${records.length} 项收录`;
    $('#dataset-load-status').textContent = matches.length ? `已显示 ${visible.length} / ${matches.length} 项资源` : '';
    $('#dataset-more').hidden = visible.length >= matches.length;
    syncControls(); if (save) saveState();
  };
  const reset = () => {state={q:'',category:'',task:'',sort:'source',page:1};render();};
  categories.forEach(button => button.addEventListener('click', () => {
    state.category = button.dataset.datasetCategory; state.page = 1; syncControls(); render();
  }));
  search.addEventListener('input', () => {state.q=search.value;state.page=1;render();});
  task.addEventListener('change', () => {state.task=task.value;state.page=1;render();});
  sort.addEventListener('change', () => {state.sort=sort.value;state.page=1;render();});
  document.querySelectorAll('[data-dataset-reset]').forEach(button => button.addEventListener('click',reset));
  $('#dataset-more').addEventListener('click', () => {
    const previous = new Set(records.filter(r => !r.node.hidden).map(r => r.node));
    state.page++; render();
    const next = [...$('#dataset-results').children].find(node => !node.hidden && !previous.has(node));
    if (next) {
      next.querySelector('h3 a').focus({preventScroll:true});
      next.scrollIntoView({block:'start',behavior:root.dataset.motion === 'off'?'instant':'smooth'});
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !event.metaKey && !event.ctrlKey && !event.altKey && !event.isComposing && !document.querySelector('dialog[open]') && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName) && !document.activeElement?.isContentEditable) {
      event.preventDefault();search.focus();
    }
  });

  const bindImageErrors = container => container.querySelectorAll('img').forEach(img => {
    const failed = () => {
      if (!img.isConnected) return;
      const note = document.createElement('span'); note.className='dataset-image-error';note.textContent='示例图暂不可用，完整说明与来源链接仍可查看。';
      img.replaceWith(note);
    };
    img.addEventListener('error',failed,{once:true});
    if (img.complete && !img.naturalWidth) failed();
  });
  let selected = null, opener = null, pushedByThisPage = false, closingFromHistory = false;
  const hashId = () => {try {return location.hash.startsWith('#dataset=') ? decodeURIComponent(location.hash.slice(9)) : null;} catch {return null;}};
  const openDetail = (id, push = false, trigger = null) => {
    const record = byId.get(id);
    if (!record) return false;
    if (dialog.open && selected?.id === id) return true;
    selected = record;
    if (trigger) opener = trigger;
    $('#dataset-dialog-title').textContent = record.name;
    $('#dataset-dialog-subtitle').textContent = record.title;
    const profile = record.node.querySelector('.dataset-profile').cloneNode(true);
    $('#dataset-dialog-content').replaceChildren(profile);
    bindImageErrors(profile);
    if (push && hashId() !== id) {
      history.pushState(history.state,'',location.pathname+location.search+'#dataset='+encodeURIComponent(id));
      pushedByThisPage = true;
    }
    if (!dialog.open) dialog.showModal();
    root.classList.add('dataset-modal-open');dialog.scrollTop=0;
    if (root.dataset.motion !== 'off' && dialog.animate) dialog.animate([{opacity:.4,transform:'translateY(10px)'},{opacity:1,transform:'translateY(0)'}],{duration:220,easing:'ease-out'});
    return true;
  };
  document.querySelectorAll('[data-dataset-open]').forEach(link => link.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.altKey || event.shiftKey) return;
    event.preventDefault();openDetail(link.dataset.datasetOpen,true,link);
  }));
  $('[data-dataset-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const r = dialog.getBoundingClientRect();
    if (event.clientX<r.left || event.clientX>r.right || event.clientY<r.top || event.clientY>r.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    root.classList.remove('dataset-modal-open');selected=null;
    const focusTarget = opener?.getClientRects().length ? opener : search;
    focusTarget.focus({preventScroll:true});
    if (closingFromHistory) {closingFromHistory=false;return;}
    if (pushedByThisPage) {pushedByThisPage=false;history.back();}
    else if (location.hash.startsWith('#dataset=')) history.replaceState(history.state,'',location.pathname+location.search+'#catalog');
  });
  $('[data-dataset-copy]').addEventListener('click', async () => {
    if (!selected) return;
    const url = new URL('datasets.html',location.href);url.hash='dataset='+selected.id;
    try {await navigator.clipboard.writeText(url.href);window.MMIFusionUI.notify('数据条目链接已复制，可以直接分享。');}
    catch {window.prompt('请复制条目链接：',url.href);}
  });
  const syncHash = () => {
    const id = hashId(), message = $('#dataset-message');message.hidden=true;
    if (id && openDetail(id)) return;
    if (dialog.open) {closingFromHistory=true;dialog.close();}
    if (location.hash.startsWith('#dataset=')) {
      message.textContent='没有找到这个数据条目，请通过名称、任务或作者搜索。';message.hidden=false;
    }
  };
  addEventListener('popstate', () => {pushedByThisPage=false;state=readState();render(false);syncHash();});
  addEventListener('hashchange', syncHash);
  render(false);
  library.classList.add('catalog-ready');
  document.querySelectorAll('[data-catalog-controls]').forEach(element => {element.hidden=false;});
  bindImageErrors(library);
  syncHash();
})();
