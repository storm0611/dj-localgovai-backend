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
    CHANNELS_TABLE_SCHEMA,
    MESSAGES_TABLE_SCHEMA,
    LANGUAGE_SUPPORT_TABLE_SCHEMA
)

# Channels Table
class ChannelModel(DynTable):

    def __init__(self):
        super().__init__(table_name="Channels", schema=CHANNELS_TABLE_SCHEMA)
    
    def put_item(self, **kwargs):
        if kwargs.get("ChannelID", "") == "":
            kwargs["ChannelID"] = uuid.uuid4().hex
        kwargs["ChannelType"] = "Group" if len(kwargs["Members"]) >= 3 else "DM"
        kwargs["ChannelName"] = kwargs["ChannelName"] if kwargs.get("ChannelName", "") != "" else kwargs["ChannelID"]
        super().put_item(**kwargs)
        return kwargs["ChannelID"]

    def scan_contains_members(self, members: list):
        """
        The Scan Channel that contains members
        
        :param members: list of member id
        """
        try:
            filter_expression = f" and ".join([f"contains(Members, :Member{i})" for i in range(len(members))])
            expression_values = {f":Member{i}": members[i] for i in range(len(members))}
            response = self.table.scan(
                FilterExpression=filter_expression,
                ExpressionAttributeValues=expression_values
            ) 
        except ClientError as err:
            s3_logger.error(
                "Couldn't scan channels contains %s from table %s. Here's why: %s: %s" % (
                members,
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return response['Items']

# ChatMessages Table
class ChatMessageModel(DynTable):

    def __init__(self):
        super().__init__(table_name="ChatMessages", schema=MESSAGES_TABLE_SCHEMA)
    
    def put_item(self, **kwargs):
        if kwargs.get("MessageID", "") == "":
            kwargs["MessageID"] = str(datetime.now().timestamp())
        super().put_item(**kwargs)
        return kwargs["MessageID"]

# LanguageSupport Table
class LanguageSupportModel(DynTable):

    def __init__(self):
        super().__init__(table_name="LanguageSupport", schema=LANGUAGE_SUPPORT_TABLE_SCHEMA)
    
    def put_item(self, **kwargs):
        if kwargs.get("LanguageID", "") == "":
            kwargs["LanguageID"] = str(datetime.now().timestamp())
        super().put_item(**kwargs)
        return kwargs["LanguageID"]

Channel = ChannelModel()
ChatMessage = ChatMessageModel()
LanguageSupport = LanguageSupportModel()