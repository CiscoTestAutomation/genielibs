"""Common verification functions for OSPF"""

# Python
import re
import logging
from prettytable import PrettyTable

# pyATS
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys

# OSPF
from genie.libs.sdk.apis.iosxe.ospf.get import (
    get_ospf_neighbors_in_state,
    get_ospf_neighbors,
)

log = logging.getLogger(__name__)


def verify_ospf_database_flag(device, lsa_id, expected_flag, has_flag=True,
                              max_time=30, check_interval=10):
    """ Verify ospf database flag does (not) have expected value

        Args:
            device (`obj`): Device object
            lsa_id (`str`): Link State ID
            expected_flag (`str`): Expected flag value
            has_flag (`bool`): True if expect to contain flag
                               False if expect not to contain flag
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            result (`bool`): Verified result
    """
    timeout = Timeout(max_time, check_interval)
    cmd = 'show ip ospf database opaque-area {} self-originate'.format(lsa_id)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{}':\n{}".format(cmd, e))
            timeout.sleep()
            continue

        reqs = R(['vrf', '(.*)', 'address_family', '(.*)',
                  'instance', '(.*)', 'areas', '(.*)',
                  'database', 'lsa_types', '(.*)',
                  'lsas', '(.*)', 'ospfv2', 'body',
                  'opaque', 'extended_prefix_tlvs', '(.*)',
                  'sub_tlvs', '(.*)', 'flags', '(?P<flags>.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={},
                                         source=found, all_keys=True)
        else:
            log.error("Failed to get flags from ospf database with Link State ID: '{}'"
                .format(lsa_id))
            timeout.sleep()
            continue

        if len(keys) == 1:
            flags = keys[0]['flags']
        else:
            log.error("Found multiple items {}, expected to have only one item"
                .format(keys))
            timeout.sleep()
            continue

        if has_flag:
            log.info("Found flags '{}' in ospf database, expected to contain '{}'"
                .format(flags, expected_flag))
            if expected_flag in flags:
                return True
        else:
            log.info("Found flags '{}' in ospf database, expected not to contain '{}'"
                .format(flags, expected_flag))
            if expected_flag not in flags:
                return True

        timeout.sleep()

    return False


def verify_ospf_max_metric_configuration(device, ospf_process_id, 
    metric_value, expected_state, max_time=15, check_interval=5):
    """Verify OSPF max-metric configuration

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process ID
            metric_value (`int`): Metric value to be configured
            expected_state (`str`): State to check
            max_time (int): Maximum wait time for the trigger,
                             in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result(`bool`): verify result
            state
    """
    cmd = "show ip ospf max-metric"
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse {cmd}: {e}".format(cmd=cmd, e=e))
            timeout.sleep()
            continue

        reqs = R(['vrf', '(.*)',
                  'address_family', 'ipv4',
                  'instance', str(ospf_process_id),
                  'base_topology_mtid', '(?P<mtid>.*)',
                  'router_lsa_max_metric', True, '(?P<sub>.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)

        if found:
            for item in found:
                condition = item[0].get('condition', '')
                state = item[0].get('state', '')
                if not state:
                    log.error("Failed to get max metric state")
                    break

                log.info("Max metric state is '{state}', expected state is '{exp}'"
                    .format(state=state, exp=expected_state))

                log.info("Configured metric value is '{val}', expected it in '{con}'"
                    .format(val=metric_value, con=condition))

                if (str(metric_value) in condition and 
                    state.lower() == expected_state.lower()):
                    return True
        else:
            log.error("Failed to get max-metric information for ospf id {id}"
                .format(id=ospf_process_id))

        timeout.sleep()

    return False


def verify_ospf_neighbor_state(device, state, max_time=15, check_interval=5):
    """Verify OSPF neighbor is state

        Args:
            device (`obj`): Device object
            state (`str`): State to check for neighbor
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True
            False        
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ip ospf neighbor")
        except SchemaEmptyParserError:
            pass
        if out:
            try:
                for intf in out["interfaces"]:
                    for neighbor in out["interfaces"][intf]["neighbors"]:
                        if (
                            state
                            in out["interfaces"][intf]["neighbors"][neighbor][
                                "state"
                            ]
                        ):
                            return True
            except KeyError:
                pass
        timeout.sleep()

    return False


def is_ospf_neighbor_established_on_interface(device, interface, max_time=30, check_interval=10):
    """ Verify OSPF is established on the interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            max_time (`int`): Maximum wait time
            check_interval (`int`): Check interval

        Returns:
            result (`bool`): Verified result
    """
    cmd = "show ip ospf neighbor"
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except Exception as e:
            log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
            timeout.sleep()
            continue

        if interface in out.get('interfaces', {}):
            log.info("OSPF interface {intf} is established".format(intf=interface))
            return True

        timeout.sleep()

    return False


def is_ospf_neighbor_state_changed_log(device, interface):
    """ Verify ospf interface didn't flap in the log

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Returns:
            result(`str`): verify result
    """
    result = []
    out = device.parse("show logging")
    p = re.compile(r".*OSPF-5-ADJCHG:.* on {} from [\w]+ to [\w]+.*".format(interface))
    for line in out["logs"]:
        if p.match(line):
            result.append(line)
    return "\n".join(result)


def is_ospf_shutdown(
    device, max_time=15, check_interval=5, interface=None
):
    """ Verifies ospf is shutdown by verifying there are
        no neighbors

        Args:
            device('obj'): device to use
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
            interface ('str'): Interface name
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        neighbors = get_ospf_neighbors(device, interface)
        if not neighbors:
            return True

        log.info(
            "OSPF is not shutdown; neighbors {} are still enabled".format(
                neighbors
            )
        )

        timeout.sleep()

    return False


def verify_ospf_in_state(
    device,
    neighbors=None,
    state=None,
    max_time=15,
    check_interval=5,
    interface=None,
):

    """ Verifies ospf process is enabled by checking if neighbors exist.
        If a list of neighbors is passed it will also verify is those neighbors
        have reached state

        Args:
            device('obj'): device to use
            neighbors('list'): If specified, function will verify the neighbors
                               are listed.
            state('str'): If specified, function will verify the neighbors are in
                          state.
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if not neighbors:
            if state:
                neighbors = get_ospf_neighbors_in_state(
                    device=device,
                    state=state,
                    neighbor_interface=interface,
                )
            else:
                neighbors = get_ospf_neighbors(
                    device=device, neighbor_interface=interface
                )

            if neighbors:
                return True
            else:
                log.info("OSPF is not enabled; no neighbors are enabled.")
        else:
            neighbors_in_state = get_ospf_neighbors_in_state(
                device, state=state
            )
            if set(neighbors).issubset(neighbors_in_state):
                return True

            log.info(
                "OSPF is not enabled; neighbors {} are not enabled.".format(
                    neighbors
                )
            )

        timeout.sleep()

    return False


def is_interface_igp_sync_ospf_enabled(
    interface,
    vrf,
    address_family,
    instance,
    area_address,
    device,
    parsed_output=None,
    max_time=15,
    check_interval=5,
):
    """ Verifies if interface has LDP IGP sync enabled 
        from command 'show ip ospf mpls ldp interface'
        
        Args:
            parsed_output ('dict')  : Output from parser
            interface ('str')       : Interface being checked
            vrf      ('str')        : vrf name
            address_family ('str')  : Interface address family (ipv4 or ipv6)
            instance ('str')        : Instance number
            area_address ('str')    : Area address
            device                  : Device to be executed command
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5

        Raises:
            Exception

        Returns
            None

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if not parsed_output:
            try:
                parsed_output = device.parse("show ip ospf mpls ldp interface")
            except SchemaEmptyParserError as se:
                pass
        try:
            igp_sync = (
                parsed_output["vrf"]
                .get(vrf, {})
                .get("address_family", {})
                .get(address_family, {})
                .get("instance", {})
                .get(instance, {})
                .get("areas", {})
                .get(area_address, {})
                .get("interfaces", {})
                .get(interface, {})
                .get("mpls", {})
                .get("ldp", {})
                .get("igp_sync", False)
            )
            return igp_sync
        except Exception:
            log.error("Could not extract IGP sync information")
        parsed_output = None
        timeout.sleep()
    return False


def verify_ospf_sid_database_prefixes_advertised(device, advertising_router, allowed_prefixes,
                                                 max_time=90, check_interval=10):
    """ Verifies prefixes advertised by advertising_router are only allowed_prefixes

        Args:
            device ('obj'): Device to execute command on
            advertising_router ('str'): Advertising router id
            allowed_prefixes ('list'): Prefixes allowed to be advertised.
                                       Can be subset of full prefix.
            max_time ('int'): Maximum time to wait
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ip ospf segment-routing sid-database")
        except SchemaEmptyParserError:
            return False

        reqs = R(
            ['process_id',
            '(?P<process_id>.*)',
            'sids',
            '(?P<sid>.*)',
            'index',
            '(?P<index>.*)',
            'prefix',
            '(.*)']
        )

        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            key_list = GroupKeys.group_keys(
                reqs=reqs.args, ret_num={}, source=found, all_keys=True
            )

            unexpected_prefix = False
            for v in key_list:
                # Get current dictionary from filtered values

                # Current process id
                c_process_id = v.get('process_id')
                # Current SID
                c_sid = v.get('sid')
                # Current index
                c_index = v.get('index')

                # sid_dict:
                #   {
                #       'codes': 'L',
                #       'prefix': '10.66.12.12/32',
                #       'adv_rtr_id': '10.66.12.12',
                #       'area_id': 10.49.0.0
                #   }
                sid_dict = out['process_id'][c_process_id]['sids'][c_sid]['index'][c_index]

                # Current prefix for SID
                c_prefix = sid_dict.get('prefix')

                # Current IP address for SID
                c_advertising_router = sid_dict.get('adv_rtr_id')

                if c_advertising_router and c_advertising_router == advertising_router:
                    for prefix in allowed_prefixes:
                        if prefix in c_prefix:
                            log.info('Found allowed prefix {}'.format(c_prefix))
                            break
                    else:
                        log.info('Found prefix {}. Allowed prefixes are {}'
                                 .format(c_prefix, allowed_prefixes))
                        unexpected_prefix = True
                        break

            if unexpected_prefix:
                log.info('Unexpected prefixes were found')
                timeout.sleep()
                continue

            log.info('All advertised prefixes under router id {} are allowed'
                     .format(advertising_router))
            return True

    return False



def verify_sid_in_ospf(device, process_id=None, sid=None, code=None, ip_address=None,
    avoid_codes=None, prefix=None, max_time=90, check_interval=10,
    expected_result=True, output=None):
    """ Verifies if SID is found in ospf
        from command 'show ip ospf segment-routing sid-database'

        Args:
            device (`obj`): Device to be executed command
            process_id (`int`): Process Id to check in output
            sid (`int`): SID value
            code (`str`): Check for codes in output
                ex.) code = 'L'
            ip_address (`str`): IP address to check in output
            avoid_codes (`list`): List of codes to avoid
                ex.)
                    avoid_codes = ['L', 'C']
            prefix (`str`): IP address to check as prefix in output
                ex.) prefix = '10.66.12.12/32'
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check
            expected_result ('bool'): Expected result
                set expected_result = False if method should fail
                set expected_result = True if method should pass (default value)
            output ('str'): Pass output as value
            output ('list'): Pass output as reference - modifies the calling output
        Raises:
            None
        Returns
            True/False

    """
    timeout = Timeout(max_time, check_interval)
    out = None
    while timeout.iterate():

        try:
            if output:
                # Can change to reference type and modify original output
                if isinstance(output, list):
                    out = device.parse("show ip ospf segment-routing sid-database", output=output[0])
                else:
                    out = device.parse("show ip ospf segment-routing sid-database", output=output)
            else:
                out = device.parse("show ip ospf segment-routing sid-database")

        except (SchemaEmptyParserError):
            return False
        sid_count = 0

        if not avoid_codes:
            avoid_codes = []

        found = None

        # ex.) Ouput for reference for dictionary out["process_id"]
        # {
        #     'process_id': {
        #         '65109': {
        #             'router_id': '10.66.12.12',
        #             'sids': {
        #                 'total_entries': 1,
        #                 1: {
        #                     'sid': 1,
        #                     'codes': 'L',
        #                     'prefix': '10.66.12.12/32',
        #                     'adv_rtr_id': '10.66.12.12',
        #                     'area_id': 10.49.0.0
        #                 }
        #             }
        #         }
        #     }
        # }

        reqs = R(
            ['process_id',
            '(?P<process_id>{})'.format('.*' if not process_id else process_id),
            'sids',
            '(?P<sid>{})'.format('.*' if not sid else sid),
            'index',
            '(?P<index>.*)',
            'prefix',
            '(.*)']
        )

        found = find([out], reqs, filter_=False, all_keys=True)

        result = False

        if found:
            key_list = GroupKeys.group_keys(
                reqs=reqs.args, ret_num={}, source=found, all_keys=True
            )

            for v in key_list:
                # Get current dictionary from filtered values
                # Current process id
                c_process_id = v.get('process_id', None)
                # Current SID
                c_sid = v.get('sid', None)
                # Current index
                c_index = v.get('index')

                # sid_dict:
                #   {
                #       'codes': 'L',
                #       'prefix': '10.66.12.12/32',
                #       'adv_rtr_id': '10.66.12.12',
                #       'area_id': 10.49.0.0
                #   }
                sid_dict = out['process_id'][c_process_id]['sids'][c_sid]['index'][c_index]

                # Current prefix for SID - Move to next SID values
                c_prefix = sid_dict.get('prefix', None)

                # Current IP address for SID - Move to next SID values
                c_ip_address = sid_dict.get('adv_rtr_id', None)

                # Current code for SID - Move to next SID values
                c_code = sid_dict.get('codes', None)

                # If SID is passed as argument and is not equal to current SID - Move to next SID values
                if sid and c_sid != sid:
                    continue

                # If prefix is passed as argument and is not equal to current Prefix - Move to next SID values
                if prefix and prefix not in c_prefix:
                    continue

                # If IP address is passed as argument and is not equal to current IP address - Move to next SID values
                if ip_address and c_ip_address != ip_address:
                    continue

                # If list of codes passed as avoid_codes
                # If Current code c_code is not None
                # If c_code is found in avoid_codes - Move to next SID values
                if avoid_codes and c_code in avoid_codes:
                    continue

                # If code is passed as argument
                # If Current code c_code is not None
                # If c_code is not equal to code - Move to next SID values
                if code and c_code != code:
                    continue

                # Result is only set to True, if it did not failed in all previous criterias
                # There are some records found in output based on filter
                result = True
                if result and expected_result:
                    return result

        if not expected_result and not result:
            return expected_result
        elif not result or not expected_result:
            timeout.sleep()
            out = device.execute("show ip ospf segment-routing sid-database")
            if isinstance(output, list):
                # Change original ouput pass as refernce type
                output[0] = out
            else:
                output = out
        else:
            return result
    return result

def is_type_10_opaque_area_link_states_originated(device, max_time=60, check_interval=10,
    expected_result=True):
    """ Verifies if Type 10 opaque area link states are originated
        from command 'show ip ospf database opaque-area self-originate'

        Args:
            device (`obj`): Device to be executed command
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check
            expected_result ('bool'): Expected result
                set expected_result = False if method should fail
                set expected_result = True if method should pass (default value)
        Raises:
            None
        Returns
            True
            False

    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ip ospf database opaque-area self-originate')
        except (SchemaEmptyParserError):
            pass

        if out:
            reqs = R(
                [
                'vrf',
                '(?P<vrf>.*)',
                'address_family',
                '(?P<af>.*)',
                'instance',
                '(?P<instance>.*)',
                'areas',
                '(?P<areas>.*)',
                'database',
                'lsa_types',
                '(?P<lsa_types>.*)',
                'lsa_type',
                '(?P<lsa_type>.*)'
                ]
            )

            found = find([out], reqs, filter_=False, all_keys=True)

            if not found and not expected_result:
                return expected_result

            if found:
                key_list = GroupKeys.group_keys(
                    reqs=reqs.args, ret_num={}, source=found, all_keys=True
                )

                if (key_list.pop()['lsa_type'] == 10) == expected_result:
                    return expected_result

        timeout.sleep()

    return False


