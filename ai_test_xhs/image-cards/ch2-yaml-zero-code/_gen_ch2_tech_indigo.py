# -*- coding: utf-8 -*-
"""生成第2章画布卡片（科技靛蓝 Tech Indigo 风格），直接输出到章节目录。"""
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

STYLE = """*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{background:#e8ecf1;padding:24px;font-family:'Noto Sans SC',sans-serif}
.toolbar{position:sticky;top:8px;z-index:100;max-width:1080px;margin:0 auto 12px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.toolbar button{background:#6366f1;color:#fff;border:none;padding:12px 28px;border-radius:24px;font-size:22px;font-weight:700;cursor:pointer;font-family:'Noto Sans SC',sans-serif;transition:background .2s}
.toolbar button:hover{background:#4f46e5}
.cards{display:flex;flex-direction:column;gap:16px;max-width:1080px;margin:0 auto}
.card{width:1080px;height:1440px;border-radius:24px;overflow:hidden;position:relative;flex-shrink:0;box-shadow:0 4px 24px rgba(30,27,75,0.10)}
.card-cover{background:linear-gradient(150deg,#dbeafe 0%,#bfdbfe 25%,#a5b4fc 55%,#818cf8 85%,#6366f1 100%);display:flex;flex-direction:column;justify-content:center;align-items:center;padding:56px;text-align:center;position:relative}
.card-cover .tag{background:rgba(255,255,255,0.6);backdrop-filter:blur(8px);color:#4338ca;padding:12px 34px;border-radius:28px;font-size:34px;font-weight:700;margin-bottom:48px}
.card-cover h1{font-size:82px;font-weight:900;color:#1e1b4b;line-height:1.25;margin-bottom:24px;max-width:880px}
.card-cover .subtitle{font-size:36px;color:#3730a3;font-weight:500;line-height:1.5}
.watermark{position:absolute;bottom:40px;right:64px;font-size:22px;color:rgba(30,27,75,0.22);font-weight:500;z-index:2}
.card-content{background:#fafafd;padding:60px 72px;display:flex;flex-direction:column;position:relative}
.card-content .num{font-size:84px;font-weight:900;color:rgba(99,102,241,0.12);position:absolute;top:32px;right:60px;line-height:1}
.section-title{font-size:42px;font-weight:900;color:#1e1b4b;margin-bottom:30px;position:relative;z-index:2;padding-left:18px;border-left:5px solid #6366f1}
.scene-row{display:flex;align-items:center;gap:16px;background:#f0f4ff;border-radius:12px;padding:18px 24px;margin-bottom:14px}
.scene-row .icon{font-size:34px}
.scene-row .text{font-size:25px;color:#374151;line-height:1.7}
.scene-row .hl{background:#fee2e2;color:#dc2626;padding:2px 8px;border-radius:4px;font-weight:700}
.chain-h{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;margin:8px 0 20px}
.chain-h .step{background:linear-gradient(135deg,#6366f1,#818cf8);color:#fff;padding:10px 18px;border-radius:10px;font-size:22px;font-weight:700}
.chain-h .arr{font-size:24px;color:#a5b4fc}
.col2{display:flex;gap:20px;flex:1}
.col2>div{flex:1;padding:26px 24px;border-radius:16px}
.col2 .bad{background:#fef2f2;border:1.5px solid #fecaca}
.col2 .good{background:#ecfdf5;border:1.5px solid #a7f3d0}
.col2 h3{font-size:26px;margin-bottom:12px}
.col2 .bad h3{color:#dc2626}.col2 .good h3{color:#059669}
.col2 p{font-size:22px;color:#4b5563;line-height:1.7}
.metaphor{background:linear-gradient(135deg,#eff6ff,#eef2ff);padding:18px 28px;border-radius:12px;font-size:24px;color:#4338ca;text-align:center;line-height:1.7;margin-top:16px}
.tbl{width:100%;border-collapse:separate;border-spacing:0;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.05);flex:1}
.tbl th{background:#6366f1;color:#fff;padding:16px 20px;font-size:23px;font-weight:700}
.tbl td{background:#fff;padding:16px 20px;font-size:22px;color:#374151;line-height:1.5;border-bottom:1px solid #f3f4f6}
.tbl tr:last-child td{border-bottom:none}
.tbl td:first-child{font-weight:700;color:#4338ca;width:160px}
.demo-grid{display:flex;flex-direction:column;gap:16px;flex:1}
.demo-card{display:flex;align-items:flex-start;gap:22px;background:#fff;border:1.5px solid #e0e7ff;border-radius:16px;padding:24px 28px;box-shadow:0 2px 8px rgba(30,27,75,0.04)}
.demo-card .dc-icon{font-size:38px;width:56px;height:56px;border-radius:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:#eef2ff}
.demo-card .dc-num{font-size:16px;font-weight:800;color:#6366f1;margin-bottom:4px;letter-spacing:1px}
.demo-card .dc-title{font-size:27px;font-weight:900;color:#1e1b4b;margin-bottom:6px}
.demo-card .dc-desc{font-size:22px;color:#4b5563;line-height:1.6}
.demo-card .dc-tag{display:inline-block;font-size:17px;background:#eef2ff;color:#4338ca;padding:3px 12px;border-radius:10px;margin-top:8px;font-weight:700}
.tag-display{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}
.tag-badge{font-size:22px;font-weight:700;padding:8px 20px;border-radius:16px;border:2px solid}
.tag-s{background:rgba(99,102,241,0.1);border-color:#a5b4fc;color:#4338ca}
.tag-p{background:rgba(236,72,153,0.1);border-color:#f9a8d4;color:#be185d}
.tag-l{background:rgba(16,185,129,0.1);border-color:#6ee7b7;color:#047857}
.dim-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;flex:1;align-content:center}
.dim-card{background:#fff;border:1.5px solid #e0e7ff;border-radius:16px;padding:28px 22px;text-align:center;box-shadow:0 2px 8px rgba(30,27,75,0.04)}
.dim-card .dim-icon{font-size:44px;margin-bottom:10px}
.dim-card .dim-title{font-size:25px;font-weight:800;color:#1e1b4b;margin-bottom:8px}
.dim-card .dim-desc{font-size:20px;color:#4b5563}
.sc-list{display:flex;flex-direction:column;gap:16px;flex:1;justify-content:space-evenly}
.sc-card{display:flex;align-items:flex-start;gap:20px;background:#fff;border:1.5px solid #e0e7ff;border-radius:16px;padding:24px 28px;box-shadow:0 2px 8px rgba(30,27,75,0.04)}
.sc-num{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:900;color:#fff;flex-shrink:0;background:#6366f1}
.sc-body{flex:1}
.sc-title{font-size:28px;font-weight:800;color:#1e1b4b;margin-bottom:6px}
.sc-desc{font-size:22px;color:#4b5563}
.code-snippet{font-size:21px;font-family:'SF Mono','Consolas',monospace;color:#4338ca;background:#eef2ff;padding:8px 14px;border-radius:8px;border:1px dashed #a5b4fc;margin-top:8px;display:inline-block}
.core-msg{text-align:center;margin-top:auto;padding-top:24px;font-size:30px;font-weight:900;color:#1e1b4b}
.core-msg .em{color:#6366f1}
.vs-table{flex:1;display:flex;flex-direction:column}
.vs-row{display:flex;align-items:center;border-bottom:1px solid #eef2ff;padding:20px 0}
.vs-row:last-child{border-bottom:none}
.vs-dim{width:170px;font-size:24px;font-weight:700;color:#4b5563;flex-shrink:0}
.vs-bad{flex:1;background:#fef2f2;padding:14px 22px;border-radius:14px;font-size:23px;color:#4b5563}
.vs-good{flex:1;background:#ecfdf5;padding:14px 22px;border-radius:14px;font-size:23px;color:#1e1b4b;margin-left:16px}
.vs-icon{width:36px;text-align:center;color:#6366f1;font-size:22px;flex-shrink:0}
.speech-box{flex:1;display:flex;flex-direction:column;gap:18px;justify-content:center}
.speech-item{background:#fff;border:1.5px solid #e0e7ff;border-radius:16px;padding:22px 26px;box-shadow:0 2px 8px rgba(30,27,75,0.04)}
.speech-item .who{font-size:23px;font-weight:800;color:#6366f1;margin-bottom:6px}
.speech-item .say{font-size:25px;color:#1e1b4b;font-weight:500;line-height:1.6}
.step-nums{display:flex;gap:18px;flex:1;align-items:stretch}
.step-box{flex:1;background:#fff;border:1.5px solid #e0e7ff;border-radius:18px;padding:28px 22px;text-align:center;box-shadow:0 2px 8px rgba(30,27,75,0.04);display:flex;flex-direction:column;gap:8px}
.step-box .sn{font-size:22px;font-weight:800;color:#6366f1}
.step-box .st{font-size:27px;font-weight:800;color:#1e1b4b}
.step-box .sd{font-size:21px;color:#4b5563;line-height:1.5}
.code-show{font-family:'SF Mono','Consolas',monospace;font-size:22px;line-height:1.8;background:#1e1b4b;color:#e0e7ff;padding:28px 34px;border-radius:16px;flex:1;white-space:pre-wrap;box-shadow:0 3px 12px rgba(30,27,75,0.2)}
.result-show{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.result-show .big-check{font-size:130px;color:#059669;line-height:1}
.result-show .pass-line{font-size:30px;font-weight:700;color:#059669;margin:12px 0}
.result-show .timer{font-size:26px;color:#4b5563;margin-top:14px}
.why-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1}
.why-card{background:#fff;border:1.5px solid #e0e7ff;border-radius:16px;padding:28px 24px;box-shadow:0 2px 8px rgba(30,27,75,0.04);display:flex;flex-direction:column;gap:10px}
.why-card .wc-icon{font-size:40px}
.why-card .wc-title{font-size:26px;font-weight:800;color:#1e1b4b}
.why-card .wc-desc{font-size:21px;color:#4b5563;line-height:1.6}
.flow-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;gap:18px}
.flow-step{display:flex;align-items:center;gap:14px}
.flow-step .fs-box{flex:1;background:#fff;border:1.5px solid #e0e7ff;border-radius:16px;padding:24px 20px;text-align:center;box-shadow:0 2px 8px rgba(30,27,75,0.04)}
.flow-step .fs-num{font-size:20px;color:#9ca3af;margin-bottom:6px}
.flow-step .fs-title{font-size:25px;font-weight:800;color:#1e1b4b;margin-bottom:4px}
.flow-step .fs-desc{font-size:20px;color:#4b5563}
.flow-step .fs-arrow{font-size:28px;color:#a5b4fc;flex-shrink:0}
.diff-box{font-family:'SF Mono','Consolas',monospace;font-size:25px;line-height:1.9;background:#1e1b4b;color:#e0e7ff;padding:34px 42px;border-radius:16px;flex:1;display:flex;align-items:center;justify-content:center;box-shadow:0 3px 12px rgba(30,27,75,0.2)}
.diff-box .red{color:#fca5a5}.diff-box .green{color:#6ee7b7}
.dir-tree{font-family:'SF Mono','Consolas',monospace;font-size:24px;line-height:1.9;background:#fff;border:1.5px solid #e0e7ff;border-radius:16px;padding:30px 38px;flex:1;color:#1e1b4b;box-shadow:0 2px 8px rgba(30,27,75,0.04)}
.dir-tree .dir{color:#4338ca;font-weight:700}
.dir-tree .file{color:#6366f1;padding-left:14px}
.benefit-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;flex:1}
.bf-card{background:#fff;border:1.5px solid #e0e7ff;border-radius:16px;padding:28px 24px;box-shadow:0 2px 8px rgba(30,27,75,0.04);display:flex;flex-direction:column;gap:10px}
.bf-card .bf-icon{font-size:40px}
.bf-card .bf-title{font-size:26px;font-weight:800;color:#1e1b4b}
.bf-card .bf-desc{font-size:21px;color:#4b5563;line-height:1.6}
.compare-wrap{display:flex;gap:20px;flex:1}
.cp-panel{flex:1;display:flex;flex-direction:column;padding:30px 32px;border-radius:18px;border:1.5px solid}
.cp-bad{background:#fef2f2;border-color:#fecaca}.cp-good{background:#ecfdf5;border-color:#a7f3d0}
.cp-head{font-size:27px;font-weight:900;display:flex;align-items:center;gap:12px;margin-bottom:16px}
.cp-head .mk{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:900;flex-shrink:0}
.mk-x{background:#fee2e2;color:#dc2626;border:2px solid #fca5a5}
.mk-ok{background:#d1fae5;color:#059669;border:2px solid #6ee7b7}
.cp-body{font-size:22px;color:#4b5563;line-height:1.8;flex:1}
.cp-body .code-box{font-family:'SF Mono','Consolas',monospace;background:rgba(99,102,241,0.08);padding:8px 14px;border-radius:8px;margin:6px 0;color:#4338ca;font-size:21px}
.card-closing{background:linear-gradient(150deg,#eef2ff 0%,#e0e7ff 50%,#c7d2fe 100%);display:flex;flex-direction:column;justify-content:center;align-items:center;padding:64px 72px;text-align:center;position:relative}
.card-closing h2{font-size:46px;font-weight:900;color:#1e1b4b;margin-bottom:24px;line-height:1.4}
.card-closing .preview{background:rgba(255,255,255,0.7);padding:22px 44px;border-radius:18px;font-size:28px;color:#4338ca;margin-bottom:28px;line-height:1.6}
.card-closing .cta{font-size:25px;color:#4338ca;line-height:1.9}
.card-closing .hashtags{font-size:21px;color:rgba(67,56,202,0.45);margin-top:24px;line-height:2}
.card-closing .bubble-q{position:relative;background:#fff;border:3px solid #6366f1;border-radius:32px;padding:42px 50px;margin-bottom:42px;max-width:720px;box-shadow:0 6px 18px rgba(99,102,241,0.15)}
.card-closing .bubble-q .q-text{font-size:40px;font-weight:900;color:#1e1b4b;line-height:1.4}
.dl-btn{position:absolute;top:20px;right:20px;z-index:10;background:rgba(30,27,75,0.45);color:#fff;border:none;padding:10px 20px;border-radius:20px;font-size:20px;cursor:pointer;font-family:'Noto Sans SC',sans-serif;transition:background .2s;backdrop-filter:blur(4px)}
.dl-btn:hover{background:rgba(30,27,75,0.65)}"""

