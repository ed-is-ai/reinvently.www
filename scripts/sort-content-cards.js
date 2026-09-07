(function () {
  var months = {
    January: 0, February: 1, March: 2, April: 3, May: 4, June: 5,
    July: 6, August: 7, September: 8, October: 9, November: 10, December: 11
  };

  document.querySelectorAll('[data-sort-cards]').forEach(function (grid) {
    var cards = Array.from(grid.children).filter(function (item) {
      return item.matches('a');
    });

    cards.sort(function (left, right) {
      var leftMeta = left.querySelector('.post-meta, p').textContent;
      var rightMeta = right.querySelector('.post-meta, p').textContent;
      var leftPinned = leftMeta.indexOf('Pinned') !== -1;
      var rightPinned = rightMeta.indexOf('Pinned') !== -1;
      if (leftPinned !== rightPinned) return leftPinned ? -1 : 1;

      function timestamp(meta) {
        var match = meta.match(/(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})/);
        return match ? Date.UTC(Number(match[3]), months[match[2]], Number(match[1])) : 0;
      }

      return timestamp(rightMeta) - timestamp(leftMeta);
    });

    cards.forEach(function (card) { grid.appendChild(card); });
  });
})();
