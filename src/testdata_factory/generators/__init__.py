"""数据生成器"""

from .phone import generate_phone
from .email import generate_email
from .id_card import generate_id_card

__all__ = ["generate_phone", "generate_email", "generate_id_card"]
