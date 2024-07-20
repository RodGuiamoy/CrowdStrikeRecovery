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

def checkCommandStatus(commandId,instances):
    
    ssm_client = boto3.client('ssm',  region_name = region)
 
    #If instances is not a list, convert it to a list
 
    # if not isinstance(instances, list):
    # instances = [instances]

    var = ""
    while not var:    
        ssmStatus = ""
        #print("Waiting 5 seconds before checking status...")
        time.sleep(10)
        #for ssmInstances in instances:
            #print(ssmInstances)
        output = ssm_client.get_command_invocation(
            CommandId=commandId,
            InstanceId=instances
        )
        #ssmStatus.append(str(output['StatusDetails']))
        ssmStatus = str(output['Status'])

            #print("Command ID: " + str(output['CommandId']) + " Instance: " + \
                #str(output['InstanceId']) + " Status: " + str(output['StatusDetails']))
 
        #Check back in 5 minutes to avoid hammering the commection with status requests
        if (ssmStatus != 'Success' or ssmStatus != 'Failed'):
            #print("Waiting 5 secs before checking back")
            print(ssmStatus)
            time.sleep(5)
        else:
            var = "okay"
             
instance_id = sys.argv[1]
region = sys.argv[2]
volume_id = sys.argv[3]
json_file = sys.argv[4]

session = boto3.Session(region_name=region)
describe_volume(volume_id, session)

ssm_file = open(json_file)
ssm_json = ssm_file.read()

ssm_doc_name = 'CSfilesDeletionOnSurrogateLinuxBox-Ubuntu'
ssm_client = boto3.client('ssm',  region_name = region)
ssm_create_response = ssm_client.create_document(Content = ssm_json, Name = ssm_doc_name, DocumentType = 'Command', DocumentFormat = 'JSON', TargetType =  "/AWS::EC2::Instance")
ssm_run_response = ssm_client.send_command(InstanceIds = [instance_id], DocumentName=ssm_doc_name, DocumentVersion="$DEFAULT", TimeoutSeconds=120)
command_id = ssm_run_response['Command']['CommandId']
checkCommandStatus(command_id,instance_id)

ssm_delete_response = ssm_client.delete_document(Name=ssm_doc_name)
