# Testdata Factory

智能测试数据生成器 - 测试同学的效率工具

## 功能

- 支持常见数据类型：手机号、身份证、邮箱、IP、地址、日期等
- 支持自定义正则规则
- 批量生成，支持导出 CSV/JSON
- CLI + Web UI 双入口

## 快速开始

```bash
# 安装
pip install -e .

# 生成 10 个手机号
testgen phone --count 10

# 生成 100 条混合数据导出 CSV
testgen generate --count 100 --output data.csv

# 帮助
testgen --help
```