def verify_opaque_type_7_prefix_and_flags(device, vrf, address_family, instance, prefix,
    flags, max_time=60, check_interval=10, expected_result=True):
    """ Verifies if SID is found in ospf
        from command 'show ip ospf segment-routing sid-database'

        Args:
            device (`obj`): Device to be executed command
            vrf (`str`): VRF name
            address_family (`str`): Address family
            instance (`str`): Instance value
                ex.) instance = '65109'
            prefix (`str`): IP address to check as prefix in output
                ex.) prefix = '10.66.12.12/32'
            flags (`str`): Flags to check in output
                ex.) flags = 'N-bit'
        Raises:
            None
        Returns
            True
            False

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        result = True
        try:
            out = device.parse('show ip ospf database opaque-area self-originate')
        except (SchemaEmptyParserError):
            pass
        if out:
            filter_dict = {}
            filter_dict.update({'flags': flags})
            filter_dict.update({'prefix': prefix})

            for k,v in filter_dict.items():
                reqs = R(
                    [
                        'vrf',
                        vrf,
                        'address_family',
                        address_family,
                        'instance',
                        instance,
                        'areas',
                        '(?P<area>.*)',
                        'database',
                        'lsa_types',
                        '(?P<lsa_types>.*)',
                        'lsas',
                        '(?P<lsas>7.*)',
                        'ospfv2',
                        'body',
                        'opaque',
                        'extended_prefix_tlvs',
                        '(?P<extended_prefix_tlvs>.*)',
                        k,
                        v
                    ]
                )
                found = find([out], reqs, filter_=False, all_keys=True)
                if not found:
                    result = False
                if not result and not expected_result:
                    return expected_result

            if result and expected_result:
                return expected_result
        timeout.sleep()
    return False

def verify_sid_is_advertised_in_ospf(device, router_id, vrf, address_family, instance, prefix,
    flags, max_time=90, check_interval=10, expected_result=True):
    """ Verifies if SID is advertised in ospf
        from command 'show ip ospf database opaque-area adv-router {router_id}'

        Args:
            device (`obj`): Device to be executed command
            router_id (`str`): Router ID
            vrf (`str`): VRF name
            address_family (`str`): Address family
            instance (`str`): Instance value
                ex.) instance = '65109'
            prefix (`str`): IP address to check as prefix in output
                ex.) prefix = '10.66.12.12/32'
            flags (`str`): Flags to check in output
                ex.) flags = 'N-bit'
        Raises:
            None
        Returns
            True
            False

    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        result = True
        try:
            out = device.parse('show ip ospf database opaque-area adv-router {router_id}'.
                    format(router_id=router_id))
        except (SchemaEmptyParserError):
            pass

        if out:
            filter_dict = {}
            filter_dict.update({'flags': flags})
            filter_dict.update({'prefix': prefix})

            for k,v in filter_dict.items():
                reqs = R(
                    [
                        'vrf',
                        vrf,
                        'address_family',
                        address_family,
                        'instance',
                        instance,
                        'areas',
                        '(?P<area>.*)',
                        'database',
                        'lsa_types',
                        '(?P<lsa_types>.*)',
                        'lsas',
                        '(?P<lsas>7.*)',
                        'ospfv2',
                        'body',
                        'opaque',
                        'extended_prefix_tlvs',
                        '(?P<extended_prefix_tlvs>.*)',
                        k,
                        v
                    ]
                )
                found = find([out], reqs, filter_=False, all_keys=True)

                if not found:
                    result = False

                if not result and not expected_result:
                    return expected_result

            if result and expected_result:
                return expected_result
        timeout.sleep()

    return False

