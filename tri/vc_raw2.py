#-------------------------------------------------------------------------------
# Name:        module4
#-------------------------------------------------------------------------------
# https://{vcenter-host}/sdk/vim25/8.0.2.0/Datacenter/datacenter-3/datastoreFolder


#-------------------------------------------------------------------------------
# Name:        module3
#-------------------------------------------------------------------------------

# https://$VC/sdk/vim25/8.0.1.0/ServiceInstance/ServiceInstance/content
# get "rootFolder"."value", "type": "Folder", "sessionManager"."value" "type": "SessionManager"
# rootFolder    ManagedObjectReference:Folder    group-d1 (Datacenters)
#

import requests
import json

nf = 'n/f'

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

############### Base Class for CISCO-SDWAN Viptela ###########
class myVC:
    # create for the ops of NSX4 tasks
    # required requests

    def __init__(self, vc="192.168.1.31", username = "Administrator@vsphere.local", passcode="VMware1!", debug=False):
        requests.packages.urllib3.disable_warnings()
        self.devices = {}
        self.s = requests.Session()
        self.vc = vc
        self.s.verify = False
        self.debug = debug
        self.headers = {
          "Content-Type": "application/json"
        }
        self.baseUrl = f"https://{vc}"
        payload = json.dumps({
          "userName": username,
          "password": passcode
        })

        self.getRootFolder()
        self.baseUrl = f"https://{vc}/sdk/vim25/{self.apiVersion}"
        print("Base URL: ", self.baseUrl)
        loginAPI = f"https://{vc}/sdk/vim25/8.0.2.0/SessionManager/SessionManager/Login"
        res = self.s.post(loginAPI, headers = self.headers ,data=payload)
        print(res.status_code)
        if res.status_code != 200:
            print ("Authentication failed, Please check username/password!")
            exit()
        self.headers.setdefault('vmware-api-session-id', res.headers['vmware-api-session-id'])
        self.sessionId = res.headers['vmware-api-session-id']
        print(self.headers)



    def getRootFolder(self):
        api = '/sdk/vim25/8.0.1.0/ServiceInstance/ServiceInstance/content'
        data = self.get(api=api)
        self.rootFolder = data.get('rootFolder', None).get('value', None)

        self.apiVersion = data.get('about', None).get('apiVersion', None)
        print("Root Folder: ", self.rootFolder, "API Version: ", self.apiVersion)






################## API method for Heavy lifting of API Calls ############
    def __do(self, method="GET", api="", payload={}, name=None):
        # headers={"vmware-api-session-id": sessionId}
        url = f"{self.baseUrl}{api}"
        if method == "GET":
          response = self.s.get(url, headers = self.headers)
          print("GET Respone: ",response)
          if response.status_code >= 200 and response.status_code <= 299:
            if isJson(response.content):
                return response.json()
            else:
                return response.content
          else:
            print("API Call: ", url)
            print("API is not accessible via GET Method, please check for API, Token/credentials!!")
            return None
        if method == "POST":
          sleep(.5)
          response = self.s.post(url, headers = self.headers, data=payload)
##          print(response.content)
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


vc = myVC()
##api = "/sdk/vim25/8.0.2.0/Datacenter/datacenter-3/datastoreFolder"
##api = "/sdk/vim25/8.0.2.0/Datacenter/datacenter-3/network"
##api = '/sdk/vim25/8.0.1.0/ServiceInstance/ServiceInstance/content'
##api = '/ServiceInstance/ServiceInstance/content'
##t = vc.get(api=api)
##>>> a['rootFolder']
##{'_typeName': 'ManagedObjectReference', 'type': 'Folder', 'value': 'group-d1'}
##>>> a['rootFolder']['value']
##'group-d1'
##>>>
##print(t)

api = f"/Folder/{vc.rootFolder}/childEntity"
t = vc.get(api=api)
print(t)

listDatacenter = [] # 'type': 'Datacenter'
listFolder = [] # 'type': 'Folder'

