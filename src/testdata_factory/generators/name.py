"""姓名生成器"""

import random
from faker import Faker

fake = Faker("zh_CN")

# 常见姓氏
SURNAMES = [
    "王", "李", "张", "刘", "陈", "杨", "黄", "赵", "吴", "周",
    "徐", "孙", "马", "朱", "胡", "郭", "何", "高", "林", "罗",
    "郑", "梁", "谢", "宋", "唐", "许", "韩", "冯", "邓", "曹",
    "彭", "曾", "萧", "田", "董", "袁", "潘", "于", "蒋", "蔡",
    "余", "杜", "叶", "程", "苏", "魏", "吕", "丁", "任", "沈"
]

# 常见名字（单字）
GIVEN_NAMES_SINGLE = [
    "伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋",
    "勇", "艳", "杰", "娟", "涛", "明", "超", "秀", "霞", "平",
    "刚", "桂", "英", "华", "建", "文", "玲", "斌", "宇", "浩"
]

# 常见名字（双字）
GIVEN_NAMES_DOUBLE = [
    "志强", "建国", "建华", "建军", "小明", "秀英", "秀兰", "秀芳",
    "美玲", "美华", "玉兰", "玉梅", "玉英", "小红", "小芳", "小燕",
    "伟强", "伟民", "国强", "国华", "国明", "志明", "志伟", "志华",
    "丽华", "丽娟", "丽萍", "丽芳", "淑珍", "淑华", "淑兰", "淑芳"
]


def generate_name(gender: int | None = None) -> str:
    """
    生成中文姓名

    Args:
        gender: 性别，1=男，2=女，None=随机

    Returns:
        姓名
    """
    # 使用 faker 生成更真实的姓名
    return fake.name()


def generate_surname() -> str:
    """生成姓氏"""
    return random.choice(SURNAMES)


def generate_given_name(single: bool | None = None) -> str:
    """
    生成名字

    Args:
        single: 是否单字名，None=随机

    Returns:
        名字
    """
    if single is None:
        single = random.random() < 0.4  # 40% 概率单字名
    
    if single:
        return random.choice(GIVEN_NAMES_SINGLE)
    return random.choice(GIVEN_NAMES_DOUBLE)