def verify_ospf_tilfa_in_state_in_ospf(
    device,
    interface,
    max_time=60,
    check_interval=10,
    process_id=None,
    state="enabled",
):
    """ Verify if TI-LFA is enabled in OSPF

        Args:
            device ('str'): Device object
            interface ('str'): Interface name
            process_id ('int'): Process id
            max_time (int): Maximum wait time in seconds checking an ouput
            check_interval (int): Wait time between iterations when looping

        Raises:
            None
        Returns:
            True
            False
    """

    if state not in ("enabled", "disabled"):
        log.error('Expected state must be either "enabled" or "disabled"')
        return False

    timeout = Timeout(max_time=max_time, interval=check_interval)
    ti_lfa_enabled = "no"
    while timeout.iterate():
        try:
            output = device.parse("show ip ospf fast-reroute ti-lfa")
        except SchemaEmptyParserError:
            if "disabled" == state:
                break
            log.info("Could not find any information about ti-lfa")
            timeout.sleep()
            continue

        if process_id:
            ti_lfa_enabled = (
                output["process_id"]
                .get(process_id, {})
                .get("ospf_object", {})
                .get(interface, {})
                .get("ti_lfa_enabled", "no")
            )
            if ti_lfa_enabled == "yes":
                log.info("TI-LFA is enabled in OSPF on process {process_id} "
                         "and interface {interface} on device {device}"\
                         .format(process_id=process_id, interface=interface, device=device.name))
                return True

        else:
            for process_id in output["process_id"]:
                for intf in output["process_id"][process_id][
                    "ospf_object"
                ].get(interface, {}):
                    ti_lfa_enabled = output["process_id"][process_id].get(
                        "ospf_object", {}
                    )[interface]["ti_lfa_enabled"]
                    if ti_lfa_enabled == "yes":
                        log.info("TI-LFA is enabled in OSPF on process {process_id} "
                                 "and interface {interface} on device {device}"\
                                 .format(process_id=process_id, interface=interface, device=device.name))
                        return True

        if "disabled" == state:
            break

        timeout.sleep()

    log.info("TI-LFA is not enabled in OSPF")
    return False

