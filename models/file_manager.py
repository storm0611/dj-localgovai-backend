import uuid
from utils.aws_dynamodb import DynTable
from utils.aws_s3 import S3Object
from .schemas import (
    RESOURCE_FOLDERS_TABLE_SCHEMA,
    RESOURCE_FILES_TABLE_SCHEMA
)

# ResourceFolders Table
class ResourceFolderModel(DynTable):

    def __init__(self):
        super().__init__(table_name="ResourceFolders", schema=RESOURCE_FOLDERS_TABLE_SCHEMA)

# ResourceFiles Table
class ResourceFileModel(DynTable):

    def __init__(self):
        super().__init__(table_name="ResourceFiles", schema=RESOURCE_FILES_TABLE_SCHEMA)

    def put_item(self, **kwargs):
        if kwargs.get("FileID", "") == "":
            kwargs["FileID"] = uuid.uuid4().hex
        super().put_item(**kwargs)
        return kwargs["FileID"]

ResourceFolder = ResourceFolderModel()
ResourceFile = ResourceFileModel()