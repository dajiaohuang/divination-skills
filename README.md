# divination-skills

多体系、可验证、可追溯的占卜计算与 Skill 工程。项目把输入、计算事实、规则派生、语言解释、来源和人工审核分层保存；任何体系或流派都不能无标注混用。

## 当前实现

| 体系 | v0.1 能力 | Skill |
|---|---|---:|
| 八字 | 子平四柱、节气、藏干、十神、支关系、大运、验证与证据报告 | 3 |
| Tarot | 原创文字版 78 张牌、可审计无放回抽牌、正逆位与三种牌阵 | 2 |
| 西方占星 | 热带黄道、日至冥王星、上升/天顶、整宫/等宫、主要相位 | 2 |
| 紫微斗数 | 项目自有的命身宫、五行局、14 主星、四化与十二宫基础盘；`iztro` 仅作忽略参考 | 1 |
| 周易 | 可重放三钱起卦、64 卦、动爻与变卦结构 | 1 |
| 六爻 | 八宫、世应、纳甲、六亲、六神、旬空与历法上下文 | 1 |
| 奇门遁甲 | 拆补法节气、阴阳遁、三元局、地盘与值符值使原始宫 | 1 |
| Lenormand | 原创文字版 36 张牌与可审计抽取 | 1 |
| 卢恩符文 | 原创文字版 Elder Futhark 24 符文与可审计抽取 | 1 |
| 数字命理 | 英文字母 Pythagorean 映射与核心数字计算 | 1 |

当前共有 10 个体系、14 个 Skill、54 条结构化规则、20 份来源清单、160 个标准 Golden Cases、39 个边界案例、29 个流派分歧案例和 477 项自动化测试。详细状态见[实施状态](docs/IMPLEMENTATION_STATUS.md)，逐项证据见[完成度审计](docs/COMPLETION_AUDIT.md)，原始路线图见[实施计划](docs/IMPLEMENTATION_PLAN.md)。

奇门 v0.1 明确只是基础盘，紫微、易经、六爻、奇门的领域规则仍需独立专家验收。任何未获签署的体系都不能被描述为已经完成生产级领域认证。

## 本地验证

需要 Python 3.12。项目没有 Git submodule，也不把任何其他仓库作为运行依赖。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\pytest.exe -q
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\divination-validate.exe .
.\.venv\Scripts\divination-readiness.exe . --require-technical
.\.venv\Scripts\python.exe -m divination_skills.build . --system all --output dist
```

所有 Skill 包使用固定 ZIP 时间戳和规范化清单构建，并生成 `.sha256` 文件；相同源码应产生相同哈希。产物携带脱离源码仓库运行所需的项目代码和 Python 依赖清单，14 个脚本均在独立解压目录执行测试。`reference_only` 来源不会进入产物。

解压产物后，可在 Skill 根目录执行 `python -m pip install -r requirements.txt` 安装其锁定的直接 Python 依赖；没有 Python 外部依赖的 Skill 会生成空清单。紫微仅复用既有的 `lunar_python` 历法转换，不需要 Node.js 或 `iztro`。

执行 `python scripts/verify_package.py` 可按 `CONTENT_MANIFEST.json` 重新校验解压后的逐文件大小和 SHA-256。项目自有内容采用 [Apache-2.0](LICENSE)；外部来源和依赖仍遵循各自许可证。开源许可不替代领域、版权与隐私发布审核。

## 核心原则

1. 体系与流派隔离：不同体系、流派和年代的规则不得无标注混用。
2. 计算与解释分层：计算事实不能被模型覆盖或改写。
3. 结论可追溯：来源、规则、Golden Case、事实和派生结论使用稳定 ID。
4. 许可优先：没有清晰来源与使用边界的资料不得进入生产目录。
5. 失败关闭：输入、历法或领域证据不足时拒绝或降级，不凭模型记忆补算。
6. 高风险隔离：占卜输出不替代医疗、法律、财务、安全等专业判断。

## 外部参考仓库

外部项目只作独立参考，不作为 Git submodule，也不由主仓库跟踪。`references/upstream/` 已被 `.gitignore` 排除。

```powershell
git clone https://github.com/CNWU16/vedic-astro-skills.git references/upstream/vedic-astro-skills
git -C references/upstream/vedic-astro-skills switch --detach e6d3d39073baca87f8e540b9b92fa758a1f5085a
```

参考项目的代码、提示词、资料与许可证边界分别登记在[参考资料台账](references/README.md)中；不得因本地可见而直接复制到生产知识库。

## 发布门禁

技术验收已经自动化，统一审计当前返回 `technical_complete=10/10`、`release_ready=0/10`、`project_license_status=selected`、`deployment_privacy_status=undecided`。九个扩展体系已有共 78 条待审案例队列；每个体系都需要各自的真实领域、版权和隐私审核，八字还要求 50 份专家候选案例全部获接受。检查命令：

```powershell
.\.venv\Scripts\divination-readiness.exe .
.\.venv\Scripts\python.exe -m systems.bazi.reviews.release --report-only
```

正式发行只能使用 `divination-build . --system all --output <dir> --release`；该命令当前会返回 `release_not_ready` 且不生成产物。不要把不带 `--release` 的内部验证包当成获得授权的发行版。

只有真实审核人完成签署后才可更新相应记录；仓库禁止用虚构姓名或自动生成的“专家通过”绕过门禁。