def is_ospf_tilfa_enabled_in_sr(
    device,
    area=None,
    interface=None,
    max_time=60,
    check_interval=10,
    process_id=None,
    output=None,
    state="enabled"
):
    """ Verify if TI-LFA is enabled in SR

    Args:
        device ('str'): Device object
        interface ('str'): Interface name
        process_id ('int'): Process id
        area ('str'): Ospf area
        neighbor_address ('str'): Neighbor address
        max_time (int): Maximum wait time in seconds checking an ouput
        check_interval (int): Wait time between iterations when looping
        output ('dict'): Parsed output of command 'show ip ospf segment-routing protected-adjacencies'
    Raises:
        None
    Returns:
        True/False
    """

    log.info("Checking if TI-LFA is {} in SR".format(state))

    if not output:
        try:
            output = device.parse(
                "show ip ospf segment-routing protected-adjacencies"
            )
        except SchemaEmptyParserError:
            log.info("TI-LFA is not enabled in SR")
            return False

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        if area and process_id and interface:
            neighbors = (
                output["process_id"]
                .get(process_id, {})
                .get("areas", {})
                .get(area, {})
                .get("neighbors", {})
            )
            for neighbor in neighbors:
                is_enabled = neighbors[neighbor]["interface"].get(interface, False)
                if is_enabled:
                    log.info(
                        "TI-LFA is enabled in SR for interface {interface}".format(
                            interface=interface
                        )
                    )
                    return True

        elif process_id and area:
            is_enabled = (
                output["process_id"]
                .get(process_id, {})
                .get("areas", {})
                .get(area, False)
            )
            if is_enabled:
                log.info(
                    "TI-LFA is enabled for process id {process_id} and area {area}".format(
                        process_id=process_id, area=area
                    )
                )
                return True

        elif process_id:
            is_enabled = (
                output["process_id"].get(process_id, {}).get("areas", False)
            )
            if is_enabled:
                log.info(
                    "TI-LFA is enabled for process id {process_id}".format(
                        process_id=process_id
                    )
                )
                return True

        elif area:
            for process_id in output["process_id"]:
                is_enabled = output["process_id"][process_id]["areas"].get(
                    area, False
                )
                if is_enabled:
                    log.info("TI-LFA is enabled on area {area}".format(area=area))
                    return True

        elif interface:
            for process_id in output["process_id"]:
                for area in output["process_id"][process_id]["areas"]:
                    for neighbor in output["process_id"][process_id]["areas"][
                        area
                    ]["neighbors"]["neighbors"]:
                        for intf in output["process_id"][process_id]["areas"][
                            area
                        ]["neighbors"]["neighbors"][neighbor]["interface"]:
                            if intf == interface:
                                log.info(
                                    "TI-LFA is enabled in SR for interface {interface}".format(
                                        interface=interface
                                    )
                                )
                                log.info("TI-LFA is enabled in SR")
                                return True
        else:
            for process_id in output["process_id"]:
                for area in output["process_id"][process_id].get("areas", {}):
                    log.info(
                        "TI-LFA is enabled in SR for process {process_id} and area {area}".format(
                            process_id=process_id, area=area
                        )
                    )
                    return True
        if state=="disabled" :
            break
        timeout.sleep()
        try:
            output = device.parse(
                "show ip ospf segment-routing protected-adjacencies"
            )
        except SchemaEmptyParserError:
            log.info("TI-LFA is not enabled in SR")
            return False

    log.info("TI-LFA is not enabled in SR")
    return False


