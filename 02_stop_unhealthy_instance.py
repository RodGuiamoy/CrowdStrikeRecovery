import boto3
import sys

# Specify your region
instance_id = sys.argv[1]
region = sys.argv[2]

# Create EC2 client
ec2 = boto3.client('ec2', region_name=region)

try:
    # Send the stop command
    ec2.stop_instances(
        InstanceIds=[instance_id],
        Force=True  # This parameter forcefully stops the instance
    )
    print(f'Instance {instance_id} is stopping forcefully.')
except Exception as e:
    print(f'Error stopping instance: {str(e)}')
