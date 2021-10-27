"""Common verify functions for acl"""

# Python
import logging

from genie.utils.timeout import Timeout
from genie.libs.sdk.apis.utils import compare_config_dicts
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_acl_applied(device, acl_name, applied_config):
    """ Verify if access list is correctly applied
        Args:
            device ('obj'): Device object
            acl_name ('str'): Access list name
            applied_config ('str'): Output from acl.configure.config_extended_acl
        Raises:
            None
        Returns:
            True
            False

    """
    log.info("Verify access-list {} is correctly programmed".format(acl_name))
    parsed_config = device.parse("show ip access-lists", output=applied_config)
    parsed_output = device.parse("show ip access-lists {}".format(acl_name))

    result = compare_config_dicts(parsed_config, parsed_output)
    if result:
        log.info("Diff:\n{}".format(result))
        return False

    return True


def verify_acl_usage(
        device,
        expected_acl_type,
        acl_id,
        max_time=15,
        check_interval=5
):
    """ Verify acl usage
        Args:
            device (`obj`): Device object
            expected_acl_type (`str`): type of ACL
            acl_id (`str`): Name of ACL
            max_time ('int',optional): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (`int`, optional): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show platform software fed active acl usage")
        except SchemaEmptyParserError:
            pass
        
        if out:
            get_acl_type = out['acl_usage']['acl_name'][acl_id]['direction']['Ingress']['feature_type']
            if expected_acl_type == get_acl_type:
                return True
            
        timeout.sleep()
        
    return False
