/* Валидация форм (Vanilla JS): понятные сообщения об ошибках, маска телефона. */
(function () {
  'use strict';

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function message(el, key, fallback) {
    return el.getAttribute('data-' + key) || fallback;
  }

  /* Возвращает текст ошибки или пустую строку */
  function check(el) {
    if (el.disabled || el.closest('[hidden]')) { return ''; }
    var value = (el.value || '').trim();

    if (el.type === 'checkbox') {
      return el.required && !el.checked ? message(el, 'msg-required', 'Поставьте галочку, чтобы продолжить') : '';
    }
    if (el.required && !value) {
      return message(el, 'msg-required', 'Заполните это поле');
    }
    if (!value) { return ''; }

    if (el.type === 'email' && !EMAIL_RE.test(value)) {
      return message(el, 'msg-invalid', 'Введите e-mail в формате name@mail.ru');
    }
    if (el.hasAttribute('data-phone')) {
      var digits = value.replace(/\D/g, '');
      var okChars = /^[+\d\s()\-]+$/.test(value);
      var okLen = digits.length === 10 || (digits.length === 11 && (digits[0] === '7' || digits[0] === '8'));
      if (!okChars || !okLen) {
        return message(el, 'msg-invalid', 'Введите телефон в формате +7 (999) 123-45-67');
      }
    }
    var min = parseInt(el.getAttribute('minlength') || '0', 10);
    if (min && value.length < min) {
      return message(el, 'msg-short', 'Слишком коротко: минимум ' + min + ' символов');
    }
    return '';
  }

  function show(el, text) {
    var wrap = el.closest('.field');
    var err = document.getElementById(el.id + '-error');
    if (!wrap || !err) { return; }
    if (text) {
      var wasInvalid = wrap.classList.contains('field--invalid');
      err.textContent = text;
      err.hidden = false;
      el.setAttribute('aria-invalid', 'true');
      el.setAttribute('aria-describedby', err.id);
      wrap.classList.add('field--invalid');
      if (!wasInvalid) { void wrap.offsetWidth; }
    } else {
      err.textContent = '';
      err.hidden = true;
      el.removeAttribute('aria-invalid');
      el.removeAttribute('aria-describedby');
      wrap.classList.remove('field--invalid');
    }
  }

  function controls(form) {
    return Array.prototype.slice.call(form.querySelectorAll('.field__control'));
  }

  function validateAll(form) {
    var firstBad = null;
    var bad = 0;
    controls(form).forEach(function (el) {
      var text = check(el);
      show(el, text);
      if (text) { bad += 1; if (!firstBad) { firstBad = el; } }
    });
    var summary = form.querySelector('.form__summary');
    if (summary) {
      if (bad) {
        summary.textContent = 'Не удалось отправить: исправьте ' + bad + ' ' +
          (bad === 1 ? 'поле' : (bad < 5 ? 'поля' : 'полей')) + ' в форме.';
        summary.hidden = false;
      } else {
        summary.hidden = true;
      }
    }
    return firstBad;
  }

  /* маска телефона: +7 (999) 123-45-67 */
  function formatPhone(raw) {
    var d = raw.replace(/\D/g, '');
    if (!d) { return ''; }
    if (d[0] === '8') { d = '7' + d.slice(1); }
    if (d[0] !== '7') { d = '7' + d; }
    d = d.slice(0, 11);
    var out = '+7';
    if (d.length > 1) { out += ' (' + d.slice(1, 4); }
    if (d.length >= 4) { out += ')'; }
    if (d.length > 4) { out += ' ' + d.slice(4, 7); }
    if (d.length > 7) { out += '-' + d.slice(7, 9); }
    if (d.length > 9) { out += '-' + d.slice(9, 11); }
    return out;
  }

  Array.prototype.forEach.call(document.querySelectorAll('form.form'), function (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var bad = validateAll(form);
      if (bad) {
        bad.focus();
        return;
      }
      form.dispatchEvent(new CustomEvent('bk:valid', { bubbles: true }));
    });

    form.addEventListener('focusout', function (event) {
      var el = event.target;
      if (el.classList && el.classList.contains('field__control') && (el.value || el.closest('.field--invalid'))) {
        show(el, check(el));
      }
    });

    form.addEventListener('input', function (event) {
      var el = event.target;
      if (!el.classList || !el.classList.contains('field__control')) { return; }
      if (el.hasAttribute('data-phone') && (event.inputType || '').indexOf('delete') !== 0) {
        el.value = formatPhone(el.value);
      }
      if (el.closest('.field--invalid')) { show(el, check(el)); }
    });

    form.addEventListener('change', function (event) {
      var el = event.target;
      if (el.classList && el.classList.contains('field__control') && (el.type === 'checkbox' || el.tagName === 'SELECT')) {
        show(el, check(el));
      }
    });
  });

  window.BKForms = { check: check, show: show, validateAll: validateAll };
})();
