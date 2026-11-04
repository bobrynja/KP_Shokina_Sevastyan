# -*- coding: utf-8 -*-
"""Сборка статического сайта «Брось кубик»: данные -> HTML-страницы + js/data.js."""
import html
import json
import os
from urllib.parse import quote

import art

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape


def nb(n):
    return f'{n:,}'.replace(',', '\u00a0')


def money(n):
    return nb(n) + '\u00a0₽'


# ======================= ДАННЫЕ =======================
CATEGORIES = [
    dict(id='strategy', title='Стратегии и экономические игры', short='Стратегии',
         desc='Глубокие партии для тех, кто любит планировать, развивать и побеждать продуманным ходом.', art='wingspan'),
    dict(id='family', title='Семейные и детские игры', short='Семейные и детские',
         desc='Простые правила и короткие партии: садитесь за стол всей семьёй.', art='carcassonne'),
    dict(id='party', title='Игры для вечеринок (Party Games)', short='Вечеринки',
         desc='Смех, ассоциации и динамика для большой компании.', art='imaginarium'),
    dict(id='ccg', title='Коллекционные карточные игры (ККИ) и варгеймы', short='ККИ и варгеймы',
         desc='Стартовые наборы Magic: The Gathering и командные стартеры Warhammer 40,000.', art='mtg-starter'),
    dict(id='accessories', title='Аксессуары для настольных игр', short='Аксессуары',
         desc='Металлические дайсы, органайзеры и вставки в коробки для долгой сохранности коллекции.', art='metal-dice'),
]
CAT = {c['id']: c for c in CATEGORIES}

PRODUCTS = [
    dict(slug='wingspan', title='Крылья (Wingspan)', cat='strategy', price=4990, pmin=1, pmax=5, stock='in', badge='Хит',
         short='Красивая и глубокая игра про птиц: стройте заповедник и развивайте движок действий.',
         card=[('Игроков', '1–5'), ('Время', '40–70 мин')],
         specs=[('Игроков', '1–5'), ('Возраст', '10+'), ('Время партии', '40–70 минут'), ('Сложность', 'Средняя'),
                ('Жанр', 'Стратегия, коллекционирование карт'), ('Язык правил', 'Русский')],
         long=['В «Крыльях» вы — любитель птиц, который привлекает в свой заповедник лучших представителей пернатых. '
               'Каждая карта птицы даёт новое действие, а из них постепенно складывается ваш собственный «движок».',
               'Красивые иллюстрации превращают партию в удовольствие, а правила осваиваются за 15 минут. '
               'Подходит и новичкам, и опытным игрокам; есть режим для одного игрока.']),
    dict(slug='stone-age', title='Каменный век (Stone Age)', cat='strategy', price=2790, pmin=2, pmax=4, stock='in', badge=None,
         short='Классическая экономическая стратегия: добывайте ресурсы, стройте и развивайте племя.',
         card=[('Игроков', '2–4'), ('Время', '60–90 мин')],
         specs=[('Игроков', '2–4'), ('Возраст', '10+'), ('Время партии', '60–90 минут'), ('Сложность', 'Средняя'),
                ('Механика', 'Размещение рабочих'), ('Язык правил', 'Русский')],
         long=['Вы управляете племенем первобытных людей: отправляете соплеменников добывать дерево, камень, глину и золото, '
               'охотиться, строить хижины и развивать земледелие.',
               'Удача с кубиками здесь смягчается разумным планированием, поэтому игра отлично подходит как первая «настоящая» '
               'экономическая стратегия.']),
    dict(slug='carcassonne', title='Каркассон (Carcassonne)', cat='family', price=1890, pmin=2, pmax=5, stock='in', badge='Хит',
         short='Культовая игра в жанре тайл-плейсмент: выкладывайте плитки и стройте средневековый пейзаж.',
         card=[('Игроков', '2–5'), ('Время', '30–45 мин')],
         specs=[('Игроков', '2–5'), ('Возраст', '7+'), ('Время партии', '30–45 минут'), ('Сложность', 'Низкая'),
                ('Механика', 'Выкладывание тайлов'), ('Язык правил', 'Русский')],
         long=['Каждый ход вы берёте плитку местности и добавляете её к общему полю: так появляются города, дороги, '
               'монастыри и поля. Подданных можно ставить на постройки, чтобы получать очки.',
               'Правила объясняются за пять минут, а партии всегда разные — игра подойдёт и детям, и взрослым.']),
    dict(slug='dobble', title='Доббль (Dobble)', cat='family', price=990, pmin=2, pmax=8, stock='in', badge=None,
         short='Игра на внимательность: найдите одинаковый символ на двух картах быстрее соперников.',
         card=[('Игроков', '2–8'), ('Время', '15 мин')],
         specs=[('Игроков', '2–8'), ('Возраст', '6+'), ('Время партии', '15 минут'), ('Сложность', 'Низкая'),
                ('Состав', '55 круглых карт'), ('Тип', 'Игра на внимательность и скорость')],
         long=['У любых двух карт ровно один общий символ. Ваша задача — заметить его раньше остальных, '
               'назвать и избавиться от карты.',
               'В коробке несколько мини-игр, поэтому набор удобно брать с собой в поездку или на дачу.']),
    dict(slug='imaginarium', title='Имаджинариум', cat='party', price=2490, pmin=3, pmax=98, stock='in', badge='Хит',
         short='Ассоциации по красивым иллюстрациям: загадывайте так, чтобы поняли не все.',
         card=[('Игроков', 'от 3'), ('Время', '30–60 мин')],
         specs=[('Игроков', 'от 3'), ('Возраст', '8+'), ('Время партии', '30–60 минут'), ('Сложность', 'Низкая'),
                ('Жанр', 'Ассоциации'), ('Язык правил', 'Русский')],
         long=['Ведущий придумывает ассоциацию к своей карте, остальные подбирают карты из руки, а потом все угадывают, '
               'какая карта чья. Секрет в том, чтобы быть понятным, но не слишком.',
               'Необычные иллюстрации рождают самые неожиданные истории — игра отлично «разогревает» компанию.']),
    dict(slug='exploding-kittens', title='Взрывные котята (Exploding Kittens)', cat='party', price=1590, pmin=2, pmax=5,
         stock='in', badge='Хит', short='Динамичная карточная игра с юмором: не вытяните карту с взрывным котёнком.',
         card=[('Игроков', '2–5'), ('Время', '15 мин')],
         specs=[('Игроков', '2–5'), ('Возраст', '7+'), ('Время партии', '15 минут'), ('Сложность', 'Низкая'),
                ('Состав', '56 карт'), ('Жанр', 'Карточная игра, юмор')],
         long=['Игроки по очереди тянут карты, пока кто-то не вытащит взрывного котёнка. Спастись помогают карты действий: '
               'пропустить ход, подсмотреть колоду, подставить соперника.',
               'Партия длится около 15 минут, поэтому в неё удобно играть «на один раз» перед основной игрой вечера.']),
    dict(slug='mtg-starter', title='Magic: The Gathering — Starter Kit', cat='ccg', price=1990, pmin=2, pmax=2, stock='in',
         badge=None, short='Стартовый набор с готовыми колодами для двоих: откройте коробку и начните играть.',
         card=[('Игроков', '2'), ('Состав', '2 колоды')],
         specs=[('Игроков', '2'), ('Возраст', '13+'), ('Время партии', '30–60 минут'), ('Сложность', 'Средняя'),
                ('Состав', 'Готовые колоды для двух игроков'), ('Тип', 'Коллекционная карточная игра')],
         long=['Starter Kit создан для знакомства с Magic: в наборе готовые колоды, поэтому не нужно собирать их самостоятельно.',
               'Мы охотно проведём короткое обучение в игровой зоне — приходите вдвоём и сыграйте первую партию бесплатно.']),
    dict(slug='warhammer-starter', title='Warhammer 40,000 — командный стартер', cat='ccg', price=6990, pmin=2, pmax=2,
         stock='order', badge='Под заказ',
         short='Стартовый набор миниатюр для знакомства с варгеймом: соберите и раскрасьте свою армию.',
         card=[('Игроков', '2'), ('Тип', 'Варгейм')],
         specs=[('Игроков', '2'), ('Возраст', '12+'), ('Время партии', 'от 60 минут'), ('Сложность', 'Высокая'),
                ('Состав', 'Миниатюры для сборки и покраски'), ('Тип', 'Настольный варгейм')],
         long=['Командный стартер — быстрый способ собрать первую армию и сыграть в Warhammer 40,000. '
               'Миниатюры собираются и раскрашиваются самостоятельно, это отдельное увлечение.',
               'Позиция доступна под заказ: срок поставки уточняйте у консультанта.']),
    dict(slug='metal-dice', title='Набор металлических дайсов (d20, d12, d10, d8, d6, d4)', cat='accessories', price=1290,
         pmin=None, pmax=None, stock='in', badge=None,
         short='Шесть металлических кубиков с гравировкой для D&D и других ролевых игр.',
         card=[('Материал', 'Металл'), ('Комплект', '6 дайсов')],
         specs=[('Материал', 'Металл'), ('Комплект', '6 дайсов: d20, d12, d10, d8, d6, d4'), ('Гравировка', 'Есть'),
                ('Применение', 'D&D и другие ролевые игры')],
         long=['Тяжёлые металлические дайсы с чёткой гравировкой: приятно держать в руке, и результат броска всегда легко прочитать.',
               'Набор подойдёт для ролевых и настольных игр, где нужны многогранные кубики.']),
    dict(slug='box-organizer', title='Органайзер-вставка для коробки', cat='accessories', price=1490, pmin=None, pmax=None,
         stock='in', badge=None,
         short='Вставка с отсеками: компоненты лежат по местам, а коробка не превращается в кучу.',
         card=[('Материал', 'Вспененный полимер'), ('Сборка', 'Без клея')],
         specs=[('Материал', 'Вспененный полимер'), ('Назначение', 'Хранение компонентов в коробке'),
                ('Совместимость', 'Популярные стратегические игры'), ('Сборка', 'Без клея')],
         long=['Органайзер делит коробку на отсеки для карт, жетонов и фишек, поэтому подготовка к игре занимает минуты, а не полвечера.',
               'Консультанты подскажут, какая вставка подходит именно к вашей игре. Маппинги для популярных стратегий — по запросу.']),
]
P = {p['slug']: p for p in PRODUCTS}
for i, p in enumerate(PRODUCTS):
    p['order'] = i
    p['url'] = f"product-{p['slug']}.html"
    p['image'] = f"img/{p['slug']}.svg"

