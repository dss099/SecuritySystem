# 数据库迁移配置
TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',  # PostgreSQL
            # 'engine': 'tortoise.backends.mysql',  # MySQL or Mariadb
            'credentials': {
                'host': '127.0.0.1',
                'port': '5432',
                'user': 'fastapi_test',
                'password': 'fastapi_test',
                'database': 'management_backend',
                'minsize': 1,
                'maxsize': 5,
                # 'charset': 'utf8mb4',
                # "echo": True
            }
        },
    },
    'apps': {
        'models': {
            'models': [ 'app.Core.models',
                        'app.Client.models',
                        'app.Employee.models',
                        'app.Project.models',
                        'aerich.models'],
            'default_connection': 'default',

        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}