JS = """<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script>
  document.querySelectorAll('.card').forEach((card, i) => {
    const btn = document.createElement('button');
    btn.className = 'dl-btn';
    btn.textContent = '📥 下载';
    btn.setAttribute('data-dl-btn', 'true');
    btn.onclick = async (e) => {
      e.stopPropagation();
      btn.style.display = 'none';
      const canvas = await html2canvas(card, { scale: 2, useCORS: true, backgroundColor: null });
      btn.style.display = '';
      const link = document.createElement('a');
      link.download = names[i] + '.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
    };
    card.appendChild(btn);
  });
  async function downloadAll() {
    const cards = document.querySelectorAll('.card');
    for (let i = 0; i < cards.length; i++) {
      const btn = cards[i].querySelector('[data-dl-btn]');
      if (btn) btn.style.display = 'none';
      const canvas = await html2canvas(cards[i], { scale: 2, useCORS: true, backgroundColor: null });
      if (btn) btn.style.display = '';
      const link = document.createElement('a');
      link.download = names[i] + '.png';
      link.href = canvas.toDataURL('image/png');
      link.click();
      await new Promise(r => setTimeout(r, 600));
    }
  }
</script>"""

SITE = "@Testkid"

# ---- 各篇内容 ----
bodies = {}

# 11 - 10分钟写完整CRUD
bodies["11-cards.html"] = {
"names": ["11-cover-crud","11-crud-chain","11-crud-compare","11-extract","11-ending"],
"html": """
<div class="card card-cover">
  <div class="tag">零代码测试 · 实战篇</div>
  <h1>10分钟写<span style="color:#4338ca">完整CRUD</span></h1>
  <div class="subtitle">从空白编辑器到四个case全通过</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">01</div>
  <div class="section-title">⛓️ CRUD 四步链</div>
  <div class="chain-h">
    <div class="step">创建 · POST</div><div class="arr">→</div>
    <div class="step">查询 · GET</div><div class="arr">→</div>
    <div class="step">更新 · PUT</div><div class="arr">→</div>
    <div class="step">删除 · DELETE</div>
  </div>
  <div style="text-align:center;font-size:28px;color:#4b5563;margin-top:8px">全部在一个 YAML 文件里 · user_id 自动串联</div>
  <div class="metaphor">创建 → 查询 → 更新 → 删除 · 一条链跑完 🎯</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">02</div>
  <div class="section-title">⚡ 两种写法 · 一套CRUD</div>
  <div class="col2">
    <div class="bad"><h3>❌ Python</h3>
      <p>conftest.py / test_create.py / test_query.py / test_update.py / test_delete.py</p>
      <p style="margin-top:10px;color:#dc2626;font-weight:700">5个文件 · ~150行</p>
      <p>变量靠全局传 · import一堆 · 易改漏</p>
    </div>
    <div class="good"><h3>✅ YAML</h3>
      <p>就一个 users.yaml</p>
      <p style="margin-top:10px;color:#059669;font-weight:700">1个文件 · ~60行</p>
      <p>extract自动串联user_id · 零import · 改一个地方就行</p>
    </div>
  </div>
  <div class="metaphor">不是行数的差距 💡 是<span style="color:#4338ca;font-weight:700">搞错一个变量</span>就能让你找半小时</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">03</div>
  <div class="section-title">🪄 核心魔法：extract 变量传递</div>
  <div class="scene-row"><div class="icon">1️⃣</div><div class="text"><span class="hl">extract: user_id</span> · POST 创建用户后，从响应体把 user_id 抠出来存好</div></div>
  <div class="scene-row"><div class="icon">2️⃣</div><div class="text"><span class="hl">GET /users/{{user_id}}</span> · 直接用花括号引用刚存的 id，查到这个用户</div></div>
  <div class="scene-row"><div class="icon">3️⃣</div><div class="text"><span class="hl">PUT /users/{{user_id}}</span> · 改邮箱密码都没问题</div></div>
  <div class="scene-row"><div class="icon">4️⃣</div><div class="text"><span class="hl">DELETE /users/{{user_id}}</span> · 删完不留脏数据，库干干净净</div></div>
  <div class="metaphor">全程没有一行变量赋值代码 · 自动串起来 🔗</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-closing">
  <div class="bubble-q"><div class="q-text">你用Python写一套CRUD<br>需要多长时间？</div></div>
  <div class="cta">评论区说说 👇</div>
  <div class="preview">下篇预告<br>数据驱动测试：一条模板 × N组数据 🔥</div>
  <div class="hashtags">#CRUD测试 #接口自动化 #YAML #零代码 #软件测试</div>
  <div class="watermark">__SITE__</div>
</div>
""".replace("__SITE__", SITE)}