def verify_ospf_sr_label_preference(device, process_id, expected_preference, output=None, max_time=60, check_interval=10):
    """ Verify SR label preference for a process id
        Args:
            device ('obj'): Device object
            process_id ('str'): Process if
            expected_preference ('bool'): Sr label preference that is expected
        Returns:
            True/False
        Raises:
            None
    """
    log.info("Getting SR attributes")
    if not output:
        try:
            output = device.parse("show ip ospf segment-routing")
        except SchemaEmptyParserError:
            log.info("Could not find any SR attributes")

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        actual_preference = (
            output["process_id"]
            .get(process_id, {})
            .get("sr_attributes", {})
            .get("sr_label_preferred", False)
        )

        if expected_preference == actual_preference:
            if actual_preference:
                log.info("As expected: SR labels are the preferred ones")
            else:
                log.info("As expected: SR labels are not the preferred ones")

            return True

        try:
            output = device.parse("show ip ospf segment-routing")
        except SchemaEmptyParserError:
            log.info("Could not find any SR attributes")
            timeout.sleep()
            continue

        if actual_preference:
            log.info("As NOT expected: SR labels are the preferred ones")
        else:
            log.info("As NOT expected: SR labels are not the preferred ones")

        timeout.sleep()

    return False


def verify_ospf_segment_routing_gb_srgb_base_and_range(
    device,
    process_id,
    router_id,
    expected_srgb_base=None,
    expected_srgb_range=None,
    max_time=30,
    check_interval=10,
):
    """ Verifies segment routing gb SRGB Base value

        Args:
            device ('obj'): Device to use
            router_id ('str'): Router entry to look under
            expected_srgb_base ('int'): Expected value for SRGB Base
            expected_srgb_base ('int'): Expected value for SRGB Range
            max_time ('int'): Maximum time to wait
            check_interval ('int'): How often to check

        Returns:
             True/False

        Raises:
            None
    """
    log.info(
        "Verifying router {router} has SRGB Base value of {value}".format(
            router=router_id, value=expected_srgb_base
        )
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        srgb_base, srgb_range = device.api.get_ospf_segment_routing_gb_srgb_base_and_range(
            device=device, process_id=process_id, router_id=router_id
        )

        if not (expected_srgb_base and expected_srgb_base != srgb_base) or (expected_srgb_range and expected_srgb_range != srgb_range):
            return True

        if expected_srgb_base and expected_srgb_base != srgb_base:
            log.info(
                "Router {router} has SRGB Base value of {value}. Expected value is {expected}".format(
                    router=router_id, value=srgb_base, expected=expected_srgb_base
                )
            )
        if expected_srgb_range and expected_srgb_range != srgb_range:
            log.info(
                "Router {router} has SRGB Range value of {value}. Expected value is {expected}".format(
                    router=router_id, value=srgb_range, expected=expected_srgb_range
                )
            )

        timeout.sleep()

    return False

def verify_ospf_segment_routing_lb_srlb_base_and_range(
    device,
    process_id,
    router_id,
    expected_srlb_base=None,
    expected_srlb_range=None,
    max_time=30,
    check_interval=10,
):
    """ Verifies segment routing lb SRLB Base value

        Args:
            device ('obj'): Device to use
            process_id ('str'): Ospf process id
            router_id ('str'): Router entry to look under
            expected_srlb_base ('int'): Expected value for SRLB Base
            expected_srlb_range ('int'): Expected value for SRLB Range
            max_time ('int'): Maximum time to wait
            check_interval ('int'): How often to check

        Returns:
             True/False

        Raises:
            None
    """
    log.info(
        "Verifying router {router} has SRLB Base value of {value} and SRLB Range value of {value2}".format(
            router=router_id,
            value=expected_srlb_base,
            value2=expected_srlb_range,
        )
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        srlb_base, srlb_range = device.api.get_ospf_segment_routing_lb_srlb_base_and_range(
            device=device, process_id=process_id, router_id=router_id
        )

        if not (expected_srlb_base and expected_srlb_base != srlb_base) or (
            expected_srlb_range and expected_srlb_range != srlb_range
        ):
            return True

        if expected_srlb_base and expected_srlb_base != srlb_base:
            log.info(
                "Router {router} has SRLB Base value of {value}. Expected value is {expected}".format(
                    router=router_id,
                    value=srlb_base,
                    expected=expected_srlb_base,
                )
            )
        if expected_srlb_range and expected_srlb_range != srlb_range:
            log.info(
                "Router {router} has SRLB Range value of {value}. Expected value is {expected}".format(
                    router=router_id,
                    value=srlb_range,
                    expected=expected_srlb_range,
                )
            )

        timeout.sleep()

    return False

def verify_sid_in_ospf_pairs(device, pairs, process_id=None, max_time=90, check_interval=10,
    expected_result=True, output=None, verbose=True,
    ):

    """ Verifies if SID is found in ospf pairs
        from command 'show ip ospf segment-routing sid-database'

        Args:
            device (`obj`): Device to be executed command
            process_id (`int`): Process Id to check in output
            max_time ('int'): maximum time to wait
            check_interval ('int'): how often to check
            expected_result ('bool'): Expected result
                set expected_result = False if method should fail
                set expected_result = True if method should pass (default value)
            output ('str'): Pass output as value
            pairs = [{'sid': 10, 'prefix':'172.16.1.1/32', 'codes': 'M'}, {...}]


        Raises:
            None
        Returns
            True/False

    """
    pt = PrettyTable()

    pt.field_names = ['SID', 'Codes', 'Prefix', 'Adv Rtr Id', 'Area ID', 'Entry Exist']

    fields_index = {
        'sid': 0,
        'codes': 1,
        'prefix': 2,
        'adv_rtr_id': 3,
        'area_id': 4,
        'entry_exist': 5
    }

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ip ospf segment-routing sid-database", output=output)
        except SchemaEmptyParserError:
            return False
        finally:
            # Set output to None for next iteration
            output = None

        # ex.) Ouput for reference for dictionary out
        # {
        #     'process_id': {
        #         '65109': {
        #             'router_id': '10.66.12.12',
        #             'sids': {
        #                 'total_entries': 1,
        #                 1: {
        #                     'index': {
        #                         1: {
        #                             'codes': 'L',
        #                             'prefix': '10.66.12.12/32',
        #                             'adv_rtr_id': '10.66.12.12',
        #                             'area_id': '10.49.0.0'
        #                         }
        #                     }
        #                 }
        #             }
        #         }
        #     }
        # }

        verified_entries = []
        for pid in out.get('process_id', {}):
            if process_id and pid != process_id:
                continue

            sids_dict = out['process_id'].get(pid, {}).get('sids', {})
            if sids_dict:

                # ex.) Ouput for reference for pairs
                # pairs = [{'sid': 10, 'prefix':'172.16.1.1/32', 'codes': 'M'}, {...}]
                for pairs_dict in pairs:
                    sid_to_verify = pairs_dict.get('sid')

                    if sids_dict.get(sid_to_verify):
                        result = True
                        for entry in sids_dict[sid_to_verify].get('index', {}):
                            temp_dict = {}
                            for k, v in pairs_dict.items():
                                # Sid is already verified at this point. Just add and move to next item
                                if k == 'sid':
                                    temp_dict.update({k: sid_to_verify})
                                    continue

                                c_value = sids_dict[sid_to_verify]['index'][entry].get(k, 'N/A')
                                temp_dict.update({k: c_value})
                                if c_value == 'N/A':
                                    result = False

                            verified_entries.append(temp_dict)
                    else:
                        result = False

                    # Create row for PrettyTable
                    row = ['N/A'] * len(pt.field_names)
                    for key_name, key_index in fields_index.items():
                        # Add all values if result found else add values which we were expecting
                        row[key_index] = pairs_dict.get(key_name, 'N/A')
                    # Update result field of current row
                    row[fields_index['entry_exist']] = 'True' if result else 'False'
                    pt.add_row(row)

        # By default verbose=True will print the PrettyTable. verbose=False will avoid printing PrettyTable.
        if verbose:
            log.info(pt)
        if expected_result and verified_entries == pairs:
            return True
        if not expected_result and verified_entries != pairs:
            return False

        pt.clear_rows()
        timeout.sleep()

    return False


def verify_ospf_neighbor_address_in_state(device, addresses, state, max_time=60, check_interval=10):
    """ Verifies that an ospf neighbor using the provided address is in a specific state

        Args:
            device ('obj'): Device to use
            addresses ('list'): List of addresses to check
            state ('str'): State to verify the interfaces are in
            max_time ('int'): Maximum time to wait
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        addresses_in_state = device.api.get_ospf_neighbor_address_in_state(state)

        if set(addresses).issubset(addresses_in_state):
            return True

        log.info("The following addresses are not in state {state}: {addresses}"
                 .format(state=state, addresses=set(addresses)-set(addresses_in_state)))

        timeout.sleep()

    return False


def verify_ospf_neighbor_addresses_are_not_listed(device, addresses, max_time=60, check_interval=10):
    """ Verifies that an ospf neighbor using the provided address is not listed

        Args:
            device ('obj'): Device to use
            addresses ('list'): List of addresses to check
            max_time ('int'): Maximum time to wait
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        addresses_listed = device.api.get_ospf_neighbor_address_in_state()
        if set(addresses).isdisjoint(addresses_listed):
            return True

        log.info('The following addresses are still listed: {}'
                 .format(list(set(addresses).intersection(addresses_listed))))

        timeout.sleep()

    return False


def verify_ospf_database_contains_sid_neighbor_address_pairs(device, router_id, pairs, vrf, address_family, instance, area, max_time=60, check_interval=10, contains=True):
    """ Verifies the ospf database contains the sid and neighbor address pairs provided

        Args:
            device ('obj'): Device to use
            router_id ('str'): Ospf router id
            pairs ('dict'): Get from 'get_ospf_sr_adj_sid_and_neighbor_address'

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show ip ospf database opaque-area type ext-link adv-router {router_id}'
                               .format(router_id=router_id))
        except SchemaEmptyParserError:
            return False

        verified_dict = {}

        for lsa in (out.get("vrf", {})
                    .get(vrf, {})
                    .get("address_family", {})
                    .get(address_family, {})
                    .get("instance", {})
                    .get(instance, {})
                    .get("areas", {})
                    .get(area, {})
                    .get("database", {})
                    .get("lsa_types", {})
                    .get(10, {})  # 10 is the opaque type. Hardcoded because show command is the opaque type
                    .get("lsas", {})):

            lsa_dict = (out["vrf"][vrf]["address_family"][address_family]["instance"][instance]
                           ["areas"][area]["database"]["lsa_types"][10]["lsas"][lsa]["ospfv2"]
                           ["body"]["opaque"])  # Last 3 keys are mandatory in schema


            for link in lsa_dict.get("extended_link_tlvs", {}):
                sid, remote_address = None, None
                for index in lsa_dict["extended_link_tlvs"][link].get("sub_tlvs", {}):
                    index_dict = lsa_dict["extended_link_tlvs"][link]["sub_tlvs"][index]
                    if index_dict["type"] == "Adj SID":
                        sid = str(index_dict.get("label"))
                    elif index_dict["type"] == "Remote Intf Addr":
                        remote_address = index_dict.get('remote_interface_address')

                if (sid and
                        remote_address and
                        remote_address in pairs and
                        pairs[remote_address] == sid):
                    verified_dict.update({remote_address: sid})

        if contains and pairs == verified_dict:
            return True

        if not contains and not verified_dict:
            return True

        timeout.sleep()

    return False

