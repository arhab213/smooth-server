from datetime import datetime, timezone
from typing import Literal, Optional

from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field

from app.models.docker_info import DockerInfo
from app.models.file_infos import FileInfos

"""main scheme"""


class DeploymentInstance(Document):
    project_name: str
    file_infos: Optional[PydanticObjectId] = None
    decompressing_succeed: bool
    is_deployed: bool
    environment: Literal["prod", "dev"]
    docker_infos: Optional[PydanticObjectId] = None
    status: bool
    deleted: bool
    created_on: datetime = datetime.now(timezone.utc)
    updated_on: Optional[datetime] = None

    class Settings:
        name = "DeploymentInstance"


"""update scheme"""


class UpdateDeployment(BaseModel):
    project_name: str
    file_infos: Link[FileInfos]
    environment: Literal["prod", "dev"]
    is_deployed: bool
    docker_info: Link[DockerInfo]
    status: bool
    deleted: bool
    updated_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
