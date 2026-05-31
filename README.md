# wetch — WeChat Article Formatter

> 一键将 Markdown 转换为**公众号兼容 HTML**，支持多主题、自动封面生成

`wetch` 是一个命令行工具，让公众号内容创作者告别手动排版。写 Markdown，一键出 HTML，直接粘贴到公众号编辑器。

## ✨ 特性

- **公众号兼容** — 输出纯 table + 内联 style 布局，flex/gradient/rgba/class 全部规避
- **5 种主题** — 极简红 · 科技蓝 · 自然绿 · 典雅紫 · 极简灰
- **自动封面** — `--cover` 生成封面 HTML，可用 Playwright 截图出图
- **智能解析** — `##` 标题 / `###` 副标题 / `>` 引用 / `-` 列表 / `---` 分隔线 / `**加粗**` / `代码`
- **零依赖运行** — 纯 Python 3，无需 Node.js、npm、数据库

## 🚀 快速开始

```bash
# 从 GitHub Release 安装（推荐，无需 PyPI）
pip install https://github.com/kissnger/wetch/releases/download/v1.0.0/wetch-1.0.0-py3-none-any.whl

# 或者从源码安装
git clone https://github.com/kissnger/wetch.git
cd wetch && pip install .

# 转换文章
wetch article.md -o output.html

# 指定主题
wetch article.md --theme blue -o output.html

# 生成封面 HTML（配合 Playwright 截图为封面图）
wetch article.md --cover -o cover.html

# 查看可用主题
wetch --list-themes
```

## 📝 输入格式

```markdown
## 文章标题

### 文章副标题

date: 2026.05.30
tags: 标签1, 标签2
author: 你的名字

> 封面: 封面显示的文字

正文内容段落。

**这是加粗文字**

> 这是引用块

- 列表项 1
- 列表项 2

#### 小节标题

---

分隔线以上的内容。
```

## 🎨 主题预览

| 主题 | 主色 | 适用场景 |
|------|------|---------|
| `default` | 红 `#cc3333` | 通用 · 焦虑/讨论型文章 |
| `blue` | 蓝 `#4a6cf7` | 技术 · 获得感型文章 |
| `green` | 绿 `#2d8a57` | 生活 · 轻松阅读 |
| `purple` | 紫 `#7c3aed` | 品牌 · 高端调性 |
| `minimal` | 灰 `#636366` | 深度长文 · 严肃内容 |

## 🖼 封面生成

```bash
# 1. 生成封面 HTML
wetch article.md --cover -o cover.html

# 2. 用 Playwright 截图
npx playwright screenshot --viewport-size=1200,675 cover.html cover.png
```

## 💰 支持项目

如果 wetch 帮到了你，欢迎请作者喝杯咖啡 ☕

<p align="center">
  <img src="assets/alipay-qr.jpg" width="200" alt="支付宝收款码">
  <br>
  <strong>支付宝扫一扫，随意打赏</strong>
</p>

- **GitHub Sponsors**: [github.com/sponsors/kissnger](https://github.com/sponsors/kissnger)

## 📄 许可

MIT License — 个人、商业均可免费使用。
如需要优先支持、定制主题、企业部署，请通过 [GitHub Issues](https://github.com/kissnger/wetch/issues) 联系。