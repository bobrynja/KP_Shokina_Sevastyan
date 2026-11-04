/* Страница контактов: подстановка темы из адреса и сообщение об успешной отправке. */
(function () {
  'use strict';

  var form = document.getElementById('feedback-form');
  if (!form) { return; }
  var done = document.getElementById('feedback-done');
  var topic = document.getElementById('fb-topic');

  var wanted = new URLSearchParams(window.location.search).get('topic');
  if (wanted && topic.querySelector('option[value="' + wanted + '"]')) {
    topic.value = wanted;
  }

  form.addEventListener('bk:valid', function () {
    form.hidden = true;
    done.hidden = false;
    done.focus();
  });

  document.getElementById('feedback-again').addEventListener('click', function () {
    form.reset();
    done.hidden = true;
    form.hidden = false;
    document.getElementById('fb-name').focus();
  });
})();
