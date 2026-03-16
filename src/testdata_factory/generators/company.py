"""公司名生成器"""

import random

# 公司前缀
COMPANY_PREFIXES = [
    "华为", "阿里", "腾讯", "百度", "字节", "美团", "京东", "小米", "网易", "滴滴",
    "快手", "拼多多", "哔哩", "知乎", "携程", "新浪", "搜狐", "360", "58", "美团",
    "顺丰", "海尔", "格力", "美的", "比亚迪", "蔚来", "理想", "小鹏", "大疆",
    "金蝶", "用友", "东软", "中软", "浪潮", "曙光", "神州", "中兴", "大唐",
]

# 公司类型
COMPANY_TYPES = [
    "科技有限公司", "网络技术有限公司", "信息技术有限公司", "软件开发有限公司",
    "互联网有限公司", "数据服务有限公司", "智能科技有限公司", "电子科技有限公司",
    "通信技术有限公司", "云计算有限公司", "人工智能有限公司", "物联网有限公司",
    "大数据有限公司", "数字技术有限公司", "创新科技有限公司", "互联网科技有限公司",
]

# 英文公司名
EN_COMPANY_NAMES = [
    "Tech", "Digital", "Cloud", "Data", "Smart", "AI", "Cyber", "Net", "Web", "Soft",
    "Info", "System", "Solution", "Service", "Lab", "Studio", "Works", "Group", "Inc",
]


def generate_company_cn() -> str:
    """生成中文公司名"""
    prefix = random.choice(COMPANY_PREFIXES)
    suffix = random.choice(COMPANY_TYPES)
    
    # 50% 概率加地区
    if random.random() < 0.5:
        regions = ["北京", "上海", "深圳", "杭州", "广州", "成都", "南京", "武汉", "西安", "苏州"]
        region = random.choice(regions)
        return f"{region}{prefix}{suffix}"
    
    return f"{prefix}{suffix}"


def generate_company_en() -> str:
    """生成英文公司名"""
    name = random.choice(EN_COMPANY_NAMES)
    suffix = random.choice(["Inc.", "Ltd.", "Co.", "Corp.", "LLC"])
    
    if random.random() < 0.5:
        prefix = random.choice(EN_COMPANY_NAMES)
        return f"{prefix}{name} {suffix}"
    
    return f"{name} {suffix}"


def generate_company() -> str:
    """生成公司名（随机中英文）"""
    if random.random() < 0.7:
        return generate_company_cn()
    return generate_company_en()