EVENTS = [
    dict(date='2026-11-04', day='4', month='ноября', wd='среда', time='19:00', title='Мастер-класс по игре «Крылья»',
         text='Разберём правила и стратегии за 15 минут и сыграем пробную партию. Вход бесплатный.'),
    dict(date='2026-11-07', day='7', month='ноября', wd='суббота', time='18:00', title='Турнир по «Каркассону»',
         text='Играем по швейцарской системе. Призовой фонд и пицца для финалистов.'),
    dict(date='2026-11-14', day='14', month='ноября', wd='суббота', time='21:00', title='Ночной турнир Magic: The Gathering',
         text='Формат — стартовые колоды. Приходите с друзьями или найдите соперника на месте. Нужна запись.'),
    dict(date='2026-11-18', day='18', month='ноября', wd='среда', time='19:00', title='Мастер-класс по «Каменному веку»',
         text='Знакомимся с экономическими стратегиями: ресурсы, рабочие и стройка племени.'),
    dict(date='2026-11-21', day='21', month='ноября', wd='суббота', time='15:00', title='Семейный день: «Доббль» и «Каркассон»',
         text='Играем всей семьёй, консультанты помогут выбрать игру для детей разного возраста.'),
    dict(date='2026-11-28', day='28', month='ноября', wd='суббота', time='18:00', title='Вечер Party-игр',
         text='«Имаджинариум», «Взрывные котята» и другие игры для большой компании.'),
]

NAV = [('index.html', 'Главная', 'home'), ('catalog.html', 'Каталог', 'catalog'), ('events.html', 'Афиша', 'events'),
       ('delivery.html', 'Доставка и оплата', 'delivery'), ('about.html', 'О нас', 'about'),
       ('contacts.html', 'Контакты', 'contacts')]

PHONE_TEXT = '+7 (999) 123-45-67'
PHONE_HREF = 'tel:+79991234567'
EMAIL = 'info@broskubik.ru'
VK = 'https://vk.com/broskubik'
TG = 'https://t.me/broskubik_news'
ADDRESS = 'г. Владимир, ул. Тракторная, д. 20'
MAP_URL = 'https://yandex.ru/maps/?text=' + quote('Владимир, ул. Тракторная, 20')


# ======================= ШАБЛОНЫ =======================
def head(title, desc, body_class):
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#F5B81C">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@500;700;800&amp;display=swap">
<link rel="stylesheet" href="css/style.css">
</head>
<body class="page {body_class}">
<a class="skip-link" href="#main">Перейти к содержимому</a>
'''


def header(active):
    items = ''
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ''
        items += f'      <li class="main-nav__item"><a class="main-nav__link" href="{href}"{cur}>{label}</a></li>\n'
    return f'''<header class="site-header">
  <div class="site-header__topbar">
    <div class="container site-header__topbar-inner">
      <p class="site-header__note">Игровая зона бесплатна: попробуйте любую игру до покупки</p>
      <ul class="site-header__contacts">
        <li><a class="site-header__contact-link" href="{PHONE_HREF}">{PHONE_TEXT}</a></li>
        <li><a class="site-header__contact-link" href="mailto:{EMAIL}">{EMAIL}</a></li>
      </ul>
    </div>
  </div>
  <div class="container site-header__bar">
    <a class="site-header__logo" href="index.html"><img class="site-header__logo-image" src="img/logo.png" alt="Брось кубик — на главную" width="144" height="44"></a>
    <form class="site-search" action="listing.html" method="get" role="search">
      <label class="visually-hidden" for="site-search-input">Поиск по каталогу</label>
      <input class="site-search__input" id="site-search-input" type="search" name="q" placeholder="Найти игру или аксессуар" autocomplete="off">
      <button class="site-search__button" type="submit">Найти</button>
    </form>
    <a class="btn btn--outline btn--small site-header__booking" href="contacts.html?topic=table#feedback">Забронировать стол</a>
    <a class="cart-link" href="cart.html" aria-label="Корзина">
      <svg class="cart-link__icon" viewBox="0 0 32 32" width="30" height="30" aria-hidden="true"><path d="M3 5h4l3 14h14l3-10H8" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="25" r="2.4" fill="currentColor"/><circle cx="22" cy="25" r="2.4" fill="currentColor"/></svg>
      <span class="cart-link__label">Корзина</span>
      <span class="cart-link__count" data-cart-count>0</span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav"><span class="nav-toggle__bars" aria-hidden="true"></span><span class="nav-toggle__text">Меню</span></button>
  </div>
  <nav class="main-nav" id="main-nav" aria-label="Основное меню">
    <ul class="container main-nav__list">
{items}    </ul>
  </nav>
