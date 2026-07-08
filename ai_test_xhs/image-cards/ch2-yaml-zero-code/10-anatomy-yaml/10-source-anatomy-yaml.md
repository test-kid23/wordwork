# 第10篇 · 小红书文案

**标题**: 📝 一个YAML文件=一个完整的测试套件？解剖一个真实案例

上次聊了"写YAML就能测接口"这件事

很多人在评论区问

"一个YAML文件到底长啥样？"

今天直接解剖一个真实的 👇

---

🧠 YAML文件四大块

一个完整的YAML测试文件 就四块

1️⃣ name — 套件名称
告诉别人这套测试测什么

2️⃣ base_url — 基础地址
所有接口共用前缀 不用每个case写一遍

3️⃣ variables — 全局变量
username / password 整个文件共用

4️⃣ cases — 用例列表
一个case = 一次HTTP请求 + 断言

就这么简单 没import 没class 没def

---

📊 同一个功能 两种写法

同一个用户管理的增删改查

❌ Python要写:
→ conftest做公共配置
→ test_create / test_query / test_update / test_delete
→ 5个文件 加上import差不多150行

✅ YAML只要写:
→ 1个users.yaml
→ 4个case排好队
→ 1个文件 大概50行

不是100行 vs 50行的差距

是5个文件来回跳 vs 1个文件看完的差距

---

🔍 解剖一个真实case

来看users.yaml里"创建用户"干了啥

🔸 name: "创建新用户"
就是给这个case起个名

🔸 request: POST到/api/v1/users
参数用{{}}引用全局变量

🔸 extract: 从返回体抠出user_id
存起来 后面case接着用

🔸 assert: 验两样
HTTP状态码是201
返回用户名跟发送的一致

没有一句Python 但啥都干了

🎯 一个文件的威力

这个users.yaml到底能做到啥

创建 → 自动测新用户能不能注册

查询 → 用刚创建的用户ID查

更新 → 改邮箱 看更新接口好不好使

删除 → 删掉测试用户 数据库干净

四个操作一条链 变量自动传递
不用手动复制粘贴user_id
测试完不留脏数据

📌 下一篇直接用users.yaml
手把手带你写完整CRUD
从0到能跑 不超10分钟

💬 YAML和Python代码比
哪个更容易看懂？
评论区聊聊～

觉得有用 ⭐ 收藏

#YAML测试 #接口自动化 #测试用例 #API测试 #零代码 #软件测试
