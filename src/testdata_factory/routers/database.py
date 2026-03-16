"""数据库逆向解析 API"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import asyncio

from ..database import DatabaseParser, DatabaseConfig, get_column_generator

router = APIRouter(prefix="/database", tags=["database"])


# ===== 请求/响应模型 =====

class DatabaseConnectRequest(BaseModel):
    """数据库连接请求"""
    db_type: str = Field(..., description="数据库类型: mysql, postgresql, sqlite")
    host: str = Field(default="localhost", description="主机地址")
    port: int = Field(default=3306, description="端口")
    username: str = Field(default="root", description="用户名")
    password: str = Field(default="", description="密码")
    database: str = Field(..., description="数据库名/SQLite 文件路径")
    charset: str = Field(default="utf8mb4", description="字符集")


class ColumnInfoResponse(BaseModel):
    """字段信息响应"""
    name: str
    data_type: str
    is_nullable: bool
    is_primary_key: bool
    is_foreign_key: bool
    foreign_key_ref: Optional[str]
    column_default: Optional[str]
    column_comment: Optional[str]
    generator_type: str


class TableInfoResponse(BaseModel):
    """表信息响应"""
    table_name: str
    columns: list[ColumnInfoResponse]
    table_comment: Optional[str]


class ConnectionTestResponse(BaseModel):
    """连接测试响应"""
    success: bool
    message: str
    tables: list[str] = []


class TableDetailResponse(BaseModel):
    """表详情响应"""
    success: bool
    table: Optional[TableInfoResponse]


# ===== 全局连接缓存 =====

_connections: dict[str, DatabaseParser] = {}


# ===== API 端点 =====

@router.post("/connect", response_model=ConnectionTestResponse)
async def connect_database(request: DatabaseConnectRequest):
    """
    连接数据库并获取表列表
    
    - **db_type**: mysql, postgresql, sqlite
    - **database**: 数据库名或 SQLite 文件路径
    """
    config = DatabaseConfig(
        db_type=request.db_type,
        host=request.host,
        port=request.port,
        username=request.username,
        password=request.password,
        database=request.database,
        charset=request.charset,
    )
    
    parser = DatabaseParser(config)
    
    try:
        connected = await parser.connect()
        
        if not connected:
            return ConnectionTestResponse(
                success=False,
                message="连接失败，请检查配置"
            )
        
        tables = await parser.get_tables()
        
        # 缓存连接（简化版，实际应用需要更完善的会话管理）
        conn_id = f"{request.db_type}:{request.host}:{request.database}"
        _connections[conn_id] = parser
        
        return ConnectionTestResponse(
            success=True,
            message=f"连接成功，发现 {len(tables)} 个表",
            tables=tables
        )
    
    except Exception as e:
        return ConnectionTestResponse(
            success=False,
            message=f"连接错误: {str(e)}"
        )


@router.post("/table/{table_name}", response_model=TableDetailResponse)
async def get_table_detail(request: DatabaseConnectRequest, table_name: str):
    """获取表结构详情"""
    config = DatabaseConfig(
        db_type=request.db_type,
        host=request.host,
        port=request.port,
        username=request.username,
        password=request.password,
        database=request.database,
        charset=request.charset,
    )
    
    parser = DatabaseParser(config)
    
    try:
        connected = await parser.connect()
        
        if not connected:
            raise HTTPException(status_code=400, detail="连接失败")
        
        table_info = await parser.parse_table(table_name)
        
        # 转换为响应格式
        columns = []
        for col in table_info.columns:
            columns.append(ColumnInfoResponse(
                name=col.name,
                data_type=col.data_type,
                is_nullable=col.is_nullable,
                is_primary_key=col.is_primary_key,
                is_foreign_key=col.is_foreign_key,
                foreign_key_ref=col.foreign_key_ref,
                column_default=col.column_default,
                column_comment=col.column_comment,
                generator_type=get_column_generator(col),
            ))
        
        await parser.close()
        
        return TableDetailResponse(
            success=True,
            table=TableInfoResponse(
                table_name=table_info.table_name,
                columns=columns,
                table_comment=table_info.table_comment,
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_from_table(
    request: DatabaseConnectRequest,
    table_name: str,
    count: int = 10,
):
    """根据表结构生成数据"""
    # 先获取表结构
    table_detail = await get_table_detail(request, table_name)
    
    if not table_detail.success or not table_detail.table:
        raise HTTPException(status_code=400, detail="获取表结构失败")
    
    # 根据字段生成数据
    from ..generators.phone import generate_phone
    from ..generators.email import generate_email
    from ..generators.id_card import generate_id_card
    from ..generators.name import generate_name
    from ..generators.address import generate_address
    from ..generators.date import generate_date, generate_datetime
    from ..generators.company import generate_company
    from ..generators.position import generate_position
    from ..generators.money import generate_price
    from ..generators.color import generate_color
    from ..generators.url import generate_url
    from ..generators.uuid import generate_uuid
    from ..generators.credential import generate_username, generate_password
    from ..generators.text import generate_sentence
    from ..generators.ip import generate_ip
    from ..generators.bank_card import generate_bank_card
    import random
    import string
    
    generator_map = {
        "phone": generate_phone,
        "email": generate_email,
        "id_card": generate_id_card,
        "name": generate_name,
        "username": generate_username,
        "password": generate_password,
        "address": generate_address,
        "company": generate_company,
        "position": generate_position,
        "price": generate_price,
        "color": generate_color,
        "url": generate_url,
        "uuid": generate_uuid,
        "text": generate_sentence,
        "sentence": generate_sentence,
        "ip": generate_ip,
        "bank_card": generate_bank_card,
        "date": generate_date,
        "datetime": generate_datetime,
    }
    
    def generate_by_type(gen_type: str, column_name: str):
        if gen_type in generator_map:
            return generator_map[gen_type]()
        elif gen_type == "integer":
            return random.randint(1, 10000)
        elif gen_type == "decimal":
            return round(random.uniform(1, 1000), 2)
        elif gen_type == "boolean":
            return random.choice([True, False])
        elif gen_type == "string":
            # 根据字段名生成更合理的数据
            if "code" in column_name.lower():
                return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            elif "title" in column_name.lower():
                return generate_sentence()[:30]
            else:
                return generate_sentence()[:20]
        else:
            return generate_sentence()[:20]
    
    data = []
    for _ in range(count):
        row = {}
        for col in table_detail.table.columns:
            if col.is_primary_key and col.data_type.lower() in ("int", "integer", "bigint"):
                # 自增主键跳过
                continue
            row[col.name] = generate_by_type(col.generator_type, col.name)
        data.append(row)
    
    return {
        "success": True,
        "table": table_name,
        "count": len(data),
        "columns": [col.name for col in table_detail.table.columns],
        "data": data,
    }
