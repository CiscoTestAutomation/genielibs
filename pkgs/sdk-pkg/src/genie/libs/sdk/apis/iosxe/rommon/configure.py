''' Common Config functions for rommon'''

import logging
log = logging.getLogger(__name__)
# Unicon
from unicon.core.errors import SubCommandFailure
import ipaddress
from ipaddress import IPv4Address, IPv6Address, IPv4Interface, IPv6Interface, ip_interface

def configure_rommon_tftp(device, ipv6_address=False):
    """configure_rommon_tftp 
    This API picks up tftp information from testbed and configures rommon. The device is assumed to be in ROMMON mode already.
       Example : set IP_ADDRESS=1.1.1.1
    Args:
        device('obj'): Device object
        ipv6_address('bool', optional): To use ipv6_address. Defaults to False.
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    tftp = {}

    # Get the current device state from the device
    if device.is_ha and hasattr(device, 'subconnections'):
        if isinstance(device.subconnections, list):
            states = list(set([con.state_machine.current_state for con in device.subconnections]))
            if states == ['rommon']:
                state = 'rommon'
            elif 'rommon' in states:
                raise Exception(f'One of the device connection is in rommon state, need to recover device.')
    else:
        state = device.state_machine.current_state

    # check the device is in rommon
    if state != 'rommon':
        raise Exception(f'The device is not in rommon state')


    # Check if management attribute in device object, if not set to empty dict
    if not hasattr(device, 'management'):
        setattr(device, "management", {})

    # Getting the tftp information, if the info not provided by user, it takes from testbed
    address_dict = device.management.get('address', {})

    # bool to check ipv6 address
    if ipv6_address:
       ip = 'ipv6'
       address = address_dict.get('ipv6')
       if not isinstance(address, ipaddress.IPv6Interface):
          address = ip_interface(address)

       # To get ipv6 ip_address and subnet mask
       ip_address = str(address.ip)
       subnet_mask = str(address.network.prefixlen)
    else:
       ip = 'ipv4'
       address = address_dict.get('ipv4')
       if not isinstance(address, ipaddress.IPv4Interface):
          address = ip_interface(address)

       # To get ipv4 ip_address and subnet mask
       ip_address = str(address.ip)
       subnet_mask = str(address.netmask)
    

    tftp.setdefault("IP_ADDRESS", ip_address)
    tftp.setdefault("IP_SUBNET_MASK", subnet_mask)
    tftp.setdefault("DEFAULT_GATEWAY", str(device.management.get('gateway', {}).get(ip, '')))
    tftp.setdefault("TFTP_SERVER", str(device.testbed.servers.get('tftp', {}).get('address', '')))

    # get the image from clean data
    tftp_image_path = getattr(device.clean, 'images', [])
    if tftp_image_path:
        tftp.setdefault("TFTP_FILE", tftp_image_path[0])

    log.info("checking if all the tftp information is given by the user")
    if not all(tftp.values()):
        log.warning(f"Some TFTP information is missing: {tftp}")

    for set_command, value in tftp.items():

        # To set rommon variables
        cmd = f'{set_command}={value}'
        try:
            # Configure tftp rommon variables in active rp
            if device.is_ha and hasattr(device, 'subconnections'):
                device.subconnections[0].execute(cmd)
            else:
                device.execute(cmd)
        except Exception as e:
            raise SubCommandFailure(
                f"Failed to set the rommon variable {set_command}. Error:\n{e}")