</header>
'''


def footer():
    cat_links = ''.join(f'<li><a class="site-footer__link" href="listing.html?cat={c["id"]}">{E(c["short"])}</a></li>' for c in CATEGORIES)
    shop = ''.join(f'<li><a class="site-footer__link" href="{h}">{l}</a></li>' for h, l, k in NAV if k != 'home') 
    return f'''<footer class="site-footer">
  <div class="container site-footer__grid">
    <div class="site-footer__brand">
      <a class="site-footer__logo" href="index.html"><img src="img/logo-light.png" alt="Брось кубик" width="144" height="44" loading="lazy"></a>
      <p class="site-footer__about">Магазин настольных игр во Владимире. Играем вместе с 2018 года.</p>
    </div>
    <nav class="site-footer__col" aria-labelledby="footer-catalog">
      <h2 class="site-footer__title" id="footer-catalog">Каталог</h2>
      <ul class="site-footer__list">{cat_links}</ul>
    </nav>
    <nav class="site-footer__col" aria-labelledby="footer-shop">
      <h2 class="site-footer__title" id="footer-shop">Магазин</h2>
      <ul class="site-footer__list">{shop}<li><a class="site-footer__link" href="cart.html">Корзина</a></li></ul>
    </nav>
    <div class="site-footer__col">
      <h2 class="site-footer__title">Контакты</h2>
      <address class="site-footer__address">
        <p class="site-footer__text">{ADDRESS}</p>
        <p class="site-footer__text"><a class="site-footer__link" href="{PHONE_HREF}">{PHONE_TEXT}</a></p>
        <p class="site-footer__text"><a class="site-footer__link" href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p class="site-footer__text">Пн–Вс с 11:00 до 22:00</p>
      </address>
    </div>
    <div class="site-footer__col">
      <h2 class="site-footer__title">Мы в соцсетях</h2>
      <ul class="site-footer__social">
        <li><a class="social-link" href="{VK}" target="_blank" rel="noopener noreferrer">ВКонтакте</a></li>
        <li><a class="social-link" href="{TG}" target="_blank" rel="noopener noreferrer">Telegram</a></li>
      </ul>
    </div>
  </div>
  <div class="container site-footer__bottom">
    <p class="site-footer__copy">© 2026 ООО «Брось кубик». Все права защищены.</p>
    <p class="site-footer__copy">Разработчики: Шокина А. Н., Севастьян М. И. (гр. ПИ-124)</p>
  </div>
</footer>
'''


def page(fname, title, desc, body_class, active, main, scripts=()):
    scripts = ['data.js'] + [s for s in scripts if s != 'data.js']
    scr = '\n'.join(f'<script src="js/{s}" defer></script>' for s in scripts)
    out = head(title, desc, body_class) + header(active) + f'<main id="main">\n{main}</main>\n' + footer()
    out += f'<div class="toast-region" id="toast-region" role="status" aria-live="polite"></div>\n{scr}\n</body>\n</html>\n'
    with open(os.path.join(ROOT, fname), 'w', encoding='utf8') as f:
        f.write(out)


def breadcrumbs(items):
    lis = ''
    for i, (href, label) in enumerate(items):
        if i < len(items) - 1:
            lis += f'<li class="breadcrumbs__item"><a class="breadcrumbs__link" href="{href}">{E(label)}</a></li>'
        else:
            lis += f'<li class="breadcrumbs__item" aria-current="page">{E(label)}</li>'
    return f'<nav class="breadcrumbs" aria-label="Хлебные крошки"><ol class="breadcrumbs__list">{lis}</ol></nav>'


def page_head(crumbs, h1, lead=''):
    lead_html = f'\n    <p class="page-head__lead">{lead}</p>' if lead else ''
    return f'''<section class="page-head">
  <div class="container">
    {breadcrumbs(crumbs)}
    <h1 class="page-head__title">{h1}</h1>{lead_html}
  </div>
</section>
'''


def product_card(p, lazy=True):
    badge = f'<span class="product-card__badge">{E(p["badge"])}</span>' if p['badge'] else ''
    specs = ''.join(f'<li class="product-card__spec"><span class="product-card__spec-name">{E(k)}</span>'
                    f'<span class="product-card__spec-value">{E(v)}</span></li>' for k, v in p['card'])
    stock = ('<p class="product-card__stock product-card__stock--in">В наличии</p>' if p['stock'] == 'in'
             else '<p class="product-card__stock product-card__stock--order">Под заказ, 3–5 дней</p>')
    loading = ' loading="lazy"' if lazy else ''
    pm = '' if p['pmin'] is None else f' data-players-min="{p["pmin"]}" data-players-max="{p["pmax"]}"'
    return f'''<li class="product-grid__item" data-slug="{p['slug']}" data-title="{E(p['title'].lower())}" data-category="{p['cat']}" data-price="{p['price']}" data-stock="{p['stock']}" data-order="{p['order']}"{pm}>
  <article class="product-card">
    <a class="product-card__media" href="{p['url']}" tabindex="-1" aria-hidden="true"><img class="product-card__image" src="{p['image']}" alt="" width="800" height="600"{loading}></a>
    {badge}
    <div class="product-card__body">
      <h3 class="product-card__title"><a class="product-card__link" href="{p['url']}">{E(p['title'])}</a></h3>
      <p class="product-card__text">{E(p['short'])}</p>
      <ul class="product-card__specs">{specs}</ul>
      {stock}
      <div class="product-card__footer">
        <p class="product-card__price">{money(p['price'])}</p>
        <button class="btn btn--primary btn--small product-card__button" type="button" data-add-to-cart="{p['slug']}">В корзину</button>
      </div>
    </div>
  </article>
</li>
'''


def count_in(cat):
    return sum(1 for p in PRODUCTS if p['cat'] == cat)


def plural(n, forms):
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        return forms[0]
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14:
        return forms[1]
    return forms[2]


def category_tile(c, mod=''):
    n = count_in(c['id'])
    return f'''<li class="category-grid__item{mod}">
  <a class="category-tile" href="listing.html?cat={c['id']}">
    <img class="category-tile__image" src="img/{c['art']}.svg" alt="" width="800" height="600" loading="lazy">
    <span class="category-tile__body">
      <span class="category-tile__title">{E(c['title'])}</span>
      <span class="category-tile__meta">{n} {plural(n, ('товар', 'товара', 'товаров'))}</span>
    </span>
  </a>
</li>
'''


def event_item(e):
    return f'''<li class="event">
  <time class="event__date" datetime="{e['date']}"><span class="event__day">{e['day']}</span><span class="event__month">{e['month']}</span></time>
  <div class="event__info">
    <h3 class="event__title">{E(e['title'])}</h3>
    <p class="event__meta">{e['wd'].capitalize()}, {e['time']}</p>
    <p class="event__text">{E(e['text'])}</p>
  </div>
  <a class="btn btn--outline btn--small event__button" href="contacts.html?topic=event#feedback">Записаться</a>
