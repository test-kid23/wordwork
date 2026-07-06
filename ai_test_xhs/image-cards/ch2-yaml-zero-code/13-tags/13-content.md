# 🏷️ 给用例打标签：比文件夹分类聪明10倍


你是不是这样分类测试用例的

```
smoke/ 放冒烟用例
regression/ 放回归用例
```

问题来了——一个用例既属于 smoke 又属于 P0

怎么办？在两个文件夹各放一份？一出BUG改两遍


## 🏷️ 标签比文件夹聪明在哪

```yaml
cases:
  - name: 用户登录
    tags: [smoke, P0, login]
    request:
      method: POST
      url: /api/v1/login
```

三个标签：smoke高频、P0必过、login模块

跑的时候

```bash
autotest run --tags=smoke          # 只跑冒烟
autotest run --tags=smoke,P0       # 冒烟且P0都要
autotest run --tags=login,regression # 登录的回归
```

一个用例 按标签切场景 零维护成本


## 🎯 三维筛选

标签 × 环境 × 优先级 组合打

```bash
autotest run --tags=smoke --env=staging --priority=P0
```

"测试环境冒烟+P0"一键跑对


💬 你现在用文件夹还是标签管理用例？

#测试管理 #测试用例 #标签分类 #自动化测试 #软件测试