# 12 - 数据驱动
bodies["12-cards.html"] = {
"names": ["12-cover-dd","12-old-copy","12-datadriven","12-scenarios","12-ending"],
"html": """
<div class="card card-cover">
  <div class="tag">零代码测试 · 进阶篇</div>
  <h1>一条模板 × <span style="color:#4338ca">N组数据</span><br>= N个用例</h1>
  <div class="subtitle">数据驱动测试 · 告别复制粘贴</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">01</div>
  <div class="section-title">🤯 传统做法：拷贝 × N</div>
  <div class="compare-wrap">
    <div class="cp-panel cp-bad">
      <div class="cp-head"><div class="mk mk-x">✕</div>复制粘贴</div>
      <div class="cp-body">同个接口查不同 user_id
        <div class="code-box">case 1: 查 user_id=1</div>
        <div class="code-box">case 2: 查 user_id=2</div>
        <div class="code-box">case 3: 查 user_id=3</div>
        <div style="text-align:center;font-size:36px;margin:8px 0">...</div>
        <div class="code-box">case 50: 查 user_id=50</div>
        <div style="text-align:center;color:#dc2626;font-weight:700;margin-top:12px">50份拷贝 = 维护噩梦 😵</div>
      </div>
    </div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">02</div>
  <div class="section-title">💡 data_driven 一行搞定</div>
  <div class="compare-wrap">
    <div class="cp-panel cp-good">
      <div class="cp-head"><div class="mk mk-ok">✓</div>模板 + 参数列表</div>
      <div class="cp-body">
        <div class="code-box">parameters:</div>
        <div class="code-box">  - {user_id:1, expect:"张三"}</div>
        <div class="code-box">  - {user_id:2, expect:"李四"}</div>
        <div class="code-box">  - {user_id:3, expect:"王五"}</div>
        <div style="margin-top:14px;text-align:center;color:#059669;font-weight:700">一个模板自动渲染 → 3个case自动生成</div>
        <div style="text-align:center;background:#fff;padding:12px 20px;border:2px solid #a7f3d0;border-radius:14px;margin-top:12px;color:#059669;font-weight:700">一行配置 · 不是50份拷贝 ✨</div>
      </div>
    </div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">03</div>
  <div class="section-title">🔥 哪些场景最值</div>
  <div class="demo-grid">
    <div class="demo-card"><div class="dc-icon">📄</div><div class="dc-body"><div class="dc-num">SCENE 01</div><div class="dc-title">分页测试</div><div class="dc-desc">page=1,2,3,4,5 一次性跑完所有分页，不用写5个case</div><div class="dc-tag">参数: [1,2,3,4,5]</div></div></div>
    <div class="demo-card"><div class="dc-icon">🔍</div><div class="dc-body"><div class="dc-num">SCENE 02</div><div class="dc-title">搜索验证</div><div class="dc-desc">不同关键词 → 验证返回结果是否正确匹配</div><div class="dc-tag">参数: ["手机","电脑","耳机"]</div></div></div>
    <div class="demo-card"><div class="dc-icon">👥</div><div class="dc-body"><div class="dc-num">SCENE 03</div><div class="dc-title">批量用户</div><div class="dc-desc">100个用户登录测试 一行parameters配完</div><div class="dc-tag">数据量越大性价比越高 💰</div></div></div>
    <div class="demo-card"><div class="dc-icon">⚠️</div><div class="dc-body"><div class="dc-num">SCENE 04</div><div class="dc-title">边界值</div><div class="dc-desc">空字符串 / 超长 / 特殊字符 全覆盖</div><div class="dc-tag">参数: ["", "A"*500, "!@#$%"]</div></div></div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-closing">
  <div class="bubble-q"><div class="q-text">你现在怎么跑<br>批量数据测试？</div></div>
  <div class="cta">还在手动改参数吗？👇</div>
  <div class="preview">下篇预告<br>给用例打标签 · 比文件夹聪明10倍 🏷️</div>
  <div class="hashtags">#数据驱动 #参数化测试 #自动化测试 #YAML #软件测试</div>
  <div class="watermark">__SITE__</div>
</div>
""".replace("__SITE__", SITE)}

