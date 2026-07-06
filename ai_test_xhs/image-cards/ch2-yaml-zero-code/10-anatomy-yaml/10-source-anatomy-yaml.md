# 第10篇 · 小红书文案

**标题**: 📝 一个YAML文件=一个完整的测试套件？解剖一个真实案例

---

上次聊了"写YAML就能测接口"这件事

很多人在评论区问

"一个YAML文件到底长啥样？"

今天直接解剖一个真实的 👇

---

## 🧠 YAML文件四大块

一个完整的YAML测试文件 就四块

```
name: "用户管理接口测试"
base_url: "https://api.example.com"
variables:
  username: test_user
  password: Test123456

cases:
  - name: 创建用户
    ...
  - name: 查询用户
    ...
```

四块分别是

1️⃣ name — 套件名称
告诉别人这套测试测什么

2️⃣ base_url — 基础地址
所有接口共用的前缀 不用每个case写一遍

3️⃣ variables — 全局变量
username / password 这些 整个文件共用

4️⃣ cases — 用例列表
一个case = 一次HTTP请求 + 断言

就这么简单 没有import 没有class 没有def

---

## 📊 同一个功能 Python vs YAML

来做个对比 同一个用户管理的增删改查

Python要写

```
4个Python文件
1个conftest.py 做公共配置
1个test_create.py 创建用户
1个test_query.py 查询用户
1个test_update.py 更新用户
1个test_delete.py 删除用户
```
一共5个文件 加上import和setup 差不多150行

YAML只要写

```
1个YAML文件 users.yaml
4个case在里面排好队
```
一共1个文件 大概50行

不是100行 vs 50行的差距

是"5个文件来回跳"vs"1个文件看完"的差距

---

## 🔍 解剖一个真实case

来看users.yaml里创建用户这个case

```yaml
- name: 创建新用户
  request:
    method: POST
    url: /api/v1/users
    json:
      username: "{{username}}"
      password: "{{password}}"
      email: "{{username}}@test.com"
  extract:
    user_id: $.data.id
  assert:
    - path: $.status_code
      operator: eq
      value: 201
    - path: $.data.username
      operator: eq
      value: "{{username}}"
```

逐行解释

- name — 这个case叫"创建新用户"
- request — 发一个POST到/api/v1/users
  参数用{{}}引用上面的全局变量
- extract — 从返回体把user_id抠出来
  存起来给后面的case用
- assert — 验两样
  HTTP状态码是201
  返回的用户名跟发送的一致

没有一句Python 但啥都干了

---

## 🎯 一个文件的威力

这个users.yaml到底能做到啥

创建 → 自动测新用户能不能注册

查询 → 用刚创建的用户ID查 有没有写入成功

更新 → 改邮箱 看更新接口好不好使

删除 → 删掉测试用户 数据库干净

四个操作一条链 变量自动传递

不需要手动复制粘贴user_id

测试完不留脏数据

---

## 📌 下一篇预告

下一篇直接用这个users.yaml

手把手带你写一套完整CRUD

从0到能跑 不超过10分钟

---

💬 你觉得YAML这种方式能看出测试逻辑吗？

和Python代码比 哪个更容易看懂？

评论区聊聊～

觉得有用 ⭐ 收藏

下一篇更新时你会收到提醒！

#YAML测试 #接口自动化 #测试用例 #API测试 #零代码 #软件测试