for item in t:
    if item.get('type', None) == 'Datacenter':
        listDatacenter.append(item.get('value', None))
    if item.get('type', None) == 'Folder':
        listFolder.append(item.get('value', None))
{
    ##
    ##GET /Datacenter/{moId}/datastore
    ##GET /Datacenter/{moId}/datastoreFolder
    ##GET /Datacenter/{moId}/declaredAlarmState
    ##GET /Datacenter/{moId}/disabledMethod
    ##GET /Datacenter/{moId}/effectiveRole
    ##GET /Datacenter/{moId}/hostFolder
    ##GET /Datacenter/{moId}/name
    ##GET /Datacenter/{moId}/network
    ##GET /Datacenter/{moId}/networkFolder
    ##GET /Datacenter/{moId}/overallStatus
    ##GET /Datacenter/{moId}/parent
    ##GET /Datacenter/{moId}/permission
    ##GET /Datacenter/{moId}/recentTask
    ##GET /Datacenter/{moId}/tag
    ##GET /Datacenter/{moId}/triggeredAlarmState
    ##GET /Datacenter/{moId}/value
    ##GET /Datacenter/{moId}/vmFolder


    ##GET /Datacenter/{clusterName}/datastore
    ##GET /Datacenter/{clusterName}/datastoreFolder
    ##GET /Datacenter/{clusterName}/hostFolder
    ##GET /Datacenter/{clusterName}/name
    ##GET /Datacenter/{clusterName}/network
    ##GET /Datacenter/{clusterName}/networkFolder
    ##GET /Datacenter/{clusterName}/parent
    ##GET /Datacenter/{clusterName}/permission
    ##GET /Datacenter/{clusterName}/value
    ##GET /Datacenter/{clusterName}/vmFolder
    ##GET /Datacenter/{clusterName}/configuration

    ##clusterName = "datacenter-3"
    ##
    ##api = f"/Datacenter/{clusterName}/datastore"
    ##t = vc.get(api=api)
    ##print(t)
    ##
    ##api = f"/Datacenter/{clusterName}/datastoreFolder"
    ##t = vc.get(api=api)
    ##print(t)
    ##
    ##api = f"/Datacenter/{clusterName}/configuration"
    ##t = vc.get(api=api)
    ##print(t)
    ##
    ##api = f"/Datacenter/{clusterName}/network"
    ##t = vc.get(api=api)
    ##print(t)
    ##
    ##
    ##api = f"/Datacenter/{clusterName}/datastore"
    ##t = vc.get(api=api)
    ##print(t)
    ##
    ##api = f"/Datacenter/{clusterName}/vmFolder"
    ##t = vc.get(api=api)
    ##print(t)
}



networks = []
for item in listDatacenter:
    api = f"/Datacenter/{item}/datastore"
    t = vc.get(api=api)
    print(t)

    api = f"/Datacenter/{item}/datastoreFolder"
    t = vc.get(api=api)
    print(t)

    api = f"/Datacenter/{item}/configuration"
    t = vc.get(api=api)
    print(t)

    api = f"/Datacenter/{item}/network"
    t = vc.get(api=api)
    for net in t:
        networks.append(net.get('value', None))
    print(t)
    print(networks)


    api = f"/Datacenter/{item}/datastore"
    t = vc.get(api=api)
    print(t)

    api = f"/Datacenter/{item}/vmFolder"
    t = vc.get(api=api)
    print(t)

##
##GET /Network/{moId}/availableField
##GET /Network/{moId}/configIssue
##GET /Network/{moId}/configStatus
##GET /Network/{moId}/customValue
##GET /Network/{moId}/declaredAlarmState
##GET /Network/{moId}/disabledMethod
##GET /Network/{moId}/effectiveRole
##GET /Network/{moId}/host
##GET /Network/{moId}/name
##GET /Network/{moId}/overallStatus
##GET /Network/{moId}/parent
##GET /Network/{moId}/permission
##GET /Network/{moId}/recentTask
##GET /Network/{moId}/summary
##GET /Network/{moId}/tag
##GET /Network/{moId}/triggeredAlarmState
##GET /Network/{moId}/value
##GET /Network/{moId}/vm

for item in networks:
##    api = f"/Network/{item}/availableField"
##    t = vc.get(api=api)
##    print(t)
##    api = f"/Network/{item}/name"
##    t = vc.get(api=api)
##    print(t)
    api = f"/Network/{item}/summary"
    t = vc.get(api=api)
    print(t)

