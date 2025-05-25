from fastapi import APIRouter

from app.services.deployment_service import DeploymentService

router = APIRouter(
    prefix="/project",
    responses={
        500: {"description": "Internal Server Error"},
        200: {"description": "Status Ok"},
    },
)


@router.post("/")
async def deploy_project(
    body: dict,
):
    return await DeploymentService().deployProject(body)


@router.put("/{id}")
async def update_project(id: str, data: dict):
    return await DeploymentService().updateProject(id, data)


@router.get("/{id}")
async def get_project(id: str):
    return await DeploymentService().getProject(id)


@router.delete("/{id}")
async def delete_project(id: str):
    return await DeploymentService().deleteProject(id)
