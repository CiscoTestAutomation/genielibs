"""Common verification functions for OSPF"""

# Python
import logging

# pyATS
from ats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError
)
from genie.libs.sdk.libs.utils.normalize import GroupKeys

# Utils
from genie.libs.sdk.apis.utils import get_config_dict

# OSPF
from genie.libs.sdk.apis.iosxe.ospf.get import (
    get_ospf_neighbors_in_state,
    get_ospf_neighbors,
)

log = logging.getLogger(__name__)


def verify_ospf_max_metric_configuration(
    device, ospf_process_id, metric_value, max_time=15, check_interval=5
):
    """Verify OSPF max-metric configuration

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process ID
            metric_value (`int`): Metric value to be configured
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            result(`bool`): verify result
            state
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ip ospf max-metric")
        except SchemaEmptyParserError:
            pass

        if out:
            try:
                for area in out["vrf"]["default"]["address_family"]["ipv4"][
                    "instance"
                ][str(ospf_process_id)]["base_topology_mtid"]:
                    res = out["vrf"]["default"]["address_family"]["ipv4"][
                        "instance"
                    ][str(ospf_process_id)]["base_topology_mtid"][area][
                        "router_lsa_max_metric"
                    ][
                        True
                    ][
                        "condition"
                    ]
                    state = out["vrf"]["default"]["address_family"]["ipv4"][
                        "instance"
                    ][str(ospf_process_id)]["base_topology_mtid"][area][
                        "router_lsa_max_metric"
                    ][
                        True
                    ][
                        "state"
                    ]

                    if str(metric_value) in res:
                        return state
            except KeyError:
                pass
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


def verify_sid_in_ospf(device):
    """ Verifies if SID is found in ospf
        from command 'show ip ospf segment-routing sid-database'
        
        Args:
            device (`obj`): Device to be executed command
        Raises:
            None
        Returns
            True
            False

    """
    try:
        out = device.parse("show ip ospf segment-routing sid-database")
    except (SchemaEmptyParserError):
        return False

    sid_count = 0
    try:
        for process_id, v in out["process_id"].items():
            sid_count += len(out["process_id"][process_id]["sids"].keys())
    except KeyError:
        pass

    return sid_count != 0

def is_type_10_opaque_area_link_states_originated(device):
    """ Verifies if Type 10 opaque area link states are originated
        from command 'show ip ospf database opaque-area self-originate'
        
        Args:
            device (`obj`): Device to be executed command
        Raises:
            None
        Returns
            True
            False

    """
    try:
        out = device.parse('show ip ospf database opaque-area self-originate')
    except (SchemaEmptyParserError):
        return False

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
    
    if not found:
        return False

    key_list = GroupKeys.group_keys(
        reqs=reqs.args, ret_num={}, source=found, all_keys=True
    )
    
    return key_list.pop()['lsa_type'] == 10