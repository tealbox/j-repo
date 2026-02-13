import requests, json, re
import requests.packages
from typing import List, Dict
from pprint import pprint
import ssl, time
# from casUtils import *

context = ssl._create_unverified_context()
# noinspection PyUnresolvedReferences
requests.packages.urllib3.disable_warnings()

def toUnderscore(s):
    import re
    pat = r"""\s|\W"""
    s = re.sub(pat,'_',s)
    return s
def removeSpecialChar(s):
    # will remove all special characters
    # all alphabets, so remining will be
    # numbers and comma and hyphen not working for -(hyphen)
    pat = r"""(?!,)\W|\s|[A-Za-z]"""
    s = re.sub(pat,'',s)
    return s

class myNSX:
    # create for the ops of NSX4 tasks
    # required requests
    def __init__(self, nsxmgr, username = "admin", password = "VMware1!VMware1!"):
        self.s = requests.Session()
        self.hostname = nsxmgr
        self.username = username
        self.password = password
        self.s.verify = False
        cred = self.getEncoded()
        self.headers = {
          'Accept-Encoding': 'gzip',
          'Content-Type': "application/json",
          'Accept': 'application/json',
          # 'Authorization': "Basic dnBhbmthajpCbHVlYmVycnkjMTQyMjA="
          'Authorization': f'Basic {cred}'
        }
##        print(cred)
##        print(self.headers)
        self.baseUrl = f"https://{self.hostname}/policy/api/v1"

    def getEncoded(self):
        # import encoding
        from base64 import b64encode
        s = f'{self.username}:{self.password}'.encode('utf-8')
        return b64encode(s).decode('utf-8')

    def __do(self, method="GET", api="", payload={}, name=None, domain_id = "default"):
        if 'https' in api:
            ## do nothing api is URL else modify url
            url = api
        elif "/policy/api/v1/" in api:
            url = f"https://{self.hostname}/{api}"
##        elif "domain-id" in api:
##            api = re.sub(r"\{domain-id\}", "{domain_id}", api)
##            url = f"{self.baseUrl}{api}"
        else:
            url = f"{self.baseUrl}{api}"

##        print("URL: ", url)
        if method == "GET":
          response = self.s.get(url, headers = self.headers)
          if response.status_code >= 200 and response.status_code <= 299:
            return response.json()
          else:
            return "Not able to GET api, please check for login/ip/credentials!!"
        if method == "POST":
          response = self.s.post(url, data = payload, headers = self.headers)
##          print(response.status_code)
##          print(response.content)
          if response.status_code >= 200 and response.status_code <= 299:
            print(f"Created successfully!!: {name}")
            return response.json()
          else:
            pass
##            print(f"Not able to create object: {name}")
        if method == "PUT":
          response = self.s.put(url, data = payload, headers = self.headers)
          if response.status_code >= 200 and response.status_code <= 299:
            print(f"Created successfully!!: {name}")
            return response.json()
          else:
            pass
            print(f"Object already exist: {name}")
##            print(f"Not able to create object: {name}")
##            print(response.json())
        if method == "PATCH":
          response = self.s.patch(url, data = payload, headers = self.headers)
          if response.status_code >= 200 and response.status_code <= 299:
            # print(response.content)
            return "Success" # .json()
          else:
            return "Error in PATCHing %s"%url
        if method == "DELETE":
          response = self.s.delete(url, data = payload, headers = self.headers)
          if response.status_code >= 200 and response.status_code <= 299:
            return "Deleted Successfully"
          else:
            return "Error in Deletion"

    def get(self, api="", method="GET", payload={},name=None):
        return self.__do(method="GET", api=api, payload={})

    def post(self, api="", method="POST", payload={}, name=None):
        return self.__do(method="POST", api=api, payload=payload, name=name)

    def put(self, api="", method="PUT", payload={}, name=None):
        return self.__do(method="PUT", api=api, payload=payload, name=name)

    def delete(self, api="", method="DELETE", payload={}, name=None):
        return self.__do(method="DELETE", api=api, payload=payload, name=name)

    def get_services(self):
        api = "/infra/services"

        res = self.__do(method="GET", api=api, payload={})
        if "results" in res:
          self.all_services =  res['results']
          return self.all_services
        else:
            return None

    def get_groups(self):
        domain_id = "default"
        api = f"/policy/api/v1/infra/domains/{domain_id}/groups"

        res = self.__do(method="GET", api=api, payload={})
        if "results" in res:
          self.all_groups =  res['results']
          return self.all_groups
        else:
            return None

