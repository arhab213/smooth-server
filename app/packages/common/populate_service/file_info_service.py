from beanie import PydanticObjectId

from app.models.file_infos import FileInfos


class FileInfoRepository:
    async def insert_one(self, file_info: FileInfos):
        await file_info.create()
        return file_info.model_dump()

    async def find_one(self, id: PydanticObjectId):
        file_info = await FileInfos.get(id)
        return file_info if file_info else {}

    async def delete_one(self, id: str):
        file_infos = await FileInfos.get(PydanticObjectId(id))
        if file_infos:
            await file_infos.delete()
            return True
        return False

    async def update_one(self, id: str, file_infos: dict):
        updated_data = {k: v for k, v in file_infos.items() if v is not None}
        result = await FileInfos.find_one(FileInfos.id == PydanticObjectId(id)).update(
            {"$set": updated_data}
        )

        if (
            result.raw_result.get("nModified", 0) == 0
            and result.raw_result.get("n", 0) == 0
        ):
            return {}

        updated = await FileInfos.get(id)

        return updated if updated else {}


class FileInfoService:
    def __init__(self):
        self.repository = FileInfoRepository()

    async def add_file_infos(self, file_infos: dict):
        created = await self.repository.insert_one(FileInfos(**file_infos))
        return created if created else {}

    async def get_file_infos(self, id: str):
        file_infos = await self.repository.find_one(PydanticObjectId(id))
        return file_infos if file_infos else {}

    async def update_file_infos(self, id: str, file_infos: dict):

        updated = await self.repository.update_one(id, file_infos)
        return updated if updated else {}

    async def delete_file_infos(self, id: str):
        Deleted = await self.repository.delete_one(id)
        return True if Deleted else False
