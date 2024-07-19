import boto3
import sys

instance_id = sys.argv[1]
region = sys.argv[2]
json_file = sys.argv[3]

ssm_file = open(json_file)
ssm_json = ssm_file.read()

ssm_doc_name = 'CSfilesDeletionOnSurrogateLinuxBox'
ssm_client = boto3.client('ssm',  region_name = region)
ssm_create_response = ssm_client.create_document(Content = ssm_json, Name = ssm_doc_name, DocumentType = 'Command', DocumentFormat = 'JSON', TargetType =  "/AWS::EC2::Instance")
ssm_run_response = ssm_client.send_command(InstanceIds = [instance_id], DocumentName=ssm_doc_name, DocumentVersion="$DEFAULT", TimeoutSeconds=120)
ssm_delete_response = ssm_client.delete_document(Name=ssm_doc_name)