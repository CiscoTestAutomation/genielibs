"""Common verify functions for show boot config"""

import logging

from genie.utils.timeout import Timeout
from genie.libs.sdk.apis.utils import compare_config_dicts
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_boot_mode_lxc_config(device, max_time=15, check_interval=5):
    """
    verify that lxc boot mode config exist in the device
    Args:
        device (`obj`): Device object
        max_time ('int', optional) : max time to wait, default value is 15 seconds.
        interval ('int', optional) : interval timer, default value is 5 seconds.
    Returns:
        True
        False
    Raises:
        None
    """
  
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse("show boot mode")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        bootmode = output.get('bootmode','')
        if bootmode == 'LXC':
           log.info("LXC config is enabled")
           return True
        else:
           timeout.sleep()

    log.info("LXC config is not enabled")
    return False

def verify_boot_mode_lxc_unconfig(device, max_time=15, check_interval=5):
    """
    verify that lxc boot mode config does not exist in the device
    Args:
        device (`obj`): Device object
        max_time ('int', optional) : max time to wait, default value is 15 seconds.
        interval ('int', optional) : interval timer, default value is 5 seconds.
    Returns:
        True
        False
    Raises:
        None
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse("show boot mode")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        bootmode = output.get('bootmode','')
        if bootmode != 'LXC':
           log.info("LXC config is not enabled")
           return True
        else:
           timeout.sleep()

    log.info("LXC config is enabled")
    return False
