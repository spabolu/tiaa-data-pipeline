import os
import boto3
from dotenv import load_dotenv

load_dotenv()

def get_s3():
    """
    Creates and returns a boto3 S3 client.
    """
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
    )
    return session.client('s3')
