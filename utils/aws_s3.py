import boto3
from botocore.exceptions import ClientError
import logging
import os
# from aws_logging_handlers.S3 import S3Handler
from backend.settings import (
    AWS_REGION,
    AWS_DYNAMODB_ACCESS_KEY_ID,
    AWS_DYNAMODB_SECRET_ACCESS_KEY,
    S3_BUCKET_NAME,
    LOG_FILE_PATH,
)

class S3Logger:

    def __init__(self, bucket_name) -> None:
        s3_resource = boto3.resource('s3', aws_access_key_id=AWS_DYNAMODB_ACCESS_KEY_ID, aws_secret_access_key=AWS_DYNAMODB_SECRET_ACCESS_KEY, region_name=AWS_REGION)
        bucket = s3_resource.Bucket(bucket_name)
        try:
            bucket.meta.client.head_bucket(Bucket=bucket.name)
        except ClientError as err:
            bucket.create(CreateBucketConfiguration={"LocationConstraint": s3_resource.meta.client.meta.region_name})
            bucket.wait_until_exists()
        self.filename = f'{bucket_name}.log'
        self.path = LOG_FILE_PATH
        self.filepath = os.path.join(self.path, self.filename)
        logging.basicConfig(filename=f'logs/{self.filename}', format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.s3_obj = bucket.Object(f"logs/{self.filename}")
        try:
            self.s3_obj.load()
        except ClientError:
            self.upload_to_s3_obj()

    def upload_to_s3_obj(self):
        if os.path.isfile(self.filepath):
            try:
                put_data = open(self.filepath, "rb")
                self.s3_obj.put(Body=put_data)
            except IOError as err:
                self.exception("Expected file name, got '%s'." % self.filepath)
                raise err            

    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def warn(self, message: str):
        self.logger.warn(message)
    
    def critical(self, message: str):
        self.logger.critical(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def exception(self, message: str):
        self.logger.exception(message)

s3_logger = S3Logger("api.localgovai.uk")

class S3Resource:
    
    def __init__(self, s3_resource=None):
        if not s3_resource:
            s3_resource = boto3.resource('s3', aws_access_key_id=AWS_DYNAMODB_ACCESS_KEY_ID, aws_secret_access_key=AWS_DYNAMODB_SECRET_ACCESS_KEY, region_name=AWS_REGION)
        self.s3_resource = s3_resource
        self.region = s3_resource.meta.client.meta.region_name
    
    def list_buckets(self):
        """
        Get the buckets in all Regions for the current account.

        :return: The list of buckets.
        """
        try:
            buckets = []
            for bucket in self.s3_resource.buckets.all():
                buckets.append(bucket)
            s3_logger.info("Got buckets: %d." % len(buckets))
            return buckets
        except ClientError as err:
            s3_logger.exception(
                "Couldn't get buckets.\nHere's why: %s: %s" % (
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

S3_resource = S3Resource()
s3_resource = S3_resource.s3_resource

class S3Bucket:
    """Encapsulates S3 bucket actions."""

    def __init__(self, s3_bucket_name=None):
        """
        :param bucket: A Boto3 Bucket resource. This is a high-level resource in Boto3
                       that wraps bucket actions in a class-like structure.
        """
        if not s3_bucket_name:
            s3_bucket_name = S3_BUCKET_NAME
        self.name = s3_bucket_name
        self.bucket = s3_resource.Bucket(s3_bucket_name)
    
    def exists(self):
        """
        Determine whether the bucket exists and you have access to it.

        :return: True when the bucket exists; otherwise, False.
        """
        try:
            self.bucket.meta.client.head_bucket(Bucket=self.bucket.name)
            s3_logger.info("Bucket %s exists." % self.bucket.name)
            exists = True
        except ClientError as err:
            s3_logger.exception(
                "Bucket %s doesn't exist or you don't have access to it.\nHere's why: %s: %s" % (
                self.bucket.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            exists = False
        return exists

    def create(self, region_override=None):
        """
        Create an Amazon S3 bucket in the default Region for the account or in the
        specified Region.

        :param region_override: The Region in which to create the bucket. If this is
                                not specified, the Region configured in your shared
                                credentials is used.
        """
        if region_override is not None:
            region = region_override
        else:
            region = self.bucket.meta.client.meta.region_name
        try:
            self.bucket.create(CreateBucketConfiguration={"LocationConstraint": region})
            self.bucket.wait_until_exists()
            s3_logger.info("Created bucket %s in region=%s" % (self.bucket.name, region))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't create bucket named %s in region=%s.\nHere's why: %s: %s" % (
                self.bucket.name,
                region,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
    
    def delete(self):
        """
        Delete the bucket. The bucket must be empty or an error is raised.
        """
        try:
            self.bucket.delete()
            self.bucket.wait_until_not_exists()
            s3_logger.info("Bucket %s successfully deleted." % (self.bucket.name))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't delete bucket %s.\nHere's why: %s: %s" % (
                self.bucket.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
    
    def delete_objects(self, object_keys):
        """
        Removes a list of objects from a bucket.
        This operation is done as a batch in a single request.

        :param object_keys: The list of keys that identify the objects to remove.
        :return: The response that contains data about which objects were deleted
                 and any that could not be deleted.
        """
        try:
            response = self.bucket.delete_objects(
                Delete={"Objects": [{"Key": key} for key in object_keys]}
            )
            if "Deleted" in response:
                s3_logger.info(
                    "Deleted objects '%s' from bucket '%s'." % (
                    [del_obj["Key"] for del_obj in response["Deleted"]],
                    self.bucket.name,
                ))
            if "Errors" in response:
                s3_logger.warning(
                    "Could not delete objects '%s' from bucket '%s'.",
                    [
                        f"{del_obj['Key']}: {del_obj['Code']}"
                        for del_obj in response["Errors"]
                    ],
                    self.bucket.name,
                )
        except ClientError as err:
            s3_logger.exception(
                "Couldn't delete any objects from bucket %s.\nHere's why: %s: %s" % (
                self.bucket.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return response
        
    def empty_bucket(self):
        """
        Remove all objects from a bucket.

        :param bucket: The bucket to empty. This is a Boto3 Bucket resource.
        """
        try:
            self.bucket.objects.delete()
            s3_logger.info("Emptied bucket '%s'." % self.bucket.name)
        except ClientError as err:
            s3_logger.exception(
                "Couldn't empty bucket '%s'.\nHere's why: %s: %s" % (
                self.bucket.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

    def list_objects(self, prefix=None):
        """
        Lists the objects in a bucket, optionally filtered by a prefix.

        :param bucket: The bucket to query. This is a Boto3 Bucket resource.
        :param prefix: When specified, only objects that start with this prefix are listed.
        :return: The list of objects.
        """
        try:
            if not prefix:
                objects = list(self.bucket.objects.all())
            else:
                objects = list(self.bucket.objects.filter(Prefix=prefix))
            s3_logger.info(
                "Got objects %s from bucket '%s'" % ([o.key for o in objects], self.bucket.name
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't get objects for bucket '%s'.\nHere's why: %s: %s" % (
                self.bucket.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

class S3Object:
    """Encapsulates S3 object actions."""

    def __init__(self, s3_object_key, s3_bucket_name=None):
        """
        :param s3_object: A Boto3 Object resource. This is a high-level resource in Boto3
                          that wraps object actions in a class-like structure.
        """
        self.bucket = S3Bucket(s3_bucket_name)
        self.key = s3_object_key
        self.object = self.bucket.bucket.Object(s3_object_key)

    def exists(self):
        """
        Determine whether the object exists and you have access to it.

        :return: True when the object exists; otherwise, False.
        """
        try:
            self.object.load()
            exists = True
        except ClientError as err:
            s3_logger.exception(
                "Object %s doesn't exist or you don't have access to it.\nHere's why: %s: %s" % (
                self.object.key,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            exists = False
        return exists

    def copy_to(self, dest_bucket_name, dest_object_key):
        """
        Copies the object to another bucket.

        :param dest_object: The destination object initialized with a bucket and key.
                            This is a Boto3 Object resource.
        """
        try:
            dest_object = s3_resource.Bucket(dest_bucket_name).Object(dest_object_key)
            dest_object.copy_from(
                CopySource={"Bucket": self.object.bucket_name, "Key": self.object.key}
            )
            dest_object.wait_until_exists()
            s3_logger.info(
                "Copied object from %s:%s to %s:%s." % (
                self.object.bucket_name,
                self.object.key,
                dest_object.bucket_name,
                dest_object.key,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't copy object from %s/%s to %s/%s.\nHere's why: %s: %s" % (
                self.object.bucket_name,
                self.object.key,
                dest_object.bucket_name,
                dest_object.key,
                self.object.bucket_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

    def copy_from(self, src_bucket_name, src_object_key):
        """
        Copies the object to another bucket.

        :param src_object: The source object initialized with a bucket and key.
                            This is a Boto3 Object resource.
        """
        try:
            self.object.copy_from(
                CopySource={"Bucket": src_bucket_name, "Key": src_object_key}
            )
            self.object.wait_until_exists()
            s3_logger.info(
                "Copied object from %s:%s to %s:%s." % (
                src_bucket_name,
                src_object_key,
                src_bucket_name,
                src_object_key,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't copy object from %s/%s to %s/%s.\nHere's why: %s: %s" % (
                src_bucket_name,
                src_object_key,
                src_bucket_name,
                src_object_key,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

    def delete(self):
        """
        Deletes the object.
        """
        try:
            self.object.delete()
            self.object.wait_until_not_exists()
            s3_logger.info(
                "Deleted object '%s' from bucket '%s'." % (
                self.object.key,
                self.object.bucket_name,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't delete object %s from bucket %s.\nHere's why: %s: %s" % (
                self.object.key,
                self.object.bucket_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
    
    def put(self, data):
        """
        Upload data to the object.

        :param data: The data to upload. This can either be bytes or a string. When this
                     argument is a string, it is interpreted as a file name, which is
                     opened in read bytes mode.
        """
        put_data = data
        if isinstance(data, str):   # file name
            try:
                put_data = open(data, "rb")
            except IOError as err:
                s3_logger.exception("Expected file name or binary data, got '%s'." % data)
                raise err
        try:
            self.object.put(Body=put_data)
            self.object.wait_until_exists()
            s3_logger.info(
                "Put object '%s' to bucket '%s'." % (
                self.object.key,
                self.object.bucket_name,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't put object '%s' to bucket '%s'.\nHere's why: %s: %s" % (
                self.object.key,
                self.object.bucket_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        finally:
            if getattr(put_data, "close", None):
                put_data.close()

    def get(self):
        """
        Gets the object.

        :return: The object data in bytes.
        """
        try:
            body = self.object.get()["Body"].read()
            s3_logger.info(
                "Got object '%s' from bucket '%s'." % (
                self.object.key,
                self.object.bucket_name,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't get object '%s' from bucket '%s'.\nHere's why: %s: %s" % (
                self.object.key,
                self.object.bucket_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return body
    
    def get_available_subresources(self):
        """
        Returns a list of all the available sub-resources for this Resource.

        :return: A list containing the name of each sub-resource for this resource
        """
        try:
            sub_resources = self.object.get_available_subresources()
            s3_logger.info(
                "Got available sub-resources '%s' from bucket '%s'." % (
                self.object.key,
                self.object.bucket_name,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't get available sub-resources '%s' from bucket '%s'.\nHere's why: %s: %s" % (
                self.object.key,
                self.object.bucket_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return sub_resources

    def download_file(self, to_path):
        """
        Download an S3 object to a file.

        :param to_path: The path to the file to download to.
        """
        try:
            self.object.download_file(to_path)
            s3_logger.info(
                "Download Object '%s' to a file '%s'." % (
                self.object.key,
                to_path,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't download object '%s' from bucket '%s' to a file '%s'.\nHere's why: %s: %s" % (
                self.object.key,
                self.object.bucket_name,
                to_path,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

    def upload_file(self, file_path):
        """
        Upload a file to an S3 object.

        :param file_path: The path to the file to upload.
        """
        try:
            self.object.upload_file(file_path)
            self.object.wait_until_exists()
            s3_logger.info(
                "Upload a file '%s' to Object '%s'." % (
                file_path,
                self.object.key,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't upload a file '%s' to object '%s' of bucket '%s'.\nHere's why: %s: %s" % (
                file_path,
                self.object.key,
                self.object.bucket_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

    def download_fileobj(self, to_fileobj, to_path):
        """
        Download this object from S3 to a file-like object.
        The file-like object must be in binary mode.
        This is a managed transfer which will perform a multipart download in multiple threads if necessary.

        :param to_fileobj: A file-like object to download into. At a minimum, it must implement the write method and must accept bytes.
        :param to_path: The path to the file to download to.
        """
        try:
            with open(to_path, 'wb') as data:
                self.object.download_fileobj(data)
            s3_logger.info(
                "Download Object '%s' to a file '%s'." % (
                self.object.key,
                to_path,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't download object '%s' from bucket '%s' to a file '%s'.\nHere's why: %s: %s" % (
                self.object.key,
                self.object.bucket_name,
                to_path,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

    def upload_fileobj(self, file_path):
        """
        Upload a file-like object to this object.
        The file-like object must be in binary mode.
        This is a managed transfer which will perform a multipart upload in multiple threads if necessary.

        :param file_path: The path to the file to upload.
        """
        try:
            with open(file_path, 'rb') as data:
                self.object.upload_fileobj(data)
            self.object.wait_until_exists()
            s3_logger.info(
                "Upload a file '%s' to Object '%s'." % (
                file_path,
                self.object.key,
            ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't upload a file '%s' to object '%s' of bucket '%s'.\nHere's why: %s: %s" % (
                file_path,
                self.object.key,
                self.object.bucket_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err

    def get_object_url(self):
        return f"https://s3.{self.bucket.bucket.meta.client.meta.region_name}.amazonaws.com/{self.bucket.name}/{self.key}"