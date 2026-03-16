"""FastAPI 后端入口"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import generator

app = FastAPI(
    title="TestData Factory API",
    description="智能测试数据生成器 - 测试同学的效率工具",
    version="0.1.0",
)

# CORS 配置 - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite 开发服务器
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(generator.router, prefix="/api", tags=["generator"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "TestData Factory API",
        "version": "0.1.0",
        "docs": "/docs",
    }
