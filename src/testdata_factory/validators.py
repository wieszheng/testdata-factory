"""内置校验规则"""

import re
from typing import Callable


def validate_phone(phone: str) -> bool:
    """校验手机号：11位，以1开头"""
    return bool(re.match(r'^1[3-9]\d{9}$', phone))


def validate_id_card(id_card: str) -> bool:
    """校验身份证：18位，最后一位可能是X"""
    return bool(re.match(r'^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$', id_card))


def validate_email(email: str) -> bool:
    """校验邮箱：包含@和."""
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validate_date(date_str: str) -> bool:
    """校验日期：YYYY-MM-DD 格式"""
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_str))


def validate_time(time_str: str) -> bool:
    """校验时间：HH:MM:SS 格式"""
    return bool(re.match(r'^\d{2}:\d{2}:\d{2}$', time_str))


def validate_url(url: str) -> bool:
    """校验URL：http/https开头"""
    return bool(re.match(r'^https?://', url))


def validate_ip(ip: str) -> bool:
    """校验IP地址：IPv4格式"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except (ValueError, TypeError):
        return False


def validate_bank_card(card: str) -> bool:
    """校验银行卡号：16-19位数字"""
    return bool(re.match(r'^\d{16,19}$', card))


def validate_postcode(code: str) -> bool:
    """校验邮政编码：6位数字"""
    return bool(re.match(r'^\d{6}$', code))


def validate_uuid(uuid_str: str) -> bool:
    """校验UUID：标准格式"""
    return bool(re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', uuid_str, re.I))


def validate_chinese_name(name: str) -> bool:
    """校验中文姓名：2-10位中文"""
    return bool(re.match(r'^[\u4e00-\u9fa5]{2,10}$', name))


def validate_credit_card(card: str) -> bool:
    """校验信用卡号（Luhn算法）"""
    if not re.match(r'^\d{13,19}$', card):
        return False
    
    # Luhn算法
    digits = [int(d) for d in card]
    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


# 内置校验规则映射
BUILTIN_VALIDATORS: dict[str, Callable[[str], bool]] = {
    'phone': validate_phone,
    'id_card': validate_id_card,
    'idcard': validate_id_card,
    'email': validate_email,
    'date': validate_date,
    'time': validate_time,
    'url': validate_url,
    'ip': validate_ip,
    'ipv4': validate_ip,
    'bank_card': validate_bank_card,
    'bankcard': validate_bank_card,
    'postcode': validate_postcode,
    'uuid': validate_uuid,
    'chinese_name': validate_chinese_name,
    'credit_card': validate_credit_card,
}


def get_validator(name: str) -> Callable[[str], bool] | None:
    """获取校验器"""
    return BUILTIN_VALIDATORS.get(name.lower())


def validate_field(value: str, field_type: str) -> bool:
    """校验字段"""
    validator = get_validator(field_type)
    if validator:
        return validator(value)
    return True  # 未知类型默认通过


# 支持的校验规则列表
SUPPORTED_VALIDATORS = list(BUILTIN_VALIDATORS.keys())