</li>
'''


def cta_band(title='Устал от экранов? Заходи, брось кубик!'):
    return f'''<section class="cta-band">
  <div class="container cta-band__inner">
    <div class="cta-band__text">
      <h2 class="cta-band__title">{title}</h2>
      <p class="cta-band__lead">Ждём вас каждый день с 11:00 до 22:00 по адресу {ADDRESS}.</p>
    </div>
    <div class="cta-band__actions">
      <a class="btn btn--dark" href="contacts.html">Как нас найти</a>
      <a class="btn btn--outline" href="{TG}" target="_blank" rel="noopener noreferrer">Наш Telegram</a>
    </div>
  </div>
</section>
'''


# ======================= СТРАНИЦЫ =======================
def build_home():
    hero = art.hero_svg(True)
    hits = ''.join(product_card(P[s], lazy=False) for s in ['wingspan', 'imaginarium', 'carcassonne', 'exploding-kittens'])
    cats = ''.join(category_tile(c, ' category-grid__item--' + ('wide' if i < 2 else 'narrow')) for i, c in enumerate(CATEGORIES))
    events = ''.join(event_item(e) for e in EVENTS[:3])
    main = f'''<section class="hero" aria-labelledby="hero-title">
  <div class="container hero__inner">
    <div class="hero__content">
      <h1 class="hero__title" id="hero-title">Сначала сыграй — потом покупай</h1>
      <p class="hero__lead">Бесплатно попробуйте любую игру из каталога за столом в нашей игровой зоне. Эксперты объяснят правила за 15 минут.</p>
      <div class="hero__actions">
        <a class="btn btn--dark btn--large" href="catalog.html">Выбрать игру</a>
        <a class="btn btn--outline btn--large" href="contacts.html?topic=table#feedback">Забронировать стол</a>
      </div>
    </div>
    <div class="hero__art hero-art">{hero}</div>
  </div>
</section>
<section class="facts" aria-label="Коротко о магазине">
  <ul class="container facts__list">
    <li class="facts__item">Тест любой игры — бесплатно</li>
    <li class="facts__item">Мастер-класс каждую неделю</li>
    <li class="facts__item">Открыты каждый день с 11:00 до 22:00</li>
  </ul>
</section>
<section class="section" aria-labelledby="advantages-title">
  <div class="container">
    <h2 class="section__title" id="advantages-title">Почему выбирают нас</h2>
    <div class="advantages">
      <article class="advantage advantage--feature">
        <h3 class="advantage__title">Тестирование перед покупкой</h3>
        <p class="advantage__text">В магазине есть просторная игровая зона. Возьмите любую игру из каталога, сядьте за стол и проверьте её в деле — без риска купить «кота в мешке».</p>
        <a class="btn btn--primary" href="contacts.html?topic=table#feedback">Забронировать стол</a>
      </article>
      <article class="advantage advantage--masterclass">
        <h3 class="advantage__title">Бесплатные мастер-классы</h3>
        <p class="advantage__text">Каждую неделю разбираем новинки и сложные игры. Правила — за 15 минут.</p>
      </article>
      <article class="advantage advantage--tournaments">
        <h3 class="advantage__title">Турниры и клуб</h3>
        <p class="advantage__text">Регулярные турниры с призовым фондом и сообщество, где легко найти новых друзей и соперников.</p>
      </article>
      <article class="advantage advantage--experts">
        <h3 class="advantage__title">Экспертный подбор</h3>
        <p class="advantage__text">Подберём игру под компанию, повод и бюджет, а ещё подскажем, какие аксессуары действительно нужны для долгой сохранности коллекции.</p>
      </article>
    </div>
  </div>
</section>
<section class="section section--mist" aria-labelledby="categories-title">
  <div class="container">
    <div class="section__head">
      <h2 class="section__title" id="categories-title">Категории каталога</h2>
      <a class="btn btn--outline btn--small" href="catalog.html">Весь каталог</a>
    </div>
    <ul class="category-grid">
{cats}    </ul>
  </div>
</section>
<section class="section" aria-labelledby="hits-title">
  <div class="container">
    <div class="section__head">
      <h2 class="section__title" id="hits-title">Хиты продаж</h2>
      <a class="btn btn--outline btn--small" href="listing.html">Смотреть все игры</a>
    </div>
    <ul class="product-grid">
{hits}    </ul>
  </div>
</section>
<section class="section section--petrol" aria-labelledby="events-title">
  <div class="container">
    <div class="section__head">
      <h2 class="section__title" id="events-title">Ближайшие события</h2>
      <a class="btn btn--outline-light btn--small" href="events.html">Вся афиша</a>
    </div>
    <ol class="event-list">
{events}    </ol>
  </div>
</section>
<section class="section" aria-labelledby="trust-title">
  <div class="container trust">
    <div class="trust__story">
      <h2 class="section__title" id="trust-title">Восемь лет за одним столом</h2>
      <p class="trust__text">Мы работаем с 2018 года. Начинали как небольшой магазинчик, а сегодня — крупнейшая локальная точка настольных игр во Владимире. Наша миссия — объединять людей за одним столом, даря эмоции и живое общение в эпоху цифровизации.</p>
      <a class="btn btn--outline" href="about.html">О магазине</a>
    </div>
    <ul class="trust__reviews">
      <li class="review review--one"><blockquote class="review__quote"><p class="review__text">Пришли с друзьями «просто посмотреть», а остались на три часа. Сыграли в «Каркассон» и сразу купили его.</p></blockquote><p class="review__author">Анна, студентка</p></li>
      <li class="review review--two"><blockquote class="review__quote"><p class="review__text">Выручили с подарком для сына: объяснили правила за десять минут и дали попробовать игру прямо в магазине.</p></blockquote><p class="review__author">Дмитрий, папа восьмилетнего игрока</p></li>
      <li class="review review--three"><blockquote class="review__quote"><p class="review__text">Хожу на турниры по Magic. Приятная атмосфера, всегда найдётся с кем сыграть.</p></blockquote><p class="review__author">Игорь, фрилансер</p></li>
    </ul>
  </div>
</section>
{cta_band()}'''
    page('index.html', 'Брось кубик — магазин настольных игр во Владимире',
         'Магазин настольных игр во Владимире: бесплатная игровая зона, мастер-классы, турниры и экспертный подбор игр.',
         'page--home', 'home', main, ['main.js'])


def build_catalog():
    cats = ''.join(f'''<li class="category-grid__item category-grid__item--large">
  <a class="category-tile category-tile--large" href="listing.html?cat={c['id']}">
    <img class="category-tile__image" src="img/{c['art']}.svg" alt="" width="800" height="600" loading="lazy">
    <span class="category-tile__body">
      <span class="category-tile__title">{E(c['title'])}</span>
      <span class="category-tile__desc">{E(c['desc'])}</span>
      <span class="category-tile__meta">{count_in(c['id'])} {plural(count_in(c['id']), ('товар', 'товара', 'товаров'))}</span>
    </span>
  </a>
</li>
''' for c in CATEGORIES)
    main = page_head([('index.html', 'Главная'), ('catalog.html', 'Каталог')], 'Каталог',
                     'Выберите раздел — от стратегий до аксессуаров для вашей коллекции.') + f'''<section class="section section--tight" aria-label="Категории">
  <div class="container">
    <ul class="category-list">
{cats}      <li class="category-list__item category-list__item--help">
        <div class="help-tile">
          <h2 class="help-tile__title">Не знаете, что выбрать?</h2>
          <p class="help-tile__text">Расскажите, с кем и как часто играете, — эксперты подберут игру под компанию, повод и бюджет.</p>
          <a class="btn btn--primary" href="contacts.html?topic=advice#feedback">Попросить подбор</a>
        </div>
      </li>
    </ul>
  </div>
