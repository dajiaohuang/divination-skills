# Vedic 多流派实现审计

## 结论

Vedic / Jyotiṣa 已作为第 11 个独立体系加入仓库。公共层负责时间、天文、
真 Citra 恒星黄道、平均交点、上升点、星座、星宿与宫位事实；其上运行三个
互不混用的模块：

| 模块 | 已实现 | 明确未实现 |
|---|---|---|
| Parāśarī | D1 整宫、27 星宿/四足、D9、Vimśottarī 大运 | 其他分盘、分运、力量、瑜伽、断事与补救 |
| Jaimini | 七/八 chara kāraka、rāśi dṛṣṭi、ārūḍha lagna | Chara Daśā、argalā、upapada、寿命与事件判断 |
| KP | 星座主、星宿主、九段不等长 Sub-lord | Placidus 宫头、宫头 Sub、Ruling Planets、Significator、时问与断事 |

## 资料库

结构化来源已登记并生成可跟踪 Markdown 快照：

- `SRC-VEDIC-BPHS-WIKISOURCE-001`：梵文《Bṛhat Parāśara
  Horāśāstra》Wikisource 转录，转录按 CC BY-SA 单独保留；
- `SRC-VEDIC-BRIHAT-JATAKA-1885-001`：1885 年英译
  《Bṛhat Jātaka》，公版 PDF OCR；
- `SRC-VEDIC-IMD-PANCHANG-001`：印度气象局 Positional Astronomy
  Centre 的现代 nirayana 历算说明，仅元数据；
- `SRC-VEDIC-JAIMINI-RAO-1949-001` 与
  `SRC-VEDIC-JAIMINI-READER-001`：Jaimini 书目与现代流派差异佐证，
  仅元数据／有限事实摘要；
- `SRC-VEDIC-KP-INTRO-001`：KP 九段不等长 Sub-lord 的现代佐证，
  不复制受版权保护的教学文本；
- `SRC-VEDIC-REF-001`：上游 `vedic-astro-skills` 的固定提交与许可记录，
  仅作工程参考；
- `SRC-VEDIC-PROJECT-SPEC-001`：本项目 Apache-2.0 的软件策略、边界与
  分歧决策。

## 计算策略

- 位置：Astronomy Engine 2.1.19 地心视黄经、日期真黄道；
- 恒星黄道：把 Spica/Chitra 的日期黄经固定到恒星黄道 180°；
- Spica：固定 J2000 坐标，不加周年光行差与自行；
- 交点：平均罗睺，计都严格相差 180°；
- 宫位：Parāśarī 层使用恒星黄道上升星座起整宫；
- 边界：内部使用未舍入值和左闭右开区间；
- 时间：IANA 时区、DST 重复时刻必须给出 fold、跳过时刻直接拒绝；
- 范围：1900–2100。

## 与参考仓库的关系

本实现没有复制上游代码、Prompt、Skill 资源、星历文件或依赖清单，也不会在
构建产物中包含忽略目录。逐项对照见
`systems/vedic_astrology/REFERENCE_COMPARISON.md`。

## 审核状态

自动测试证明计算可重放、Schema 与追溯链完整；它不证明占星具有经验预测
效度，也不替代 Parāśarī、Jaimini、KP 三类具名专家的独立审核。正式发布门
继续保持关闭。
