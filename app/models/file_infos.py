from beanie import Document


class FileInfos(Document):
    zip_file_weight: str
    file_weight: str
    zip_file_path: str
    decompressed_file_path: str

    class Settings:
        name = "FileInfos"
