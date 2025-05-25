from beanie import PydanticObjectId


def user_id_not_found(id: int) -> str:
    return f"this user_id {id} is not found"


## Docker info :
FAILED_TO_ADD_DOCKER_INFO = "Failed to add docker informations"
DOCKER_INFO_NOT_FOUND = "Docker details not found"
FAILED_TO_DELETE_DOCKER_INFO = "Failed to delete docker informations"
FAILED_TO_UPDATE_DOCKER_INFO = "Failed to update docker informations"

## file info :
FAILED_TO_ADD_FILE_INFO = "Failed to add file informations"
FILE_INFO_NOT_FOUND = " file details not found"
FAILED_TO_DELETE_FILE_INFO = "Failed to delete file informations"
FAILED_TO_UPDATE_FILE_INFO = "Failed to update file informations"

##Deployment instances:
FAILED_TO_CREATE_DEPLOYEMENT_INSTANCE = "Failed to create deployment instance"
DEPLOYEMENT_INSTANCE_NOT_FOUND = "Deployement instance not found"
FAILED_TO_UPDATE_DEPLOYMENT_INSTANCE = "Failed to update the deployment instance"
FAILED_TO_DELETE_DEPLOYMENT_INSTANCE = "Failed to delete the deployemnt instance"


def deployment_instance_created_successfully(id: PydanticObjectId):
    return f"Deployment instance created successfully _id : {str(id)}"


def deployment_instance_deleted_successfully(id: PydanticObjectId):
    return f"Deployment instance deleted successfully _id : {str(id)}"


def deployment_instance_updated_successfully(id: str):
    return f"Deployment instance updated successfully _id : {str(id)}"
