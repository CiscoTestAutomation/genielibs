"""Common verification functions for Segment-Routing"""

# Python
import logging

# pyATS
from genie.utils.timeout import Timeout
from ats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys

log = logging.getLogger(__name__)


def verify_sid_in_segment_routing(device, address_family="ipv4", local=False):
    """ Verifies if SID is found in segment-routing
        from command 'show segment-routing mpls connected-prefix-sid-map ipv4' or
        from command 'show segment-routing mpls connected-prefix-sid-map local ipv4'
        
        Args:
            device (`obj`): Device to be executed command
            address_family (`str`): Address family name
            local (`bool`): Flag to check command with local

        Raises:
            None
        Returns
            True/False

    """

    try:
        if local:
            out = device.parse(
                "show segment-routing mpls connected-prefix-sid-map local {}".format(
                    address_family
                ),
                local=True,
            )
        else:
            out = device.parse(
                "show segment-routing mpls connected-prefix-sid-map {}".format(
                    address_family
                )
            )
    except (SchemaEmptyParserError):
        return False
    sid_count = 0
    try:
        sid_count = len(
            out["segment_routing"]["bindings"]["connected_prefix_sid_map"][
                address_family
            ][
                "ipv4_prefix_sid"
                if address_family is "ipv4"
                else "ipv6_prefix_sid"
            ].keys()
        )
    except KeyError:
        pass
    return sid_count != 0


def verify_status_of_segment_routing(device, state="ENABLED"):
    """ Verifies if state matches expected_state state in segment-routing
        from command 'show segment-routing mpls state'

        Args:
            device (`obj`): Device to be executed command
            state (`str`): Expected state
        Raises:
            None
        Returns
            True/False

    """

    state_found = None
    try:
        out = device.parse("show segment-routing mpls state")
    except (SchemaEmptyParserError):
        return False
    try:
        state_found = out["sr_mpls_state"]
    except KeyError:
        return False
    return state_found.upper() == state.upper()


def verify_ip_and_sid_in_segment_routing(device, address_sid_dict, algorithm, 
    address_family='ipv4', local=False, max_time=90, check_interval=10, 
    expected_result=True):
    """ Verifies if IP address and SID is present in Segment Routing
        from command 'show segment-routing mpls connected-prefix-sid-map local <address_family>' or
        from command 'show segment-routing mpls connected-prefix-sid-map <address_family>'
        Args:
            device (`obj`): Device to be executed command
            address_sid_dict (`dict`): Dictionary containing ip address and SID as key and value pair
            ex.)
                {
                    '10.4.1.1/32': 1,
                    '10.4.1.2/32': 2,
                } 
            algorithm (`str`): Algorithm to check
            ex.) 
                algorithm = 'ALGO_0'
            address_family (`str`): Address family
            local (`bool`): Flag to check command with local
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check
            expected_result ('bool'): Expected result
                set expected_result = False if method should fail
                set expected_result = True if method should pass (default value)
                
        Raises:
            None
        Returns
            True/False

    """

    prefix_mapping = {
        'ipv4': 'ipv4_prefix_sid',
        'ipv6': 'ipv6_prefix_sid'
    }

    prefix_mapping_local = {
        'ipv4': 'ipv4_prefix_sid_local',
        'ipv6': 'ipv6_prefix_sid_local'
    }
    
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            if local:
                out = device.parse(
                    "show segment-routing mpls connected-prefix-sid-map local {}".format(address_family)
                )
            else:
                out = device.parse(
                    "show segment-routing mpls connected-prefix-sid-map {}".format(address_family)
                )
        except (SchemaEmptyParserError):
            pass
        
        found_local = None
        found = None 
        
        for ip_address, sid in address_sid_dict.items():
            
            # find using Prefix SID local
            # It will use ipv4_prefix_sid_local or ipv6_prefix_sid_local as key for search data
            # based on address_family provided
            sid = str(sid)
            if out:
                reqs_local = R(
                    ['segment_routing',
                    'bindings',
                    'local_prefix_sid',
                    address_family,
                    prefix_mapping_local[address_family],
                    ip_address,
                    'algorithm',
                    algorithm,
                    'sid',
                    sid]
                )
                
                # find using just Prefix SID
                # It will use ipv4_prefix_sid or ipv6_prefix_sid as key for search data
                # based on address_family provided
                reqs = R(
                    ['segment_routing',
                    'bindings',
                    'connected_prefix_sid_map',
                    address_family,
                    prefix_mapping[address_family],
                    ip_address,
                    'algorithm',
                    algorithm,
                    'sid',
                    sid]
                )
                
                found_local = find([out], reqs_local, filter_=False, all_keys=True)
                found = find([out], reqs, filter_=False, all_keys=True)
                
                # Returns false if SID is not found Prefix SID or Prefix SID local
                if not expected_result and (not found_local or not found):
                    return expected_result
        
        if expected_result and found_local and found:
            return expected_result
        
        timeout.sleep()

    return False

