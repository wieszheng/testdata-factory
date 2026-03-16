"""银行卡号生成器"""

import random

# 银行卡号前缀（部分常见银行）
BANK_PREFIXES = {
    "工商银行": ["622202", "622203", "622208"],
    "农业银行": ["622848", "622849"],
    "中国银行": ["621660", "621661", "621663"],
    "建设银行": ["622700", "622280"],
    "交通银行": ["622260", "622261"],
    "招商银行": ["622580", "622588"],
    "浦发银行": ["622260", "622262"],
    "民生银行": ["622615", "622617"],
    "兴业银行": ["622909", "622910"],
    "平安银行": ["622155", "622156"],
}


def _luhn_checksum(card_number: str) -> int:
    """Luhn 算法计算校验位"""
    digits = [int(d) for d in card_number]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    
    total = sum(odd_digits)
    for d in even_digits:
        doubled = d * 2
        total += doubled - 9 if doubled > 9 else doubled
    
    return (10 - total % 10) % 10


def generate_bank_card(bank: str | None = None) -> str:
    """
    生成银行卡号

    Args:
        bank: 指定银行名称，不指定则随机

    Returns:
        16 位银行卡号
    """
    if bank is None or bank not in BANK_PREFIXES:
        bank = random.choice(list(BANK_PREFIXES.keys()))
    
    prefix = random.choice(BANK_PREFIXES[bank])
    
    # 生成剩余位数（总共 16 位，前缀后还需要生成，最后一位是校验位）
    remaining_length = 15 - len(prefix)
    remaining = "".join([str(random.randint(0, 9)) for _ in range(remaining_length)])
    
    # 计算校验位
    card_without_check = prefix + remaining
    check_digit = _luhn_checksum(card_without_check)
    
    return card_without_check + str(check_digit)


def get_bank_name(card_number: str) -> str | None:
    """
    根据卡号判断银行

    Args:
        card_number: 银行卡号

    Returns:
        银行名称
    """
    for bank, prefixes in BANK_PREFIXES.items():
        for prefix in prefixes:
            if card_number.startswith(prefix):
                return bank
    return None
