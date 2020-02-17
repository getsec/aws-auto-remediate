import logging
import os
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)
bad_ports = os.environ['bad_ports'].split(',')
good_ip_range = os.environ['good_ip_range']


def lambda_handler(event, context):
    security_group_id = event['detail']['requestParameters']['groupId']

    ec2 = boto3.resource('ec2')
    sg = ec2.SecurityGroup(security_group_id)

    permissions = sg.ip_permissions
    sets_to_be_removed = []
    sets_to_be_added = []
    for p_set in permissions:
        if p_set.get('IpRanges')[0].get('CidrIp') == '0.0.0.0/0':
            if p_set.get('FromPort') == 22 or p_set.get('ToPort') == 22:
                sets_to_be_removed.append(p_set)
            if p_set.get('FromPort') == 3389 or p_set.get('ToPort') == 3389:
                sets_to_be_removed.append(p_set)

    sg.revoke_ingress(IpPermissions=sets_to_be_removed)

    for sets in sets_to_be_removed:
        sets['IpRanges'][0]['CidrIp'] = good_ip_range
        sets_to_be_added.append(sets)

    sg.authorize_ingress(IpPermissions=sets_to_be_added)
