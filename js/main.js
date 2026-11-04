/* Брось кубик — общее ядро: корзина (localStorage), шапка, уведомления.
   Чистый JavaScript, без библиотек. */
(function () {
  'use strict';

  var CART_KEY = 'bk-cart';
  var PROMO_KEY = 'bk-promo';
  var MAX_QTY = 20;
  var products = window.BK_PRODUCTS || [];
  var config = window.BK_CONFIG || { deliveryPrice: 300, freeDeliveryFrom: 5000, promoCode: 'КУБИК10', promoPercent: 10 };

  var bySlug = {};
  products.forEach(function (p) { bySlug[p.slug] = p; });

  /* ---------- хранилище ---------- */
  function read(key, fallback) {
    try {
      var raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function write(key, value) {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (e) { /* хранилище недоступно — работаем без сохранения */ }
  }

  function getCart() {
    var raw = read(CART_KEY, {});
    var clean = {};
    Object.keys(raw || {}).forEach(function (slug) {
      var qty = parseInt(raw[slug], 10);
      if (bySlug[slug] && qty > 0) { clean[slug] = Math.min(qty, MAX_QTY); }
    });
    return clean;
  }

  function countItems(cart) {
    return Object.keys(cart).reduce(function (sum, slug) { return sum + cart[slug]; }, 0);
  }

  function updateCount(bump) {
    var total = countItems(getCart());
    var nodes = document.querySelectorAll('[data-cart-count]');
    Array.prototype.forEach.call(nodes, function (node) {
      node.textContent = String(total);
      node.setAttribute('data-empty', total === 0 ? 'true' : 'false');
      if (bump) {
        node.classList.remove('cart-link__count--bump');
        void node.offsetWidth; // перезапуск анимации
        node.classList.add('cart-link__count--bump');
      }
    });
  }

  function setCart(cart, bump) {
    write(CART_KEY, cart);
    updateCount(bump);
  }

  function lines(cart) {
    return Object.keys(cart).map(function (slug) {
      return { product: bySlug[slug], qty: cart[slug] };
    }).filter(function (l) { return l.product; });
  }

  function subtotal(cart) {
    return lines(cart).reduce(function (sum, l) { return sum + l.product.price * l.qty; }, 0);
  }

  function getPromo() { return read(PROMO_KEY, '') === config.promoCode ? config.promoCode : ''; }
  function setPromo(code) { write(PROMO_KEY, code); }

  function discount(sum) {
    return getPromo() ? Math.round(sum * config.promoPercent / 100) : 0;
  }

  function formatPrice(n) {
    return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '\u00a0') + '\u00a0₽';
  }

  function plural(n, forms) {
    var n10 = n % 10, n100 = n % 100;
    if (n10 === 1 && n100 !== 11) { return forms[0]; }
    if (n10 >= 2 && n10 <= 4 && (n100 < 12 || n100 > 14)) { return forms[1]; }
    return forms[2];
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* ---------- уведомления ---------- */
  function toast(text, linkHref, linkText) {
    var region = document.getElementById('toast-region');
    if (!region) { return; }
    var el = document.createElement('div');
    el.className = 'toast';
    var span = document.createElement('span');
    span.textContent = text;
    el.appendChild(span);
    if (linkHref) {
      var a = document.createElement('a');
      a.className = 'toast__link link';
      a.href = linkHref;
      a.textContent = linkText;
      el.appendChild(a);
    }
    region.appendChild(el);
    window.setTimeout(function () {
      el.classList.add('toast--leaving');
      el.addEventListener('animationend', function () { el.remove(); });
      window.setTimeout(function () { el.remove(); }, 600);
    }, 3800);
  }

  /* ---------- добавление в корзину ---------- */
  function addToCart(slug, qty) {
    if (!bySlug[slug]) { return; }
    var cart = getCart();
    cart[slug] = Math.min(MAX_QTY, (cart[slug] || 0) + qty);
    setCart(cart, true);
    toast('Добавлено: ' + bySlug[slug].title, 'cart.html', 'В корзину');
  }

  document.addEventListener('click', function (event) {
    var addBtn = event.target.closest('[data-add-to-cart]');
    if (addBtn) {
      var qty = 1;
      var sel = addBtn.getAttribute('data-qty-source');
      if (sel) {
        var input = document.querySelector(sel);
        qty = Math.max(1, Math.min(MAX_QTY, parseInt(input && input.value, 10) || 1));
      }
      addToCart(addBtn.getAttribute('data-add-to-cart'), qty);
      var original = addBtn.getAttribute('data-label') || addBtn.textContent;
      addBtn.setAttribute('data-label', original);
      addBtn.textContent = 'Добавлено';
      addBtn.classList.remove('btn--added');
      void addBtn.offsetWidth;
      addBtn.classList.add('btn--added');
      window.setTimeout(function () {
        addBtn.textContent = original;
        addBtn.classList.remove('btn--added');
      }, 1400);
      return;
    }

    var stepBtn = event.target.closest('[data-qty-minus], [data-qty-plus]');
    if (stepBtn) {
      var box = stepBtn.closest('[data-quantity]');
      var field = box && box.querySelector('input');
      if (!field) { return; }
      var value = parseInt(field.value, 10) || 1;
      value += stepBtn.hasAttribute('data-qty-plus') ? 1 : -1;
      field.value = String(Math.max(1, Math.min(MAX_QTY, value)));
    }
  });

  document.addEventListener('change', function (event) {
    var input = event.target.closest('[data-quantity] input');
    if (input) {
      var v = parseInt(input.value, 10);
      input.value = String(isNaN(v) ? 1 : Math.max(1, Math.min(MAX_QTY, v)));
    }
  });

  /* ---------- меню на мобильных ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('main-nav--open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('main-nav--open')) {
        nav.classList.remove('main-nav--open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* ---------- публичный интерфейс для страниц ---------- */
  window.BK = {
    config: config,
    maxQty: MAX_QTY,
    getCart: getCart,
    setCart: setCart,
    lines: lines,
    subtotal: subtotal,
    countItems: countItems,
    getPromo: getPromo,
    setPromo: setPromo,
    discount: discount,
    formatPrice: formatPrice,
    plural: plural,
    escapeHtml: escapeHtml,
    toast: toast
  };

  updateCount(false);
})();
