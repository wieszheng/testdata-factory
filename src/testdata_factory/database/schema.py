"""数据库逆向解析模块"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class ColumnInfo:
    """字段信息"""
    name: str
    data_type: str
    is_nullable: bool
    is_primary_key: bool
    is_foreign_key: bool
    foreign_key_ref: Optional[str]  # 格式: table.column
    column_default: Optional[str]
    column_comment: Optional[str]
    

@dataclass
class TableInfo:
    """表信息"""
    table_name: str
    columns: list[ColumnInfo]
    table_comment: Optional[str] = None


@dataclass
class DatabaseSchema:
    """数据库结构"""
    tables: dict[str, TableInfo]


# 数据类型到生成器的映射
TYPE_MAPPING = {
    # 字符串类型
    "varchar": "string",
    "char": "string",
    "text": "text",
    "longtext": "text",
    "mediumtext": "text",
    
    # 数字类型
    "int": "integer",
    "integer": "integer",
    "bigint": "integer",
    "smallint": "integer",
    "tinyint": "integer",
    "decimal": "decimal",
    "float": "decimal",
    "double": "decimal",
    "numeric": "decimal",
    
    # 日期时间
    "date": "date",
    "datetime": "datetime",
    "timestamp": "datetime",
    "time": "time",
    
    # 布尔
    "boolean": "boolean",
    "bool": "boolean",
    
    # JSON
    "json": "json",
    
    # 其他
    "uuid": "uuid",
    "enum": "enum",
}


def map_column_to_generator(column: ColumnInfo) -> str:
    """
    根据字段信息推断生成器类型
    
    Args:
        column: 字段信息
        
    Returns:
        生成器类型
    """
    column_name_lower = column.name.lower()
    data_type_lower = column.data_type.lower()
    
    # 根据字段名推断
    name_patterns = {
        "phone": "phone",
        "mobile": "phone",
        "tel": "phone",
        "email": "email",
        "mail": "email",
        "id_card": "id_card",
        "idcard": "id_card",
        "identity": "id_card",
        "name": "name",
        "username": "username",
        "user_name": "username",
        "password": "password",
        "pwd": "password",
        "age": "age",
        "sex": "gender",
        "gender": "gender",
        "address": "address",
        "addr": "address",
        "city": "city",
        "province": "province",
        "country": "country",
        "company": "company",
        "company_name": "company",
        "url": "url",
        "website": "url",
        "link": "url",
        "ip": "ip",
        "ip_address": "ip",
        "bank_card": "bank_card",
        "card_no": "bank_card",
        "price": "price",
        "amount": "price",
        "money": "price",
        "salary": "salary",
        "color": "color",
        "avatar": "avatar",
        "image": "image",
        "photo": "image",
        "pic": "image",
        "title": "title",
        "subject": "title",
        "description": "description",
        "content": "content",
        "remark": "text",
        "note": "text",
        "comment": "text",
        "status": "status",
        "type": "type",
        "create_time": "datetime",
        "created_at": "datetime",
        "update_time": "datetime",
        "updated_at": "datetime",
        "create_date": "date",
        "birth": "date",
        "birthday": "date",
        "date": "date",
    }
    
    for pattern, generator in name_patterns.items():
        if pattern in column_name_lower:
            return generator
    
    # 根据数据类型推断
    for type_pattern, generator in TYPE_MAPPING.items():
        if type_pattern in data_type_lower:
            return generator
    
    return "string"


def infer_generator_from_comment(column: ColumnInfo) -> Optional[str]:
    """
    从字段注释推断生成器
    
    Args:
        column: 字段信息
        
    Returns:
        生成器类型或 None
    """
    if not column.column_comment:
        return None
    
    comment_lower = column.column_comment.lower()
    
    comment_patterns = {
        "手机": "phone",
        "电话": "phone",
        "邮箱": "email",
        "身份证": "id_card",
        "姓名": "name",
        "用户名": "username",
        "密码": "password",
        "地址": "address",
        "公司": "company",
        "价格": "price",
        "金额": "price",
        "状态": "status",
        "日期": "date",
        "时间": "datetime",
    }
    
    for pattern, generator in comment_patterns.items():
        if pattern in comment_lower:
            return generator
    
    return None


def get_column_generator(column: ColumnInfo) -> str:
    """
    获取字段的生成器类型
    
    优先级：注释 > 字段名 > 数据类型
    
    Args:
        column: 字段信息
        
    Returns:
        生成器类型
    """
    # 1. 从注释推断
    generator = infer_generator_from_comment(column)
    if generator:
        return generator
    
    # 2. 从字段名推断
    generator = map_column_to_generator(column)
    if generator != "string":
        return generator
    
    # 3. 从数据类型推断
    return map_column_to_generator(column)
