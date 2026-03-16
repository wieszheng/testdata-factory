"""颜色生成器"""

import random


# 常见颜色名称
COLOR_NAMES = [
    "红色", "橙色", "黄色", "绿色", "青色", "蓝色", "紫色", "粉色",
    "黑色", "白色", "灰色", "棕色", "米色", "金色", "银色",
    "深红", "深蓝", "深绿", "浅蓝", "浅绿", "浅灰", "天蓝",
    "玫红", "珊瑚色", "薄荷绿", "薰衣草紫", "海军蓝", "巧克力色",
]

# 常见十六进制颜色
COMMON_COLORS = [
    "#FF0000", "#FF6B6B", "#FFE66D", "#4ECB71", "#00D2D3",
    "#54A0FF", "#5F27CD", "#FF9FF3", "#2C3E50", "#7F8C8D",
    "#F39C12", "#E74C3C", "#1ABC9C", "#3498DB", "#9B59B6",
    "#34495E", "#16A085", "#27AE60", "#2980B9", "#8E44AD",
]


def generate_hex_color() -> str:
    """生成十六进制颜色代码"""
    return "#{:06X}".format(random.randint(0, 0xFFFFFF))


def generate_rgb() -> str:
    """生成 RGB 颜色"""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgb({r}, {g}, {b})"


def generate_rgba(alpha: float | None = None) -> str:
    """生成 RGBA 颜色"""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = alpha if alpha is not None else round(random.random(), 2)
    return f"rgba({r}, {g}, {b}, {a})"


def generate_hsl() -> str:
    """生成 HSL 颜色"""
    h = random.randint(0, 360)
    s = random.randint(50, 100)
    l = random.randint(30, 70)
    return f"hsl({h}, {s}%, {l}%)"


def generate_color_name() -> str:
    """生成颜色名称"""
    return random.choice(COLOR_NAMES)


def generate_color(format: str = "hex") -> str:
    """
    生成颜色

    Args:
        format: 格式，可选: hex, rgb, rgba, hsl, name

    Returns:
        颜色值
    """
    if format == "hex":
        return generate_hex_color()
    elif format == "rgb":
        return generate_rgb()
    elif format == "rgba":
        return generate_rgba()
    elif format == "hsl":
        return generate_hsl()
    elif format == "name":
        return generate_color_name()
    elif format == "common":
        return random.choice(COMMON_COLORS)
    else:
        return generate_hex_color()
