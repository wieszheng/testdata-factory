"""CLI 入口"""

import typer
from rich.console import Console
from rich.table import Table

from .generators.phone import generate_phone
from .generators.email import generate_email
from .generators.id_card import generate_id_card
from .exporters.csv_exporter import export_csv
from .exporters.json_exporter import export_json

app = typer.Typer(name="testgen", help="智能测试数据生成器")
console = Console()


@app.command()
def phone(
    count: int = typer.Option(10, "--count", "-c", help="生成数量"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """生成手机号"""
    data = [generate_phone() for _ in range(count)]
    _output_data(data, ["手机号"], output)


@app.command()
def email(
    count: int = typer.Option(10, "--count", "-c", help="生成数量"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """生成邮箱"""
    data = [generate_email() for _ in range(count)]
    _output_data(data, ["邮箱"], output)


@app.command()
def idcard(
    count: int = typer.Option(10, "--count", "-c", help="生成数量"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """生成身份证号"""
    data = [generate_id_card() for _ in range(count)]
    _output_data(data, ["身份证号"], output)


@app.command()
def generate(
    count: int = typer.Option(10, "--count", "-c", help="生成数量"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
    format: str = typer.Option("csv", "--format", "-f", help="输出格式: csv/json"),
):
    """生成混合数据（手机号 + 邮箱 + 身份证）"""
    data = [
        {
            "手机号": generate_phone(),
            "邮箱": generate_email(),
            "身份证号": generate_id_card(),
        }
        for _ in range(count)
    ]

    if output:
        if format == "json":
            export_json(data, output)
        else:
            export_csv(data, output)
        console.print(f"[green]OK[/green] 已导出到 {output}")
    else:
        table = Table(title=f"生成 {count} 条数据")
        table.add_column("手机号")
        table.add_column("邮箱")
        table.add_column("身份证号")
        for row in data:
            table.add_row(row["手机号"], row["邮箱"], row["身份证号"])
        console.print(table)


def _output_data(data: list, headers: list, output: str | None):
    """输出数据到控制台或文件"""
    if output:
        # 简单处理：每行一个值
        with open(output, "w", encoding="utf-8") as f:
            f.write(",".join(headers) + "\n")
            for item in data:
                f.write(f"{item}\n")
        console.print(f"[green]OK[/green] 已导出到 {output}")
    else:
        for item in data:
            console.print(item)


if __name__ == "__main__":
    app()
