from beanie import Document


class DockerInfo(Document):
    container_id: str
    base_image: str
    docker_composed: bool
    package_manager: str
    used_languages: list[str]

    class Settings:
        name = "DockerInfos"
