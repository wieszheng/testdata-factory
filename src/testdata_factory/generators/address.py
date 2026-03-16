"""地址生成器"""

import random
from faker import Faker

fake = Faker("zh_CN")

# 省份和城市映射
PROVINCES = [
    "北京市", "上海市", "天津市", "重庆市",
    "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省",
    "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省",
    "河南省", "湖北省", "湖南省", "广东省", "海南省",
    "四川省", "贵州省", "云南省", "陕西省", "甘肃省", "青海省",
    "台湾省", "内蒙古自治区", "广西壮族自治区", "西藏自治区",
    "宁夏回族自治区", "新疆维吾尔自治区", "香港特别行政区", "澳门特别行政区"
]

STREET_NAMES = [
    "中山路", "人民路", "建设路", "解放路", "和平路",
    "幸福路", "胜利路", "长江路", "黄河路", "文化路",
    "科技路", "创新路", "发展路", "朝阳路", "复兴路",
    "东风路", "新华路", "光明路", "友谊路", "团结路"
]


def generate_address() -> str:
    """
    生成中国地址

    Returns:
        完整地址字符串
    """
    province = random.choice(PROVINCES)
    
    # 区县
    district = fake.district()[:2] + "区"
    
    # 街道
    street = random.choice(STREET_NAMES)
    street_num = random.randint(1, 999)
    
    # 楼栋门牌
    building = random.randint(1, 50)
    room = random.randint(101, 2599)
    
    return f"{province}{district}{street}{street_num}号{building}栋{room}室"


def generate_province() -> str:
    """生成省份"""
    return random.choice(PROVINCES)


def generate_city() -> str:
    """生成城市"""
    return fake.city()
