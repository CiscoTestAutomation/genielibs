"""Common verification functions for LDP"""

# Python
import logging
from netaddr import IPAddress
import re

# pyATS
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils import Dq


log = logging.getLogger(__name__)

def verify_ldp_neighbor(device,
                        expected_neighbor,
                        max_time=60,
                        check_interval=10):
    """Verify 'show ldp neighbor'

    Args:
        device ('obj'): device to use
        expected_neighbor ('str'): expected neighbor address
        max_time ('int'): Maximum time to keep checking. Defaults to 60 seconds
        check_interval ('int'): How often to check. Defaults to 10 seconds

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ldp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        #{'interface-name': 'ge-0/0/0.0',
        #'ldp-label-space-id': '59.128.2.250:0',
        #'ldp-neighbor-address': '106.187.14.158',
        #'ldp-remaining-time': '14'
        #}
        ldp_neighbor = Dq(out).get_values('ldp-neighbor-address')
        for neighbor in ldp_neighbor:
            if neighbor != expected_neighbor:
                continue
            return True

        timeout.sleep()
        
    return False

def verify_ldp_interface(device,
                        expected_interface,
                        max_time=60,
                        check_interval=10):
    """Verify 'show ldp neighbor'

    Args:
        device ('obj'): device to use
        expected_interface ('str'): expected interface
        max_time ('int'): Maximum time to keep checking. Defaults to 60 seconds
        check_interval ('int'): How often to check. Defaults to 10 seconds

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ldp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        #{'interface-name': 'ge-0/0/0.0',
        #'ldp-label-space-id': '59.128.2.250:0',
        #'ldp-neighbor-address': '106.187.14.158',
        #'ldp-remaining-time': '14'
        #}
        interface_name_list = Dq(out).get_values('interface-name')
        for interface in interface_name_list:
            if interface != expected_interface:
                continue
            return True

        timeout.sleep()
        
    return False    


def verify_ldp_database_session(
    device,
    interface=None,
    expected_interface=None,
    label_type='input',
    local_label=None,
    max_time=60,
    check_interval=10,
):
    """Verifies ldp session exists

    Args:
        device (obj): device object
        interface (str): Interface to use in show command
        expected_interface (str): Expected interface
        label_type (str): Database label
        local_label (str): Database local label
        max_time (int): Maximum timeout time
        check_interval (int): Interval to check
    """

    timeout = Timeout(max_time, check_interval)
    if label_type.lower() == 'input':
        label_type = 0
    elif label_type.lower() == 'output':
        label_type = 1

    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ldp database session {interface}".format(interface=interface))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        ldp_database = Dq(out).get_values('ldp-database',label_type)
        
        if ldp_database:
            for ldp in ldp_database.get('ldp-binding',[]):
                if label_type == 0:
                    if not ldp.get('ldp-label'):
                        continue
                else:
                    if ldp.get('ldp-label') != str(local_label):
                        continue
                if ldp.get('ldp-prefix').split('/')[0] != expected_interface:
                    continue

                return True

        timeout.sleep()
    return False


def verify_ldp_session(
    device,
    address=None,
    expected_session_state=None,
    max_time=60,
    check_interval=10,
):
    """Verifies ldp session exists

    Args:
        device (obj): device object
        address (str): Neighbor address to check for
        expected_address (str): Expected address
        max_time (int): Maximum timeout time
        check_interval (int): Interval to check
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ldp session")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        sessions = out.q.get_values('ldp-session')

        for session in sessions:
            if address:
                if session['ldp-neighbor-address'] != address:
                    continue

            if expected_session_state:
                if session['ldp-session-state'] != expected_session_state:
                    continue

            return True

        timeout.sleep()
    return False


def verify_igp_metric_in_ldp(
    device,
    expected_metric,
    max_time=60,
    check_interval=10,
):
    """Verifies ldp session exists

    Args:
        device (obj): device object
        expected_metric (str): Expected IGP metric value
        max_time (int, optional): Maximum timeout time. Defaul to 60
        check_interval (int, optional): Interval to check. Default to 10
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ldp overview")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ldp_tracking_igp_metric = out.q.get_values('ldp-tracking-igp-metric', 0)

        if ldp_tracking_igp_metric == expected_metric:
            return True

        timeout.sleep()
    return False
def verify_hello_interval_holdtime(
    device,
    expected_hello_interval,
    expected_hold_time,
    interface,
    max_time=60,
    check_interval=10,
):
    """Verifies ldp session exists

    Args:
        device (obj): device object
        expected_hello_interval (int): Expected Hello interval
        expected_hold_time(int): Expected Holdtime
        interface(str): Address that passed in show command
        max_time (int, optional): Maximum timeout time. Defaul to 60
        check_interval (int, optional): Interval to check. Default to 10
    """

    # {'ldp-interface-information': {'ldp-interface': {'interface-name': 'ge-0/0/0.0',
    #                                                 'ldp-hello-interval': '5',
    #                                                 'ldp-holdtime': '15',
    #                                                 'ldp-interface-local-address': '106.187.14.157',
    #                                                 'ldp-label-space-id': '106.187.14.240:0',
    #                                                 'ldp-neighbor-count': '1',
    #                                                 'ldp-next-hello': '3',
    #                                                 'ldp-transport-address': '106.187.14.240'}}}

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ldp interface {interface} detail".format(interface=interface))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ldp_hello_interval = int(out.q.get_values('ldp-hello-interval', 0))
        ldp_holdtime = int(out.q.get_values('ldp-holdtime', 0))

        if ldp_hello_interval == expected_hello_interval and ldp_holdtime == expected_hold_time:
            return True

        timeout.sleep()
    return False
