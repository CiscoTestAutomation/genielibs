"""Common verify functions for acl"""

# Python
import logging
import re

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

def verify_acl_log(device, acl_name, rule, protocol):
    """ Verify acl log messages when log option is enabled

        Args:
            device (`obj`): Device object
            acl_name (`str`): ACL name
            rule ('str'): permitted|denied
            protocol ('str'): protocol to be matched
        Returns:
            True : returns true in case of passed scenario
            False : returns false if not expected output
    """
    result = []
    out = device.parse("show logging | include IPV6_ACL-6-ACCESSLOG")
    p = re.compile(r".*IPV6_ACL-6-ACCESSLOG.*{acl_name}\S+\s{rule}\s{protocol}.*".format(
                   acl_name=acl_name,
                   rule=rule,
                   protocol=protocol)
    )

    return any(p.match(line) for line in out["logs"])

def verify_acl_info_summary(
        device,
        acl_name,
        expected_protocol,
        expected_no_of_aces,
        expected_direction_ingress=None,
        expected_direction_egress=None,
        max_time = 15,
        check_interval = 5
):
    """ Verify acl info summary
        Args:
            device (`obj`): Device object
            acl_name (`str`): Name of ACL
            expected_protocol ('str'): Expected protocol IPv4|IPv6
            expected_no_of_aces ('int'): Expected number of aces
            expected_direction_ingress ('str'): Expected direction Ingress Y or N
            expected_direction_egress ('str'): Expected direction Egress Y or N
            max_time ('int',optional): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (`int`, optional): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True : returns true in case of passed scenario
            False : returns false if not expected output
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show platform software fed active acl info summary")
        except SchemaEmptyParserError:
            return False
        acl = out['acl_name'][acl_name]
        get_acl_protocol = acl['protocol']
        get_no_of_aces = acl['no_of_aces']
        if expected_direction_ingress:
            get_acl_direction = acl['direction_ingress']
            return (expected_protocol, expected_no_of_aces, expected_direction_ingress) == (get_acl_protocol, get_no_of_aces, get_acl_direction)

        else:
            get_acl_direction = acl['direction_egress']
            return (expected_protocol, expected_no_of_aces, expected_direction_egress) == (get_acl_protocol, get_no_of_aces, get_acl_direction)

    return False

def verify_ipv6_acl_tcam_utilization(
        device,
        slice_id,
        direction,
        expected_acl_mem_usage
):
    """ Verify ipv6 acl tcam utilization
        Args:
            device (`obj`): Device object
            slice_id (`int`): Slice ID
            direction ('str'): Ingress or egress
            expected_acl_mem_usage ('int'): Expected ACL entries memory usage

        Returns:
            True : returns true in case of passed scenario
            False : returns false if not expected output
    """
    try:
        out = device.parse("show platform hardware fed active fwd-asic resource tcam utilization")
    except SchemaEmptyParserError:
        return False

    get_acl_mem_usage = ''
    slice = f'Slice{slice_id}'

    #Intrepid has ports distributed in different slices, hence checking the memory usage of the required slice
    if 0 <= int(slice_id) <= 5:
        used_slice_id = f'{"inw_" if direction == "ingress" else ""}used{slice_id}'
        get_acl_mem_usage = out[slice][used_slice_id]

        return (expected_acl_mem_usage == get_acl_mem_usage)

    return False

def verify_object_manager_error_objects_statistics(
        device,
        sp_type,
        expected_error_objects
):
    """ Verify show platform software object-manager {sp_type} statistics
        Args:
            device (`obj`): Device object
            sp_type (`str`): fp active | fp standby
            expected_error_objects (`int`): expected no.of error objects

        Returns:
            True : returns true in case of passed scenario
            False : returns false if not expected output
    """
    try:
        out = device.parse("show platform software object-manager {} statistics".format(sp_type))
    except SchemaEmptyParserError:
        return False

    get_error_objects = out['statistics']['error-objects']
    return expected_error_objects == get_error_objects

