---
source_id: "SRC-ZIWEI-IZTRO-001"
title: "iztro 2.5.8"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/ziwei/sources/SRC-ZIWEI-IZTRO-001.json"
capture_mode: "full"
aggregate_payload_sha256: "77976cf604ae7f356ee7a341cdab26994083a743996c87cd97260c1a800c908c"
license: "MIT"
---

# iztro 2.5.8

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-ZIWEI-IZTRO-001`
- Manifest: `systems/ziwei/sources/SRC-ZIWEI-IZTRO-001.json`
- Type: `software`
- Language: `zh-Hans`
- Edition/version: `2.5.8`
- Retrieved: `2026-07-23`
- Usage status: `reference_only`
- Systems: `ziwei`
- Lineages: `iztro-default-natal-v2.5.8`

## Rights envelope

- License: `MIT`
- Rights review: `reference_only`
- Derivative use: `allowed`
- Dataset use: `not_applicable`
- Evidence: The ignored local clone is pinned to tag 2.5.8 at commit 9d39f1743bf31c2b3c635c9b9556215d9c90ee2c. It is excluded from production code and artifacts.

## Locator capture ledger

### Locator 1

- Registered: https://github.com/SylarLong/iztro
- Resolved: https://api.github.com/repos/SylarLong/iztro
- Status: `captured`
- Media type: `application/json; charset=utf-8`
- SHA-256: `9b7b8c4a1cd128ba7614d6ac5257b6f3c530adfe810255d88acaf6d94a2b9fc5`
- Note: Retrieved repository metadata through the GitHub API: https://api.github.com/repos/SylarLong/iztro; README snapshot https://raw.githubusercontent.com/SylarLong/iztro/main/README.md sha256=72890306766b7f7b09c9252042c3afc25a71cdeb7903243b9292a79301fb0670

#### Parsed material

# SylarLong/iztro

⭐This is a lightweight kit for generating astrolabes for Zi Wei Dou Shu (The Purple Star Astrology), an ancient Chinese astrology. It allows you to obtain your horoscope and personality analysis. 支持多语言轻量级获取紫微斗数排盘信息的javascript开源库。

## Repository metadata

- Default branch: `main`
- License: `MIT`
- Archived: `False`
- Created: `2023-07-27T08:41:40Z`
- Updated: `2026-07-23T10:52:36Z`
- Repository: https://github.com/SylarLong/iztro

## Upstream README

<div align="center">

![banner2](https://github.com/SylarLong/iztro/assets/6510425/e8457a88-e52e-435e-8f93-e3f375486d70)

# 一套轻量级紫微斗数排盘工具库

简体中文 🔸 [繁體中文](./README-zh_TW.md) 🔸 [English](./README-en_US.md)

[![Join our Discord](https://img.shields.io/badge/JOIN%20OUR%20DISCORD-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/xvmu6gww6B)

</div>

<div align="center">

  [![NPM Version](https://img.shields.io/npm/v/iztro?logo=npm&logoColor=%23959DA5)](https://www.npmjs.com/package/iztro)
  [![NPM Minified Size](https://img.shields.io/bundlephobia/min/iztro?logo=npm&logoColor=%23959DA5)](https://www.npmjs.com/package/iztro)
  [![NPM Downloads](https://img.shields.io/npm/dt/iztro.svg?logo=npm&logoColor=%23959DA5)](https://www.npmjs.com/package/iztro)
  [![jsDelivr Hits](https://data.jsdelivr.com/v1/package/npm/iztro/badge)](https://www.jsdelivr.com/package/npm/iztro)

  [![GitHub Code Size in Bytes](https://img.shields.io/github/languages/code-size/SylarLong/iztro?logo=github&logoColor=%23959DA5)](https://github.com/SylarLong/iztro)
  [![Codecov Coverage](https://img.shields.io/codecov/c/github/SylarLong/iztro?logo=codecov&logoColor=%23959DA5)](https://github.com/SylarLong/iztro/actions/workflows/Codecov.yaml)
  [![Codecov Status](https://github.com/SylarLong/iztro/actions/workflows/Codecov.yaml/badge.svg)](https://github.com/SylarLong/iztro/actions/workflows/Codecov.yaml)

  [![Maintainability](https://qlty.sh/gh/SylarLong/projects/iztro/maintainability.svg)](https://qlty.sh/gh/SylarLong/projects/iztro)
  [![Package Quality](https://packagequality.com/shield/iztro.svg?logo=github)](https://packagequality.com/#?package=iztro)

  [![License](https://img.shields.io/github/license/sylarlong/iztro?logo=github)](https://www.npmjs.com/package/iztro)
  [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FSylarLong%2Fiztro.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FSylarLong%2Fiztro?ref=badge_shield)

</div>


## iztro AI · 紫微与奇门模型

除了开源排盘库，`iztro` 还提供两个托管的专业 AI 模型。它们会自动调用服务端术数工具，并通过 Chat API 或 Iztro Agents SDK 接入；你不需要自行维护排盘提示词或让通用模型猜测盘面。

| 模型 | 适合的问题 | 需要提供 |
| --- | --- | --- |
| **`iztro-ziwei-v3`** | 本命性格、人生格局、两人适配度，以及大限、流年、流月、流日等中长期趋势 | 出生日期、出生时间、性别和分析主题 |
| **`iztro-qimen-v3`** | 一件当下具体事情的决断、发展、阻力与应期，例如合作、谈判、面试、上线、出行或关系中的下一步 | 事情背景、一个明确问题和问事时刻；**不需要出生信息** |

### `iztro-ziwei-v3`：命盘与长期趋势

- 自动调用 `iztro` 排盘工具，按问题读取本命、大限、流年、流月、流日等必要层级。
- 针对紫微解读优化提示词与推理策略，并可在会话中记住出生信息和此前上下文。

### `iztro-qimen-v3`：一事一局的决断与应期

- 根据问事时刻分析**一件具体事情**，给出结论、主要依据、阻力与行动建议。
- 当用户问“什么时候”或时间是结论关键时，给出真实日历中的候选触发窗口。
- 一事一局：互不相关的事情应分开提问。应期日期是结合全局解读的触发候选，不是“某天必然成功”的保证。

例如，一个清晰的奇门问题是：“我们已经谈过两次渠道合作，但分成和上线时间还没定。现在应该推进、继续谈，还是暂缓？如果可以推进，请给出最近的行动窗口和依据。”

> [!NOTE]
> NPM 包 `iztro` 本身仍是开源的**紫微斗数排盘库**；`iztro-qimen-v3` 是通过 API/Agents SDK 使用的托管 AI 模型，不是本地奇门排盘模块。

两个模型都支持以下接入方式：

### 1. iztro Chat API —— 调用我们的 HTTP API

如果你需要紫微或奇门对话能力，可以使用 iztro Chat API。使用时需要 API key，你可以在 [开发者文档](https://api-doc.iztro.com) 查看完整接口，并通过[模型指南](https://api-doc.iztro.com/sdk/qimen)比较紫微与奇门。

以下示例假设你已把控制台生成的密钥保存到服务端环境变量 `ZIWEI_API_KEY`。不要把密钥写入浏览器代码。

推荐的集成方式是多轮对话 API：先创建会话，再向该会话发送用户消息。API 会自动处理上下文。

```shell
curl https://chat-api.iztro.com/v2/platform/sessions \
  -H "Authorization: Bearer $ZIWEI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "external_user_id": "user_123",
    "model": "iztro-ziwei-v3",
    "system_prompt_override": "用简洁中文回答，避免过度术语，并在最后给出可继续追问的方向。"
  }'

