from app.models.deployment_instance import DeploymentInstance
from app.packages.common.http_exceptions_handling import AppException, ExceptionCase
from app.packages.common.populate_service.populate import PopulateService
from app.packages.constant.response_messages import (
    DEPLOYEMENT_INSTANCE_NOT_FOUND,
    FAILED_TO_CREATE_DEPLOYEMENT_INSTANCE,
    FAILED_TO_DELETE_DEPLOYMENT_INSTANCE,
    FAILED_TO_UPDATE_DEPLOYMENT_INSTANCE,
    deployment_instance_created_successfully,
    deployment_instance_deleted_successfully,
    deployment_instance_updated_successfully,
)
from app.repository.deployment_repository import DeploymentRepositoty


class DeploymentService:
    def __init__(self):
        self.repository = DeploymentRepositoty()
        self.populate = PopulateService()

    async def deployProject(self, deployement_data: dict):
        try:

            docker_infos = deployement_data.pop("docker_infos", None)
            file_infos = deployement_data.pop("file_infos", None)

            converted_data = await self.populate.create_populated_fields(
                DeploymentInstance(**deployement_data),
                docker_infos,
                file_infos,
            )

            result = await self.repository.insert_one(
                DeploymentInstance(**converted_data)
            )
            if not result:
                return AppException.InternalServer(
                    FAILED_TO_CREATE_DEPLOYEMENT_INSTANCE, None
                ).json()
            return AppException.Created(
                deployment_instance_created_successfully(result["id"]), result
            ).json()

        except ExceptionCase as e:
            return e.json()
        except Exception as e:
            return AppException.InternalServer(
                "An unexpected error occurred", {"error": str(e)}
            ).json()

    async def getProject(self, id: str):
        try:

            deployment_instance = await self.repository.get_one(id)
            if not deployment_instance:
                return AppException.NotFound(
                    DEPLOYEMENT_INSTANCE_NOT_FOUND, None
                ).json()

            result = await self.populate.get_populated_fields(deployment_instance)
            return result

        except ExceptionCase as e:
            return e.json()
        except Exception as e:
            return AppException.InternalServer(
                "An unexpected error occurred", {"error": str(e)}
            ).json()

    async def updateProject(self, id: str, update_deployment_instance: dict):
        try:
            deployment_instance = await self.repository.get_one(id)

            docker_infos = update_deployment_instance.pop(
                "docker_infos", str(deployment_instance.docker_infos)
            )
            file_infos = update_deployment_instance.pop(
                "file_infos", str(deployment_instance.file_infos)
            )

            await self.populate.update_populated_fields(
                deployment_instance, docker_infos, file_infos
            )

            updated = await self.repository.update_one(id, update_deployment_instance)
            if not updated:
                return AppException.InternalServer(
                    FAILED_TO_UPDATE_DEPLOYMENT_INSTANCE, None
                ).json()

            return AppException.Created(
                deployment_instance_updated_successfully(id), updated
            ).json()

        except ExceptionCase as e:
            return e.json()
        except Exception as e:
            return AppException.InternalServer(
                "An unexpected error occurred", {"error": str(e)}
            ).json()

    async def deleteProject(self, id: str):
        try:
            deployment_instance = await self.repository.get_one(id)

            PopulatedFieldDeleted = await self.populate.delete_populated_fields(
                deployment_instance
            )

            if not PopulatedFieldDeleted:
                return AppException.InternalServer(
                    FAILED_TO_DELETE_DEPLOYMENT_INSTANCE, None
                ).json()

            Deleted = await self.repository.delete_one(id)
            if not Deleted:
                return AppException.InternalServer(
                    FAILED_TO_DELETE_DEPLOYMENT_INSTANCE, None
                ).json()

            return AppException.StatusOK(
                deployment_instance_deleted_successfully(id), None
            ).json()
        except ExceptionCase as e:
            return e.json()
        except Exception as e:
            return AppException.InternalServer(
                "An unexpected error occurred", {"error": str(e)}
            ).json()
