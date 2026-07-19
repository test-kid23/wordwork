# -*- coding: utf-8 -*-
"""第3–16章 科技靛蓝 小红书卡片生成器（对齐 published/04-08 排版风格）。

渲染规则：
- 封面卡 / 内容卡(1080x1440, space-evenly) / 收尾卡。
- 内容块按 `---` 切分，每个块渲染为一张内容卡：
  · 块首 emoji 行 → 小号靛蓝强调标题(.section-title)
  · 📌 块（开场）→ 故事盒 + 清单
  · 🔸/✅/❌ 图标行 + 其说明 → 合并定义列表(.def-list，✅绿/❌红/⚠️橙)
  · 含 `→` 的行 → 链路图(.chain)
  · 含 `＞/＜` 或 优先级/顺序 语义 → 有序阶梯列表(.order)
  · 其余散文 → 故事盒(.story-box)
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
CHAPTERS = {
    'ch3-variable-system': '变量系统',
    'ch4-assertion-art': '断言艺术',
    'ch5-data-extract': '数据提取',
    'ch6-fixture': 'Fixture 妙用',
    'ch7-db-closure': '数据库闭环',
    'ch8-websocket': 'WebSocket 测试',
    'ch9-plugin-system': '插件系统',
    'ch10-interceptor': '拦截器',
    'ch11-report-log': '报告与日志',
    'ch12-architecture': '架构设计',
    'ch13-cicd': 'CI/CD 流水线',
    'ch14-platform': '平台化',
    'ch15-security': '测试安全',
    'ch16-mindset': '测试思维',
}

BULLET_ICONS = {'🔸', '✅', '❌', '▪️', '▶️', '➡️', '·', '•', '➜', '→'}
ORDER_KEYS = ['优先级', '顺序', '阶梯', '层级', '从低到高', '从高到低', '谁说了算', '覆盖规则']

BASE_CSS = """
  *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
  body { background:#e8ecf1; padding:24px; font-family:'Noto Sans SC',sans-serif; }
  .cards { display:flex; flex-direction:column; gap:16px; max-width:1080px; margin:0 auto; }
  .card { width:1080px; height:1440px; border-radius:24px; overflow:hidden; position:relative; flex-shrink:0; box-shadow:0 4px 24px rgba(30,27,75,0.10); }
  /* 封面 */
  .card-cover { background:linear-gradient(150deg,#dbeafe 0%,#bfdbfe 25%,#a5b4fc 55%,#818cf8 85%,#6366f1 100%); display:flex; flex-direction:column; justify-content:center; align-items:center; padding:48px 56px; text-align:center; position:relative; }
  .card-cover .tag { background:rgba(255,255,255,0.6); backdrop-filter:blur(8px); color:#4338ca; padding:12px 32px; border-radius:28px; font-size:36px; font-weight:700; margin-bottom:44px; }
  .card-cover h1 { font-size:88px; font-weight:900; color:#1e1b4b; line-height:1.25; margin-bottom:24px; max-width:900px; }
  .card-cover .subtitle { font-size:38px; color:#3730a3; font-weight:500; line-height:1.5; max-width:880px; }
  .watermark { position:absolute; bottom:36px; right:56px; font-size:22px; font-weight:500; z-index:3; }
  .card-cover .watermark { color:rgba(30,27,75,0.30); }
  .card-content .watermark { color:rgba(0,0,0,0.10); }
  .card-closing .watermark { color:rgba(30,27,75,0.18); }
  /* 内容卡 */
  .card-content { background:#fafafd; padding:60px 72px 60px; display:flex; flex-direction:column; position:relative; justify-content:space-evenly; }
  .card-content > *:not(.num) { position:relative; z-index:1; }
  .card-content .num { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:300px; font-weight:900; color:rgba(99,102,241,0.05); line-height:1; z-index:0; pointer-events:none; user-select:none; }
  .card-content .section { margin:0; }
  .section-title { font-size:32px; font-weight:800; color:#1e1b4b; margin-bottom:20px; padding-left:18px; border-left:6px solid #6366f1; line-height:1.35; }
  .section-title.warn { color:#b91c1c; border-left-color:#ef4444; }
  /* 故事盒 */
  .story-box { background:#f0f4ff; padding:26px 32px; border-radius:14px; font-size:25px; color:#374151; line-height:1.85; }
  .story-box .hl { background:#fee2e2; color:#dc2626; padding:1px 8px; border-radius:4px; font-weight:700; }
  .story-box .em { color:#4338ca; font-weight:700; }
  /* 开场清单 */
  .agenda-label { font-size:26px; font-weight:800; color:#4338ca; margin:6px 0 14px; }
  .checklist { display:flex; flex-direction:column; gap:12px; }
  .check-item { display:flex; align-items:center; gap:14px; background:#fff; border:1.5px solid #e0e7ff; border-left:4px solid #6366f1; padding:16px 24px; border-radius:12px; font-size:25px; color:#1e1b4b; font-weight:600; }
  .check-item .ci { font-size:28px; }
  /* 定义列表：图标 + 术语 + 说明 合并为单张行卡片（避免图标盒与说明盒割裂） */
  .def-list { display:flex; flex-direction:column; gap:16px; }
  .def-item { display:flex; align-items:flex-start; gap:18px; background:#fff; border:1.5px solid #e0e7ff; border-left:4px solid #6366f1; padding:20px 26px; border-radius:12px; }
  .def-item.green { border-left-color:#059669; }
  .def-item.red { border-left-color:#ef4444; }
  .def-item.amber { border-left-color:#f59e0b; }
  .def-item .di { font-size:32px; flex-shrink:0; line-height:1.3; }
  .def-item .dt { font-size:27px; font-weight:800; color:#1e1b4b; line-height:1.4; }
  .def-item .dd { font-size:23px; color:#4b5563; line-height:1.7; margin-top:6px; }
  /* 链路图 */
  .chain { display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; margin:8px 0; }
  .chain .step { background:linear-gradient(135deg,#6366f1,#818cf8); color:#fff; padding:14px 24px; border-radius:12px; font-size:25px; font-weight:700; }
  .chain .arr { font-size:28px; color:#a5b4fc; font-weight:700; }
  /* 有序阶梯 */
  .order { display:flex; flex-direction:column; }
  .order-item { display:flex; align-items:center; gap:18px; padding:18px 4px; }
  .order-item .on { width:56px; height:56px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:27px; font-weight:900; color:#fff; flex-shrink:0; background:#6366f1; }
  .order-item .ot { font-size:26px; color:#1e1b4b; font-weight:600; line-height:1.5; }
  .order-item .oa { text-align:center; color:#a5b4fc; font-size:28px; font-weight:700; margin:-2px 0; }
  .order-item:not(:last-child) { border-bottom:2px dashed #e0e7ff; }
  /* 收尾卡 */
  .card-closing { background:linear-gradient(150deg,#eef2ff 0%,#e0e7ff 50%,#c7d2fe 100%); display:flex; flex-direction:column; justify-content:center; align-items:center; padding:64px 72px; text-align:center; position:relative; }
  .card-closing h2 { font-size:46px; font-weight:900; color:#1e1b4b; margin-bottom:22px; line-height:1.4; }
  .card-closing .golden { background:rgba(255,255,255,0.7); padding:24px 44px; border-radius:18px; font-size:30px; color:#4338ca; margin-bottom:26px; line-height:1.7; font-weight:800; }
  .card-closing .cta-ask { font-size:26px; color:#4f46e5; line-height:1.9; margin-bottom:18px; font-weight:600; }
  .card-closing .save-tip { font-size:26px; color:#4f46e5; font-weight:800; margin-bottom:24px; }
  .card-closing .hashtags { font-size:21px; color:rgba(67,56,202,0.45); line-height:2; }
  /* 下载按钮 / 工具条 */
  .dl-btn { position:absolute; top:20px; right:20px; z-index:10; background:rgba(30,27,75,0.45); color:#fff; border:none; padding:10px 20px; border-radius:20px; font-size:20px; cursor:pointer; font-family:'Noto Sans SC',sans-serif; backdrop-filter:blur(4px); }
  .dl-btn:hover { background:rgba(30,27,75,0.65); }
  .toolbar { position:sticky; top:8px; z-index:100; max-width:1080px; margin:0 auto 12px; display:flex; gap:12px; justify-content:center; }
  .toolbar button { background:#6366f1; color:#fff; border:none; padding:12px 32px; border-radius:24px; font-size:22px; font-weight:700; cursor:pointer; font-family:'Noto Sans SC',sans-serif; }
  .toolbar button:hover { background:#4f46e5; }
"""


def esc(s):
    return html.escape(s, quote=False)


def is_bullet(line):
    s = line.strip()
    if not s:
        return False
    if s[0] in BULLET_ICONS:
        return True
    # 处理 "✅ xxx" / "🔸 xxx"
    return False


def is_emoji_head(line):
    s = line.strip()
    if not s:
        return False
    if s[0] in BULLET_ICONS:
        return False
    # 首字符非中文（emoji/符号）→ 视为小标题
    return not ('\u4e00' <= s[0] <= '\u9fff')


def first_icon(line):
    s = line.strip()
    if not s:
        return '', s
    for ic in ['🔸', '✅', '❌', '▪️', '▶️', '➡️', '➜']:
        if s.startswith(ic):
            return ic, s[len(ic):].strip()
    return '', s


def parse_segments(body):
    """body: 列表（不含块首标题）。返回 segment 列表。

    关键：图标行(🔸/✅/❌)紧跟着的说明文字，合并到同一个 deflist 项，
    避免被切成「小图标盒 + 故事盒」两个割裂的块。
    """
    segs = []
    cur = None

    def flush():
        nonlocal cur
        if cur is not None:
            segs.append(cur)
        cur = None

    i, n = 0, len(body)
    while i < n:
        ls = body[i].strip()
        if not ls:
            i += 1
            continue
        if is_bullet(ls):
            # 收集 bullet + 其后说明行，直到空行/下一个 bullet/chain/order
            group = [ls]
            j = i + 1
            while j < n:
                nl = body[j].strip()
                if not nl:
                    break
                if is_bullet(nl) or ('→' in nl and len(nl) < 70) or ('＞' in nl or '＜' in nl):
                    break
                group.append(nl)
                j += 1
            if cur is None or cur[0] != 'deflist':
                flush()
                cur = ('deflist', [])
            cur[1].append(group)
            i = j
            continue
        if '→' in ls and len(ls) < 70:
            if cur is None or cur[0] != 'chain':
                flush()
                cur = ('chain', [])
            cur[1].append(ls)
            i += 1
            continue
        if '＞' in ls or '＜' in ls:
            if cur is None or cur[0] != 'order':
                flush()
                cur = ('order', [])
            cur[1].append(ls)
            i += 1
            continue
        # story
        if cur is None or cur[0] != 'story':
            flush()
            cur = ('story', [])
        cur[1].append(ls)
        i += 1
    flush()
    return segs


def render_story(lines):
    parts = []
    for ln in lines:
        parts.append(esc(ln.strip()))
    return f'<div class="story-box">{"<br>".join(parts)}</div>'


def render_deflist(groups):
    items = []
    for g in groups:
        head = g[0]
        desc = g[1:]
        ic, tx = first_icon(head)
        cls = ''
        if ic == '✅':
            cls = ' green'
        elif ic == '❌':
            cls = ' red'
        elif ic in ('⚠️', '🔥'):
            cls = ' amber'
        term = esc(tx)
        dd = ''
        if desc:
            dd = f'<div class="dd">{"<br>".join(esc(d) for d in desc)}</div>'
        items.append(
            f'<div class="def-item{cls}"><span class="di">{esc(ic) if ic else "🔸"}</span>'
            f'<div><div class="dt">{term}</div>{dd}</div></div>'
        )
    return f'<div class="def-list">{"".join(items)}</div>'


def render_chain(boxes):
    # 多行 → 合并为一个链路
    steps = []
    for ln in boxes:
        for part in ln.split('→'):
            p = part.strip()
            if p:
                steps.append(p)
    out = []
    for i, s in enumerate(steps):
        if i > 0:
            out.append('<span class="arr">→</span>')
        out.append(f'<span class="step">{esc(s)}</span>')
    return f'<div class="chain">{"".join(out)}</div>'


def render_order(lines):
    items = []
    n = 0
    for ln in lines:
        t = ln.strip().lstrip('＞').lstrip('＜').strip()
        if not t:
            continue
        n += 1
        if n > 1:
            items.append('<div class="oa">▼</div>')
        items.append(
            f'<div class="order-item"><div class="on">{n}</div>'
            f'<div class="ot">{esc(t)}</div></div>'
        )
    return f'<div class="order">{"".join(items)}</div>'


def render_block(block_lines, is_intro=False):
    if is_intro:
        # 开场：散文 + 📌 清单
        prose, agenda, checks = [], None, []
        for l in block_lines.splitlines():
            ls = l.strip()
            if not ls:
                continue
            if ls.startswith('📌') or ls.startswith('📍'):
                agenda = ls.lstrip('📌').lstrip('📍').strip()
            elif ls[0] in ('✅', '🔸') and agenda is not None:
                checks.append(ls)
            else:
                if agenda is None:
                    prose.append(ls)
                else:
                    checks.append(ls) if ls[0] in ('✅', '🔸') else prose.append(ls)
        # 没有清单项时，把 📌 行并入正文，避免孤立的空标题
        if agenda and not checks:
            prose.append(agenda)
            agenda = None
        inner = []
        if prose:
            inner.append(render_story(prose))
        if agenda:
            inner.append(f'<div class="agenda-label">📌 {esc(agenda)}</div>')
        if checks:
            items = []
            for c in checks:
                ic, tx = first_icon(c)
                items.append(
                    f'<div class="check-item"><span class="ci">{esc(ic) if ic else "✅"}</span>'
                    f'<span>{esc(tx)}</span></div>'
                )
            inner.append(f'<div class="checklist">{"".join(items)}</div>')
        return ''.join(inner)

    # 普通块
    lines = [l.strip() for l in block_lines.splitlines() if l.strip()]
    heading = None
    body = lines
    if lines and is_emoji_head(lines[0]):
        heading = lines[0].strip()
        body = lines[1:]
    warn = bool(heading and ('不推荐' in heading or '坑' in heading or '⚠' in heading or '罪' in heading))
    segs = parse_segments(body)
    inner = []
    if heading:
        cls = ' warn' if warn else ''
        inner.append(f'<div class="section"><div class="section-title{cls}">{esc(heading)}</div></div>')
    for typ, data in segs:
        if typ == 'story':
            inner.append(render_story(data))
        elif typ == 'deflist':
            inner.append(render_deflist(data))
        elif typ == 'chain':
            inner.append(render_chain(data))
        elif typ == 'order':
            inner.append(render_order(data))
    return ''.join(inner)


def render_closing(block_lines, chapter_tag):
    golden, cta, save, tags = [], [], [], ''
    cur = None
    for l in block_lines.splitlines():
        ls = l.strip()
        if not ls:
            continue
        if ls.startswith('🎯'):
            cur = 'g'; golden = [ls.lstrip('🎯').strip()]; continue
        if ls.startswith('💬'):
            cur = 'c'; cta = [ls.lstrip('💬').strip()]; continue
        if ls.startswith('⭐'):
            cur = 's'; save = [ls.lstrip('⭐').strip()]; continue
        if ls.startswith('#'):
            cur = None; tags = ls.strip(); continue
        # 同块续行
        if cur == 'g':
            golden.append(ls)
        elif cur == 'c':
            cta.append(ls)
        elif cur == 's':
            save.append(ls)
    inner = []
    if golden:
        inner.append(f'<div class="golden">{"<br>".join(esc(x) for x in golden)}</div>')
    if cta:
        inner.append(f'<div class="cta-ask">💬 {"<br>".join(esc(x) for x in cta)}</div>')
    if save:
        inner.append(f'<div class="save-tip">⭐ {"<br>".join(esc(x) for x in save)}</div>')
    if tags:
        inner.append(f'<div class="hashtags">{esc(tags)}</div>')
    inner.append('<div class="watermark">@Testkid · 2026</div>')
    return ('<div class="card card-closing">' + ''.join(inner) + '</div>')


def split_articles(text):
    arts = []
    cur = []
    for line in text.splitlines():
        if line.startswith('## 第') and '篇' in line:
            if cur:
                arts.append('\n'.join(cur))
            cur = [line]
        else:
            cur.append(line)
    if cur:
        arts.append('\n'.join(cur))
    return arts


def parse_note_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    articles = []
    for art in split_articles(text):
        if '总结' in art[:30] or art.lstrip().startswith('## 📌'):
            continue
        m = re.search(r'第(\d+)篇', art)
        if not m:
            continue
        num = int(m.group(1))
        # 标题
        hm = re.search(r'## 第\d+篇[ ·]*(.*)', art)
        title = hm.group(1).strip() if hm else f'第{num}篇'
        # 切块
        blocks = [b.strip() for b in re.split(r'\n---\n', art) if b.strip()]
        # 找收尾块：只有真正的结尾才含 💬/⭐（中间小节的 🎯 标题不含这些）
        closing_idx = None
        for i, b in enumerate(blocks):
            if '💬' in b or '⭐' in b:
                closing_idx = i
                break
        intro = blocks[0] if blocks else ''
        # 去掉 intro 里的 `## 第N篇` 标题行（已在 title 提取）
        intro = '\n'.join(l for l in intro.splitlines()
                          if l.strip() and not l.strip().startswith('## '))
        content = blocks[1:closing_idx] if closing_idx is not None else blocks[1:]
        closing = blocks[closing_idx] if closing_idx is not None else ''
        articles.append({
            'num': num, 'title': title, 'intro': intro,
            'content': content, 'closing': closing,
        })
    return articles


def build_html(article, chapter_tag):
    num = article['num']
    title = article['title']
    # 封面副标题：intro 前两句
    intro_lines = [l.strip() for l in article['intro'].splitlines() if l.strip() and not l.strip().startswith('📌')]
    subtitle = ' '.join(intro_lines[:2]) if intro_lines else chapter_tag
    cover = (
        f'<div class="card card-cover">'
        f'<div class="tag">{esc(chapter_tag)}</div>'
        f'<h1>{esc(title)}</h1>'
        f'<div class="subtitle">{esc(subtitle)}</div>'
        f'<div class="watermark">@Testkid · 2026</div>'
        f'</div>'
    )
    cards = [cover]
    card_names = [f'{num}-cover']
    ci = 0

    def add_card(body_html):
        nonlocal ci
        ci += 1
        card = (
            f'<div class="card card-content">'
            f'<div class="num">{ci:02d}</div>'
            f'{body_html}'
            f'<div class="watermark">@Testkid</div>'
            f'</div>'
        )
        cards.append(card)
        card_names.append(f'{num}-c{ci}')

    # 开场块（钩子故事 + 📌 清单）作为第一张内容卡
    if article['intro'].strip():
        add_card(render_block(article['intro'], is_intro=True))

    # 正文块上下文归并：相邻小节若合并后行数不超阈值则合并，
    # 既减少满屏薄卡，又保证单卡不超出 1440px（避免裁切）。
    def _blk_lines(blk):
        return sum(1 for l in blk.splitlines() if l.strip())

    def smart_group(blocks, cap=16):
        groups, cur, curh = [], [], 0
        for b in blocks:
            h = _blk_lines(b)
            if cur and curh + h > cap:
                groups.append(cur)
                cur, curh = [b], h
            else:
                cur.append(b)
                curh += h
        if cur:
            groups.append(cur)
        return groups

    for grp in smart_group(article['content'], cap=16):
        body = ''.join(render_block(b, is_intro=False) for b in grp)
        add_card(body)
    if article['closing']:
        cards.append(render_closing(article['closing'], chapter_tag))
        card_names.append(f'{num}-closing')

    names_js = '[' + ','.join(f"'{n}'" for n in card_names) + ']'
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{num} · 小红书卡片 · 科技靛蓝</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>{BASE_CSS}</style>
</head>
<body>
<div class="toolbar"><button onclick="downloadAll()">📥 一键下载全部卡片</button></div>
<div class="cards">
{''.join(cards)}
</div>
<script>const names = {names_js};</script>
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script>
  document.querySelectorAll('.card').forEach((card, i) => {{
    const btn = document.createElement('button');
    btn.className = 'dl-btn';
    btn.textContent = '📥 下载';
    btn.setAttribute('data-dl-btn', 'true');
    btn.onclick = async (e) => {{
      e.stopPropagation();
      btn.style.display = 'none';
      const canvas = await html2canvas(card, {{ scale: 2, useCORS: true, backgroundColor: null }});
      btn.style.display = '';
      const link = document.createElement('a');
      link.download = names[i] + '.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
    }};
    card.appendChild(btn);
  }});
  async function downloadAll() {{
    const cards = document.querySelectorAll('.card');
    for (let i = 0; i < cards.length; i++) {{
      const btn = cards[i].querySelector('[data-dl-btn]');
      if (btn) btn.style.display = 'none';
      const canvas = await html2canvas(cards[i], {{ scale: 2, useCORS: true, backgroundColor: null }});
      if (btn) btn.style.display = '';
      const link = document.createElement('a');
      link.download = names[i] + '.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
      await new Promise(r => setTimeout(r, 600));
    }}
  }}
</script>
</body>
</html>"""


def main():
    total = 0
    for d, tag in CHAPTERS.items():
        dpath = os.path.join(ROOT, d)
        if not os.path.isdir(dpath):
            continue
        for fn in sorted(os.listdir(dpath)):
            if not fn.endswith('-notes.md'):
                continue
            arts = parse_note_file(os.path.join(dpath, fn))
            for art in arts:
                out = build_html(art, tag)
                out_path = os.path.join(dpath, f"{art['num']}-cards.html")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(out)
                total += 1
    print(f'已生成 {total} 篇卡片')


if __name__ == '__main__':
    main()
