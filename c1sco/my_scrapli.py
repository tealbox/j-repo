import logging
from scrapli.driver.core import NXOSDriver, IOSXEDriver, IOSDriver
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define commands to run on devices
commands = [
    "show version",
    "show ip interface brief",
    "show running-config"
]

# Define devices (Nexus, IOS-XE, IOS)
devices = [
    {
        "host": "192.168.1.1",
        "auth_username": "admin",
        "auth_password": "password",
        "auth_strict_key": False,
        "platform": "nxos",  # Nexus
    },
    {
        "host": "192.168.1.2",
        "auth_username": "admin",
        "auth_password": "password",
        "auth_strict_key": False,
        "platform": "iosxe",  # IOS-XE
    },
    {
        "host": "192.168.1.3",
        "auth_username": "admin",
        "auth_password": "password",
        "auth_strict_key": False,
        "platform": "ios",  # IOS
    }
]

# Function to run commands and log results
def run_commands(device):
    try:
        # Log start time
        start_time = datetime.now()
        logging.info(f"Connecting to {device['host']}")

        # Determine the appropriate driver based on platform
        if device["platform"] == "nxos":
            driver = NXOSDriver
        elif device["platform"] == "iosxe":
            driver = IOSXEDriver
        elif device["platform"] == "ios":
            driver = IOSDriver
        else:
            raise ValueError(f"Unsupported platform: {device['platform']}")

        # Connect to the device
        with driver(**device) as conn:
            logging.info(f"Successfully connected to {device['host']}")
            for command in commands:
                try:
                    # Run the command
                    cmd_start_time = datetime.now()
                    response = conn.send_command(command)
                    cmd_end_time = datetime.now()

                    # Calculate command runtime
                    cmd_runtime = (cmd_end_time - cmd_start_time).total_seconds()

                    # Log command runtime
                    logging.info(f"Command '{command}' on {device['host']} completed in {cmd_runtime:.2f} seconds")

                    # Save output to a file
                    with open(f"{device['host']}_{command.replace(' ', '_')}.txt", "w") as f:
                        f.write(response.result)

                except Exception as e:
                    # Log failed commands
                    logging.error(f"Failed to execute command '{command}' on {device['host']}: {e}")

        # Log total runtime
        end_time = datetime.now()
        total_runtime = (end_time - start_time).total_seconds()
        logging.info(f"All commands on {device['host']} completed in {total_runtime:.2f} seconds")

    except Exception as e:
        # Log connection errors
        logging.error(f"Failed to connect to {device['host']}: {e}")

# Main function to iterate over devices
if __name__ == "__main__":
    for device in devices:
        run_commands(device)