# 13 - 标签
bodies["13-cards.html"] = {
"names": ["13-cover-tags","13-folder-pain","13-tag-solution","13-3d-filter","13-ending"],
"html": """
<div class="card card-cover">
  <div class="tag">零代码测试 · 效率篇</div>
  <h1>给用例<span style="color:#4338ca">打标签</span></h1>
  <div class="subtitle">比文件夹分类聪明10倍的管理方式 🏷️</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">01</div>
  <div class="section-title">📁 文件夹的困局</div>
  <div class="compare-wrap">
    <div class="cp-panel cp-bad">
      <div class="cp-head"><div class="mk mk-x">✕</div>传统分类</div>
      <div class="cp-body">
        一个case既属于 smoke <br>又属于 P0 怎么办？
        <div style="text-align:center;color:#dc2626;font-weight:700;font-size:28px;margin-top:16px">复制两份 ❌</div>
        <div style="text-align:center;color:#4b5563;font-size:20px">改一处漏一处 → 线上Bug</div>
      </div>
    </div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">02</div>
  <div class="section-title">🏷️ 标签方案</div>
  <div class="compare-wrap">
    <div class="cp-panel cp-good">
      <div class="cp-head"><div class="mk mk-ok">✓</div>tags: [smoke, P0, login]</div>
      <div class="cp-body">
        <div class="tag-display">
          <div class="tag-badge tag-s">🔧 smoke</div>
          <div class="tag-badge tag-p">⭐ P0</div>
          <div class="tag-badge tag-l">🔑 login</div>
        </div>
        一个用例 · 三个标签 · 交叉筛选
        <div class="code-box">--tags=smoke → 只跑冒烟</div>
        <div class="code-box">--tags=smoke,P0 → 冒烟且P0</div>
        <div class="code-box">--tags=login,regression → 登录回归</div>
        <div style="text-align:center;color:#059669;font-weight:700;margin-top:12px">零维护成本 ✨</div>
      </div>
    </div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">03</div>
  <div class="section-title">🎯 三维筛选 精准打击</div>
  <div class="dim-grid">
    <div class="dim-card"><div class="dim-icon">🏷️</div><div class="dim-title">标签维度</div><div class="dim-desc">smoke / regression / P0</div></div>
    <div class="dim-card"><div class="dim-icon">🌍</div><div class="dim-title">环境维度</div><div class="dim-desc">dev / staging / prod</div></div>
    <div class="dim-card"><div class="dim-icon">⚡</div><div class="dim-title">优先级</div><div class="dim-desc">P0 必过 / P1 常规 / P2 低优</div></div>
  </div>
  <div style="margin-top:auto;padding-top:28px;text-align:center">
    <div class="code-box" style="display:inline-block;font-size:24px">--tags=smoke --env=staging --priority=P0</div>
    <div style="font-size:28px;font-weight:800;color:#1e1b4b;margin-top:18px">「测试环境冒烟+P0」<span style="color:#4338ca">一键命中</span> 🎯</div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-closing">
  <div class="bubble-q"><div class="q-text">你现在用文件夹<br>还是标签管理用例？</div></div>
  <div class="cta">评论区聊聊 👇</div>
  <div class="preview">下篇预告<br>聪明的测试知道什么时候不跑 🚦</div>
  <div class="hashtags">#测试管理 #测试用例 #标签分类 #自动化测试 #软件测试</div>
  <div class="watermark">__SITE__</div>
</div>
""".replace("__SITE__", SITE)}

