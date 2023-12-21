from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError, ValidationError
from datetime import datetime
import uuid
from utils.aws_dynamodb import DynTable
from utils.aws_s3 import (
    S3Bucket,
    s3_logger
)
from .schemas import (
    ROLES_TABLE_SCHEMA,
    TEAMS_TABLE_SCHEMA,
    TEAM_MEMBERS_TABLE_SCHEMA,
)

# Roles Table
class RoleModel(DynTable):

    def __init__(self):
        super().__init__(table_name="Roles", schema=ROLES_TABLE_SCHEMA)
    
    def put_item(self, **kwargs):
        if kwargs.get("RoleID", "") == "":
            kwargs["RoleID"] = uuid.uuid4().hex
        super().put_item(**kwargs)
        return kwargs["RoleID"]

# Teams Table
class TeamModel(DynTable):
    def __init__(self):
        super().__init__(table_name="Teams", schema=TEAMS_TABLE_SCHEMA)

    def put_item(self, **kwargs):
        if kwargs.get("TeamID", "") == "":
            kwargs["TeamID"] = uuid.uuid4().hex
        super().put_item(**kwargs)
        return kwargs["TeamID"]        

# TeamMembers Table
class TeamMemberModel(DynTable):

    def __init__(self):
        super().__init__(table_name="TeamMembers", schema=TEAM_MEMBERS_TABLE_SCHEMA)

    def put_item(self, **kwargs):
        if kwargs.get("TeamMemberID", "") == "":
            kwargs["TeamMemberID"] = uuid.uuid4().hex
        super().put_item(**kwargs)
        return kwargs["TeamMemberID"]
    
Role = RoleModel()
Team = TeamModel()
TeamMember = TeamMemberModel()