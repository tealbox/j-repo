#-------------------------------------------------------------------------------
# Name:        To create Port groups on a given DVS
# Version:     1.0, creation
# Version:     1.1, documentation
#-------------------------------------------------------------------------------

import atexit
import sys, re
import time, openpyxl

from pyVmomi import vim, vmodl # pyVmomi VMware SDK implementation
from pyvim import connect # VMware SDK implementation for connection to VC
from pyvim.connect import Disconnect
from ExcelColumnIterator import * # custom class for excel column generator for getting column name like 'A', 'B', 'C'
import argparse, getpass # parsing command line, and getpass for password input
import ssl # ssl implementation

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

def get_obj(content, vimtype, name):
    """
    Get the vsphere object associated with a given text name,
    eg to get VDS object, give VDS name it will return obj
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    # return None if nothing found
    return obj

class CustomException(BaseException):
    """Custom exception class if obj not found"""
    pass

def wait_for_task(task, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """
    from contextlib import suppress

    with suppress(Exception):
        while task.info.state == vim.TaskInfo.State.running:
            time.sleep(2)

        if task.info.state == vim.TaskInfo.State.success:
            if task.info.result is not None and not hideResult:
                out = '%s completed successfully, result: %s' % (actionName, task.info.result)
                print(out)
            else:
                out = '%s completed successfully.' % actionName
                print(out)
        else:
            out = '%s did not complete successfully: %s' % (actionName, task.info.error)
            raise task.info.error
            print (out)

        return task.info.result

class Password(argparse.Action):
    """
    class to handle password during argument parsing, it will not echo password
    """
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass() # to get password without echo
        setattr(namespace, self.dest, values) # set attribute for value


def createPG(si, dv_switch, pgName, vlan):
    dvPGSpec = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
    dvPGSpec.name = pgName
    dvPGSpec.numPorts = 32
    dvPGSpec.type = vim.dvs.DistributedVirtualPortgroup.PortgroupType.ephemeral

    dvPGSpec.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()

    vlan = vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec()
##    vlan.vlanId = extract_numbers_from_end(pgName)
    t = (pgName).split("-")[1]
    vlan.vlanId = extract_numbers_from_end(t)
    dvPGSpec.defaultPortConfig.vlan = vlan

    dvPGSpec.defaultPortConfig.securityPolicy = vim.dvs.VmwareDistributedVirtualSwitch.SecurityPolicy()
    dvPGSpec.defaultPortConfig.securityPolicy.allowPromiscuous = vim.BoolPolicy(value=False)
    dvPGSpec.defaultPortConfig.securityPolicy.forgedTransmits = vim.BoolPolicy(value=False)
    dvPGSpec.defaultPortConfig.securityPolicy.macChanges = vim.BoolPolicy(value=False)
    dvPGSpec.defaultPortConfig.securityPolicy.inherited = False

    # Create uplink teaming policy
    teaming_policy = vim.dvs.VmwareDistributedVirtualSwitch.UplinkPortTeamingPolicy()
    uplinkPortOrder = vim.dvs.VmwareDistributedVirtualSwitch.UplinkPortOrderPolicy()
    if "VMOTION-A" in pgName:
        uplinkPortOrder.activeUplinkPort = ['Uplink 1',]
        uplinkPortOrder.standbyUplinkPort  = ['Uplink 2',]

    elif "VMOTION-B" in pgName:
        uplinkPortOrder.activeUplinkPort = ['Uplink 2',]
        uplinkPortOrder.standbyUplinkPort  = ['Uplink 1',]

    elif "VSAN" in pgName:
        uplinkPortOrder.activeUplinkPort = ['Uplink 2',]
        uplinkPortOrder.standbyUplinkPort  = ['Uplink 1',]

    else: # mgmt & vSAN both are active
        uplinkPortOrder.activeUplinkPort = ['Uplink 1','Uplink 2']

    teaming_policy.uplinkPortOrder = uplinkPortOrder

    dvPGSpec.defaultPortConfig.uplinkTeamingPolicy = teaming_policy
    print("started task: creation of PG %s" % pgName)
    task = dv_switch.CreateDVPortgroup_Task(dvPGSpec)
    results = wait_for_task(task)
    print ("Successfully created DV Port Group ", pgName)
    return dvPGSpec


def main():
    # declare all input variables required to create PG e.g
    # VC, username, password, input XLS file.
##
##    parser = argparse.ArgumentParser(description=":: PortGroup Create ::")
##    parser.add_argument('-x', '--xls', dest="xls", type=str, default=None, required=True, help='input xls file')
##    parser.add_argument('-vc', '--vcenter', dest="vcenter", type=str, default=None, required=True, help='vCenter IP/FQDN')
##    parser.add_argument('-u', '--username', dest="username", type=str, default=None, required=True,help='vCenter username')
##    parser.add_argument('-p', action=Password, nargs='?', dest='password', help='vCenter Password')
##    args = parser.parse_args()
##    xlsFile = args.xls
##
##   # xlsFile = "vc_inputs_schwab.xlsx"
##   # open file for reading XLS
##    wb = openpyxl.load_workbook(xlsFile,data_only=True)
##    ws = wb.active
##    iterator = ExcelColumnIterator(num='D') # choose 'D' column
    vcenter = '192.168.1.32'
    username = 'Administrator@vsphere.local'
    password = "VMware1!"
    try:
        si = None
        try:
            print ("Trying to connect to VCENTER SERVER . . .")
            # connect to vCenter else throw error
            si = connect.Connect(vcenter, 443, username, password, sslContext=context)
        except IOError:
            pass
            atexit.register(Disconnect, si)

        print ("Connected to VCENTER SERVER !")

        content = si.RetrieveContent() # get VC object connect
        datacenter = get_obj(content, [vim.Datacenter], 'LAB-DC')
        cluster = get_obj(content, [vim.ClusterComputeResource], "LAB-Cluster")
        network_folder = datacenter.networkFolder

        print(datacenter, cluster, network_folder)
        # to get dv swtich name
        dvs_name = 'X99C3VBDC'
        dv_switch = get_obj(content, [vim.dvs.VmwareDistributedVirtualSwitch], dvs_name)
        print(dv_switch)
        return (si, content, dv_switch)
    except vmodl.MethodFault:
        print ("Caught vmodl fault: %s" % vmodl.MethodFault)
        pass
##        return 1
    except CustomException as e :
        print ("Caught exception: %s" % e)
        pass
##        return 1

# Start program
if __name__ == "__main__":
    main()