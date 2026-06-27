# Playwright 核心编程与 AI 协作实现

> 先跑通最小链路，再用 AI 帮你加固每一环

---

## 一、为什么是 Playwright

Selenium 统治了 Web 自动化十年，但 Playwright 带来了三个本质变化：

| 特性 | Selenium | Playwright |
|------|----------|------------|
| 自动等待 | 需要显式 WebDriverWait | 内置 auto-wait |
| 网络拦截 | 需要额外代理 | 原生 route API |
| 多浏览器 | 需要不同 driver | 同一个 API |
| 移动端 | 需要 Appium | 原生 device emulation |
| 执行速度 | 慢（HTTP 协议通信） | 快（WebSocket 协议通信） |
| AI 协作 | 手写为主 | 有官方 CLI Agent |

**最重要的是最后一点**：Playwright 正在原生集成 AI Agent 能力，这意味着你的测试代码未来可以被 AI 理解和优化——而不是被 AI 绕过去。

---

## 二、最小浏览器自动化链路

和接口测试一样，原则是**先亲自跑通一条完整链路**：

```python
from playwright.sync_api import sync_playwright

# 最小链路：启动 → 打开 → 操作 → 断言 → 关闭
def test_login_basic():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 开发阶段先有头，方便观察
        page = browser.new_page()
        
        # 1. 打开登录页
        page.goto("https://example.com/login")
        
        # 2. 输入用户名密码
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "Test@123")
        
        # 3. 点击登录
        page.click('button[type="submit"]')
        
        # 4. 等待页面跳转（Playwright 自动等待）
        page.wait_for_url("**/dashboard")
        
        # 5. 断言
        assert page.locator(".welcome-text").inner_text() == "欢迎回来，admin"
        
        browser.close()
```

这段代码跑通后，你已经具备了最基本的 Web 自动化能力。接下来，**让 AI 帮你加固每一个环节**。

---

## 三、AI 辅助生成并审核 Locator

### 3.1 Locator 的稳定性金字塔

```
         ┌─────────────┐
         │   test-id    │  ← 最稳定（开发配合加 data-testid）
         ├─────────────┤
         │    role      │  ← 稳定（语义化，符合无障碍规范）
         ├─────────────┤
         │    text      │  ← 较稳定（用户可见文本）
         ├─────────────┤
         │ placeholder  │  ← 中等（可能被改）
         ├─────────────┤
         │    CSS       │  ← 不稳定（样式修改概率高）
         ├─────────────┤
         │   XPath      │  ← 最不稳定（绝对路径极易断裂）
         └─────────────┘
```

### 3.2 让 AI 生成 Locator

给 AI 描述你要定位的元素，让它推荐定位策略：

```markdown
给 AI 的 Prompt：
---
页面 HTML：
<div class="user-form">
  <label>用户名</label>
  <input type="text" placeholder="请输入用户名" class="ant-input" id="rc-1" />

请给出 3 种定位这个输入框的方式，按稳定性排序：
1. 最佳方案（最稳定）
2. 备选方案（较稳定）
3. 兜底方案（可能断裂但一定能找到）
---
```

AI 通常会给出：

```python
# 1. 最佳：通过 label/role 语义定位（推荐）
page.get_by_role("textbox", name="用户名")

# 2. 备选：通过 placeholder（较稳定）
page.get_by_placeholder("请输入用户名")

# 3. 兜底：通过 CSS（可能断裂）
page.locator(".ant-input")
```

### 3.3 审核 AI 生成的 Locator

拿到 AI 推荐的定位器后，你需要问三个问题：

```python
def audit_locator(page, locator):
    """审核 Locator 的稳定性"""
    
    # 问题1：是否唯一？
    count = locator.count()
    if count == 0:
        print("❌ 找不到元素")
        return False
    if count > 1:
        print(f"⚠️ 找到 {count} 个匹配元素，需要更精确的定位")
        return False
    
    # 问题2：是否可见可用？
    if not locator.is_visible():
        print("❌ 元素不可见")
        return False
    if not locator.is_enabled():
        print("❌ 元素不可用")
        return False
    
    # 问题3：是否稳定？（多次查找能否一致命中）
    print("✅ Locator 审核通过")
    return True
```

