"""Common verify functions for fips"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_fips_auth_key(device, expected_auth_key, st_key, max_time=60, check_interval=10):
    """Verify fips authorization-key

        Args:
            device (`obj`): Device object
            expected_auth_key(`str`): expected authorization key
            st_key(`str`): Actual key
            max_time (`int`): max time
            check_interval (`int`): check interval

        Returns:
            result(`bool`): verify result
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show fips authorization-key")
        except SchemaEmptyParserError:
            pass
        if out:
            get_key = out['fips']['stored_key'][st_key]
            if expected_auth_key == get_key:
                return True
            
        timeout.sleep()
    return False
        