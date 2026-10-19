#!/usr/bin/env python3
"""Gera os SVGs em pixel art do perfil: o escritório da CodeWave e a ficha de estatísticas.

Uso: GITHUB_TOKEN=... python3 gerar.py        (no Mac: GITHUB_TOKEN=$(gh auth token) python3 gerar.py)
     python3 gerar.py --teste                 (só os auto-testes)
"""
import datetime as dt, json, os, random, sys, unicodedata, urllib.request

USUARIO = 'Pedrovictorrr'

# ---------- fonte 3x5 ----------
F = {
 'A': '.#.#.#####.##.#', 'B': '##.#.###.#.###.', 'C': '.###..#..#...##', 'D': '##.#.##.##.###.',
 'E': '####..##.#..###', 'F': '####..##.#..#..', 'G': '.###..#.##.#.##', 'H': '#.##.#####.##.#',
 'I': '###.#..#..#.###', 'J': '..#..#..##.#.#.', 'K': '#.##.###.#.##.#', 'L': '#..#..#..#..###',
 'M': '#.#####.##.##.#', 'N': '##.#.##.##.##.#', 'O': '.#.#.##.##.#.#.', 'P': '##.#.###.#..#..',
 'Q': '.#.#.##.###..##', 'R': '##.#.###.#.##.#', 'S': '.###...#...###.', 'T': '###.#..#..#..#.',
 'U': '#.##.##.##.####', 'V': '#.##.##.##.#.#.', 'W': '#.##.########.#', 'X': '#.##.#.#.#.##.#',
 'Y': '#.##.#.#..#..#.', 'Z': '###..#.#.#..###',
 '0': '####.##.##.####', '1': '.#.##..#..#.###', '2': '##...#.#.#..###', '3': '##...#.#...###.',
 '4': '#.##.####..#..#', '5': '####..##...###.', '6': '.###..####.####', '7': '###..#.#..#..#.',
 '8': '####.#####.####', '9': '####.####..###.', ' ': '...............', '.': '.............#.',
 ',': '..........#.#..', ':': '....#.....#....', '!': '.#..#..#.....#.', '?': '##...#.#.....#.',
 '-': '......###......', '+': '....#.###.#....', '/': '..#..#.#.#..#..', '%': '#.#..#.#.#..#.#',
 '#': '#.####.####.#.#', '>': '#...#...#.#.#..', '<': '..#.#.#...#...#', '_': '............###',
 '(': '.#.#..#..#...#.', ')': '.#...#..#..#.#.', '*': '...#.#.#.#.#...', '=': '...###...###...',
 '@': '.#.#.####...###', "'": '.#..#..........', '|': '.#..#..#..#..#.', '$': '.####..#..####.',
}


def limpa(s):
    s = unicodedata.normalize('NFKD', str(s).upper()).encode('ascii', 'ignore').decode()
    return ''.join(c if c in F else ' ' for c in s)


def largura(s, e=1):
    return (len(limpa(s)) * 4 - 1) * e


def caminho(pontos):
    """Junta pixels (x, y) em corridas horizontais num único path."""
    linhas, d = {}, []
    for x, y in set(pontos):
        linhas.setdefault(y, []).append(x)
    for y, xs in sorted(linhas.items()):
        xs.sort()
        ini = ant = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == ant + 1:
                ant = x
                continue
            d.append(f'M{ini} {y}h{ant - ini + 1}v1h{ini - ant - 1}z')
            if x is not None:
                ini = ant = x
    return ''.join(d)


def P(pontos, cor, attrs=''):
    return f'<path fill="{cor}" d="{caminho(pontos)}"{attrs}/>' if pontos else ''