# 14 - 条件跳过
bodies["14-cards.html"] = {
"names": ["14-cover-skip","14-prod-protect","14-more-scenes","14-core-insight","14-ending"],
"html": """
<div class="card card-cover">
  <div class="tag">零代码测试 · 策略篇</div>
  <h1>聪明的测试<br>知道什么时候<span style="color:#4338ca">不跑</span></h1>
  <div class="subtitle">条件跳过 · 比跑错更高级的能力 🚦</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">01</div>
  <div class="section-title">🔴 场景：生产环境保护</div>
  <div class="sc-list">
    <div class="sc-card"><div class="sc-num">!</div><div class="sc-body"><div class="sc-title">生产不能删数据</div><div class="sc-desc">创建用户 / 删除用户 → 线上绝对不能跑</div></div></div>
    <div class="sc-card"><div class="sc-num">✓</div><div class="sc-body"><div class="sc-title">查询可以跑</div><div class="sc-desc">GET请求、健康检查 → 生产要跑</div></div></div>
  </div>
  <div class="core-msg">
    <span class="code-snippet">skip: if: "{{env}} == 'production'"<br>  reason: "生产环境不能删数据"</span>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">02</div>
  <div class="section-title">🎯 更多实战场景</div>
  <div class="sc-list">
    <div class="sc-card"><div class="sc-num">2</div><div class="sc-body"><div class="sc-title">第三方服务挂了</div><div class="sc-desc">短信/支付接口不可用 → 跳过依赖它的case</div></div></div>
    <div class="sc-card"><div class="sc-num">3</div><div class="sc-body"><div class="sc-title">版本升级兼容</div><div class="sc-desc">API v1升到v2 → 旧版测试自动跳过</div><div class="code-snippet">skip: if: "{{version}} < 2.0"</div></div></div>
  </div>
  <div class="core-msg" style="font-size:28px">传统做法：手动注释/取消 ← <span style="color:#dc2626">总有人忘</span><br>YAML做法：<span class="em">自动识别</span> ← 永不出错</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">03</div>
  <div class="section-title">💡 核心认知</div>
  <div style="flex:1;display:flex;align-items:center;justify-content:center">
    <div style="text-align:center">
      <div style="font-size:120px;font-weight:900;color:#dc2626;line-height:1">✕</div>
      <div style="font-size:34px;color:#1e1b4b;font-weight:900;margin:16px 0">生产环境不该跑的用例<br>强行跑 = 事故</div>
      <div style="width:80px;height:3px;background:#c7d2fe;margin:32px auto;border-radius:2px"></div>
      <div style="font-size:72px;font-weight:900;color:#059669;line-height:1">✓</div>
      <div style="font-size:34px;color:#1e1b4b;font-weight:900;margin:16px 0">自动跳过 ≠ 偷懒<br>是在保护生产环境</div>
    </div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-closing">
  <div class="bubble-q"><div class="q-text">你在生产跑漏过<br>不该跑的测试吗？</div></div>
  <div class="cta">评论区说出你的故事 👇</div>
  <div class="preview">下篇预告<br>一个文件测完一个业务模块 🏗️</div>
  <div class="hashtags">#条件跳过 #测试策略 #生产安全 #自动化测试 #软件测试</div>
  <div class="watermark">__SITE__</div>
</div>
""".replace("__SITE__", SITE)}

