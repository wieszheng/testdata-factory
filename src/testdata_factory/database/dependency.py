"""表依赖关系解析和拓扑排序"""

from dataclasses import dataclass
from typing import Optional
from collections import defaultdict


@dataclass
class ForeignKeyRelation:
    """外键关系"""
    from_table: str
    from_column: str
    to_table: str
    to_column: str


class TableDependencyGraph:
    """
    表依赖图
    
    用于解析表之间的外键依赖关系，并提供拓扑排序功能，
    确保在生成数据时按照依赖顺序插入。
    """
    
    def __init__(self):
        self._relations: list[ForeignKeyRelation] = []
        self._dependencies: dict[str, set[str]] = defaultdict(set)  # table ->依赖的表
        self._dependents: dict[str, set[str]] = defaultdict(set)    # table -> 被哪些表依赖
    
    def add_foreign_key(self, relation: ForeignKeyRelation):
        """添加外键关系"""
        self._relations.append(relation)
        self._dependencies[relation.from_table].add(relation.to_table)
        self._dependents[relation.to_table].add(relation.from_table)
    
    def get_dependencies(self, table: str) -> set[str]:
        """获取表依赖的所有表"""
        return self._dependencies.get(table, set()).copy()
    
    def get_dependents(self, table: str) -> set[str]:
        """获取依赖此表的所有表"""
        return self._dependents.get(table, set()).copy()
    
    def topological_sort(self, tables: Optional[list[str]] = None) -> tuple[list[str], list[str]]:
        """
        拓扑排序
        
        Args:
            tables: 要排序的表列表，默认排序所有表
            
        Returns:
            (排序后的表列表, 检测到的循环依赖列表)
        """
        if tables is None:
            tables = list(set(self._dependencies.keys()) | set(self._dependents.keys()))
        
        # Kahn's algorithm
        in_degree = defaultdict(int)
        for table in tables:
            in_degree[table] = 0
        
        for table in tables:
            for dep in self._dependencies.get(table, set()):
                if dep in tables:
                    in_degree[table] += 1
        
        # 入度为 0 的节点入队
        queue = [t for t in tables if in_degree[t] == 0]
        result = []
        
        while queue:
            # 按名称排序，保证结果稳定
            queue.sort()
            table = queue.pop(0)
            result.append(table)
            
            # 减少依赖此表的节点的入度
            for dependent in self._dependents.get(table, set()):
                if dependent in tables:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)
        
        # 检测循环依赖
        if len(result) < len(tables):
            cycles = [t for t in tables if t not in result]
            return result, cycles
        
        return result, []
    
    def get_generation_order(self, tables: list[str]) -> list[list[str]]:
        """
        获取分批生成顺序
        
        将表按依赖层级分组，同一层级的表可以并行生成。
        
        Args:
            tables: 要排序的表列表
            
        Returns:
            分层后的表列表，[[layer1_tables], [layer2_tables], ...]
        """
        sorted_tables, cycles = self.topological_sort(tables)
        
        if cycles:
            # 有循环依赖，把循环的表放在最后
            sorted_tables.extend(cycles)
        
        # 按层级分组
        layers = []
        remaining = set(sorted_tables)
        assigned = set()
        
        while remaining:
            layer = []
            for table in list(remaining):
                # 检查此表的所有依赖是否已分配
                deps = self._dependencies.get(table, set())
                if deps.issubset(assigned) or not deps:
                    layer.append(table)
            
            if not layer:
                # 无法继续分配（可能是循环依赖），把剩余的都放进去
                layer = list(remaining)
            
            layer.sort()
            layers.append(layer)
            for t in layer:
                remaining.discard(t)
                assigned.add(t)
        
        return layers
    
    def has_cycles(self, tables: Optional[list[str]] = None) -> bool:
        """检测是否存在循环依赖"""
        _, cycles = self.topological_sort(tables)
        return len(cycles) > 0
    
    def get_cycle_info(self, tables: Optional[list[str]] = None) -> list[str]:
        """获取循环依赖的表"""
        _, cycles = self.topological_sort(tables)
        return cycles


def build_dependency_graph(table_infos: dict[str, 'TableInfo']) -> TableDependencyGraph:
    """
    从表信息构建依赖图
    
    Args:
        table_infos: 表名 -> TableInfo 的映射
        
    Returns:
        构建好的依赖图
    """
    graph = TableDependencyGraph()
    
    for table_name, table_info in table_infos.items():
        for column in table_info.columns:
            if column.is_foreign_key and column.foreign_key_ref:
                # foreign_key_ref 格式: "table.column"
                parts = column.foreign_key_ref.split('.')
                if len(parts) == 2:
                    ref_table, ref_column = parts
                    graph.add_foreign_key(ForeignKeyRelation(
                        from_table=table_name,
                        from_column=column.name,
                        to_table=ref_table,
                        to_column=ref_column,
                    ))
    
    return graph
