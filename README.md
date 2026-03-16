# TestData Factory

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.109+-orange?style=flat-square" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react" alt="React">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
</p>

智能测试数据生成器 - 测试同学的效率工具

## 功能特性

### 🎯 核心能力
- **17 种内置数据类型**：手机号、身份证、邮箱、IP、地址、日期、银行卡号、价格、颜色、URL、UUID、用户名、密码、姓名、公司名、职位、句子
- **自定义正则规则**：支持自定义正则表达式，灵活生成各种格式数据
- **批量生成**：支持 1-1000 条数据生成
- **多格式导出**：CSV、JSON、SQL

### 🎨 UI 特性
- **双主题模式**：深色/亮色主题一键切换
- **Glassmorphism 设计**：现代科技风界面
- **响应式布局**：适配不同屏幕尺寸

### 🔌 API 能力
- 完整的 RESTful API
- OpenAPI 文档自动生成

## 快速开始

### 后端启动

```bash
# 进入项目目录
cd testdata-factory

# 安装依赖
pip install -e .

# 启动后端 (默认端口 8001)
uvicorn testdata_factory.api:app --reload --port 8001

# 或使用 Python 直接运行
python -m testdata_factory.api
```

### 前端启动

```bash
# 进入前端目录
cd web

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 使用 CLI

```bash
# 生成 10 个手机号
testgen phone --count 10

# 生成 100 条混合数据导出 CSV
testgen generate --count 100 --output data.csv

# 查看帮助
testgen --help
```

## API 调用示例

```bash
# 生成混合数据（内置类型 + 自定义正则）
curl -X POST http://localhost:8001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "count": 10,
    "types": ["phone", "email"],
    "custom_rules": [
      {"name": "订单号", "pattern": "ORD\\d{10}"}
    ]
  }'

# 仅使用自定义正则生成
curl -X POST http://localhost:8001/api/regex \
  -H "Content-Type: application/json" \
  -d '{
    "count": 10,
    "pattern": "\\d{4}-\\d{2}-\\d{2}"
  }'
```

## 项目结构

```
testdata-factory/
├── src/
│   └── testdata_factory/
│       ├── api.py              # FastAPI 主入口
│       ├── generators/         # 数据生成器
│       │   ├── phone.py
│       │   ├── email.py
│       │   └── ...
│       └── routers/            # API 路由
│           └── generator.py
├── web/                       # React 前端
│   ├── src/
│   │   ├── App.tsx
│   │   └── index.css
│   └── package.json
└── README.md
```

## 技术栈

- **后端**：Python + FastAPI + Faker
- **前端**：React + TypeScript + Tailwind CSS
- **数据库**：SQLAlchemy (支持 PostgreSQL/MySQL/SQLite)

## 预览

![深色模式](https://via.placeholder.com/800x400/1a1f2e/ff6b4a?text=Dark+Mode)
![亮色模式](https://via.placeholder.com/800x400/f3f4f6/4a3df0?text=Light+Mode)

## License

MIT License - Made with ♥ by 知微 & 千机
