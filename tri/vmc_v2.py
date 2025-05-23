
import requests
import os, json
import ssl
from time import sleep
requests.packages.urllib3.disable_warnings()

def rprint(item, *keys):
    print([item[key] if key in item.keys() else None for key in keys])

def removeKeys(d, keys=[], idKey = False, keyType = None):
    # removeKeys(item, keys=["unique_id", 'realization_id', 'origin_site_id','owner_id'])
    # keyType = 'service_entries'
    ## filtered_list = [s for s in strings if (not flag and s.startswith("_ ")) or (flag and (s.startswith("_ ") or s.endswith("_id")))]
    def _removeKeys(_d, keys=[]):
##        keys = ['display_name','id']
        rKeys = [key for key in _d.keys() if key.startswith('_') or (idKey and key.endswith("_id")) ]
        rKeys.extend(keys)
        [_d.pop(key) for key in rKeys ]
    _removeKeys(d, keys)
    if keyType:
        [_removeKeys(_i, keys) for _i in d['keyType'] ]
##    for _i in d['service_entries']:
####        if isinstance(value, dict):
##        _removeKeys(_i, keys)


def isJson(jString):
    # if jstring bytes convert to str
    if isinstance(jString, (bytes,)):
        jString = str(jString, encoding='utf-8')
        # other method byte_string.decode("utf-8")
    if not isinstance(jString, (str,)):
        return False
    try:
        json.loads(jString)
        return True
    except ValueError:
        return False
##    except JSONDecodeError:
##        return False

############### Base Class for VMWare VMC  ###########
class myVMC:
    # create for the ops of NSX4 tasks
    # required requests

    def __init__(self, loginKey=None, debug=False):
##        self.loginKey = loginKey
        self.loginKey = "XXXXXXXX"
        self.s = requests.Session()
        self.baseUrl = 'https://console.cloud.vmware.com'
        self.s.verify = False
        self.debug = debug
##        self.headers = {
##          "Accept-Encoding": "gzip",
##          "Content-Type": "application/x-www-form-urlencoded",
##          "Accept": "application/json",
##        }
        loginAPI = "/csp/gateway/am/api/auth/api-tokens/authorize"
        self.headers = {'Content-Type':'application/json'}
        payload = {'refresh_token': self.loginKey}

        res = self.post(api=loginAPI, payload=payload)
##        print(res)
        auth_json = res['access_token']
        self.headers = {'Content-Type':'application/json','csp-auth-token':auth_json}
        self.baseUrl = "https://vmc.vmware.com/vmc/api"
##        print(self.headers)

################## API method for Heavy lifting of API Calls ############
    def __do(self, method="GET", api="", payload={}, name=None):
        if 'https' in api:
            ## do nothing api is URL else modify url
            url = api
        else:
            url = f"{self.baseUrl}{api}"
        print("URL: ", url)
        ############### GET ###############
        if method == "GET":
          response = self.s.get(url, headers = self.headers)
##          print(response.status_code, response.content)
          if response.status_code >= 200 and response.status_code <= 299:
            if isJson(response.content):
                return response.json()
            else:
                return response.content
          else:
            print("API Call: ", url)
            print("API is not accessible via GET Method, please check for API, Token/credentials!!")
            return None
        ############### POST ###############
        if method == "POST":
          sleep(.5)
          response = self.s.post(url, headers = self.headers, data=payload, params=payload)

##          print(response.content)
##          print(response.json())
          if response.status_code >= 200 and response.status_code <= 299:
            if isJson(response.content):
                if name:
                    print("%s created Successfully" % name)
                return response.json()
            else:
                return response.content
          else:
            print("API Call: Name: %s API: %s" % (name, url))
            print("Not able to perform Object creation, please check for API, Token/credentials!!")
            print("Exiting.... Please correct and rerun again")
            print(response.content)
            if self.debug:
                print(payload)
##            print("Done.")
##            raise SystemExit() # to quit if object is already exist
            return None  # to
        ############### PUT ###############
        if method == "PUT":
          sleep(.5)
          response = self.s.put(url, headers = self.headers, data=payload)
##          print(response.content)
##          print(response.json())
          if response.status_code >= 200 and response.status_code <= 299:
            if isJson(response.content):
                if name:
                    print("%s created Successfully" % name)
                return response.json()
            else:
                return response.content
          else:
            print("API Call: Name: %s API: %s" % (name, url))
            print("Not able to perform Object creation, please check for API, Token/credentials!!")
            print("Exiting.... Please correct and rerun again")
            print(response.content)
            if self.debug:
                print(payload)
##            print("Done.")
            raise SystemExit()
