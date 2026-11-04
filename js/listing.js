/* Каталог: фильтрация по категории, цене, числу игроков, наличию, поиск и сортировка. */
(function () {
  'use strict';

  var grid = document.getElementById('product-grid');
  if (!grid) { return; }

  var items = Array.prototype.slice.call(grid.children);
  var form = document.getElementById('filters-form');
  var search = document.getElementById('filter-search');
  var catBoxes = Array.prototype.slice.call(form.querySelectorAll('input[name="cat"]'));
  var minInput = document.getElementById('price-min');
  var maxInput = document.getElementById('price-max');
  var playersSel = document.getElementById('filter-players');
  var stockBox = document.getElementById('filter-stock');
  var sortSel = document.getElementById('sort-select');
  var countEl = document.getElementById('catalog-count');
  var emptyEl = document.getElementById('catalog-empty');
  var panel = document.getElementById('filters-panel');
  var timer = null;

  function plural(n, forms) {
    var n10 = n % 10, n100 = n % 100;
    if (n10 === 1 && n100 !== 11) { return forms[0]; }
    if (n10 >= 2 && n10 <= 4 && (n100 < 12 || n100 > 14)) { return forms[1]; }
    return forms[2];
  }

  function num(v) {
    var n = parseFloat(v);
    return isNaN(n) ? null : n;
  }

  /* диапазон игроков для выбранного значения фильтра */
  function playersRange(v) {
    if (v === '1') { return [1, 1]; }
    if (v === '2') { return [2, 2]; }
    if (v === '3') { return [3, 4]; }
    if (v === '5') { return [5, 999]; }
    return null;
  }

  function matches(li, f) {
    var title = li.getAttribute('data-title');
    var price = Number(li.getAttribute('data-price'));
    if (f.q && title.indexOf(f.q) === -1) { return false; }
    if (f.cats.length && f.cats.indexOf(li.getAttribute('data-category')) === -1) { return false; }
    if (f.min !== null && price < f.min) { return false; }
    if (f.max !== null && price > f.max) { return false; }
    if (f.stock && li.getAttribute('data-stock') !== 'in') { return false; }
    if (f.range) {
      var pmin = li.getAttribute('data-players-min');
      if (pmin === null) { return false; } // аксессуары не имеют числа игроков
      if (!(Number(pmin) <= f.range[1] && Number(li.getAttribute('data-players-max')) >= f.range[0])) { return false; }
    }
    return true;
  }

  function sorters(kind) {
    if (kind === 'price-asc') { return function (a, b) { return a.price - b.price; }; }
    if (kind === 'price-desc') { return function (a, b) { return b.price - a.price; }; }
    if (kind === 'title') { return function (a, b) { return a.title.localeCompare(b.title, 'ru'); }; }
    return function (a, b) { return a.order - b.order; };
  }

  function readFilters() {
    return {
      q: search.value.trim().toLowerCase(),
      cats: catBoxes.filter(function (c) { return c.checked; }).map(function (c) { return c.value; }),
      min: num(minInput.value),
      max: num(maxInput.value),
      range: playersRange(playersSel.value),
      stock: stockBox.checked
    };
  }

  function syncUrl() {
    var params = new URLSearchParams();
    if (search.value.trim()) { params.set('q', search.value.trim()); }
    catBoxes.forEach(function (c) { if (c.checked) { params.append('cat', c.value); } });
    if (minInput.value) { params.set('min', minInput.value); }
    if (maxInput.value) { params.set('max', maxInput.value); }
    if (playersSel.value) { params.set('players', playersSel.value); }
    if (stockBox.checked) { params.set('stock', '1'); }
    if (sortSel.value !== 'default') { params.set('sort', sortSel.value); }
    var qs = params.toString();
    try {
      window.history.replaceState(null, '', window.location.pathname + (qs ? '?' + qs : ''));
    } catch (e) { /* file:// и т. п. — адрес не обновляем */ }
  }

  function apply(animate) {
    var f = readFilters();
    var visible = [];
    items.forEach(function (li) {
      var ok = matches(li, f);
      li.hidden = !ok;
      li.classList.remove('product-grid__item--enter');
      if (ok) { visible.push(li); }
    });

    // сортировка: переставляем узлы в нужном порядке
    var cmp = sorters(sortSel.value);
    var meta = function (li) {
      return { li: li, price: Number(li.getAttribute('data-price')), title: li.getAttribute('data-title'), order: Number(li.getAttribute('data-order')) };
    };
    items.map(meta).sort(function (a, b) { return cmp(a, b); }).forEach(function (m) { grid.appendChild(m.li); });

    if (animate) {
      visible = Array.prototype.slice.call(grid.children).filter(function (li) { return !li.hidden; });
      visible.forEach(function (li, i) {
        li.style.setProperty('--i', String(i));
        void li.offsetWidth;
        li.classList.add('product-grid__item--enter');
      });
    }

    var n = visible.length;
    countEl.textContent = 'Найдено: ' + n + ' ' + plural(n, ['товар', 'товара', 'товаров']);
    emptyEl.hidden = n !== 0;
    grid.hidden = n === 0;
    syncUrl();
  }

  function reset() {
    form.reset();
    search.value = '';
    sortSel.value = 'default';
    apply(true);
  }

  function restoreFromUrl() {
    var params = new URLSearchParams(window.location.search);
    search.value = params.get('q') || '';
    var cats = params.getAll('cat').concat((params.get('cats') || '').split(',')).filter(Boolean);
    catBoxes.forEach(function (c) { c.checked = cats.indexOf(c.value) !== -1; });
    minInput.value = params.get('min') || '';
    maxInput.value = params.get('max') || '';
    playersSel.value = params.get('players') || '';
    stockBox.checked = params.get('stock') === '1';
    sortSel.value = params.get('sort') || 'default';
    if (sortSel.value === '') { sortSel.value = 'default'; }
  }

  form.addEventListener('submit', function (e) { e.preventDefault(); apply(true); });
  form.addEventListener('input', function (e) {
    if (e.target === search || e.target === minInput || e.target === maxInput) {
      window.clearTimeout(timer);
      timer = window.setTimeout(function () { apply(true); }, 180);
    }
  });
  form.addEventListener('change', function (e) {
    if (e.target !== search && e.target !== minInput && e.target !== maxInput) { apply(true); }
  });
  sortSel.addEventListener('change', function () { apply(true); });
  document.getElementById('filters-reset').addEventListener('click', reset);
  document.getElementById('catalog-empty-reset').addEventListener('click', reset);

  // на широких экранах панель фильтров всегда раскрыта
  if (panel && window.matchMedia) {
    var mq = window.matchMedia('(min-width: 901px)');
    var sync = function () { if (mq.matches) { panel.open = true; } };
    sync();
    if (mq.addEventListener) { mq.addEventListener('change', sync); }
  }

  restoreFromUrl();
  apply(false);
})();
