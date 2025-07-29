from fastapi import FastAPI
import uvicorn

from router import api_router

from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM


app = FastAPI(title="My Project")

# 数据库迁移配置
register_tortoise(
    app = app,
    config = TORTOISE_ORM,
    # generate_schemas=True, #如数据库为空，则自动生成对应表单
)
# aerich init -t Backend.settings.TORTOISE_ORM --location Backend/migrations

# 挂载所有子路由
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)