# 15 - 组织
bodies["15-cards.html"] = {
"names": ["15-cover-org","15-dir-structure","15-benefits","15-where-put","15-ending"],
"html": """
<div class="card card-cover">
  <div class="tag">零代码测试 · 工程篇</div>
  <h1>一个文件<br><span style="color:#4338ca">测完一个业务模块</span></h1>
  <div class="subtitle">测试用例的组织哲学 🏗️</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">01</div>
  <div class="section-title">📁 推荐目录结构</div>
  <div class="dir-tree">
    <div class="dir">testcases/</div>
    <div class="dir">├── smoke/ <span style="color:#9ca3af;font-weight:400"># 冒烟测试</span></div>
    <div class="file">│   └── login.yaml</div>
    <div class="dir">├── regression/ <span style="color:#9ca3af;font-weight:400"># 回归测试</span></div>
    <div class="file">│   ├── users.yaml</div>
    <div class="file">│   └── orders.yaml</div>
    <div class="dir">└── local/ <span style="color:#9ca3af;font-weight:400"># 本地调试</span></div>
    <div class="file">    └── wip.yaml</div>
  </div>
  <div style="text-align:center;font-size:28px;font-weight:800;color:#1e1b4b;padding-top:24px">
    <span style="color:#4338ca">1个YAML</span> = 1个业务场景 = <span style="color:#059669">1套完整测试</span> ✨
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">02</div>
  <div class="section-title">🎁 四大好处</div>
  <div class="benefit-grid">
    <div class="bf-card"><div class="bf-icon">👀</div><div class="bf-title">一眼看完</div><div class="bf-desc">打开users.yaml 增删改查全在眼前 不用跳五个文件</div></div>
    <div class="bf-card"><div class="bf-icon">📝</div><div class="bf-title">Git Diff 清晰</div><div class="bf-desc">改了什么接口的什么测试 一行diff看清楚</div></div>
    <div class="bf-card"><div class="bf-icon">🔍</div><div class="bf-title">Code Review</div><div class="bf-desc">测试用例也能review 开发改接口→测试review YAML</div></div>
    <div class="bf-card"><div class="bf-icon">⏪</div><div class="bf-title">版本回滚</div><div class="bf-desc">git revert 一键回 测试用例也能倒带</div></div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">03</div>
  <div class="section-title">🤔 放哪？</div>
  <div class="compare-wrap">
    <div class="cp-panel cp-bad"><div class="cp-head"><div class="mk mk-x">✕</div>和代码一起</div><div class="cp-body">开发改接口时顺手改测试<br>小团队首选<br>改代码=改测试 不会忘<br><div style="color:#dc2626;font-weight:700;margin-top:12px">适合 3-10人团队</div></div></div>
    <div class="cp-panel cp-good"><div class="cp-head"><div class="mk mk-ok">✓</div>独立仓库</div><div class="cp-body">测试团队完全自治<br>大团队标准做法<br>权限清晰 各管各的<br><div style="color:#059669;font-weight:700;margin-top:12px">适合 10+ 人团队</div></div></div>
  </div>
  <div style="text-align:center;font-size:26px;font-weight:700;color:#1e1b4b;padding-top:20px">关键不是位置 是<span style="color:#4338ca">每个YAML独立版本</span> 🎯</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-closing">
  <div class="bubble-q"><div class="q-text">你的测试用例<br>现在怎么组织的？</div></div>
  <div class="cta">评论区聊聊 👇</div>
  <div class="preview">下篇预告<br>YAML vs Python 真实对比 ✅</div>
  <div class="hashtags">#测试组织 #测试架构 #版本管理 #自动化测试 #软件工程</div>
  <div class="watermark">__SITE__</div>
</div>
""".replace("__SITE__", SITE)}

