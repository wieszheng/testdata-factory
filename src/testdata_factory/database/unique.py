"""唯一约束解析和处理"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class UniqueConstraint:
    """唯一约束"""
    name: str
    table_name: str
    columns: list[str]
    

class UniqueConstraintParser:
    """
    唯一约束解析器
    
    用于从数据库表结构中提取唯一约束信息，
    并在生成数据时确保不违反约束。
    """
    
    def __init__(self, connection, db_type: str):
        self._connection = connection
        self._db_type = db_type
    
    async def parse_unique_constraints(self, table_name: str) -> list[UniqueConstraint]:
        """
        解析表的唯一约束
        
        Args:
            table_name: 表名
            
        Returns:
            唯一约束列表
        """
        if self._db_type == "mysql":
            return await self._parse_mysql_unique(table_name)
        elif self._db_type == "postgresql":
            return await self._parse_postgresql_unique(table_name)
        elif self._db_type == "sqlite":
            return await self._parse_sqlite_unique(table_name)
        return []
    
    async def _parse_mysql_unique(self, table_name: str) -> list[UniqueConstraint]:
        """解析 MySQL 唯一约束"""
        constraints = []
        
        # 查询唯一索引
        async with self._connection.cursor() as cursor:
            await cursor.execute("""
                SELECT 
                    INDEX_NAME,
                    GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) as columns
                FROM information_schema.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = %s
                AND NON_UNIQUE = 0
                AND INDEX_NAME != 'PRIMARY'
                GROUP BY INDEX_NAME
            """, (table_name,))
            
            rows = await cursor.fetchall()
            
            for row in rows:
                index_name = row[0]
                columns = row[1].split(',') if row[1] else []
                
                constraints.append(UniqueConstraint(
                    name=index_name,
                    table_name=table_name,
                    columns=columns,
                ))
        
        return constraints
    
    async def _parse_postgresql_unique(self, table_name: str) -> list[UniqueConstraint]:
        """解析 PostgreSQL 唯一约束"""
        constraints = []
        
        rows = await self._connection.fetch("""
            SELECT 
                con.conname as constraint_name,
                array_agg(a.attname ORDER BY array_position(con.conkey, a.attnum)) as columns
            FROM pg_constraint con
            JOIN pg_class rel ON rel.oid = con.conrelid
            JOIN pg_namespace nsp ON nsp.oid = con.connamespace
            JOIN pg_attribute a ON a.attrelid = con.conrelid AND a.attnum = ANY(con.conkey)
            WHERE con.contype = 'u'
            AND nsp.nspname = 'public'
            AND rel.relname = $1
            GROUP BY con.conname
        """, table_name)
        
        for row in rows:
            constraints.append(UniqueConstraint(
                name=row['constraint_name'],
                table_name=table_name,
                columns=list(row['columns']),
            ))
        
        return constraints
    
    async def _parse_sqlite_unique(self, table_name: str) -> list[UniqueConstraint]:
        """解析 SQLite 唯一约束"""
        constraints = []
        
        async with self._connection.cursor() as cursor:
            # 获取表的 CREATE 语句
            await cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            row = await cursor.fetchone()
            
            if row and row[0]:
                create_sql = row[0]
                
                # 解析 UNIQUE 约束
                # 格式1: UNIQUE (col1, col2)
                unique_pattern = r'UNIQUE\s*\(([^)]+)\)'
                for match in re.finditer(unique_pattern, create_sql, re.IGNORECASE):
                    columns_str = match.group(1)
                    columns = [c.strip().strip('"\'`') for c in columns_str.split(',')]
                    
                    constraints.append(UniqueConstraint(
                        name=f"unique_{table_name}_{ '_'.join(columns)}",
                        table_name=table_name,
                        columns=columns,
                    ))
                
                # 格式2: 列定义中的 UNIQUE
                col_unique_pattern = r'"?(\w+)"?\s+\w+[^,]*\bUNIQUE\b'
                for match in re.finditer(col_unique_pattern, create_sql, re.IGNORECASE):
                    column = match.group(1)
                    
                    constraints.append(UniqueConstraint(
                        name=f"unique_{table_name}_{column}",
                        table_name=table_name,
                        columns=[column],
                    ))
        
        return constraints


class UniqueValueTracker:
    """
    唯一值追踪器
    
    用于在批量生成数据时追踪已生成的值，确保不违反唯一约束。
    """
    
    def __init__(self):
        # {constraint_key: set of generated values}
        self._generated: dict[str, set] = {}
    
    def _make_key(self, table: str, columns: list[str]) -> str:
        """生成约束键"""
        return f"{table}:{':'.join(sorted(columns))}"
    
    def register_constraint(self, table: str, columns: list[str]):
        """注册唯一约束"""
        key = self._make_key(table, columns)
        if key not in self._generated:
            self._generated[key] = set()
    
    def is_unique(self, table: str, columns: list[str], values: tuple) -> bool:
        """
        检查值组合是否唯一
        
        Args:
            table: 表名
            columns: 列名列表
            values: 值元组，与 columns 顺序对应
            
        Returns:
            是否唯一（未被使用）
        """
        key = self._make_key(table, columns)
        value_key = values
        
        return value_key not in self._generated.get(key, set())
    
    def mark_used(self, table: str, columns: list[str], values: tuple):
        """标记值组合为已使用"""
        key = self._make_key(table, columns)
        if key not in self._generated:
            self._generated[key] = set()
        self._generated[key].add(values)
    
    def get_or_generate_unique(
        self,
        table: str,
        columns: list[str],
        generator_func,
        max_attempts: int = 100
    ) -> tuple:
        """
        获取或生成唯一值
        
        Args:
            table: 表名
            columns: 列名列表
            generator_func: 生成函数，返回值元组
            max_attempts: 最大尝试次数
            
        Returns:
            唯一值元组
            
        Raises:
            ValueError: 无法生成唯一值
        """
        for _ in range(max_attempts):
            values = generator_func()
            if self.is_unique(table, columns, values):
                self.mark_used(table, columns, values)
                return values
        
        raise ValueError(f"无法在 {max_attempts} 次尝试内生成唯一值: {table}.{columns}")
    
    def clear(self):
        """清空所有记录"""
        self._generated.clear()
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "constraint_count": len(self._generated),
            "value_counts": {k: len(v) for k, v in self._generated.items()},
        }
