"""CSV 导出器"""

import csv
from pathlib import Path


def export_csv(data: list[dict], output_path: str) -> None:
    """
    导出数据到 CSV 文件

    Args:
        data: 数据列表，每个元素是一个字典
        output_path: 输出文件路径
    """
    if not data:
        return

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(data[0].keys())

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
