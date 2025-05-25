from beanie import PydanticObjectId

from app.models.deployment_instance import DeploymentInstance
from app.packages.common.http_exceptions_handling import AppException, ExceptionCase
from app.packages.common.populate_service.docker_info_service import DockerInfoService
from app.packages.common.populate_service.file_info_service import FileInfoService
from app.packages.constant.response_messages import (
    DOCKER_INFO_NOT_FOUND,
    FAILED_TO_ADD_DOCKER_INFO,
    FAILED_TO_ADD_FILE_INFO,
    FAILED_TO_DELETE_DOCKER_INFO,
    FAILED_TO_DELETE_FILE_INFO,
    FAILED_TO_UPDATE_DOCKER_INFO,
    FAILED_TO_UPDATE_FILE_INFO,
    FILE_INFO_NOT_FOUND,
)
from app.packages.helpers.build_functions_responses import beanie_document_to_dict


class PopulateService:
    def __init__(self):
        self.DockerInfoService = DockerInfoService()
        self.FilesInfoService = FileInfoService()

    async def create_populated_fields(
        self,
        deployment_instance: DeploymentInstance,
        docker_info: dict,
        file_info: dict,
    ):
        try:

            created_docker_infos = await self.DockerInfoService.add_docker_info(
                docker_info
            )
            if not created_docker_infos:
                return AppException.InternalServer(
                    FAILED_TO_ADD_DOCKER_INFO, None
                ).json()

            created_file_infos = await self.FilesInfoService.add_file_infos(file_info)
            if not created_file_infos:
                return AppException.InternalServer(FAILED_TO_ADD_FILE_INFO, None).json()

            deployment_instance.file_infos = PydanticObjectId(created_file_infos["id"])
            deployment_instance.docker_infos = PydanticObjectId(
                created_docker_infos["id"]
            )
            return beanie_document_to_dict(deployment_instance)
        except ExceptionCase as e:
            return e.json()

        except Exception as e:
            return AppException.InternalServer(
                "An unexpected error occurred", {"error": str(e)}
            ).json()

    async def get_populated_fields(self, deployment_instance: DeploymentInstance):
        try:

            file_infos = await self.FilesInfoService.get_file_infos(
                deployment_instance.file_infos
            )
            if not file_infos:
                return AppException.NotFound(FILE_INFO_NOT_FOUND, None).json()

            docker_infos = await self.DockerInfoService.get_docker_info(
                deployment_instance.docker_infos
            )
            if not docker_infos:
                return AppException.NotFound(DOCKER_INFO_NOT_FOUND, None).json()

            deployment_instance.file_infos = beanie_document_to_dict(file_infos)
            deployment_instance.docker_infos = beanie_document_to_dict(docker_infos)

            return beanie_document_to_dict(deployment_instance)

        except ExceptionCase as e:
            return e.json()
        except Exception as e:
            return AppException.InternalServer(
                "An unexpected error occurred", {"error": str(e)}
            ).json()

    async def update_populated_fields(
        self,
        deployment_instance: DeploymentInstance,
        update_docker_infos_data: dict,
        update_file_infos_data: dict,
    ):
        try:

            updated_docker_infos = await self.DockerInfoService.update_docker_info(
                str(deployment_instance.docker_infos), update_docker_infos_data
            )

            if not updated_docker_infos:
                return AppException.InternalServer(FAILED_TO_UPDATE_DOCKER_INFO, None)

            updated_file_infos = await self.FilesInfoService.update_file_infos(
                str(deployment_instance.file_infos), update_file_infos_data
            )

            if not updated_file_infos:
                return AppException.InternalServer(FAILED_TO_UPDATE_FILE_INFO, None)

            return deployment_instance
        except ExceptionCase as e:
            return e
        except Exception as e:
            return AppException.InternalServer("populate_service", {"error": str(e)})

    async def delete_populated_fields(self, deployment_instance: DeploymentInstance):

        try:
            DockerInfoDeleted = await self.DockerInfoService.delete_docker_infos(
                str(deployment_instance.docker_infos)
            )

            if not DockerInfoDeleted:
                return AppException.InternalServer(FAILED_TO_DELETE_DOCKER_INFO, None)

            FileInfoDeleted = await self.FilesInfoService.delete_file_infos(
                str(deployment_instance.file_infos)
            )

            if not FileInfoDeleted:
                return AppException.InternalServer(FAILED_TO_DELETE_FILE_INFO, None)
            return True

        except ExceptionCase as e:
            return e.json()
        except Exception as e:
            return AppException.InternalServer("populate_service", {"error": str(e)})