curl https://chat-api.iztro.com/v2/platform/sessions/{session_id}/messages \
  -H "Authorization: Bearer $ZIWEI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "分析我的 2026 年事业趋势。生日是 1995-02-23，出生时辰 17 点，性别女。",
    "title": "2026 事业解读",
    "language": "zh",
    "enable_iztro_call": true
  }'
```

奇门会话在创建时选择 `iztro-qimen-v3`。默认使用请求时刻起局；如果用户时区不同或结果需要可复现，请在消息中传入带 UTC 偏移量的 `current_datetime`：

```shell
curl https://chat-api.iztro.com/v2/platform/sessions \
  -H "Authorization: Bearer $ZIWEI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "external_user_id": "user_123",
    "model": "iztro-qimen-v3"
  }'

curl https://chat-api.iztro.com/v2/platform/sessions/{session_id}/messages \
  -H "Authorization: Bearer $ZIWEI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我们已经谈过两次渠道合作，但分成和上线时间还没定。现在应该推进、继续谈，还是暂缓？如果可以推进，请给出最近的行动窗口。",
    "current_datetime": "2026-07-20T14:30:00+08:00",
    "language": "zh",
    "enable_iztro_call": true
  }'
```

JavaScript 和 Python 示例见 [`examples/chat-api`](./examples/chat-api)。完整的前后端流式聊天、编辑、重新发送示例见 [`examples/fullstack-demo`](./examples/fullstack-demo)。

### 2. iztro Agents SDK —— 构建你自己的 Agent

在 `iztro-ziwei-v3` 或 `iztro-qimen-v3` 上构建你自己的 Agent，并加入自己的工具、MCP 服务器和人工确认。它是对 [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) 的轻量封装，提供 Python 与 TypeScript 两个版本：

- **Python** —— `pip install openai-iztro-agents` · [github.com/SylarLong/openai-iztro-agents-python](https://github.com/SylarLong/openai-iztro-agents-python)
- **TypeScript / JavaScript** —— `npm install openai-iztro-agents` · [github.com/SylarLong/openai-iztro-agents-js](https://github.com/SylarLong/openai-iztro-agents-js)

两个 SDK 都提供紫微与奇门便捷工厂。Python 使用 `iztro_ziwei_agent(...)` / `iztro_qimen_agent(...)`，TypeScript 使用 `iztroZiweiAgent({...})` / `iztroQimenAgent({...})`。API 返回的公开计算名称见[模型指南](https://api-doc.iztro.com/sdk/qimen)。

### 全栈演示

| 方案 | 完整示例 | 主要能力 |
| --- | --- | --- |
| iztro Chat API | [`examples/fullstack-demo`](./examples/fullstack-demo) | Node/Python 后端、流式输出、编辑消息、重新生成；API key 仅保存在后端 |
| Python Agents SDK | [ChatSession full-stack demo](https://github.com/SylarLong/openai-iztro-agents-python/tree/main/examples/fullstack-demo) | 会话列表、新建/删除/重命名、应用层编辑分支与 Fork、调用命盘记录、Markdown 渲染 |
| TypeScript / JavaScript Agents SDK | [ChatSession full-stack demo](https://github.com/SylarLong/openai-iztro-agents-js/tree/master/examples/fullstack-demo) | 与 Python 版相同的会话工作台和流式体验 |

<img src="./examples/fullstack-demo/assets/chat-session-workbench.png" alt="iztro Agents SDK ChatSession 全栈演示" width="1200" />

## 介绍

用于紫微斗数排盘的 JavaScript 开源库，有以下功能：

- 输入

  - 生日（阳历或农历皆可）
  - 出生时间
  - 性别

- 可以实现下列功能

  - 紫微斗数 12 宫的星盘数据
  - 获取生肖
  - 获取星座
  - 获取四柱（干支纪年法的生辰）
  - 获取运限（大限、小限、流年、流月、流日、流时）的数据
  - 获取流耀（大限和流年的动态星耀）
  - 判断指定宫位是否存在某些星耀
  - 判断指定宫位三方四正是否存在某些星耀
  - 判断指定宫位三方四正是否存在四化
  - 判断指定星耀是否存在四化
  - 判断指定星耀三方四正是否存在四化
  - 判断指定星耀是否是某个亮度
  - 根据天干获取四化
  - 获取指定星耀所在宫位
  - 获取指定宫位三方四正宫位
  - 获取指定星耀三方四正宫位
  - 获取指定星耀对宫
  - 获取指定运限宫位
  - 获取指定运限宫位的三方四正
  - 判断指定运限宫位内是否存在某些星耀
  - 判断指定运限宫位内是否存在四化
  - 判断指定运限三方四正内是否存在某些星耀
  - 判断指定运限三方四正内是否存在四化
  - 判断指定宫位是否是空宫
  - 判断宫位是否产生飞星到目标宫位
  - 获取宫位产生的四化宫位

- 其他

  - 多语言输入/输出

    输入的时候支持多个国家和地区语言混合输入，可以输出指定语言。目前支持 简体中文，繁体中文，英文，日文，韩文，越南语。英文的翻译目前还没有标准，所以我大多是意译的，但也正因为如此，可能英文版本的会更加易懂。如果有精通星象翻译的欢迎提 PR 。任何语言都可以。

  - 链式调用

    假如你想判断 `紫微星` 的 `三方四正` 有没有 `化忌`，你可以这样做

    ```ts
    import { astro } from 'iztro';

    const astrolabe = astro.bySolar('2000-8-16', 2, '男', true, 'zh-CN');

    astrolabe.star('紫微').surroundedPalaces().haveMutagen('忌');
    ```

  - 配置和插件

    紫微斗数流派众多，不同的流派的四化以及星耀亮度都会有些许差异，为了满足不同流派的需求和功能的扩展，`iztro` 在 `v2.3.0` 版本加入了全局配置和第三方插件功能。详见 [配置文档](https://ziwei.pro/posts/config-n-plugin.html)

> [!IMPORTANT]
> 如果你在开发中遇到任何问题，可以添加作者微信咨询。<br>
> 你也可以任意魔改代码，或联系作者获取技术支持。<br>
> <img src="https://github.com/SylarLong/SylarLong/assets/6510425/a2af4876-7d26-4900-a0fc-f5a2030f6205" alt="WeChat" width="350" />

## 快捷跳转

- [文档](https://docs.iztro.com)
- [讨论](https://github.com/SylarLong/iztro/discussions)
- [问题](https://github.com/SylarLong/iztro/issues)
- [排盘](https://ziwei.pub)

## 直接使用

如果你想要零开发直接查看 `iztro` 的排盘结果，请直接使用 [紫微派（ziwei.pub）](https://ziwei.pub) 在线排盘。

## 安装依赖

你可以使用任何你熟悉的包管理库来安装 `iztro`。

```shell
# npm
npm install iztro -S

