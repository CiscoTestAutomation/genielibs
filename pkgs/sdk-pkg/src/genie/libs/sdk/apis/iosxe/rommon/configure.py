''' Common Config functions for rommon'''

import logging
import re
from contextlib import contextmanager
from contextvars import ContextVar
from pyats.utils.schemaengine import SchemaError
log = logging.getLogger(__name__)
# Unicon
from unicon.core.errors import SubCommandFailure
from genie.libs.clean.utils import get_image_handler
from genie.libs.sdk.apis.iosxe.rommon.get import _normalize_image_paths
from genie.libs.sdk.libs.utils.utils import get_recovery_tftp_server
import ipaddress
from ipaddress import IPv4Address, IPv6Address, IPv4Interface, IPv6Interface, ip_interface



# Legacy configuration providers discard the delegated API return value.
# Capture the actual path at that delegation boundary without device-global state.
_rommon_tftp_image_capture = ContextVar('rommon_tftp_image_capture', default=None)


@contextmanager
def _capture_rommon_tftp_image():
    """Collect successfully configured transport paths in this provider call."""
    images = []
    token = _rommon_tftp_image_capture.set(images)
    try:
        yield images
    finally:
        _rommon_tftp_image_capture.reset(token)


def _record_rommon_tftp_image(image_path):
    images = _rommon_tftp_image_capture.get()
    if images is not None:
        images.append(image_path)


def _get_rommon_tftp_image(device, image_path):
    """Validate the primary image before configuring ROMMON."""
    if image_path is None:
        image_handler = get_image_handler(device)
        image_path = getattr(image_handler, 'image', None)
    try:
        return _normalize_image_paths(image_path)[0]
    except (SchemaError, ImportError) as e:
        raise SubCommandFailure(f'Invalid ROMMON TFTP image metadata: {e}') from e


def _verify_rommon_tftp_file(device, image_path, connection=None):
    """Verify the configured transport path in the supported Cat9k environment."""
    # These platform paths support `set` environment readback. Do not assume
    # that untested IOS-XE ROMMON implementations support the same command.
    if (getattr(device, 'platform', None) != 'cat9k' or
            getattr(device, 'model', None) not in ('c9300', 'c9200')):
        return
    environment = (connection if connection is not None else device).execute('set')
    lines = environment.splitlines() if isinstance(environment, str) else []
    # A nested Unicon execute can retain the assignment echo before the query
    # prompt. Ignore only that echo, never a value in the returned environment.
    if (len(lines) >= 2 and lines[0].startswith('TFTP_FILE=') and
            re.fullmatch(r'switch:\s*(?:set)?', lines[1])):
        lines = lines[2:]
    paths = [line[len('TFTP_FILE='):] for line in lines if line.startswith('TFTP_FILE=')]
    if paths != [image_path]:
        raise SubCommandFailure(
            f'ROMMON TFTP_FILE readback did not match selected image {image_path!r}. '
            'Check ROMMON assignment support and console output; aborting boot '
            'to avoid an existing/stale TFTP_FILE value.')


