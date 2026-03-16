"""数据生成器"""

from .phone import generate_phone
from .email import generate_email
from .id_card import generate_id_card
from .ip import generate_ip, generate_ipv4, generate_ipv6
from .address import generate_address, generate_province, generate_city
from .date import generate_date, generate_datetime, generate_timestamp
from .bank_card import generate_bank_card
from .name import generate_name, generate_surname, generate_given_name
from .url import generate_url, generate_domain
from .company import generate_company, generate_company_cn, generate_company_en
from .position import generate_position, generate_job_title
from .money import generate_amount, generate_price, generate_salary
from .color import generate_color, generate_hex_color, generate_rgb
from .uuid import generate_uuid, generate_id, generate_order_id, generate_serial_number
from .credential import generate_username, generate_password
from .text import generate_sentence, generate_paragraph, generate_text

__all__ = [
    # 基础数据
    "generate_phone",
    "generate_email", 
    "generate_id_card",
    "generate_ip",
    "generate_ipv4",
    "generate_ipv6",
    "generate_address",
    "generate_province",
    "generate_city",
    "generate_date",
    "generate_datetime",
    "generate_timestamp",
    "generate_bank_card",
    "generate_name",
    "generate_surname",
    "generate_given_name",
    "generate_url",
    "generate_domain",
    # 新增数据类型
    "generate_company",
    "generate_company_cn",
    "generate_company_en",
    "generate_position",
    "generate_job_title",
    "generate_amount",
    "generate_price",
    "generate_salary",
    "generate_color",
    "generate_hex_color",
    "generate_rgb",
    "generate_uuid",
    "generate_id",
    "generate_order_id",
    "generate_serial_number",
    "generate_username",
    "generate_password",
    "generate_sentence",
    "generate_paragraph",
    "generate_text",
]
