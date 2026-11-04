/* Страница корзины: список позиций, количество, удаление, промокод, итог. */
(function () {
  'use strict';

  var root = document.getElementById('cart-root');
  if (!root || !window.BK) { return; }
  var BK = window.BK;
  var focusKey = null;

  function render() {
    var cart = BK.getCart();
    var lines = BK.lines(cart);

    if (!lines.length) {
      root.innerHTML =
        '<div class="cart-empty">' +
        '<h2 class="cart-empty__title">В корзине пока пусто</h2>' +
        '<p class="cart-empty__text">Выберите игру в каталоге — а чтобы не ошибиться с выбором, сначала попробуйте её в нашей игровой зоне.</p>' +
        '<a class="btn btn--primary btn--large" href="catalog.html">Перейти в каталог</a>' +
        '</div>';
      return;
    }

    var sum = BK.subtotal(cart);
    var disc = BK.discount(sum);
    var total = sum - disc;
    var count = BK.countItems(cart);
    var left = BK.config.freeDeliveryFrom - sum;
    var percent = Math.min(100, Math.round(sum / BK.config.freeDeliveryFrom * 100));
    var promo = BK.getPromo();

    var items = lines.map(function (l) {
      var p = l.product;
      var t = BK.escapeHtml(p.title);
      return '<li class="cart-item" data-slug="' + p.slug + '">' +
        '<a href="' + p.url + '"><img class="cart-item__image" src="' + p.image + '" alt="" width="120" height="90"></a>' +
        '<div class="cart-item__info">' +
        '<h2 class="cart-item__title"><a class="cart-item__link" href="' + p.url + '">' + t + '</a></h2>' +
        '<p class="cart-item__price">' + BK.formatPrice(p.price) + ' за штуку</p></div>' +
        '<div class="quantity" data-quantity>' +
        '<button class="quantity__button" type="button" data-cart-minus="' + p.slug + '" aria-label="Уменьшить количество: ' + t + '">−</button>' +
        '<input class="quantity__input" type="number" min="1" max="' + BK.maxQty + '" value="' + l.qty + '" inputmode="numeric" data-cart-qty="' + p.slug + '" aria-label="Количество: ' + t + '">' +
        '<button class="quantity__button" type="button" data-cart-plus="' + p.slug + '" aria-label="Увеличить количество: ' + t + '">+</button></div>' +
        '<p class="cart-item__sum">' + BK.formatPrice(p.price * l.qty) + '</p>' +
        '<button class="cart-item__remove" type="button" data-cart-remove="' + p.slug + '">Удалить</button>' +
        '</li>';
    }).join('');

    var progress = left > 0
      ? 'До бесплатной доставки по Владимиру осталось <strong>' + BK.formatPrice(left) + '</strong>'
      : 'Доставка по Владимиру для вашего заказа <strong>бесплатная</strong>';

    var promoMsg = promo
      ? '<p class="promo__message promo__message--ok" id="promo-message">Промокод ' + promo + ' применён: скидка ' + BK.config.promoPercent + '%</p>'
      : '<p class="promo__message" id="promo-message"></p>';

    root.innerHTML =
      '<div class="cart__main"><ul class="cart-list">' + items + '</ul>' +
      '<div class="cart__actions">' +
      '<a class="btn btn--outline" href="listing.html">Продолжить покупки</a>' +
      '<button class="btn btn--outline btn--small" type="button" data-cart-clear>Очистить корзину</button></div></div>' +
      '<aside class="summary" aria-label="Итог заказа">' +
      '<h2 class="summary__title">Ваш заказ</h2>' +
      '<div class="progress"><p class="progress__text">' + progress + '</p>' +
      '<div class="progress__track" aria-hidden="true"><div class="progress__bar" style="width:' + percent + '%"></div></div></div>' +
      '<dl class="summary__rows">' +
      '<div class="summary__row"><dt>Товары (' + count + ')</dt><dd>' + BK.formatPrice(sum) + '</dd></div>' +
      (disc ? '<div class="summary__row"><dt>Скидка по промокоду</dt><dd>−' + BK.formatPrice(disc) + '</dd></div>' : '') +
      '</dl>' +
      '<div class="promo"><label class="field__label" for="promo-input">Промокод</label>' +
      '<div class="promo__row"><input class="input" id="promo-input" type="text" autocomplete="off" placeholder="Введите промокод" value="' + (promo || '') + '">' +
      '<button class="btn btn--outline btn--small" type="button" data-promo-apply>Применить</button></div>' + promoMsg + '</div>' +
      '<p class="summary__total"><span>Итого</span><span class="summary__total-value">' + BK.formatPrice(total) + '</span></p>' +
      '<a class="btn btn--primary btn--large" href="checkout.html">Оформить заказ</a>' +
      '<p class="summary__note">Способ получения и стоимость доставки выбираются на следующем шаге.</p>' +
      '</aside>';

    if (focusKey) {
      var el = root.querySelector('[' + focusKey + ']');
      if (el) { el.focus(); }
      focusKey = null;
    }
  }

  function setQty(slug, qty) {
    var cart = BK.getCart();
    if (qty < 1) { delete cart[slug]; } else { cart[slug] = Math.min(BK.maxQty, qty); }
    BK.setCart(cart, false);
  }

  root.addEventListener('click', function (e) {
    var t = e.target.closest('button');
    if (!t) { return; }
    var cart = BK.getCart();
    var slug;
    if ((slug = t.getAttribute('data-cart-minus'))) {
      setQty(slug, (cart[slug] || 1) - 1);
      focusKey = cart[slug] > 1 ? 'data-cart-minus="' + slug + '"' : null;
      render();
    } else if ((slug = t.getAttribute('data-cart-plus'))) {
      setQty(slug, (cart[slug] || 0) + 1);
      focusKey = 'data-cart-plus="' + slug + '"';
      render();
    } else if ((slug = t.getAttribute('data-cart-remove'))) {
      setQty(slug, 0);
      render();
      BK.toast('Товар удалён из корзины');
    } else if (t.hasAttribute('data-cart-clear')) {
      BK.setCart({}, false);
      render();
    } else if (t.hasAttribute('data-promo-apply')) {
      var code = root.querySelector('#promo-input').value.trim().toUpperCase();
      if (code === BK.config.promoCode) {
        BK.setPromo(code);
        render();
      } else {
        var msg = root.querySelector('#promo-message');
        msg.className = 'promo__message promo__message--error';
        msg.textContent = code ? 'Такого промокода нет. Проверьте написание.' : 'Введите промокод.';
      }
    }
  });

  root.addEventListener('change', function (e) {
    var input = e.target.closest('[data-cart-qty]');
    if (input) {
      var v = parseInt(input.value, 10);
      setQty(input.getAttribute('data-cart-qty'), isNaN(v) ? 1 : v);
      focusKey = 'data-cart-qty="' + input.getAttribute('data-cart-qty') + '"';
      render();
    }
  });

  render();
})();
