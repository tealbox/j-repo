import sys
import os
import argparse
import django
import netaddr

sys.path.append('/opt/avi/python/bin/portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings_local')

django.setup()

from avi.rest.pb_utils import get_pb_if_exists
from avi.rest.pb2model import protobuf2model_transaction
from avi.protobuf import options_pb2
from api.models import NetworkRuntime, Cloud, IpamDnsProviderProfile
import api.models as models

def change_ipam_profile_in_cloud(cloud_name, new_ipam_profile_name):
    try:
        cloud = Cloud.objects.get(name=cloud_name)
    except Cloud.DoesNotExist:
        print(f"Cloud {cloud_name} not found, no action taken")
        return
    if not cloud:
        print(f"Cloud {cloud_name} not found, no action taken")
        return
    try:
          ipam_profile = IpamDnsProviderProfile.objects.get(name=new_ipam_profile_name)
    except IpamDnsProviderProfile.DoesNotExist:
        print(f"IPAM profile {new_ipam_profile_name} not found, no action taken")
        return
    if not ipam_profile:
        print(f"IPAM profile {new_ipam_profile_name} not found, no action taken")
        return
    cloud_pb = cloud.protobuf()
    cloud_pb.ipam_provider_uuid = ipam_profile.uuid
    protobuf2model_transaction(cloud_pb, None, True)
    return

def main():
    parser = argparse.ArgumentParser(description='Change IPAM profile in cloud')
    parser.add_argument('--cloud-name', type=str, required=True)
    parser.add_argument('--new-ipam-profile-name', type=str, required=True)
    args = parser.parse_args()
    change_ipam_profile_in_cloud(args.cloud_name, args.new_ipam_profile_name)

if __name__ == '__main__':
    main()
