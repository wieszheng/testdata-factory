"""数据库逆向解析 API"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import asyncio

from ..database import (
    DatabaseParser, DatabaseConfig, get_column_generator,
    TableDependencyGraph, build_dependency_graph,
    UniqueConstraintParser, UniqueValueTracker,
)

router = APIRouter(tags=["database"])


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
        connected, error_msg = await parser.connect()
        
        if not connected:
            return ConnectionTestResponse(
                success=False,
                message=error_msg or "连接失败，请检查配置"
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
        connected, error_msg = await parser.connect()
        
        if not connected:
            raise HTTPException(status_code=400, detail=error_msg or "连接失败")
        
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


class MultiTableGenerateRequest(BaseModel):
    """多表生成请求"""
    db_type: str = Field(..., description="数据库类型")
    host: str = Field(default="localhost")
    port: int = Field(default=3306)
    username: str = Field(default="root")
    password: str = Field(default="")
    database: str = Field(..., description="数据库名")
    charset: str = Field(default="utf8mb4")
    tables: Optional[list[str]] = Field(default=None, description="要生成的表，默认全部")
    count_per_table: int = Field(default=10, description="每表生成数量")


class TableGenerationResult(BaseModel):
    """单表生成结果"""
    table_name: str
    count: int
    data: list[dict]


class MultiTableGenerateResponse(BaseModel):
    """多表生成响应"""
    success: bool
    message: str
    generation_order: list[str]
    dependency_layers: list[list[str]]
    unique_constraints: dict[str, list[list[str]]]
    results: list[TableGenerationResult]


@router.post("/generate-multi", response_model=MultiTableGenerateResponse)
async def generate_multi_tables(request: MultiTableGenerateRequest):
    """
    多表批量生成（支持外键依赖和唯一约束）
    
    - 自动解析外键依赖，按拓扑顺序生成
    - 自动检测唯一约束，确保数据不重复
    - 返回生成顺序和约束信息
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
        # 1. 连接数据库
        connected, error_msg = await parser.connect()
        if not connected:
            raise HTTPException(status_code=400, detail=error_msg)
        
        # 2. 解析数据库结构
        schema = await parser.parse_database()
        
        # 3. 确定要生成的表
        tables_to_generate = request.tables or list(schema.tables.keys())
        
        # 4. 构建依赖图
        dep_graph = build_dependency_graph(schema.tables)
        generation_order, cycles = dep_graph.topological_sort(tables_to_generate)
        dependency_layers = dep_graph.get_generation_order(tables_to_generate)
        
        # 5. 解析唯一约束
        unique_parser = UniqueConstraintParser(parser._connection, request.db_type)
        unique_constraints: dict[str, list[list[str]]] = {}
        
        for table_name in tables_to_generate:
            constraints = await unique_parser.parse_unique_constraints(table_name)
            unique_constraints[table_name] = [c.columns for c in constraints]
        
        # 6. 初始化唯一值追踪器
        value_tracker = UniqueValueTracker()
        for table_name, columns_list in unique_constraints.items():
            for columns in columns_list:
                value_tracker.register_constraint(table_name, columns)
        
        # 7. 按顺序生成数据
        results = []
        fk_values: dict[str, dict] = {}  # 外键值缓存 {table: {column: [values]}}
        
        for table_name in generation_order:
            table_info = schema.tables.get(table_name)
            if not table_info:
                continue
            
            table_data = await _generate_table_data_with_constraints(
                table_info=table_info,
                count=request.count_per_table,
                value_tracker=value_tracker,
                unique_columns=unique_constraints.get(table_name, []),
                fk_values=fk_values,
            )
            
            # 缓存外键值供后续表使用
            if table_info.columns:
                fk_values[table_name] = {}
                for col in table_info.columns:
                    fk_values[table_name][col.name] = [row.get(col.name) for row in table_data]
            
            results.append(TableGenerationResult(
                table_name=table_name,
                count=len(table_data),
                data=table_data,
            ))
        
        await parser.close()
        
        return MultiTableGenerateResponse(
            success=True,
            message=f"成功生成 {len(results)} 个表的数据",
            generation_order=generation_order,
            dependency_layers=dependency_layers,
            unique_constraints=unique_constraints,
            results=results,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        await parser.close()
        raise HTTPException(status_code=500, detail=str(e))


async def _generate_table_data_with_constraints(
    table_info: 'TableInfo',
    count: int,
    value_tracker: UniqueValueTracker,
    unique_columns: list[list[str]],
    fk_values: dict[str, dict],
) -> list[dict]:
    """
    生成单表数据（支持唯一约束和外键）
    """
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
            if "code" in column_name.lower():
                return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            elif "title" in column_name.lower():
                return generate_sentence()[:30]
            else:
                return generate_sentence()[:20]
        else:
            return generate_sentence()[:20]
    
    data = []
    max_attempts_per_row = 100
    
    for _ in range(count):
        row = {}
        attempts = 0
        
        while attempts < max_attempts_per_row:
            attempts += 1
            row = {}
            
            for col in table_info.columns:
                # 自增主键跳过
                if col.is_primary_key and col.data_type.lower() in ("int", "integer", "bigint"):
                    continue
                
                # 外键处理：从已生成的数据中随机选取
                if col.is_foreign_key and col.foreign_key_ref:
                    ref_parts = col.foreign_key_ref.split('.')
                    if len(ref_parts) == 2:
                        ref_table, ref_column = ref_parts
                        if ref_table in fk_values and ref_column in fk_values[ref_table]:
                            available_values = fk_values[ref_table][ref_column]
                            if available_values:
                                row[col.name] = random.choice(available_values)
                                continue
                
                # 普通字段生成
                row[col.name] = generate_by_type(
                    get_column_generator(col),
                    col.name
                )
            
            # 检查唯一约束
            if unique_columns:
                all_unique = True
                for columns in unique_columns:
                    values = tuple(row.get(c) for c in columns)
                    if not value_tracker.is_unique(table_info.table_name, columns, values):
                        all_unique = False
                        break
                
                if all_unique:
                    # 标记为已使用
                    for columns in unique_columns:
                        values = tuple(row.get(c) for c in columns)
                        value_tracker.mark_used(table_info.table_name, columns, values)
                    break
            else:
                break
        
        if row:
            data.append(row)
    
    return data
