"""邮箱生成器"""

import random
from faker import Faker

fake = Faker("zh_CN")
fake_en = Faker("en_US")

# 常见邮箱域名
EMAIL_DOMAINS = [
    "qq.com",
    "163.com",
    "126.com",
    "gmail.com",
    "outlook.com",
    "sina.com",
    "sohu.com",
    "foxmail.com",
]


def generate_email(domain: str | None = None) -> str:
    """
    生成邮箱地址

    Args:
        domain: 指定域名，不指定则随机选择

    Returns:
        邮箱地址
    """
    if domain is None:
        domain = random.choice(EMAIL_DOMAINS)

    # 生成用户名：使用英文名字 + 随机数字，避免中文
    name = f"{fake_en.last_name().lower()}{fake_en.first_name().lower()}".replace(" ", "")
    num = random.randint(1, 9999)

    return f"{name}{num}@{domain}"
