import uuid
import bcrypt
from utils.aws_dynamodb import (
    DynTable
)
from .schemas import (
    USERS_TABLE_SCHEMA,
    GLOBAL_ADMINS_TABLE_SCHEMA,
    ORGANIZATIONS_TABLE_SCHEMA
)

# Users Table
class UserModel(DynTable):

    def __init__(self):
        super().__init__(table_name="Users", schema=USERS_TABLE_SCHEMA)
    
    def put_item(self, **kwargs):
        if kwargs.get("UserID", "") == "":
            kwargs["UserID"] = uuid.uuid4().hex
        if kwargs.get("Password", "") != "":
            kwargs["Password"] = bcrypt.hashpw(kwargs["Password"].encode('utf-8'), bcrypt.gensalt()).decode()
        super().put_item(**kwargs)
        return kwargs["UserID"]
    
    def update_item(self, keys:dict, **kwargs):
        if kwargs.get("Password", "") != "":
            kwargs["Password"] = bcrypt.hashpw(kwargs["Password"].encode('utf-8'), bcrypt.gensalt()).decode()
        super().update_item(keys, **kwargs)
    
    def search(self, who: str):
        users = User.scan(
            UserID=who
        )
        if len(users):
            return users
        users = User.scan(
            Email=who
        )
        if len(users):
            return users
        users = User.scan(
            UserName=who
        )
        if len(users):
            return users
        users = User.scan(
            FirstName=who.split(" ")[0],
            LastName=who.split(" ")[-1]
        )
        if len(users):
            return users   
        return []     

    def authenticate(self, email, password):
        """
        Authenticate with Email and Password.

        :param email: The Email of the User.
        :param password: The Password of the User.
        :return: True when passed, otherwise, False.
        """
        try:
            user = self.exists_item(Email=email)
            if not user:
                raise Exception("Not registered yet")
            else:
                if bcrypt.checkpw(password.encode('utf-8'), user["Password"].encode('utf-8')):
                    return user
                else:
                    raise Exception("Incorrect password")
        except Exception as err:
            raise err

# Organizations Table
class OrgModel(DynTable):

    def __init__(self):
        super().__init__(table_name="Organizations", schema=ORGANIZATIONS_TABLE_SCHEMA)
    
    def put_item(self, **kwargs):
        if kwargs.get("OrgID", "") == "":
            kwargs["OrgID"] = uuid.uuid4().hex
        if kwargs.get("InstanceType", "") == "":
            kwargs["InstanceType"] = "gov"
        super().put_item(**kwargs)
        return kwargs["OrgID"]

User = UserModel()
Org = OrgModel()