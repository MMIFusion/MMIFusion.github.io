/* Calendar display rules; date-only entries never acquire an invented deadline. */
(function (root) {
  'use strict';
  function status(event, now = new Date()) {
    const timestamp = +now;
    if (event.kind === 'deadline') {
      const remaining = Date.parse(event.at) - timestamp;
      return {ended:remaining <= 0, imminent:remaining > 0 && remaining <= 72 * 3600000,
        remaining, order:Date.parse(event.at)};
    }
    // Retain floating dates until they have ended even in UTC−12. This is only
    // an archive/display boundary, never a precise submission cutoff or ICS time.
    return {ended:timestamp >= Date.parse(event.endExclusive + 'T12:00:00Z'),
      imminent:false, remaining:null, order:Date.parse(event.start + 'T12:00:00Z')};
  }
  const api = {status};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.MMIFusionCalendar = api;
})(typeof window === 'undefined' ? globalThis : window);
