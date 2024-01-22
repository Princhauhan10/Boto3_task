import boto3
import time
import pytz
from datetime import datetime

def create_elb():
    # Replace 'your_access_key', 'your_secret_key', and 'your_region' with your AWS credentials and region
    access_key = '#####'
    secret_key = '#########'
    region = 'us-east-1'

    # Connect to AWS
    elbv2_client = boto3.client('elbv2', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    # Specify load balancer details
    load_balancer_name = 'my-load-balancer'
    subnets = ['subnet-08edc469b2d842fd9', 'subnet-08337da8e42623939']  # Replace with your subnet IDs
    security_groups = ['sg-08b11ceb490405231']  # Replace with your security group IDs

    # Create a load balancer
    response = elbv2_client.create_load_balancer(
        Name=load_balancer_name,
        Subnets=subnets,
        SecurityGroups=security_groups,
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'MyLoadBalancer'
            },
        ]
    )

    # Get load balancer ARN
    load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']
    print(f"Load Balancer {load_balancer_arn} created.")

    # Wait for the load balancer to be active
    waiter = elbv2_client.get_waiter('load_balancer_exists')
    waiter.wait(Names=[load_balancer_name])
    print("Load Balancer is now active.")

    # Describe load balancer details
    load_balancer_details = elbv2_client.describe_load_balancers(Names=[load_balancer_name])
    load_balancer_info = load_balancer_details['LoadBalancers'][0]

    # Convert creation time to IST
    creation_time_utc = load_balancer_info['CreatedTime']
    creation_time_utc = creation_time_utc.replace(tzinfo=pytz.utc)
    creation_time_ist = creation_time_utc.astimezone(pytz.timezone('Asia/Kolkata'))

    # Print load balancer details with IST creation time
    print("Load Balancer Details:")
    print(f"Load Balancer ARN: {load_balancer_info['LoadBalancerArn']}")
    print(f"DNS Name: {load_balancer_info['DNSName']}")
    print(f"Scheme: {load_balancer_info['Scheme']}")
    print(f"Creation Time (UTC): {creation_time_utc}")
    print(f"Creation Time (IST): {creation_time_ist.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Simulate some time passing (you may want to perform other actions or wait for user input)
    time.sleep(60)

    # Delete the load balancer
    elbv2_client.delete_load_balancer(LoadBalancerArn=load_balancer_arn)
    print(f"Load Balancer {load_balancer_arn} deleted.")

if __name__ == "__main__":
    create_elb()
