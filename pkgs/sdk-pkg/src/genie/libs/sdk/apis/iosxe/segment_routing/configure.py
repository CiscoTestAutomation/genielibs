"""Common configure functions for segment-routing"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_segment_routing(device, sr_mode, block_start=None, block_end=None,
        address_family=None, ip_address=None, mask=None, index=None, in_range=None):
    """ Configures segment-routing

        Args:
            device ('obj'): device to use
            sr_mode ('str'): segment-routing mode
            block_start ('str', optional): Global block Label Range Start
            block_end ('str', optional): Global block Label Range End
            address_family ('str', optional): address-family
            ip_address ('str', optional): sid ip address
            mask ('str', optional): mask
            index ('str', optional): index, Eg: Start of SID
            in_range ('str', optional): range, Eg: Set # of SIDs in range
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface

    """

    log.debug("Configuring segment-routing")

    cmds = [f'segment-routing {sr_mode}']

    if block_start and block_end:
        cmds.append(f'global-block {block_start} {block_end}')

    if address_family:
        cmds.append('connected-prefix-sid-map')
        cmds.append(f'address-family {address_family}')
        if ip_address and mask and index:
            if in_range:
                cmds.append(f'{ip_address}/{mask} index {index} range {in_range}')
            else:
                cmds.append(f'{ip_address}/{mask} index {index}')

    try:
        device.configure(cmds)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure segment-routing. Error: {error}'.format(error=e)
        )

def unconfigure_segment_routing(device, sr_mode):
    """ Unconfigure segment-routing
        Args:
            device ('obj'): device to use
            sr_mode ('str'): segment-routing mode
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring segment-routing on the device
    """
    log.debug("Unconfigure segment-routing on the device")
    try:
        device.configure(f'no segment-routing {sr_mode}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure segment-routing on the device. Error:\n{e}"
        )
