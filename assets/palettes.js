/* Each palette collection searches its full library before applying pagination. */
(() => {
  'use strict';
  const norm = value => value.normalize('NFKC').toLowerCase().trim();
  document.querySelectorAll('[data-palette-library]').forEach(section => {
    const cards = [...section.querySelectorAll('[data-palette-card]')];
    const grid = section.querySelector('.palette-grid');
    // Retain every original node/content for search and links, but mount only
    // the current page. Closed detail bodies do not need a live render tree.
    const records = cards.map(card => ({card,search:norm(card.dataset.paletteSearch),uses:JSON.parse(card.dataset.uses)}));
    cards.forEach(card => {
      const detail = card.querySelector('.palette-details');
      if (!detail || detail.open) return;
      const body = document.createDocumentFragment();
      [...detail.childNodes].filter(node => node !== detail.querySelector('summary')).forEach(node => body.append(node));
      detail.addEventListener('toggle',() => {if (detail.open && body.childNodes.length) detail.append(body);});
    });
    const input = section.querySelector('[data-palette-search-input]');
    const selects = [...section.querySelectorAll('[data-palette-filter]')];
    const pagers = [...section.querySelectorAll('[data-palette-pagination]')];
    const pageSize = 12;
    let page = 1, matched = cards;
    const render = () => {
      const terms = norm(input.value).split(/\s+/).filter(Boolean);
      matched = records.filter(({card,search,uses}) => terms.every(term => search.includes(term)) && selects.every(select => {
        const key = select.dataset.paletteFilter;
        return !select.value || (key === 'use' ? uses.includes(select.value) : card.dataset[key] === select.value);
      })).map(record => record.card);
      const pages = Math.max(1, Math.ceil(matched.length / pageSize));
      page = Math.max(1, Math.min(page, pages));
      const visible = matched.slice((page - 1) * pageSize, page * pageSize);
      const previous = [...grid.children];
      if (previous.length !== visible.length || previous.some((node,index) => node !== visible[index])) grid.replaceChildren(...visible);
      section.querySelector('[data-palette-count]').textContent = `匹配 ${matched.length} / ${cards.length} 组`;
      section.querySelector('[data-palette-empty]').hidden = matched.length > 0;
      pagers.forEach(pager => {
        pager.hidden = matched.length <= pageSize;
        pager.querySelector('[data-palette-page-label]').textContent = `第 ${page} / ${pages} 页 · 每页 ${pageSize} 组`;
        pager.querySelector('[data-palette-prev]').disabled = page === 1;
        pager.querySelector('[data-palette-next]').disabled = page === pages;
      });
    };
    const clearCardHash = () => {
      if (cards.some(card => '#' + card.id === location.hash)) history.replaceState(null, '', location.pathname + location.search + '#' + section.id);
    };
    const reset = () => {input.value = '';selects.forEach(s => {s.value = '';});page = 1;};
    const filter = () => {page = 1;clearCardHash();render();};
    input.addEventListener('input', filter);
    selects.forEach(select => select.addEventListener('change', filter));
    section.querySelectorAll('[data-palette-reset]').forEach(button => button.addEventListener('click', () => {reset();clearCardHash();render();}));
    pagers.forEach(pager => {
      pager.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
        page += button.hasAttribute('data-palette-next') ? 1 : -1;
        clearCardHash();render();
        pagers[0].focus({preventScroll:true});
        pagers[0].scrollIntoView({block:'start',behavior:document.documentElement.dataset.motion === 'off' ? 'instant' : 'smooth'});
      }));
    });
    const revealHash = () => {
      let id;try {id = decodeURIComponent(location.hash.slice(1));} catch {return;}
      const card = cards.find(card => card.id === id);
      if (!card) return;
      reset();page = Math.floor(cards.indexOf(card) / pageSize) + 1;render();
      card.focus({preventScroll:true});card.scrollIntoView({block:'start',behavior:'instant'});
    };
    render();
    addEventListener('hashchange', revealHash);
    if (location.hash) requestAnimationFrame(revealHash);
  });
})();
