🎯 第一次用YAML写测试？手把手带你写第一个用例


看完前几篇 想试试了是吧

来 五分钟从零到第一个通过的测试


第1步：建文件

在 testcases/local/ 下新建 hello.yaml

就一个空文件，准备开写


第2步：写

定义测试名 + 接口地址（用免费的 JSONPlaceholder 做靶场）

一个GET请求查 /todos/1，两个断言：
• 状态码必须200
• 返回的id必须等于1

七行YAML 搞定


第3步：跑

autotest run testcases/local/hello.yaml -v

看到 ✅ PASS 的那一刻


彩蛋

真的就五分钟 从零到第一个通过的测试

不需要import 不需要class 不需要def

唯一需要的：知道接口地址和期望结果


💬 第一次看到✅PASS是什么感觉？

#入门教程 #自动化测试 #YAML #零基础学测试 #接口测试
