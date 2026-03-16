"""手机号生成器"""

import random

# 中国移动号段
CHINA_MOBILE_PREFIXES = [
    "134", "135", "136", "137", "138", "139", "150", "151", "152", "157", "158", "159",
    "182", "183", "184", "187", "188", "178", "147", "172", "198"
]

# 中国联通号段
CHINA_UNICOM_PREFIXES = [
    "130", "131", "132", "155", "156", "185", "186", "145", "176", "175", "166", "196"
]

# 中国电信号段
CHINA_TELECOM_PREFIXES = [
    "133", "153", "180", "181", "189", "177", "173", "199", "191"
]

ALL_PREFIXES = CHINA_MOBILE_PREFIXES + CHINA_UNICOM_PREFIXES + CHINA_TELECOM_PREFIXES


def generate_phone(prefix: str | None = None) -> str:
    """
    生成中国手机号

    Args:
        prefix: 指定号段，不指定则随机选择

    Returns:
        11位手机号
    """
    if prefix is None:
        prefix = random.choice(ALL_PREFIXES)

    # 生成剩余8位数字
    suffix = "".join([str(random.randint(0, 9)) for _ in range(11 - len(prefix))])

    return prefix + suffix
