"""URL 生成器"""

import random
from faker import Faker

fake = Faker("zh_CN")

# 常见域名
DOMAINS = [
    "baidu.com", "taobao.com", "jd.com", "tmall.com", "qq.com",
    "weibo.com", "zhihu.com", "csdn.net", "github.com", "google.com",
    "example.com", "test.com", "demo.com"
]

# 常见路径
PATHS = [
    "/api/users", "/api/products", "/api/orders", "/api/data",
    "/user/profile", "/user/settings", "/user/dashboard",
    "/products/list", "/products/detail", "/products/search",
    "/articles", "/posts", "/news", "/blog", "/docs",
    "/login", "/register", "/logout", "/reset-password"
]

# 常见查询参数
QUERY_PARAMS = [
    "id", "page", "size", "limit", "offset", "sort", "order",
    "keyword", "q", "search", "filter", "category", "tag",
    "from", "to", "start", "end", "date", "time"
]


def generate_url(https: bool = True) -> str:
    """
    生成 URL

    Args:
        https: 是否使用 HTTPS

    Returns:
        URL 字符串
    """
    protocol = "https" if https else "http"
    domain = random.choice(DOMAINS)
    path = random.choice(PATHS)
    
    # 50% 概率添加查询参数
    if random.random() < 0.5:
        params = []
        for _ in range(random.randint(1, 3)):
            key = random.choice(QUERY_PARAMS)
            value = fake.uuid4()[:8] if key == "id" else str(random.randint(1, 100))
            params.append(f"{key}={value}")
        query = "?" + "&".join(params)
    else:
        query = ""
    
    return f"{protocol}://{domain}{path}{query}"


def generate_domain() -> str:
    """生成域名"""
    return random.choice(DOMAINS)
