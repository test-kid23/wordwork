# ⚡ 10分钟写一套完整CRUD，隔壁小哥看傻了


上篇解剖了YAML文件长啥样

有人说"看着不错 真能干活吗？"

今天跑给你看 计个时 ⏱️


## 🛠️ 目标：一个文件测完增删改查

创建 → 查询 → 更新 → 删除 四个操作一条链


## ✍️ 套件定义（1分钟）

```yaml
name: "用户CRUD完整测试"
base_url: "http://localhost:8000"
variables:
  username: cjtest
  password: Test@123456
```

三行 比写conftest.py快十倍


## ✍️ 创建用例（3分钟）

```yaml
  - name: 创建用户
    request:
      method: POST
      url: /api/v1/users
      json:
        username: "{{username}}"
        password: "{{password}}"
    extract:
      user_id: $.data.id
    assert:
      - path: $.status_code | eq | 201
```

重点：extract把返回的user_id存起来 后面查/改/删全靠它


## ✍️ 查询+更新+删除（5分钟）

查询、更新、删除 三个case都引用{{user_id}}

零手动传变量 一步到位


## 🚀 跑（1分钟）

```bash
autotest run users.yaml -v
```

✅✅✅✅ 四连过 数据库干干净净

真正省的不是代码行数 是这些：不用切文件、不用import、不用手动传变量、不用写teardown


💬 你用Python写CRUD要多久？评论区聊聊～

#CRUD测试 #接口自动化 #YAML #零代码 #软件测试
