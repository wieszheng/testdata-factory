"""API 路由"""

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional

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
    
    if not valid_types:
        valid_types = ["phone", "email", "id_card"]
    
    data = []
    
    for _ in range(request.count):
        item = {}
        for data_type in valid_types:
            item[data_type] = DATA_TYPE_GENERATORS[data_type]()
        data.append(item)
    
    return GenerateResponse(
        count=len(data),
        types=valid_types,
        data=data
    )


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


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
