#-------------------------------------------------------------------------------
# Purpose:        To do network assesment
# Name:           Ashok CHAUHAN
# Version:        v1.0
# Description:    Based on CIS, NIST, or PCI DSS Benchmarks & Gold Standard Practice
#-------------------------------------------------------------------------------

from ciscoconfparse2 import CiscoConfParse
from list_of_conf_files import *
import inspect
import csv

################## End of Import Section ##############################

class myConfigParse:
    def __init__(self, config):
        ##file = 'eccsx100a-dfn.txt'
        self.config_file = config
##        self._hostname = "" # GS_Item_
##        self._ssh_version =""
##        self._service_timestamps_debug = '' # GS_Item_1
##        self._service_timestamps_log = '' # GS_Item_1
##        self._service_counters_max_age = "" # GS_Item_3
##        self._service_password_encryption = '' # GS_Item_2
##        self._boot_system_bootflash = "" # GS_Item_4
##        self._security_password_min_length = "" # GS_Item_5
##        self._logging_buffered = "" # GS_Item_5
##        self._maximum_try_password = "" # GS_Item_6
##        self._logging_buffered  = "disabled" # GS_Item_7
##        self._no_logging_console  = "disabled" # GS_Item_8
##        self._enable_secret  = "disabled" # GS_Item_9
##        self._username_admin  = "Not Exist" # GS_Item_10

        self.parse = CiscoConfParse(file, syntax='ios')

    @property
    def hostname(self):
        # Find the hostname
        hostname = self.parse.find_objects(r"^hostname")
##        print(hostname)
        if hostname:
            _hostname = hostname[0].text.split()[1]
            return _hostname
##        else:
##            return ""

    def _get_property_enabled(self, parentspec, childspec):
        _a = self.parse.find_parent_objects_wo_child(parentspec=parentspec, childspec=childspec)
        if _a:
            return "enabled"
        else:
            return "disabled"

    def _get_property_found(self, parentspec, childspec):
        _a = self.parse.find_parent_objects_wo_child(parentspec=parentspec, childspec=childspec)
        if _a:
            return "found"
        else:
            return "not_found"

    def check_vtp(self):
        # Find detailed VTP information
        self.vtp_data = {"domain": "not_found" , 'mode': "not_found", "version": "not_found"}
        vtp = self.parse.find_parent_objects_wo_child(parentspec=r"^vtp", childspec=r"mode")
        if not vtp:
            return self.vtp_data
        vtp = [ item.text for item in  vtp ]
    ##    print(vtp)

        for item in vtp:
            if "domain" in item:
                self.vtp_data ['domain'] = item.split()[-1]
            elif "mode" in item:
                self.vtp_data ['mode'] = item.split()[-1]
            elif "version" in item:
                self.vtp_data ['version'] = item.split()[-1]
        return self.vtp_data
    def list_all_attributes(self):
        """
        Returns a dictionary containing:
        - 'instance_variables': A dictionary of instance variables.
        - 'properties': A list of property names.
        """
        # Get instance variables using vars()
        instance_variables = {k: v for k, v in vars(self).items() if not k.startswith('__')}

        # Get properties by inspecting the class
        properties = [
            name for name, value in inspect.getmembers(type(self))
            if isinstance(value, property)
        ]

        return {
            "instance_variables": instance_variables,
            "properties": properties
        }

    def printInstance(self):
        q = self.list_all_attributes()
        values = {}
        for m in q['instance_variables']:
##            print(self.__dict__[m])
            values.setdefault(m, self.__dict__[m])
        for prop_name in q['properties']:
##            print(getattr(self, prop_name))
            values.setdefault(prop_name, getattr(self, prop_name))
        return values
#####################################################################
############################# Properties Section ####################
    @property
    def ssh_version(self):
        ssh_version = self.parse.find_objects(r"^ssh\s+version")

        if ssh_version:
##        print("SSH version", ssh_version[0].text)
            if "2" in ssh_version[0].text:
                _ssh_version = "2"
                return _ssh_version
            elif "1" in ssh_version[0].text:
                _ssh_version = "1"
                return _ssh_version

        else:
            ssh_version = self.parse.find_objects(r"^SSH\s+Enabled")
            if ssh_version:
                if "2" in ssh_version[0].text:
                    self._ssh_version = "2"
                    return self._ssh_version
                elif "1" in ssh_version[0].text:
                    self._ssh_version = "1"
                    return self._ssh_version
            else:
