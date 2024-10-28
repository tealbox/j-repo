#-------------------------------------------------------------------------------
# Name:        module3
#-------------------------------------------------------------------------------

# https://$VC/sdk/vim25/8.0.1.0/ServiceInstance/ServiceInstance/content
# get "rootFolder"."value", "type": "Folder", "sessionManager"."value" "type": "SessionManager"
# rootFolder    ManagedObjectReference:Folder    group-d1 (Datacenters)
#

import requests
import json


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

        loginAPI = f"https://{vc}/sdk/vim25/8.0.2.0/SessionManager/SessionManager/Login"
        res = self.s.post(loginAPI, headers = self.headers ,data=payload)
        print(res.status_code)
        if res.status_code != 200:
            print ("Authentication failed, Please check username/password!")
            exit()
        self.headers.setdefault('vmware-api-session-id', res.headers['vmware-api-session-id'])
        self.sessionId = res.headers['vmware-api-session-id']
        print(self.headers)


    def getNetworks(self):
        print(self.sessionId)
        url = f"{self.baseUrl}{api}"
        res = requests.get(url,  headers={"vmware-api-session-id": self.sessionId}, verify=False)
##        return res.json()
    # Get VMs, for example
        response = requests.get("https://192.168.1.31/api/vcenter/network", headers={"vmware-api-session-id": self.sessionId}, verify=False)
        if response.ok:
            print(f"VMs: {response.json()}")
        else:
            pass
##            raise ValueError("Unable to retrieve VMs.")

################## API method for Heavy lifting of API Calls ############
    def __do(self, method="GET", api="", payload={}, name=None):
        # headers={"vmware-api-session-id": sessionId}
        url = f"{self.baseUrl}{api}"
        if method == "GET":
          response = self.s.get(url, headers = {'vmware-api-session-id': self.sessionId})
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
api = "/api/vcenter/network"
t = vc.get(api=api)
t = vc.getNetworks()

print(t)





# Get session ID
response = requests.post("https://192.168.1.31/api/session", auth=("administrator@vsphere.local", "VMware1!"), verify=False)
if response.ok:
    sessionId = response.json()
    print(sessionId)
else:
    raise ValueError("Unable to retrieve a session ID.")

# Get VMs, for example
response = requests.get("https://192.168.1.31/api/vcenter/vm", headers={"vmware-api-session-id": sessionId}, verify=False)
if response.ok:
    print(f"VMs: {response.json()}")
else:
    raise ValueError("Unable to retrieve VMs.")


# Get VMs, for example
response = requests.get("https://192.168.1.31/api/vcenter/network", headers={"vmware-api-session-id": sessionId}, verify=False)
if response.ok:
    print(f"VMs: {response.json()}")
else:
    raise ValueError("Unable to retrieve VMs.")





def main():
    pass

if __name__ == '__main__':
    main()
