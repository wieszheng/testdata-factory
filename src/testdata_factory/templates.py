"""行业数据模板"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class IndustryTemplate:
    """行业模板"""
    name: str  # 模板名称
    description: str  # 描述
    fields: list[dict]  # 字段列表，每项包含 name 和 type


# 8个行业模板
INDUSTRY_TEMPLATES: dict[str, IndustryTemplate] = {
    "user_profile": IndustryTemplate(
        name="用户资料",
        description="用户注册信息",
        fields=[
            {"name": "user_id", "type": "uuid"},
            {"name": "username", "type": "username"},
            {"name": "password", "type": "password"},
            {"name": "email", "type": "email"},
            {"name": "phone", "type": "phone"},
            {"name": "real_name", "type": "name"},
            {"name": "id_card", "type": "id_card"},
            {"name": "address", "type": "address"},
            {"name": "register_time", "type": "datetime"},
        ]
    ),
    "order": IndustryTemplate(
        name="订单信息",
        description="电商订单数据",
        fields=[
            {"name": "order_id", "type": "order_id"},
            {"name": "user_id", "type": "uuid"},
            {"name": "product_name", "type": "sentence"},
            {"name": "product_price", "type": "price"},
            {"name": "quantity", "type": "integer"},
            {"name": "total_amount", "type": "price"},
            {"name": "order_status", "type": "status"},
            {"name": "create_time", "type": "datetime"},
            {"name": "pay_time", "type": "datetime"},
        ]
    ),
    "product": IndustryTemplate(
        name="商品信息",
        description="商品基础数据",
        fields=[
            {"name": "product_id", "type": "uuid"},
            {"name": "product_name", "type": "sentence"},
            {"name": "category", "type": "category"},
            {"name": "brand", "type": "company"},
            {"name": "price", "type": "price"},
            {"name": "stock", "type": "integer"},
            {"name": "color", "type": "color"},
            {"name": "url", "type": "url"},
        ]
    ),
    "employee": IndustryTemplate(
        name="员工信息",
        description="企业员工档案",
        fields=[
            {"name": "employee_id", "type": "uuid"},
            {"name": "name", "type": "name"},
            {"name": "gender", "type": "gender"},
            {"name": "phone", "type": "phone"},
            {"name": "email", "type": "email"},
            {"name": "department", "type": "department"},
            {"name": "position", "type": "position"},
            {"name": "salary", "type": "salary"},
            {"name": "hire_date", "type": "date"},
        ]
    ),
    "finance": IndustryTemplate(
        name="财务数据",
        description="财务报表数据",
        fields=[
            {"name": "transaction_id", "type": "uuid"},
            {"name": "amount", "type": "price"},
            {"name": "currency", "type": "currency"},
            {"name": "transaction_type", "type": "transaction_type"},
            {"name": "account", "type": "bank_card"},
            {"name": "create_time", "type": "datetime"},
            {"name": "status", "type": "status"},
        ]
    ),
    "logistics": IndustryTemplate(
        name="物流信息",
        description="快递物流数据",
        fields=[
            {"name": "tracking_no", "type": "tracking_no"},
            {"name": "order_id", "type": "order_id"},
            {"name": "sender_name", "type": "name"},
            {"name": "sender_phone", "type": "phone"},
            {"name": "sender_address", "type": "address"},
            {"name": "receiver_name", "type": "name"},
            {"name": "receiver_phone", "type": "phone"},
            {"name": "receiver_address", "type": "address"},
            {"name": "status", "type": "logistics_status"},
            {"name": "update_time", "type": "datetime"},
        ]
    ),
    "article": IndustryTemplate(
        name="文章内容",
        description="文章/帖子数据",
        fields=[
            {"name": "article_id", "type": "uuid"},
            {"name": "title", "type": "sentence"},
            {"name": "author", "type": "name"},
            {"name": "content", "type": "paragraph"},
            {"name": "category", "type": "category"},
            {"name": "tags", "type": "tags"},
            {"name": "views", "type": "integer"},
            {"name": "likes", "type": "integer"},
            {"name": "create_time", "type": "datetime"},
        ]
    ),
    "hotel": IndustryTemplate(
        name="酒店预订",
        description="酒店房间数据",
        fields=[
            {"name": "hotel_id", "type": "uuid"},
            {"name": "hotel_name", "type": "company"},
            {"name": "room_type", "type": "room_type"},
            {"name": "price", "type": "price"},
            {"name": "capacity", "type": "integer"},
            {"name": "address", "type": "address"},
            {"name": "phone", "type": "phone"},
            {"name": "rating", "type": "rating"},
        ]
    ),
}


def get_template(name: str) -> IndustryTemplate | None:
    """获取模板"""
    return INDUSTRY_TEMPLATES.get(name)


def list_templates() -> dict:
    """列出所有模板"""
    return {
        name: {
            "name": template.name,
            "description": template.description,
            "field_count": len(template.fields),
            "fields": [f["name"] for f in template.fields]
        }
        for name, template in INDUSTRY_TEMPLATES.items()
    }


def get_template_fields(name: str) -> list[dict] | None:
    """获取模板字段"""
    template = get_template(name)
    return template.fields if template else None