def configure_rommon_tftp(device, use_ipv6=False, image_path=None):
    """configure_rommon_tftp 
    This API picks up tftp information from testbed and configures rommon. The device is assumed to be in ROMMON mode already.
       Example : set IP_ADDRESS=1.1.1.1
    Args:
        device('obj'): Device object
        use_ipv6('bool', optional): To use use_ipv6. Defaults to False.
        image_path: Primary image path or supported Clean image/file metadata.
            None uses the platform-validated Clean image. Empty or ambiguous
            metadata fails without configuring ROMMON variables.
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

    selected_image = _get_rommon_tftp_image(device, image_path)

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

    tftp_server = get_recovery_tftp_server(device)
    tftp.setdefault("TFTP_SERVER", str(tftp_server))

    tftp["TFTP_FILE"] = selected_image

    log.info("checking if all the tftp information is given by the user")
    if not all(tftp.values()):
        log.warning(f"Some TFTP information is missing: {tftp}")

    for set_command, value in tftp.items():

        # To set rommon variables
        cmd = f'{set_command}={value}'
        try:
            # Set rommon variables for tftp boot
            device.execute(cmd)
            if set_command == 'TFTP_FILE':
                _verify_rommon_tftp_file(device, selected_image)
        except Exception as e:
            raise SubCommandFailure(
                f"Failed to set the rommon variable {set_command}. Error:\n{e}")

    _record_rommon_tftp_image(selected_image)


def configure_rommon_tftp_ha(device, use_ipv6=False, image_path=None):
    """configure_rommon_tftp_ha
    This API picks up tftp information from testbed and configures rommon. The device is assumed to be in ROMMON mode already.
       Example : set IP_ADDRESS=1.1.1.1
    Args:
        device('obj'): Device object
        use_ipv6('bool', optional): To use use_ipv6. Defaults to False.
        image_path: Primary image path or supported Clean image/file metadata.
            None uses the platform-validated Clean image. Empty or ambiguous
            metadata fails before configuring any RP.
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

    # Check if management attribute in device object, if not set to empty dict
    if not hasattr(device, 'management'):
        setattr(device, "management", {})
    management_dict = device.management
    rommon_dict = management_dict.setdefault('rommon', {})
    # Valid RP entries (rp0, rp1, ...) are sorted numerically and then
    # mapped positionally to device.subconnections. Changing this mapping
    # requires a separate schema/API change.
    rp_details = dict(
        sorted(
            ((rp, info) for rp, info in rommon_dict.items()
             if (isinstance(rp, str) and
                 rp.lower().startswith('rp') and
                 rp[2:].isdigit())),
            key=lambda item: int(item[0][2:])))
    address_key = 'ipv6' if use_ipv6 else 'ipv4'

    # Check the selected address family before building ROMMON commands.
    address_family = 'IPv6' if use_ipv6 else 'IPv4'
    rommon_fields = ('address', 'gateway')
    missing_information = []
    rp_entries = list(rp_details.values())
    for rp_number, connection in enumerate(device.subconnections):
        rp_info = (rp_entries[rp_number]
                   if rp_number < len(rp_entries) else {})
        missing_fields = []
        for section in rommon_fields:
            section_details = (rp_info.get(section, {})
                               if isinstance(rp_info, dict) else {})
            if (not isinstance(section_details, dict) or
                    not section_details.get(address_key)):
                missing_fields.append(
                    f'ROMMON {address_family} {section} '
                    f'({section}.{address_key})')

        if missing_fields:
            missing_field_text = '\n  - '.join(missing_fields)
            missing_information.append(
                f"Missing ROMMON recovery information for "
                f"subconnection '{connection.alias}':\n"
                f'  - {missing_field_text}')

    if missing_information:
        raise SubCommandFailure('\n'.join(missing_information))

    selected_image = _get_rommon_tftp_image(device, image_path)

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

            tftp_server = get_recovery_tftp_server(device)
            tftp.update({
                "IP_ADDRESS": ip_address,
                "IP_SUBNET_MASK": subnet_mask,
                "DEFAULT_GATEWAY": gateway_ip,
                "TFTP_SERVER": str(tftp_server),
            })

            tftp["TFTP_FILE"] = selected_image

            log.info("checking if all the tftp information is given by the user")
            if not all(tftp.values()):
                log.warning(f"Some TFTP information is missing: {tftp}")

            tftp_details.append(tftp)
        return tftp_details

    tftp_details_list = _process_tftp_boot_details(rp_details)

    # rp counter to incrementally configure each rp with rommon variables
    for rp_number, con in enumerate(device.subconnections):
        for set_command, value in tftp_details_list[rp_number].items():
            cmd = f'{set_command}={value}'
            try:
                if con.state_machine.current_state == 'rommon':
                    log.info(f"{device.name} rp{rp_number}: executing ROMMON cmd: {cmd}")
                    con.execute(cmd)
                    if set_command == 'TFTP_FILE':
                        _verify_rommon_tftp_file(device, selected_image, connection=con)
                else:
                    break
            except Exception as e:
                log.error(f"{device.name} rp{rp_number}: ROMMON cmd failed: {cmd} ({e})")
                raise

    _record_rommon_tftp_image(selected_image)