##            return None
    def get(self, api="", method="GET", payload={},name=None):
        return self.__do(method="GET", api=api, payload={})

    def post(self, api="", method="POST", payload={}, name=None):
        return self.__do(method="POST", api=api, payload=payload, name=name)

    def put(self, api="", method="POST", payload={}, name=None):
        return self.__do(method="PUT", api=api, payload=payload, name=name)


    def getOrgList(self):
        api = "https://vmc.vmware.com/vmc/api/orgs"
        orgList = self.get(api=api)
        self.orgId = orgList[0]['id']
        print(f"Org ID: {self.orgId}")


    def getSDDCList(self):
        sddcList = self.get(f'/orgs/{self.orgId}/sddcs')
##        print(type(sddcList), sddcList)
        for sddc in sddcList:
            print("SDDC Name: " + sddc['name'])
            print("SDDC Create Date: " + sddc['created'])
            print("SDDC Provider: " + sddc['provider'])
            print("SDDC Region: " + sddc['resource_config']['region'])
            print("NSX API PUBLIC ENDPOINT: ", sddc['resource_config']['nsx_api_public_endpoint_url'])


    def getSPPolicies(self, domain='cgw'):
        if "nsxt" in self.baseUrl:
            # add api call and create new URL
            url = f"{self.baseUrl}/infra/domains/{domain}/security-policies"
        else:
            # set base url
            self.baseUrl = 'https://nsx-13-210-234-170.rp.vmwarevmc.com/vmc/reverse-proxy/api/orgs/ea4e8ef5-8e66-4a46-95a6-302d8ead04e8/sddcs/83be4c46-975c-4c35-9991-e5bc0a72b7fa/sks-nsxt-manager/policy/api/v1'
            url = f"{self.baseUrl}/infra/domains/{domain}/security-policies"
        temp_1 = self.get(api=url)
        if "results" in temp_1.keys():
            self.allSP = temp_1["results"]
            spFile = f'{self.baseUrl.split("/")[2].split(".")[0]}_{domain}.json'
            [removeKeys(item, keys = ["id", "relative_path", "sequence_number", "internal_sequence_number", "remote_path"], idKey = True) for item in temp_1['results']]
            with open(spFile, 'w') as f:
                json.dump(temp_1, f, indent=2)
        else:
                print("Error in retriving Security Policies")



    def getGroups(self, domain='cgw'):
        if "nsxt" in self.baseUrl:
            # add api call and create new URL
            url = f"{self.baseUrl}/infra/domains/{domain}/groups"
        else:
            # set base url
            self.baseUrl = 'https://nsx-13-210-234-170.rp.vmwarevmc.com/vmc/reverse-proxy/api/orgs/ea4e8ef5-8e66-4a46-95a6-302d8ead04e8/sddcs/83be4c46-975c-4c35-9991-e5bc0a72b7fa/sks-nsxt-manager/policy/api/v1'
            url = f"{self.baseUrl}/infra/domains/{domain}/groups"
        temp_1 = self.get(api=url)
        if "results" in temp_1.keys():
            self.grps = temp_1["results"]
            grpFile = f'grpup_{domain}.json'
##            [removeKeys(item, keys = ["id", "relative_path", "sequence_number", "internal_sequence_number", "remote_path"], idKey = True) for item in temp_1['results']]
            with open(grpFile, 'w') as f:
                json.dump(temp_1, f, indent=2)
        else:
                print("Error in retriving Security Policies")



#
# /infra/domains/{domain-id}/groups
# /infra/domains/{domain-id}/groups/{group-id}
##
##/infra/domains/cgw
##    "_system_owned": false
##/infra/domains/default
##    "_system_owned": true
##/infra/domains/mgw
##    "_system_owned": false
##
# /infra/domains/cgw/groups
# /infra/domains/cgw/groups/{group-id}
# /infra/domains/mgw/groups
# /infra/domains/mgw/groups/{group-id}

## /infra/domains/cgw/security-policies


a = myVMC()
a.getOrgList()
a.getSDDCList()


a.baseUrl = 'https://nsx-13-210-234-170.rp.vmwarevmc.com/vmc/reverse-proxy/api/orgs/ea4e8ef5-8e66-4a46-95a6-302d8ead04e8/sddcs/83be4c46-975c-4c35-9991-e5bc0a72b7fa/sks-nsxt-manager/policy/api/v1'

##a.getSPPolicies(domain='default')
##
##p = """{       "logging_enabled": false,       "resource_type": "SecurityPolicy",       "display_name": "Deny Inbound",       "path": "/infra/domains/cgw/security-policies/Deny_Inbound",       "parent_path": "/infra/domains/cgw",       "remote_path": "",       "marked_for_delete": false,       "overridden": false,       "category": "Environment",       "stateful": true,       "tcp_strict": true,       "locked": false,       "lock_modified_time": 0,       "scope": [         "ANY"       ],       "is_default": false     }"""
##
##a.post(api="", method="POST", payload=p)

api = '/infra/domains/cgw/groups'
##print(a.get(api=api))

print(a.getGroups(domain='mgw'))




