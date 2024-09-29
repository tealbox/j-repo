#----------------------------------------------------------------------------------------------------
# Name:        VMWare VI/JSON retrive all VM objects, require aiohttp, python-dotenv and .env file
#----------------------------------------------------------------------------------------------------
import json
import logging
import os
import sys

import aiohttp
from dotenv import load_dotenv
import asyncio

load_dotenv()

server = os.environ['VSPHERE_SERVER']
user = os.environ['VSPHERE_USER']
pwd = os.environ['VSPHERE_PASSWORD']

load_dotenv()

server = os.environ['VSPHERE_SERVER']
user = os.environ['VSPHERE_USER']
pwd = os.environ['VSPHERE_PASSWORD']

print(server, user, pwd)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(stream=sys.stdout)])


class APIException(Exception):
    """Exception raised for errors in API calls."""
    def __init__(self, message: str, status_code: int, response: dict) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response

def to_path(obj: dict) -> str:
    """Convert a vSphere ManagedObjectReference to a path string"""
    return f"{obj['type']}/{obj['value']}"

def short_json(json_data: dict) -> str:
    """Shorten a JSON string to a maximum length"""
    str = json.dumps(json_data, indent=2)
    lines = str.splitlines()
    if len(lines) > 23:
        lines = lines[:20] + ["..."] + lines[-2:]
        str = "\n".join(lines)
    return str


# ServiceInstance ManagedObjectReference
# This is the root object of the vSphere API
# It is a well-known object and is not discoverable
SERVICE_INSTANCE = {
   "type": "ServiceInstance",
   "value": "ServiceInstance"
}

JSON_CONTENT_TYPE = "application/json"

SUPPORTED_RELEASES = ["8.0.2.0", "8.0.1.0"]

async def negotiate_release(server: str,
                            supported_releases: list[str],
                            session: aiohttp.ClientSession,
                            verify: bool):
    """Negotiates API release identifier to use.
    The application author sends the list of releases they have tested with
    in order of priority and the server returns mutually acceptable release
    identifier.
    The API was released in 8.0.2.0 and thus if the server is 8.0.1.0 it
    will return HTTP status code 404.
    See
    https://developer.vmware.com/apis/vsphere-automation/latest/vcenter/api/vcenter/systemactionhello/post/
    """
    body = {
        "api_releases": supported_releases
    }
    async with session.post(
            f"https://{server}/api/vcenter/system?action=hello",
            json=body,
            headers={"content-type": "application/json"},
            verify_ssl=verify) as r:
        if r.status == 404:
            logging.debug("System.hello is not found. Assuming 8.0.1.0")
            return "8.0.1.0"
        if r.status != 200:
            logging.debug("Failed to negotiate release. received status: %s",
                          r.status)
            raise APIException("Failed to negotiate release",
                               r.status,
                               await r.json())
        release = (await r.json())["api_release"]
        if not release:
            raise APIException("No mutually acceptable release found. \
                                Perhaps the script is very old", 0, {})
        logging.debug("Negotiated release: %s", release)
        return release


##async with aiohttp.ClientSession() as session:
##    release = await negotiate_release(server, SUPPORTED_RELEASES, session, False)
##
##