# yarn
yarn add iztro

# pnpm
pnpm install iztro -S
```

## 独立 JavaScript 库

假如你使用的是静态 HTML 文件，可以下载 [release](https://github.com/SylarLong/iztro/releases) 资源文件中的 `iztro-min-js.tar.gz` 压缩包，里面包含了一个 `iztro` 压缩混淆过的 `js` 文件和对应的 `sourcemap` 文件。

> `v2.0.4+` 版本才提供独立js库。

将 `iztro.min.js` 用 `script` 标签引入 HTML 文件使用。

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>iztro-紫微斗数开源库</title>
  </head>
  <body>
    <script src="./iztro.min.js"></script>
    <script>
      // 获取一张星盘数据
      var astrolabe = iztro.astro.bySolar('2000-8-16', 2, '男', true, 'zh-CN');
    </script>
  </body>
</html>
```

当然，我们更推荐你直接使用 `CDN` 加速链接，你可以在下面列表中选择一个，在没有指定版本号的时候，会自动指向最新发布的版本。

- jsdelivr

  - https://cdn.jsdelivr.net/npm/iztro/dist/iztro.min.js
  - https://cdn.jsdelivr.net/npm/iztro@2.0.5/dist/iztro.min.js

- unpkg

  - https://unpkg.com/iztro/dist/iztro.min.js
  - https://unpkg.com/iztro@2.0.5/dist/iztro.min.js

你也可以使用如下规则来指定版本：

- `iztro@2`
- `iztro@^2.0.5`
- `iztro@2.0.5`

