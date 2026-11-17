const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

// Exercise the production counter with controlled network/lifecycle events.
// Clock, navigation and rankings are independent of this block.
const source = fs.readFileSync(require.resolve('../assets/community.js'),'utf8');
const start = source.indexOf('  // Keep the confirmed history;');
const end = source.indexOf('\n  const rankTabs',start);
assert.ok(start > 0 && end > start);
const code = source.slice(start,end);
const cacheKey = 'mmifusion-site-pv-v2', legacyKey = 'mmifusion-site-pv-v1';
const provider = 'bsz-saop-20261117';

function setup({legacy, saved, denied=false, hostname='mmifusion.github.io', ready='loading'}={}) {
  const elements = {
    '[data-visit-count]': {textContent:'1,100',dataset:{total:'1100'}},
    '[data-visit-state]': {textContent:''},
    '[data-visit-hint]': {textContent:'',hidden:false},
    '.visit-meter': {dataset:{visitBaseline:'1100'},classList:{add() {}}}
  };
  const storage = new Map([[legacyKey,legacy],[cacheKey,saved]]), events = new Map(), timers = new Map(), calls = [];
  let timerId=0, aborted=0;
  vm.runInNewContext(code,{
    $: selector=>elements[selector],location:{hostname},document:{readyState:ready},
    window:{addEventListener(name,fn) {events.set(name,fn);}},
    store:{read(key,fallback) {return denied ? fallback : storage.get(key) ?? fallback;},write(key,value) {if (!denied) storage.set(key,value);}},
    setTimeout(fn,ms) {timers.set(++timerId,{fn,ms});return timerId;},clearTimeout(id) {timers.delete(id);},
    AbortController,Date,Intl,Number,Error,motion:()=>false,
    fetch(url,options) {
      return new Promise((resolve,reject)=>{
        options.signal.addEventListener('abort',()=>{aborted++;reject(new Error('aborted'));});
        calls.push({url,options,resolve,reject});
      });
    }
  });
  const runTimer = ms => {
    for (const [id,timer] of timers) if (timer.ms === ms) {timers.delete(id);timer.fn();break;}
  };
  const settle = async()=>{await new Promise(resolve=>setImmediate(resolve));};
  return {elements,storage,calls,events,timers,runTimer,settle,get aborted(){return aborted;},
    async load() {events.get('load')?.();runTimer(0);await settle();},
    async response(body,ok=true) {calls.at(-1).resolve({ok,json:async()=>body});await settle();},
    async success(raw) {await this.response({success:true,data:{site_pv:raw}});},
    count:()=>elements['[data-visit-count]'].textContent,
    state:()=>elements['.visit-meter'].dataset.visitStatus,
    hint:()=>elements['[data-visit-hint]'].textContent,
    status:()=>elements['[data-visit-state]'].textContent
  };
}

(async()=>{
  const fresh=setup();
  assert.equal(fresh.count(),'1,100');assert.equal(fresh.hint(),'历史保留');assert.equal(fresh.calls.length,0);
  await fresh.load();assert.equal(fresh.calls.length,1);
  assert.equal(fresh.calls[0].options.method,'POST');
  assert.equal(fresh.calls[0].options.credentials,'omit');
  assert.equal(fresh.calls[0].options.headers['x-bsz-referer'],'https://mmifusion.github.io/');
  await fresh.success(3);assert.equal(fresh.count(),'1,103');assert.equal(fresh.state(),'live');assert.equal(fresh.timers.size,0);
  const next=setup({saved:fresh.storage.get(cacheKey)});await next.load();await next.success(4);
  assert.equal(next.count(),'1,104','history is added once, never compounded with cached totals');

  const legacy={total:1250,at:Date.now()-60000};
  const offline=setup({legacy});await offline.load();offline.calls[0].reject(new Error('offline'));await offline.settle();
  assert.equal(offline.count(),'1,250');assert.equal(offline.hint(),'上次同步');assert.match(offline.status(),/不是实时数据/);
  assert.equal(offline.storage.get(legacyKey),legacy);

  const slow=setup();await slow.load();slow.runTimer(8000);await slow.settle();
  assert.equal(slow.aborted,1);assert.equal(slow.count(),'1,100');assert.match(slow.status(),/已停止等待/);
  assert.equal(slow.calls.length,1);assert.equal(slow.timers.size,0);

  const reading=setup();await reading.load();
  reading.calls[0].resolve({ok:true,json:()=>new Promise((_,reject)=>reading.calls[0].options.signal.addEventListener('abort',()=>reject(new Error('body stalled'))))});
  await reading.settle();reading.runTimer(8000);await reading.settle();assert.match(reading.status(),/已停止等待/);

  for (const raw of [-1,1.5,'20',null,Number.MAX_SAFE_INTEGER]) {
    const bad=setup();await bad.load();await bad.success(raw);assert.equal(bad.count(),'1,100');assert.equal(bad.state(),'cached');
  }
  for (const body of [{success:false,data:{site_pv:20}},{success:true},null]) {
    const bad=setup();await bad.load();await bad.response(body);assert.equal(bad.state(),'cached');assert.equal(bad.count(),'1,100');
  }
  const badHttp=setup();await badHttp.load();await badHttp.response({},false);assert.equal(badHttp.state(),'cached');
  for (const legacy of [{total:-2,at:Date.now()},{total:999,at:Date.now()},{total:'1200',at:Date.now()},{total:1500,at:Date.now()+60000}]) {
    assert.equal(setup({legacy}).count(),'1,100');
  }
  const denied=setup({denied:true});await denied.load();await denied.success(10);assert.equal(denied.count(),'1,110');
  const lower=setup({legacy});await lower.load();await lower.success(2);
  assert.equal(lower.count(),'1,250');assert.equal(lower.state(),'cached');assert.match(lower.status(),/尚未超过/);
  const concurrent=setup();await concurrent.load();concurrent.storage.set(cacheKey,{total:1300,at:Date.now(),provider});await concurrent.success(4);
  assert.equal(concurrent.count(),'1,300');assert.equal(concurrent.state(),'cached');
  const preview=setup({hostname:'localhost'});await preview.load();assert.equal(preview.calls.length,0);assert.equal(preview.state(),'preview');
  const late=setup({ready:'complete'});late.runTimer(0);await late.settle();assert.equal(late.calls.length,1);await late.success(1);
  const leaving=setup();await leaving.load();leaving.events.get('pagehide')();await leaving.settle();assert.equal(leaving.aborted,1);
  console.log('PASS visits: load isolation, 1100 baseline, migration/reload, offline and timeout abort, invalid responses, cache floors, blocked storage, preview, page exit.');
})().catch(error=>{console.error(error);process.exitCode=1;});
