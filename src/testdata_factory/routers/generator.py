"""API 路由"""

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional

from ..generators.phone import generate_phone
from ..generators.email import generate_email
from ..generators.id_card import generate_id_card

router = APIRouter()


# ===== 请求/响应模型 =====

class GenerateRequest(BaseModel):
    """生成请求"""
    count: int = Field(default=10, ge=1, le=1000, description="生成数量")
    types: list[str] = Field(
        default=["phone", "email", "id_card"],
        description="要生成的数据类型"
    )


class PhoneRequest(BaseModel):
    """手机号生成请求"""
    count: int = Field(default=10, ge=1, le=1000)
    prefix: Optional[str] = Field(default=None, description="指定号段")


class EmailRequest(BaseModel):
    """邮箱生成请求"""
    count: int = Field(default=10, ge=1, le=1000)
    domain: Optional[str] = Field(default=None, description="指定域名")


class IdCardRequest(BaseModel):
    """身份证生成请求"""
    count: int = Field(default=10, ge=1, le=1000)
    province: Optional[str] = Field(default=None, description="省份")
    gender: Optional[int] = Field(default=None, ge=1, le=2, description="性别: 1=男, 2=女")
    min_age: int = Field(default=18, ge=1, le=100)
    max_age: int = Field(default=65, ge=1, le=100)


class GenerateResponse(BaseModel):
    """生成响应"""
    success: bool = True
    count: int
    data: list[dict]


# ===== API 端点 =====

@router.post("/generate", response_model=GenerateResponse)
async def generate_data(request: GenerateRequest):
    """
    生成混合数据
    
    - **count**: 生成数量 (1-1000)
    - **types**: 数据类型列表，可选: phone, email, id_card
    """
    data = []
    
    for _ in range(request.count):
        item = {}
        if "phone" in request.types:
            item["phone"] = generate_phone()
        if "email" in request.types:
            item["email"] = generate_email()
        if "id_card" in request.types:
            item["id_card"] = generate_id_card()
        data.append(item)
    
    return GenerateResponse(count=len(data), data=data)


@router.post("/phone")
async def generate_phones(request: PhoneRequest):
    """生成手机号"""
    phones = [generate_phone(request.prefix) for _ in range(request.count)]
    return {"success": True, "count": len(phones), "data": phones}


@router.post("/email")
async def generate_emails(request: EmailRequest):
    """生成邮箱"""
    emails = [generate_email(request.domain) for _ in range(request.count)]
    return {"success": True, "count": len(emails), "data": emails}


@router.post("/idcard")
async def generate_idcards(request: IdCardRequest):
    """生成身份证号"""
    id_cards = [
        generate_id_card(
            province=request.province,
            gender=request.gender,
            min_age=request.min_age,
            max_age=request.max_age,
        )
        for _ in range(request.count)
    ]
    return {"success": True, "count": len(id_cards), "data": id_cards}


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}
