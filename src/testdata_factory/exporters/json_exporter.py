"""JSON 导出器"""

import json
from pathlib import Path


def export_json(data: list[dict], output_path: str) -> None:
    """
    导出数据到 JSON 文件

    Args:
        data: 数据列表
        output_path: 输出文件路径
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
