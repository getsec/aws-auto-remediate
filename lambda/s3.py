import boto3
import json
import logging
from os import environ
logger = logging.getLogger()
logger.setLevel(logging.INFO)

WHITELIST = environ.get("S3_WHITELIST")

def get_aws_account_id():
    sts = boto3.client("sts")
    user_arn = sts.get_caller_identity()["Arn"]
    return user_arn.split(":")[4]


def updated_policy(bucket, new_policy):
    """Replaces bucket policy with the new one
    
    Arguments:
        bucket {Str} -- name of the bucket
        new_policy {json.dumps(jsonobj)} -- json policy
    
    Returns:
        obj -- response
    """
    s3 = boto3.client('s3')
    response = s3.put_bucket_policy(
        Bucket=bucket,
        ConfirmRemoveSelfBucketAccess=True,
        Policy=json.dumps(new_policy)
    )
    return response

def updated_acl(bucket):
    s3 = boto3.client('s3')
    response = s3.put_bucket_acl(
        Bucket=bucket,
        ACL='private'
    )
    return response

def lambda_handler(event, context):
    bucket = event['detail']['requestParameters']['bucketName']

    # Try to see if bucket in whitelist
    if bucket in WHITELIST:
        return f"{bucket} found in whitelist: {WHITELIST} - Not running."

    if event['detail']['eventName'] == "PutBucketPolicy":
        new_policy = event['detail']['requestParameters']['bucketPolicy']
        new_principal = {"AWS": f"arn:aws:iam::{get_aws_account_id()}:root"}
        new_policy['Statement'][0]['Principal'] = new_principal
        out = updated_policy(bucket, new_policy)
        return out

    elif event['detail']['eventName']  == "PutBucketAcl":
        out = updated_acl(bucket)
        return out
    
    else:
        return None