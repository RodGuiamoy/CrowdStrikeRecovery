import boto3
import sys



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
        
instance_id = sys.argv[1]
volume_id = sys.argv[2]
region = sys.argv[3]

# Create an EC2 client
ec2_client = boto3.client('ec2', region_name=region)

if __name__ == "__main__":

    detach_ebs_volume(volume_id, instance_id)