# 16 - vs Python
bodies["16-cards.html"] = {
"names": ["16-cover-vs","16-4d-compare","16-best-fit","16-real-feedback","16-ending"],
"html": """
<div class="card card-cover">
  <div class="tag">零代码测试 · 观点篇</div>
  <h1><span style="color:#4338ca">YAML</span> vs <span style="color:#1e1b4b">Python</span></h1>
  <div class="subtitle">真实对比 · 不端水 · 说人话 ✅</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">01</div>
  <div class="section-title">📊 四个维度对比</div>
  <div class="vs-table">
    <div class="vs-row"><div class="vs-dim">学习成本</div><div class="vs-bad">Python<br>要懂编程</div><div class="vs-icon">➡️</div><div class="vs-good">YAML<br>懂接口就行</div></div>
    <div class="vs-row"><div class="vs-dim">可读性</div><div class="vs-bad">Python<br>逻辑藏在代码里</div><div class="vs-icon">➡️</div><div class="vs-good">YAML<br>一眼看清测什么</div></div>
    <div class="vs-row"><div class="vs-dim">维护成本</div><div class="vs-bad">Python<br>改接口改N处</div><div class="vs-icon">➡️</div><div class="vs-good">YAML<br>改一行配置</div></div>
    <div class="vs-row"><div class="vs-dim">协作性</div><div class="vs-bad">Python<br>只有开发能改</div><div class="vs-icon">➡️</div><div class="vs-good">YAML<br>产品经理都能看懂</div></div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">02</div>
  <div class="section-title">🎯 不是谁比谁好 · 是用对场景</div>
  <div style="flex:1;display:flex;gap:40px;align-items:center;justify-content:center">
    <div style="flex:1;text-align:center;background:#ecfdf5;border:1.5px solid #a7f3d0;border-radius:18px;padding:36px 28px">
      <div style="font-size:60px;margin-bottom:12px">📋</div>
      <div style="font-size:30px;font-weight:900;color:#1e1b4b;margin-bottom:12px">YAML 适合</div>
      <div style="font-size:22px;color:#4b5563;line-height:1.7">接口增删改查<br>简单断言验证<br>CRUD批量测试<br>参数化数据驱动</div>
      <div style="font-size:42px;font-weight:900;color:#059669;margin-top:16px">90%</div>
      <div style="font-size:20px;color:#4b5563">的接口测试场景</div>
    </div>
    <div style="flex:1;text-align:center;background:#fef2f2;border:1.5px solid #fecaca;border-radius:18px;padding:36px 28px">
      <div style="font-size:60px;margin-bottom:12px">🐍</div>
      <div style="font-size:30px;font-weight:900;color:#1e1b4b;margin-bottom:12px">Python 兜底</div>
      <div style="font-size:22px;color:#4b5563;line-height:1.7">复杂业务编排<br>条件循环逻辑<br>自定义插件<br>非标协议测试</div>
      <div style="font-size:42px;font-weight:900;color:#dc2626;margin-top:16px">10%</div>
      <div style="font-size:20px;color:#4b5563">的复杂场景</div>
    </div>
  </div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">03</div>
  <div class="section-title">🗣️ 真实反馈</div>
  <div class="speech-box">
    <div class="speech-item"><div class="who">🧑‍💻 产品经理</div><div class="say">"咦 这个我看懂了 就是说我请求什么 希望返回什么"</div></div>
    <div class="speech-item"><div class="who">👨‍💻 开发同学</div><div class="say">"你给我看Python代码我不想看，YAML可以 改了接口我也能帮你改测试"</div></div>
    <div class="speech-item"><div class="who">🐣 新人测试</div><div class="say">"不用学pytest直接上手 入职第二天写的用例就过了"</div></div>
  </div>
  <div style="text-align:center;font-size:26px;font-weight:700;color:#4338ca;padding-top:16px">降低门槛 ≠ 降低质量</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-closing">
  <div class="bubble-q"><div class="q-text">你站哪一边？<br>YAML 还是 Python？</div></div>
  <div class="cta">评论区辩一辩 👇</div>
  <div class="preview">下篇预告<br>手把手带你写第一个用例 🎯</div>
  <div class="hashtags">#YAML #Python测试 #测试框架对比 #自动化测试 #测试效率</div>
  <div class="watermark">__SITE__</div>
</div>
""".replace("__SITE__", SITE)}

# 17 - 第一个用例
bodies["17-cards.html"] = {
"names": ["17-cover-first","17-3step","17-code","17-result","17-ending"],
"html": """
<div class="card card-cover">
  <div class="tag">零代码测试 · 入门篇</div>
  <h1>手把手写<span style="color:#4338ca">第一个</span>用例</h1>
  <div class="subtitle">5分钟 · 从零到第一个 ✅ PASS 🎯</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">01</div>
  <div class="section-title">🚶 就三步</div>
  <div class="step-nums">
    <div class="step-box"><div class="sn">Step 1</div><div class="st">建文件</div><div class="sd">mkdir 加 touch<br>hello.yaml 就位</div></div>
    <div class="step-box"><div class="sn">Step 2</div><div class="st">写7行</div><div class="sd">一个GET请求<br>两个断言<br>没有代码</div></div>
    <div class="step-box"><div class="sn">Step 3</div><div class="st">跑起来</div><div class="sd">autotest run<br>hello.yaml -v</div></div>
  </div>
  <div style="text-align:center;font-size:28px;font-weight:800;color:#1e1b4b;padding-top:28px">不需要 import · 不需要 class · <span style="color:#4338ca">不需要 def</span></div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">02</div>
  <div class="section-title">✍️ 就这些</div>
  <div class="code-show">name: "我的第一个测试"
base_url: "https://jsonplaceholder.typicode.com"

cases:
  - name: 获取Todo列表
    request:
      method: GET
      url: /todos/1
    assert:
      - path: $.status_code
        operator: eq
        value: 200
      - path: $.data.id
        operator: eq
        value: 1</div>
  <div style="text-align:center;font-size:28px;font-weight:800;color:#059669;padding-top:20px">一个 GET · 两个断言 · 七行 · <span style="color:#4338ca">零代码</span></div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">03</div>
  <div class="section-title">🎉 看到这个没有</div>
  <div class="result-show">
    <div class="big-check">✅</div>
    <div class="pass-line">获取Todo列表 ........... PASS</div>
    <div style="font-size:26px;color:#4b5563;margin-top:20px">1 passed in 0.32s</div>
    <div class="timer">⏱️ 真正花了多久？不到5分钟</div>
  </div>
  <div style="text-align:center;font-size:28px;font-weight:800;color:#1e1b4b;padding-top:20px">第一次看到 <span style="color:#059669">✅ PASS</span> 的感觉 懂的都懂 🔥</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-closing">
  <div class="bubble-q"><div class="q-text">第一次看到 ✅ PASS<br>是什么感觉？</div></div>
  <div class="cta">评论区说说 👇</div>
  <div class="preview">下篇预告<br>YAML测试也能Git管理 🧩</div>
  <div class="hashtags">#入门教程 #自动化测试 #YAML #零基础学测试 #接口测试</div>
  <div class="watermark">__SITE__</div>
</div>
""".replace("__SITE__", SITE)}

