import boto3
import os
from dotenv import load_dotenv


def get_aws_session(configure: bool = True):
    if configure:
        load_dotenv()  # Get env vars
        session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_SECRET_KEY"),
            aws_secret_access_key=os.getenv("AWS_ACCESS_KEY")
        )
        return session.client('ec2'), session.resource("ec2")
    else:
        # If AWS profile
        return boto3.client("ec2"), boto3.resource("ec2")


def add_rules():
    ec2_client, ec2_resource = get_aws_session()

    security_group = ec2_client.describe_security_groups(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'servicetier_sg',
                ]
            },
        ]
    )
    assert len(security_group["SecurityGroups"]) == 1
    security_group_id = security_group["SecurityGroups"][0]["GroupId"]

    ec2_client.authorize_security_group_egress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'FromPort': 123,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '81.153.213.176/32',
                        'Description': 'Test sg rule'
                    }
                ],
                'ToPort': 256
            }
        ]
    )

    #iain = abi
