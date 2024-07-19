import boto3
import sys
from datetime import datetime

def create_snapshot(instance_name, volume_id):
    # Create a snapshot
    response = ec2.create_snapshot(VolumeId=volume_id, Description='Snapshot of volume {}'.format(volume_id))
    
    # Get the snapshot ID
    snapshot_id = response.get('SnapshotId')
    if snapshot_id:
        print(f"Snapshot created with ID: {snapshot_id}")
        
        # Get the current date in MMDDYYYY format
        current_date = datetime.now().strftime('%m%d%Y')
        
        # Tag the snapshot with a name
        snapshot_name = f"{instance_name}_C_snapshot_for_crowdstrike_fix_{current_date}"
        ec2.create_tags(Resources=[snapshot_id], Tags=[{'Key': 'Name', 'Value': snapshot_name}])
        print(f"Snapshot tagged with name: {snapshot_name}")
        
        return snapshot_id
    else:
        print("Failed to create snapshot")
        return None
    
# Replace with your instance ID
instance_name = sys.argv[1]
volume_id = sys.argv[2]
region = sys.argv[3]

# Initialize a session using Amazon EC2
ec2 = boto3.client('ec2', region_name=region)

snapshot_id = create_snapshot(instance_name, volume_id)
print(snapshot_id)

    

