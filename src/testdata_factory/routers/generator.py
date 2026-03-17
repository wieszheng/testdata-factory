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
from ..exporters.excel_exporter import export_to_excel, export_single_column_to_excel
from ..templates import list_templates, get_template, get_template_fields, INDUSTRY_TEMPLATES

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
    dedup_info: Optional[Dict[str, Any]] = Field(
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


@router.post("/export/excel")
async def export_excel(request: GenerateRequest):
    """导出为 Excel 格式"""
    # 先调用 generate 生成数据
    request_copy = GenerateRequest(
        count=request.count,
        types=request.types,
        custom_rules=request.custom_rules,
        validate=request.validate,
        dedup=request.dedup
    )
    result = await generate_data(request_copy)
    
    if not result.data:
        return {"success": False, "message": "没有数据可导出"}
    
    try:
        excel_bytes = export_to_excel(result.data, result.types)
        # 返回 base64 编码的 Excel 数据
        import base64
        excel_b64 = base64.b64encode(excel_bytes).decode('utf-8')
        return {
            "success": True,
            "filename": f"test_data_{result.count}_{result.types[0] if result.types else 'export'}.xlsx",
            "data": excel_b64
        }
    except ImportError as e:
        return {"success": False, "message": str(e)}
    except Exception as e:
        return {"success": False, "message": f"导出失败: {str(e)}"}


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


# ===== 行业模板 API =====

@router.get("/industry/templates")
async def get_industry_templates():
    """获取行业模板列表"""
    return {
        "templates": list_templates(),
        "count": len(INDUSTRY_TEMPLATES)
    }


@router.get("/industry/templates/{template_name}")
async def get_template_detail(template_name: str):
    """获取模板详情"""
    template = get_template(template_name)
    if not template:
        return {"success": False, "message": "模板不存在"}
    return {
        "success": True,
        "template": {
            "name": template.name,
            "description": template.description,
            "fields": template.fields
        }
    }


class TemplateGenerateRequest(BaseModel):
    """行业模板生成请求"""
    template_name: str = Field(..., description="模板名称")
    count: int = Field(default=10, ge=1, le=1000, description="生成数量")
    validate: bool = Field(default=True, description="是否启用校验")
    dedup: bool = Field(default=False, description="是否启用去重")


@router.post("/industry/templates/generate")
async def generate_from_template(request: TemplateGenerateRequest):
    """根据行业模板生成数据"""
    template = get_template(request.template_name)
    if not template:
        return {"success": False, "message": "模板不存在"}
    
    # 字段类型映射到生成器
    type_to_generator = {
        "uuid": generate_uuid,
        "username": generate_username,
        "password": generate_password,
        "email": generate_email,
        "phone": generate_phone,
        "name": generate_name,
        "id_card": generate_id_card,
        "address": generate_address,
        "datetime": generate_datetime,
        "date": generate_date,
        "order_id": generate_order_id,
        "price": generate_price,
        "sentence": generate_sentence,
        "paragraph": generate_paragraph,
        "company": generate_company,
        "position": generate_position,
        "salary": generate_salary,
        "color": generate_color,
        "url": generate_url,
        "bank_card": generate_bank_card,
    }
    
    # 扩展映射 - 添加不存在的生成器
    def gen_integer():
        import random
        return str(random.randint(1, 10000))
    
    def gen_gender():
        import random
        return random.choice(["男", "女", "未知"])
    
    def gen_department():
        import random
        return random.choice(["技术部", "市场部", "运营部", "财务部", "人力资源部", "行政部"])
    
    def gen_category():
        import random
        return random.choice(["电子产品", "服装", "食品", "图书", "运动", "家居", "美妆"])
    
    def gen_status():
        import random
        return random.choice(["待支付", "已支付", "已完成", "已取消", "退款中"])
    
    def gen_currency():
        import random
        return random.choice(["CNY", "USD", "EUR", "JPY"])
    
    def gen_transaction_type():
        import random
        return random.choice(["收入", "支出", "转账", "退款"])
    
    def gen_tracking_no():
        import random
        return f"YT{random.randint(100000000000, 999999999999)}"
    
    def gen_logistics_status():
        import random
        return random.choice(["待揽收", "运输中", "已到达", "派送中", "已签收"])
    
    def gen_room_type():
        import random
        return random.choice(["标准间", "大床房", "豪华间", "套房", "总统套房"])
    
    def gen_rating():
        import random
        return str(round(random.uniform(3.5, 5.0), 1))
    
    def gen_tags():
        import random
        all_tags = ["热门", "新品", "推荐", "特价", "限时", "爆款"]
        return ",".join(random.sample(all_tags, k=random.randint(1, 3)))
    
    type_to_generator.update({
        "integer": gen_integer,
        "gender": gen_gender,
        "department": gen_department,
        "category": gen_category,
        "status": gen_status,
        "currency": gen_currency,
        "transaction_type": gen_transaction_type,
        "tracking_no": gen_tracking_no,
        "logistics_status": gen_logistics_status,
        "room_type": gen_room_type,
        "rating": gen_rating,
        "tags": gen_tags,
    })
    
    # 去重管理器
    dedup_mgr = get_dedup_manager()
    if request.dedup:
        dedup_mgr.clear()
    
    data = []
    field_names = [f["name"] for f in template.fields]
    field_types = [f["type"] for f in template.fields]
    
    for _ in range(request.count):
        row = {}
        for fname, ftype in zip(field_names, field_types):
            gen = type_to_generator.get(ftype, generate_sentence)
            row[fname] = gen()
        data.append(row)
    
    return {
        "success": True,
        "template": template.name,
        "count": len(data),
        "fields": field_names,
        "data": data
    }


# ===== 批量和异步生成 =====

class BatchGenerateRequest(BaseModel):
    """批量生成请求"""
    batches: list[GenerateRequest] = Field(..., description="批量生成配置列表")


@router.post("/generate/batch")
async def batch_generate(request: BatchGenerateRequest):
    """批量生成多组数据
    
    一次请求生成多组不同的数据
    
    示例请求:
    {
      "batches": [
        {"count": 10, "types": ["phone"]},
        {"count": 5, "types": ["email", "name"]},
        {"count": 20, "types": ["id_card"]}
      ]
    }
    """
    results = []
    for i, batch in enumerate(request.batches):
        # 调用生成逻辑
        batch_data = await generate_data(batch)
        results.append({
            "batch_index": i,
            "data": batch_data.data,
            "count": batch_data.count,
            "types": batch_data.types
        })
    
    return {
        "success": True,
        "batch_count": len(results),
        "total_records": sum(r["count"] for r in results),
        "results": results
    }


class AsyncGenerateRequest(BaseModel):
    """异步生成请求（大数据量）"""
    count: int = Field(default=100, ge=1, le=100000, description="生成数量")
    types: list[str] = Field(default=["phone", "email"], description="数据类型")
    validate: bool = Field(default=True)
    dedup: bool = Field(default=False)
    callback_url: Optional[str] = Field(default=None, description="完成后回调URL")


import asyncio
import uuid as uuid_module

# 存储异步任务状态
_async_tasks: dict[str, dict] = {}


@router.post("/generate/async")
async def async_generate(request: AsyncGenerateRequest):
    """异步生成大数据量
    
    适用于生成大量数据（>1000条），立即返回任务ID，
    后台处理完成后可通过 callback_url 回调或主动查询状态
    
    返回任务ID，可通过 /api/generate/async/status/{task_id} 查询状态
    """
    task_id = str(uuid_module.uuid4())[:8]
    
    # 创建任务记录
    _async_tasks[task_id] = {
        "status": "pending",
        "progress": 0,
        "total": request.count,
        "result": None,
        "error": None
    }
    
    # 启动后台任务
    asyncio.create_task(_run_async_generate(task_id, request))
    
    return {
        "success": True,
        "task_id": task_id,
        "status": "pending",
        "message": f"任务已创建，预计生成 {request.count} 条数据"
    }


async def _run_async_generate(task_id: str, request: AsyncGenerateRequest):
    """后台异步生成任务"""
    try:
        task = _async_tasks[task_id]
        task["status"] = "running"
        
        # 分批处理，避免内存溢出
        batch_size = 1000
        all_data = []
        
        for i in range(0, request.count, batch_size):
            current_count = min(batch_size, request.count - i)
            req = GenerateRequest(
                count=current_count,
                types=request.types,
                validate=request.validate,
                dedup=request.dedup
            )
            result = await generate_data(req)
            all_data.extend(result.data)
            
            # 更新进度
            task["progress"] = len(all_data)
        
        task["status"] = "completed"
        task["progress"] = request.count
        task["result"] = {
            "count": len(all_data),
            "types": request.types,
            "data": all_data[:100]  # 只返回前100条，实际应存文件
        }
        
    except Exception as e:
        _async_tasks[task_id]["status"] = "failed"
        _async_tasks[task_id]["error"] = str(e)


@router.get("/generate/async/status/{task_id}")
async def get_async_status(task_id: str):
    """查询异步任务状态"""
    task = _async_tasks.get(task_id)
    if not task:
        return {"success": False, "message": "任务不存在"}
    
    return {
        "success": True,
        "task_id": task_id,
        "status": task["status"],
        "progress": task["progress"],
        "total": task["total"],
        "result": task.get("result"),
        "error": task.get("error")
    }