</section>
'''
    page('catalog.html', 'Каталог — Брось кубик', 'Все категории настольных игр и аксессуаров магазина «Брось кубик».',
         'page--catalog', 'catalog', main, ['main.js'])


def build_listing():
    cat_checks = ''.join(f'''<li class="filters__option"><label class="check"><input class="check__input" type="checkbox" name="cat" value="{c['id']}"><span class="check__box" aria-hidden="true"></span><span class="check__label">{E(c['short'])}</span></label></li>''' for c in CATEGORIES)
    cards = ''.join(product_card(p) for p in PRODUCTS)
    main = page_head([('index.html', 'Главная'), ('catalog.html', 'Каталог'), ('listing.html', 'Все игры')], 'Игры и аксессуары',
                     'Фильтруйте по категории, цене и числу игроков — результаты обновляются сразу.') + f'''<div class="container listing">
  <details class="filters" id="filters-panel" open>
    <summary class="filters__summary">Фильтры</summary>
    <form class="filters__form" id="filters-form" action="listing.html" method="get" aria-label="Фильтры каталога">
      <div class="filters__header">
        <h2 class="filters__title">Фильтры</h2>
        <button class="filters__reset" type="button" id="filters-reset">Сбросить</button>
      </div>
      <div class="filters__group">
        <label class="filters__label" for="filter-search">Поиск по названию</label>
        <input class="input" id="filter-search" type="search" name="q" placeholder="Например, каркассон" autocomplete="off">
      </div>
      <fieldset class="filters__group">
        <legend class="filters__label">Категория</legend>
        <ul class="filters__options">{cat_checks}</ul>
      </fieldset>
      <fieldset class="filters__group">
        <legend class="filters__label">Цена, ₽</legend>
        <div class="filters__range">
          <label class="visually-hidden" for="price-min">Цена от</label>
          <input class="input" id="price-min" type="number" name="min" min="0" step="100" inputmode="numeric" placeholder="От">
          <label class="visually-hidden" for="price-max">Цена до</label>
          <input class="input" id="price-max" type="number" name="max" min="0" step="100" inputmode="numeric" placeholder="До">
        </div>
      </fieldset>
      <div class="filters__group">
        <label class="filters__label" for="filter-players">Количество игроков</label>
        <select class="input" id="filter-players" name="players">
          <option value="">Любое</option>
          <option value="1">1 игрок</option>
          <option value="2">2 игрока</option>
          <option value="3">3–4 игрока</option>
          <option value="5">5 и более</option>
        </select>
      </div>
      <div class="filters__group">
        <label class="check"><input class="check__input" type="checkbox" id="filter-stock" name="stock" value="1"><span class="check__box" aria-hidden="true"></span><span class="check__label">Только в наличии</span></label>
      </div>
    </form>
  </details>
  <section class="catalog" aria-labelledby="catalog-title">
    <h2 class="visually-hidden" id="catalog-title">Список товаров</h2>
    <div class="catalog__bar">
      <p class="catalog__count" id="catalog-count" aria-live="polite">Найдено: {len(PRODUCTS)} товаров</p>
      <div class="catalog__sort">
        <label class="catalog__sort-label" for="sort-select">Сортировка</label>
        <select class="input input--compact" id="sort-select" name="sort">
          <option value="default">По умолчанию</option>
          <option value="price-asc">Сначала дешевле</option>
          <option value="price-desc">Сначала дороже</option>
          <option value="title">По названию (А–Я)</option>
        </select>
      </div>
    </div>
    <ul class="product-grid product-grid--listing" id="product-grid">
{cards}    </ul>
    <div class="catalog__empty" id="catalog-empty" hidden>
      <p class="catalog__empty-title">Ничего не нашлось</p>
      <p class="catalog__empty-text">Попробуйте изменить условия поиска или сбросить фильтры.</p>
      <button class="btn btn--primary" type="button" id="catalog-empty-reset">Сбросить фильтры</button>
    </div>
  </section>
</div>
'''
    page('listing.html', 'Игры и аксессуары — каталог с фильтрами — Брось кубик',
         'Каталог настольных игр и аксессуаров с фильтрами по категории, цене и количеству игроков.',
         'page--listing', 'catalog', main, ['main.js', 'listing.js'])


def build_products():
    for p in PRODUCTS:
        c = CAT[p['cat']]
        rows = ''.join(f'<div class="specs__row"><dt class="specs__name">{E(k)}</dt><dd class="specs__value">{E(v)}</dd></div>' for k, v in p['specs'])
        paras = ''.join(f'<p class="product__paragraph">{E(t)}</p>' for t in p['long'])
        stock = ('<p class="product__stock product__stock--in">В наличии</p>' if p['stock'] == 'in'
                 else '<p class="product__stock product__stock--order">Под заказ, срок поставки 3–5 дней</p>')
        sim_slugs = [q['slug'] for q in PRODUCTS if q['cat'] == p['cat'] and q['slug'] != p['slug']]
        for q in PRODUCTS:
            if len(sim_slugs) >= 4:
                break
            if q['slug'] != p['slug'] and q['slug'] not in sim_slugs:
                sim_slugs.append(q['slug'])
        sim = ''.join(product_card(P[s]) for s in sim_slugs[:4])
        main = page_head([('index.html', 'Главная'), ('catalog.html', 'Каталог'),
                          (f"listing.html?cat={c['id']}", c['short']), (p['url'], p['title'])], E(p['title'])) + f'''<section class="product container" aria-label="Информация о товаре">
  <div class="product__gallery">
    <img class="product__image" src="{p['image']}" alt="{E(p['title'])}: иллюстрация коробки" width="800" height="600">
  </div>
  <div class="product__info">
    <p class="product__category"><a class="product__category-link" href="listing.html?cat={c['id']}">{E(c['title'])}</a></p>
    {stock}
    <p class="product__price">{money(p['price'])}</p>
    <p class="product__lead">{E(p['short'])}</p>
    <div class="product__buy">
      <div class="quantity" data-quantity>
        <button class="quantity__button" type="button" data-qty-minus aria-label="Уменьшить количество">−</button>
        <label class="visually-hidden" for="qty">Количество</label>
        <input class="quantity__input" id="qty" type="number" name="qty" value="1" min="1" max="20" inputmode="numeric">
        <button class="quantity__button" type="button" data-qty-plus aria-label="Увеличить количество">+</button>
      </div>
      <button class="btn btn--primary btn--large product__add" type="button" data-add-to-cart="{p['slug']}" data-qty-source="#qty">Добавить в корзину</button>
    </div>
    <aside class="try-block">
      <h2 class="try-block__title">Попробуйте перед покупкой</h2>
      <p class="try-block__text">Возьмите эту игру бесплатно в игровой зоне магазина и сыграйте за нашим столом.</p>
      <a class="btn btn--outline btn--small" href="contacts.html?topic=table#feedback">Забронировать стол</a>
    </aside>
    <p class="product__delivery">Самовывоз: {ADDRESS}, бесплатно. Доставка по Владимиру — <a class="link" href="delivery.html">условия</a>.</p>
  </div>
</section>
<section class="section section--tight" aria-labelledby="product-details-title">
  <div class="container product-details">
    <div class="product-details__text">
      <h2 class="product-details__title" id="product-details-title">Описание</h2>
      {paras}
    </div>
    <div class="product-details__specs">
      <h2 class="product-details__title">Характеристики</h2>
      <dl class="specs">{rows}</dl>
    </div>
  </div>
