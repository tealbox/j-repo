#-------------------------------------------------------------------------------
# Name:        module1
#-------------------------------------------------------------------------------
from ciscoconfparse2 import CiscoConfParse
from list_of_conf_files import *
import inspect


class myConfigParse:
    def __init__(self, config):
        ##file = 'eccsx100a-dfn.txt'
        self.config_file = config
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
##########################################################################################
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
                    print(exec_q)
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
    def aaa_enabled(self):
        status = self._get_property_enabled(parentspec=r"^aaa\s+new-model", childspec=r"")
        if status == "disabled":
            # check for tacacs-server in cisco nexus 9k
            print("for nexus Xk")
            status = self._get_property_enabled(parentspec=r"^tacacs-server", childspec=r"")
        return status



####file = 'eccsx100a-dfn.txt'
file = r'conf\eccrx131_19.211.243.55.txt'
##parse = CiscoConfParse(file, syntax='ios')
device = myConfigParse(file)
##print(device.telnet_enabled)
##print(device.console_timeout_enabled)
##print(device.vty_timeout_enabled)
##print(device.ip_http_server)
##print(device.ip_https_server)
##print(device.ntp_server)
##print(device.multiple_ntp_server)
print(device.mac_address_timeout_enabled)
print(device.aaa_enabled)


##files = list_of_conf_files()
##for file in files:
##    device = myConfigParse(file)
##    print(f"Processing file: {file}")
##    vtp = device.check_vtp()
##    ##device.get_hostname()
####    print(device.hostname)
####    print(device.ssh_version)
####    print(vtp)
####    print(device.service_password_encryption)
####    print(device.service_timestamps_log)
####    print(device.tcp_keepalives_in_out)
##    attributes = device.list_all_attributes()
##    values = device.printInstance()
##    print(values)
def main():
    pass

if __name__ == '__main__':
    main()
