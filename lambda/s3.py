import boto3
import json
import logging
from os import environ
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Whitelist that allows you to pick buckets you dont want to revoke public permissions
WHITELIST = environ.get("S3_WHITELIST")

def get_aws_account_id():
    """This just grabs the account ID so we can set a S3 bucket policy
    That is only owned by your account. Removing public, but not blocking access
    
    Returns:
        str -- The string of the account ID
    """
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
    """Sets a bucket ACL to private
    
    Arguments:
        bucket {str} -- the name of the bucket
    
    Returns:
        json -- response object
    """
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

    # if the event is putbucketpolicy
    if event['detail']['eventName'] == "PutBucketPolicy":
        # Get the policy
        new_policy = event['detail']['requestParameters']['bucketPolicy']
        
        # create new principal ID by getting the current account id
        new_principal = {"AWS": f"arn:aws:iam::{get_aws_account_id()}:root"}
        
        # Set the new principal to the new_principal json
        new_policy['Statement'][0]['Principal'] = new_principal

        # update the policy
        out = updated_policy(bucket, new_policy)
        return out

    # if the event is putbucketacl
    elif event['detail']['eventName']  == "PutBucketAcl":
        # Set the bucket ACL to private
        out = updated_acl(bucket)
        return out
    
    else:
        return None