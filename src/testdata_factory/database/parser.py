"""数据库连接和解析"""

import asyncio
from typing import Optional
from dataclasses import dataclass

from .schema import ColumnInfo, TableInfo, DatabaseSchema, get_column_generator


@dataclass
class DatabaseConfig:
    """数据库连接配置"""
    db_type: str  # mysql, postgresql, sqlite
    host: str = "localhost"
    port: int = 3306
    username: str = "root"
    password: str = ""
    database: str = ""
    charset: str = "utf8mb4"


class DatabaseParser:
    """数据库解析器"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._connection = None
        self._last_error: Optional[str] = None
    
    async def connect(self) -> tuple[bool, str]:
        """连接数据库，返回 (是否成功, 错误信息)"""
        try:
            if self.config.db_type == "mysql":
                import aiomysql
                self._connection = await aiomysql.connect(
                    host=self.config.host,
                    port=self.config.port,
                    user=self.config.username,
                    password=self.config.password,
                    db=self.config.database,
                    charset=self.config.charset,
                    connect_timeout=10,
                )
                return (True, "")
            
            elif self.config.db_type == "postgresql":
                import asyncpg
                self._connection = await asyncpg.connect(
                    host=self.config.host,
                    port=self.config.port,
                    user=self.config.username,
                    password=self.config.password,
                    database=self.config.database,
                    timeout=10,
                )
                return (True, "")
            
            elif self.config.db_type == "sqlite":
                import aiosqlite
                self._connection = await aiosqlite.connect(self.config.database)
                return (True, "")
            
            else:
                return (False, f"不支持的数据库类型: {self.config.db_type}")
        
        except ImportError as e:
            return (False, f"缺少依赖: {str(e)}，请安装对应的数据库驱动")
        except Exception as e:
            error_msg = str(e)
            # 友好化错误信息
            if "Access denied" in error_msg:
                return (False, "用户名或密码错误")
            elif "Unknown database" in error_msg:
                return (False, f"数据库 '{self.config.database}' 不存在")
            elif "Connection refused" in error_msg:
                return (False, f"无法连接到 {self.config.host}:{self.config.port}，请检查服务是否启动")
            elif "No such file" in error_msg:
                return (False, f"SQLite 文件不存在: {self.config.database}")
            elif "name or service not known" in error_msg.lower():
                return (False, f"无法解析主机名: {self.config.host}")
            elif "timed out" in error_msg.lower():
                return (False, "连接超时，请检查网络或防火墙设置")
            else:
                return (False, f"连接失败: {error_msg}")
    
    async def close(self):
        """关闭连接"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    async def get_tables(self) -> list[str]:
        """获取所有表名"""
        if self.config.db_type == "mysql":
            async with self._connection.cursor() as cursor:
                await cursor.execute("SHOW TABLES")
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
        
        elif self.config.db_type == "postgresql":
            # asyncpg 使用不同的 API
            rows = await self._connection.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            return [row['table_name'] for row in rows]
        
        elif self.config.db_type == "sqlite":
            async with self._connection.cursor() as cursor:
                await cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                """)
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
        
        return []
    
    async def parse_table(self, table_name: str) -> TableInfo:
        """解析单个表结构"""
        columns = []
        
        if self.config.db_type == "mysql":
            columns = await self._parse_mysql_table(table_name)
        elif self.config.db_type == "postgresql":
            columns = await self._parse_postgresql_table(table_name)
        elif self.config.db_type == "sqlite":
            columns = await self._parse_sqlite_table(table_name)
        
        return TableInfo(table_name=table_name, columns=columns)
    
    async def _parse_mysql_table(self, table_name: str) -> list[ColumnInfo]:
        """解析 MySQL 表结构"""
        columns = []
        
        async with self._connection.cursor() as cursor:
            # 获取字段信息
            await cursor.execute(f"""
                SELECT 
                    COLUMN_NAME,
                    COLUMN_TYPE,
                    IS_NULLABLE,
                    COLUMN_KEY,
                    COLUMN_DEFAULT,
                    COLUMN_COMMENT
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """, (self.config.database, table_name))
            
            column_rows = await cursor.fetchall()
            
            # 获取外键信息
            await cursor.execute(f"""
                SELECT 
                    COLUMN_NAME,
                    REFERENCED_TABLE_NAME,
                    REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                AND REFERENCED_TABLE_NAME IS NOT NULL
            """, (self.config.database, table_name))
            
            fk_rows = await cursor.fetchall()
            fk_map = {row[0]: f"{row[1]}.{row[2]}" for row in fk_rows}
            
            for row in column_rows:
                col_name, col_type, is_nullable, col_key, col_default, col_comment = row
                
                column = ColumnInfo(
                    name=col_name,
                    data_type=col_type,
                    is_nullable=(is_nullable == "YES"),
                    is_primary_key=(col_key == "PRI"),
                    is_foreign_key=(col_name in fk_map),
                    foreign_key_ref=fk_map.get(col_name),
                    column_default=col_default,
                    column_comment=col_comment,
                )
                columns.append(column)
        
        return columns
    
    async def _parse_postgresql_table(self, table_name: str) -> list[ColumnInfo]:
        """解析 PostgreSQL 表结构"""
        columns = []
        
        # asyncpg 使用 fetch 方法
        column_rows = await self._connection.fetch("""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = $1
            ORDER BY ordinal_position
        """, table_name)
        
        # 获取主键信息
        pk_rows = await self._connection.fetch("""
            SELECT a.attname
            FROM pg_index i
            JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = $1::regclass AND i.indisprimary
        """, table_name)
        
        pk_columns = {row['attname'] for row in pk_rows}
        
        for row in column_rows:
            col_name = row['column_name']
            col_type = row['data_type']
            is_nullable = (row['is_nullable'] == "YES")
            col_default = row['column_default']
            
            column = ColumnInfo(
                name=col_name,
                data_type=col_type,
                is_nullable=is_nullable,
                is_primary_key=(col_name in pk_columns),
                is_foreign_key=False,
                foreign_key_ref=None,
                column_default=col_default,
                column_comment=None,
            )
            columns.append(column)
        
        return columns
    
    async def _parse_sqlite_table(self, table_name: str) -> list[ColumnInfo]:
        """解析 SQLite 表结构"""
        columns = []
        
        async with self._connection.cursor() as cursor:
            await cursor.execute(f"PRAGMA table_info({table_name})")
            rows = await cursor.fetchall()
            
            for row in rows:
                # cid, name, type, notnull, dflt_value, pk
                col_name = row[1]
                col_type = row[2]
                not_null = row[3]
                col_default = row[4]
                is_pk = row[5]
                
                column = ColumnInfo(
                    name=col_name,
                    data_type=col_type,
                    is_nullable=(not_null == 0),
                    is_primary_key=(is_pk == 1),
                    is_foreign_key=False,
                    foreign_key_ref=None,
                    column_default=col_default,
                    column_comment=None,
                )
                columns.append(column)
        
        return columns
    
    async def parse_database(self) -> DatabaseSchema:
        """解析整个数据库"""
        tables = {}
        table_names = await self.get_tables()
        
        for table_name in table_names:
            tables[table_name] = await self.parse_table(table_name)
        
        return DatabaseSchema(tables=tables)