##
##
##
##
##GET /DistributedVirtualPortgroup/{moId}/availableField
##GET /DistributedVirtualPortgroup/{moId}/config
##GET /DistributedVirtualPortgroup/{moId}/configIssue
##GET /DistributedVirtualPortgroup/{moId}/configStatus
##GET /DistributedVirtualPortgroup/{moId}/customValue
##GET /DistributedVirtualPortgroup/{moId}/declaredAlarmState
##GET /DistributedVirtualPortgroup/{moId}/disabledMethod
##GET /DistributedVirtualPortgroup/{moId}/effectiveRole
##GET /DistributedVirtualPortgroup/{moId}/host
##GET /DistributedVirtualPortgroup/{moId}/key
##GET /DistributedVirtualPortgroup/{moId}/name
##GET /DistributedVirtualPortgroup/{moId}/overallStatus
##GET /DistributedVirtualPortgroup/{moId}/parent
##GET /DistributedVirtualPortgroup/{moId}/permission
##GET /DistributedVirtualPortgroup/{moId}/portKeys
##GET /DistributedVirtualPortgroup/{moId}/recentTask
##GET /DistributedVirtualPortgroup/{moId}/summary
##GET /DistributedVirtualPortgroup/{moId}/tag
##GET /DistributedVirtualPortgroup/{moId}/triggeredAlarmState
##GET /DistributedVirtualPortgroup/{moId}/value
##GET /DistributedVirtualPortgroup/{moId}/vm
##

DistributedVirtualPortgroup = []
for item in networks:
    print(f"------------------------ [networks] ------------------------------")
##    api = f"/Network/{item}/availableField"
##    t = vc.get(api=api)
##    print(t)
##    api = f"/Network/{item}/name"
##    t = vc.get(api=api)
##    print(t)
    api = f"/Network/{item}/summary"
    t = vc.get(api=api)
    if t['network']['type'] == "DistributedVirtualPortgroup":
        DistributedVirtualPortgroup.append( t['network']['value'])
    print(t)

for item in DistributedVirtualPortgroup:
##    api = f"/Network/{item}/availableField"
##    t = vc.get(api=api)
##    print(t)
##    api = f"/Network/{item}/name"
##    t = vc.get(api=api)
##    print(t)
    api = f"/DistributedVirtualPortgroup/{item}/config"
    item2 = vc.get(api=api)

    print(
        item2.get('backingType',nf),
        item2.get('defaultPortConfig',nf).get('VNI',nf).get('value',nf),
        item2.get('distributedVirtualSwitch',nf).get('value',nf),
        item2.get('key',nf),
        item2.get('name',nf),
        item2.get('segmentId',nf),
        item2.get('transportZoneName',nf),
        item2.get('type',nf))
    print(item2)

##
##
##
##GET /DistributedVirtualSwitch/{moId}/alarmActionsEnabled
##GET /DistributedVirtualSwitch/{moId}/availableField
##GET /DistributedVirtualSwitch/{moId}/capability
##GET /DistributedVirtualSwitch/{moId}/config
##GET /DistributedVirtualSwitch/{moId}/configIssue
##GET /DistributedVirtualSwitch/{moId}/configStatus
##GET /DistributedVirtualSwitch/{moId}/customValue
##GET /DistributedVirtualSwitch/{moId}/declaredAlarmState
##GET /DistributedVirtualSwitch/{moId}/disabledMethod
##GET /DistributedVirtualSwitch/{moId}/effectiveRole
##GET /DistributedVirtualSwitch/{moId}/name
##GET /DistributedVirtualSwitch/{moId}/networkResourcePool
##GET /DistributedVirtualSwitch/{moId}/overallStatus
##GET /DistributedVirtualSwitch/{moId}/parent
##GET /DistributedVirtualSwitch/{moId}/permission
##GET /DistributedVirtualSwitch/{moId}/portgroup
##GET /DistributedVirtualSwitch/{moId}/recentTask
##GET /DistributedVirtualSwitch/{moId}/runtime
##GET /DistributedVirtualSwitch/{moId}/summary
##GET /DistributedVirtualSwitch/{moId}/tag
##GET /DistributedVirtualSwitch/{moId}/triggeredAlarmState
##GET /DistributedVirtualSwitch/{moId}/uuid
##GET /DistributedVirtualSwitch/{moId}/value
##
