# -*- coding: utf-8 -*-
"""Авторские векторные иллюстрации (без использования чужих обложек и логотипов)."""
import math

INK = '#1A1713'
SAFFRON = '#F5B81C'
PETROL = '#12485B'
RED = '#D9402B'
WHITE = '#FFFFFF'


def pip_die(x, y, s, n, fill=WHITE, stroke=INK, pip=INK, rot=0):
    """Игральный кубик с n точками; (x, y) — центр."""
    r = s * 0.09
    o = s * 0.27
    pos = {
        1: [(0, 0)], 2: [(-o, -o), (o, o)], 3: [(-o, -o), (0, 0), (o, o)],
        4: [(-o, -o), (o, -o), (-o, o), (o, o)],
        5: [(-o, -o), (o, -o), (0, 0), (-o, o), (o, o)],
        6: [(-o, -o), (o, -o), (-o, 0), (o, 0), (-o, o), (o, o)],
    }[n]
    g = f'<g transform="translate({x} {y}) rotate({rot})">'
    g += f'<rect x="{-s / 2}" y="{-s / 2}" width="{s}" height="{s}" rx="{s * 0.2}" fill="{fill}" stroke="{stroke}" stroke-width="{max(2, s * 0.04)}"/>'
    for px, py in pos:
        g += f'<circle cx="{px}" cy="{py}" r="{r}" fill="{pip}"/>'
    return g + '</g>'


# ---------- мотивы (центр около 400, 250) ----------

def m_wingspan(a):
    return (
        f'<path d="M290 300 Q330 170 430 190 Q470 140 520 160 Q505 190 520 210 Q540 250 470 300 Q400 350 290 300Z" fill="{a}" stroke="{INK}" stroke-width="5"/>'
        f'<path d="M300 292 Q360 250 440 262 Q400 300 300 292Z" fill="{WHITE}" opacity=".35"/>'
        f'<path d="M330 280 Q380 230 460 235" fill="none" stroke="{INK}" stroke-width="4"/>'
        f'<path d="M520 160 L560 172 L522 184Z" fill="{RED}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        f'<circle cx="490" cy="170" r="7" fill="{INK}"/>'
        f'<path d="M290 300 L250 330 L300 322 L262 356 L330 330Z" fill="{a}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        f'<path d="M250 360 Q400 330 560 372" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    )


def m_stone(a):
    return (
        f'<polygon points="300,330 330,230 410,200 480,240 500,330" fill="#C9B79C" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        f'<polygon points="330,230 410,200 420,260 360,300" fill="#E2D4BC" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        f'<polygon points="420,260 410,200 480,240 470,290" fill="#A99880" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        f'<line x1="520" y1="360" x2="560" y2="170" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
        f'<polygon points="560,170 540,200 580,198" fill="{a}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        f'<circle cx="270" cy="350" r="22" fill="#A99880" stroke="{INK}" stroke-width="4"/>'
        f'<path d="M340 350 Q380 300 420 350 Q400 380 380 360 Q360 380 340 350Z" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
    )


