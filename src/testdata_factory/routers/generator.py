"""API 路由"""

import sys
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from ..generators.phone import generate_phone
from ..generators.email import generate_email
from ..generators.id_card import generate_id_card
from ..generators.ip import generate_ip
from ..generators.address import generate_address
from ..generators.date import generate_date, generate_datetime
from ..generators.bank_card import generate_bank_card
from ..generators.name import generate_name
from ..generators.url import generate_url
from ..generators.company import generate_company
from ..generators.position import generate_position
from ..generators.money import generate_price, generate_salary
from ..generators.color import generate_color
from ..generators.uuid import generate_uuid, generate_order_id, generate_serial_number
from ..generators.credential import generate_username, generate_password
from ..generators.text import generate_sentence, generate_paragraph
from ..generators.regex import generate_from_regex, list_templates
from ..validators import BUILTIN_VALIDATORS, validate_field, SUPPORTED_VALIDATORS
from ..dedup import get_dedup_manager, reset_dedup

router = APIRouter()


# ===== 数据类型映射 =====

DATA_TYPE_GENERATORS = {
    # 基础类型
    "phone": lambda: generate_phone(),
    "email": lambda: generate_email(),
    "id_card": lambda: generate_id_card(),
    "ip": lambda: generate_ip(4),
    "address": lambda: generate_address(),
    "date": lambda: generate_date(),
    "datetime": lambda: generate_datetime(),
    "bank_card": lambda: generate_bank_card(),
    "name": lambda: generate_name(),
    "url": lambda: generate_url(),
    # 新增类型
    "company": lambda: generate_company(),
    "position": lambda: generate_position(),
    "price": lambda: generate_price(),
    "color": lambda: generate_color(),
    "uuid": lambda: generate_uuid(),
    "username": lambda: generate_username(),
    "password": lambda: generate_password(),
    "sentence": lambda: generate_sentence(),
}

DATA_TYPE_LABELS = {
    # 基础类型
    "phone": "手机号",
    "email": "邮箱",
    "id_card": "身份证号",
    "ip": "IP地址",
    "address": "地址",
    "date": "日期",
    "datetime": "日期时间",
    "bank_card": "银行卡号",
    "name": "姓名",
    "url": "URL",
    # 新增类型
    "company": "公司名",
    "position": "职位",
    "price": "价格",
    "color": "颜色",
    "uuid": "UUID",
    "username": "用户名",
    "password": "密码",
    "sentence": "句子",
}


# ===== 请求/响应模型 =====

class GenerateRequest(BaseModel):
    """生成请求"""
    count: int = Field(default=10, ge=1, le=1000, description="生成数量")
    types: list[str] = Field(
        default=["phone", "email", "id_card"],
        description="要生成的数据类型"
    )
    # 新增：自定义正则规则
    custom_rules: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="自定义正则规则列表，每项包含 name 和 pattern"
    )
    # 新增：校验和去重配置
    validate: bool = Field(
        default=True,
        description="是否启用内置校验（生成时保证格式正确）"
    )
    dedup: bool = Field(
        default=False,
        description="是否启用去重（同一批次内去重）"
    )


class RegexGenerateRequest(BaseModel):
    """正则生成请求"""
    count: int = Field(default=10, ge=1, le=1000, description="生成数量")
    pattern: str = Field(..., description="正则表达式模式")
    name: Optional[str] = Field(default=None, description="字段名称")


class GenerateResponse(BaseModel):
    """生成响应"""
    success: bool = True
    count: int
    types: list[str]
    data: list[dict]
    validation: Optional[Dict[str, Any]] = Field(
        default=None,
        description="校验结果统计"
    )
    dedup_info: Optional[Dict[str, int]] = Field(
        default=None,
        description="去重统计"
    )


class RegexGenerateResponse(BaseModel):
    """正则生成响应"""
    success: bool = True
    count: int
    pattern: str
    data: list[str]


# ===== API 端点 =====

