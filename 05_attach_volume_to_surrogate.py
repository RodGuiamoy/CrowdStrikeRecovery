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
            print(response)
            volume_status = (response['Volumes'][0]['State'])
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
                
instance_id = sys.argv[1]
region = sys.argv[2]
volume_id = sys.argv[3]
json_file = sys.argv[4]

session = boto3.Session(region_name=region)
describe_volume(volume_id, session)

ssm_file = open(json_file)
ssm_json = ssm_file.read()

ssm_doc_name = 'CSfilesDeletionOnSurrogateLinuxBox'
ssm_client = boto3.client('ssm',  region_name = region)
ssm_create_response = ssm_client.create_document(Content = ssm_json, Name = ssm_doc_name, DocumentType = 'Command', DocumentFormat = 'JSON', TargetType =  "/AWS::EC2::Instance")
ssm_run_response = ssm_client.send_command(InstanceIds = [instance_id], DocumentName=ssm_doc_name, DocumentVersion="$DEFAULT", TimeoutSeconds=120)
ssm_delete_response = ssm_client.delete_document(Name=ssm_doc_name)