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
from ..generators.regex import generate_from_regex, list_templates

router = APIRouter()


# ===== 数据类型映射 =====

DATA_TYPE_GENERATORS = {
    "phone": lambda: generate_phone(),
    "email": lambda: generate_email(),
    "id_card": lambda: generate_id_card(),
    "ip": lambda: generate_ip(4),
    "ipv6": lambda: generate_ip(6),
    "address": lambda: generate_address(),
    "date": lambda: generate_date(),
    "datetime": lambda: generate_datetime(),
    "bank_card": lambda: generate_bank_card(),
    "name": lambda: generate_name(),
    "url": lambda: generate_url(),
}

DATA_TYPE_LABELS = {
    "phone": "手机号",
    "email": "邮箱",
    "id_card": "身份证号",
    "ip": "IP地址",
    "ipv6": "IPv6地址",
    "address": "地址",
    "date": "日期",
    "datetime": "日期时间",
    "bank_card": "银行卡号",
    "name": "姓名",
    "url": "URL",
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
    """
    生成混合数据
    
    - **count**: 生成数量 (1-1000)
    - **types**: 数据类型列表
    """
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
    """
    根据正则表达式生成数据
    
    支持的格式：
    - \d: 数字
    - \w: 字母数字下划线
    - \a: 小写字母
    - \A: 大写字母
    - [abc], [a-z]: 字符类
    - {n}, {n,m}: 重复次数
    - *, +, ?: 量词
    - .: 任意字符
    - 普通字符: 原样输出
    
    示例：
    - 手机号: 1[3-9]\d{9}
    - 邮箱: [a-z]{3,8}\d{2,4}@(qq|163|126)\.com
    - 订单号: ORD\d{14}
    """
    try:
        results = [generate_from_regex(request.pattern) for _ in range(request.count)]
        return RegexGenerateResponse(
            success=True,
            count=len(results),
            pattern=request.pattern,
            data=results
        )
    except Exception as e:
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


@router.post("/phone")
async def generate_phones(count: int = Query(default=10, ge=1, le=1000)):
    """生成手机号"""
    phones = [generate_phone() for _ in range(count)]
    return {"success": True, "count": len(phones), "data": phones}


@router.post("/email")
async def generate_emails(count: int = Query(default=10, ge=1, le=1000)):
    """生成邮箱"""
    emails = [generate_email() for _ in range(count)]
    return {"success": True, "count": len(emails), "data": emails}


@router.post("/idcard")
async def generate_idcards(count: int = Query(default=10, ge=1, le=1000)):
    """生成身份证号"""
    id_cards = [generate_id_card() for _ in range(count)]
    return {"success": True, "count": len(id_cards), "data": id_cards}


@router.post("/ip")
async def generate_ips(count: int = Query(default=10, ge=1, le=1000), version: int = Query(default=4, ge=4, le=6)):
    """生成 IP 地址"""
    ips = [generate_ip(version) for _ in range(count)]
    return {"success": True, "count": len(ips), "data": ips}


@router.post("/address")
async def generate_addresses(count: int = Query(default=10, ge=1, le=1000)):
    """生成地址"""
    addresses = [generate_address() for _ in range(count)]
    return {"success": True, "count": len(addresses), "data": addresses}


@router.post("/bankcard")
async def generate_bankcards(count: int = Query(default=10, ge=1, le=1000)):
    """生成银行卡号"""
    cards = [generate_bank_card() for _ in range(count)]
    return {"success": True, "count": len(cards), "data": cards}


@router.post("/name")
async def generate_names(count: int = Query(default=10, ge=1, le=1000)):
    """生成姓名"""
    names = [generate_name() for _ in range(count)]
    return {"success": True, "count": len(names), "data": names}


@router.post("/url")
async def generate_urls(count: int = Query(default=10, ge=1, le=1000)):
    """生成 URL"""
    urls = [generate_url() for _ in range(count)]
    return {"success": True, "count": len(urls), "data": urls}


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
