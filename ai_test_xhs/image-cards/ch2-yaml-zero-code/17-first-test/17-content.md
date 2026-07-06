# 🎯 第一次用YAML写测试？手把手带你写第一个用例


看完前几篇 想试试了是吧

来 五分钟从零到第一个通过的测试


## 第1步：建文件

```bash
mkdir testcases/local
touch testcases/local/hello.yaml
```


## 第2步：写

```yaml
name: "我的第一个测试"
base_url: "https://jsonplaceholder.typicode.com"

cases:
  - name: 获取Todo列表
    request:
      method: GET
      url: /todos/1
    assert:
      - path: $.status_code | eq | 200
      - path: $.data.id | eq | 1
```

一个GET请求 + 两个断言 七行


## 第3步：跑

```bash
autotest run testcases/local/hello.yaml -v
```

看到 ✅ PASS 的那一刻


## 彩蛋

真的就五分钟 从零到第一个通过的测试

不需要import 不需要class 不需要def

唯一需要的：知道接口地址和期望结果


💬 第一次看到✅PASS是什么感觉？

#入门教程 #自动化测试 #YAML #零基础学测试 #接口测试
