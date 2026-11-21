/* Live navigation, real PV integration, source-based rankings and playful rituals. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const root = document.documentElement, Core = window.MMIFusionCommunity;
  const motion = () => root.dataset.motion !== 'off';
  const store = {read(key, fallback) {try {return JSON.parse(localStorage.getItem(key)) ?? fallback;} catch {return fallback;}},
    write(key, value) {try {localStorage.setItem(key,JSON.stringify(value)); return true;} catch {return false;}}};
  const announce = text => window.MMIFusionUI.notify(text);
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
    const active = links.find(a => a.hasAttribute('aria-current')) || null;
    let displayed = active;
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
  function paintClock(clock, value) {
    // Keep a single readable time label; only changed digits move.
    if (clock.children.length !== value.length) {
      clock.replaceChildren(...[...value].map(char => {
        const span = document.createElement('span');
        span.className = char === ':' ? 'clock-separator' : 'clock-digit';
        span.textContent = char;span.setAttribute('aria-hidden','true');return span;
      }));
    } else {
      [...value].forEach((char,index) => {
        const digit = clock.children[index];
        if (digit.textContent === char) return;
        digit.textContent = char;
        if (!document.hidden && clock.getBoundingClientRect().bottom > 0) {
          animate(digit,[{opacity:.4,transform:'translateY(-5px)'},{opacity:1,transform:'translateY(0)'}],{duration:360,easing:'cubic-bezier(.2,.8,.2,1)'});
        }
      });
    }
    clock.setAttribute('aria-label',`北京时间 ${value}`);
  }
  function updateClock() {
    const now = new Date(), day = Core.dateKey(now), date = $('[data-live-date]'), clock = $('[data-live-clock]');
    if (date && date.dateTime !== day) {date.textContent = dateFormat.format(now).replace('星期',' 星期');date.dateTime = day;}
    if (clock) {paintClock(clock,clockFormat.format(now));clock.dateTime = now.toISOString();}
    if (knownDay && knownDay !== day) document.dispatchEvent(new CustomEvent('mmi-date-change',{detail:day}));
    knownDay = day;
  }
  updateClock(); setInterval(updateClock,1000);

  // Keep the confirmed history; only the provider can increment new visits.
  const count = $('[data-visit-count]'), status = $('[data-visit-state]');
  if (count && status) {
    const meter = $('.visit-meter');
    const baseline = Number(meter.dataset.visitBaseline);
    const setState = (state, text) => {
      // Keep connection/cache details available to assistive technology only.
      meter.dataset.visitStatus = state;status.textContent = text;
    };
    if (location.hostname.toLowerCase() !== 'mmifusion.github.io') {
      count.textContent = '—';
      setState('preview','本地预览不计入网站访问量');
    } else if (Number.isSafeInteger(baseline) && baseline >= 0) {
      const cacheKey = 'mmifusion-site-pv-v2', provider = 'bsz-saop-20261117';
      const validCache = saved => saved && Number.isSafeInteger(saved.total) && saved.total >= baseline &&
        Number.isSafeInteger(saved.at) && saved.at > 0 && saved.at <= Date.now();
      const readCache = () => {
        const current = store.read(cacheKey,null), legacy = store.read('mmifusion-site-pv-v1',null);
        return [current?.provider === provider ? current : null,legacy].filter(validCache)
          .sort((a,b) => b.total-a.total || b.at-a.at)[0] || null;
      };
      let cached = readCache();
      const stamp = at => new Intl.DateTimeFormat('zh-CN',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}).format(new Date(at));
      const retain = reason => {
        // Another tab may have synchronized a higher count in the meantime.
        const latest = readCache();
        if (latest && (!cached || latest.total >= cached.total)) cached = latest;
        const total = cached ? cached.total : baseline;
        count.textContent = total.toLocaleString('en-US');count.dataset.total = String(total);
        const detail = cached ? `${stamp(cached.at)} 上次同步的 PV` : `迁移时确认保留的 ${baseline.toLocaleString('en-US')} 次历史访问`;
        setState('cached',`${reason}；当前显示${detail}，不是实时数据。`);
      };
      retain('访问统计将在页面加载完成后后台更新');
      let started = false, controller, timeout, leaving = false;
      window.addEventListener('pagehide',() => {
        leaving = true;clearTimeout(timeout);controller?.abort();
      },{once:true});
      const sync = async () => {
        if (started || leaving) return;
        started = true;
        // Fetch never delays window.load; abort cancels a stalled request/body.
        controller = new AbortController();
        timeout = setTimeout(() => controller.abort(),8000);
        try {
          const response = await fetch('https://bsz.saop.cc/api',{
            method:'POST',credentials:'omit',cache:'no-store',referrerPolicy:'no-referrer',
            headers:{'x-bsz-referer':'https://mmifusion.github.io/'},signal:controller.signal
          });
          if (!response.ok) throw new Error('统计服务暂不可用');
          const result = await response.json(), raw = result?.data?.site_pv;
          if (result?.success !== true || !Number.isSafeInteger(raw) || raw < 0 || raw > Number.MAX_SAFE_INTEGER-baseline) throw new Error('统计服务返回的数据无效');
          if (controller.signal.aborted) throw new Error('统计请求已取消');
          const total = baseline+raw, latest = readCache();
          if (latest && (!cached || latest.total >= cached.total)) cached = latest;
          if (total < (cached?.total ?? baseline)) {
            retain('新统计结果尚未超过已保存次数');return;
          }
          const previous = Number(count.dataset.total) || baseline;
          cached = {total,at:Date.now(),provider};store.write(cacheKey,cached);
          count.dataset.total = String(total);
          setState('live',`本站页面访问次数（PV），保留 ${baseline.toLocaleString('en-US')} 次历史基数，加上 BSZ 服务自 2026-11-17 起累计的新增访问；不代表独立人数。`);
          meter.classList.add('visit-connected');
          if (!motion()) {count.textContent = total.toLocaleString('en-US');return;}
          const start = performance.now();
          const tick = time => {
            const progress = motion() ? Math.min(1,(time-start)/1100) : 1;
            count.textContent = Math.round(previous+(total-previous)*(1-Math.pow(1-progress,3))).toLocaleString('en-US');
            if (progress < 1) requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
        } catch {
          retain(controller.signal.aborted ? '访问统计响应超时，已停止等待' : '访问统计暂时无法连接');
        } finally {
          clearTimeout(timeout);
        }
        // No increment retry: an interrupted request may already have counted.
      };
      const schedule = () => setTimeout(sync,0);
      if (document.readyState === 'complete') schedule();
      else window.addEventListener('load',schedule,{once:true});
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
