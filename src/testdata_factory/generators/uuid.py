"""UUID 和唯一标识生成器"""

import uuid
import random
import string
import time


def generate_uuid(version: int = 4) -> str:
    """
    生成 UUID

    Args:
        version: UUID 版本，1 或 4

    Returns:
        UUID 字符串
    """
    if version == 1:
        return str(uuid.uuid1())
    return str(uuid.uuid4())


def generate_uuid_short() -> str:
    """生成短 UUID（无连字符）"""
    return uuid.uuid4().hex


def generate_id(prefix: str = "") -> str:
    """
    生成带前缀的 ID

    Args:
        prefix: 前缀

    Returns:
        ID 字符串
    """
    return f"{prefix}{uuid.uuid4().hex[:12].upper()}"


def generate_snowflake_id() -> str:
    """
    生成雪花 ID（简化版）

    Returns:
        数字 ID
    """
    timestamp = int(time.time() * 1000)
    random_part = random.randint(0, 4095)
    return f"{timestamp}{random_part:04d}"


def generate_order_id(prefix: str = "ORD") -> str:
    """生成订单号"""
    timestamp = time.strftime("%Y%m%d%H%M%S")
    random_part = ''.join(random.choices(string.digits, k=6))
    return f"{prefix}{timestamp}{random_part}"


def generate_serial_number(length: int = 12) -> str:
    """
    生成序列号

    Args:
        length: 长度

    Returns:
        序列号
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_trace_id() -> str:
    """生成链路追踪 ID"""
    return uuid.uuid4().hex[:32]
