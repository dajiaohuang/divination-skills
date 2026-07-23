"""Generate conventional hexagram identifiers with original project themes."""

from __future__ import annotations

import json
from pathlib import Path

ROWS = [
    (1, "乾", "Qian", "Creative"),
    (2, "坤", "Kun", "Receptive"),
    (3, "屯", "Zhun", "Difficulty at the Beginning"),
    (4, "蒙", "Meng", "Youthful Folly"),
    (5, "需", "Xu", "Waiting"),
    (6, "讼", "Song", "Conflict"),
    (7, "师", "Shi", "Army"),
    (8, "比", "Bi", "Holding Together"),
    (9, "小畜", "Xiao Chu", "Small Taming"),
    (10, "履", "Lu", "Treading"),
    (11, "泰", "Tai", "Peace"),
    (12, "否", "Pi", "Standstill"),
    (13, "同人", "Tong Ren", "Fellowship"),
    (14, "大有", "Da You", "Great Possession"),
    (15, "谦", "Qian", "Modesty"),
    (16, "豫", "Yu", "Enthusiasm"),
    (17, "随", "Sui", "Following"),
    (18, "蛊", "Gu", "Repairing What Was Spoiled"),
    (19, "临", "Lin", "Approach"),
    (20, "观", "Guan", "Contemplation"),
    (21, "噬嗑", "Shi He", "Biting Through"),
    (22, "贲", "Bi", "Grace"),
    (23, "剥", "Bo", "Splitting Apart"),
    (24, "复", "Fu", "Return"),
    (25, "无妄", "Wu Wang", "Innocence"),
    (26, "大畜", "Da Chu", "Great Taming"),
    (27, "颐", "Yi", "Nourishment"),
    (28, "大过", "Da Guo", "Great Exceeding"),
    (29, "坎", "Kan", "Abysmal Water"),
    (30, "离", "Li", "Clinging Fire"),
    (31, "咸", "Xian", "Influence"),
    (32, "恒", "Heng", "Duration"),
    (33, "遁", "Dun", "Retreat"),
    (34, "大壮", "Da Zhuang", "Great Power"),
    (35, "晋", "Jin", "Progress"),
    (36, "明夷", "Ming Yi", "Darkening of Light"),
    (37, "家人", "Jia Ren", "Family"),
    (38, "睽", "Kui", "Opposition"),
    (39, "蹇", "Jian", "Obstruction"),
    (40, "解", "Xie", "Deliverance"),
    (41, "损", "Sun", "Decrease"),
    (42, "益", "Yi", "Increase"),
    (43, "夬", "Guai", "Breakthrough"),
    (44, "姤", "Gou", "Coming to Meet"),
    (45, "萃", "Cui", "Gathering Together"),
    (46, "升", "Sheng", "Pushing Upward"),
    (47, "困", "Kun", "Oppression"),
    (48, "井", "Jing", "Well"),
    (49, "革", "Ge", "Revolution"),
    (50, "鼎", "Ding", "Cauldron"),
    (51, "震", "Zhen", "Arousing Thunder"),
    (52, "艮", "Gen", "Keeping Still"),
    (53, "渐", "Jian", "Development"),
    (54, "归妹", "Gui Mei", "Marrying Maiden"),
    (55, "丰", "Feng", "Abundance"),
    (56, "旅", "Lu", "Wanderer"),
    (57, "巽", "Xun", "Gentle Wind"),
    (58, "兑", "Dui", "Joyous Lake"),
    (59, "涣", "Huan", "Dispersion"),
    (60, "节", "Jie", "Limitation"),
    (61, "中孚", "Zhong Fu", "Inner Truth"),
    (62, "小过", "Xiao Guo", "Small Exceeding"),
    (63, "既济", "Ji Ji", "After Completion"),
    (64, "未济", "Wei Ji", "Before Completion"),
]


def main() -> None:
    output = [
        {
            "number": number,
            "hanzi": hanzi,
            "pinyin": pinyin,
            "english": english,
            "project_themes": [
                f"current structure: {english.lower()}",
                "what can be observed before assuming an outcome",
                "a small reversible response to the present conditions",
            ],
        }
        for number, hanzi, pinyin, english in ROWS
    ]
    path = Path(__file__).with_name("hexagrams.json")
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Generated 64 I Ching identifiers.")


if __name__ == "__main__":
    main()
