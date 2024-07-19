import boto3
import sys
import time

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
        

def verInstance(verInstanceId,session):
    #print(f'This the verInstance function') #---Changes here
    try:
        ec2 = session.client('ec2')
        response = ec2.describe_instance_status(
            InstanceIds=[verInstanceId],
        )
        
        print(response)
        
        verStatus = (response['InstanceStatuses'][0]['InstanceState']['Name'])
        return verStatus
    except Exception as e:
        print(f'Function: verInstance. Error message: {e}')
        
def checkInstanceStatusRunning(chk_instance_id,session):
    var = ""
    try:
        while not var:

            server_status = verInstance(chk_instance_id,session)
            server_status = server_status.lower()
            if (server_status == 'Stopped'):
                var = 'ok'
                return server_status
            else:
                time.sleep(5)
                #break
    except Exception as e:
        print(f'Function: checkInstanceStatusRunning. Error message: {e}')
        
instance_id = sys.argv[1]
volume_id = sys.argv[2]
region = sys.argv[3]

# Create an EC2 client
ec2_client = boto3.client('ec2', region_name=region)
session = boto3.Session(region_name=region)

if __name__ == "__main__":
    checkInstanceStatusRunning(instance_id,session)
    detach_ebs_volume(volume_id, instance_id)
