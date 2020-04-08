"""Common verification functions for Segment-Routing"""

# Python
import re
import logging

# pyATS
from genie.utils.timeout import Timeout
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys

log = logging.getLogger(__name__)  


def verify_segment_routing_policy_attributes(device, policy, expected_bsid=None, 
    expected_mode='dynamic', expected_state='programmed', policy_dict=None, 
    max_time=30, check_interval=10):
    """ Verify segment-routing policy attributes is as expected
        using 'show segment-routing traffic-eng policy name {policy}'
        
        Args:
            device (`obj`): Device object
            policy (`str`): Policy name
            expected_bsid (`int`): Expected Binding SID
            expected_mode (`str`): Expected allocation mode
            expected_state (`str`): Expected binding state
            policy_dict (`dict`): Policy dict from parser output 
                IOSXE Parser - ShowSegmentRoutingTrafficEngPolicy
                cmd - show segment-routing traffic-eng policy all
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns
            result (`bool`): Verified result
            sid (`int`): Binding sid
    """
    cmd = 'show segment-routing traffic-eng policy name {policy}'.format(policy=policy)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():

        if policy_dict is None:
            try:
                out = device.parse(cmd)
            except Exception as e:
                log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
                timeout.sleep()
                continue
        else:
            out = policy_dict

        bsid_dict = out.get(policy, {}).get('attributes', {}).get('binding_sid', {})

        if bsid_dict:
            for key, value in bsid_dict.items():
                sid = key
                mode = value.get('allocation_mode', '')
                state = value.get('state', '')
        else:
            log.error("No binding SID was found in policy '{policy}'"
                .format(policy=policy))
            timeout.sleep()
            continue

        check_sid = True
        if expected_bsid is None:
            log.info("Policy {policy} binding SID is {sid}, expected it to "
                     "be an integer".format(policy=policy, sid=sid))
            check_sid = isinstance(sid, int)
        else:
            log.info("Policy {policy} binding SID is {sid}, expected value "
                     "is {expected_bsid}".format(policy=policy,
                        sid=sid, expected_bsid=expected_bsid))
            check_sid = str(sid) == str(expected_bsid)

        log.info("Policy {policy} allocation mode is {mode}, expected value "
                 "is {expected_mode}".format(policy=policy,
                    mode=mode, expected_mode=expected_mode))
        log.info("Policy {policy} binding state is {state}, expected value "
                 "is {expected_state}".format(policy=policy,
                    state=state, expected_state=expected_state))

        if (mode.lower() == expected_mode.lower() and 
            state.lower() == expected_state.lower() and check_sid):
            return True, sid

        timeout.sleep()

    return False, None


def verify_segment_routing_policy_state(device, policy=None, expected_admin='up',
    expected_oper='up', max_time=30, check_interval=10):
    """ Verify segment-routing policy state is as expected (Admin/Operational)
        using 'show segment-routing traffic-eng policy name {policy}'
        
        Args:
            device (`obj`): Device object
            policy (`str`): Policy name, if not specified will verify all
            expected_admin (`str`): Expected admin state
            expected_oper (`str`): Expected operational state
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns
            result (`bool`): Verified result
    """
    if policy:
        cmd = 'show segment-routing traffic-eng policy name {policy}'.format(policy=policy)
    else:
        cmd = 'show segment-routing traffic-eng policy all'

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
            timeout.sleep()
            continue

        policy_list = []
        if policy:
            policy_list.append(policy)
        else:
            policy_list = list(out)

        for plc in policy_list:
            admin = out.get(plc, {}).get('status', {}).get('admin', '')
            oper = out.get(plc, {}).get('status', {}).\
                    get('operational', {}).get('state', '')

            log.info("Policy {policy} Admin state is {admin}, expected state "
                    "is {expected_admin}".format(policy=plc, admin=admin,
                        expected_admin=expected_admin))
            log.info("Policy {policy} Operational state is {oper}, expected "
                    "state is {expected_oper}".format(policy=plc,
                        oper=oper, expected_oper=expected_oper))

            if (admin.lower() != expected_admin.lower() or 
                oper.lower() != expected_oper.lower()):
                result = False

        if result:
            return True
        timeout.sleep()

    return False


