/* Оформление заказа: сводка, способ получения, отправка формы. */
(function () {
  'use strict';

  var form = document.getElementById('checkout-form');
  if (!form || !window.BK) { return; }
  var BK = window.BK;
  var summary = document.getElementById('checkout-summary');
  var done = document.getElementById('checkout-done');
  var addressField = document.getElementById('address-field');
  var addressInput = document.getElementById('order-address');

  function delivery() {
    return form.querySelector('input[name="delivery"]:checked').value;
  }

  function renderSummary() {
    var cart = BK.getCart();
    var lines = BK.lines(cart);
    var sum = BK.subtotal(cart);
    var disc = BK.discount(sum);
    var after = sum - disc;
    var ship = 0;
    if (delivery() === 'courier') {
      ship = after >= BK.config.freeDeliveryFrom ? 0 : BK.config.deliveryPrice;
    }
    var rows = lines.map(function (l) {
      return '<li class="mini-list__item"><span>' + BK.escapeHtml(l.product.title) + ' × ' + l.qty +
        '</span><span class="mini-list__sum">' + BK.formatPrice(l.product.price * l.qty) + '</span></li>';
    }).join('');
    summary.innerHTML =
      '<div class="summary"><h2 class="summary__title">Ваш заказ</h2>' +
      '<ul class="mini-list">' + rows + '</ul>' +
      '<dl class="summary__rows">' +
      '<div class="summary__row"><dt>Товары</dt><dd>' + BK.formatPrice(sum) + '</dd></div>' +
      (disc ? '<div class="summary__row"><dt>Скидка по промокоду</dt><dd>−' + BK.formatPrice(disc) + '</dd></div>' : '') +
      '<div class="summary__row"><dt>Получение</dt><dd>' + (delivery() === 'courier' ? (ship ? BK.formatPrice(ship) : 'Бесплатно') : 'Самовывоз, бесплатно') + '</dd></div>' +
      '</dl>' +
      '<p class="summary__total"><span>К оплате</span><span class="summary__total-value">' + BK.formatPrice(after + ship) + '</span></p>' +
      '<p class="summary__note">Оплата при получении наличными или картой.</p>' +
      '<a class="link" href="cart.html">Изменить состав заказа</a></div>';
    return after + ship;
  }

  function toggleAddress() {
    var courier = delivery() === 'courier';
    addressField.hidden = !courier;
    addressInput.required = courier;
    if (!courier && window.BKForms) { window.BKForms.show(addressInput, ''); }
  }

  if (!BK.lines(BK.getCart()).length) {
    form.hidden = true;
    summary.hidden = true;
    done.hidden = false;
    done.querySelector('.checkout__done-title').textContent = 'Корзина пуста';
    document.getElementById('checkout-done-text').textContent = 'Добавьте товары в корзину, чтобы оформить заказ.';
    return;
  }

  form.addEventListener('change', function (e) {
    if (e.target.name === 'delivery') { toggleAddress(); renderSummary(); }
  });

  form.addEventListener('bk:valid', function () {
    var total = renderSummary();
    var number = 'БК-' + String(Date.now()).slice(-6);
    var name = form.elements.name.value.trim();
    var text = name + ', ваш заказ ' + number + ' на сумму ' + BK.formatPrice(total) +
      ' принят. Мы позвоним по номеру ' + form.elements.phone.value + ', чтобы подтвердить детали.' +
      (form.elements.table.checked ? ' Стол в игровой зоне забронируем по вашему заказу.' : '');
    document.getElementById('checkout-done-text').textContent = text;
    BK.setCart({}, false);
    BK.setPromo('');
    form.hidden = true;
    summary.hidden = true;
    done.hidden = false;
    done.focus();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  toggleAddress();
  renderSummary();
})();
