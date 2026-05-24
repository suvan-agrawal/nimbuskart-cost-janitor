import boto3

ec2 = boto3.client(
    "ec2",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

response = ec2.describe_instances()

instance_id = response["Reservations"][0]["Instances"][0]["InstanceId"]

ec2.stop_instances(
    InstanceIds=[instance_id]
)

print(f"Stopped instance: {instance_id}")