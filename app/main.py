import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.models.deployment_instance import DeploymentInstance
from app.models.docker_info import DockerInfo
from app.models.file_infos import FileInfos
from app.packages.common.db_config import DbConfig
from app.packages.common.http_exceptions_handling import ExceptionCase
from app.router import deployment_router

load_dotenv()

db_config = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_config

    db_config = DbConfig(
        models=[DeploymentInstance, DockerInfo, FileInfos],
        mongo_uri=os.getenv("DB_PATH_DEVELOPMENT"),
    )
    await db_config.init_db()
    yield

    db_config.close_db()


app = FastAPI(lifespan=lifespan)


@app.exception_handler(ExceptionCase)
async def custom_exception_handler(request: Request, exc: ExceptionCase):
    return JSONResponse(status_code=exc.status_code, content=exc.json())


app.include_router(deployment_router.router, tags=["Deployment"])


@app.get("/")
def root():
    return "working good"
