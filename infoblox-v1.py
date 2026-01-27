import requests
import json
import argparse
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings (for self-signed certs - remove in production)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class InfobloxClient:
    def __init__(self, host, username, password, wapi_version="v2.12"):
        self.base_url = f"https://{host}/wapi/{wapi_version}"
        self.auth = (username, password)
        self.session = requests.Session()
        self.session.verify = False  # Set to True in production with valid certs

    def get_networks_in_view(self, network_view):
        """
        Fetch all networks in a specific Network View
        
        Args:
            network_view (str): Name of the Network View
            
        Returns:
            list: List of network objects
        """
        # Build query parameters
        params = {
            "_return_fields": "network,network_view,options,extattrs,comment",
            "network_view": network_view
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/network",
                auth=self.auth,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            networks = response.json()
            
            # Handle case where no networks exist (returns empty list)
            if isinstance(networks, list):
                return networks
            else:
                # Single object returned (shouldn't happen for /network)
                return [networks]
                
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"Network View '{network_view}' not found")
            elif response.status_code == 401:
                raise PermissionError("Invalid credentials or insufficient permissions")
            else:
                raise RuntimeError(f"HTTP Error: {e} - {response.text}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Connection failed: {e}")

    def print_networks(self, networks, format="table"):
        """Pretty print networks in table or JSON format"""
        if not networks:
            print("No networks found in this Network View.")
            return

        if format == "json":
            print(json.dumps(networks, indent=2))
            return

        # Table format
        print(f"\n{'NETWORK':<18} {'GATEWAY':<15} {'DNS SERVERS':<25} {'COMMENT'}")
        print("-" * 75)
        
        for net in networks:
            # Extract gateway from DHCP options
            gateway = "N/A"
            dns_servers = "N/A"
            
            if "options" in net:
                for opt in net["options"]:
                    if opt.get("name") == "routers":
                        gateway = opt.get("value", "N/A")
                    elif opt.get("name") == "domain-name-servers":
                        dns_servers = opt.get("value", "N/A")
            
            comment = net.get("comment", "")
            print(f"{net['network']:<18} {gateway:<15} {dns_servers[:24]:<25} {comment}")

def main():
    parser = argparse.ArgumentParser(description="List Infoblox networks in a Network View")
    parser.add_argument("--host", required=True, help="Infoblox appliance IP/FQDN")
    parser.add_argument("--user", required=True, help="WAPI username")
    parser.add_argument("--password", required=True, help="WAPI password")
    parser.add_argument("--view", required=True, help="Network View name")
    parser.add_argument("--format", choices=["table", "json"], default="table",
                        help="Output format (default: table)")
    
    args = parser.parse_args()

    try:
        client = InfobloxClient(args.host, args.user, args.password)
        networks = client.get_networks_in_view(args.view)
        client.print_networks(networks, args.format)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
