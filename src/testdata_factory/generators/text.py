"""中文文本生成器"""

import random
from faker import Faker

fake = Faker("zh_CN")

# 常用中文句子
COMMON_SENTENCES = [
    "这是一段测试文本。",
    "系统正常运行中。",
    "数据已成功保存。",
    "操作完成。",
    "请稍后再试。",
    "欢迎使用本系统。",
    "功能正在开发中。",
    "如有疑问请联系客服。",
    "感谢您的使用。",
    "已为您处理完成。",
]


def generate_sentence() -> str:
    """生成中文句子"""
    return fake.sentence()


def generate_paragraph(sentences: int = 3) -> str:
    """
    生成中文段落

    Args:
        sentences: 句子数量

    Returns:
        段落文本
    """
    return fake.paragraph(nb_sentences=sentences)


def generate_text(max_chars: int = 100) -> str:
    """
    生成指定长度的中文文本

    Args:
        max_chars: 最大字符数

    Returns:
        文本
    """
    return fake.text(max_nb_chars=max_chars)


def generate_word() -> str:
    """生成中文词语"""
    return fake.word()


def generate_title() -> str:
    """生成标题"""
    return fake.sentence(nb_words=random.randint(4, 10))


def generate_lorem() -> str:
    """生成乱数假文"""
    return fake.paragraph(nb_sentences=5)


def generate_common_sentence() -> str:
    """生成常用中文句子"""
    return random.choice(COMMON_SENTENCES)


def generate_description() -> str:
    """生成描述文本"""
    templates = [
        f"这是一个关于{fake.word()}的项目，主要功能包括{fake.word()}和{fake.word()}。",
        f"该系统支持{fake.word()}功能，适用于{fake.word()}场景。",
        f"用户可以通过{fake.word()}方式完成{fake.word()}操作。",
        f"本产品专注于{fake.word()}领域，提供{fake.word()}解决方案。",
    ]
    return random.choice(templates)
