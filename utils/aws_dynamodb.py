import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from utils.aws_s3 import s3_logger
from backend.settings import (
    AWS_REGION,
    AWS_DYNAMODB_ACCESS_KEY_ID,
    AWS_DYNAMODB_SECRET_ACCESS_KEY
)

class DynResource:

    def __init__(self, dyn_resource=None):
        if not dyn_resource:
            dyn_resource = boto3.resource('dynamodb', aws_access_key_id=AWS_DYNAMODB_ACCESS_KEY_ID, aws_secret_access_key=AWS_DYNAMODB_SECRET_ACCESS_KEY, region_name=AWS_REGION)
        self.dyn_resource = dyn_resource
        self.region = self.dyn_resource.meta.client.meta.region_name
    
    def list_tables(self):
        """
        Lists the Amazon DynamoDB tables for the current account.

        :return: The list of tables.
        """
        try:
            tables = []
            for table in self.dyn_resource.tables.all():
                table.append(tables)
        except ClientError as err:
            s3_logger.error(
                "Couldn't list tables. Here's why: %s: %s" % (
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                )
            )
            raise err
        else:
            return tables

Dyn_resource = DynResource()
dyn_resource = Dyn_resource.dyn_resource

# Table
class DynTable:

    def __init__(self, table_name, schema):
        super().__init__()
        self.table_name = table_name
        self.table = dyn_resource.Table(table_name)
        self.schema = schema

    def exists_table(self):
        """
        Determines whether a table exists.

        :return: True when the table exists; otherwise, False.
        """
        try:
            self.table.load()
            exists = True
        except ClientError as err:
            if err.response["Error"]["Code"] == "ResourceNotFoundException":
                exists = False
            else:
                s3_logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s" % (
                    self.table_name,
                    err.response["Error"]["Code"],
                    err.response["Error"]["Message"],
                    )
                )
                raise err
        return exists

    
    def create_table(self):
        f"""
        Creates an Amazon DynamoDB table.
        """
        try:
            self.table = dyn_resource.create_table(**self.schema)
            self.table.wait_until_exists()
        except ClientError as err:
            s3_logger.error(
                "Couldn't create table %s. Here's why: %s: %s" % (
                    self.table_name, 
                    err.response["Error"]["Code"], 
                    err.response["Error"]["Message"]
                    )
                )
            raise err
        else:
            return self.table
    
    
    def delete_table(self):
        """
        Deletes the table.
        """
        try:
            self.table.delete()
            self.table.wait_until_not_exists()
            self.table = None
        except ClientError as err:
            s3_logger.error(
                "Couldn't delete table %s. Here's why: %s: %s" % (
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

    
    def exists_item(self, **kwargs):
        """
        Determines whether an item exists in the table.
        
        :param **kwargs: The attributes of the Item.
        :return: True when the Item exists; otherwise, False.
        """
        try:
            items = self.scan(**kwargs)
            if len(items):
                return items[0]
            else:
                return None
        except Exception as err:
            raise err
    
    def put_item(self, **kwargs):
        """
        Creates a new item, or replaces an old item with a new item. 
        If an item that has the same primary key as the new item already exists in the specified table, 
        the new item completely replaces the existing item. 
        You can perform a conditional put operation (add a new item if one with the specified primary key doesn't exist), 
        or replace an existing item if it has certain attribute values. 
        You can return the item's attribute values in the same operation, using the ReturnValues parameter.

        When you add an item, the primary key attributes are the only required attributes.

        :param **kwargs: The Key-Value pairs to be added to the table.
        """
        try:
            kwargs["CreatedOn"] = str(datetime.timestamp(datetime.now()))
            kwargs["UpdatedOn"] = str(datetime.timestamp(datetime.now()))
            response = self.table.put_item(
                Item=kwargs,
            )
        except ClientError as err:
            s3_logger.error(
                "Couldn't put item %s to table %s. Here's why: %s: %s" % (
                kwargs,
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return response.get("Attributes", None)

    
    def get_item(self, **kwargs):
        """
        The GetItem operation returns a set of attributes for the item with the given primary key. 
        If there is no matching item, GetItem does not return any data and there will be no Item element in the response.

        :param **kwargs: The Key attributes of the table.
        :return: The data about.
        """
        try:
            expression = {f"{k}": v for k, v in kwargs.items()}
            response = self.table.get_item(
                Key=expression
            )
        except ClientError as err:
            s3_logger.error(
                "Couldn't get item %s from table %s. Here's why: %s: %s" % (
                kwargs,
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return response.get("Item", None)

    
    def query(self, limit=None, scan_index_forward=True, condition_op='and', comparison_op='=', **kwargs):
        """
        A Query operation always returns a result set. 
        If no matching items are found, the result set will be empty. Queries that do not return results consume the minimum number of read capacity units for that type of read operation.
        Query results are always sorted by the sort key value. 
        If the data type of the sort key is Number, the results are returned in numeric order; otherwise, the results are returned in order of UTF-8 bytes. By default, the sort order is ascending. To reverse the order, set the ScanIndexForward parameter to false.
        
        You must provide the name of the partition key attribute and a single value for that attribute.
        Query returns all items with that partition key value. 
        Optionally, you can provide a sort key attribute and use a comparison operator to refine the search results.
        :param limit: The maximum number of items to evaluate (not necessarily the number of matching items).
        :param scan_index_forward: Specifies the order for index traversal: If true (default), the traversal is performed in ascending order; if false, the traversal is performed in descending order.
        :param condition_op: The Key Attributes of the table.
        :param **kwargs: The Key Attributes of the table.
        """
        try:
            if comparison_op == "contains":
                key_condition_expression = f" {condition_op} ".join([f"{comparison_op}({k}, :{k})" for k in kwargs.keys()])
            else:
                key_condition_expression = f" {condition_op} ".join([f"({k} = :{k})" for k in kwargs.keys()])
            expression_values = {f":{k}": v for k, v in kwargs.items()}
            if not limit:
                response = self.table.query(
                    ScanIndexForward=scan_index_forward,
                    KeyConditionExpression=key_condition_expression,
                    ExpressionAttributeValues=expression_values
                )
            else:
                response = self.table.query(
                    Limit=limit,
                    ScanIndexForward=scan_index_forward,
                    KeyConditionExpression=key_condition_expression,
                    ExpressionAttributeValues=expression_values
                ) 
        except ClientError as err:
            s3_logger.error(
                "Couldn't query item %s from table %s. Here's why: %s: %s" % (
                kwargs,
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return response['Items']

    
    def scan(self, limit=None, condition_op='and', comparison_op='=', **kwargs):
        """
        The Scan operation returns one or more items and item attributes by accessing every item in a table or a secondary index.
        
        :param limit: The maximum number of items to evaluate (not necessarily the number of matching items).
        :param condition_op: The Key Attributes of the table.
        :param **kwargs: The Key Attributes of the table.
        """
        try:
            if comparison_op == 'contains':
                filter_expression = f" {condition_op} ".join([f"{comparison_op}({k}, :{k})" for k in kwargs.keys()])
            else:
                filter_expression = f" {condition_op} ".join([f"({k} = :{k})" for k in kwargs.keys()])
            expression_values = {f":{k}": v for k, v in kwargs.items()}
            if limit:
                response = self.table.scan(
                    Limit=limit,
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values
                ) 
            else:
                response = self.table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values
                ) 
        except ClientError as err:
            s3_logger.error(
                "Couldn't scan item %s from table %s. Here's why: %s: %s" % (
                kwargs,
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return response['Items']

    
    def update_item(self, keys:dict, **kwargs):
        """
        Edits an existing item's attributes, or adds a new item to the table if it does not already exist. 
        You can put, delete, or add attribute values. 
        You can also perform a conditional update on an existing item (insert a new attribute name-value pair if it doesn't exist, 
        or replace an existing name-value pair if it has certain expected attribute values).
        
        For the primary key, you must provide all of the attributes.
        :param keys: Key Attributes of the table.
        :param **kwargs: Attributes of the table.
        :return: The fields that were updated, with their new values.
        """
        try:
            update_expression = "SET " + ', '.join(f"{k}=:{k}" for k in kwargs.keys()) + ", UpdatedOn=:UpdatedOn"
            expression_values = {f":{k}": v for k, v in kwargs.items()}
            expression_values[":UpdatedOn"] = str(datetime.timestamp(datetime.now()))
            response = self.table.update_item(
                Key=keys,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
        except ClientError as err:
            s3_logger.error(
                "Couldn't update item %s in table %s. Here's why: %s: %s" % (
                kwargs,
                self.table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            print(err)
            raise
        else:
            return response.get("Attributes", None)

    
    def delete_item(self, **kwargs):
        """
        Deletes the specific.

        :param **kwargs: The key attributes of the table to delete.
        """
        try:
            expression = {f"{k}": v for k, v in kwargs.items()}
            self.table.delete_item(
                Key=expression
            )
        except ClientError as err:
            s3_logger.error(
                "Couldn't delete item %s. Here's why: %s: %s" % (
                kwargs,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
    
    
    def get_all(self):
        """
        Get All items from table.
        """
        try:
            response = self.table.scan()
            items = response['Items']
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                items.extend(response['Items'])
        except ClientError as err:
            s3_logger.error(
                "Couldn't get all items. Here's why: %s: %s" % (
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return items