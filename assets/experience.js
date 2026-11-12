/* Original motion and reading UI. Content remains available without JavaScript. */
(() => {
  'use strict';
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const root = document.documentElement, reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let motion = root.dataset.motion !== 'off';
  const running = new Set();
  const syncMotion = () => {
    root.dataset.motion = motion ? 'on' : 'off';
    const button = $('.motion-toggle');
    button?.setAttribute('aria-pressed', String(!motion));
    button?.setAttribute('aria-label', motion ? '暂停装饰动画' : '开启装饰动画');
    if ($('[data-motion-label]')) $('[data-motion-label]').textContent = motion ? '动效开启' : '动效暂停';
    if (!motion) {
      running.forEach(animation => animation.finish()); running.clear();
      $('.fusion-scene')?.style.removeProperty('--scene-x'); $('.fusion-scene')?.style.removeProperty('--scene-y');
    }
  };
  syncMotion();
  $('.motion-toggle')?.addEventListener('click', () => {
    motion = !motion;
    try { localStorage.setItem('mmifusion-motion', motion ? 'on' : 'off'); } catch { /* Session preference still applies. */ }
    syncMotion();
  });
  reduced.addEventListener('change', event => { if (event.matches) { motion = false; syncMotion(); } });

  const scenes = {
    vision:['红外','热辐射 · 目标线索','可见光','纹理 · 颜色信息','互补信息，融合表达'],
    perception:['图像','场景 · 语义信息','三维','几何 · 空间结构','跨越模态，理解场景'],
    research:['论文','方法 · 研究问题','实验','数据 · 评估证据','连接知识，探索新可能']
  };
  const scene = $('.fusion-scene');
  $$('[data-signal-mode]').forEach(button => button.addEventListener('click', () => {
    if (!scene) return;
    const name = button.dataset.signalMode;
    scene.dataset.mode = name;
    ['left','left-note','right','right-note','result'].forEach((key,index) => $('[data-scene-'+key+']').textContent = scenes[name][index]);
    $$('[data-signal-mode]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  }));
  if (scene && 'IntersectionObserver' in window) {
    const visibility = new IntersectionObserver(([entry]) => scene.classList.toggle('scene-paused', !entry.isIntersecting));
    visibility.observe(scene);
    if (matchMedia('(hover:hover) and (pointer:fine)').matches) {
      let frame;
      scene.addEventListener('pointermove', event => {
        if (!motion) return;
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(() => {
          const rect = scene.getBoundingClientRect();
          scene.style.setProperty('--scene-y', ((event.clientX - rect.left) / rect.width - .5) * 5 + 'deg');
          scene.style.setProperty('--scene-x', ((event.clientY - rect.top) / rect.height - .5) * -4 + 'deg');
        });
      });
      scene.addEventListener('pointerleave', () => { cancelAnimationFrame(frame); scene.style.setProperty('--scene-x','0deg'); scene.style.setProperty('--scene-y','0deg'); });
    }
  }

  const readingTabs = $$('[data-reading-tab]'), groups = $$('[data-reading-group]');
  const covers = $$('.editorial-cover');
  const touchCovers = matchMedia('(hover:none), (pointer:coarse)');
  if (covers.length && 'IntersectionObserver' in window) {
    const coverVisibility = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        entry.target.classList.toggle('cover-offscreen', !entry.isIntersecting);
        entry.target.classList.toggle('stats-in-view', touchCovers.matches && entry.intersectionRatio >= .55);
      });
    }, {threshold:[0,.55],rootMargin:'-140px 0px 0px 0px'});
    covers.forEach(cover => coverVisibility.observe(cover));
    touchCovers.addEventListener('change', () => {
      covers.forEach(cover => { cover.classList.remove('stats-in-view'); coverVisibility.unobserve(cover); coverVisibility.observe(cover); });
    });
  } else if (touchCovers.matches) {
    covers.forEach(cover => cover.classList.add('stats-in-view'));
  }
  if (readingTabs.length) {
    const select = button => {
      readingTabs.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      groups.forEach(group => { group.hidden = group.dataset.readingGroup !== button.dataset.readingTab; });
      const visible = groups.find(group => !group.hidden);
      if (motion && visible?.animate) {
        const animation = visible.animate([{opacity:.3, transform:'translateY(10px)'},{opacity:1, transform:'translateY(0)'}],{duration:280,easing:'ease-out'});
        running.add(animation); animation.onfinish = () => running.delete(animation);
      }
    };
    groups.forEach(group => { group.hidden = group.dataset.readingGroup !== readingTabs[0].dataset.readingTab; });
    readingTabs.forEach((button,index) => {
      button.addEventListener('click', () => select(button));
      button.addEventListener('keydown', event => {
        let target;
        if (event.key === 'ArrowRight') target = (index + 1) % readingTabs.length;
        if (event.key === 'ArrowLeft') target = (index - 1 + readingTabs.length) % readingTabs.length;
        if (event.key === 'Home') target = 0;
        if (event.key === 'End') target = readingTabs.length - 1;
        if (target === undefined) return;
        event.preventDefault(); readingTabs[target].focus(); select(readingTabs[target]);
      });
    });
  }

  // Native content is never hidden waiting for an animation library or observer.
  if ('IntersectionObserver' in window) {
    const reveal = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        reveal.unobserve(entry.target);
        if (!motion || !entry.target.animate) return;
        const animation = entry.target.animate([{opacity:.12,transform:'translateY(24px)'},{opacity:1,transform:'translateY(0)'}],{duration:600,easing:'cubic-bezier(.16,1,.3,1)'});
        running.add(animation); animation.onfinish = () => running.delete(animation);
      });
    }, {threshold:.08});
    $$('.section-heading,.path-card,.dataset-preview,.dataset-overview,.catalog-card,.dataset-about,.venue-overview,.venue-spotlight,.team-overview,.community-members,.workbench-card,.module,.conference-card,.profile-card,.venue-card,.opportunity-card,.metric-definition,.download-card,.qr-card').filter(e => !e.closest('dialog')).forEach(e => reveal.observe(e));
  }

  let scrollFrame;
  const progress = () => {
    const remaining = document.documentElement.scrollHeight - innerHeight;
    root.style.setProperty('--reading-progress', remaining > 0 ? String(Math.min(1,scrollY / remaining)) : '0');
    if ($('.back-to-top')) $('.back-to-top').hidden = scrollY < 650;
    scrollFrame = null;
  };
  addEventListener('scroll', () => { if (!scrollFrame) scrollFrame = requestAnimationFrame(progress); }, {passive:true});
  addEventListener('resize', progress); progress();
  $('.back-to-top')?.addEventListener('click', () => scrollTo({top:0,behavior:motion?'smooth':'instant'}));
  $$('.resource-nav a').forEach(link => {
    if (new URL(link.href).pathname === location.pathname && !link.hash) link.setAttribute('aria-current','page');
  });
})();
