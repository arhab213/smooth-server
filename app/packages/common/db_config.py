from typing import List

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

##change the print with logger service


class DbConfig:
    def __init__(self, models: List[Document], mongo_uri: str):
        self.models = models
        self.MongoURI = mongo_uri
        self.Client = AsyncIOMotorClient(self.MongoURI)

    async def init_db(self) -> None:
        print("initializing the db connection.....")
        await init_beanie(
            database=self.Client["SmoothServer"], document_models=self.models
        )

    def close_db(self) -> None:
        print("closing the db connection.....")
        self.Client.close()
