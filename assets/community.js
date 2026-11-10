/* Live navigation, real PV integration, source-based rankings and playful rituals. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const root = document.documentElement, Core = window.MMIFusionCommunity;
  const motion = () => root.dataset.motion !== 'off';
  const store = {read(key, fallback) {try {return JSON.parse(localStorage.getItem(key)) ?? fallback;} catch {return fallback;}},
    write(key, value) {try {localStorage.setItem(key,JSON.stringify(value)); return true;} catch {return false;}}};
  const announce = text => {
    const box = $('#toast'); if (!box) return;
    (document.querySelector('dialog[open]') || document.body).append(box);
    box.textContent = text; box.classList.add('visible');
    clearTimeout(announce.timer); announce.timer = setTimeout(() => box.classList.remove('visible'),3000);
  };
  const running = new Set();
  const animate = (element, frames, options) => {
    if (!motion() || !element?.animate) return null;
    const animation = element.animate(frames,options);running.add(animation);
    animation.onfinish = () => running.delete(animation);return animation;
  };
  new MutationObserver(() => {if (!motion()) {running.forEach(a => a.finish());running.clear();}}).observe(root,{attributes:true,attributeFilter:['data-motion']});

  // A single pill follows both pointer and keyboard selection. Links stay native.
  const nav = $('.resource-nav'), indicator = $('.resource-indicator');
  if (nav && indicator) {
    const links = [...nav.querySelectorAll('.resource-item')];
    let active = links.find(a => a.hasAttribute('aria-current')) || null, displayed = active;
    const move = target => {
      displayed = target;
      links.forEach(a => a.classList.toggle('indicator-selected',a === target));
      indicator.style.opacity = target ? '1' : '0';
      if (!target) return;
      indicator.style.width = `${target.offsetWidth}px`;
      indicator.style.transform = `translateX(${target.offsetLeft}px)`;
    };
    move(active);
    requestAnimationFrame(() => nav.classList.add('indicator-ready'));
    links.forEach(link => {
      link.addEventListener('pointerenter', () => move(link));
      link.addEventListener('focus', () => move(link));
      link.addEventListener('click', event => {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.target === '_blank') return;
        if (!motion()) return;
        event.preventDefault(); active = link; move(link);
        setTimeout(() => location.assign(link.href),180);
      });
    });
    nav.addEventListener('pointerleave', () => move(active));
    nav.addEventListener('focusout', event => {if (!nav.contains(event.relatedTarget)) move(active);});
    if ('ResizeObserver' in window) new ResizeObserver(() => move(displayed)).observe(nav);
    document.fonts.ready.then(() => {
      move(active);
      if (active && nav.scrollWidth > nav.clientWidth) nav.scrollLeft = Math.max(0,active.offsetLeft - (nav.clientWidth-active.offsetWidth)/2);
    });
  }

  const dateFormat = new Intl.DateTimeFormat('zh-CN',{timeZone:'Asia/Shanghai',year:'numeric',month:'long',day:'numeric',weekday:'long'});
  const clockFormat = new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Shanghai',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'});
  let knownDay;
  function updateClock() {
    const now = new Date(), day = Core.dateKey(now), date = $('[data-live-date]'), clock = $('[data-live-clock]');
    if (date) {date.textContent = dateFormat.format(now);date.dateTime = day;}
    if (clock) {clock.textContent = clockFormat.format(now);clock.dateTime = now.toISOString();}
    if (knownDay && knownDay !== day) document.dispatchEvent(new CustomEvent('mmi-date-change',{detail:day}));
    knownDay = day;
  }
  updateClock(); setInterval(updateClock,1000);

  // Provider-owned aggregate count. Never invent a total or count preview visits.
  const count = $('[data-visit-count]'), status = $('[data-visit-state]');
  if (count && status) {
    const setState = text => {status.textContent = text;$('.visit-meter').title = text;};
    if (location.hostname.toLowerCase() !== 'mmifusion.github.io') {
      setState('本地预览不计入网站访问量');
    } else {
      const source = $('#busuanzi_value_site_pv');
      let timeout;
      const observer = new MutationObserver(() => {
        const raw = source.textContent.trim();
        if (!/^\d+$/.test(raw)) return;
        const total = Number(raw); if (!Number.isSafeInteger(total)) return;
        observer.disconnect(); clearTimeout(timeout); count.dataset.total = raw;
        setState('本站页面访问次数（PV），由不蒜子提供，从接入起累计；不代表独立人数。');
        $('.visit-meter').classList.add('visit-connected');
        if (!motion()) {count.textContent = total.toLocaleString('en-US');return;}
        const start = performance.now();
        const tick = time => {
          const progress = motion() ? Math.min(1,(time-start)/1100) : 1;
          count.textContent = Math.round(total*(1-Math.pow(1-progress,3))).toLocaleString('en-US');
          if (progress < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
      observer.observe(source,{childList:true,subtree:true,characterData:true});
      timeout = setTimeout(() => {count.textContent = '—';setState('访问统计暂不可用，请稍后再试；不影响阅读。');},15000);
      const script = document.createElement('script'); script.async = true;
      script.src = 'https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js';
      script.onerror = () => {clearTimeout(timeout);setState('访问统计服务暂不可用；不影响阅读。');};
      document.head.append(script);
    }
  }

  const rankTabs = $$('[data-rank-tab]'), rankGroups = $$('[data-rank-group]');
  if (rankTabs.length) {
    const select = button => {
      rankTabs.forEach(tab => tab.setAttribute('aria-pressed',String(tab === button)));
      rankGroups.forEach(group => {group.hidden = group.dataset.rankGroup !== button.dataset.rankTab;});
      const visible = rankGroups.find(group => !group.hidden);
      animate(visible,[{opacity:.3,transform:'translateY(12px)'},{opacity:1,transform:'translateY(0)'}],{duration:350,easing:'ease-out'});
    };
    rankGroups.forEach(group => {group.hidden = group.dataset.rankGroup !== 'reads';});
    rankTabs.forEach((button,index) => {
      button.addEventListener('click', () => select(button));
      button.addEventListener('keydown', event => {
        const next = event.key === 'ArrowRight' ? (index+1)%rankTabs.length : event.key === 'ArrowLeft' ? (index+rankTabs.length-1)%rankTabs.length : event.key === 'Home' ? 0 : event.key === 'End' ? rankTabs.length-1 : null;
        if (next === null) return; event.preventDefault();rankTabs[next].focus();select(rankTabs[next]);
      });
    });
  }
  $$('[data-share-url]').forEach(button => button.addEventListener('click', async () => {
    const url = button.dataset.shareUrl, title = button.dataset.shareTitle;
    try {
      if (navigator.share) {await navigator.share({title,url});return;}
      await navigator.clipboard.writeText(`${title}\n${url}`);announce('标题和原文链接已复制，可以粘贴转发。');
    } catch (error) {
      if (error.name !== 'AbortError') window.prompt('复制原文链接后转发：',url);
    }
  }));

  const luck = $('#luck-dialog');
  if (luck && typeof luck.showModal === 'function') {
    let opener, busy = false;
    const dayState = () => {
      const day = Core.dateKey(), saved = store.read('mmifusion-luck-v1',{});
      return {date:day,count:saved && saved.date === day && Number.isSafeInteger(saved.count) ? Math.max(0,saved.count) : 0};
    };
    const syncLuck = () => {
      const state = dayState();
      $('[data-luck-saved]').textContent = state.count ? `今天已接住 ${state.count} 份好心情 · 本机记录` : '送给正在认真努力的你';
      $('[data-luck-message]').textContent = state.count ? Core.messages[(Core.hash(state.date)+state.count-1)%Core.messages.length] : '点一下，把今天的好运收下。';
    };
    $$('[data-luck-open]').forEach(button => button.addEventListener('click', () => {
      opener = button;syncLuck();luck.showModal();root.classList.add('luck-modal-open');
    }));
    $('[data-luck-close]').addEventListener('click', () => luck.close());
    luck.addEventListener('close', () => {root.classList.remove('luck-modal-open');opener?.focus({preventScroll:true});});
    luck.addEventListener('click', event => {
      if (event.target !== luck) return;
      const r = luck.getBoundingClientRect();
      if (event.clientX<r.left || event.clientX>r.right || event.clientY<r.top || event.clientY>r.bottom) luck.close();
    });
    $('[data-luck-claim]').addEventListener('click', () => {
      if (busy) return;busy = true;setTimeout(() => {busy=false;},350);
      const state = dayState();state.count = Math.min(99999,state.count+1);
      const saved = store.write('mmifusion-luck-v1',state);
      $('[data-luck-message]').textContent = Core.messages[(Core.hash(state.date)+state.count-1)%Core.messages.length];
      $('[data-luck-saved]').textContent = saved ? `今天已接住 ${state.count} 份好心情 · 本机记录` : '好运已收到，本次祝福不保存到浏览器';
      animate($('.luck-seal'),[{transform:'scale(1) rotate(0)'},{transform:'scale(1.18) rotate(-8deg)'},{transform:'scale(1) rotate(0)'}],{duration:600,easing:'ease-out'});
      const confetti = $('.luck-confetti');confetti.replaceChildren();
      if (motion()) {
        for(let i=0;i<22;i++) {
          const dot = document.createElement('i');dot.style.setProperty('--x',`${(i%11-5)*27}px`);dot.style.setProperty('--y',`${-80-(i%5)*31}px`);dot.style.setProperty('--turn',`${i*31}deg`);dot.style.background=['#bd9cff','#f7bd78','#91ddd0','#ef8fbb'][i%4];confetti.append(dot);
        }
        setTimeout(() => confetti.replaceChildren(),1400);
      }
    });
  }

  const calendar = $('[data-fortune-days]');
  if (calendar) {
    let selected = Core.dateKey(), viewYear = Number(selected.slice(0,4)), viewMonth = Number(selected.slice(5,7));
    const detail = () => {
      const sign = Core.fortune(selected);
      $('[data-fortune-date]').textContent = dateFormat.format(new Date(selected+'T04:00:00Z'));
      $('[data-fortune-date]').dateTime = selected;
      $('[data-fortune-verdict]').textContent = sign.label;$('[data-fortune-title]').textContent = sign.title;
      $('[data-fortune-note]').textContent = sign.note;$('[data-fortune-do]').textContent = sign.yes;$('[data-fortune-avoid]').textContent = sign.avoid;
      calendar.querySelectorAll('[data-day]').forEach(b => {b.setAttribute('aria-pressed',String(b.dataset.day===selected));});
    };
    const render = () => {
      const {offset,days} = Core.monthDays(viewYear,viewMonth), today = Core.dateKey();
      $('[data-fortune-month]').textContent = `${viewYear} 年 ${viewMonth} 月`;
      calendar.replaceChildren();
      for(let i=0;i<offset;i++){const blank=document.createElement('span');blank.className='fortune-blank';blank.setAttribute('aria-hidden','true');calendar.append(blank);}
      days.forEach(day => {
        const sign=Core.fortune(day),button=document.createElement('button'),number=document.createElement('strong'),label=document.createElement('span');
        button.type='button';button.dataset.day=day;button.className='fortune-day';
        if(sign.label==='大吉'||sign.label==='宜投')button.classList.add('day-lucky');
        if(day===today){button.classList.add('day-today');button.setAttribute('aria-current','date');}
        button.setAttribute('aria-label',`${day}${day===today?' 今天':''}，趣味日签：${sign.label}`);
        number.textContent=String(Number(day.slice(8)));label.textContent=sign.label;button.append(number,label);
        button.addEventListener('click',()=>{selected=day;detail();animate($('.fortune-detail'),[{opacity:.5,transform:'translateY(8px)'},{opacity:1,transform:'translateY(0)'}],{duration:280});});
        calendar.append(button);
      });
      $('[data-month-step="-1"]').disabled=viewYear===1900&&viewMonth===1;
      $('[data-month-step="1"]').disabled=viewYear===2200&&viewMonth===12;detail();
    };
    $$('[data-month-step]').forEach(button => button.addEventListener('click', () => {
      const next=new Date(Date.UTC(viewYear,viewMonth-1+Number(button.dataset.monthStep),1));viewYear=next.getUTCFullYear();viewMonth=next.getUTCMonth()+1;
      selected=`${viewYear}-${String(viewMonth).padStart(2,'0')}-01`;render();
    }));
    $('[data-month-today]').addEventListener('click', () => {selected=Core.dateKey();viewYear=Number(selected.slice(0,4));viewMonth=Number(selected.slice(5,7));render();});
    document.addEventListener('mmi-date-change', render);render();
  }
  const checks = store.read('mmifusion-submission-checks-v1',{});
  $$('[data-submission-check]').forEach(input => {
    input.checked = checks?.[input.dataset.submissionCheck] === true;
    input.addEventListener('change', () => {
      const values=Object.fromEntries($$('[data-submission-check]').map(i=>[i.dataset.submissionCheck,i.checked]));
      if(!store.write('mmifusion-submission-checks-v1',values))announce('当前浏览器无法保存勾选，本次打开期间仍然可用。');
    });
  });
})();
