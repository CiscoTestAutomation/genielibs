"""Common verify functions for lacp"""

# Python
import re
import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_lacp_link_state(device,
                           interface,
                           links,
                           state_name,
                           expected_state,
                           max_time=30,
                           check_interval=10):
    """ Verify links of lag interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name (lag interface)
            links (`list`): list of links for lag interface
            state_name (`str`): state name where check
            expected_state (`str`): expected state
            max_time ('int'): Maximum time to keep checking
                              Default to 30 secs
            check_interval ('int'): How often to check
                                    Default to 10 secs
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """
    if not isinstance(links, list):
        log.warn("Given 'links' is not list.")
        return None

    timeout = Timeout(max_time, check_interval)
    parsed_output = None
    while timeout.iterate():
        try:
            parsed_output = device.parse(
                'show lacp interfaces {interface}'.format(interface=interface))
        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            timeout.sleep()
            continue

        # example of out
        # {
        #   "lacp-interface-information-list": {
        #     "lacp-interface-information": {
        #       (snip)
        #       "lag-lacp-protocol": [ # <-----
        #         {
        #           "lacp-mux-state": "Collecting distributing",
        #           "lacp-receive-state": "Current",
        #           "lacp-transmit-state": "Fast periodic",
        #           "name": "xe-3/0/1"
        #         }
        #       ],

        lag_lacp_protocol_list = parsed_output.q.get_values('lag-lacp-protocol')

        expected_link_count = sum(
            link['name'] in links
            and link.get(state_name, '') == expected_state
            for link in lag_lacp_protocol_list
        )

        if expected_link_count == len(links):
            return True

        timeout.sleep()
    return False

def verify_lacp_interface_receive_state(
    device, 
    interface, 
    expected_state,
    expected_interface=None,
    max_time=60,
    check_interval=10,
    ):
    """Verify the state of an lackp interface

    Args:
        device (obj): Device object
        interface (str): Interface name. Will be used if expected_interface isn't set
        expected_state (str): Expected state to check against. Defaults to None.
        expected_interface (str, optional): Expected interface to check against. Defaults to None.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    interface_to_use = expected_interface if expected_interface else interface

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show lacp interfaces {interface}'.format(interface=interface))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # {
        # "lacp-interface-information-list": {
        #     "lacp-interface-information": {
        #         "lag-lacp-protocol": [
        #             {
        #                 "lacp-mux-state": "Collecting " "distributing",
        #                 "lacp-receive-state": "Current",
        #                 "lacp-transmit-state": "Fast " "periodic",
        #                 "name": "ge-0/0/0",
        #             },

        interfaces = out.q.get_values('lag-lacp-protocol')
        states = {intr['name']: intr['lacp-receive-state'] for intr in interfaces}

        if expected_state == states.get(interface_to_use, None):
            return True
        
        timeout.sleep()
    
    return False


def verify_lacp_role_activity(
    device, 
    interface, 
    role_activity_dicts,
    max_time=60,
    check_interval=10,
    ):
    """Verify interfaces roles and activities via show lacp interfaces {interface}

    Args:
        device (obj): Device object
        interface (str): Interface name. Will be used if expected_interface isn't set
        role_activity_dicts (dict): Expected interfaces roles and activities.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show lacp interfaces {interface}'.format(interface=interface))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Sample output
        #     {
        #     "lacp-interface-information-list": {
        #         "lacp-interface-information": {
        #             "lag-lacp-state": [
        #                 {
        #                     "lacp-activity": "Active", <-----------
        #                     "lacp-aggregation": "Yes",
        #                     "lacp-collecting": "Yes",
        #                     "lacp-defaulted": "No",
        #                     "lacp-distributing": "Yes",
        #                     "lacp-expired": "No",
        #                     "lacp-role": "Actor", <-----------------
        #                     "lacp-synchronization": "Yes",
        #                     "lacp-timeout": "Fast",
        #                     "name": "xe-3/0/1", <-------------------
        #                 },
        #             ],
        #         }
        #     }
        # }

        lag_lacp_state_dict_list = out.q.get_values("lag-lacp-state")

        # role_activity_dicts example:
        # [
        #         {   'name': 'interface1',
        #             'lacp-role': 'Actor',
        #             'lacp-activity': 'Active'
        #         },
        #         {   'name':'interface2',
        #             'lacp-role': 'Actor',
        #             'lacp-activity': 'Active'
        #         },
        #     ]

        new_lag_lacp_state_dict_list = []
        for i in lag_lacp_state_dict_list:
            tmp_dict = {}
            for key in ["name", "lacp-role", "lacp-activity"]:
                   tmp_dict.update({key: i[key]})
            new_lag_lacp_state_dict_list.append(tmp_dict)

        # check if role_activity_dicts a subset of new_lag_lacp_state_dict_list
        if all(i in new_lag_lacp_state_dict_list for i in role_activity_dicts):
            return True
        timeout.sleep()
    
    return False

