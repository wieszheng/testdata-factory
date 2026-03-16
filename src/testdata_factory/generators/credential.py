"""用户名和密码生成器"""

import random
import string
from faker import Faker

fake = Faker("zh_CN")

# 用户名前缀
USERNAME_PREFIXES = ["user", "admin", "test", "demo", "member", "guest"]

# 密码特殊字符
PASSWORD_SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"


def generate_username(style: str = "random") -> str:
    """
    生成用户名

    Args:
        style: 风格，可选: random, email_style, prefix_num, pinyin

    Returns:
        用户名
    """
    if style == "email_style":
        name = fake.name_ascii().replace(" ", ".").lower()
        num = random.randint(1, 999)
        return f"{name}{num}"
    
    elif style == "prefix_num":
        prefix = random.choice(USERNAME_PREFIXES)
        num = random.randint(1000, 99999)
        return f"{prefix}{num}"
    
    elif style == "pinyin":
        name = fake.name_ascii().replace(" ", "").lower()
        return name
    
    else:
        # 随机风格
        styles = ["email_style", "prefix_num", "pinyin"]
        return generate_username(random.choice(styles))


def generate_password(
    length: int = 12,
    include_upper: bool = True,
    include_lower: bool = True,
    include_digit: bool = True,
    include_special: bool = True,
) -> str:
    """
    生成密码

    Args:
        length: 长度
        include_upper: 包含大写字母
        include_lower: 包含小写字母
        include_digit: 包含数字
        include_special: 包含特殊字符

    Returns:
        密码
    """
    chars = ""
    
    if include_upper:
        chars += string.ascii_uppercase
    if include_lower:
        chars += string.ascii_lowercase
    if include_digit:
        chars += string.digits
    if include_special:
        chars += PASSWORD_SPECIAL_CHARS
    
    if not chars:
        chars = string.ascii_letters + string.digits
    
    # 确保包含各种字符类型
    password = []
    
    if include_upper:
        password.append(random.choice(string.ascii_uppercase))
    if include_lower:
        password.append(random.choice(string.ascii_lowercase))
    if include_digit:
        password.append(random.choice(string.digits))
    if include_special:
        password.append(random.choice(PASSWORD_SPECIAL_CHARS))
    
    # 填充剩余长度
    remaining_length = length - len(password)
    password.extend(random.choices(chars, k=remaining_length))
    
    # 打乱顺序
    random.shuffle(password)
    
    return ''.join(password)


def generate_simple_password() -> str:
    """生成简单密码（6-8位纯数字或字母）"""
    length = random.randint(6, 8)
    
    if random.random() < 0.5:
        # 纯数字
        return ''.join(random.choices(string.digits, k=length))
    else:
        # 字母数字混合
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