# 18 - Git
bodies["18-cards.html"] = {
"names": ["18-cover-git","18-why-git","18-collab-flow","18-diff","18-ending"],
"html": """
<div class="card card-cover">
  <div class="tag">零代码测试 · 工程篇</div>
  <h1>YAML<span style="color:#4338ca">也能进</span>Git？</h1>
  <div class="subtitle">测试用例的版本管理正确姿势 🧩</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">01</div>
  <div class="section-title">🤔 测试用例为什么要进Git</div>
  <div class="why-grid">
    <div class="why-card"><div class="wc-icon">📝</div><div class="wc-title">纯文本</div><div class="wc-desc">YAML天生Git友好 自动diff 改了什么一行看清</div></div>
    <div class="why-card"><div class="wc-icon">👥</div><div class="wc-title">团队协作</div><div class="wc-desc">开发改接口→提PR→测试review YAML diff</div></div>
    <div class="why-card"><div class="wc-icon">🌿</div><div class="wc-title">分支管理</div><div class="wc-desc">feature分支带测试用例 hotfix分支带回归测试</div></div>
    <div class="why-card"><div class="wc-icon">⏪</div><div class="wc-title">随时回滚</div><div class="wc-desc">git revert 一行命令 测试用例也能倒回去</div></div>
  </div>
  <div style="text-align:center;font-size:26px;font-weight:700;color:#4338ca;padding-top:16px">测试用例也是代码 该有的Git能力一样不少</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">02</div>
  <div class="section-title">🔄 协作流程</div>
  <div class="flow-wrap">
    <div class="flow-step"><div class="fs-box"><div class="fs-num">Step 1</div><div class="fs-title">开发改接口</div><div class="fs-desc">提交代码 + YAML变更</div></div><div class="fs-arrow">→</div><div class="fs-box"><div class="fs-num">Step 2</div><div class="fs-title">CI自动跑</div><div class="fs-desc">看测试有没有挂</div></div><div class="fs-arrow">→</div><div class="fs-box"><div class="fs-num">Step 3</div><div class="fs-title">Review YAML</div><div class="fs-desc">测试看diff确认</div></div><div class="fs-arrow">→</div><div class="fs-box"><div class="fs-num">Step 4</div><div class="fs-title">Merge</div><div class="fs-desc">一起进主干</div></div></div>
  </div>
  <div style="text-align:center;font-size:28px;font-weight:800;color:#1e1b4b;padding-top:20px">测试用例的 <span style="color:#4338ca">Code Review</span> 跟代码一样流程 🔄</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-content">
  <div class="num">03</div>
  <div class="section-title">👀 Git Diff 长这样</div>
  <div class="diff-box">
    <span class="red">- base_url: "http://localhost:8000"</span><br>
    <span class="green">+ base_url: "https://api.example.com"</span><br><br>
    <span class="red">- username: admin</span><br>
    <span class="green">+ username: test_user</span>
  </div>
  <div style="text-align:center;font-size:28px;font-weight:800;color:#1e1b4b;padding-top:20px">改了哪个环境 · 换了哪个账号<br><span style="color:#4338ca">一行diff看得明明白白</span> 👁️</div>
  <div class="watermark">__SITE__</div>
</div>

<div class="card card-closing">
  <div class="bubble-q"><div class="q-text">你的测试用例<br>有没有进Git管理？</div></div>
  <div class="cta">评论区聊聊 👇</div>
  <div class="preview">第2章完结 · 下期预告<br>变量系统深度 · 三层作用域 📦</div>
  <div class="hashtags">#Git #版本管理 #测试协作 #DevOps #软件工程</div>
  <div class="watermark">__SITE__</div>
</div>
""".replace("__SITE__", SITE)}


def main():
    for fname, data in bodies.items():
        names_js = "const names = " + str(data["names"]) + ";"
        doc = (
            "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n"
            "<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            "<title>" + fname.replace("-cards.html", "") + " · 小红书卡片 · 科技靛蓝</title>\n"
            "<link href=\"https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap\" rel=\"stylesheet\">\n"
            "<style>\n" + STYLE + "\n</style>\n</head>\n<body>\n"
            "<div class=\"toolbar\"><button onclick=\"downloadAll()\">📥 一键下载全部卡片</button></div>\n"
            "<div class=\"cards\">\n" + data["html"] + "\n</div>\n"
            "<script>" + names_js + "</script>\n" + JS + "\n</body>\n</html>\n"
        )
        path = os.path.join(OUT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc)
        print("wrote", path)


if __name__ == "__main__":
    main()