def m_carcassonne(a):
    cols = ['#7FB069', '#5E9A4F', '#C9A66B', '#7FB069', '#5E9A4F', '#7FB069', '#C9A66B', '#7FB069', '#5E9A4F']
    s = 78
    out = ''
    for i in range(9):
        x, y = 285 + (i % 3) * s, 130 + (i // 3) * s
        out += f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{cols[i]}" stroke="{INK}" stroke-width="3"/>'
    out += f'<path d="M285 247 Q340 230 363 247 T519 247" fill="none" stroke="#F3E6C2" stroke-width="16"/>'
    # замок
    out += f'<rect x="372" y="165" width="60" height="50" fill="{a}" stroke="{INK}" stroke-width="4"/>'
    for k in range(3):
        out += f'<rect x="{372 + k * 22}" y="152" width="16" height="16" fill="{a}" stroke="{INK}" stroke-width="3"/>'
    out += f'<rect x="392" y="190" width="20" height="25" rx="10" fill="{INK}"/>'
    out += f'<circle cx="480" cy="300" r="12" fill="{RED}" stroke="{INK}" stroke-width="3"/>'
    return out


def m_dobble(a):
    out = f'<circle cx="400" cy="250" r="130" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
    items = [(400, 170, 30, RED), (470, 215, 26, '#2E86AB'), (470, 290, 28, SAFFRON), (400, 335, 26, '#3F9D5B'),
             (330, 290, 30, '#8E5BD0'), (330, 215, 26, '#F28C28'), (400, 250, 34, INK)]
    for x, y, r, c in items:
        out += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{INK}" stroke-width="3"/>'
    out += f'<polygon points="400,232 406,246 421,246 409,255 413,270 400,261 387,270 391,255 379,246 394,246" fill="{WHITE}"/>'
    return out


def m_imaginarium(a):
    return (
        f'<rect x="300" y="110" width="200" height="280" rx="16" fill="{WHITE}" stroke="{INK}" stroke-width="5" transform="rotate(-6 400 250)"/>'
        f'<rect x="320" y="132" width="160" height="236" rx="10" fill="#5B4AA8" transform="rotate(-6 400 250)"/>'
        f'<circle cx="440" cy="190" r="34" fill="{a}"/><circle cx="452" cy="182" r="30" fill="#5B4AA8"/>'
        f'<g fill="{WHITE}"><circle cx="360" cy="300" r="26"/><circle cx="392" cy="290" r="34"/><circle cx="430" cy="302" r="26"/><rect x="360" y="300" width="96" height="26"/></g>'
        f'<polygon points="350,180 355,194 370,194 358,203 362,217 350,208 338,217 342,203 330,194 345,194" fill="{a}"/>'
        f'<circle cx="468" cy="350" r="5" fill="{a}"/><circle cx="340" cy="250" r="4" fill="{a}"/>'
    )


def m_kittens(a):
    pts = []
    for i in range(24):
        ang = i * math.pi / 12
        r = 150 if i % 2 == 0 else 105
        pts.append(f'{400 + r * math.cos(ang):.0f},{250 + r * math.sin(ang):.0f}')
    return (
        f'<polygon points="{" ".join(pts)}" fill="{RED}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        f'<polygon points="330,230 340,160 385,200" fill="{a}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        f'<polygon points="470,230 460,160 415,200" fill="{a}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        f'<ellipse cx="400" cy="262" rx="82" ry="70" fill="{a}" stroke="{INK}" stroke-width="5"/>'
        f'<circle cx="372" cy="250" r="11" fill="{INK}"/><circle cx="428" cy="250" r="11" fill="{INK}"/>'
        f'<polygon points="392,272 408,272 400,282" fill="{RED}"/>'
        f'<path d="M400 282 Q392 296 380 292 M400 282 Q408 296 420 292" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M340 276 L300 266 M340 288 L302 296 M460 276 L500 266 M460 288 L498 296" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
    )


def m_mtg(a):
    cols = ['#F5F0D0', '#3C78D8', '#2B2B2B', '#D9402B', '#3F9D5B']
    out = ''
    for i, c in enumerate(cols):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        x, y = 400 + 100 * math.cos(ang), 250 + 100 * math.sin(ang)
        out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="46" fill="{c}" stroke="{INK}" stroke-width="5"/>'
    out += f'<polygon points="400,200 450,250 400,300 350,250" fill="{a}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    return out


def m_warhammer(a):
    return (
        f'<path d="M300 140 L500 140 L520 260 Q510 340 400 390 Q290 340 280 260Z" fill="#4C5E3A" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        f'<path d="M300 140 L400 180 L500 140" fill="none" stroke="{INK}" stroke-width="5"/>'
        f'<path d="M318 200 L400 236 L482 200 M326 256 L400 292 L474 256" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="400" cy="200" r="0" fill="none"/>'
        f'<line x1="560" y1="130" x2="560" y2="380" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
        f'<polygon points="560,110 545,150 575,150" fill="{a}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
    )


def m_dice(a):
    pts = ' '.join(f'{400 + 120 * math.cos(math.pi / 6 + i * math.pi / 3):.0f},{250 + 120 * math.sin(math.pi / 6 + i * math.pi / 3):.0f}' for i in range(6))
    tri = ' '.join(f'{400 + 70 * math.cos(-math.pi / 2 + i * 2 * math.pi / 3):.0f},{250 + 70 * math.sin(-math.pi / 2 + i * 2 * math.pi / 3):.0f}' for i in range(3))
    return (
        f'<polygon points="{pts}" fill="{a}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        f'<polygon points="{tri}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        f'<path d="M400 180 L400 130 M{400 + 61:.0f} 285 L{400 + 104:.0f} 310 M{400 - 61:.0f} 285 L{400 - 104:.0f} 310" stroke="{INK}" stroke-width="5"/>'
        f'<text x="400" y="272" font-family="Arial, sans-serif" font-size="56" font-weight="700" text-anchor="middle" fill="{INK}">20</text>'
        + pip_die(280, 360, 70, 5, WHITE, INK, INK, -12) + pip_die(520, 365, 62, 3, WHITE, INK, INK, 14)
    )


def m_organizer(a):
    out = f'<rect x="260" y="130" width="280" height="240" rx="12" fill="#B9884F" stroke="{INK}" stroke-width="6"/>'
    cells = [(276, 146, 110, 90), (394, 146, 130, 90), (276, 244, 70, 110), (354, 244, 80, 110), (442, 244, 82, 110)]
    for x, y, w, h in cells:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#8A6030" stroke="{INK}" stroke-width="3"/>'
    out += f'<circle cx="330" cy="190" r="26" fill="{a}" stroke="{INK}" stroke-width="3"/>'
    out += f'<rect x="420" y="170" width="46" height="62" rx="4" fill="{WHITE}" stroke="{INK}" stroke-width="3" transform="rotate(-8 443 200)"/>'
    out += f'<rect x="440" y="170" width="46" height="62" rx="4" fill="{RED}" stroke="{INK}" stroke-width="3" transform="rotate(8 463 200)"/>'
    out += f'<rect x="288" y="262" width="46" height="26" rx="4" fill="{PETROL}" stroke="{INK}" stroke-width="3"/>'
    out += f'<circle cx="394" cy="300" r="22" fill="{a}" stroke="{INK}" stroke-width="3"/>'
    out += f'<rect x="458" y="262" width="50" height="70" rx="4" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
    return out


PRODUCT_ART = {
    'wingspan': (m_wingspan, '#D6ECEA', PETROL, SAFFRON, 'КРЫЛЬЯ'),
    'stone-age': (m_stone, '#F1DDC0', '#8A4B2A', SAFFRON, 'КАМЕННЫЙ ВЕК'),
    'carcassonne': (m_carcassonne, '#DDEBC9', '#2F6B3A', '#F2D16B', 'КАРКАССОН'),
    'dobble': (m_dobble, '#FBD9D3', RED, WHITE, 'ДОББЛЬ'),
    'imaginarium': (m_imaginarium, '#E3DDF5', '#4B3A8F', SAFFRON, 'ИМАДЖИНАРИУМ'),
    'exploding-kittens': (m_kittens, '#FFE3A8', INK, SAFFRON, 'ВЗРЫВНЫЕ КОТЯТА'),
    'mtg-starter': (m_mtg, '#E1E6EA', '#2B3440', SAFFRON, 'СТАРТОВЫЙ НАБОР'),
    'warhammer-starter': (m_warhammer, '#E6E2D6', '#3B4A2F', '#C9A227', 'КОМАНДНЫЙ СТАРТЕР'),
    'metal-dice': (m_dice, '#D9E8F0', '#6A2C70', SAFFRON, 'МЕТАЛЛИЧЕСКИЕ ДАЙСЫ'),
    'box-organizer': (m_organizer, '#EADFCB', '#5B3A1E', SAFFRON, 'ОРГАНАЙЗЕР'),
}


def product_svg(slug):
    motif, bg, box, acc, title = PRODUCT_ART[slug]
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600" role="img" aria-label="{title}">'
         f'<rect width="800" height="600" fill="{bg}"/>'
         f'<circle cx="690" cy="90" r="150" fill="{box}" opacity=".08"/><circle cx="90" cy="540" r="120" fill="{box}" opacity=".08"/>'
         f'<ellipse cx="400" cy="548" rx="230" ry="18" fill="{INK}" opacity=".18"/>'
         f'<g transform="rotate(-3 400 300)">'
         f'<rect x="215" y="62" width="370" height="476" rx="16" fill="{box}" stroke="{INK}" stroke-width="6"/>'
         f'<rect x="215" y="62" width="34" height="476" rx="16" fill="{INK}" opacity=".25"/>'
         f'<g transform="translate(0 0)">{motif(acc)}</g>'
         f'<rect x="215" y="420" width="370" height="76" fill="{INK}" opacity=".88"/>'
         f'<text x="400" y="468" font-family="Arial, Helvetica, sans-serif" font-size="{26 if len(title) < 15 else 22}" font-weight="700" text-anchor="middle" fill="{WHITE}">{title}</text>'
         f'</g>'
         + pip_die(120, 130, 58, 4, WHITE, INK, INK, -14) + pip_die(690, 470, 66, 6, SAFFRON, INK, INK, 12)
         + '</svg>')
    return s