class VSphereConnection:
    """vSphere VI/JSON API client connection"""
    def __init__(self,
                 server: str,
                 release: str,
                 session: aiohttp.ClientSession,
                 verify: bool = True) -> None:
        """Initialize the vSphere client
        Args:
            server: vSphere server name or IP address
            release: vSphere release identifier
            session: aiohttp session
            verify: Check TLS trusts or not
        """
        self.base = f"https://{server}/sdk/vim25/{release}"
        self.session = session
        self.headers = { "Accept": "application/json"}
        self.verify = verify

    async def set_session_key(self, session_key: str) -> None:
        """Set session key"""
        self.headers["vmware-api-session-id"] = session_key

    async def fetch(self, obj: dict, prop: str) -> dict:
        """Fetch a property from a vSphere object using HTTP GET"""
        logging.debug("fetching %s from %s", prop, obj)
        print("Fetch Url: ", f"{self.base}/{to_path(obj)}/{prop}")
        async with self.session.get(f"{self.base}/{to_path(obj)}/{prop}",
                                    headers=self.headers,
                                    verify_ssl=self.verify) as r:
            pyaload, _ = await self._process_response(obj, prop, r)
            return pyaload

    async def invoke(self, obj: dict, method: str, body: dict) -> dict:
        """Invoke a method on a vSphere object using HTTP POST"""
        logging.debug("invoking %s on %s", method, obj)
        headers = {
            "Content-Type": "application/json"
        } | self.headers
        url = f"{self.base}/{to_path(obj)}/{method}"
        print("Invoke Url: ", url)
        async with self.session.post(url,
                                     json=body,
                                     headers=headers,
                                     verify_ssl=self.verify) as r:
            return await self._process_response(obj, method, r)

    async def _process_response(self, obj: dict,
                                operation: str,
                                response: aiohttp.ClientResponse) \
            -> (dict, dict):
        """Process a response from the vSphere server. Returns JSON payload
        and headers on success and throws APIException on error."""
        content = {}
        if response.headers.get('content-type', '') \
                .startswith(JSON_CONTENT_TYPE):
            content = await response.json()
        if response.status < 300:
            return content, response.headers
        logging.debug("Error received: %s: %s", response.status, content)
        raise APIException(f"Invoke {operation} operation on {obj} failed! \
                               {response.status}: {await response.text()}",
                           response.status,
                           content)


class SessionManager:
    """vSphere SessionManager proxy"""
    def __init__(self, session_manager: dict, connection: VSphereConnection) -> None:
        self.moref = session_manager
        self.connection = connection

    async def login(self, user: str, pwd: str) -> str:
        """Login to vSphere server and set session key in the connection"""
        logging.debug("logging in")
        body = {
            "userName": user,
            "password": pwd
        }
        user_session, headers = await self.connection.invoke(self.moref,
                                                             "Login",
                                                             body)
        session_key = headers.get("vmware-api-session-id")
        if not session_key:
            raise APIException("Login did not return a session key", 0, {})
        # Set the session key in the connection for subsequent calls
        await self.connection.set_session_key(session_key)
        logging.debug("logged in")
        return user_session

    async def logout(self) -> None:
        """Logout from vSphere server"""
        await self.connection.invoke(self.moref, "Logout", {})
        await self.connection.set_session_key(None)
        logging.debug("logged out")

class ContainerView:
    """vSphere ContainerView proxy"""
    def __init__(self, view: dict, connection: VSphereConnection) -> None:
        self.moref = view
        self.connection = connection

    async def destroy_view(self) -> None:
        """Destroy the view using DestroyView"""
        await self.connection.invoke(self.moref, "DestroyView", {})
        logging.debug("destroyed view: %s", self.moref)


class ViewManager:
    """vSphere ViewManager proxy"""
    def __init__(self, view_manager: dict, connection: VSphereConnection) -> None:
        self.moref = view_manager
        self.connection = connection

    async def create_container_view(self, container: dict,
                                    recursive: bool,
                                    _type: list[str]) -> ContainerView:
        """Create a container view using the ViewManager"""
        logging.debug("creating container view for %s", container)
        body = {
                "container": container,
                "recursive": recursive,
                "type": _type
        }
        view, _ = await self.connection.invoke(self.moref,
                                               "CreateContainerView",
                                               body)
        logging.debug("created view: %s", view)
        return ContainerView(view, self.connection)


