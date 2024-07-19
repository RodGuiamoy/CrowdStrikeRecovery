import sys

# Define the region codes using dictionaries
region_codes_goss = [
    {"code": "ASE1", "region": "ap-southeast-1"},
    {"code": "ASE2", "region": "ap-southeast-2"},
    {"code": "CAC1", "region": "ca-central-1"},
    {"code": "EUC1", "region": "eu-central-1"},
    {"code": "EUW1", "region": "eu-west-1"},
    {"code": "USE1", "region": "us-east-1"},
    {"code": "USW2", "region": "us-west-2"}
]

region_codes_non_goss = [
    {"code": "USEA", "region": "us-east-1"},
    {"code": "USWE", "region": "us-west-2"},
    {"code": "EUCE", "region": "eu-central-1"},
    {"code": "EUWE", "region": "eu-west-1"},
    {"code": "APAU", "region": "ap-southeast-2"},
    {"code": "APSP", "region": "ap-southeast-1"},
    {"code": "UOUE", "region": "us-east-1"},
    {"code": "UOUW", "region": "us-west-1"},
    {"code": "CACE", "region": "ca-central-1"}
]

def find_region_goss(instance_name, region_codes):
    if len(instance_name) >= 8:
        substring = instance_name[4:8]
        for region_code in region_codes:
            if substring.upper() == region_code["code"]:
                return region_code["region"]
    return None

def find_region_non_goss(instance_name, region_codes):
    instance_name_upper = instance_name.upper()
    for region_code in region_codes:
        if instance_name_upper.startswith(region_code["code"]):
            return region_code["region"]
    return None


instance_name = sys.argv[1]
aws_environment = sys.argv[2]

if aws_environment != "GlobalOSS":
    region = find_region_non_goss(instance_name, region_codes_non_goss)
else:
    region = find_region_goss(instance_name, region_codes_goss)

print(f"{region}")
