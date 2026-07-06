# 🔄 数据驱动测试：一条模板 × N组数据 = N个用例


你有没有试过 同一个接口用不同参数测好几遍

比如查用户 用 user_id=1 跑一次 → user_id=2 再跑一次 → user_id=3……

传统做法：复制三个case 改id

维护噩梦 50个用户 = 50份拷贝


## 💡 data_driven 来了

```yaml
cases:
  - name: 批量查询用户
    data_driven:
      parameters:
        - { user_id: 1, expect_name: "张三" }
        - { user_id: 2, expect_name: "李四" }
        - { user_id: 3, expect_name: "王五" }
    request:
      method: GET
      url: /api/v1/users/{{user_id}}
    assert:
      - path: $.data.name | eq | "{{expect_name}}"
```

一行配置 三个case自动生成

不是复制粘贴 是模板渲染


## 🔥 真实场景

- 分页测试：page=1,2,3,4,5 五个值自动轮询
- 搜索测试：不同关键词的返回结果校验
- 批量用户：100个用户的登录测试
- 边界值：空字符串、超长字符串、特殊字符

全部用 data_driven 一行搞定


💬 你现在是怎么做批量数据测试的？

#数据驱动 #参数化测试 #自动化测试 #YAML #软件测试
