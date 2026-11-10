const assert = require('node:assert/strict');
const {dateKey, fortune, monthDays} = require('../assets/community-core.js');

// The real clock is Beijing-based, independently of the browser's own timezone.
assert.equal(dateKey(new Date('2026-12-31T15:59:59Z')), '2026-12-31');
assert.equal(dateKey(new Date('2026-12-31T16:00:00Z')), '2027-01-01');
assert.equal(dateKey(new Date('2026-11-10T16:00:00Z')), '2026-11-11');

// Gregorian month boundaries, including leap-year exceptions and weekday offset.
assert.equal(monthDays(2028,2).days.length,29);
assert.equal(monthDays(2027,2).days.length,28);
assert.equal(monthDays(2000,2).days.length,29);
assert.equal(monthDays(2100,2).days.length,28);
assert.equal(monthDays(2026,11).offset,6); // Nov 1 is Sunday; Monday-first calendar.
assert.equal(monthDays(2026,12).days.at(-1),'2026-12-31');
assert.throws(() => monthDays(2026,13));
assert.throws(() => fortune('2026-02-29'));
assert.throws(() => fortune('2026-13-01'));
assert.deepEqual(fortune('2028-02-29'),fortune('2028-02-29'));
for (const day of monthDays(2026,11).days) {
  const sign = fortune(day);
  assert.ok(['大吉','宜投','顺遂','蓄力'].includes(sign.label));
  assert.ok(sign.title && sign.note && sign.yes && sign.avoid);
}
console.log('PASS: Beijing midnight rollover, Gregorian leap years/months, deterministic playful day cards.');
