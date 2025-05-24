from netmiko import ConnectHandler, redispatch

jumpserver = {
    'device_type': 'terminal_server',
    'ip': 'JUMP_SERVER_IP',
    'username': 'jump_user',
    'password': 'jump_pass',
}
net_connect = ConnectHandler(**jumpserver)
net_connect.write_channel('ssh WLC_IP\n')
net_connect.write_channel('admin\n')
net_connect.write_channel('Cisco123!\n')
redispatch(net_connect, device_type='cisco_wlc_ssh')
output = net_connect.send_command("show ap summary")
print(output)
net_connect.disconnect()


from netmiko import ConnectHandler

# Define the device parameters
wlc = {
    'device_type': 'cisco_wlc_ssh',  # Specific device type for Cisco WLC
    'host': '192.168.1.1',          # WLC IP address
    'username': 'admin',            # WLC username
    'password': 'Cisco123!',        # WLC password
    'port': 22,                     # SSH port (default is 22)
}

try:
    # Establish SSH connection
    with ConnectHandler(**wlc) as connection:
        print("Connected to WLC successfully!")
        
        # Disable paging to prevent "Press Enter to continue" prompts
        connection.send_command("config paging disable")
        
        # Example: Run a command to retrieve AP summary
        output = connection.send_command("show ap summary")
        print("AP Summary:\n", output)
        
except Exception as e:
    print(f"Failed to connect: {e}")

# Connection is automatically closed when using 'with' context manager

# Special Login Handler: Netmiko’s CiscoWlcSSH class includes a special_login_handler method to manage the WLC’s login process, which may prompt for "User:" or "Password:" in certain OS versions

from netmiko import ConnectHandler
import logging

# Enable logging for debugging
logging.basicConfig(filename='netmiko_debug.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

# Device connection details
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
    'session_log': 'session_debug.log',  # Log file for session output
    'verbose': True  # Enable verbose logging
}

try:
    # Establish connection
    with ConnectHandler(**device) as net_connect:
        # Run a command
        output = net_connect.send_command("show version")
        print(output)
except Exception as e:
    print(f"Error: {e}")
#######################################################
# If you want to capture logs in memory (instead of a file) for debugging, use BufferedSessionLog:
from netmiko import ConnectHandler
from netmiko.session_log import BufferedSessionLog

# Device connection details
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
    'session_log': BufferedSessionLog(),  # In-memory buffer
    'verbose': True
}

try:
    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_command("show version")
        print(output)
        # Access buffered log
        session_log_content = net_connect.session_log.getvalue()
        print("Session Log Contents:")
        print(session_log_content)
except Exception as e:
    print(f"Error: {e}")
    
