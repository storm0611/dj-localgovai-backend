import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.aws_s3 import s3_logger
from backend.settings import (
    AWS_REGION,
    AWS_SES_ACCESS_KEY_ID,
    AWS_SES_SECRET_ACCESS_KEY,
    CHARSET
)

class SesClient:
    """Encapsulates actions with Amazon SES."""

    def __init__(self, ses_client=None):
        """
        :param ses_client: A Boto3 Amazon SES client.
        """
        if not ses_client:
            ses_client = boto3.client('ses', aws_access_key_id=AWS_SES_ACCESS_KEY_ID, aws_secret_access_key=AWS_SES_SECRET_ACCESS_KEY, region_name=AWS_REGION)
        self.ses_client = ses_client


    def send_raw_email(self, source, destination, subject, content):
        """
        Sends an raw email.

        Note: If your account is in the Amazon SES  sandbox, the source and
        destination email accounts must both be verified.

        :param source: The source email account.
        :param destination: The destination email account.
        :param subject: The subject of the email.
        :param content: The plain text version of the body of the email.
        :return: The ID of the message, assigned by Amazon SES.
        """
        # Create a multipart/mixed parent container.
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = source
        msg['To'] = destination
        msg_body = MIMEMultipart('alternative')
        textpart = MIMEText(content.encode(CHARSET), 'plain', CHARSET)
        msg_body.attach(textpart)
        msg.attach(msg_body)
        send_args = {
            "Source": source,
            "Destinations": [
                destination
            ],
            "RawMessage": {
                'Data': msg.as_string(),
            }
        }
        try:
            response = self.ses_client.send_raw_email(**send_args)
            message_id = response["MessageId"]
            s3_logger.info(
                "Sent raw mail %s from %s to %s." % (
                    message_id, 
                    source, 
                    destination
                ))
        except ClientError as err:
            s3_logger.exception(
                "Couldn't send raw mail from %s to %s.\nHere's why: %s: %s" % ( 
                source, 
                destination,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            ))
            raise err
        else:
            return response['MessageId']        
        
ses_client = SesClient()