##                return "SSH_Disabled"
                return "SSH_v2"

    @property
    def service_timestamps_debug(self):
        return self._get_property_enabled(parentspec=r"^service\s+timestamps\s+debug", childspec=r"debug")

    @property
    def service_timestamps_log(self):
        return self._get_property_enabled(parentspec=r"^service\s+timestamps\s+log", childspec=r"log")

    @property
    def service_password_encryption(self):
        return self._get_property_enabled(parentspec=r"^service password-encryption", childspec=r"")

    @property
    def tcp_keepalives_in(self):
        _tcp_keepalives_in =  self._get_property_enabled(parentspec=r"^service\s+tcp-keepalives-in", childspec=r"")
        return _tcp_keepalives_in
    @property
    def tcp_keepalives_out(self):
        _tcp_keepalives_out  =  self._get_property_enabled(parentspec=r"^service\s+tcp-keepalives-out", childspec=r"")
        return _tcp_keepalives_out

    @property
    def logging_console(self):
        return self._get_property_enabled(parentspec=r"^no\s+logging\s+console", childspec=r"")

    @property
    def aaa_enabled(self):
        status = self._get_property_enabled(parentspec=r"^aaa\s+new-model", childspec=r"")
        if status == "disabled":
            # check for tacacs-server in cisco nexus 9k
            print("for nexus Xk")
            status = self._get_property_enabled(parentspec=r"^tacacs-server", childspec=r"")
        return status

    @property
    def enable_secret(self): #GS_Item_9
        return self._get_property_found(parentspec=r"^enable\s+secret", childspec=r"")

    @property
    def check_admin_user(self): #GS_Item_9
        return self._get_property_found(parentspec=r"^username\s+admin", childspec=r"")

    @property
    def ip_domain_lookup(self): #GS_Item_9
        return self._get_property_enabled(parentspec=r"^no\s+ip\s+domain\s+lookup", childspec=r"")

    ##########################################################################################
    @property
    def telnet_enabled(self): #GS_Item_9
        vty_blocks = self.parse.find_objects(r"^line vty")
        if len(vty_blocks) and "line vty 0" in vty_blocks[0].text:
            ## check if transport input ssh
            ## then telnet is disabled
            for child in vty_blocks[0].children:
                if "transport input ssh" in child.text:
                    return "disabled"
                if "transport preferred none" in child.text or "transport input all" in child.text:
                    return "enabled"
##        print(vty_blocks)
##        return self._get_property_enabled(parentspec=r"^no\s+ip\s+domain\s+lookup", childspec=r"")

    @property
    def console_timeout_enabled(self): #GS_Item_9
        con_blocks = self.parse.find_objects(r"^line con 0")
        if len(con_blocks) and "line con 0" in con_blocks[0].text:
            ## check if transport input ssh
            ## then telnet is disabled
            for child in con_blocks[0].children:
                if "exec-timeout" in child.text:
                    # check if exec-timeout x y, x < = 10
                    exec_q = child.text.split()
                    if exec_q[1] == '0':
                        return "disabled"
                    else:
                        return "enabled"
        else:
            return "disabled"

    @property
    def vty_timeout_enabled(self): #GS_Item_9
        # default value: Default Timeout : 10 minutes (10:00)
        # If no exec-timeout is configured, remote sessions (via Telnet or SSH)
        # will automatically terminate after 10 minutes of inactivity
        vty_blocks = self.parse.find_objects(r"^line vty")
        _default = 1
        if len(vty_blocks) and "line vty 0" in vty_blocks[0].text:
            ## check if transport input ssh
            ## then telnet is disabled
            for child in vty_blocks[0].children:
##                print(child.text)
                if "exec-timeout" in child.text:
                    # check if exec-timeout x y, x < = 10
                    exec_q = child.text.split()
##                    print(exec_q)
                    if exec_q[1] == '0':
                        return "disabled"
                else:
                    _default  = 1

        return "enabled" if _default else "disabled"


    @property
    def ip_http_server(self): #GS_Item_9
        return self._get_property_enabled(parentspec=r"^ip http server", childspec=r"")
    @property
    def ip_https_server(self): #GS_Item_9
        return self._get_property_enabled(parentspec=r"^ip http secure-server", childspec=r"")

    @property
    def ntp_server(self): #GS_Item_9
        return self._get_property_enabled(parentspec=r"^ntp server", childspec=r"")

    @property
    def multiple_ntp_server(self): #GS_Item_9
        ntp_blocks = self.parse.find_objects(r"^ntp server")
        return "configured" if len(ntp_blocks) >= 2 else "not_configured"

