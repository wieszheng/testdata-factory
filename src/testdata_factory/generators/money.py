"""金额/价格生成器"""

import random
from decimal import Decimal


def generate_amount(
    min_value: float = 0.01,
    max_value: float = 100000,
    decimal_places: int = 2,
) -> float:
    """
    生成金额

    Args:
        min_value: 最小值
        max_value: 最大值
        decimal_places: 小数位数

    Returns:
        金额
    """
    value = random.uniform(min_value, max_value)
    return round(value, decimal_places)


def generate_price(
    min_price: float = 1,
    max_price: float = 10000,
) -> str:
    """
    生成价格（带货币符号）

    Args:
        min_price: 最低价格
        max_price: 最低价格

    Returns:
        价格字符串，如 ¥99.00
    """
    price = random.uniform(min_price, max_price)
    
    # 常见定价策略：.00, .90, .99
    endings = [0, 0.9, 0.99, 0.5, 0.8]
    ending = random.choice(endings)
    
    final_price = int(price) + ending
    
    # 随机货币符号
    symbols = ["¥", "$", "€", "₽", "£"]
    symbol = random.choice(symbols)
    
    return f"{symbol}{final_price:.2f}"


def generate_salary(
    min_k: int = 5,
    max_k: int = 100,
) -> str:
    """
    生成薪资范围

    Args:
        min_k: 最低 K
        max_k: 最高 K

    Returns:
        薪资范围，如 15K-25K
    """
    low = random.randint(min_k, max_k - 5)
    high = random.randint(low + 3, max_k)
    
    # 14薪、15薪、16薪
    months = random.choice([12, 13, 14, 15, 16])
    
    return f"{low}K-{high}K · {months}薪"


def generate_bank_amount(
    min_value: float = 100,
    max_value: float = 1000000,
) -> str:
    """
    生成银行金额（千分位格式）

    Args:
        min_value: 最小值
        max_value: 最大值

    Returns:
        格式化金额，如 1,234,567.89
    """
    value = random.uniform(min_value, max_value)
    return f"{value:,.2f}"