def verify_segment_routing_lb_range(
    device,
    expected_minimum=None,
    expected_maximum=None,
    max_time=30,
    check_interval=10,
):
    """ Verifies the segment routing lb range is as expected

        Args:
            device ('obj'): device to use
            expected_minimum ('int'): expected label range minimum to compare against. Ignored if None
            expected_maximum ('int'): expected label range maximum to compare against. Ignored if None
            max_time ('int'): maximum time to keep checking
            check_interval ('int'): how often to check

        Returns:
            True/False

        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        minimum, maximum = device.api.get_segment_routing_lb_range(
            device=device
        )
        if not (
            (expected_minimum and expected_minimum != minimum)
            or (expected_maximum and expected_maximum != maximum)
        ):
            return True

        if expected_minimum and expected_minimum != minimum:
            log.info(
                "Actual minimum of {actual} does not equal expected minimum of {expected}".format(
                    actual=minimum, expected=expected_minimum
                )
            )

        if expected_maximum and expected_maximum != maximum:
            log.info(
                "Actual maximum of {actual} does not equal expected maximum of {expected}".format(
                    actual=maximum, expected=expected_maximum
                )
            )

        timeout.sleep()

    return False


def verify_segment_routing_gb_range(
    device,
    expected_minimum=None,
    expected_maximum=None,
    max_time=30,
    check_interval=10,
):
    """ Verifies the segment routing gb range is as expected

        Args:
            device ('obj'): device to use
            expected_minimum ('int'): expected label range minimum to compare against. Ignored if None
            expected_maximum ('int'): expected label range maximum to compare against. Ignored if None
            max_time ('int'): maximum time to keep checking
            check_interval ('int'): how often to check

        Returns:
            True/False

        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        minimum, maximum = device.api.get_segment_routing_gb_range(
            device=device
        )
        if not (
            (expected_minimum and expected_minimum != minimum)
            or (expected_maximum and expected_maximum != maximum)
        ):
            return True

        if expected_minimum and expected_minimum != minimum:
            log.info(
                "Actual minimum of {actual} does not equal expected minimum of {expected}".format(
                    actual=minimum, expected=expected_minimum
                )
            )

        if expected_maximum and expected_maximum != maximum:
            log.info(
                "Actual maximum of {actual} does not equal expected maximum of {expected}".format(
                    actual=maximum, expected=expected_maximum
                )
            )

        timeout.sleep()

    return False

def verify_ip_and_sid_in_segment_routing_mapping_server(device, address_sid_dict, address_family, 
    algorithm, mapping_server, max_time=300, check_interval=30, expected_result=True, output=None):
    """ Verifies if IP address and SID is present in Segment Routing mapping server
        from show segment-routing mpls mapping-server {address_family}'
        Args:
            device (`obj`): Device to be executed command
            address_family (`str`): Address family
            address_sid_dict (`dict`): Dictionary containing ip address and SID as key and value pair
            ex.)
                {
                    '10.4.1.1/32': 1,
                    '10.4.1.2/32': 2,
                } 
            algorithm (`str`): Algorithm to check
            ex.) 
                algorithm = 'ALGO_0' 
            mapping_server (`str`): mapping server to check
            ex.)
                mapping_server = 'PREFIX_SID_EXPORT_MAP'   or
                mapping_server = 'PREFIX_SID_REMOTE_EXPORT_MAP'
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check
            expected_result ('bool'): Expected result
                set expected_result = False if method should fail
                set expected_result = True if method should pass (default value)
                
        Raises:
            None
        Returns
            True/False

    """

    mapping_dict_export = {
        'ipv4': 'ipv4_prefix_sid_export_map',
        'ipv6': 'ipv6_prefix_sid_export_map',
    }

    mapping_dict_remote_export = {
        'ipv4': 'ipv4_prefix_sid_remote_export_map',
        'ipv6': 'ipv6_prefix_sid_remote_export_map',
    }
    
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = None
            if output:
                out = device.parse(
                    "show segment-routing mpls mapping-server {}".format(address_family),
                    output=output
                )
            else:
                out = device.parse(
                    "show segment-routing mpls mapping-server {}".format(address_family)
                )
            output = None
        except (SchemaEmptyParserError):
            pass
        
        found = None

        for ip_address, sid in address_sid_dict.items():
            
            # find using Prefix SID local
            # It will use ipv4_prefix_sid_local or ipv6_prefix_sid_local as key for search data
            # based on address_family provided
            if out:
                reqs = R(
                    ['segment_routing',
                    'bindings',
                    'mapping_server',
                    'policy',
                    mapping_server.lower(),
                    address_family,
                    'mapping_entry',
                    ip_address,
                    'algorithm',
                    algorithm,
                    'sid',
                    sid]
                )
                
                found = find([out], reqs, filter_=False, all_keys=True)
                
            # Returns false if SID is not found Prefix SID or Prefix SID local
            if not expected_result and not found:
                return expected_result
        if expected_result and found:
            return expected_result
        
        if not found:
            timeout.sleep()

    return False