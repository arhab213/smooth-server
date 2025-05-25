from beanie import PydanticObjectId

from app.models.deployment_instance import (
    DeploymentInstance,
)
from app.packages.helpers.build_functions_responses import beanie_document_to_dict


class DeploymentRepositoty:
    async def insert_one(self, deployment: DeploymentInstance) -> DeploymentInstance:
        await deployment.insert()
        result = deployment.model_dump()
        return result

    async def get_one(self, deployment_id: str) -> DeploymentInstance:
        return await DeploymentInstance.get(PydanticObjectId(deployment_id))

    async def delete_one(self, id: str) -> bool:
        deployment = await DeploymentInstance.get(PydanticObjectId(id))

        if deployment:
            await deployment.delete()
            return True
        else:
            return False

    async def update_one(
        self,
        deployment_id: str,
        updated_deployment_instance: dict,
    ) -> DeploymentInstance:

        await DeploymentInstance.find_one(
            DeploymentInstance.id == PydanticObjectId(deployment_id)
        ).update({"$set": updated_deployment_instance})
        updated = await DeploymentInstance.get(deployment_id)
        return beanie_document_to_dict(updated)
