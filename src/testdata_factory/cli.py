"""CLI 入口"""

import typer
from rich.console import Console
from rich.table import Table

from .generators.phone import generate_phone
from .generators.email import generate_email
from .generators.id_card import generate_id_card
from .generators.ip import generate_ip
from .generators.address import generate_address
from .generators.date import generate_date, generate_datetime
from .generators.bank_card import generate_bank_card
from .generators.name import generate_name
from .generators.url import generate_url
from .generators.company import generate_company
from .generators.position import generate_position
from .generators.money import generate_price, generate_salary
from .generators.color import generate_color
from .generators.uuid import generate_uuid, generate_order_id, generate_serial_number
from .generators.credential import generate_username, generate_password
from .generators.text import generate_sentence, generate_paragraph
from .generators.regex import generate_from_regex
from .exporters.csv_exporter import export_csv
from .exporters.json_exporter import export_json
from .templates import INDUSTRY_TEMPLATES, list_templates

app = typer.Typer(name="testgen", help="智能测试数据生成器")
console = Console()

# 数据类型生成器映射
DATA_TYPE_GENERATORS = {
    "phone": generate_phone,
    "email": generate_email,
    "id_card": generate_id_card,
    "idcard": generate_id_card,
    "ip": generate_ip,
    "address": generate_address,
    "date": generate_date,
    "datetime": generate_datetime,
    "bank_card": generate_bank_card,
    "bankcard": generate_bank_card,
    "name": generate_name,
    "url": generate_url,
    "company": generate_company,
    "position": generate_position,
    "price": generate_price,
    "salary": generate_salary,
    "color": generate_color,
    "uuid": generate_uuid,
    "order_id": generate_order_id,
    "serial_number": generate_serial_number,
    "username": generate_username,
    "password": generate_password,
    "sentence": generate_sentence,
    "paragraph": generate_paragraph,
}


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
    types: list[str] = typer.Option(["phone"], "--type", "-t", help="数据类型"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """生成混合类型数据
    
    示例: testgen generate -c 100 -t phone -t email -t name
    """
    # 过滤有效的类型
    valid_types = [t for t in types if t in DATA_TYPE_GENERATORS]
    if not valid_types:
        console.print("[red]无可用的数据类型[/red]")
        return
    
    data = []
    for _ in range(count):
        row = {}
        for dtype in valid_types:
            row[dtype] = DATA_TYPE_GENERATORS[dtype]()
        data.append(row)
    
    _output_data(data, valid_types, output)


@app.command()
def templates():
    """查看行业模板列表"""
    template_list = list_templates()
    
    table = Table(title="行业模板")
    table.add_column("Key", style="cyan")
    table.add_column("名称", style="green")
    table.add_column("描述", style="white")
    table.add_column("字段数", justify="right", style="yellow")
    
    for key, info in template_list.items():
        table.add_row(
            key,
            info["name"],
            info["description"],
            str(info["field_count"])
        )
    
    console.print(table)


@app.command()
def types():
    """查看支持的数据类型"""
    table = Table(title="支持的数据类型")
    table.add_column("类型", style="cyan")
    table.add_column("说明", style="white")
    
    type_docs = {
        "phone": "手机号",
        "email": "邮箱",
        "id_card": "身份证",
        "ip": "IP地址",
        "address": "地址",
        "date": "日期",
        "datetime": "日期时间",
        "bank_card": "银行卡号",
        "name": "姓名",
        "url": "网址",
        "company": "公司名",
        "position": "职位",
        "price": "价格",
        "salary": "薪资",
        "color": "颜色",
        "uuid": "UUID",
        "order_id": "订单号",
        "serial_number": "序列号",
        "username": "用户名",
        "password": "密码",
        "sentence": "句子",
        "paragraph": "段落",
    }
    
    for dtype, doc in type_docs.items():
        table.add_row(dtype, doc)
    
    console.print(table)


@app.command()
def user_profile(
    count: int = typer.Option(10, "--count", "-c", help="生成数量"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """用户资料模板"""
    _generate_template("user_profile", count, output)


@app.command()
def order(
    count: int = typer.Option(10, "--count", "-c", help="生成数量"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """订单信息模板"""
    _generate_template("order", count, output)


@app.command()
def product(
    count: int = typer.Option(10, "--count", "-c", help="生成数量"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """商品信息模板"""
    _generate_template("product", count, output)


@app.command()
def employee(
    count: int = typer.Option(10, "--count", "-c", help="生成数量"),
    output: str = typer.Option(None, "--output", "-o", help="输出文件路径"),
):
    """员工信息模板"""
    _generate_template("employee", count, output)


def _generate_template(template_name: str, count: int, output: str):
    """根据模板生成数据"""
    template = INDUSTRY_TEMPLATES.get(template_name)
    if not template:
        console.print(f"[red]模板 {template_name} 不存在[/red]")
        return
    
    # 字段类型映射
    field_types = template.fields
    
    data = []
    for _ in range(count):
        row = {}
        for field in field_types:
            fname = field["name"]
            ftype = field["type"]
            
            # 简单映射
            if ftype in DATA_TYPE_GENERATORS:
                row[fname] = DATA_TYPE_GENERATORS[ftype]()
            elif ftype == "gender":
                row[fname] = "男" if _ % 2 == 0 else "女"
            elif ftype == "department":
                depts = ["技术部", "市场部", "运营部", "财务部", "人力资源部"]
                row[fname] = depts[_ % len(depts)]
            elif ftype == "category":
                cats = ["电子产品", "服装", "食品", "图书", "运动"]
                row[fname] = cats[_ % len(cats)]
            elif ftype == "status":
                row[fname] = "已完成"
            elif ftype == "currency":
                row[fname] = "CNY"
            elif ftype == "transaction_type":
                row[fname] = "收入"
            elif ftype == "tracking_no":
                row[fname] = f"YT{100000000000 + _}"
            elif ftype == "room_type":
                rooms = ["标准间", "大床房", "豪华间", "套房"]
                row[fname] = rooms[_ % len(rooms)]
            elif ftype == "rating":
                row[fname] = str(round(3.5 + (_ % 15) * 0.1, 1))
            elif ftype == "tags":
                row[fname] = "热门,推荐"
            elif ftype == "integer":
                row[fname] = str(_ + 1)
            else:
                row[fname] = str(_)
        
        data.append(row)
    
    _output_data(data, [f["name"] for f in field_types], output)


def _output_data(data, columns: list[str], output: str):
    """输出数据"""
    if not data:
        console.print("[yellow]没有数据生成[/yellow]")
        return
    
    # 显示前5条
    console.print(f"[green]已生成 {len(data)} 条数据[/green]")
    
    if output:
        # 根据扩展名判断格式
        if output.endswith(".csv"):
            export_csv(data, columns, output)
            console.print(f"[green]已导出到 {output}[/green]")
        elif output.endswith(".json"):
            export_json(data, output)
            console.print(f"[green]已导出到 {output}[/green]")
        else:
            # 默认 CSV
            export_csv(data, columns, output + ".csv")
            console.print(f"[green]已导出到 {output}.csv[/green]")
    else:
        # 打印前几条
        table = Table(show_header=True, header_style="bold magenta")
        for col in columns:
            table.add_column(col)
        
        for row in data[:5]:
            table.add_row(*[str(row.get(col, "")) for col in columns])
        
        console.print(table)
        
        if len(data) > 5:
            console.print(f"[dim]... 还有 {len(data) - 5} 条数据， use -o output.csv 导出全部[/dim]")


if __name__ == "__main__":
    app()
