# divination-skills

多体系、可验证、可追溯的占卜计算与 Skill 工程。项目把输入、计算事实、规则派生、语言解释、来源和人工审核分层保存；任何体系、流派或年代都不能无标注混用。

项目自有内容采用 [Apache-2.0](LICENSE)。仓库没有 Git submodule，也不把任何其他 Git 仓库作为运行、构建或测试依赖。

## 当前实现

| 体系 | 版本 | 主要能力 | Skill |
|---|---:|---|---:|
| 八字 | 0.2 | 四柱、节气、藏干、十神、支关系、大运、导入校验、时序、合盘事实与时辰区间扫描 | 7 |
| Tarot | 0.2 | 原创文字版 78 张牌、七种牌阵、正逆位、组合摘要、同意后本地日记与描述统计 | 3 |
| 西方占星 | 0.2 | 热带黄道、本命、整宫/等宫、主要相位、行运、太阳返照、合盘与出生时间区间扫描 | 7 |
| 紫微斗数 | 0.4 | 原生命盘、扩展星曜、四套十二神、六层运限、查询分析、导入校验、结构解读与双盘比较 | 6 |
| 周易 | 0.2 | 可重放三钱起卦、64 卦、动爻与变卦、两种显式动爻取用策略及经典来源定位层 | 1 |
| 六爻 | 0.2 | 八宫、世应、纳甲、六亲、六神、旬空，以及显式问题包下的候选用神、强度与动变事实 | 2 |
| 奇门遁甲 | 0.2 | 拆补转盘的地盘、天盘、九星、八门、八神、值符值使及空亡/入墓/击刑/门迫结构 | 1 |
| Lenormand | 0.2 | 原创文字版 36 张牌、牌对、九宫与 4×9 Grand Tableau 宫位/坐标 | 1 |
| 卢恩符文 | 0.2 | Elder Futhark 24 符文、可审计抽取、历史证据层与现代反思层隔离 | 1 |
| 数字命理 | 0.2 | Pythagorean 与独立 Chaldean 映射；非拉丁姓名只接受用户明确提供的完整拉丁转写 | 1 |

当前技术快照：

- 10 个体系、30 个 Skill、101 条结构化规则、27 份来源清单；
- 255 个基线 Golden Cases、68 个边界案例、48 个流派分歧案例、20 个错误输入案例；
- 850 个 M10–M13 扩展功能回放案例；
- 221 条待真实领域审核的扩展体系案例，另有八字 50 份专家候选；
- 1497 项自动化测试全部通过。

路线与证据见[扩展功能计划](docs/EXTENSION_PLAN.md)、[实施状态](docs/IMPLEMENTATION_STATUS.md)和[完成度审计](docs/COMPLETION_AUDIT.md)。

## 本地验证

需要 Python 3.12。使用 `uv`：

```powershell
uv sync --extra dev
uv run pytest -q
uv run ruff check .
uv run divination-validate .
uv run divination-readiness . --require-technical
uv run python -m divination_skills.build . --system all --output dist
```

构建器为每个 Skill 生成固定时间戳、规范清单、逐文件 SHA-256、直接依赖清单和 Apache-2.0 许可说明。30 个 ZIP 可重复构建，并在脱离源码仓库的解压目录执行入口工作流。`reference_only` 来源与被忽略的参考仓库不会进入产物。

解压后可执行 `python scripts/verify_package.py` 校验 `CONTENT_MANIFEST.json`。有直接 Python 依赖的 Skill 会在 `requirements.txt` 中固定版本；这不构成对其他 Git 仓库的依赖。紫微不需要 Node.js 或 `iztro`。

## 核心原则

1. 体系与流派隔离：不同体系、流派和年代的规则不得无标注混用。
2. 计算与解释分层：计算事实不能被模型覆盖或改写。
3. 结论可追溯：来源、规则、案例、事实和派生结论使用稳定 ID。
4. 许可优先：没有清晰来源与使用边界的资料不得进入生产目录。
5. 失败关闭：输入、历法或领域证据不足时拒绝或降级，不凭模型记忆补算。
6. 高风险隔离：输出不替代医疗、法律、财务、安全等专业判断。

## 外部参考仓库

外部项目只作独立参考，不作为 submodule，也不由主仓库跟踪。`references/upstream/` 已被 `.gitignore` 排除。

```powershell
git clone https://github.com/CNWU16/vedic-astro-skills.git references/upstream/vedic-astro-skills
git -C references/upstream/vedic-astro-skills switch --detach e6d3d39073baca87f8e540b9b92fa758a1f5085a
git clone https://github.com/SylarLong/iztro.git references/upstream/iztro
git -C references/upstream/iztro switch --detach 2.5.8
```

参考代码、提示词、资料、翻译与数据表不会复制进本项目。具体边界登记在[参考资料台账](references/README.md)。

## 发布门禁

技术路线已经完成，统一审计返回：

```text
technical_complete = 10 / 10
release_ready = 0 / 10
project_license_status = selected
deployment_privacy_status = undecided
```

这表示代码、契约、测试和普通验证包已经就绪，不表示领域内容已获专业认可，也不表示实际部署的版权与隐私方案已批准。正式发行必须使用：

```powershell
uv run divination-build . --system all --output <dir> --release
```

在真实审核人完成各体系领域、版权与隐私签核，以及所有者记录实际部署的数据流之前，该命令会返回 `release_not_ready` 且不生成正式发行产物。仓库禁止自动伪造审核身份或“专家通过”状态。
