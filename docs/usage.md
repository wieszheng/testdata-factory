# TestData Factory 使用说明

## 快速开始

### 1. 安装

```bash
pip install testdata-factory
```

### 2. 启动 Web 界面

```bash
# 启动后端 API 服务
cd testdata-factory
uvicorn testdata_factory.api:app --host 0.0.0.0 --port 8003 --reload

# 启动前端界面
cd web
npm install
npm run dev
```

访问 `http://localhost:5173/` 即可使用。

## 功能介绍

### 数据类型

支持 **18种** 常用数据类型：

| 数据类型 | 说明 | 示例 |
|---------|------|------|
| username | 用户名 | john_doe123 |
| password | 密码 | Abc@123456 |
| email | 邮箱 | user@example.com |
| phone | 手机号 | 13812345678 |
| name | 中文姓名 | 张三 |
| idcard | 身份证号 | 110101199001011234 |
| address | 地址 | 北京市朝阳区xxx路xxx号 |
| datetime | 日期时间 | 2024-01-01 12:00:00 |
| date | 日期 | 2024-01-01 |
| time | 时间 | 12:00:00 |
| url | 网址 | https://example.com |
| ip | IP地址 | 192.168.1.1 |
| uuid | UUID | 123e4567-e89b-12d3-a456-426614174000 |
| age | 年龄 | 25 |
| gender | 性别 | 男/女 |
| company | 公司名称 | 北京科技有限公司 |
| job | 职位 | 软件工程师 |
| salary | 薪资 | 15000 |

### 行业模板

提供 **8个** 预设行业模板：

1. **用户资料** - 用户名、密码、邮箱、手机号、姓名、身份证、地址、日期时间
2. **订单信息** - 订单号、用户名、商品名、数量、价格、日期、状态
3. **商品信息** - 商品名、价格、库存、分类、描述、图片
4. **员工信息** - 员工号、姓名、部门、职位、薪资、入职日期
5. **财务数据** - 交易号、类型、金额、账户、日期、备注
6. **物流信息** - 运单号、收件人、地址、状态、日期
7. **文章内容** - 标题、作者、内容、分类、日期、阅读量
8. **酒店预订** - 预订号、客户名、房型、入住日期、退房日期、价格

### 自定义规则

支持通过正则表达式自定义数据生成规则：

**示例：**

| 字段名 | 正则表达式 | 生成结果 |
|-------|-----------|---------|
| 订单号 | `ORD\d{14}` | ORD38472910562831 |
| 产品编码 | `PROD[A-Z]{2}\d{6}` | PRODAB123456 |
| 会员卡 | `VIP\d{8}` | VIP12345678 |

**支持的语法：**

- `\d` - 数字 (0-9)
- `\w` - 字母数字下划线
- `\a` - 小写字母
- `\A` - 大写字母
- `[abc]` - 字符类
- `[a-z]` - 范围
- `{n}` - 重复 n 次
- `{n,m}` - 重复 n-m 次

### 数据去重

支持对指定字段进行去重：

- 手机号
- 身份证号
- 邮箱
- 自定义字段

### 导出格式

支持 **4种** 导出格式：

1. **CSV** - 逗号分隔值
2. **JSON** - JSON 格式
3. **Excel** - Excel 表格 (.xlsx)
4. **SQL** - INSERT 语句

## CLI 命令

### 生成数据

```bash
# 生成 100 条数据
testgen generate -c 100 -t phone -t email -t name

# 导出到文件
testgen generate -c 100 -t phone -t email -o output.csv

# 使用模板
testgen user-profile -c 50
```

### 查看模板

```bash
testgen templates
```

### 查看数据类型

```bash
testgen types
```

## API 接口

### 生成数据

```bash
POST /api/generate
Content-Type: application/json

{
  "count": 10,
  "types": ["phone", "email", "name"],
  "custom_rules": [
    {
      "name": "订单号",
      "pattern": "ORD\\d{14}"
    }
  ]
}
```

### 获取模板

```bash
GET /api/industry/templates
```

### 导出数据

```bash
POST /api/export
Content-Type: application/json

{
  "data": [...],
  "format": "csv"
}
```

## 常见问题

### 1. 如何添加新的数据类型？

在 `src/testdata_factory/generators/` 目录下添加新的生成器。

### 2. 如何自定义数据格式？

使用自定义规则功能，通过正则表达式定义格式。

### 3. 生成的数据会有重复吗？

启用去重功能后，系统会自动去重。

## 技术支持

- GitHub: https://github.com/wieszheng/testdata-factory
- Issues: https://github.com/wieszheng/testdata-factory/issues
