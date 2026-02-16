from fastapi import FastAPI
from infra.api.routers import user_routers
from infra.api.routers import task_routers
from infra.api.database import create_tables

app = FastAPI()

app.include_router(user_routers.router)
app.include_router(task_routers.router)

create_tables()