**对于动态 ID（如 Ant Design 的 `rc-1`、`rc-2`），AI 很难自主识别。你的审核必须覆盖这一点。**

---

## 四、从"能操作"到"能验证"

很多测试人只断言了"操作执行了"，但没有验证"业务生效了"。

```python
# ❌ 只验证操作，不验证结果
def test_add_to_cart_shallow(page):
    page.click('button:has-text("加入购物车")')
    # 仅验证操作完成，不知道商品真的加了没
    assert page.locator(".toast-success").is_visible()

# ✅ 验证业务结果
def test_add_to_cart_deep(page):
    initial_count = page.locator(".cart-badge").inner_text()
    
    page.click('button:has-text("加入购物车")')
    
    # 等 toasts 消失
    page.wait_for_selector(".toast-success", state="hidden")
    
    # 验证购物车数量 +1
    new_count = page.locator(".cart-badge").inner_text()
    assert int(new_count) == int(initial_count) + 1, \
        f"购物车数量未增加：{initial_count} → {new_count}"
```

### 等待策略的三层设计

```python
class WaitStrategy:
    """等待策略封装"""
    
    @staticmethod
    def for_navigation(page):
        """页面跳转等待"""
        page.wait_for_load_state("networkidle")  # 网络空闲
        page.wait_for_load_state("domcontentloaded")  # DOM 完成
    
    @staticmethod
    def for_element(page, locator, state="visible"):
        """元素状态等待"""
        page.locator(locator).wait_for(state=state, timeout=10000)
    
    @staticmethod  
    def for_data_ready(page, check_fn, timeout=10000):
        """自定义数据就绪等待"""
        import time
        deadline = time.time() + timeout / 1000
        while time.time() < deadline:
            if check_fn():
                return True
            page.wait_for_timeout(500)
        raise TimeoutError("数据就绪等待超时")


# 实战：搜索后等待结果加载
def test_search_with_wait(page):
    page.fill('.search-input', "iPhone 15")
    page.click('.search-btn')
    
    # 等搜索结果出现
    WaitStrategy.for_element(page, '.product-card')
    
    # 等加载动画消失
    page.locator('.loading-spinner').wait_for(state="hidden")
    
    # 等数据稳定（不再变化）
    def results_stable():
        count1 = page.locator('.product-card').count()
        page.wait_for_timeout(500)
        count2 = page.locator('.product-card').count()
        return count1 == count2 and count1 > 0
    
    WaitStrategy.for_data_ready(page, results_stable)
    
    # 再断言
    assert page.locator('.product-card').count() >= 1
```

---

## 五、Page Object：测试框架的第一块砖

当你有 10 个测试文件都在操作同一个登录页时，就该引入 Page Object 了：

```python
class LoginPage:
    """登录页对象"""
    
    def __init__(self, page):
        self.page = page
        self.username_input = page.get_by_placeholder("用户名")
        self.password_input = page.get_by_placeholder("密码")
        self.login_button = page.get_by_role("button", name="登录")
        self.error_message = page.locator(".error-msg")
    
    def navigate(self):
        self.page.goto("/login")
        self.page.wait_for_load_state("networkidle")
        return self
    
    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return DashboardPage(self.page)  # 链式返回下一个页面对象
    
    def get_error(self) -> str:
        return self.error_message.inner_text()


class DashboardPage:
    """仪表盘页面对象"""
    
    def __init__(self, page):
        self.page = page
        self.welcome_text = page.locator(".welcome-text")
        self.user_menu = page.locator(".user-menu")
    
    def wait_loaded(self):
        self.page.wait_for_url("**/dashboard")
        self.welcome_text.wait_for(state="visible")
        return self
    
    def get_welcome_message(self) -> str:
        return self.welcome_text.inner_text()


# 测试用例变得极简
def test_login_success(page):
    dashboard = (
        LoginPage(page)
        .navigate()
        .login("admin", "Test@123")
        .wait_loaded()
    )
    assert "欢迎回来" in dashboard.get_welcome_message()


def test_login_failed(page):
    error = (
        LoginPage(page)
        .navigate()
        .login("admin", "wrong_password")
        .get_error()
    )
    assert "密码错误" in error
```

