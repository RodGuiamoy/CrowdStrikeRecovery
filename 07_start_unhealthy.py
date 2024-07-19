import boto3
import sys
import time

def describe_volume(volume_id, session):
    #print(f'This is the describe_volume function') #--- CHANGES HERE
    try:
        var = ""
        while not var:
            ec2 = session.client('ec2')
            response = ec2.describe_volumes(VolumeIds=[volume_id])
            #print(type(response))
            # print(response)
            volume_status = (response['Volumes'][0]['Attachments'][0]['State'])
            volume_status = volume_status.lower()
            if (volume_status == 'attached'):
                #print("Waiting 5 secs before checking back")
                var = "okay"
                print(volume_status)
                return volume_status

            else:
                time.sleep(5)
                #break

    except Exception as e:
        print(f'Function: describe_volume. Error message: {e}')

def start_instance(start_instance_id,session):
    #print(f'This is the start_instance function') #--- CHANGES HERE
    try:
        ec2 = session.client('ec2')
        response = ec2.start_instances(
            InstanceIds=[start_instance_id]
        )
        
        print(response)
       
        print(f'STATUS: Instance ID: {start_instance_id} has been successfully started.')
    except Exception as e:
        print(f'Function: start_instance. Error message: {e}')
        
instance_id = sys.argv[1]
volume_id = sys.argv[2]
region = sys.argv[3]

session = boto3.Session(region_name=region)
describe_volume(volume_id, session)
start_instance(instance_id,session)
