import boto3
import sys



def get_volume_for_dev_sda1(instance_id):
    # Describe the instance
    response = ec2.describe_instances(InstanceIds=[instance_id])
    
    # Check if the instance exists
    reservations = response.get('Reservations', [])
    if not reservations:
        print("Instance not found")
        return
    
    instance = reservations[0]['Instances'][0]
    
    # Get block device mappings
    block_device_mappings = instance.get('BlockDeviceMappings', [])
    
    # Find the volume for /dev/sda1
    for mapping in block_device_mappings:
        device_name = mapping.get('DeviceName')
        if device_name == '/dev/sda1':
            volume_id = mapping.get('Ebs', {}).get('VolumeId')
            if volume_id:
                return volume_id
            else:
                print("No EBS volume found for /dev/sda1")
                return
    
    print("/dev/sda1 not found in block device mappings")
    return

instance_id = sys.argv[1]
region = sys.argv[2]

# Initialize a session using Amazon EC2
ec2 = boto3.client('ec2', region_name=region)

volume_id = get_volume_for_dev_sda1(instance_id)
print(volume_id)