# 全引擎与 Skill 审计（2026-07-24）

## 结论

本轮审计覆盖仓库中的 12 个技术体系目录、约 190 个 Python 模块、141 条结构化规则、
47 份来源清单、1265 条案例记录和 35 个可安装 Skill。审计确认并修复了 12 类实现或
契约缺陷；修复后的全量测试为 `1584 passed`，代码风格、参考库、追溯矩阵、仓库验证、
Skill 官方结构校验和 35 个 Skill 的实际 `--help` 调用全部通过。

在当前已声明的流派、输入范围与测试证据内，没有留下已知且可复现的代码错误。这个结论
不是“所有术数流派绝对正确”的声明：历史文本校勘、流派实践接受度和解释规则仍需具名
领域审阅者验收；回放测试也不等于独立外部验证或经验预测效度。

## 证据标准

本轮按以下强度区分证据，避免把循环回放误写成独立验证：

1. 官方科学或技术资料：时区折叠遵循 Python `zoneinfo`/PEP 495 语义；真太阳时近似式
   对照 NOAA；节气定义与时刻对照香港天文台；西方和印度占星的行星位置由
   Astronomy Engine 计算。Astronomy Engine 官方说明其算法来自 VSOP87/NOVAS，并以
   JPL Horizons 作验证。
2. 独立实现或外部样本：八字有 `lunar_python`、`sxtwl` 差分案例；紫微有用户提供的
   文墨天机 1.1.5 命盘回归；符文字符名直接对照 Python Unicode 数据。
3. 不变量与边界测试：时区缺口/折叠、历法边界、唯一 ID、范围、轮转、对称性、
   不可变输入、确定性随机与拒绝采样均有自动断言。
4. 项目回放：用于证明输出契约与版本稳定，不能单独证明算法来源正确。850 条扩展回放
   在报告中只按“回归证据”计。

主要外部资料：