class PropertyCollector:
    """vSphere PropertyCollector proxy"""
    def __init__(self, property_collector: dict, connection: VSphereConnection) -> None:
        self.moref = property_collector
        self.connection = connection

    async def retrieve_properties_ex(self, params: dict) -> dict:
        """Retrieve properties using the PropertyCollector"""
        result, _ = await self.connection.invoke(self.moref,
                                                 "RetrievePropertiesEx",
                                                 params)
        logging.debug("retrieved properties")
        return result

    async def continue_retrieve_properties_ex(self, token: str) -> dict:
        """Continue retrieving properties using the PropertyCollector"""
        logging.debug("continuing to retrieve properties")
        body = {
            "token": token,
        }
        result, _ = await self.connection.invoke(self.moref,
                                                 "ContinueRetrievePropertiesEx",
                                                 body)
        logging.debug("continued to retrieve properties")
        return result

    async def cancel_retrieve_properties_ex(self, token: str) -> None:
        """Cancel retrieving properties using the PropertyCollector"""
        logging.debug("canceling retrieve properties on token %s", token)
        body = {
            "token": token,
        }
        await self.connection.invoke(self.moref,
                                     "CancelRetrievePropertiesEx",
                                     body)
        logging.debug("canceled to retrieve properties")


class ServiceInstance:
    """vSphere ServiceInstance proxy"""
    def __init__(self, service_instance: dict, connection: VSphereConnection) -> None:
        self.moref = service_instance
        self.connection = connection
        self.content = None

    async def get_content(self) -> dict:
        """Get ServiceInstance content"""
        if self.content is None:
            self.content = await self.connection.fetch(self.moref,
                                                       "content")
            logging.debug("retrieved service instance content")
        return self.content

    async def get_session_manager(self) -> SessionManager:
        """Get the identifier of the session manager from the ServiceInstance
        content"""
        return SessionManager((await self.get_content())["sessionManager"],
                              self.connection)

    async def get_view_manager(self) -> ViewManager:
        """Get the identifier of the view manager from the ServiceInstance
        content"""
        return ViewManager((await self.get_content())["viewManager"],
                           self.connection)

    async def get_property_collector(self) -> PropertyCollector:
        """Get the identifier of the default property collector from the
        ServiceInstance content"""
        pc_moref = (await self.get_content())["propertyCollector"]
        return PropertyCollector(pc_moref, self.connection)

    async def get_root_folder_moref(self) -> dict:
        """Get the identifier of the root folder from the ServiceInstance
        content"""
        return (await self.get_content())["rootFolder"]


def build_retrieve_properties_ex_params(view: dict, page_size: int) -> dict:
    """Build the RetrievePropertiesEx parameters"""
    # See https://developer.vmware.com/apis/vi-json/latest/sdk/vim25/release/PropertyCollector/moId/RetrievePropertiesEx/post/
    return {
            "options": {
                "_typeName": "RetrieveOptions",
                "maxObjects": page_size
            },
            "specSet": [
                {
                    "_typeName": "PropertyFilterSpec",
                    "objectSet": [
                        {
                            "_typeName": "ObjectSpec",
                            "obj": view,
                            "selectSet": [
                                {
                                    "_typeName": "TraversalSpec",
                                    "name": "traverseEntities",
                                    "path": "view",
                                    "skip": False,
                                    "type": "ContainerView"
                                }
                            ],
                            "skip": True
                        }
                    ],
                    "propSet": [
                        {
                            "_typeName": "PropertySpec",
                            "all": False,
                            "pathSet": [
                                # https://vdc-download.vmware.com/vmwb-repository/dcr-public/184bb3ba-6fa8-4574-a767-d0c96e2a38f4/ba9422ef-405c-47dd-8553-e11b619185b2/SDK/vsphere-ws/docs/ReferenceGuide/vim.VirtualMachine.html
                                "name",
                                # You can traverse in depth the property
                                # structures to select only relevant data
                                "summary.guest.ipAddress"
                            ],
                            "type": "VirtualMachine"
                        },
                        {
                            "_typeName": "PropertySpec",
                            "all": False,
                            "pathSet": [
                                "name"
                            ],
                            "type": "HostSystem"
                        }
                    ],
                    "reportMissingObjectsInResults": False
                }
            ]
        }