def ret(x, y, w, h, cor, attrs=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{cor}"{attrs}/>'


def texto(s, x, y, cor, e=1, centro=False, attrs=''):
    s = limpa(s)
    if centro:
        x -= largura(s, e) // 2
    pts = []
    for i, c in enumerate(s):
        for j, b in enumerate(F[c]):
            if b == '#':
                px, py = x + (i * 4 + j % 3) * e, y + (j // 3) * e
                pts += [(px + a, py + b2) for a in range(e) for b2 in range(e)]
    return P(pts, cor, attrs)


def sprite(linhas, paleta, x, y, attrs=''):
    por_cor = {}
    for j, linha in enumerate(linhas):
        for i, c in enumerate(linha):
            if c in paleta:
                por_cor.setdefault(paleta[c], []).append((x + i, y + j))
    return f'<g{attrs}>' + ''.join(P(p, c) for c, p in por_cor.items()) + '</g>'


def g(conteudo, cls='', estilo=''):
    a = (f' class="{cls}"' if cls else '') + (f' style="{estilo}"' if estilo else '')
    return f'<g{a}>{conteudo}</g>'


def fmt(n):
    return f'{n:,}'.replace(',', '.')


# ---------- dados ----------
def graphql(query, token):
    req = urllib.request.Request('https://api.github.com/graphql', json.dumps({'query': query}).encode(),
                                 {'Authorization': f'bearer {token}', 'User-Agent': USUARIO})
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.load(r)
    if 'errors' in resp:
        raise SystemExit(f'GraphQL: {resp["errors"]}')
    return resp['data']


CAL = 'contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}'


def busca(token):
    u = graphql(f'''{{user(login:"{USUARIO}"){{createdAt followers{{totalCount}}
      todos: repositories(ownerAffiliations:OWNER, privacy:PUBLIC){{totalCount}}
      repos: repositories(first:100, ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false){{nodes{{stargazerCount
        languages(first:10, orderBy:{{field:SIZE, direction:DESC}}){{edges{{size node{{name color}}}}}}}}}}
      contributionsCollection{{{CAL}}}}}}}''', token)['user']
    anos = range(int(u['createdAt'][:4]), dt.date.today().year + 1)
    partes = ' '.join(f'a{a}: contributionsCollection(from:"{a}-01-01T00:00:00Z", to:"{a}-12-31T23:59:59Z"){{{CAL}}}'
                      for a in anos)
    por_ano = graphql(f'{{user(login:"{USUARIO}"){{{partes}}}}}', token)['user']
    dias = {}
    for c in por_ano.values():
        for w in c['contributionCalendar']['weeks']:
            for d in w['contributionDays']:
                dias[d['date']] = d['contributionCount']
    ultimo_ano = [d['contributionCount'] for w in u['contributionsCollection']['contributionCalendar']['weeks']
                  for d in w['contributionDays']]
    langs = {}
    for r in u['repos']['nodes']:
        for e in r['languages']['edges']:
            n = e['node']['name']
            langs.setdefault(n, [0, e['node']['color'] or '#8b8fb5'])[0] += e['size']
    atual, recorde = streaks(dias, dt.date.today().isoformat())
    return dict(
        ano=u['contributionsCollection']['contributionCalendar']['totalContributions'],
        total=sum(c['contributionCalendar']['totalContributions'] for c in por_ano.values()),
        desde=anos[0], atual=atual, recorde=recorde, repos=u['todos']['totalCount'],
        estrelas=sum(r['stargazerCount'] for r in u['repos']['nodes']),
        seguidores=u['followers']['totalCount'], melhor=max(dias.values(), default=0),
        dias=ultimo_ano, langs=sorted(langs.items(), key=lambda kv: -kv[1][0])[:5],
    )


def streaks(dias, hoje):
    """(sequência atual, recorde). Hoje sem contribuição ainda não quebra a sequência."""
    datas = sorted(d for d in dias if d <= hoje)
    recorde = seq = 0
    for d in datas:
        seq = seq + 1 if dias[d] else 0
        recorde = max(recorde, seq)
    dia = dt.date.fromisoformat(hoje)
    if not dias.get(hoje):
        dia -= dt.timedelta(days=1)
    atual = 0
    while dias.get(dia.isoformat()):
        atual += 1
        dia -= dt.timedelta(days=1)
    return atual, recorde


# ---------- o escritório ----------
CSS_COMUM = '''
@keyframes pisca{50%{opacity:.15}}
@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.rot0{opacity:1!important}}
'''

CSS_ESCRITORIO = '''
.tw{animation:tw 3s steps(1) infinite}
.led{animation:pisca 1.1s steps(1) infinite}
.type{animation:type .34s steps(1) infinite}
@keyframes type{50%{transform:translateY(-1px)}}
.olho{opacity:0;animation:olho 4.5s steps(1) infinite}
@keyframes olho{93%{opacity:1}97%{opacity:0}}
.scroll{animation:scroll 5s steps(12) infinite}
@keyframes scroll{to{transform:translateY(-24px)}}
.neon{animation:neon 7s steps(1) infinite}
@keyframes neon{3%{opacity:.35}4%{opacity:1}6%{opacity:.5}7%{opacity:1}61%{opacity:.6}62%{opacity:1}}
.rot{opacity:0;animation:rot 12s steps(1) infinite}
@keyframes rot{0%{opacity:1}25%,100%{opacity:0}}
.pop{opacity:0;animation:pop 6s steps(1) infinite}
@keyframes pop{0%{opacity:0;transform:translateY(2px)}8%{opacity:1;transform:translateY(1px)}12%{transform:none}55%{opacity:1}60%{opacity:0}}
.sobe{opacity:0;animation:sobe 3s steps(12) infinite}
@keyframes sobe{0%{opacity:0;transform:none}15%{opacity:1}75%{opacity:1}100%{opacity:0;transform:translateY(-12px)}}
.vapor{opacity:0;animation:vapor 2.4s steps(6) infinite}
@keyframes vapor{0%{opacity:0;transform:none}30%{opacity:.8}100%{opacity:0;transform:translateY(-5px)}}
.barra{transform-box:fill-box;transform-origin:bottom;animation:barra 2.4s steps(6) infinite}
@keyframes barra{0%{transform:scaleY(.2)}70%,100%{transform:scaleY(1)}}
.anda{animation:anda 22s steps(310) infinite}
@keyframes anda{from{transform:translateX(-24px)}to{transform:translateX(286px)}}
.pa{animation:pa .36s steps(1) infinite}
.pb{opacity:0;animation:pb .36s steps(1) infinite}
@keyframes pa{50%{opacity:0}}
@keyframes pb{50%{opacity:1}}
.scan{animation:scan 4s steps(44) infinite}
@keyframes scan{to{transform:translateX(88px)}}
.frame{opacity:0;animation:frame 6s steps(1) infinite}
@keyframes frame{0%{opacity:1}50%,100%{opacity:0}}
.rot3{opacity:0;animation:rot3 9s steps(1) infinite}
@keyframes rot3{0%{opacity:1}33.3%,100%{opacity:0}}
.dot{animation:dot 1.2s steps(1) infinite}
@keyframes dot{0%,33%{opacity:1}34%,100%{opacity:.25}}
'''

CABECAS = {
    'longo': ['............', '....HHHHH...', '...HHHHHHH..', '..HHHHSSSS..', '..HHHSSSES..',
              '..HHHSSSSSS.', '..HHHSSSSS..', '..HHH..SS...'],
    'curto': ['............', '....HHHHH...', '...HHHHHHH..', '...HHHSSSS..', '...HHSSSES..',
              '...HHSSSSSS.', '....SSSSSS..', '......SS....'],
    'topete': ['......HH....', '....HHHHHH..', '...HHHHHHH..', '...HHHSSSS..', '...HHGGLLG..',
               '...HHSSSSSS.', '....SSSSSS..', '......SS....'],
    'cacheado': ['...HHHHHH...', '..HHHHHHHH..', '.HHHHHHHHHH.', '.HHHHHSSSS..', '.HHHHSSSES..',
                 '.HHHHSSSSSS.', '..HHYSSSSS..', '..HH...SS...'],
    'coque': ['..HH........', '.HHHHHHHH...', '..HHHHHHHH..', '...HHHSSSS..', '...HHSSSES..',
              '...HHSSSSSS.', '....SSSSSS..', '......SS....'],
    'bone': ['............', '....AAAAA...', '...AAAAAAAA.', '...HHHSSSS..', '...HHSSSES..',
             '...HHSSSSSS.', '....SSSSSS..', '......SS....'],
}
CORPO = ['....CCCC....', '...CCCCCC...', '...CCCCCC...', '...CCCCCC...', '...CCCCCC...', '...CCCCCC...',
         '...PPPPPPPP.', '...PPPPPPPP.', '........PP..', '........PP..', '........PP..', '........BBB.']

# cores dos avatares oficiais (codewave-equipe/avatares/gera.py)
EQUIPE = [
    dict(nome='Jessica', setor='Suporte', estilo='longo', pele='#E9B48F', cabelo='#3B2416', roupa='#2F8F83',
         cor='#F47B2A', extra='headset', acao='chat'),
    dict(nome='Igor', setor='Vendas', estilo='curto', pele='#C98D62', cabelo='#1E1A17', roupa='#22304A',
         cor='#4F86F7', extra='gravata', acao='grafico'),
    dict(nome='Marcos', setor='Dev / TI', estilo='topete', pele='#F1C8A6', cabelo='#5A3A22', roupa='#3A3F4B',
         cor='#1ECB8B', extra='', acao='merge', cafe=True),
    dict(nome='Alana', setor='Marketing', estilo='cacheado', pele='#8D5A3B', cabelo='#1F130D', roupa='#F2C14E',
         cor='#E8489A', extra='', acao='likes'),
    dict(nome='Bruno', setor='QA', estilo='bone', pele='#D9A07A', cabelo='#2E2118', roupa='#33415C',
         cor='#F2B800', extra='', acao='bug'),
    dict(nome='Gabrielle', setor='Executiva', estilo='coque', pele='#F3D1B6', cabelo='#A0612F', roupa='#EDEAF7',
         cor='#9B6BFF', extra='', acao='agenda', cafe=True),
]


def escurece(cor, f=.72):
    r, g_, b = (int(cor[i:i + 2], 16) for i in (1, 3, 5))
    return '#%02x%02x%02x' % (int(r * f), int(g_ * f), int(b * f))


def personagem(p, x, y):
    linhas = [list(l) for l in CABECAS[p['estilo']] + CORPO]
    if p['extra'] == 'headset':
        for c, l in [(6, 1), (6, 2), (5, 3), (5, 4), (5, 5), (6, 6), (7, 6), (8, 6)]:
            linhas[l][c] = 'M'
        linhas[6][9] = 'A'
    if p['extra'] == 'gravata':
        linhas[9][8], linhas[10][8], linhas[11][8] = 'W', 'R', 'R'
    if p['estilo'] == 'longo':
        for l in (8, 9):
            linhas[l][2] = linhas[l][3] = 'H'
    pal = dict(H=p['cabelo'], S=p['pele'], E='#1b1420', C=p['roupa'], P='#2b2d42', B='#111018',
               G='#111018', L='#9fd8ff', Y='#F2C14E', M='#26242e', A=p['cor'], W='#ffffff', R='#E4572E')
    s = sprite([''.join(l) for l in linhas], pal, x, y)
    # antena de bot: haste + LED piscando na cor do setor
    topo = y - 1 if p['estilo'] in ('topete', 'cacheado', 'coque') else y
    s += ret(x + 7, topo - 2, 1, 2, '#6b6f8f') + ret(x + 7, topo - 3, 1, 1, p['cor'], ' class="led"')
    olho = (8, 4) if p['estilo'] != 'topete' else None
    if olho:
        s += ret(x + olho[0], y + olho[1], 1, 1, p['pele'], ' class="olho"' +
                 f' style="animation-delay:-{random.random() * 4:.1f}s"')
    braco = P([(x + i, y + 10) for i in range(5, 9)] + [(x + 8, y + 11), (x + 9, y + 11)], escurece(p['roupa']))
    braco += P([(x + 10, y + 11)], p['pele'])
    s += g(braco, 'type', f'animation-delay:-{random.random():.2f}s')
    return s


def cadeira(x, y):
    k, k2 = '#3b3f58', '#2a2d40'
    return (ret(x, y + 2, 2, 13, k) + ret(x + 1, y + 16, 9, 2, k) + ret(x + 5, y + 18, 1, 4, k2) +
            ret(x + 2, y + 22, 7, 1, k2) + ret(x + 2, y + 23, 1, 1, '#111') + ret(x + 8, y + 23, 1, 1, '#111'))


def tela_codigo(x, y, w, h, cor, uid):
    rnd = random.Random(uid)
    linhas, yy = [], 0
    for _ in range(12):
        ind = rnd.choice([0, 0, 1, 2, 2, 3])
        tam = rnd.randint(3, w - 3 - ind)
        c = rnd.choice([cor, cor, '#c8cbe8', '#6b6f8f', '#ffd86b'])
        linhas.append((ind, tam, c, yy))
        yy += 2
    pts = ''.join(ret(x + 1 + ind, y + 1 + yy + o, tam, 1, c) for o in (0, 24) for ind, tam, c, yy in linhas)
    return (f'<clipPath id="t{uid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
            f'<g clip-path="url(#t{uid})">{g(pts, "scroll", f"animation-delay:-{uid * .7:.1f}s")}</g>')


CORACAO = ['.#.#.', '#####', '#####', '.###.', '..#..']
INSETO = ['#...#', '.###.', '#####', '.###.', '#.#.#']
CHECK = ['....#', '...#.', '#.#..', '.#...']


def balao(x, y, w, h, fundo='#ffffff'):
    return (ret(x + 1, y, w - 2, h, fundo) + ret(x, y + 1, w, h - 2, fundo) +
            ret(x + w // 2 - 1, y + h, 3, 1, fundo) + ret(x + w // 2, y + h + 1, 1, 1, fundo))


def acao(p, mx, y):
    a, c = p['acao'], p['cor']
    if a == 'chat':
        s = balao(mx - 7, y + 4, 15, 7)
        for i in range(3):
            s += ret(mx - 4 + i * 3, y + 7, 2, 1, c, f' class="dot" style="animation-delay:{i * .4:.1f}s"')
        return s
    if a == 'grafico':
        s = ret(mx - 7, y + 1, 15, 11, '#0b0c1a') + ret(mx - 7, y + 11, 15, 1, '#6b6f8f')
        for i, h in enumerate((3, 5, 7, 9)):
            s += ret(mx - 5 + i * 3, y + 11 - h, 2, h, c, f' class="barra" style="animation-delay:-{i * .3:.1f}s"')
        return s
    if a == 'merge':
        s = balao(mx - 15, y + 3, 31, 8, c) + sprite(CHECK, {'#': '#ffffff'}, mx - 13, y + 5)
        s += texto('MERGED', mx - 7, y + 5, '#ffffff')
        return g(s, 'pop')
    if a == 'likes':
        return ''.join(g(sprite(CORACAO, {'#': c}, mx - 6 + i * 5, y + 8), 'sobe', f'animation-delay:{i:.0f}s')
                       for i in range(3))
    if a == 'bug':
        f1 = balao(mx - 6, y + 3, 13, 9) + sprite(INSETO, {'#': '#E4572E'}, mx - 2, y + 5)
        f2 = balao(mx - 10, y + 3, 21, 9, '#1ECB8B') + texto('PASS', mx - 7, y + 5, '#ffffff')
        return (g(f1, 'frame rot0') + g(f2, 'frame', 'animation-delay:-3s'))
    if a == 'agenda':
        out = ''
        for i, h in enumerate(('08:00', '13:00', '19:00')):
            s = balao(mx - 12, y + 3, 25, 9) + texto(h, mx - 9, y + 5, c)
            out += g(s, 'rot3' + (' rot0' if i == 0 else ''), f'animation-delay:-{(3 - i) % 3 * 3}s')
        return out
    return ''


def cachorro(x, y):
    corpo = ['.........DO..', '........OOOO.', 'O.......OOOEO', '.O......OOOOK', '.OOOOOOORROO.',
             '.OOOOOOOOOO..']
    pal = {'O': '#E8913A', 'D': '#9a5418', 'E': '#1b1420', 'K': '#1b1420', 'R': '#E4572E'}
    pa = sprite(corpo + ['.O.O.....O.O.', '.O.O.....O.O.'], pal, x, y, ' class="pa"')
    pb = sprite(corpo + ['..O.O...O.O..', '.O...O.O...O.'], pal, x, y, ' class="pb"')
    return g(pa + pb, 'anda')


def escritorio(d):
    W, H = 256, 144
    random.seed(42)
    s = [ret(0, 0, W, 100, '#17182b')]
    s += [ret(x, 0, 1, 100, '#1c1d33') for x in range(16, W, 32)]
    s += [ret(0, 100, W, 2, '#2c2e48'), ret(0, 102, W, H - 102, '#211f36')]
    s += [ret(0, y, W, 1, '#272540') for y in (110, 122, 136)]

    # janela com a cidade à noite
    s += [ret(6, 8, 50, 40, '#3a3d5c'), ret(8, 10, 46, 36, '#0e1233')]
    for i in range(18):
        x, y = random.randint(9, 52), random.randint(11, 28)
        s.append(ret(x, y, 1, 1, '#ffffff', f' class="tw" style="animation-delay:-{random.random() * 3:.1f}s"'))
    s += [sprite(['.##.', '###.', '##..', '.##.'], {'#': '#f6f1c7'}, 45, 13)]
    x = 8
    while x < 54:
        w, h = random.randint(4, 8), random.randint(6, 16)
        w = min(w, 54 - x)
        s.append(ret(x, 46 - h, w, h, '#1d2147'))
        for wx in range(x + 1, x + w - 1, 2):
            for wy in range(46 - h + 2, 45, 3):
                if random.random() < .45:
                    cls = f' class="tw" style="animation-duration:{random.randint(4, 9)}s"' if random.random() < .3 else ''
                    s.append(ret(wx, wy, 1, 1, '#ffd86b', cls))
        x += w
    s += [ret(30, 10, 1, 36, '#3a3d5c'), ret(6, 47, 50, 2, '#2c2e48')]

    # letreiro neon
    neon = texto('CODEWAVE', 107, 11, '#3ff5d0', 2, True) + texto('SYSTEMS', 107, 25, '#3ff5d0', 1, True)
    s.append(f'<g filter="url(#brilho)">{g(neon, "neon")}</g>')
    s.append(texto('CEO: PEDRO VICTOR', 107, 36, '#6b6f8f', 1, True))

    # telão com as estatísticas
    s += [ret(158, 5, 93, 49, '#2c2e48'), ret(160, 7, 89, 45, '#071018')]
    s += [ret(163, 10, 3, 3, '#ff4f5e', ' class="led"'), texto('AO VIVO', 168, 9, '#ff4f5e'),
          texto('GITHUB', 245 - largura('GITHUB'), 9, '#6b6f8f')]
    paineis = [('CONTRIBUICOES', fmt(d['ano']), 'NO ULTIMO ANO'),
               ('STREAK ATUAL', f'{d["atual"]} DIAS', f'RECORDE: {d["recorde"]} DIAS'),
               ('REPOS PUBLICOS', str(d['repos']), f'{d["estrelas"]} STARS  {d["seguidores"]} SEGUIDORES'),
               (f'TOTAL DESDE {d["desde"]}', fmt(d['total']), 'E CONTANDO...')]
    for i, (t1, t2, t3) in enumerate(paineis):
        p = texto(t1, 204, 17, '#8b8fb5', 1, True) + texto(t2, 204, 24, '#3ff5d0', 2, True) + \
            texto(t3, 204, 36, '#ffd86b', 1, True)
        s.append(g(p, 'rot' + (' rot0' if i == 0 else ''), f'animation-delay:-{(12 - i * 3) % 12}s'))
    ult = d['dias'][-44:]
    m = max(ult) or 1
    s += [ret(160 + i * 2, 51 - max(1, round(v / m * 8)), 1, max(1, round(v / m * 8)), '#1ECB8B' if v else '#1b2a33')
          for i, v in enumerate(ult)]
    s.append(ret(160, 43, 1, 8, '#ffffff', ' class="scan" opacity=".35"'))

    # equipe
    for i, p in enumerate(EQUIPE):
        sx = 6 + i * 41
        s.append(cadeira(sx, 82))
        s.append(personagem(p, sx + 1, 82))
        s += [ret(sx + 11, 94, 28, 2, '#a8714b'), ret(sx + 11, 96, 28, 1, '#7a4f33'),
              ret(sx + 12, 97, 2, 11, '#5e3c27'), ret(sx + 36, 97, 2, 11, '#5e3c27'),
              ret(sx + 26, 97, 9, 6, '#7a4f33'), ret(sx + 30, 99, 2, 1, '#c79a6b')]
        s += [ret(sx + 11, 93, 7, 1, '#c9cbe0'), ret(sx + 19, 77, 17, 13, '#2d2f45'),
              ret(sx + 20, 78, 15, 11, '#0b0c1a'), ret(sx + 26, 90, 3, 3, '#2d2f45'), ret(sx + 24, 93, 7, 1, '#2d2f45')]
        s.append(tela_codigo(sx + 20, 78, 15, 11, p['cor'], i + 1))
        s.append(ret(sx + 33, 88, 1, 1, p['cor'], ' class="led"'))
        if p.get('cafe'):
            s += [ret(sx + 36, 91, 2, 3, '#e9e6f5'), ret(sx + 38, 92, 1, 1, '#e9e6f5')]
            s += [ret(sx + 36 + k, 89, 1, 1, '#c8cbe8', f' class="vapor" style="animation-delay:{k * 1.2}s"')
                  for k in range(2)]
        s.append(acao(p, sx + 27, 60))
        s.append(texto(p['nome'], sx + 21, 112, p['cor'], 1, True))
        s.append(texto(p['setor'], sx + 21, 119, '#8b8fb5', 1, True))

    s.append(cachorro(0, 131))
    defs = ('<defs><filter id="brilho" x="-20%" y="-50%" width="140%" height="200%">'
            '<feGaussianBlur stdDeviation="1.3" result="b"/><feMerge><feMergeNode in="b"/>'
            '<feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
    return svg(W, H, 'Escritório em pixel art da CodeWave Systems com a equipe de IA trabalhando',
               CSS_COMUM + CSS_ESCRITORIO, defs + ''.join(s))


# ---------- ficha de estatísticas ----------
CSS_FICHA = '''
.cursor{animation:pisca 1s steps(1) infinite}
.enche{transform-box:fill-box;transform-origin:left;animation:enche 1.6s steps(16) both}
@keyframes enche{from{transform:scaleX(0)}}
.cresce{transform-box:fill-box;transform-origin:bottom;animation:cresce 1s steps(8) both}
@keyframes cresce{from{transform:scaleY(0)}}
'''


def moldura(x, y, w, h, cor):
    return (ret(x + 2, y, w - 4, 1, cor) + ret(x + 2, y + h - 1, w - 4, 1, cor) + ret(x, y + 2, 1, h - 4, cor) +
            ret(x + w - 1, y + 2, 1, h - 4, cor) + ret(x + 1, y + 1, 1, 1, cor) + ret(x + w - 2, y + 1, 1, 1, cor) +
            ret(x + 1, y + h - 2, 1, 1, cor) + ret(x + w - 2, y + h - 2, 1, 1, cor))


def ficha(d, hoje):
    W, H = 256, 100
    teal, cinza, branco, rosa, amarelo = '#3ff5d0', '#8b8fb5', '#e8e8ff', '#ff4f9a', '#ffd86b'
    s = [ret(0, 0, W, H, '#0f1023'), moldura(1, 1, W - 2, H - 2, teal), moldura(3, 3, W - 6, H - 6, '#23264a')]
    s += [texto('PLAYER', 9, 9, cinza), texto('PEDROVICTORRR', 37, 9, branco),
          ret(37 + largura('PEDROVICTORRR') + 2, 13, 3, 1, branco, ' class="cursor"'),
          texto('GUILD', 9, 17, cinza), texto('CODEWAVE SYSTEMS', 37, 17, teal),
          texto('CLASS', 9, 25, cinza), texto('FULL STACK DEV', 37, 25, amarelo)]
    lvl, xp = divmod(d['total'], 1000)
    s += [texto(f'LVL {lvl}', 9, 34, rosa, 2), ret(52, 36, 70, 6, '#23264a'),
          ret(53, 37, max(1, round(68 * xp / 1000)), 4, rosa, ' class="enche"'),
          texto(f'XP {xp}/1000', 53, 44, cinza)]
    linhas = [('NO ANO', fmt(d['ano']), 'TOTAL', fmt(d['total'])),
              ('STREAK', f'{d["atual"]}D', 'RECORDE', f'{d["recorde"]}D'),
              ('REPOS', str(d['repos']), 'STARS', str(d['estrelas'])),
              ('MELHOR DIA', str(d['melhor']), 'SEGUIDORES', str(d['seguidores']))]
    for i, (k1, v1, k2, v2) in enumerate(linhas):
        y = 54 + i * 8
        s += [texto(k1, 9, y, cinza), texto(v1, 66 - largura(v1), y, branco),
              texto(k2, 72, y, cinza), texto(v2, 124 - largura(v2), y, branco)]
    s.append(texto(f'ATUALIZADO {hoje:%d/%m/%Y}', 9, 89, '#4a4e78'))
    s.append(ret(131, 8, 1, 84, '#23264a'))

    s.append(texto('LINGUAGENS', 137, 9, teal))
    total = sum(v[0] for _, v in d['langs']) or 1
    for i, (nome, (tam, cor)) in enumerate(d['langs']):
        y, pct = 17 + i * 7, tam / total
        s += [texto(nome[:9], 137, y, cinza), ret(176, y, 54, 5, '#23264a'),
              ret(176, y, max(1, round(54 * pct)), 5, cor, f' class="enche" style="animation-delay:{i * .15:.2f}s"'),
              texto(f'{pct * 100:.0f}%', 248 - largura(f'{pct * 100:.0f}%'), y, branco)]
    s.append(texto('ATIVIDADE - 52 SEMANAS', 137, 55, teal))
    semanas = [sum(d['dias'][i:i + 7]) for i in range(max(0, len(d['dias']) - 364), len(d['dias']), 7)][-52:]
    m = max(semanas) or 1
    for i, v in enumerate(semanas):
        h = max(1, round(v / m * 26))
        s.append(ret(140 + i * 2, 90 - h, 1, h, rosa if v == m else teal,
                     f' class="cresce" style="animation-delay:{i * .02:.2f}s"'))
    return svg(W, H, 'Ficha de estatísticas do GitHub em pixel art', CSS_COMUM + CSS_FICHA, ''.join(s))


def svg(w, h, titulo, css, corpo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w * 4}" height="{h * 4}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{titulo}"><title>{titulo}</title>'
            f'<style>{css}</style>{corpo}</svg>\n')


def teste():
    d = {'2026-10-15': 1, '2026-10-16': 2, '2026-10-17': 0, '2026-10-18': 3, '2026-10-19': 0}
    assert streaks(d, '2026-10-19') == (1, 2)
    assert streaks({**d, '2026-10-19': 5}, '2026-10-19') == (2, 2)
    assert caminho([(0, 0), (1, 0), (3, 0)]) == 'M0 0h2v1h-2zM3 0h1v1h-1z'
    assert all(len(v) == 15 for v in F.values())
    print('ok')


if __name__ == '__main__':
    if '--teste' in sys.argv:
        teste()
        sys.exit()
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token:
        sys.exit('Defina GITHUB_TOKEN')
    dados = busca(token)
    os.makedirs('assets', exist_ok=True)
    with open('assets/escritorio.svg', 'w') as f:
        f.write(escritorio(dados))
    with open('assets/stats.svg', 'w') as f:
        f.write(ficha(dados, dt.datetime.now(dt.timezone(dt.timedelta(hours=-3)))))
    print(json.dumps({k: v for k, v in dados.items() if k != 'dias'}, ensure_ascii=False))
