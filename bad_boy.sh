
GROUP_ID=$1

aws ec2 authorize-security-group-ingress \
    --group-id $GROUP_ID \
    --ip-permissions IpProtocol=tcp,FromPort=3389,ToPort=3389,IpRanges='[{CidrIp=0.0.0.0/0}]' 

aws ec2 authorize-security-group-ingress \
    --group-id $GROUP_ID \
    --ip-permissions IpProtocol=tcp,FromPort=22,ToPort=22,IpRanges='[{CidrIp=0.0.0.0/0}]' 
