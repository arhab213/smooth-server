from beanie import PydanticObjectId

from app.models.docker_info import DockerInfo
from app.packages.helpers.build_functions_responses import beanie_document_to_dict


class DockerInfoRepository:
    async def insert_one(self, docker_info: DockerInfo):
        await docker_info.create()
        return docker_info.model_dump()

    async def find_one(self, id: PydanticObjectId):
        docker_info = await DockerInfo.get(id)
        return docker_info if docker_info else None

    async def delete_one(self, id: str):
        docker_info = await DockerInfo.get(PydanticObjectId(id))
        if docker_info:
            await docker_info.delete()
            return True
        return False

    async def update_one(self, id: str, docker_info: dict):
        update_data = {k: v for k, v in docker_info.items() if v is not None}
        result = await DockerInfo.find_one(
            DockerInfo.id == PydanticObjectId(id)
        ).update({"$set": update_data})

        updated = await DockerInfo.get(id)

        if (
            result.raw_result.get("nModified", 0) == 0
            and result.raw_result.get("n", 0) == 0
        ):
            return {}

        return beanie_document_to_dict(updated) if updated else {}


class DockerInfoService:
    def __init__(self):
        self.repository = DockerInfoRepository()

    async def add_docker_info(self, data: dict):
        result = await self.repository.insert_one(DockerInfo(**data))
        return result if result else {}

    async def get_docker_info(self, id: str):
        result = await self.repository.find_one(PydanticObjectId(id))
        return result if result else {}

    async def update_docker_info(self, id: str, update_data: dict):

        updated = await self.repository.update_one(id, update_data)
        return updated if updated else {}

    async def delete_docker_infos(self, id: str):
        Deleted = await self.repository.delete_one(PydanticObjectId(id))
        return True if Deleted else False
