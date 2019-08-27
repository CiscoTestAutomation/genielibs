"""Common verify functions for acl"""

# Python
import logging

from genie.libs.sdk.apis.utils import compare_config_dicts

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