因为纯 JS 库没有代码提示和注释，所以在集成的时候请参阅 [iztro 开发文档](https://docs.iztro.com/quick-start.html)。

## 简单示例

这里是一个简单的例子显示如何调用 `iztro` 获取到紫微斗数星盘数据，详细文档请移步 [开发文档](https://docs.iztro.com)。

- ES6 Module

  ```ts
  import { astro } from 'iztro';

  // 通过阳历获取星盘信息
  const astrolabe = astro.bySolar('2000-8-16', 2, '女', true, 'zh-CN');

  // 通过农历获取星盘信息
  const astrolabe = astro.byLunar('2000-7-17', 2, '女', false, true, 'zh-CN');
  ```

- CommonJS

  ```ts
  var iztro = require('iztro');

  // 通过阳历获取星盘信息
  var astrolabe = iztro.astro.bySolar('2000-8-16', 2, '女', true, 'zh-CN');

  // 通过农历获取星盘信息
  var astrolabe = iztro.astro.byLunar('2000-7-17', 2, '女', false, true, 'zh-CN');
  ```


## 贡献

如果你对 `iztro` 有兴趣，也想加入贡献队伍，我们非常欢迎，你可以用以下方式进行：

- 如果你对程序功能有什么建议，请到 [这里](https://github.com/SylarLong/iztro/issues/new?assignees=SylarLong&labels=%E5%8A%9F%E8%83%BD%EF%BD%9Cfeature&projects=&template=new-feature.md&title=%7B%E6%A0%87%E9%A2%98%7D%EF%BD%9C%7Btitle%7D) 创建一个 `功能需求`。
- 如果你发现程序有 BUG，请到 [这里](https://github.com/SylarLong/iztro/issues/new?assignees=SylarLong&labels=%E6%BC%8F%E6%B4%9E%EF%BD%9Cbug&projects=&template=bug-report.md&title=%7Bversion%7D%3A%7Bfunction%7D-) 创建一个 `BUG 报告`。
- 你也可以将本仓库 `fork` 到你自己的仓库进行编辑，然后提交 PR 到本仓库。
- 假如你擅长外语，我们也欢迎你对国际化文件的翻译做出你的贡献，你可以 `fork` 本仓库，然后在 [locales](https://github.com/SylarLong/iztro/tree/main/src/i18n/locales) 文件夹下创建一个国际化语言文件，然后复制其他语言文件目录里面的文件到你的目录下进行更改。
- 当然，如果你觉得本程序对你有用，请给我买杯咖啡☕️ [![Static Badge](https://img.shields.io/badge/PaypalMe-8A2BE2?logo=paypal&link=https%3A%2F%2Fwww.paypal.com%2Fsylarlong)](https://PayPal.Me/sylarlong)

> [!NOTE]
> 在开始之前，请阅读 [贡献指南](https://github.com/SylarLong/iztro/blob/main/CONTRIBUTING.md)。

## 总结

使用本程序返回的数据，你可以生成这样一张星盘，当然这只是一个例子，你可以把注意力集中在星盘的设计上，也可以把重心放在数据的分析上，本程序为你解决了最繁冗的工作，让你可以把精力更多的放在你所需要关注的事情上面。

<img width="966" alt="image" src="https://github.com/SylarLong/react-iztro/assets/6510425/f4335997-fdd8-42e2-bb1a-600942f9b0ba">

## Star 历史

> [!IMPORTANT]
> 如果你觉得代码对你有用，请点 ⭐ 支持，你的 ⭐ 是我持续更新的动力～

[![Star History Chart](https://api.star-history.com/svg?repos=sylarlong/iztro&type=Date)](https://www.star-history.com/#sylarlong/iztro&Date)

## 版权

[MIT License](https://github.com/SylarLong/iztro/blob/main/LICENSE)

Copyright &copy; 2023 All Contributors

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FSylarLong%2Fiztro.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FSylarLong%2Fiztro?ref=badge_large)

> [!NOTE]
> 请合理使用本开源代码，禁止用于非法目的。

### Locator 2

- Registered: https://www.npmjs.com/package/iztro/v/2.5.8
- Resolved: https://registry.npmjs.org/iztro/2.5.8
- Status: `metadata_only`
- Media type: `application/json`
- SHA-256: `63f4ad00151662f4590c06fb93633eb5d8b262f205c42f9b37b0a2bae12e4d77`
- Note: Retrieved through the npm registry API: https://registry.npmjs.org/iztro/2.5.8

#### Parsed material

# iztro 2.5.8

轻量级紫微斗数星盘生成库。可以通过出生年月日获取到紫微斗数星盘信息、生肖、星座等信息。This is a lightweight kit for generating astrolabes for Zi Wei Dou Shu (The Purple Star Astrology), an ancient Chinese astrology. It allows you to obtain your horoscope and personality analysis.

## Package metadata

- License: `MIT`
- Repository: `{'type': 'git', 'url': 'git+https://github.com/SylarLong/iztro.git'}`
- Dependencies: `{'dayjs': '^1.11.10', 'i18next': '^23.5.1', 'lunar-lite': '^0.2.8', 'lunar-typescript': '^1.7.8'}`

### Locator 3

- Registered: https://docs.iztro.com/quick-start
- Resolved: https://docs.iztro.com/quick-start
- Status: `captured`
- Media type: `text/html; charset=utf-8`
- SHA-256: `ed0fdf329634ecf60404691ec841ec129f97776076fd8fe85fe4909625184a30`

#### Parsed material

iztro官方文档 | 紫微研习社 iztro.com

[Skip to content](#VPContent)

[紫微研习社 iztro.com](/)

Search K

Main Navigation[主页](/)[开发](/quick-start.html)[新手村](/learn/basis.html)[排盘](https://ziwei.pub)[解盘](https://app.ziwei.pro/register?ref=TPgWxvwH)[讨论](https://github.com/SylarLong/iztro/discussions)[关于作者](/about.html)

v2.4.7

[更改日志](https://github.com/SylarLong/iztro/blob/main/CHANGELOG.md)

[NPM地址](https://www.npmjs.com/package/iztro)

简体中文

[繁體中文](/zh_TW/quick-start.html)

[English](/en_US/quick-start.html)



简体中文

[繁體中文](/zh_TW/quick-start.html)

[English](/en_US/quick-start.html)

Appearance



Menu

Return to top

Sidebar Navigation

## iztro开发文档

[

快速开始

](/quick-start.html)

[

类型定义

](/type-definition.html)

[

星盘

](/posts/astrolabe.html)

[

宫位

](/posts/palace.html)

[

星曜

](/posts/star.html)

[

运限

](/posts/horoscope.html)

[

配置和插件

](/posts/config-n-plugin.html)

## 紫微斗数知识

[

基础扫盲

](/learn/basis.html)

[

星盘介绍

](/learn/astrolabe.html)

[

宫位知识

](/learn/palace.html)

[

### 星曜知识

](/learn/star.html)

[

14主星

](/learn/major-star.html)

[

14辅星

](/learn/minor-star.html)

[

37杂耀

](/learn/adj-star.html)

[

48神煞

](/learn/dec-star.html)

[

四化

](/learn/mutagen.html)

[

格局

](/learn/pattern.html)

[

运限

](/learn/horoscope.html)

[

安星诀

](/learn/setup.html)

[

### 紫微斗数全书

](/learn/ancientBook.html)

[

卷一

](/learn/ancientBook-1.html)

[

卷二

](/learn/ancientBook-2.html)

[

卷三

](/learn/ancientBook-3.html)

[

诸星问答论

](/learn/ancientBook-qa.html)

页内导航

Table of Contents for current page

# IZTRO

一套轻量级获取紫微斗数排盘信息的 Javascript 开源库。

## 前言[​](#前言)

欢迎使用`iztro`开发文档！本页将向你介绍如何集成、如何获取数据、以及如何快速得到紫微斗数里一张星盘上的所有数据。如果你只是基础使用者，阅读完本篇文档将足够你日常使用。 如果你已经掌握了本页内容，可以到其他页面进行更深入的探索。如果你对紫微斗数感兴趣，但是有没有相关基础，可以点击[基础知识扫盲](/learn/basis.html) 进行扫盲学习。

你将获取到以下信息：

- 如何将`iztro`安装和集成到你的代码里
- 如何获取到一张星盘
- 如何基于星盘开始分析宫位
- 如何基于宫位开始分析星曜

## 产品[​](#产品)

 |  | 名称 | 链接 | 语言 | 作者 |  | iztro | [GitHub](https://github.com/sylarlong/iztro) ｜[Gitee](https://gitee.com/sylarlong/iztro) | Typescript | [SylarLong](https://github.com/SylarLong) |  | react-iztro | [GitHub](https://github.com/sylarlong/react-iztro) ｜[Gitee](https://gitee.com/sylarlong/react-iztro) | React | [SylarLong](https://github.com/SylarLong) |  | iztro-hook | [GitHub](https://github.com/sylarlong/iztro-hook) ｜[Gitee](https://gitee.com/sylarlong/iztro-hook) | React | [SylarLong](https://github.com/SylarLong) |  | py-iztro | [GitHub](https://github.com/x-haose/py-iztro) ｜[Gitee](https://gitee.com/x-haose/py-iztro) | Python | [昊色居士](https://github.com/x-haose) |  | dart_iztro | [GitHub](https://github.com/EdwinXiang/dart_iztro) ｜[Gitee](https://gitee.com/EdwinXiang/dart_iztro) | Dart | [EdwinXiang](https://github.com/EdwinXiang)

## 安装[​](#安装)

### 使用包管理安装[​](#使用包管理安装)

你可以使用任意一种你熟悉的包管理工具进行安装

npm yarn pnpm bun

sh

```text
npm install iztro -S
```

安装顺利的话，会在你的`package.json`依赖列表中找到`iztro`

json

```text
"dependencies": {
  "iztro": "^1.1.0"
}
```

>

版本号可能会有所不同

### 纯JS库使用 ^2.0.4[​](#纯js库使用)

在`v2.0.4`版本以后，编译了`umd`的纯Javascript库。可以下载[release](https://github.com/SylarLong/iztro/releases) 资源文件中的`🗜️iztro-min-js.tar.gz`压缩包，里面包含了一个`iztro`压缩混淆过的js文件和对应的sourcemap文件。

当然，我们更推荐你直接使用`CDN`加速链接，你可以在下面列表中选择一个，在没有指定版本号的时候，会自动指向最新版本的代码库

-

jsdelivr

  - [https://cdn.jsdelivr.net/npm/iztro/dist/iztro.min.js](https://cdn.jsdelivr.net/npm/iztro/dist/iztro.min.js)
  - [https://cdn.jsdelivr.net/npm/ [email protected] /dist/iztro.min.js](https://cdn.jsdelivr.net/npm/iztro@2.0.5/dist/iztro.min.js)

-

unpkg

  - [https://unpkg.com/iztro/dist/iztro.min.js](https://unpkg.com/iztro/dist/iztro.min.js)
  - [https://unpkg.com/ [email protected] /dist/iztro.min.js](https://unpkg.com/iztro@2.0.5/dist/iztro.min.js)

你也可以使用如下规则来指定版本：

- `iztro@2`
- `iztro@^2.0.5`
- `[[email protected]](/cdn-cgi/l/email-protection)`

## 开始使用[​](#开始使用)

### 引入代码[​](#引入代码)

你可以根据下列方式将`iztro`引入你的代码

ES6 Module CommonJS HTML

ts

```text
import { astro } from "iztro";
```

### 获取星盘数据[​](#获取星盘数据)

在获取紫微斗数星盘的时候，可以根据`农历`或者`阳历`日期来获取，`iztro`提供了这两种获取方式，你可以根据你的需求使用，但我们更推荐你使用`阳历`的方式来使用。 放心，阳历和农历在程序内部获取到的数据是统一的。

使用`阳历`有如下便利性：

- 可以很方便的在出生证上查到
- 可以使用日历组件进行日期选择
- 现在很多人都无法记住农历日期
- 可以避免因为忽略了闰月而带来的一系列问题

ES6 Module CommonJS

ts

```text
import { astro } from "iztro";

// 通过阳历获取星盘信息
const astrolabe = astro.bySolar("2000-8-16", 2, "女");

// 通过农历获取星盘信息
const astrolabe = astro.byLunar("2000-7-17", 2, "女");
```

你会发现以上`bySolar`和`byLunar`的返回值是一样的， 这是因为`byLunar`方法在内部处理的时候，也是将日期转化为`阳历`以后调用`bySolar`方法。 以下是执行结果，因为结果比较长，所以将之折叠起来，如果你想要查看你调用结果是否和这个一样，可以展开查看：

`astro.bySolar()`和`astro.byLunar()`方法执行结果

ts

```text
{
  // 阳历日期
  solarDate: '2000-8-16',
   // 农历日期
  lunarDate: '二〇〇〇年七月十七',
  // 四柱
  chineseDate: '庚辰 甲申 丙午 庚寅',
  // 时辰
  time: '寅时',
  // 时辰对应的时间段
  timeRange: '03:00~05:00',
  // 星座
  sign: '狮子座',
  // 生肖
  zodiac: '龙',
  // 命宫地支
  earthlyBranchOfSoulPalace: '午',
  // 身宫地支
  earthlyBranchOfBodyPalace: '戌',
  // 命主
  soul: '破军',
  // 身主
  body: '文昌',
  // 五行局
  fiveElementsClass: '木三局',
  // 十二宫数据
  palaces: [
    {
      // 宫名
      name: '财帛',
      // 是否身宫
      isBodyPalace: false,
      // 是否来因宫
      isOriginalPalace: false,
      // 宫位天干
      heavenlyStem: '戊',
      // 宫位地支
      earthlyBranch: '寅',
      // 主星（含天马禄存）
      majorStars: [
        { name: '武曲', type: 'major', scope: 'origin', brightness: '得' },
        { name: '天相', type: 'major', scope: 'origin', brightness: '庙' },
        { name: '天马', type: 'tianma', scope: 'origin', brightness: '' },
      ],
      // 辅星（含六吉六煞）
      minorStars: [],
      // 杂耀
      adjectiveStars: [
        { name: '月解', type: 'helper', scope: 'origin' },
        { name: '三台', type: 'adjective', scope: 'origin' },
        { name: '天寿', type: 'adjective', scope: 'origin' },
        { name: '天巫', type: 'adjective', scope: 'origin' },
        { name: '天厨', type: 'adjective', scope: 'origin' },
        { name: '阴煞', type: 'adjective', scope: 'origin' },
        { name: '天哭', type: 'adjective', scope: 'origin' },
      ],
      // 长生12神
      changsheng12: '绝',
      // 博士12神
      boshi12: '蜚廉',
      // 流年将前12神
      jiangqian12: '岁驿',
      // 流年岁前12神
      suiqian12: '吊客',
      // 大限
      stage: { range: [44, 53], heavenlyStem: '戊' },
      // 小限
      ages: [9, 21, 33, 45, 57, 69, 81],
    },
    {
      name: '子女',
      isBodyPalace: false,
      isOriginalPalace: false,
      heavenlyStem: '己',
      earthlyBranch: '卯',
      majorStars: [
        { name: '太阳', type: 'major', scope: 'origin', brightness: '庙' },
        { name: '天梁', type: 'major', scope: 'origin', brightness: '庙' },
      ],
      minorStars: [],
      adjectiveStars: [{ name: '天刑', type: 'adjective', scope: 'origin' }],
      changsheng12: '墓',
      boshi12: '奏书',
      jiangqian12: '息神',
      suiqian12: '病符',
      stage: { range: [34, 43], heavenlyStem: '己' },
      ages: [8, 20, 32, 44, 56, 68, 80],
    },
    {
      name: '夫妻',
      isBodyPalace: false,
      isOriginalPalace: true,
      heavenlyStem: '庚',
      earthlyBranch: '辰',
      majorStars: [{ name: '七杀', type: 'major', scope: 'origin', brightness: '庙' }],
      minorStars: [
        { name: '右弼', type: 'soft', scope: 'origin', brightness: '' },
        { name: '火星', type: 'tough', scope: 'origin', brightness: '陷' },
      ],
      adjectiveStars: [
        { name: '封诰', type: 'adjective', scope: 'origin' },
        { name: '华盖', type: 'adjective', scope: 'origin' },
      ],
      changsheng12: '死',
      boshi12: '将军',
      jiangqian12: '华盖',
      suiqian12: '岁建',
      stage: { range: [24, 33], heavenlyStem: '庚' },
      ages: [7, 19, 31, 43, 55, 67, 79],
    },
    {
      name: '兄弟',
      isBodyPalace: false,
      isOriginalPalace: false,
      heavenlyStem: '辛',
      earthlyBranch: '巳',
      majorStars: [{ name: '天机', type: 'major', scope: 'origin', brightness: '平' }],
      minorStars: [],
      adjectiveStars: [
        { name: '天喜', type: 'flower', scope: 'origin' },
        { name: '天空', type: 'adjective', scope: 'origin' },
        { name: '孤辰', type: 'adjective', scope: 'origin' },
      ],
      changsheng12: '病',
      boshi12: '小耗',
      jiangqian12: '劫煞',
      suiqian12: '晦气',
      stage: { range: [14, 23], heavenlyStem: '辛' },
      ages: [6, 18, 30, 42, 54, 66, 78],
    },
    {
      name: '命宫',
      isBodyPalace: false,
      isOriginalPalace: false,
      heavenlyStem: '壬',
      earthlyBranch: '午',
      majorStars: [{ name: '紫微', type: 'major', scope: 'origin', brightness: '庙' }],
      minorStars: [{ name: '文曲', type: 'soft', scope: 'origin', brightness: '陷' }],
      adjectiveStars: [
        { name: '年解', type: 'helper', scope: 'origin' },
        { name: '凤阁', type: 'adjective', scope: 'origin' },
        { name: '天福', type: 'adjective', scope: 'origin' },
        { name: '截路', type: 'adjective', scope: 'origin' },
        { name: '蜚廉', type: 'adjective', scope: 'origin' },
      ],
      changsheng12: '衰',
      boshi12: '青龙',
      jiangqian12: '灾煞',
      suiqian12: '丧门',
      stage: { range: [4, 13], heavenlyStem: '壬' },
      ages: [5, 17, 29, 41, 53, 65, 77],
    },
    {
      name: '父母',
      isBodyPalace: false,
      isOriginalPalace: false,
      heavenlyStem: '癸',
      earthlyBranch: '未',
      majorStars: [],
      minorStars: [
        { name: '天钺', type: 'soft', scope: 'origin', brightness: '' },
        { name: '陀罗', type: 'tough', scope: 'origin', brightness: '庙' },
      ],
      adjectiveStars: [
        { name: '天姚', type: 'flower', scope: 'origin' },
        { name: '空亡', type: 'adjective', scope: 'origin' },
      ],
      changsheng12: '帝旺',
      boshi12: '力士',
      jiangqian12: '天煞',
      suiqian12: '贯索',
      stage: { range: [114, 123], heavenlyStem: '癸' },
      ages: [4, 16, 28, 40, 52, 64, 76],
    },
    {
      name: '福德',
      isBodyPalace: false,
      isOriginalPalace: false,
      heavenlyStem: '甲',
      earthlyBranch: '申',
      majorStars: [
        { name: '破军', type: 'major', scope: 'origin', brightness: '得' },
        { name: '禄存', type: 'lucun', scope: 'origin', brightness: '' },
      ],
      minorStars: [{ name: '文昌', type: 'soft', scope: 'origin', brightness: '得' }],
      adjectiveStars: [
        { name: '龙池', type: 'adjective', scope: 'origin' },
        { name: '台辅', type: 'adjective', scope: 'origin' },
        { name: '旬空', type: 'adjective', scope: 'origin' },
      ],
      changsheng12: '临官',
      boshi12: '博士',
      jiangqian12: '指背',
      suiqian12: '官符',
      stage: { range: [104, 113], heavenlyStem: '甲' },
      ages: [3, 15, 27, 39, 51, 63, 75],
    },
    {
      name: '田宅',
      isBodyPalace: false,
      isOriginalPalace: false,
      heavenlyStem: '乙',
      earthlyBranch: '酉',
      majorStars: [],
      minorStars: [
        { name: '地空', type: 'tough', scope: 'origin', brightness: '' },
        { name: '擎羊', type: 'tough', scope: 'origin', brightness: '陷' },
      ],
      adjectiveStars: [
        { name: '咸池', type: 'flower', scope: 'origin' },
        { name: '天贵', type: 'adjective', scope: 'origin' },
        { name: '月德', type: 'adjective', scope: 'origin' },
      ],
      changsheng12: '冠带',
      boshi12: '官府',
      jiangqian12: '咸池',
      suiqian12: '小耗',
      stage: { range: [94, 103], heavenlyStem: '乙' },
      ages: [2, 14, 26, 38, 50, 62, 74],
    },
    {
      name: '官禄',
      isBodyPalace: true,
      isOriginalPalace: false,
      heavenlyStem: '丙',
      earthlyBranch: '戌',
      majorStars: [
        { name: '廉贞', type: 'major', scope: 'origin', brightness: '利' },
        { name: '天府', type: 'major', scope: 'origin', brightness: '庙' },
      ],
      minorStars: [{ name: '左辅', type: 'soft', scope: 'origin', brightness: '' }],
      adjectiveStars: [
        { name: '天才', type: 'adjective', scope: 'origin' },
        { name: '天虚', type: 'adjective', scope: 'origin' },
      ],
      changsheng12: '沐浴',
      boshi12: '伏兵',
      jiangqian12: '月煞',
      suiqian12: '大耗',
      stage: { range: [84, 93], heavenlyStem: '丙' },
      ages: [1, 13, 25, 37, 49, 61, 73],
    },
    {
      name: '仆役',
      isBodyPalace: false,
      isOriginalPalace: false,
      heavenlyStem: '丁',
      earthlyBranch: '亥',
      majorStars: [{ name: '太阴', type: 'major', scope: 'origin', brightness: '庙' }],
      minorStars: [],
      adjectiveStars: [
        { name: '红鸾', type: 'flower', scope: 'origin' },
        { name: '恩光', type: 'adjective', scope: 'origin' },
        { name: '天官', type: 'adjective', scope: 'origin' },
        { name: '天月', type: 'adjective', scope: 'origin' },
        { name: '天伤', type: 'adjective', scope: 'origin' },
      ],
      changsheng12: '长生',
      boshi12: '大耗',
      jiangqian12: '亡神',
      suiqian12: '龙德',
      stage: { range: [74, 83], heavenlyStem: '丁' },
      ages: [12, 24, 36, 48, 60, 72, 84],
    },
    {
      name: '迁移',
      isBodyPalace: false,
      isOriginalPalace: false,
      heavenlyStem: '戊',
      earthlyBranch: '子',
      majorStars: [{ name: '贪狼', type: 'major', scope: 'origin', brightness: '旺' }],
      minorStars: [{ name: '铃星', type: 'tough', scope: 'origin', brightness: '陷' }],
      adjectiveStars: [{ name: ' 八座', type: 'adjective', scope: 'origin' }],
      changsheng12: '养',
      boshi12: '病符',
      jiangqian12: '将星',
      suiqian12: '白虎',
      stage: { range: [64, 73], heavenlyStem: '戊' },
      ages: [11, 23, 35, 47, 59, 71, 83],
    },
    {
      name: '疾厄',
      isBodyPalace: false,
      isOriginalPalace: false,
      heavenlyStem: '己',
      earthlyBranch: '丑',
      majorStars: [
        { name: '天同', type: 'major', scope: 'origin', brightness: '不' },
        { name: '巨门', type: 'major', scope: 'origin', brightness: '不' },
      ],
      minorStars: [
        { name: '天魁', type: 'soft', scope: 'origin', brightness: '' },
        { name: '地劫', type: 'tough', scope: 'origin', brightness: '' },
      ],
      adjectiveStars: [
        { name: '天德', type: 'adjective', scope: 'origin' },
        { name: '寡宿', type: 'adjective', scope: 'origin' },
        { name: '破碎', type: 'adjective', scope: 'origin' },
        { name: '天使', type: 'adjective', scope: 'origin' },
      ],
      changsheng12: '胎',
      boshi12: '喜神',
      jiangqian12: '攀鞍',
      suiqian12: '天德',
      stage: { range: [54, 63], heavenlyStem: '己' },
      ages: [10, 22, 34, 46, 58, 70, 82],
    },
  ],
}
```

### 方法定义[​](#方法定义)

-

通过阳历日期获取星盘信息

`astro`.`bySolar(solarDateStr, timeIndex, gender, fixLeap, language)`

  -

参数

 | 参数 | 类型 | 是否必填 | 默认值 | 说明 | solarDateStr | `string` | `true` | - | 阳历日期【YYYY-M-D】 | timeIndex | `number` | `true` | - | 出生时辰序号【0~12】，对应从早子时（0）一直到晚子时（12）的序号 | gender | `string` | `true` | - | 性别【男/女】 | fixLeap | `boolean` | `false` | `true` | 是否调整闰月，为`true`闰月的前半个月算上个月，后半个月算下个月 | language | `Language` | `false` | `zh-CN` | 返回数据将被国际化为指定语言。目前支持`zh-CN`,`zh-TW`,`en-US`,`ko-KR`和`ja-JP`

  -

返回值

[`FunctionalAstrolabe`](./posts/astrolabe.html#functionalastrolabe)

-

通过农历日期获取星盘信息

`astro`.`byLunar(lunarDateStr, timeIndex, gender, isLeapMonth, fixLeap, language)`

  -

参数

 | 参数 | 类型 | 是否必填 | 默认值 | 说明 | lunarDateStr | `string` | `true` | - | 农历日期【YYYY-M-D】，例如`2000年七月十七`则传入`2000-7-17` | timeIndex | `number` | `true` | - | 出生时辰序号【0~12】，对应从早子时（0）一直到晚子时（12）的序号 | gender | `string` | `true` | - | 性别【男/女】 | isLeapMonth | `boolean` | `false` | `false` | 是否闰月，当实际月份没有闰月时该参数不生效 | fixLeap | `boolean` | `false` | `true` | 是否调整闰月，为`true`闰月的前半个月算上个月，后半个月算下个月 | language | `Language` | `false` | `zh-CN` | 返回数据将被国际化为指定语言。目前支持`zh-CN`,`zh-TW`,`en-US`,`ko-KR`和`ja-JP`

  -

返回值

[`FunctionalAstrolabe`](./posts/astrolabe.html#functionalastrolabe)

## 获取运限[​](#获取运限)

紫微斗数的运限分为`大限`、`流年`、`流月`、`流日`、`流时`、`流分`、`流秒`，由于`流分`、`流秒`使用场景不多，所以我们暂时不提供。`大限`、`流年`、`流月`、`流日`、`流时`已经能满足绝大部分需求和使用场景了，使用`iztro`能够很轻松的获取到这些数据。

ES6 Module CommonJS

ts

```text
import { astro } from "iztro";

// 通过阳历获取星盘信息
const astrolabe = astro.bySolar("2000-8-16", 2, "女");

// 获取运限数据
astrolabe.horoscope(new Date());
```

调用`astrolabe`.`horoscope()`方法以后你会获得如下数据

`horoscope()`方法返回数据

ts

```text
{
  solarDate: "2023-8-28"
  lunarDate: "二〇二三年七月十三"
  decadal: {
    index: 2
    heavenlyStem: "庚"
    earthlyBranch: "辰"
    palaceNames: ["夫妻", "兄弟", "命宫", "父母", "福德", "田宅", "官禄", "仆役", "迁移", "疾厄", "财帛", "子女"]
    mutagen: ["太阳", "武曲", "太阴", "天同"]
    stars: [{name: "运马", type: "tianma", scope: "decadal"}], …]
    age: {
      index: 10
      nominalAge: 23
    }
  },
  yearly: {
    index: 1
    heavenlyStem: "癸"
    earthlyBranch: "卯"
    palaceNames: ["兄弟", "命宫", "父母", "福德", "田宅", "官禄", "仆役", "迁移", "疾厄", "财帛", "子女", "夫妻"]
    mutagen: ["破军", "巨门", "太阴", "贪狼"]
    stars: [[], [{name: "流魁", type: "soft", scope: "yearly"}, …], [], …]
  },
  monthly: {
  index: 3
    heavenlyStem: "庚"
    earthlyBranch: "申"
    palaceNames: ["子女", "夫妻", "兄弟", "命宫", "父母", "福德", "田宅", "官禄", "仆役", "迁移", "疾厄", "财帛"]
    mutagen: ["太阳", "武曲", "太阴", "天同"]
  },
  daily: {
    index: 3
    heavenlyStem: "戊"
    earthlyBranch: "午"
    palaceNames: ["子女", "夫妻", "兄弟", "命宫", "父母", "福德", "田宅", "官禄", "仆役", "迁移", "疾厄", "财帛"]
    mutagen: ["贪狼", "太阴", "右弼", "天机"]
  },
  hourly: {
    index: 3
    heavenlyStem: "壬"
    earthlyBranch: "子"
    palaceNames: ["子女", "夫妻", "兄弟", "命宫", "父母", "福德", "田宅", "官禄", "仆役", "迁移", "疾厄", "财帛"]
    mutagen: ["天梁", "紫微", "左辅", "武曲"]
  }
}
```

>

Tips: 上面的运限数据和你调用的会因为传入的时间参数不同而不同，但是结构上是一致的。

### 方法定义[​](#方法定义-1)

-

获取当前星盘的运限信息

`astrolabe`.`horoscope(date, timeIndex)`

  -

参数

 | 参数 | 类型 | 是否必填 | 默认值 | 说明 | date | `string`|`Date` | `false` | `new Date()` | 阳历日期字符串或日期对象，若时间字符串或日期对象中包含了小时的信息，`timeIndex`可以省略 | timeIndex | `number` | `false` | `0` | 时辰序号，若不传该参数则会尝试从`date`里获取小时信息转化为时辰序号

  -

返回值

[`Horoscope`](./type-definition.html#horoscope)

## 获取流耀[​](#获取流耀)

上面的`horoscope()`方法内已经包含了`大限`和`流年`的流耀，所以一般情况下无需在单独调用获取流耀的方法，但也有例外的情况需要自行获取流耀，那就需要调用下列方法自行获取。

ES6 Module CommonJS

ts

```text
import { star } from "iztro";

// 通过天干地支获取流耀
const horoscopeStars = star.getHoroscopeStar("庚", "辰", "decadal");
```

调用`star`.`getHoroscopeStar()`方法以后你会获得如下数据

`getHoroscopeStar()`方法返回数据

ts

```text
[
  [{ name: "运马", type: "tianma", scope: "decadal" }],
  [{ name: "运曲", type: "soft", scope: "decadal" }],
  [],
  [{ name: "运喜", type: "flower", scope: "decadal" }],
  [],
  [
    { name: "运钺", type: "soft", scope: "decadal" },
    { name: "运陀", type: "tough", scope: "decadal" },
  ],
  [{ name: "运禄", type: "lucun", scope: "decadal" }],
  [{ name: "运羊", type: "tough", scope: "decadal" }],
  [],
  [
    { name: "运昌", type: "soft", scope: "decadal" },
    { name: "运鸾", type: "flower", scope: "decadal" },
  ],
  [],
  [{ name: "运魁", type: "soft", scope: "decadal" }],
];
```

### 方法定义[​](#方法定义-2)

-

通过`天干`、`地支`获取流耀

`star`.`getHoroscopeStar(heavenlyStem, earthlyBranch, scope)`

  -

参数

 | 参数 | 类型 | 是否必填 | 默认值 | 说明 | heavenlyStem | `HeavenlyStemName` | `true` | - | 天干 | earthlyBranch | `EarthlyBranchName` | `true` | - | 地支 | scope | `'decadal'`|`'yearly'` | `true` | - | 限定是大限还是流年的流耀，其中大限流耀会在星曜前面加上`运`，流年流耀会在星曜前面加上`流`，`年解`比较特殊，只会出现在流年的流耀里

  -

返回值

[`Star[][]`](./type-definition.html#star)

## ☕ 总结[​](#☕-总结)

如果您觉得本程序对您有用的话，可以给我带杯咖啡吗？👍[Paypal Me](https://PayPal.Me/sylarlong)

以上数据可以生成如下星盘，其中`palaces`数据用于填充 12 宫，其他数据用于填充中宫。图片中流耀的显示和实际上有偏差，那是因为图片是古早以前的一个版本生成的，请以实际返回数据为准。

## 📜 版权[​](#📜-版权)

MIT License

Copyright © 2023 Sylar Long

请合理使用本开源代码，禁止用于非法目的。

[Next page 类型定义](/type-definition.html)

© 2025 iztro.com All rights reserved.
友情链接：[紫微派](https://ziwei.pub)

## Manifest quality note

Comparison reference only; the production runtime never imports, invokes, vendors, or packages iztro.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `77976cf604ae7f356ee7a341cdab26994083a743996c87cd97260c1a800c908c`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
