# 上游参考资料登记

外部仓库放在 `references/upstream/`，只用于架构研究、对照和可复现审计，不是本项目生产知识库的一部分。整个 `references/upstream/` 目录由主仓库忽略，不使用 Git submodule。

## REF-REPO-0001：vedic-astro-skills

| 字段 | 值 |
|---|---|
| 上游 | `https://github.com/CNWU16/vedic-astro-skills` |
| 本地路径 | `references/upstream/vedic-astro-skills` |
| 获取日期 | 2026-07-23 |
| 固定提交 | `e6d3d39073baca87f8e540b9b92fa758a1f5085a` |
| 代码许可 | 仓库声明为 AGPL-3.0 |
| 指令/资源附加条款 | `COMMERCIAL_NOTICE` 声明 SKILL、prompt、resources 和 references 未经书面许可不得用于向第三方提供商业服务 |
| 本项目用途 | 研究模块边界、数据流、验证思路和工程经验 |
| 生产使用 | 默认禁止复制或改写上游提示词及资源；代码复用必须另做许可证与架构审查 |

上述记录用于工程风险控制，不构成法律意见。若计划复用任何具体代码或内容，应以届时的完整许可证、依赖许可证、目标部署方式和专业法律意见为准。

## 可借鉴的抽象思想

- 计算器与解读器分离；
- Reader 在进入解读前执行事实校验；
- Core 与职业、感情、合盘等专项能力分离；
- 时盘作为独立数据流；
- 关键天文和时间数据由计算程序生成，不由模型心算；
- 低置信度输入应显式降级。

这些是通用工程思想。实现时必须从本项目自己的需求、公开规范和获授权来源重新设计数据结构、规则、提示词、测试与文案。

## REF-REPO-0003：iztro

| 字段 | 值 |
|---|---|
| 上游 | `https://github.com/SylarLong/iztro` |
| 本地路径 | `references/upstream/iztro` |
| 获取日期 | 2026-07-23 |
| 固定版本 | tag `2.5.8` |
| 固定提交 | `9d39f1743bf31c2b3c635c9b9556215d9c90ee2c` |
| 许可证 | MIT |
| 本项目用途 | 仅作紫微字段、边界和计算结果的独立对照参考 |
| 生产使用 | 禁止；不导入、不调用、不 vendor、不打包，也不作为 Git 依赖 |

## REF-REPO-0002：kinqimen

| 字段 | 值 |
|---|---|
| 上游 | `https://github.com/kentang2017/kinqimen` |
| 本地路径 | `references/upstream/kinqimen` |
| 获取日期 | 2026-07-23 |
| 固定提交 | `f4c6118665253f897889290d8630f9b4cb3a4404` |
| 许可状态 | 上游 README 声称 MIT，但本次快照未含可核验的 LICENSE 正文，登记为 `NOASSERTION` |
| 本项目用途 | 仅作奇门字段覆盖和独立实现可行性参考 |
| 生产使用 | 禁止；未导入代码、规则、提示词或资源 |

## 不直接继承的做法

- 不维护 Codex、Claude Code、Antigravity 三份手工复制源；
- 不以大型 Markdown 文件作为唯一结构化主数据；
- 不用少量案例的通过率代表整体准确性；
- 不让产品解释与用户反馈污染原始计算事实；
- 不在没有独立来源对照时把单一实现定义为行业标准。

## 更新参考版本

先审查上游差异，再更新固定提交：

```powershell
git -C references/upstream/vedic-astro-skills fetch origin
git -C references/upstream/vedic-astro-skills log --oneline HEAD..origin/main
git -C references/upstream/vedic-astro-skills diff --stat HEAD..origin/main
```

确认后才执行：

```powershell
git -C references/upstream/vedic-astro-skills switch --detach <reviewed-commit>
```

更新本地参考版本时同步修改本文件的提交哈希、获取日期和许可备注。参考目录始终保持忽略，严禁执行 `git add -f references/upstream/`，也不得改成 Git submodule。