- [Python `zoneinfo`：模糊时间通过 `fold` 选择](https://docs.python.org/3.10/library/zoneinfo.html)
- [NOAA General Solar Position Calculations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF)
- [香港天文台：二十四节气](https://www.hko.gov.hk/tc/gts/time/24solarterms.htm)
- [Astronomy Engine 官方仓库与验证说明](https://github.com/cosinekitty/astronomy)
- [Unicode 标准：Runic](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-8/)
- [British Museum：Lenormand 游戏牌实物记录](https://www.britishmuseum.org/collection/object/P_1896-0501-387?selectedImageId=1493350001)
- [Project Gutenberg：Waite 的 Tarot 文本](https://www.gutenberg.org/cache/epub/43548/pg43548-images.html)

所有实际使用资料都另有 `catalog/sources/` 或 `systems/*/sources/` 清单、权利状态、
本地 Markdown 快照与 SHA-256；网页链接不是来源台账的替代品。

## 已修复问题

| 严重度 | 范围 | 原问题 | 修复与回归证据 |
|---|---|---|---|
| 高 | 八字流运 | 年、月柱按立春和“节”计算，但时间轴错误地标为公历 1 月 1 日和每月 1 日 | 时间轴改用精确立春及前后节气 UTC 边界；50 条 timing 回放重建，并增加精确边界断言 |
| 高 | 紫微流运 | 流年、流月事实按农历计算，时间轴却使用公历年、月边界 | 改用农历正月初一和实际农历月边界，含闰月标识；增加 2026 年精确回归 |
| 高 | 多体系出生编排 | 对外声明 `previous_month`、`next_month` 两种紫微闰月策略，但原生紫微引擎不支持 | Schema 与运行时只保留原生的 `preserve`、`split_after_15`；支持项路由、非支持项拒绝均有测试 |
| 中 | 规则引擎 | Schema 宣称支持没有替代载荷、运行时也未实现的 `override`；`require_review` 被记录但不生效 | 删除虚假的 `override`，`require_review` 现在产生 `review_required=true`；增加规则回归 |
| 中 | 西方太阳返照 | 牛顿迭代未对最终残差作失败判定；返照本地时间未传递 DST `fold` | 增加收敛残差检查并保留 `fold`，避免模糊本地时刻被拒绝或重解释 |
| 中 | 导入器/校验器 | 八字文本可从任意散文中抓取四柱；西方导入可接受重复天体、非法宫位和错误字段类型 | 八字要求恰好四个分隔柱并校验干支；西方校验天体唯一性、经度类型和 1–12 宫位 |
| 中 | 校时器 | 未完整落实 Skill 的硬事件约束；重复/空事件 ID 与未知 split 可进入部分路径 | 八字和西方均拒绝人格软描述、重复/空 ID 和非法 split，并保持训练/留出集门槛 |
| 中 | 校时器契约 | 输入允许事件区间，实际评分只取起始日中午，却未对用户披露 | 输出新增 `event_date_policy=start_date_at_local_noon` 和警告；两个 Skill 同步说明；100 条回放重建 |
| 低 | 八字输入 | Python 的 `bool` 是 `int` 子类，导致 `fold=true/false` 绕过整数类型检查 | 显式拒绝布尔值，只接受 0、1 或缺省 |
| 低 | I Ching Skill | 文档仍声明 `zhu-xi-count-routing-v0.2`，引擎、规则和案例已是 v0.3 | Skill 与数据契约统一到 v0.3，并增加跨文件版本门禁 |
| 低 | Vedic Skill CLI | Parāśarī、Jaimini、KP 三个脚本不支持 `--help`，错误结构和输入方式不一致 | 共用 `lineage_cli.py`，统一 argparse、stdin/文件、`--pretty` 和类型化 JSON 错误 |
| 低 | Tarot 日志 | `tags` 传字符串会按字符拆分；非字符串 `occurred_at` 会产生未归一化异常 | 显式类型检查并统一为 `JournalError`；验证失败前不创建日志文件 |

所有因确定性输出变化而更新的案例都由仓库内生成器重建；没有手工修改期望哈希来绕过
失败测试。

## 分体系审计结果

| 体系 | 审计重点 | 当前结论 | 仍需人工验收 |
|---|---|---|---|
| 八字 | 节气年/月柱、日界、时柱、十神、纳音、十二长生、关系、起运、流运、合盘、校时 | 两处时间/输入契约错误已修复；提供的己卯/癸酉/庚午/丙戌样本及独立历法差分保持通过 | 旺衰、格局、调候与各派解释优先级 |
| 紫微斗数 | 农历转换、命身宫、五行局、十四主星、辅煞、四化、三方四正、流限 | 文墨样本五组外部回归通过；流运公历边界错误已修复；项目声明的壬干天府化科差异仍隔离 | 各派四化、自化、亮度与流月/流日解释 |
| 西方占星 | 行星、角点、宫位、相位、返照、行运、合盘、导入与校时 | 天文层使用已验证库；返照与导入鲁棒性问题已修复 | 宫制、容许度和现代/传统判读差异 |
| 印度占星 | 真 Citra 固定 Spica 锚点、平均交点、D1/D9、Vimshottari、Jaimini、有限 KP 身份层 | 公式与已声明范围内部一致；Parāśarī/Jaimini/KP 严格隔离；无参考仓库运行依赖 | ayanāṃśa、真/平均交点、Jaimini 与 KP 实务接受度 |
| 六爻 | 八宫、纳甲、世应、六亲、六神、旬空、动变、项目判定因子 | 表驱动计算、轮转与不变量测试通过，未发现新的可复现代码错误 | 用神、旺衰、应期的流派判断 |
| 奇门 | 三元局数、阴阳遁、地/天盘、门星神、值符值使、空亡与格局标志 | 与声明的项目流派内部一致，未发现新的可复现代码错误 | 拆补/置闰、转盘/飞盘和断局规则 |
| 周易 | 铜钱权重、由下而上、卦序、变爻与两套取爻策略 | v0.3 策略已统一，映射与性质测试通过 | 多动爻取法的版本/传承接受度 |
| Tarot | 无偏抽样、牌阵、正逆位、组合、隐私日志 | 抽样和日志契约通过，错误类型处理已修复 | 现代牌义与组合解释不作古典共识声明 |
| Lenormand | 36 牌身份、牌对、九宫与 Grand Tableau 坐标 | 身份、坐标和无放回抽样测试通过 | 现代组合语义 |
| Runes | 24 Elder Futhark Unicode 身份、历史元数据、现代反思提示隔离 | Unicode 名称与牌组身份测试通过 | 现代占卜释义不是历史共识 |
| 数字命理 | Pythagorean/Chaldean 隔离、转写、归约 | 映射、逐字符轨迹和显式转写门槛通过 | 姓名语言与流派约定 |
| Multi-natal | 共享 UTC、四引擎原生输出、热带坐标审计、有限跨体系导航 | 非原生策略已删除；共享时刻和不等价原则继续通过 | 跨体系综合只能作导航，不能投票或声称相互证实 |

## 35 个 Skill 审计

自动门禁逐个验证了：

- `SKILL.md` frontmatter 存在，`name` 与目录一致，描述包含触发条件且不超过 1024 字符；
- `agents/openai.yaml` 的默认提示显式调用对应 `$skill-name`；
- Markdown 本地引用、跨 Skill 引用、规则 ID 与运行时来源 ID 全部可解析；
- 文档中出现的命令行参数确实由脚本 argparse 注册；
- 35/35 个入口脚本在无输入、无副作用条件下成功执行 `--help`；
- Skill Creator 的 `quick_validate.py` 在 `PYTHONUTF8=1` 下对 35/35 通过。

Windows 默认 GBK 下，Skill Creator 自带校验脚本会因其 `Path.read_text()` 未指定 UTF-8 而
无法读取含中文的合法 Skill。这是外部校验器的区域设置问题，不是仓库文件损坏；仓库自身
所有读取与 CI 均显式使用 UTF-8。

## 发布门禁结果

```text
pytest                                      1584 passed
ruff                                        passed
reference snapshots                         47 / 47 verified
repository validation                       passed
traceability report                         current
Skill metadata/links/rules/flags/help       35 / 35 passed
Skill Creator quick_validate                35 / 35 passed (PYTHONUTF8=1)
```

技术审计通过不自动打开正式发布门槛。当前每个体系的 `expert_accepted` 仍由真实领域审阅者
签署，部署隐私与最终权利决策也不能由自动化伪造。
