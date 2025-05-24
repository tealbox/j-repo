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