async def list_vms_and_hosts(si: ServiceInstance, page_size: int) -> list[dict]:
    """List all VMs and ESX hosts in the vSphere server using the PropertyCollector and
    ContainerView APIs. We first create a ContainerView that contains all VMs and ESX hosts.
    Then we use the PropertyCollector to retrieve the name and IP address of each VM and
    the name of each ESX host. We use the RetrievePropertiesEx API to retrieve the data
    in pages. We use the ContinueRetrievePropertiesEx API to retrieve the next page(s).
    We use the CancelRetrievePropertiesEx API to cancel the retrieval of the data if we
    fail to read all pages. At last we use the DestroyView API to destroy the ContainerView."""
    view_mgr = await si.get_view_manager()
    root_folder = await si.get_root_folder_moref()
    pc = await si.get_property_collector()
    # See https://developer.vmware.com/apis/vi-json/latest/sdk/vim25/release/ViewManager/moId/CreateContainerView/post/
    view = await view_mgr.create_container_view(root_folder,
                                                True,
                                                ["VirtualMachine", "HostSystem"])
    token = None
    try:
        params = build_retrieve_properties_ex_params(view.moref, page_size)
        result = await pc.retrieve_properties_ex(params)
        token = result.get("token")
        objects = result["objects"]
        # Iterate result in pages with ContinueRetrievePropertiesEx
        while token:
            result = await pc.continue_retrieve_properties_ex(token)
            token = result.get("token")
            objects = objects + result["objects"]
    finally:
        # Very important to dismiss the result when we fail to read it all
        if token:
            await pc.cancel_retrieve_properties_ex(token)
        # Dismiss the view object we allocated earlier
        await view.destroy_view()
    return objects



def extract_primitive_property(item, property_name):
    for prop in item['propSet']:
        if prop['name'] == property_name:
            return prop['val']['_value']
    return 'N/A'

def print_tables(data):
    vm_table = []
    host_table = []

    for item in data:
        if item['obj']['type'] == 'VirtualMachine':
            id = item['obj']['value']
            name = extract_primitive_property(item, 'name')
            ip_address = extract_primitive_property(item, 'summary.guest.ipAddress')
            vm_table.append((id, name, ip_address))
        elif item['obj']['type'] == 'HostSystem':
            id = item['obj']['value']
            name = extract_primitive_property(item, 'name')
            host_table.append((id, name))

    print("Virtual Machines:")
    print(f"{'ID':<15} {'Name':<25} {'IP Address':<15}")
    for row in vm_table:
        print(f"{row[0]:<15} {row[1]:<25} {row[2]:<15}")

    print("\nHosts:")
    print(f"{'ID':<15} {'Name':<25}")
    for row in host_table:
        print(f"{row[0]:<15} {row[1]:<25}")












async def main():
    async with aiohttp.ClientSession() as session:
        release = await negotiate_release(server, SUPPORTED_RELEASES, session, False)

    async with aiohttp.ClientSession() as session:
        connection = VSphereConnection(server, release, session, False)

        # Get the service instance content
        content = await connection.fetch(SERVICE_INSTANCE, "content")

        logging.info("Service Instance Content: %s", short_json(content))

    async with aiohttp.ClientSession() as session:
        connection = VSphereConnection(server, release, session, False)

        si = ServiceInstance(SERVICE_INSTANCE, connection)
        session_manager = await si.get_session_manager()
        user_session = await session_manager.login(user, pwd)
        logging.info("Session Details %s", short_json(user_session))
        await session_manager.logout()



    objects = None
    async with aiohttp.ClientSession() as session:
        connection = VSphereConnection(server, release, session, False)

        si = ServiceInstance(SERVICE_INSTANCE, connection)
        session_manager = await si.get_session_manager()
        user_session = await session_manager.login(user, pwd)
        try:
            objects = await list_vms_and_hosts(si, 5)
            logging.info("VMs and Hosts: %s", short_json(objects))
        finally:
            await session_manager.logout()
    print_tables(objects)



asyncio.run(main())