</section>
<section class="section section--mist" aria-labelledby="similar-title">
  <div class="container">
    <h2 class="section__title" id="similar-title">Вам может понравиться</h2>
    <ul class="product-grid">
{sim}    </ul>
  </div>
</section>
'''
        page(p['url'], f"{p['title']} — купить в магазине «Брось кубик»",
             f"{p['title']}: {p['short']} Цена {p['price']} ₽.", 'page--product', 'catalog', main, ['main.js'])


def build_cart():
    main = page_head([('index.html', 'Главная'), ('cart.html', 'Корзина')], 'Корзина') + '''<section class="container cart" id="cart-root" aria-live="polite" aria-label="Содержимое корзины">
  <noscript><p class="cart__noscript">Для работы корзины включите JavaScript в браузере.</p></noscript>
</section>
'''
    page('cart.html', 'Корзина — Брось кубик', 'Ваш заказ в магазине настольных игр «Брось кубик».', 'page--cart', None, main,
         ['data.js', 'main.js', 'cart.js'])


FIELD_MSG = 'data-msg-required'


def build_checkout():
    main = page_head([('index.html', 'Главная'), ('cart.html', 'Корзина'), ('checkout.html', 'Оформление заказа')],
                     'Оформление заказа', 'Заполните форму — мы свяжемся с вами для подтверждения.') + '''<div class="container checkout" id="checkout-root">
  <form class="checkout__form form" id="checkout-form" action="checkout.html" method="post" novalidate>
    <p class="form__summary" id="checkout-form-summary" role="alert" hidden></p>
    <fieldset class="form__group">
      <legend class="form__legend">Ваши данные</legend>
      <div class="field">
        <label class="field__label" for="order-name">Имя</label>
        <input class="input field__control" id="order-name" name="name" type="text" autocomplete="name" required minlength="2" data-msg-required="Введите ваше имя" data-msg-short="Имя слишком короткое: минимум 2 символа">
        <p class="field__error" id="order-name-error" hidden></p>
      </div>
      <div class="field">
        <label class="field__label" for="order-phone">Телефон</label>
        <input class="input field__control" id="order-phone" name="phone" type="tel" autocomplete="tel" placeholder="+7 (999) 123-45-67" required data-phone data-msg-required="Укажите телефон, чтобы мы могли подтвердить заказ" data-msg-invalid="Телефон указан неверно. Пример: +7 (999) 123-45-67">
        <p class="field__error" id="order-phone-error" hidden></p>
      </div>
      <div class="field">
        <label class="field__label" for="order-email">E-mail</label>
        <input class="input field__control" id="order-email" name="email" type="email" autocomplete="email" placeholder="name@mail.ru" required data-msg-required="Укажите e-mail для чека и уведомлений" data-msg-invalid="Проверьте e-mail: он должен выглядеть как name@mail.ru">
        <p class="field__error" id="order-email-error" hidden></p>
      </div>
    </fieldset>
    <fieldset class="form__group">
      <legend class="form__legend">Получение заказа</legend>
      <div class="choice-row">
        <label class="choice"><input class="choice__input" type="radio" name="delivery" value="pickup" checked><span class="choice__body"><span class="choice__title">Самовывоз</span><span class="choice__text">ул. Тракторная, д. 20, бесплатно</span></span></label>
        <label class="choice"><input class="choice__input" type="radio" name="delivery" value="courier"><span class="choice__body"><span class="choice__title">Доставка по Владимиру</span><span class="choice__text">300 ₽, бесплатно от 5 000 ₽</span></span></label>
      </div>
      <div class="field" id="address-field" hidden>
        <label class="field__label" for="order-address">Адрес доставки</label>
        <input class="input field__control" id="order-address" name="address" type="text" autocomplete="address-line1" placeholder="Улица, дом, квартира" minlength="6" data-msg-required="Укажите адрес доставки" data-msg-short="Адрес слишком короткий: укажите улицу, дом и квартиру">
        <p class="field__error" id="order-address-error" hidden></p>
      </div>
      <div class="field field--checkbox">
        <label class="check"><input class="check__input field__control" id="order-table" type="checkbox" name="table" value="1"><span class="check__box" aria-hidden="true"></span><span class="check__label">Забронировать стол в игровой зоне, чтобы сыграть перед покупкой</span></label>
      </div>
    </fieldset>
    <fieldset class="form__group">
      <legend class="form__legend">Комментарий</legend>
      <div class="field">
        <label class="field__label" for="order-comment">Пожелания к заказу</label>
        <textarea class="input field__control" id="order-comment" name="comment" rows="4" placeholder="Например, удобное время звонка"></textarea>
        <p class="field__error" id="order-comment-error" hidden></p>
      </div>
      <div class="field field--checkbox">
        <label class="check"><input class="check__input field__control" id="order-consent" type="checkbox" name="consent" value="1" required data-msg-required="Подтвердите согласие на обработку персональных данных"><span class="check__box" aria-hidden="true"></span><span class="check__label">Согласен на обработку персональных данных</span></label>
        <p class="field__error" id="order-consent-error" hidden></p>
      </div>
    </fieldset>
    <button class="btn btn--primary btn--large form__submit" type="submit">Подтвердить заказ</button>
  </form>
  <aside class="checkout__summary" id="checkout-summary" aria-label="Ваш заказ"></aside>
  <section class="checkout__done" id="checkout-done" hidden tabindex="-1" aria-live="polite">
    <h2 class="checkout__done-title">Спасибо за заказ!</h2>
    <p class="checkout__done-text" id="checkout-done-text"></p>
    <a class="btn btn--primary" href="catalog.html">Вернуться в каталог</a>
  </section>
</div>
'''
    page('checkout.html', 'Оформление заказа — Брось кубик', 'Оформление заказа в магазине настольных игр «Брось кубик».',
         'page--checkout', None, main, ['data.js', 'main.js', 'forms.js', 'checkout.js'])


def map_svg():
    return f'''<svg class="map__svg" viewBox="0 0 640 420" role="img" aria-label="Схема проезда: магазин на улице Тракторной, рядом остановка и парковка" width="640" height="420">
