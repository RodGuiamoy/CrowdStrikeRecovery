import boto3
import sys

def get_instance_availability_zone(instance_id, region):
    # Create a session using the specified AWS region
    session = boto3.Session(region_name=region)

    # Create an EC2 resource object
    ec2 = session.resource('ec2')

    # Retrieve the instance
    instance = ec2.Instance(instance_id)

    # Get the availability zone
    return instance.placement['AvailabilityZone']

# Replace with your instance ID and region
instance_id = sys.argv[1]
region = sys.argv[2]

if __name__ == "__main__":
    # # Replace with your instance ID and region
    # instance_id = 'your-instance-id'  # e.g., 'i-0abcd1234efgh5678'
    # region = 'your-region'  # e.g., 'us-east-1'
    
    availability_zone = get_instance_availability_zone(instance_id, region)
    print(f"{availability_zone}")
