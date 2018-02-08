"""
	Example of obtaining credentials from an IAM role rather then having them staticly set.
	See an example of the IAM setup in Terraform: link
"""
import boto3
from botocore.exceptions import ClientError

# Config:
role_arn = ""
session_name = "MySession"
region = ""

# ASG Example
asg_name = ""

# STS get credentials
def get_credentials(role, session):
	sts_client = boto3.client('sts')
	try:
		assumedroleobject = sts_client.assume_role(
			RoleArn=role,
			RoleSessionName=session
		)
		return assumedroleobject['Credentials']
	except ClientError as e:
		print("Received error: %s" % e)
		return False

# Boto Client
def boto3_client(client):
	credentials = get_credentials(role_arn, session_name)
	try:
		client = boto3.client(
			client,
			region_name=region,
			aws_access_key_id=credentials['AccessKeyId'],
			aws_secret_access_key=credentials['SecretAccessKey'],
			aws_session_token=credentials['SessionToken'],
		)
		return client
	except ClientError as e:
		print("Received error: %s" % e)
		return False

### ASG Example
# ASG - Get target instance
def get_asg(asg_name):
	client = boto3_client('autoscaling')
	response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
	if not response['AutoScalingGroups']:
		return False
	else:
		return response

# Main
def main():
	asg_response = get_asg(asg_name)
	if not asg_name:
		print("No Such ASG.")
		return False

	target_instances = []
	for instance in asg_response.get('AutoScalingGroups')[0]['Instances']:
		target_instances.append(instance['InstanceId'])

	return target_instances

if __name__ == "__main__":
	main()