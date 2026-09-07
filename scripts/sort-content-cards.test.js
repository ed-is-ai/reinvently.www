var appended = [];
function card(meta) {
  return {
    meta: meta,
    matches: function () { return true; },
    querySelector: function () { return { textContent: this.meta }; }
  };
}

var grid = {
  children: [card('2 July 2026'), card('Pinned · Updated 1 September 2026'), card('Updated 7 September 2026')],
  appendChild: function (item) { appended.push(item.meta); }
};
global.document = { querySelectorAll: function () { return [grid]; } };

require('./sort-content-cards.js');

var expected = ['Pinned · Updated 1 September 2026', 'Updated 7 September 2026', '2 July 2026'];
if (JSON.stringify(appended) !== JSON.stringify(expected)) throw new Error('Unexpected card order: ' + appended.join(', '));