<rect width="640" height="420" fill="#EAF1F3"/>
<g fill="#FFFFFF" stroke="#C5D2D6" stroke-width="2">
<rect x="30" y="30" width="130" height="90" rx="8"/><rect x="30" y="150" width="130" height="80" rx="8"/><rect x="190" y="30" width="170" height="90" rx="8"/>
<rect x="400" y="30" width="90" height="90" rx="8"/><rect x="520" y="30" width="90" height="90" rx="8"/><rect x="400" y="150" width="210" height="80" rx="8"/>
<rect x="30" y="285" width="130" height="105" rx="8"/><rect x="190" y="285" width="130" height="105" rx="8"/><rect x="360" y="285" width="110" height="105" rx="8"/><rect x="500" y="285" width="110" height="105" rx="8"/>
</g>
<g fill="none" stroke="#FFFFFF" stroke-width="26" stroke-linecap="round"><path d="M0 255H640"/><path d="M176 0V420"/><path d="M380 0V420"/></g>
<g fill="none" stroke="#C5D2D6" stroke-width="2"><path d="M0 242H640M0 268H640M163 0V420M189 0V420M367 0V420M393 0V420"/></g>
<path d="M0 255H640" stroke="#F5B81C" stroke-width="4" stroke-dasharray="14 12" fill="none"/>
<text x="430" y="304" font-family="Arial, sans-serif" font-size="15" fill="#535D62">ул. Тракторная</text>
<g transform="translate(280 255)"><path d="M0 0 L-16 -34 A22 22 0 1 1 16 -34Z" fill="#1A1713"/><circle cx="0" cy="-44" r="8" fill="#F5B81C"/></g>
<g font-family="Arial, sans-serif" font-size="14" font-weight="700"><rect x="296" y="150" width="196" height="34" rx="8" fill="#FFFFFF" stroke="#1A1713" stroke-width="2"/><text x="394" y="172" text-anchor="middle" fill="#1A1713">Магазин «Брось кубик»</text></g>
<g font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#1A1713"><rect x="410" y="204" width="30" height="30" rx="6" fill="#FFFFFF" stroke="#1A1713" stroke-width="2"/><text x="425" y="225" text-anchor="middle">А</text><rect x="208" y="204" width="30" height="30" rx="6" fill="#FFFFFF" stroke="#1A1713" stroke-width="2"/><text x="223" y="225" text-anchor="middle">P</text></g>
<g font-family="Arial, sans-serif" font-size="12" fill="#535D62"><text x="446" y="225">Остановка</text><text x="244" y="225">Парковка</text></g>
</svg>'''


def build_contacts():
    main = page_head([('index.html', 'Главная'), ('contacts.html', 'Контакты')], 'Контакты и обратная связь',
                     'Приходите в гости или напишите нам — ответим в течение рабочего дня.') + f'''<section class="container contacts" aria-label="Как с нами связаться">
  <div class="contacts__card">
    <h2 class="contacts__title">Магазин и игровая зона</h2>
    <dl class="contact-list">
      <div class="contact-list__row"><dt class="contact-list__name">Адрес</dt><dd class="contact-list__value">{ADDRESS}</dd></div>
      <div class="contact-list__row"><dt class="contact-list__name">Телефон</dt><dd class="contact-list__value"><a class="link" href="{PHONE_HREF}">{PHONE_TEXT}</a> (WhatsApp, Telegram)</dd></div>
      <div class="contact-list__row"><dt class="contact-list__name">E-mail</dt><dd class="contact-list__value"><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      <div class="contact-list__row"><dt class="contact-list__name">Режим работы</dt><dd class="contact-list__value">Пн–Вс с 11:00 до 22:00</dd></div>
      <div class="contact-list__row"><dt class="contact-list__name">Соцсети</dt><dd class="contact-list__value"><a class="link" href="{VK}" target="_blank" rel="noopener noreferrer">ВКонтакте</a>, <a class="link" href="{TG}" target="_blank" rel="noopener noreferrer">Telegram-канал @broskubik_news</a></dd></div>
    </dl>
  </div>
  <figure class="map">
    {map_svg()}
    <figcaption class="map__caption">Схема проезда. <a class="link" href="{MAP_URL}" target="_blank" rel="noopener noreferrer">Открыть в Яндекс Картах</a></figcaption>
  </figure>
</section>
<section class="section section--mist" id="feedback" aria-labelledby="feedback-title">
  <div class="container feedback">
    <div class="feedback__intro">
      <h2 class="section__title" id="feedback-title">Напишите нам</h2>
      <p class="feedback__text">Задайте вопрос, забронируйте стол в игровой зоне или запишитесь на событие. Организаторам детских праздников, школам и компаниям подготовим оптовые цены: выберите тему «Сотрудничество и опт».</p>
    </div>
    <form class="feedback__form form" id="feedback-form" action="contacts.html" method="post" novalidate>
      <p class="form__summary" id="feedback-form-summary" role="alert" hidden></p>
      <div class="field">
        <label class="field__label" for="fb-name">Имя</label>
        <input class="input field__control" id="fb-name" name="name" type="text" autocomplete="name" required minlength="2" placeholder="Как к вам обращаться" data-msg-required="Введите ваше имя" data-msg-short="Имя слишком короткое: минимум 2 символа">
        <p class="field__error" id="fb-name-error" hidden></p>
      </div>
      <div class="field">
        <label class="field__label" for="fb-email">E-mail</label>
        <input class="input field__control" id="fb-email" name="email" type="email" autocomplete="email" required placeholder="name@mail.ru" data-msg-required="Укажите e-mail, чтобы мы смогли ответить" data-msg-invalid="Проверьте e-mail: он должен выглядеть как name@mail.ru">
        <p class="field__error" id="fb-email-error" hidden></p>
      </div>
      <div class="field">
        <label class="field__label" for="fb-phone">Телефон <span class="field__optional">(необязательно)</span></label>
        <input class="input field__control" id="fb-phone" name="phone" type="tel" autocomplete="tel" placeholder="+7 (999) 123-45-67" data-phone data-msg-invalid="Телефон указан неверно. Пример: +7 (999) 123-45-67">
        <p class="field__error" id="fb-phone-error" hidden></p>
      </div>
      <div class="field">
        <label class="field__label" for="fb-topic">Тема обращения</label>
        <select class="input field__control" id="fb-topic" name="topic" required data-msg-required="Выберите тему обращения">
          <option value="">Выберите тему</option>
          <option value="question">Вопрос по товару или заказу</option>
          <option value="table">Бронирование стола</option>
          <option value="event">Запись на событие</option>
          <option value="advice">Подбор игры</option>
          <option value="partner">Сотрудничество и опт</option>
        </select>
        <p class="field__error" id="fb-topic-error" hidden></p>
      </div>
      <div class="field field--wide">
        <label class="field__label" for="fb-message">Сообщение</label>
        <textarea class="input field__control" id="fb-message" name="message" rows="5" required minlength="10" placeholder="Расскажите, чем мы можем помочь" data-msg-required="Напишите сообщение" data-msg-short="Сообщение слишком короткое: опишите вопрос подробнее (минимум 10 символов)"></textarea>
        <p class="field__error" id="fb-message-error" hidden></p>
      </div>
      <div class="field field--wide field--checkbox">
        <label class="check"><input class="check__input field__control" id="fb-consent" type="checkbox" name="consent" value="1" required data-msg-required="Подтвердите согласие на обработку персональных данных"><span class="check__box" aria-hidden="true"></span><span class="check__label">Согласен на обработку персональных данных</span></label>
        <p class="field__error" id="fb-consent-error" hidden></p>
      </div>
      <div class="field--wide">
        <button class="btn btn--primary btn--large form__submit" type="submit">Отправить сообщение</button>
      </div>
    </form>
    <section class="feedback__done" id="feedback-done" hidden tabindex="-1" aria-live="polite">
      <h3 class="feedback__done-title">Сообщение отправлено</h3>
      <p class="feedback__done-text">Спасибо! Мы ответим на указанный e-mail в течение рабочего дня.</p>
      <button class="btn btn--outline" type="button" id="feedback-again">Написать ещё</button>
    </section>
  </div>
