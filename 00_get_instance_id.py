import boto3
import sys

def get_instance_id(instance_name, region):
    # Create a session using the specified region
    session = boto3.Session(region_name=region)
    
    # Create an EC2 client
    ec2_client = session.client('ec2')
    
    # Describe instances with filters
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [instance_name]
            }
        ]
    )
    
    # Iterate through the reservations and instances to find the instance ID
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            return instance['InstanceId']
    
    return None

instance_name = sys.argv[1]
region = sys.argv[2]

# Example usage
if __name__ == "__main__":
    instance_id = get_instance_id(instance_name, region)
    if instance_id:
        print(f'{instance_id}')
