import boto3
import sys
import time

def get_volume_for_dev_sdf(instance_id):
    # Describe the instance
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    
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
        if device_name == '/dev/sdf':
            volume_id = mapping.get('Ebs', {}).get('VolumeId')
            if volume_id:
                return volume_id
            else:
                # print("No EBS volume found for /dev/sda1")
                return None
    
    # print("/dev/sda1 not found in block device mappings")
    return None

def detach_ebs_volume(volume_id, instance_id):
    try:
        # Detach the volume
        response = ec2_client.detach_volume(
            VolumeId=volume_id,
            InstanceId=instance_id
        )

        print(f"Detaching volume {volume_id} from instance {instance_id}")
        print(response)

        # Wait until the volume is detached
        waiter = ec2_client.get_waiter('volume_available')
        waiter.wait(VolumeIds=[volume_id])

        print(f"Volume {volume_id} successfully detached from instance {instance_id}")

    except Exception as e:
        print(f"Error detaching volume: {str(e)}")

def describe_volume(volume_id, session):
    #print(f'This is the describe_volume function') #--- CHANGES HERE
    try:
        var = ""
        while not var:
            ec2 = session.client('ec2')
            response = ec2.describe_volumes(VolumeIds=[volume_id])
            #print(type(response))
            # print(response)
            volume_status = (response['Volumes'][0]['State'])
            volume_status = volume_status.lower()
            if (volume_status == 'available'):
                #print("Waiting 5 secs before checking back")
                var = "okay"
                print(volume_status)
                return volume_status

            else:
                time.sleep(5)
                #break

    except Exception as e:
        print(f'Function: describe_volume. Error message: {e}')
 

instance_id = sys.argv[1]
region = sys.argv[2]

# Initialize a session using Amazon EC2
ec2_client = boto3.client('ec2', region_name=region)
session = boto3.Session(region_name=region)

volume_id = get_volume_for_dev_sdf(instance_id)

if volume_id:
    detach_ebs_volume(volume_id, instance_id)
    describe_volume(volume_id, session)