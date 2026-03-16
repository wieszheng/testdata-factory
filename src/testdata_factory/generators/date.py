"""日期生成器"""

import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("zh_CN")


def generate_date(
    start_date: str | None = None,
    end_date: str | None = None,
    format: str = "%Y-%m-%d"
) -> str:
    """
    生成日期

    Args:
        start_date: 开始日期 (YYYY-MM-DD)，默认 10 年前
        end_date: 结束日期 (YYYY-MM-DD)，默认今天
        format: 输出格式

    Returns:
        日期字符串
    """
    if start_date is None:
        start = datetime.now() - timedelta(days=365 * 10)
    else:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    
    if end_date is None:
        end = datetime.now()
    else:
        end = datetime.strptime(end_date, "%Y-%m-%d")
    
    delta = (end - start).days
    random_date = start + timedelta(days=random.randint(0, delta))
    
    return random_date.strftime(format)


def generate_datetime(
    start_date: str | None = None,
    end_date: str | None = None,
    format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    生成日期时间

    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
        format: 输出格式

    Returns:
        日期时间字符串
    """
    if start_date is None:
        start = datetime.now() - timedelta(days=365 * 10)
    else:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    
    if end_date is None:
        end = datetime.now()
    else:
        end = datetime.strptime(end_date, "%Y-%m-%d")
    
    delta = (end - start).days
    random_date = start + timedelta(
        days=random.randint(0, delta),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )
    
    return random_date.strftime(format)


def generate_timestamp(
    start_date: str | None = None,
    end_date: str | None = None
) -> int:
    """
    生成时间戳

    Args:
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)

    Returns:
        Unix 时间戳（毫秒）
    """
    if start_date is None:
        start = datetime.now() - timedelta(days=365 * 10)
    else:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    
    if end_date is None:
        end = datetime.now()
    else:
        end = datetime.strptime(end_date, "%Y-%m-%d")
    
    delta = (end - start).total_seconds()
    random_seconds = random.uniform(0, delta)
    random_dt = start + timedelta(seconds=random_seconds)
    
    return int(random_dt.timestamp() * 1000)
