import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

ec2 = object  # Global reference to boto3 ec2 reference instantiated by get_aws_session


def create_sg_rules(use_local_aws_creds: bool, connectivity_config: dict):
    """ Create Security Group Rules as defined in connectivity block """
    print("Creating additional Security Group rules defined in Connectivity Config")
    get_aws_session(use_local_aws_creds)
    for rule in connectivity_config:
        apply_sg_rules(connectivity_config[rule])


def get_aws_session(use_local_aws_creds: bool = True):
    """ Initialise AWS session client with local AWS creds """
    global ec2
    if use_local_aws_creds:
        load_dotenv()  # Get env vars
        session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_SECRET_KEY"),
            aws_secret_access_key=os.getenv("AWS_ACCESS_KEY")
        )
        ec2 = session.client('ec2')
    else:
        # If AWS profile available from OS no need to set access keys
        ec2 = boto3.client("ec2")


def get_target_ip(target_server: str):
    """ Get the private IP address of the target server """
    target_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Identifier',
                'Values': [
                    target_server,
                ]
            }
        ]
    )

    private_ips = []
    for reservations in target_instances["Reservations"]:
        for instance in reservations["Instances"]:
            private_ips.append(instance["PrivateIpAddress"])

    return private_ips


def get_security_group_id(group_name: str):
    """ Get Security Group ID for the supplied group name """
    security_group = ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    group_name,
                ]
            },
        ]
    )
    assert len(security_group["SecurityGroups"]) == 1
    return security_group["SecurityGroups"][0]["GroupId"]


def apply_sg_rules(rule_config: dict):
    """ Apply rule config to target security group """
    private_ips = get_target_ip(rule_config["destination_identifier"])
    source_security_group_id = get_security_group_id(rule_config["source_security_group"])

    for ip in private_ips:
        try:
            ec2.authorize_security_group_egress(
                GroupId=source_security_group_id,
                IpPermissions=[
                    {
                        'FromPort': rule_config["from_port"],
                        'IpProtocol': 'tcp',
                        'IpRanges': [
                            {
                                'CidrIp': f'{ip}/32',
                                'Description': rule_config["rule_description"]
                            }
                        ],
                        'ToPort': rule_config["to_port"]
                    }
                ]
            )
        except ClientError as e:
            if "InvalidPermission.Duplicate" in str(e):
                pass  # If rule already exists ignore the exception
