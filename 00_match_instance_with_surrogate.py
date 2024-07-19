import json
import sys

aws_environment = sys.argv[1]
az = sys.argv[2]

az_file = open('surrogate.json')
az_map = json.load(az_file)

def match_instance_with_surrogate(target_environment, instance_az):
	target_surrogate_instance = az_map[target_environment][0][instance_az]
	return target_surrogate_instance

print(match_instance_with_surrogate(aws_environment,az))