def verify_segment_routing_policy_hops(device, policy, segment_list, 
    max_time=30, check_interval=10, path_type='explicit'):
    """ Verify segment-routing policy hops with order and extract labels
        using 'show segment-routing traffic-eng policy name {policy}'
        
        Args:
            device (`obj`): Device object
            policy (`str`): Policy name
            segment_list (`list`): Segment list to verify
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
            path_type (`int`): Tath Type, default: explicit
        Returns
            result (`bool`): Verified result
            labels (`list`): Hops labels
    """
    cmd = 'show segment-routing traffic-eng policy name {policy}'.format(policy=policy)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
            timeout.sleep()
            continue

        # Get label or ip value to verify (with order)
        slist = []
        p = re.compile(r'[\d\.]+$')
        for line in segment_list:
            value = p.search(line).group()
            if value:
                slist.append(value)
        reqs = R([policy,'candidate_paths',
                'preference','(?P<preference>.*)',
                'path_type', path_type,
                '(?P<category>.*)','(?P<name>.*)',
                'hops','(?P<hops>.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)
        # for dynamic path type
        reqs2 = R([policy,'candidate_paths',
                'preference','(?P<preference>.*)',
                'path_type', path_type,
                'hops','(?P<hops>.*)'])
        found2 = find([out], reqs2, filter_=False, all_keys=True)
        labels = []
        result = True
        # if can't find explicit type, try the dynamic one
        if not found:
            found = found2
        if found:
            item = found[0][0]
            if len(item) == len(slist):
                for index, dct in sorted(item.items()):
                    s_value = slist[index-1]
                    sid = dct.get('sid', '')
                    local_address = dct.get('local_address', '')
                    remote_address = dct.get('remote_address', '')
                    log.info("Expect '{val}' is present in label '{sid}', "
                             "or local_address '{local_address}', or "
                             "remote_address '{remote_address}'".format(
                                 val=s_value, sid=sid, 
                                 local_address=local_address, 
                                 remote_address=remote_address))
                    if (s_value == str(sid) or 
                        s_value == local_address or 
                        s_value == remote_address):
                        labels.append(sid)
                    else:
                        result = False
            else:
                log.error("The length of segment list does not match:\n"
                          "Configured value: {conf}   Operational value: {oper}"
                            .format(conf=len(item), oper=len(slist)))
                result = False
        else:
            log.error("Failed to find any hop in policy '{policy}'".format(policy=policy))
            result = False

        if result:
            return result, labels

        timeout.sleep()

    return False, None


def verify_segment_routing_dynamic_metric_type(device, policy, expected_type='TE', 
    max_time=30, check_interval=10):
    """ Verify segment-routing metric type under dynamic path with active state
        using 'show segment-routing traffic-eng policy name {policy}'
        
        Args:
            device (`obj`): Device object
            policy (`str`): Policy name
            expected_type (`str`): Expected metric type
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns
            result (`bool`): Verified result
    """
    cmd = 'show segment-routing traffic-eng policy name {policy}'.format(policy=policy)
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
            timeout.sleep()
            continue

        reqs = R([policy,'candidate_paths',
                'preference','(?P<preference>.*)',
                'path_type','dynamic','(?P<path>.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)

        for item in found:
            if item[0]['status'].lower() == 'active':
                metric_type = item[0]['metric_type']
                break
        else:
            log.error("Failed to find a dynamic path in active state")
            timeout.sleep()
            continue

        log.info("Policy {policy} active dynamic path's metric_type is "
                 "{metric_type}, expected type is {expected_type}".format(
                     policy=policy, metric_type=metric_type, 
                     expected_type=expected_type))

        if (metric_type.lower() == expected_type.lower()):
            return True

        timeout.sleep()
    
    return False


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
                if address_family == "ipv4"
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


def verify_segment_routing_traffic_eng_policies(device, policy_name=None, expected_preference=None, expected_admin_status=None,
                                                expected_oper_status=None, expected_metric_type=None,
                                                expected_path_accumulated_metric=None, expected_path_status=None,
                                                expected_affinity_type=None, expected_affinities=None,
                                                expected_endpoint_ip=None,
                                                max_time=30, check_interval=10):
    """ Verifies configured traffic_eng policies have expected configurations

        Args:
            device ('obj'): Device to use
            policy_name ('str'): Policy name to verify. If not specified will verify all
            expected_admin_status ('str'): Expected admin status
            expected_oper_status ('str'): Expected operational status
            expected_metric_type ('str'): Expected metric type
            expected_path_accumulated_metric ('int'): Expected path accumulated metric
            expected_path_status ('str'): Expected path status
            expected_affinity_type ('str'): Expected affinity type
            expected_affinities ('list'): Expected affinities
            expected_preference ('int'): Expected preference path 
            expected_endpoint_ip ('str'): Expected Endpoint IP
            max_time ('int'): Maximum amount of time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    if (not expected_admin_status and
            not expected_oper_status and
            not expected_metric_type and
            not expected_path_accumulated_metric and
            not expected_path_status and
            not expected_affinity_type and
            not expected_affinities and
            not expected_endpoint_ip):
        log.info('Must provide at-least one optional argument to verify')
        return False

    if policy_name:
        cmd = 'show segment-routing traffic-eng policy name {policy}'.format(policy=policy_name)
    else:
        cmd = 'show segment-routing traffic-eng policy all'

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            log.info('Parser output is empty')
            timeout.sleep()
            continue
        for policy in out:
            if expected_endpoint_ip:
                endpoint_ip = out[policy].get('end_point', None)
                if endpoint_ip != expected_endpoint_ip:
                    # Check other policy
                    continue
            admin = out[policy].get('status', {}).get('admin', '')
            if expected_admin_status and expected_admin_status != admin:
                log.info('Expected admin status is "{admin_status}" actual is "{admin}"'
                         .format(admin_status=expected_admin_status,
                                 admin=admin))
                break            
            operational = out[policy].get('status', {}).get('operational', {}).get('state', '')
            if expected_oper_status and expected_oper_status != operational:
                log.info('Expected operational status is "{operational_status}" actual is "{operational}"'
                         .format(operational_status=expected_oper_status,
                                 operational=operational))
                break

            for preference in out[policy].get('candidate_paths', {}).get('preference', {}):
                if expected_preference and expected_preference != preference:
                    continue
                if out[policy]['candidate_paths']['preference'][preference].get('path_type'):
                    path_type_dict = out[policy]['candidate_paths']['preference'][preference]['path_type']

                    if 'dynamic' in path_type_dict:
                        metric = path_type_dict['dynamic'].get('metric_type', '')
                        if expected_metric_type and expected_metric_type != metric:
                            log.info('Expected metric type for path {path} is "{expected}" actual is "{actual}"'
                                     .format(
                                         expected=expected_metric_type, 
                                         actual=metric,
                                         path=preference))
                            break

                        status = path_type_dict['dynamic'].get('status', '')
                        if expected_path_status and expected_path_status != status:
                            log.info('Expected status for path {path} is "{expected}" actual is "{actual}"'
                                     .format(
                                         expected=expected_path_status, 
                                         actual=status,
                                         path=preference))
                            break

                        accumulated_metric = path_type_dict['dynamic'].get('path_accumulated_metric', '')
                        if (expected_path_accumulated_metric and
                                isinstance(accumulated_metric, int) and
                                expected_path_accumulated_metric != accumulated_metric):
                            log.info('Expected accumulated metric for path {path} is "{expected}" actual is "{actual}"'
                                     .format(
                                         expected=expected_path_accumulated_metric, 
                                         actual=accumulated_metric,
                                         path=preference))
                            break

                    elif 'explicit' in path_type_dict:
                        for segment in path_type_dict['explicit'].get('segment_list', {}):
                            metric = path_type_dict['explicit'].get('segment_list', {}).get(segment, {}).get('metric_type', '')

                            if expected_metric_type and expected_metric_type != metric:
                                log.info('Expected metric type for path {path} is "{expected}" actual is "{actual}"'
                                         .format(
                                             expected=expected_metric_type, 
                                             actual=metric,
                                             path=preference))
                                break

                            status = path_type_dict['explicit'].get('segment_list', {}).get(segment, {}).get('status', '')
                            if expected_path_status and expected_path_status != status:
                                log.info('Expected path status for path {path} is "{expected}" actual is "{actual}"'
                                         .format(expected=expected_path_status, 
                                                actual=status,
                                                path=preference))
                                break

                        else:
                            continue
                        break

                    else:
                        log.info('Path type not defined in api call.')
                        break

                if out[policy]['candidate_paths']['preference'][preference].get('constraints'):
                    constraint_dict = out[policy]['candidate_paths']['preference'][preference]['constraints']

                    if expected_affinity_type and expected_affinity_type not in constraint_dict.get('affinity', {}):
                        log.info('Expected affinity_type is for path {path} "{expected}". Actual is "{actual}"'
                                 .format(expected=expected_affinity_type,
                                         actual=list(constraint_dict.keys()),
                                         path=preference))
                        break

                    if expected_affinities:
                        for aff_type in constraint_dict.get('affinity', {}):
                            if not set(expected_affinities).issubset(constraint_dict['affinity'][aff_type]):
                                log.info('Expected affinities "{expected}" for path {path} are not set'
                                         .format(expected=expected_affinities,
                                                path=preference))
                                break

                        else:
                            continue
                        break

            else:
                continue
            break

        else:
            return True
        
        timeout.sleep()

    return False
