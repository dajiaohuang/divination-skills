# 实施状态

日期：2026-07-23
技术状态：M0–M5 既定范围已实现并通过全仓自动化验收
发布状态：未发布；真实领域、版权与隐私签署仍是 fail-closed 阻塞项

## 已完成

- M0：仓库治理、clean-room、来源接纳、贡献、安全、ADR 与 issue 模板。
- M1：四个核心 JSON Schema、可审计报告/评估/签核契约、正反示例、交叉引用与逐体系完整性验证器、CI、确定性 Skill 构建器。
- M2：八字端到端计算、验证和证据报告切片。
- M3：100 标准盘、30 边界案例、20 流派分歧、20 错误输入、50 专家候选、属性测试、隐私政策、Model Card、迁移策略和发布审计。
- M4：Tarot 与西方占星独立垂直切片。
- M5：紫微、周易、六爻、奇门基础盘、Lenormand、卢恩和数字命理垂直切片。
- 发布治理：10 份独立签核记录、九个扩展体系共 78 条领域复核队列、统一 fail-closed readiness 审计。
- Skill 交付：14 个 ZIP 携带最小项目运行时与依赖声明，并通过脱离源码仓库的逐脚本执行测试；紫微传递依赖均带许可通知。
- 审核证据：接受状态必须携带 SHA-256 证据对象；仓库内证据由 readiness 重新哈希，敏感材料可保留在受控外部存储。
- 项目许可：所有者已选择 Apache-2.0；所有产物携带许可证决策与逐文件内容清单。
- 部署数据政策：`DEPLOYMENT_PRIVACY.json` 保持 `undecided`；发布前必须记录实际存储、用途、保留、处理商、安全控制、导出和删除行为。

## 自动化验收快照

| 项目 | 结果 |
|---|---:|
| 体系 | 10 |
| Skill | 14 |
| 结构化规则 | 54 |
| 来源清单 | 20 |
| 标准 Golden Cases | 160 |
| 边界案例 | 39 |
| 流派分歧案例 | 29 |
| pytest | 477 passed |
| Schema/ID/许可交叉引用 | passed |
| 技术完整性 | 10/10 passed |
| 正式发布就绪 | 0/10（等待真实签核） |
| 项目许可证 | Apache-2.0（selected） |
| 部署隐私配置 | undecided（禁止发布） |
| Ruff | passed |
| Skill 结构验证 | 14 passed |
| 确定性 ZIP 构建 | 14 passed |

## 已知范围边界

- 八字的季节支持评分是低置信度、默认关闭的工程基线，不是专家共识。
- 西方占星 v0.1 只支持本命基础事实，不含行运、推运、合盘或卜卦占星。
- 紫微使用项目自有基础排盘；`iztro` 2.5.8 只保留在被 Git 忽略的参考目录，不进入运行时或产物。
- 六爻不选用神，不做旺衰、吉凶和应期。
- 奇门只实现节气、阴阳遁、三元局、地盘和值符值使原始宫；天盘、转动九星八门、八神和断事均未实现。
- Lenormand 与卢恩使用项目原创关键词；卢恩不是历史占卜实践复原。
- 数字命理只处理拉丁字母，不做非拉丁姓名自动转写。
- 风水、手相、面相和 Human Design 不在本轮获授权实现范围内。

## 仍需真实人员完成

八字发布审计当前预期返回：

```text
expert_accepted = 0 / 50
domain signoff = false
rights signoff = false
privacy signoff = false
ready = false
```

需要用户指定真实审核人，按[外部审核指南](../systems/bazi/reviews/REVIEW_GUIDE.md)完成八字 50 份候选案例，并按[统一发布复核协议](../common/evaluation/RELEASE_REVIEW.md)完成九个扩展体系的 78 条复核队列；随后在各体系 `reviews/release-signoff.json` 留下可验证签署。各体系必须分别完成领域验收，不能继承八字或参考项目的审核结论。

## 验收命令

```powershell
.\.venv\Scripts\pytest.exe -q
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\divination-validate.exe .
.\.venv\Scripts\divination-readiness.exe . --require-technical
.\.venv\Scripts\python.exe -m divination_skills.build . --system all --output dist
.\.venv\Scripts\python.exe -m systems.bazi.evaluations.run_evaluation
.\.venv\Scripts\python.exe -m systems.bazi.reviews.release --report-only
```
