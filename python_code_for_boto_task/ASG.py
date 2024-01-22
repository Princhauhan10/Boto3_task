


import boto3
import time

def create_asg():
    # Replace 'your_access_key', 'your_secret_key', and 'your_region' with your AWS credentials and region
    access_key = '######'
    secret_key = '#######'
    region = 'us-east-1'

    # Connect to AWS
    autoscaling_client = boto3.client('autoscaling', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # Specify Auto Scaling Group details
    asg_name = 'my-auto-scaling-group'
    launch_config_name = 'my-launch-con'
    min_size = 1
    max_size = 3
    desired_capacity = 2
    subnet_ids = ['subnet-08edc469b2d842fd9', 'subnet-08337da8e42623939']  # Replace with your subnet IDs

    # Create Launch Configuration
    response_lc = autoscaling_client.create_launch_configuration(
        LaunchConfigurationName=launch_config_name,
        ImageId='ami-06aa3f7caf3a30282',  # Replace with your AMI ID
        InstanceType='t2.micro',
        KeyName='key',  # Replace with your key pair name
    )

    # Create Auto Scaling Group
    response_asg = autoscaling_client.create_auto_scaling_group(
        AutoScalingGroupName=asg_name,
        LaunchConfigurationName=launch_config_name,
        MinSize=min_size,
        MaxSize=max_size,
        DesiredCapacity=desired_capacity,
        VPCZoneIdentifier=','.join(subnet_ids),
    )

    print(f"Auto Scaling Group {asg_name} created.")

    return asg_name, region, access_key, secret_key

def describe_asg(asg_name, region, access_key, secret_key):
    # Describe Auto Scaling Group details
    autoscaling_client = boto3.client('autoscaling', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    response = autoscaling_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])

    # Print Auto Scaling Group details
    print("Auto Scaling Group Details:")
    for group in response['AutoScalingGroups']:
        print(f"Auto Scaling Group Name: {group['AutoScalingGroupName']}")
        print(f"Launch Configuration Name: {group['LaunchConfigurationName']}")
        print(f"Min Size: {group['MinSize']}")
        print(f"Max Size: {group['MaxSize']}")
        print(f"Desired Capacity: {group['DesiredCapacity']}")
        print(f"VPC Zone Identifier: {group['VPCZoneIdentifier']}")
        print("Instances:")
        for instance in group['Instances']:
            print(f"  - {instance['InstanceId']}")

def delete_asg(asg_name, region, access_key, secret_key):
    # Delete Auto Scaling Group
    autoscaling_client = boto3.client('autoscaling', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    response = autoscaling_client.delete_auto_scaling_group(AutoScalingGroupName=asg_name, ForceDelete=True)

    print(f"Auto Scaling Group {asg_name} deleted.")

if __name__ == "__main__":
    asg_name, region, access_key, secret_key = create_asg()

    # Wait for Auto Scaling Group to become active
    time.sleep(60)

    # Describe Auto Scaling Group details
    describe_asg(asg_name, region, access_key, secret_key)

    # Delete Auto Scaling Group
    delete_asg(asg_name, region, access_key, secret_key)
