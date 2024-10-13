# https://www.lesinskis.com/python_sorting_IP_addresses.html
>>> ips = ['192.168.1.10', '10.67.160.10', '43.43.0.1', '10.0.0.1', '255.255.255.0', '19.19.0.1', '140.0.0.1', '141.0.0.1', '255.255.255.255', '192.30.30.1', '255.255.255.0', '10.66.91.140', '255.255.255.0', '192.168.1.1','192.168.2.254', '0.0.0.0', '0.0.0.0', '10.66.91.1', '192.30.30.1', ]
>>> sorted(ips)
['0.0.0.0', '0.0.0.0', '10.0.0.1', '10.66.91.1', '10.66.91.140', '10.67.160.10', '140.0.0.1', '141.0.0.1', '19.19.0.1', '192.168.1.1', '192.168.1.10', '192.168.2.254', '192.30.30.1', '192.30.30.1', '255.255.255.0', '255.255.255.0', '255.255.255.0', '255.255.255.255', '43.43.0.1']

>>> import ipaddress
>>> sorted([ipaddress.ip_address(addr) for addr in ips])
[IPv4Address('0.0.0.0'), IPv4Address('0.0.0.0'), IPv4Address('10.0.0.1'), IPv4Address('10.66.91.1'), IPv4Address('10.66.91.140'), IPv4Address('10.67.160.10'), IPv4Address('19.19.0.1'), IPv4Address('43.43.0.1'), IPv4Address('140.0.0.1'), IPv4Address('141.0.0.1'), IPv4Address('192.30.30.1'), IPv4Address('192.30.30.1'), IPv4Address('192.168.1.1'), IPv4Address('192.168.1.10'), IPv4Address('192.168.2.254'), IPv4Address('255.255.255.0'), IPv4Address('255.255.255.0'), IPv4Address('255.255.255.0'), IPv4Address('255.255.255.255')]

But if for some reason you wanted to keep strings you can make use of the fact that sorting in Python just requires that the less than operator is defined which it is in the case of ipaddress.IPv4Address. We can therefore use this constructor as a sort key like so:

>>> sorted(ips, key = ipaddress.IPv4Address)
['0.0.0.0', '0.0.0.0', '10.0.0.1', '10.66.91.1', '10.66.91.140', '10.67.160.10', '19.19.0.1', '43.43.0.1', '140.0.0.1', '141.0.0.1', '192.30.30.1', '192.30.30.1', '192.168.1.1', '192.168.1.10', '192.168.2.254', '255.255.255.0', '255.255.255.0', '255.255.255.0', '255.255.255.255']