@router.post("/generate", response_model=GenerateResponse)
async def generate_data(request: GenerateRequest):
    """生成混合数据"""
    valid_types = [t for t in request.types if t in DATA_TYPE_GENERATORS]
    
    # 处理自定义正则规则
    custom_fields = []
    if request.custom_rules:
        for rule in request.custom_rules:
            if rule.get("name") and rule.get("pattern"):
                custom_fields.append({
                    "name": rule["name"],
                    "pattern": rule["pattern"]
                })
    
    if not valid_types and not custom_fields:
        valid_types = ["phone", "email", "id_card"]
    
    # 去重管理器
    dedup_mgr = get_dedup_manager()
    if request.dedup:
        dedup_mgr.clear()  # 开始新批次前清空
    
    data = []
    dedup_stats = {t: 0 for t in valid_types}
    validation_stats = {t: {"passed": 0, "failed": 0} for t in valid_types}
    
    max_attempts = request.count * 10  # 防止无限循环
    attempts = 0
    
    while len(data) < request.count and attempts < max_attempts:
        attempts += 1
        item = {}
        skip_item = False
        
        # 生成内置类型数据
        for data_type in valid_types:
            value = DATA_TYPE_GENERATORS[data_type]()
            
            # 校验
            if request.validate:
                is_valid = validate_field(value, data_type)
                if is_valid:
                    validation_stats[data_type]["passed"] += 1
                else:
                    validation_stats[data_type]["failed"] += 1
                    continue  # 跳过无效数据
            
            # 去重
            if request.dedup:
                if not dedup_mgr.add(data_type, value):
                    dedup_stats[data_type] += 1
                    continue  # 跳过重复数据
            
            item[data_type] = value
        
        # 生成自定义正则数据
        for field in custom_fields:
            try:
                item[field["name"]] = generate_from_regex(field["pattern"])
            except:
                item[field["name"]] = ""
        
        if item and len(item) == len(valid_types) + len(custom_fields):
            data.append(item)
    
    # 合并所有字段名
    all_types = valid_types + [f["name"] for f in custom_fields]
    
    # 构建响应
    response_data = {
        "count": len(data),
        "types": all_types,
        "data": data
    }
    
    # 添加校验结果（仅在启用时）
    if request.validate:
        response_data["validation"] = validation_stats
    
    # 添加去重统计（仅在启用时）
    if request.dedup:
        response_data["dedup_info"] = {
            "duplicates_removed": sum(dedup_stats.values()),
            "by_type": dedup_stats
        }
    
    return GenerateResponse(**response_data)


@router.post("/regex", response_model=RegexGenerateResponse)
async def generate_from_regex_pattern(request: RegexGenerateRequest):
    """根据正则表达式生成数据"""
    try:
        results = [generate_from_regex(request.pattern) for _ in range(request.count)]
        return RegexGenerateResponse(
            success=True,
            count=len(results),
            pattern=request.pattern,
            data=results
        )
    except Exception:
        return RegexGenerateResponse(
            success=False,
            count=0,
            pattern=request.pattern,
            data=[]
        )


@router.get("/templates")
async def get_regex_templates():
    """获取预定义的正则模板"""
    templates = list_templates()
    return {
        "templates": [
            {"name": name, "pattern": pattern}
            for name, pattern in templates.items()
        ]
    }


@router.get("/types")
async def get_data_types():
    """获取支持的数据类型"""
    return {
        "types": [
            {"key": key, "label": label}
            for key, label in DATA_TYPE_LABELS.items()
        ]
    }


@router.get("/validators")
async def get_validators():
    """获取支持的校验规则"""
    return {
        "validators": SUPPORTED_VALIDATORS,
        "count": len(SUPPORTED_VALIDATORS)
    }


@router.post("/dedup/reset")
async def reset_dedup_manager():
    """重置去重管理器"""
    reset_dedup()
    return {"success": True, "message": "去重记录已清空"}


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