def hero_svg(animated=True):
    """Игровой стол: войлочное поле, кубики, карты. Классы нужны для CSS-анимации."""
    cls = (lambda c: f' class="{c}"') if animated else (lambda c: '')
    s = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 560" role="img" '
         'aria-label="Игровой стол с кубиками и картами" width="640" height="560">'
         f'<ellipse cx="330" cy="500" rx="260" ry="26" fill="{INK}" opacity=".2"/>'
         f'<g{cls("hero-art__table")}>'
         f'<rect x="40" y="70" width="560" height="400" rx="46" fill="{PETROL}" stroke="{INK}" stroke-width="8"/>'
         f'<rect x="64" y="94" width="512" height="352" rx="30" fill="none" stroke="{SAFFRON}" stroke-width="3" stroke-dasharray="3 12" stroke-linecap="round"/>'
         '</g>'
         # карты веером
         f'<g{cls("hero-art__cards")}>'
         f'<rect x="130" y="170" width="120" height="170" rx="12" fill="{WHITE}" stroke="{INK}" stroke-width="5" transform="rotate(-18 190 255)"/>'
         f'<rect x="170" y="160" width="120" height="170" rx="12" fill="{SAFFRON}" stroke="{INK}" stroke-width="5" transform="rotate(-4 230 245)"/>'
         f'<rect x="212" y="164" width="120" height="170" rx="12" fill="{WHITE}" stroke="{INK}" stroke-width="5" transform="rotate(12 272 249)"/>'
         f'<circle cx="230" cy="245" r="26" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
         f'<polygon points="272,214 279,232 298,232 283,243 289,262 272,251 255,262 261,243 246,232 265,232" fill="{INK}" transform="translate(4 8)"/>'
         '</g>'
         # кубики
         f'<g{cls("hero-art__die hero-art__die--one")}>{pip_die(420, 230, 110, 6, WHITE, INK, INK, 0)}</g>'
         f'<g{cls("hero-art__die hero-art__die--two")}>{pip_die(500, 360, 92, 5, SAFFRON, INK, INK, 0)}</g>'
         f'<g{cls("hero-art__die hero-art__die--three")}>{pip_die(360, 380, 78, 3, RED, INK, WHITE, 0)}</g>'
         '</svg>')
    return s


def favicon_svg():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">'
            f'<rect x="4" y="4" width="56" height="56" rx="14" fill="{SAFFRON}" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="20" cy="20" r="5" fill="{INK}"/><circle cx="44" cy="20" r="5" fill="{INK}"/>'
            f'<circle cx="32" cy="32" r="5" fill="{INK}"/><circle cx="20" cy="44" r="5" fill="{INK}"/>'
            f'<circle cx="44" cy="44" r="5" fill="{INK}"/></svg>')


if __name__ == '__main__':
    import os
    os.makedirs('../img', exist_ok=True)
    for k in PRODUCT_ART:
        open(f'../img/{k}.svg', 'w', encoding='utf8').write(product_svg(k))
    open('../img/table.svg', 'w', encoding='utf8').write(hero_svg(False))
    open('../img/favicon.svg', 'w', encoding='utf8').write(favicon_svg())
    print('ok')
