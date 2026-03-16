"""IP 地址生成器"""

import random


def generate_ipv4() -> str:
    """生成 IPv4 地址"""
    return ".".join([str(random.randint(0, 255)) for _ in range(4)])


def generate_ipv6() -> str:
    """生成 IPv6 地址"""
    segments = [format(random.randint(0, 65535), 'x') for _ in range(8)]
    return ":".join(segments)


def generate_ip(version: int = 4) -> str:
    """
    生成 IP 地址

    Args:
        version: 4 或 6

    Returns:
        IP 地址字符串
    """
    if version == 6:
        return generate_ipv6()
    return generate_ipv4()
