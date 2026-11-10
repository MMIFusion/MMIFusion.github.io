/* Analytical fixtures, independent of implementation details. No dependencies. */
const assert = require('node:assert/strict');
const {evaluate} = require('../assets/metrics-core.js');
const rgba = values => Uint8ClampedArray.from(values.flatMap(value => [value,value,value,255]));
const near = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-9, `${actual} != ${expected}`);
let r = evaluate(rgba([128,128,128,128]),2,2);
for (const v of Object.values(r)) near(v,0);
r = evaluate(rgba([0,255,255,0]),2,2);
near(r.en,1); near(r.sd,127.5); near(r.sf,255*Math.SQRT2);
r = evaluate(rgba(Array.from({length:256},(_,i)=>i)),256,1);
near(r.en,8); near(r.sd,Math.sqrt((256**2-1)/12)); near(r.sf,1);
r = evaluate(Uint8ClampedArray.from([0,0,0,0,255,255,255,255]),2,1);
for (const v of Object.values(r)) near(v,0);
r = evaluate(rgba([42]),1,1);
for (const v of Object.values(r)) near(v,0);
assert.throws(()=>evaluate(new Uint8Array(3),1,1));
console.log('PASS: EN / population SD / valid-neighbour SF; flat, checker, ramp, transparency, 1px, invalid dimensions.');