</section>
'''
    page('contacts.html', 'Контакты — Брось кубик', 'Адрес, телефон, схема проезда и форма обратной связи магазина «Брось кубик» во Владимире.',
         'page--contacts', 'contacts', main, ['main.js', 'forms.js', 'contacts.js'])


def info_nav(active):
    items = [('about.html', 'О нас', 'about'), ('delivery.html', 'Доставка и оплата', 'delivery'), ('events.html', 'Афиша', 'events'),
             ('contacts.html', 'Контакты', 'contacts')]
    lis = ''.join(f'<li class="info-nav__item"><a class="info-nav__link" href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if k == active else ""}>{l}</a></li>' for h, l, k in items)
    return f'<nav class="info-nav" aria-label="Информация"><h2 class="info-nav__title">Информация</h2><ul class="info-nav__list">{lis}</ul></nav>'


def build_about():
    main = page_head([('index.html', 'Главная'), ('about.html', 'О нас')], 'О магазине «Брось кубик»') + f'''<div class="container info">
  {info_nav('about')}
  <div class="info__content">
    <img class="info__banner" src="img/table.svg" alt="Игровой стол с кубиками и картами" width="640" height="560">
    <p class="info__lead">Мы работаем с 2018 года. Начинали как небольшой магазинчик, а сегодня — крупнейшая локальная точка настольных игр во Владимире: с просторной игровой зоной, мастер-классами и турнирами.</p>
    <blockquote class="mission"><p class="mission__text">Объединять людей за одним столом, даря эмоции и живое общение в эпоху цифровизации.</p><footer class="mission__caption">Наша миссия</footer></blockquote>
    <h2 class="info__title">Что нас отличает</h2>
    <ul class="traits">
      <li class="traits__item"><h3 class="traits__title">Тестирование перед покупкой</h3><p class="traits__text">Любую игру из каталога можно бесплатно опробовать за столом в игровой зоне и убедиться, что она подходит именно вам.</p></li>
      <li class="traits__item"><h3 class="traits__title">Бесплатное обучение</h3><p class="traits__text">Еженедельно проводим мастер-классы по новинкам и сложным играм. Наши сотрудники объяснят правила за 15 минут.</p></li>
      <li class="traits__item"><h3 class="traits__title">Турниры и клуб</h3><p class="traits__text">Регулярные турниры с призовым фондом создают вокруг магазина сообщество, где можно найти друзей и соперников.</p></li>
      <li class="traits__item"><h3 class="traits__title">Экспертный подбор</h3><p class="traits__text">Подскажем игру для вечеринки, семейного вечера или серьёзной стратегии и расскажем, какие аксессуары действительно нужны.</p></li>
    </ul>
    <h2 class="info__title">Наш путь</h2>
    <ol class="timeline">
      <li class="timeline__item"><p class="timeline__year">2018</p><p class="timeline__text">Открыли небольшой магазин настольных игр.</p></li>
      <li class="timeline__item"><p class="timeline__year">Дальше</p><p class="timeline__text">Появились игровая зона, мастер-классы и турниры.</p></li>
      <li class="timeline__item"><p class="timeline__year">2026</p><p class="timeline__text">Отмечаем 8 лет и остаёмся крупнейшей локальной точкой во Владимире.</p></li>
    </ol>
    <div class="info__cta">
      <h2 class="info__cta-title">Приходите в гости</h2>
      <p class="info__cta-text">{ADDRESS}. Ежедневно с 11:00 до 22:00.</p>
      <div class="info__cta-actions"><a class="btn btn--primary" href="contacts.html">Контакты</a><a class="btn btn--outline" href="contacts.html?topic=table#feedback">Забронировать стол</a></div>
    </div>
  </div>
</div>
'''
    page('about.html', 'О нас — Брось кубик', 'История, миссия и преимущества магазина настольных игр «Брось кубик» во Владимире.',
         'page--about', 'about', main, ['main.js'])


def build_delivery():
    main = page_head([('index.html', 'Главная'), ('delivery.html', 'Доставка и оплата')], 'Доставка и оплата') + f'''<div class="container info">
  {info_nav('delivery')}
  <div class="info__content">
    <p class="info__lead">Заберите заказ в магазине или попросите привезти его по Владимиру.</p>
    <h2 class="info__title">Самовывоз</h2>
    <p class="info__text">Бесплатно из магазина по адресу {ADDRESS}. Заказ ждёт вас каждый день с 11:00 до 22:00. Перед получением можно попробовать игру в игровой зоне.</p>
    <h2 class="info__title">Доставка по Владимиру</h2>
    <ul class="plain-list">
      <li class="plain-list__item">Стоимость — 300 ₽, при заказе от 5 000 ₽ доставка бесплатная.</li>
      <li class="plain-list__item">Срок — 1–2 дня после подтверждения заказа.</li>
      <li class="plain-list__item">Товары «под заказ» доставляем после поступления в магазин, обычно за 3–5 дней.</li>
    </ul>
    <h2 class="info__title">Оплата</h2>
    <p class="info__text">Оплата наличными или банковской картой при получении. Мы позвоним, чтобы подтвердить заказ и согласовать время.</p>
    <h2 class="info__title">Бронирование стола</h2>
    <p class="info__text">Игровая зона бесплатна для покупателей. Чтобы место точно нашлось, забронируйте стол заранее через <a class="link" href="contacts.html?topic=table#feedback">форму обратной связи</a> или по телефону <a class="link" href="{PHONE_HREF}">{PHONE_TEXT}</a>.</p>
    <h2 class="info__title">Обмен и возврат</h2>
    <p class="info__text">Условия обмена и возврата регулируются законодательством РФ. По любым вопросам позвоните нам или напишите на <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  </div>
</div>
'''
    page('delivery.html', 'Доставка и оплата — Брось кубик', 'Условия самовывоза, доставки по Владимиру и оплаты заказов в магазине «Брось кубик».',
         'page--delivery', 'delivery', main, ['main.js'])


def build_events():
    items = ''.join(event_item(e) for e in EVENTS)
    main = page_head([('index.html', 'Главная'), ('events.html', 'Афиша')], 'Афиша событий',
                     'Мастер-классы, турниры и семейные дни в игровой зоне магазина. Участие в мастер-классах бесплатное.') + f'''<div class="container info">
  {info_nav('events')}
  <div class="info__content">
    <ol class="event-list event-list--light">
{items}    </ol>
    <p class="info__text">Расписание обновляется. Следите за анонсами в <a class="link" href="{TG}" target="_blank" rel="noopener noreferrer">Telegram-канале</a> и <a class="link" href="{VK}" target="_blank" rel="noopener noreferrer">ВКонтакте</a>.</p>
  </div>
</div>
'''
    page('events.html', 'Афиша — Брось кубик', 'Расписание мастер-классов и турниров магазина настольных игр «Брось кубик».',
         'page--events', 'events', main, ['main.js'])


def write_data():
    data = [dict(slug=p['slug'], title=p['title'], price=p['price'], image=p['image'], url=p['url'], stock=p['stock']) for p in PRODUCTS]
    js = ('/* Файл создаётся скриптом build.py */\n'
          'window.BK_PRODUCTS = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n'
          'window.BK_CONFIG = {\n  deliveryPrice: 300,\n  freeDeliveryFrom: 5000,\n  promoCode: "КУБИК10",\n  promoPercent: 10\n};\n')
    with open(os.path.join(ROOT, 'js', 'data.js'), 'w', encoding='utf8') as f:
        f.write(js)


def main():
    os.makedirs(os.path.join(ROOT, 'img'), exist_ok=True)
    for k in art.PRODUCT_ART:
        open(os.path.join(ROOT, 'img', f'{k}.svg'), 'w', encoding='utf8').write(art.product_svg(k))
    open(os.path.join(ROOT, 'img', 'table.svg'), 'w', encoding='utf8').write(art.hero_svg(False))
    open(os.path.join(ROOT, 'img', 'favicon.svg'), 'w', encoding='utf8').write(art.favicon_svg())
    build_home(); build_catalog(); build_listing(); build_products(); build_cart(); build_checkout()
    build_contacts(); build_about(); build_delivery(); build_events(); write_data()
    open(os.path.join(ROOT, '.nojekyll'), 'w').close()
    print('built')


if __name__ == '__main__':
    main()
