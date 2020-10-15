"""Common verify functions for routing"""

# Python
import re
import logging

# pyATS
from genie.utils import Dq

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.libs.sdk.apis.utils import get_config_dict

# Unicon
from unicon.core.errors import SubCommandFailure


log = logging.getLogger(__name__)


def verify_config_exists_in_routing_options(device, regex,
    max_time=60, check_interval=10):
    """ Verify maximum-path exists in configuration

        Args:
            device (`obj`): Device object
            regex (`str`): Config to search
            max_time (`int`): Max time, default: 60
            check_interval (`int`): Check interval, default: 10
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.execute('show configuration routing-options')
        except SubCommandFailure as e:
            timeout.sleep()
            continue
        if not out:
            return False
        config_dict = get_config_dict(out)
        config_found = Dq(config_dict).contains(regex, regex=True)
        if config_found:
            return True
        timeout.sleep()
    return False