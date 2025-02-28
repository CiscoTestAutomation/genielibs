# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def configure_tacacs_server(device, server_config):
    """ Configure tacacs server
        Args:
            device ('obj'): Device object
            server_config('dict'): Dictionary object
                dictionary contains following  keys:
                    host ('str'): host ip address
                    timeout ('int'): server time out value in seconds
                    key_type (str): key type for tacacs server
                    key ('str'): key value from tacacs server
                    server ('str'): server ip address
                    ipv6_server('str'): server ipv6 address
                    single_connection('boolean'): set to True
                    send_nat_address('boolean'): set to True
                    fqdn_name('str'): Fully Qualified domain name
            Returns:
                configurations list
            Raises:
                Failed configuring tacacs server
            Example:
                server_config = {
                            'host': 'mgmt-tac',
                            'timeout': '10',
                            'key_type': '7',
                            'key': '01239132C123',
                            'server': '192.168.21.1'
                            'ipv6_server': '2000::2'
                            'single_connection': True
                            'send_nat_address': True
                            'fqdn_name': 'f1'
                        },
    """

    config = []

    # tacacs server mgmt-tac
    if "host" in server_config:
        config.append("tacacs server {0}".format(server_config["host"]))

    # address ipv4 10.106.26.213
    if "server" in server_config:
        config.append("address ipv4 {0}".format(server_config["server"]))

    # address ipv6 200::4
    if "ipv6_server" in server_config:
        config.append("address ipv6 {0}".format(server_config["ipv6_server"]))

    # key 0 Cisco123
    if "key_type" in server_config and "key" in server_config:
        config.append("key {0} {1}".format(server_config["key_type"],
                                             server_config["key"]))
    # key Cisco123
    elif "key" in server_config:
        config.append("key {0}".format(server_config["key"]))

    # timeout 10
    if "timeout" in server_config:
        config.append("timeout {0}".format(server_config["timeout"]))

    # single-connection
    if server_config.get("single_connection", False):
        config.append("single-connection")

    # send-nat-address
    if server_config.get("send_nat_address", False):
        config.append("send-nat-address")

    # address fqdn f1
    if 'fqdn_name' in server_config:
        config.append("address fqdn {0}".format(server_config["fqdn_name"]))

    try:
        device.configure(config)
        return config
    except SubCommandFailure as e:
        logger.error(f"Failed to configure tacacs server with error {e}")
        raise

def configure_policy_map(device,
        policy_name,
        class_map_list
        ):
    """ Configures policy_map
        Args:
             device ('obj'): device to use
             policy_name('str) : name of the policy name
             class_map_list('list'): list of data type hold number class map information
             [
             {
             class_map_name('str') : name of the class
             policer_val('int',optional): police,
             priority_level('int',optional): 1 to 7,
             bandwidth_percent('int',optional): percentage value
             shape_average('str',optional): shape value
             child_policy('str',optional): name of the child policy
             } 
             ]


        example:
             class_map_list=[
             {
             'class_map_name':'test1',
             'policer_val':2000000000,
             'priority_level':1 to 7,
             'bandwidth_percent':10,
             'shape_average':2000000000,
             'child_policy':'child_policy'
             }
             ]


        Returns:
            None
        Raises:
            SubCommandFailure
    """
    logger.debug(
        "Configuring policy_map {policy_name} ".format(
            policy_name=policy_name,
        )
    )
    cmd = [f"policy-map {policy_name}"]
    for class_map  in class_map_list:
        cmd.append(f"class {class_map['class_map_name']}")
        if 'policer_val' in class_map:
            cmd.append(f"police  {class_map['policer_val']}")
        if 'priority_level' in class_map:
            cmd.append(f"priority level  {class_map['priority_level']}")
        if 'bandwidth_percent' in class_map:
            cmd.append(f"bandwidth percent {class_map['bandwidth_percent']}")
        if 'shape_average' in class_map:
            cmd.append(f"shape average {class_map['shape_average']}")
        if 'child_policy'  in class_map:
            cmd.append(f"service-policy {class_map['child_policy']}")

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class_map. Error:\n{error}".format(
                error=e
            )
        )

def configure_ignore_startup_config(device):
    """  To configure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure the device
    """

    try:
        # If the device state is in rommon configure rommon variable
        if device.state_machine.current_state == 'rommon':
            cmd = 'SWITCH_IGNORE_STARTUP_CFG=1'
            device.execute(cmd)
        else:
            cmd = 'system ignore startupconfig switch all'
            device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ignore startup config on {device.name}. Error:\n{e}")

def unconfigure_ignore_startup_config(device):
    """ To unconfigure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to unconfigure the device
    """
    try:
        # If the device state is in rommon configure rommon variable
        if device.state_machine.current_state == 'rommon':
            cmd = 'SWITCH_IGNORE_STARTUP_CFG=0'
            device.execute(cmd)
        else:
            cmd = 'no system ignore startupconfig switch all'
            device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ignore startup config on {device.name}. Error:\n{e}")
