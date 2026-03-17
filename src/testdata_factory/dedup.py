"""数据去重工具"""

from typing import Any


class DedupManager:
    """去重管理器"""

    def __init__(self):
        self._seen: dict[str, set[Any]] = {}

    def add(self, field_type: str, value: Any) -> bool:
        """
        添加值并检查是否重复

        Args:
            field_type: 字段类型（如 phone, id_card, email）
            value: 要检查的值

        Returns:
            True if value is new (not duplicate), False if duplicate
        """
        if field_type not in self._seen:
            self._seen[field_type] = set()

        if value in self._seen[field_type]:
            return False

        self._seen[field_type].add(value)
        return True

    def get_seen(self, field_type: str) -> set[Any]:
        """获取已见过的值"""
        return self._seen.get(field_type, set())

    def count(self, field_type: str) -> int:
        """获取某类型的去重后数量"""
        return len(self._seen.get(field_type, set()))

    def clear(self, field_type: str | None = None):
        """清空去重记录"""
        if field_type:
            self._seen.pop(field_type, None)
        else:
            self._seen.clear()

    def __len__(self):
        """总去重数量"""
        return sum(len(v) for v in self._seen.values())


# 全局去重管理器实例
_global_dedup = DedupManager()


def get_dedup_manager() -> DedupManager:
    """获取全局去重管理器"""
    return _global_dedup


def reset_dedup():
    """重置全局去重管理器"""
    _global_dedup.clear()
