import boto3

iam_client = boto3.client('iam')

response = iam_client.attach_user_policy(UserName='sre-cli-user',PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess")
print(f'---------------------------------\nAttaching temporary admin policy\n---------------------------------\n')