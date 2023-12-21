import os
from datetime import datetime
import uuid
import shutil
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from utils.aws_s3 import (
    S3Object
)
from .schemas import (
    KNOWLEDGE_BASE_TABLE_SCHEMA,
    KNOWLEDGE_BASE_QUESTION_TABLE_SCHEMA,
)
from backend.settings import (
    MEDIA_KNOWLEDGE_BASE
)
from utils.aws_dynamodb import DynTable

# Create your models here.
# KnowledgeBase Table
class KnowledgeBaseModel(DynTable):

    def __init__(self):
        super().__init__(table_name="KnowledgeBase", schema=KNOWLEDGE_BASE_TABLE_SCHEMA)

    def put_item(self, files=[], **kwargs):
        if kwargs.get("KnowledgeBaseID", "") == "":
            kwargs["KnowledgeBaseID"] = uuid.uuid4().hex
        # Upload Files
        # knowledge_base_dir = os.path.join(MEDIA_KNOWLEDGE_BASE, kwargs["KnowledgeBaseID"])
        # if os.path.exists(knowledge_base_dir):
        #     print("Knowledge Base folder is not empty")
        #     shutil.rmtree(knowledge_base_dir)
        # os.mkdir(knowledge_base_dir)
        # for file in files:
        #     file_path = os.path.join(knowledge_base_dir, file.name)
        #     with open(file_path, "wb") as f:
        #         f.write(file.read())
        # kwargs["KnowledgeFiles"] = knowledge_base_dir 
        super().put_item(**kwargs)
        return kwargs["KnowledgeBaseID"]

    def delete_item(self, **kwargs):
        # knowledge_base_dir = self.get_item(**kwargs)["KnowledgeFiles"]
        # if os.path.exists(knowledge_base_dir):
        #     shutil.rmtree(knowledge_base_dir)
        super().delete_item(**kwargs)

# KnowledgeBaseQuestion Table
class KnowledgeBaseQuestionModel(DynTable):

    def __init__(self):
        super().__init__(table_name="KnowledgeBaseQuestion", schema=KNOWLEDGE_BASE_QUESTION_TABLE_SCHEMA)
    
    def put_item(self, **kwargs):
        if kwargs.get("KnowledgeBaseQuestionID", "") == "":
            kwargs["KnowledgeBaseQuestionID"] = uuid.uuid4().hex
        super().put_item(**kwargs)
        return kwargs["KnowledgeBaseQuestionID"]

KnowledgeBase = KnowledgeBaseModel()
KnowledgeBaseQuestion = KnowledgeBaseQuestionModel()