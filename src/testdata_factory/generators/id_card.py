"""身份证号生成器"""

import random
from datetime import datetime, timedelta

# 省份代码（部分）
PROVINCE_CODES = {
    "北京": "11",
    "天津": "12",
    "河北": "13",
    "山西": "14",
    "内蒙古": "15",
    "辽宁": "21",
    "吉林": "22",
    "黑龙江": "23",
    "上海": "31",
    "江苏": "32",
    "浙江": "33",
    "安徽": "34",
    "福建": "35",
    "江西": "36",
    "山东": "37",
    "河南": "41",
    "湖北": "42",
    "湖南": "43",
    "广东": "44",
    "广西": "45",
    "海南": "46",
    "重庆": "50",
    "四川": "51",
    "贵州": "52",
    "云南": "53",
    "西藏": "54",
    "陕西": "61",
    "甘肃": "62",
    "青海": "63",
    "宁夏": "64",
    "新疆": "65",
}


def _generate_birthday(min_age: int = 18, max_age: int = 65) -> str:
    """生成出生日期"""
    today = datetime.now()
    min_date = today - timedelta(days=max_age * 365)
    max_date = today - timedelta(days=min_age * 365)

    random_date = min_date + timedelta(
        days=random.randint(0, (max_date - min_date).days)
    )

    return random_date.strftime("%Y%m%d")


def _generate_sequence(gender: int | None = None) -> str:
    """
    生成顺序码（3位）

    Args:
        gender: 1=男，2=女，None=随机

    Returns:
        3位顺序码
    """
    seq = random.randint(1, 999)

    if gender == 1:
        seq = seq if seq % 2 == 1 else seq + 1
    elif gender == 2:
        seq = seq if seq % 2 == 0 else seq + 1

    return f"{seq:03d}"


def _calculate_checksum(id_17: str) -> str:
    """计算校验码"""
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = "10X98765432"

    total = sum(int(id_17[i]) * weights[i] for i in range(17))
    return check_codes[total % 11]


def generate_id_card(
    province: str | None = None,
    gender: int | None = None,
    min_age: int = 18,
    max_age: int = 65,
) -> str:
    """
    生成中国身份证号

    Args:
        province: 省份名称，不指定则随机
        gender: 性别，1=男，2=女，None=随机
        min_age: 最小年龄
        max_age: 最大年龄

    Returns:
        18位身份证号
    """
    # 省份代码
    if province and province in PROVINCE_CODES:
        province_code = PROVINCE_CODES[province]
    else:
        province_code = random.choice(list(PROVINCE_CODES.values()))

    # 城市 + 区县（2位 + 2位），随机生成
    city_district = f"{random.randint(1, 99):02d}{random.randint(1, 99):02d}"

    # 出生日期
    birthday = _generate_birthday(min_age, max_age)

    # 顺序码
    sequence = _generate_sequence(gender)

    # 前17位
    id_17 = f"{province_code}{city_district}{birthday}{sequence}"

    # 校验码
    checksum = _calculate_checksum(id_17)

    return id_17 + checksum
