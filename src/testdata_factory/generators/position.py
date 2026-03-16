"""职位生成器"""

import random
from faker import Faker

fake = Faker("zh_CN")

# 技术类职位
TECH_POSITIONS = [
    "软件工程师", "前端开发工程师", "后端开发工程师", "全栈工程师", "架构师",
    "技术总监", "技术经理", "研发工程师", "算法工程师", "数据工程师",
    "测试工程师", "测试开发工程师", "运维工程师", "DevOps工程师", "安全工程师",
    "移动端开发工程师", "iOS开发工程师", "Android开发工程师", "嵌入式工程师",
    "大数据工程师", "AI工程师", "机器学习工程师", "深度学习工程师",
]

# 产品类职位
PRODUCT_POSITIONS = [
    "产品经理", "产品总监", "产品助理", "产品运营", "用户研究",
    "交互设计师", "UI设计师", "UX设计师", "视觉设计师",
]

# 运营类职位
OPERATION_POSITIONS = [
    "运营经理", "运营专员", "新媒体运营", "内容运营", "用户运营",
    "活动运营", "社区运营", "电商运营", "市场经理", "市场专员",
]

# 管理类职位
MANAGEMENT_POSITIONS = [
    "项目经理", "项目总监", "部门经理", "总经理", "副总经理",
    "CEO", "CTO", "CFO", "COO", "总监",
]

# 职级
LEVELS = ["实习生", "初级", "中级", "高级", "资深", "专家", "首席"]


def generate_position(department: str | None = None) -> str:
    """
    生成职位名称

    Args:
        department: 部门类型，可选: tech, product, operation, management

    Returns:
        职位名称
    """
    if department == "tech":
        positions = TECH_POSITIONS
    elif department == "product":
        positions = PRODUCT_POSITIONS
    elif department == "operation":
        positions = OPERATION_POSITIONS
    elif department == "management":
        positions = MANAGEMENT_POSITIONS
    else:
        positions = TECH_POSITIONS + PRODUCT_POSITIONS + OPERATION_POSITIONS + MANAGEMENT_POSITIONS
    
    position = random.choice(positions)
    
    # 30% 概率加职级
    if random.random() < 0.3 and department != "management":
        level = random.choice(LEVELS)
        return f"{level}{position}"
    
    return position


def generate_job_title() -> str:
    """生成职位头衔（更正式）"""
    return fake.job()
