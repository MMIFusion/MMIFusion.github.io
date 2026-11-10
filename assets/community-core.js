/* Deterministic entertainment cards, independent from real conference deadlines. */
(function (root) {
  'use strict';
  const messages = [
    '愿你的每一份认真，都迎来值得的回响。',
    '祝实验顺利，想法清晰，好消息正在路上。',
    '今天接住好运，明天继续把研究做好。',
    '愿你遇见懂这份工作的读者和同行。',
    '祝灵感常来，代码少报错，稿件早日定稿。',
    '愿你的耐心和坚持，开出自己的花。',
    '接住一份好心情，下一步也从容。',
    '祝论文表达清楚，实验结果经得起推敲。'
  ];
  const signs = [
    {label:'大吉',title:'准备充分，今天就勇敢提交。',note:'把最后一轮核对做完，为这段研究按下新的起点。',yes:'核对附件 · 提前上传 · 从容投稿',avoid:'卡点提交 · 忘记匿名'},
    {label:'宜投',title:'带着底气，迈出下一步。',note:'一份清楚、完整的稿件，值得被认真看见。',yes:'通读摘要 · 核对作者 · 预览文件',avoid:'漏传材料 · 只看本地版本'},
    {label:'顺遂',title:'不慌不忙，把细节安排妥当。',note:'让表达再清楚一点，让证据再完整一点。',yes:'检查引用 · 校对图表 · 留出余量',avoid:'临时改大段 · 忽略投稿说明'},
    {label:'蓄力',title:'再打磨一下，也是在向前。',note:'今天适合认真核对。若已准备好且临近截止，请按时提交。',yes:'复查实验 · 精简表达 · 备份文件',avoid:'等待运气 · 错过真实截止'},
    {label:'大吉',title:'好日子，留给认真准备的你。',note:'给自己一个积极的开始，余下的交给扎实的工作。',yes:'完成检查 · 保存回执 · 好好休息',avoid:'遗漏确认邮件 · 上传后不检查'}
  ];
  function dateKey(date = new Date()) {
    const parts = new Intl.DateTimeFormat('en-CA', {timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(date);
    const values = Object.fromEntries(parts.map(p => [p.type,p.value]));
    return `${values.year}-${values.month}-${values.day}`;
  }
  function hash(value) {
    let result = 2166136261;
    for (const char of value) { result ^= char.charCodeAt(0); result = Math.imul(result,16777619); }
    return result >>> 0;
  }
  function fortune(key) {
    const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(key);
    if (!match) throw new Error('Invalid date');
    const day = new Date(`${key}T12:00:00Z`);
    if (Number.isNaN(day.getTime()) || day.toISOString().slice(0,10) !== key) throw new Error('Invalid date');
    return {...signs[hash('MMIFusion-research-day-v1:' + key) % signs.length], key};
  }
  function monthDays(year, month) {
    if (!Number.isInteger(year) || year < 1900 || year > 2200 || !Number.isInteger(month) || month < 1 || month > 12) throw new Error('Invalid month');
    const count = new Date(Date.UTC(year, month, 0)).getUTCDate();
    return {offset:(new Date(Date.UTC(year, month - 1, 1)).getUTCDay() + 6) % 7,
      days:Array.from({length:count}, (_, i) => `${year}-${String(month).padStart(2,'0')}-${String(i+1).padStart(2,'0')}`)};
  }
  const api = {dateKey, fortune, monthDays, messages, hash};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.MMIFusionCommunity = api;
})(typeof window === 'undefined' ? globalThis : window);
