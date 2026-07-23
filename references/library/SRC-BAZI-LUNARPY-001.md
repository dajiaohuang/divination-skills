---
source_id: "SRC-BAZI-LUNARPY-001"
title: "lunar-python 1.4.8"
parser_version: "1.0.1"
retrieved_at: "2026-07-23"
manifest_path: "systems/bazi/sources/SRC-BAZI-LUNARPY-001.json"
capture_mode: "full"
aggregate_payload_sha256: "97e4e1859d5b585d35e726ef1ac4042173292a6505393af4e2399a6fcd7f374d"
license: "MIT"
---

# lunar-python 1.4.8

> Generated audit snapshot. The structured source manifest remains the
> authority for rights, lineage, and production status.

## Provenance

- Source ID: `SRC-BAZI-LUNARPY-001`
- Manifest: `systems/bazi/sources/SRC-BAZI-LUNARPY-001.json`
- Type: `software`
- Language: `zh`
- Edition/version: `1.4.8`
- Retrieved: `2026-07-23`
- Usage status: `production`
- Systems: `bazi`, `liuyao`, `qimen`
- Lineages: `ziping-calculation-baseline`, `lunar-python-sect-1`, `lunar-python-sect-2`, `chaibu-rotating-plate-v0.3`

## Rights envelope

- License: `MIT`
- Rights review: `accepted`
- Derivative use: `allowed`
- Dataset use: `allowed`
- Evidence: Repository LICENSE and package metadata both identify the MIT License.

## Locator capture ledger

### Locator 1

- Registered: https://github.com/6tail/lunar-python
- Resolved: https://api.github.com/repos/6tail/lunar-python
- Status: `captured`
- Media type: `application/json; charset=utf-8`
- SHA-256: `75ae4112fd98cb4be52e774848950ac07f6e04cc7b78c4bc9ac734e20b20efe5`
- Note: Retrieved repository metadata through the GitHub API: https://api.github.com/repos/6tail/lunar-python; README snapshot https://raw.githubusercontent.com/6tail/lunar-python/master/README.md sha256=20104764507ed36a1287d217926925f158e1f873d5727881f5264c6203fe5462

#### Parsed material

# 6tail/lunar-python

日历、公历(阳历)、农历(阴历、老黄历)、佛历、道历，支持节假日、星座、儒略日、干支、生肖、节气、节日、彭祖百忌、每日宜忌、吉神宜趋凶煞宜忌、吉神(喜神/福神/财神/阳贵神/阴贵神)方位、胎神方位、冲煞、纳音、星宿、八字、五行、十神、建除十二值星、青龙名堂等十二神、黄道黑道日及吉凶等。lunar is a calendar library for Solar and Chinese Lunar.

## Repository metadata

- Default branch: `master`
- License: `MIT`
- Archived: `False`
- Created: `2020-05-13T13:37:04Z`
- Updated: `2026-07-19T17:32:10Z`
- Repository: https://github.com/6tail/lunar-python

## Upstream README

# lunar [![License](https://img.shields.io/badge/license-MIT-4EB1BA.svg?style=flat-square)](https://github.com/6tail/lunar-python/blob/master/LICENSE)

lunar是一款无第三方依赖的公历(阳历)、农历(阴历、老黄历)、佛历和道历工具，支持星座、儒略日、干支、生肖、节气、节日、彭祖百忌、吉神(喜神/福神/财神/阳贵神/阴贵神)方位、胎神方位、冲煞、纳音、星宿、八字、五行、十神、建除十二值星、青龙名堂等十二神、黄道日及吉凶、法定节假日及调休等。

> v1.2.23起不再兼容python2。

[English](https://github.com/6tail/lunar-python/blob/master/README_EN.md)

## 示例

    $ pip install lunar_python

    from lunar_python import Lunar

    # 通过指定年月日初始化阴历
    lunar = Lunar.fromYmd(1986, 4, 21)

    # 打印阴历
    print(lunar.toFullString())

    # 阴历转阳历并打印
    print(lunar.getSolar().toFullString())

输出结果：

    一九八六年四月廿一 丙寅(虎)年 癸巳(蛇)月 癸酉(鸡)日 子(鼠)时 纳音[炉中火 长流水 剑锋金 桑柘木] 星期四 北方玄武 星宿[斗木獬](吉) 彭祖百忌[癸不词讼理弱敌强 酉不会客醉坐颠狂] 喜神方位[巽](东南) 阳贵神方位[巽](东南) 阴贵神方位[震](正东) 福神方位[兑](正西) 财神方位[离](正南) 冲[(丁卯)兔] 煞[东]
    1986-05-29 00:00:00 星期四 双子座

## 文档

请移步至 [https://6tail.cn/calendar/api.html](https://6tail.cn/calendar/api.html "https://6tail.cn/calendar/api.html")

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=6tail/lunar-python&type=Date)](https://star-history.com/#6tail/lunar-python&Date)

### Locator 2

- Registered: https://pypi.org/project/lunar-python/1.4.8/
- Resolved: https://pypi.org/pypi/lunar-python/1.4.8/json
- Status: `captured`
- Media type: `application/json`
- SHA-256: `5ab7cdd3c56eacd8cbea34d57e7e1e61b638bd78abb6dbadc2029a62f1dc4f53`
- Note: Retrieved through the PyPI JSON API: https://pypi.org/pypi/lunar-python/1.4.8/json

#### Parsed material

# lunar_python 1.4.8

lunar is a calendar library for Solar and Chinese Lunar.

## Package metadata

- License: MIT
- Python requirement: not declared
- Project URL: https://pypi.org/project/lunar_python/
- Package URL: https://pypi.org/project/lunar_python/

## Declared dependencies


## Published description

lunar is a calendar library for Solar and Chinese Lunar.

## Manifest quality note

Pinned implementation source and comparator, not sole proof of astronomical or lineage correctness.

## Reproducibility

- Parser: `tooling/scripts/build_reference_library.py` v1.0.1
- Aggregate payload SHA-256: `97e4e1859d5b585d35e726ef1ac4042173292a6505393af4e2399a6fcd7f374d`
- Use `--check` to verify tracked snapshot integrity; run without it to refresh remote material.
