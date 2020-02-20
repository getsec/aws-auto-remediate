import boto3
import json
import logging
from os import environ
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Grab all the ENV Vars
instance_whitelist = environ.get("EC2_WHITELIST")
owner_tag_name = environ.get("EC2_OWNER_TAG_NAME")
status_change_tag_name = environ.get("EC2_STATUS_CHANGE_TAG_NAME")

# Canned error message to be  used later if needed
ERROR = """
Looks like you ran into a pretty weird issue that should have never happened.
Please create an issue at https://github.com/getsec/aws-auto-remediate.git

When raising an issue, please make sure you send in the lambda execution logs. Extract anything you might think is sensitive
"""

def tag_instance(instance_id, tagset):
    """Tags an instance
    
    Arguments:
        instance_id {str} -- ID of the ec2 instance
        tagset {list} -- list of dicts - example
            [
                {
                    "Key": name_of_key (str)
                    "Value": value_of_key (str)
                },
                 {
                    "Key": name_of_key (str)
                    "Value": value_of_key (str)
                },
                ....
            ]
    
    Returns:
        json -- response object
    """ 
    client = boto3.client('ec2')
    response = client.create_tags(
        Resources=[instance_id],
        Tags=tagset
    )
    return response




def lambda_handler(event, context):
    # Log the event for troubleshooting
    logger.info(event)
    user = event['detail']['userIdentity']['userName']
    event_name = event['detail']['eventName']

    if event_name in "RunInstances":
        # If event is run instance it means the id will be in the responseparams
        # since it hasnt been created yet
        instance_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
        tagset = [{
            "Key": owner_tag_name,
            "Value": user
        }]
        out = tag_instance(instance_id, tagset)
        return out
    elif event_name in ["RebootInstances", "StopInstances", "StartInstances"]:
        # Since the instance is already created - The instance ID will be found in the requestparams
        instance_id = event['detail']['requestParameters']['instancesSet']['items'][0]['instanceId']
        tagset = [
        {
            "Key": status_change_tag_name,
            "Value": user
        }
        ]
        out = tag_instance(instance_id, tagset)
        return out
    else:
        return {
            "output": "error",
            "message": json.dumps(ERROR)
        }
    