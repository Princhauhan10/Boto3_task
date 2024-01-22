import boto3
import time
import pytz
from datetime import datetime

def create_ec2_instance():
    # Replace 'your_access_key', 'your_secret_key', and 'your_region' with your AWS credentials and region
    access_key = '########'
    secret_key = '########'
    region = 'us-east-2'

    # Connect to AWS
    ec2_client = boto3.client('ec2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # Specify instance details
    instance_type = 't2.micro'
    ami_id = 'ami-07b36ea9852e986ad'  # Replace with your desired AMI ID
    security_group_id = 'sg-0883a37f0a1128b2e'  # Replace with your security group ID

    # Launch EC2 instance without specifying key pair
    response = ec2_client.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        SecurityGroupIds=[security_group_id],
        MinCount=1,
        MaxCount=1
    )

    # Get instance ID
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Instance {instance_id} created.")

    # Wait for the instance to be running
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    print("Instance is now running.")

    # Get instance details
    instance_details = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance_info = instance_details['Reservations'][0]['Instances'][0]

    # Convert launch time to IST
    launch_time_utc = instance_info['LaunchTime']
    launch_time_utc = launch_time_utc.replace(tzinfo=pytz.utc)
    launch_time_ist = launch_time_utc.astimezone(pytz.timezone('Asia/Kolkata'))

    # Print instance details with IST launch time
    print("Instance Details:")
    print(f"Instance ID: {instance_id}")
    print(f"Instance Type: {instance_info['InstanceType']}")
    print(f"Launch Time (UTC): {launch_time_utc}")
    print(f"Launch Time (IST): {launch_time_ist.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Simulate some time passing (you may want to perform other actions or wait for user input)
    time.sleep(60)

    # Terminate the instance
    ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} terminated.")

if __name__ == "__main__":
    create_ec2_instance()
