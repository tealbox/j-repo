import requests
import os

def login():
##    key = os.environ['oauthkey']
    key = "kmOC_bLbTzs2-j8hoJYLXUysZvS7NYjhw-J4-uHpiB7F4Yo7o9LdW-nqNT-QXnM7"
    baseurl = 'https://console.cloud.vmware.com/csp/gateway'
    uri = '/am/api/auth/api-tokens/authorize'
    headers = {'Content-Type':'application/json'}
    payload = {'refresh_token': key}
    r = requests.post(f'{baseurl}{uri}', headers = headers, params = payload)
    if r.status_code != 200:
        print(f'Unsuccessful Login Attmept. Error code {r.status_code}')
    else:
        print('Login successful. ')
        print(r.json())
        auth_json = r.json()['access_token']
        auth_Header = {'Content-Type':'application/json','csp-auth-token':auth_json}
        print("auth_Header: ", auth_Header)
        return auth_Header

## https://console.cloud.vmware.com/vmc/api/orgs
## https://vmc.vmware.com/vmc/api/orgs
auth_header = login()
orgList = requests.get('https://vmc.vmware.com/vmc/api/orgs', headers = auth_header)
orgID = orgList.json()[0]['id']
sddcList = requests.get(f'https://vmc.vmware.com/vmc/api/orgs/{orgID}/sddcs', headers = auth_header)
if sddcList.status_code != 200:
    print('API Error')
else:
    for sddc in sddcList.json():
        print("SDDC Name: " + sddc['name'])
        print("SDDC Create Date: " + sddc['created'])
        print("SDDC Provider: " + sddc['provider'])
        print("SDDC Region: " + sddc['resource_config']['region'])

