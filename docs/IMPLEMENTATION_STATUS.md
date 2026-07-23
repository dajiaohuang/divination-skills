# 实施状态

日期：2026-07-24

技术状态：`IMPLEMENTATION_PLAN.md` 的 M0–M5、`EXTENSION_PLAN.md` 的 M6–M13、Vedic M14 与综合本命 M15 已全部实现并通过全仓自动化验收

发布状态：未正式发布；真实领域、版权与部署隐私签署仍是 fail-closed 阻塞项

## 已完成路线

- M0–M1：仓库治理、clean-room、来源接纳、Apache-2.0、核心 Schema、交叉引用验证、CI 和可复现 Skill 构建器。
- M2–M3：八字端到端计算、验证、证据报告、100/30/20/20 基线案例、独立比较、评估与 50 份专家候选。
- M4–M5：Tarot、西方占星、紫微、周易、六爻、奇门、Lenormand、卢恩和数字命理的独立垂直切片。
- M6：六个跨体系会话/导入/置信度/时间线/比较/报告契约，旧盘兼容包装与隐私安全默认值。
- M7：紫微 v0.2 原生本命深度、扩展星曜/十二神目录、版本化历法边界和独立差异分类。
- M8：紫微 v0.3 大限、小限、流年、流月、流日、流时，宫星/三方四正/四化查询与统一时间线。
- M9：紫微 v0.4 结构解读、结构化 Reader/Validator、双盘结构比较、50 份合盘回放案例和 150 条待审领域案例。
- M9.1：紫微 v0.5 真太阳时选项、古典庙旺表、宫干自化路径和扩展外部盘对照；八字补齐纳音、十二长生与旺相休囚死。
- M10：八字与西方占星的 Reader、Validator、Timing、Synastry 和 Rectifier，共 300 个扩展回放案例。
- M11：八字、西方占星和紫微的共享 career/relationship/timing/QA 报告选择层及高影响问题降级。
- M12：三体系双盘比较、八字/西占保留集校时，以及西方卜卦占星的独立体系可行性与来源评估。
- M13：六爻显式问题规则包、奇门完整结构盘、周易来源/动爻策略层、Lenormand Grand Tableau、Tarot 手牌阵/组合/日记、卢恩历史/现代分层、独立 Chaldean 映射。
- M14：独立 Vedic/Jyotiṣa 垂直切片，采用 true-Citra 恒星黄道基线，明确隔离 Parāśarī、Jaimini 与 KP Stellar 三条路径；参考仓库仅作被忽略的 clean-room 对照。
- M15：统一出生资料编排层，一次运行八字、西占、紫微与 Vedic 原生引擎，可选数字命理；校验 UTC 和共同热带天文坐标，只按结构导航轴并列事实，不做跨体系等价或一致性评分。

## 自动化验收快照

| 项目 | 结果 |
|---|---:|
| 技术系统目录 | 12（十一种体系 + 一个综合编排层） |
| Skill | 35 |
| 结构化规则 | 141 |
| 来源清单 | 47 |
| 基线 Golden Cases | 264 |
| 边界案例 | 74 |
| 流派分歧案例 | 55 |
| 错误输入案例 | 20 |
| 扩展功能回放案例 | 850 |
| 待审扩展领域案例 | 243 |
| 八字专家候选 | 50 |
| pytest | 1573 passed |
| Schema/ID/许可交叉引用 | passed |
| 技术完整性 | 12/12 passed |
| 正式发布就绪 | 0/12（等待真实签核） |
| 项目许可证 | Apache-2.0（selected） |
| 部署隐私配置 | undecided（禁止正式发布） |
| Ruff | passed |
| Skill 结构与包外入口验证 | 35 passed |
| 确定性 ZIP 构建 | 35 passed |

## 当前明确边界

- 八字季节支持评分仍是默认关闭、低置信度的工程基线；时序与合盘只返回结构事实，校时不能证明唯一出生分钟。
- 西方占星支持行运、太阳返照、合盘与区间校时，但不支持推运、方向法、组合盘或卜卦占星。卜卦占星已评估为未来独立体系。
- 紫微运行时完全由本项目实现；`iztro` 2.5.8 只在被 Git 忽略的参考目录中用于人工差异比较。
- Vedic 运行时完全由本项目实现；上游 `vedic-astro-skills` 仅作被 Git 忽略的角色边界参考。Parāśarī、Jaimini 和 KP 不共享判读规则，KP v0.1 仅实现 Stellar/Sub-lord 数学身份，不含宫位尖轴、significator 或事件断法。
- 综合本命要求显式 IANA 时区、经纬度、地点解析来源和排盘性别；地点歧义与 DST 重叠时段 fail closed。它保留各原生盘，不把各体系结构转换成通用真理。
- 周易不捆绑经典译文，两个动爻策略都需独立审校；来源层只提供定位和版本元数据。
- 六爻 v0.2 用神与强度输出是显式问题包下的候选/工程评分，不是专家认可的吉凶或应期结论。
- 奇门 v0.2 提供完整的限定结构盘，但不做用神、断事、择方或事件应期。
- Lenormand Grand Tableau 限于 4×9 宫位与坐标；Tarot 日记默认本地且必须明确同意，统计不衡量预测准确率。
- 卢恩严格分隔历史来源元数据与现代反思关键词；数字命理绝不自动猜测非拉丁姓名转写。
- 风水、手相、面相和 Human Design 不在本轮授权范围内。

## 仍需真实人员完成

当前统一 readiness 返回：

```text
technical_complete = 12 / 12
release_ready = 0 / 12
project_license_status = selected
deployment_privacy_status = undecided
bazi expert_accepted = 0 / 50
extension domain-review cases accepted = 0 / 243
```

发布前需要真实审核人按[八字外部审核指南](../systems/bazi/reviews/REVIEW_GUIDE.md)完成八字 50 份候选，并按[统一发布复核协议](../common/evaluation/RELEASE_REVIEW.md)分别完成十个扩展体系及一个综合编排层的 243 条队列。所有者还必须记录实际部署的数据流、用途、保留期、处理商、安全控制、用户导出/删除和事件响应责任。

各体系必须独立完成领域、版权与隐私验收，不能继承参考项目或另一体系的结论。接受记录必须包含可验证的 SHA-256 证据对象；自动化不得虚构审核身份或签名。

## 验收命令

```powershell
uv run pytest -q
uv run ruff check .
uv run divination-validate .
uv run divination-readiness . --require-technical
uv run python -m divination_skills.build . --system all --output dist
uv run python -m systems.bazi.evaluations.run_evaluation
uv run python -m systems.bazi.reviews.release --report-only
```