################## Date: 4/7/2025
    @property
    def bootp_enabled(self): #GS_Item_9
        return self._get_property_enabled(parentspec=r"^ip bootp server", childspec=r"")

    @property
    def mac_address_timeout_enabled(self): #GS_Item_9
        # default value: Default Timeout : 10 minutes (10:00)
        # If no exec-timeout is configured, remote sessions (via Telnet or SSH)
        # will automatically terminate after 10 minutes of inactivity
        mac_blocks = self.parse.find_objects(r"^mac address-table aging-time")
        if not mac_blocks:
            return "300sec"
        else:
            exec_q = mac_blocks[0].text.split()[-1]
            return exec_q + "sec"
    @property
    def ip_source_route(self): #GS_Item_9
        return self._get_property_enabled(parentspec=r"^ip source-route", childspec=r"")

################## End of Properties Section ##############################


headers = ["Hostname", "IP_Address", "VTP_Domain", "VTP_Mode", "VTP_Version",
            "AAA/Tacacs", "Bootp", "Admin_User", "Console_Timeout", "Enable_Secret",
            "IP_Domain_lookup", "HTTP", "HTTPS", "IP_Source_Route", "Console_logging",
            "MAC_Address_Timeout", "NTP", "NTP_Redundancy", "Service_Pass_Encryption",
            "Service_Timestamps_Debug", "Service_Timestamps_log", "SSH_Version", "Telnet",
            "TCP_Keepalives_In", "TCP_Keepalives_Out", "VTY_Timeout"]

####file = 'eccsx100a-dfn.txt'
file = r'conf\duncr002_19.211.225.32.txt'
##parse = CiscoConfParse(file, syntax='ios')


all_devices_data = []
all_devices_data.append(headers)

print(headers)
files = list_of_conf_files()
for file in files:
    device_ip = file.split("_")[1][:-4]
    device = myConfigParse(file)
    print(f"Processing file: {file}")
    vtp = device.check_vtp()
    ##device.get_hostname()
##    print(device.hostname)
##    print(device.ssh_version)
##    print(vtp)
##    print(device.service_password_encryption)
##    print(device.service_timestamps_log)
##    print(device.tcp_keepalives_in_out)
    attributes = device.list_all_attributes()
    values = device.printInstance()

##    print(
##        device.hostname,
##        device.vtp_data["domain"],
##        device.vtp_data["mode"],
##        device.vtp_data["version"],
##        device.aaa_enabled,
##        device.bootp_enabled,
##        device.check_admin_user,
##        device.console_timeout_enabled,
##        device.enable_secret,
##        device.ip_domain_lookup,
##        device.ip_http_server,
##        device.ip_https_server,
##        device.ip_source_route,
##        device.logging_console,
##        device.mac_address_timeout_enabled,
##        device.ntp_server,
##        device.multiple_ntp_server,
##        device.service_password_encryption,
##        device.service_timestamps_debug,
##        device.service_timestamps_log,
##        device.ssh_version,
##        device.telnet_enabled,
##        device.tcp_keepalives_in,
##        device.tcp_keepalives_out,
##        device.vty_timeout_enabled,)


    l = [
        device.hostname,
        device_ip,
        device.vtp_data["domain"],
        device.vtp_data["mode"],
        device.vtp_data["version"],
        device.aaa_enabled,
        device.bootp_enabled,
        device.check_admin_user,
        device.console_timeout_enabled,
        device.enable_secret,
        device.ip_domain_lookup,
        device.ip_http_server,
        device.ip_https_server,
        device.ip_source_route,
        device.logging_console,
        device.mac_address_timeout_enabled,
        device.ntp_server,
        device.multiple_ntp_server,
        device.service_password_encryption,
        device.service_timestamps_debug,
        device.service_timestamps_log,
        device.ssh_version,
        device.telnet_enabled,
        device.tcp_keepalives_in,
        device.tcp_keepalives_out,
        device.vty_timeout_enabled,
        ]
    all_devices_data.append(l)
    print(l)


with open("Ford_Network_Switch_Routers.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(all_devices_data)


def main():
    pass

if __name__ == '__main__':
    main()
