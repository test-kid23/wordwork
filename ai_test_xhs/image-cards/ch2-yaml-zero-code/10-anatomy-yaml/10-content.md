# 📝 一个YAML文件=一个完整的测试套件？


上次聊了"写YAML就能测接口" 很多人问"到底长啥样"

今天直接解剖一个真实的 👇


## 🧠 四大块 就这么简单

```
name: 套件名
base_url: 接口地址
variables:
  用户名密码
cases:
  - 用例1: 创建
  - 用例2: 查询
  ...
```

1️⃣ name — 这套测什么
2️⃣ base_url — 所有接口共用
3️⃣ variables — 全局变量共享
4️⃣ cases — 一条case = 一个请求+断言

没有import 没有class 没有def


## 📊 Python vs YAML

同一个用户的增删改查

Python：5个文件、150行、import一堆库
YAML：1个文件、50行、零import

差距不在行数 在"5个文件来回跳 vs 1个文件看完"


## 🔍 解剖一个case

```yaml
- name: 创建新用户
  request:
    method: POST
    url: /api/v1/users
    json:
      username: "{{username}}"
  extract:
    user_id: $.data.id
  assert:
    - path: $.status_code
      operator: eq
      value: 201
```

name说测什么 → request发请求 → extract把id存起来给后面用 → assert验状态码

没有一行代码 但该干的都干了


💬 你觉得YAML和Python 哪种更容易看懂？评论区聊聊～

#YAML测试 #接口自动化 #测试用例 #零代码 #软件测试
