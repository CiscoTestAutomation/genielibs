''' Common Config functions for rommon'''

import logging
log = logging.getLogger(__name__)
# Unicon
from unicon.core.errors import SubCommandFailure
from genie.libs.clean.utils import get_image_handler
import ipaddress
from ipaddress import IPv4Address, IPv6Address, IPv4Interface, IPv6Interface, ip_interface

def configure_rommon_tftp(device, use_ipv6=False):
    """configure_rommon_tftp 
    This API picks up tftp information from testbed and configures rommon. The device is assumed to be in ROMMON mode already.
       Example : set IP_ADDRESS=1.1.1.1
    Args:
        device('obj'): Device object
        use_ipv6('bool', optional): To use use_ipv6. Defaults to False.
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
            if 'rommon' in states:
                state = 'rommon'
                raise Exception(f'Use the `configure_rommon_tftp_ha` API to configure rommon for tftp boot')
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
    if use_ipv6:
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
    image_handler = get_image_handler(device)
    if image_handler.image:
        tftp.setdefault("TFTP_FILE", image_handler.image[0])

    log.info("checking if all the tftp information is given by the user")
    if not all(tftp.values()):
        log.warning(f"Some TFTP information is missing: {tftp}")

    for set_command, value in tftp.items():

        # To set rommon variables
        cmd = f'{set_command}={value}'
        try:
            # Set rommon variables for tftp boot
            device.execute(cmd)
        except Exception as e:
            raise SubCommandFailure(
                f"Failed to set the rommon variable {set_command}. Error:\n{e}")


def configure_rommon_tftp_ha(device, use_ipv6=False):
    """configure_rommon_tftp_ha
    This API picks up tftp information from testbed and configures rommon. The device is assumed to be in ROMMON mode already.
       Example : set IP_ADDRESS=1.1.1.1
    Args:
        device('obj'): Device object
        use_ipv6('bool', optional): To use use_ipv6. Defaults to False.
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    tftp = {}

    # Get the current device state from the device
    if device.is_ha and hasattr(device, 'subconnections'):
        if isinstance(device.subconnections, list):
            states = [con.state_machine.current_state for con in device.subconnections]
            if "rommon" not in states:
                # check the device is in rommon
                raise Exception(f'The device is not in rommon state')

    # Check if rommon attribute in device object, if not set to empty dict
    if not hasattr(device, 'rommon'):
        setattr(device, "rommon", {})

    # Getting the tftp information, if the info not provided by user, it takes from testbed
    rommon_dict = device.rommon

    def _process_tftp_boot_details(rommon_dict):
        # To process the tftp information for each rp
        tftp_details = []

        for rp, info in rommon_dict.items():

            tftp = {}

            # Add address dict logic
            address_dict = info.get('address', {})
            
            # bool to check ipv6 address
            if use_ipv6:
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

            # Add gateway dict logic
            gateway_dict = info.get('gateway', {})
            # bool to check ipv6 address
            if use_ipv6:
                gateway_ip = str(gateway_dict.get('ipv6'))
            else:
                gateway_ip = str(gateway_dict.get('ipv4'))

            tftp.update({
                "IP_ADDRESS": ip_address,
                "IP_SUBNET_MASK": subnet_mask,
                "DEFAULT_GATEWAY": gateway_ip,
                "TFTP_SERVER": str(device.testbed.servers.get('tftp', {}).get('address', '')),
            })

            # get the image from clean data
            tftp_image_path = getattr(device.clean, 'images', [])
            if tftp_image_path:
                tftp.setdefault("TFTP_FILE", tftp_image_path[0])

            log.info("checking if all the tftp information is given by the user")
            if not all(tftp.values()):
                log.warning(f"Some TFTP information is missing: {tftp}")

            tftp_details.append(tftp)
        return tftp_details

    tftp_details_list = _process_tftp_boot_details(rommon_dict)

    # check if information is there for all rps
    if len(tftp_details_list)!=len(device.subconnections):
        log.warning(f"TFTP information is missing for some subconnections")

    # rp counter to incrementally configure each rp with rommon variables
    for rp_number, con in enumerate(device.subconnections):
        for set_command, value in tftp_details_list[rp_number].items():
            # To set rommon variables
            cmd = f'{set_command}={value}'
            try:
                if con.state_machine.current_state == 'rommon':
                    con.execute(cmd)
                else:
                    break
            except Exception as e:
                raise SubCommandFailure(
                    f"Failed to set the rommon variable {set_command}. Error:\n{e}")