### AI 辅助生成 Page Object

```markdown
给 AI 的 Prompt：
---
根据以下登录页 HTML，生成 Playwright Page Object 类：

<form class="login-form">
  <input type="text" placeholder="用户名" name="username" />
  <input type="password" placeholder="密码" name="password" />
  <button type="submit">登录</button>
  <div class="error-msg" style="display:none"></div>
</form>

要求：
1. 使用 get_by_role / get_by_placeholder 等语义化定位
2. 包含 navigate() 和 login() 两个方法
3. login() 返回下一个页面对象（暂用 None）
4. 添加等待逻辑
---
```

---

## 六、浏览器生命周期管理

在多用例并发时，浏览器的管理是关键：

```python
import pytest
from playwright.sync_api import sync_playwright, Page

@pytest.fixture(scope="session")
def browser():
    """Session 级别：只启动一次浏览器"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage"]  # CI 环境必须
        )
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    """Function 级别：每个用例创建独立上下文"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN"
    )
    yield context
    context.close()

@pytest.fixture
def page(context) -> Page:
    """Function 级别：每个用例独立页面"""
    page = context.new_page()
    yield page
    page.close()
```

### Context 隔离的关键价值

| 特性 | 说明 |
|------|------|
| **数据隔离** | 每个 Context 的 cookies/localStorage 完全独立 |
| **并行安全** | 多个 Context 可以同时运行，互不干扰 |
| **模拟多用户** | 不同 Context 可以有不同登录态 |
| **性能更好** | Context 创建比 Browser 创建快得多 |

---

## 七、复杂场景处理

### iframe 处理

```python
# Playwright 的 iframe 处理比 Selenium 优雅得多
def test_iframe_interaction(page):
    # 获取 iframe 内的元素
    frame = page.frame_locator("#payment-iframe")
    frame.get_by_placeholder("卡号").fill("4111111111111111")
    frame.get_by_role("button", name="支付").click()
```

### 网络拦截（Mock API）

```python
def test_with_mocked_api(page):
    # 拦截 API 请求，返回 mock 数据
    page.route("**/api/products", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"products":[{"id":1,"name":"测试商品","price":99}]}'
    ))
    
    page.goto("/products")
    # 页面会渲染 mock 数据，而不需要真实后端
    assert page.locator(".product-name").inner_text() == "测试商品"
```

### 下载文件验证

```python
def test_file_download(page):
    # 监听下载事件
    with page.expect_download() as download_info:
        page.click('button:has-text("导出报表")')
    
    download = download_info.value
    # 验证文件名
    assert download.suggested_filename.endswith(".xlsx")
    
    # 保存并验证内容
    download.save_as("/tmp/report.xlsx")
```

---

## 八、总结

Playwright + AI 协作的心法：

```
1. 亲自跑通最小链路 → 理解每个 API 的语义
2. 让 AI 生成 Locator → 你审核稳定性
3. 让 AI 生成 Page Object → 你设计页面间流转
4. 让 AI 生成复杂场景代码 → 你验证业务正确性
5. 让 AI diff 审核重构 → 确保行为不变
```

**与传统 Selenium 时代的核心区别**：以前是"你会什么就写什么"，现在是"你知道要什么，AI 帮你写什么"。你的领域知识（什么场景测什么、什么定位方式稳）比你的代码能力更重要。

---

*下一篇预告：《Page Object 模式与 Web 测试框架设计》——组件化封装、数据驱动、并行执行*

---

#Playwright #Web自动化 #Python #PageObject #AI测试
