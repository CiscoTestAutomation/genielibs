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
        address (str): Neighbor address to check for; default to None
        expected_address (str): Expected address; default to None
        max_time (int): Maximum timeout time
        check_interval (int): Interval to check
    """
    # 'ldp-session-information': {
    #     'ldp-session': [{
    #         'ldp-neighbor-address': '10.3.2.23',
    #         'ldp-session-state': 'Operational',
    #         'ldp-connection-state': 'Open',
    #         'ldp-remaining-time': '26',
    #         'ldp-session-adv-mode': 'DU'
    #     }]
    # }
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
                if session.get('ldp-neighbor-address') != address:
                    continue

            if expected_session_state:
                if session.get('ldp-session-state') != expected_session_state:
                    continue

            return True

        timeout.sleep()
    return False

    # "ldp-timer-overview": {
    #     "ldp-instance-keepalive-interval": int,
    #     "ldp-instance-keepalive-timeout": int,
    #     "ldp-instance-link-hello-interval": int,
    #     "ldp-instance-link-hello-hold-time": int,
    #     "ldp-instance-targeted-hello-interval": int,
    #     "ldp-instance-targeted-hello-hold-time": int,
    #     "ldp-instance-label-withdraw-delay": int,
    #     "ldp-instance-make-before-break-timeout": int,
    #     "ldp-instance-make-before-break-switchover-delay": int,
    #     "ldp-instance-link-protection-timeout": int


def verify_ldp_overview(device,
                        default_keepalive_interval=None,
                        default_keepalive_holdtime=None,
                        max_time=60,
                        check_interval=10
                        ):
    """Verifies ldp overview values as indicated

    Args:
        device (obj): device object
        default_keepalive_interval (int): a number for interval; default is None
        default_keepalive_holdtime (int): a number for holdtime; default is None 
        max_time (int): Maximum timeout time; default is 60
        check_interval (int): Interval to check; default is 10
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ldp overview")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        interval_flag = False
        holdtime_flag = False
        # 'ldp-timer-overview': {
        #     'ldp-instance-keepalive-interval': 10,
        #     'ldp-instance-keepalive-timeout': 30,
        #     'ldp-instance-label-withdraw-delay': 60,
        #     'ldp-instance-link-hello-hold-time': 15,
        #     'ldp-instance-link-hello-interval': 5,
        #     'ldp-instance-link-protection-timeout': 120,
        #     'ldp-instance-make-before-break-switchover-delay': 3,
        #     'ldp-instance-make-before-break-timeout': 30,
        #     'ldp-instance-targeted-hello-hold-time': 45,
        #     'ldp-instance-targeted-hello-interval': 15
        overview = out.q.contains('ldp-timer-overview')

        if default_keepalive_interval:
            keepalive_interval = overview.get_values(
                'ldp-instance-keepalive-interval', 0)
            if keepalive_interval == default_keepalive_interval:
                interval_flag = True

        if default_keepalive_holdtime:
            keepalive_timeout = overview.get_values(
                'ldp-instance-keepalive-timeout', 0)
            if keepalive_timeout == default_keepalive_holdtime:
                holdtime_flag = True

        if default_keepalive_interval and default_keepalive_holdtime:
            if holdtime_flag and interval_flag:
                return True

        else:
            if default_keepalive_interval:
                if keepalive_interval:
                    return True

            elif default_keepalive_holdtime:
                if keepalive_timeout:
                    return True

            timeout.sleep()
            continue

        return False


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

        # {'interface-name': 'ge-0/0/0.0',
        # 'ldp-label-space-id': '10.12.2.25:0',
        # 'ldp-neighbor-address': '16.17.14.18',
        # 'ldp-remaining-time': '14'
        # }
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

        # {'interface-name': 'ge-0/0/0.0',
        # 'ldp-label-space-id': '10.1.2.2:0',
        # 'ldp-neighbor-address': '10.17.14.15',
        # 'ldp-remaining-time': '14'
        # }
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
            out = device.parse(
                "show ldp database session {interface}".format(interface=interface))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ldp_database = Dq(out).get_values('ldp-database', label_type)

        if ldp_database:
            for ldp in ldp_database.get('ldp-binding', []):
                if label_type == 0:
                    if not ldp.get('ldp-label'):
                        continue
                    if local_label and ldp.get('ldp-label') != str(local_label):
                        continue
                else:
                    if ldp.get('ldp-label') != str(local_label):
                        continue
                if ldp.get('ldp-prefix').split('/')[0] != expected_interface:
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
        max_time (int, optional): Maximum timeout time. Default to 60
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

        ldp_tracking_igp_metric = out.q.get_values(
            'ldp-tracking-igp-metric', 0)

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
        max_time (int, optional): Maximum timeout time. Default to 60
        check_interval (int, optional): Interval to check. Default to 10
    """

    # {'ldp-interface-information': {'ldp-interface': {'interface-name': 'ge-0/0/0.0',
    #                                                 'ldp-hello-interval': '5',
    #                                                 'ldp-holdtime': '15',
    #                                                 'ldp-interface-local-address': '10.18.14.15',
    #                                                 'ldp-label-space-id': '10.17.10.24:0',
    #                                                 'ldp-neighbor-count': '1',
    #                                                 'ldp-next-hello': '3',
    #                                                 'ldp-transport-address': '10.17.14.24'}}}

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse(
                "show ldp interface {interface} detail".format(interface=interface))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ldp_hello_interval = int(out.q.get_values('ldp-hello-interval', 0))
        ldp_holdtime = int(out.q.get_values('ldp-holdtime', 0))

        if ldp_hello_interval == expected_hello_interval and ldp_holdtime == expected_hold_time:
            return True

        timeout.sleep()
    return False


def verify_ldp_restart_state(
    device,
    expected_restart_state,
    max_time=60,
    check_interval=10,
):
    """Verifies ldp restart state

    Args:
        device (obj): device object
        expected_restart_state (str): Expected state for the restart value in ldp
        max_time (int, optional): Maximum timeout time. Default to 60
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

        #"ldp-gr-overview": {
        #        "ldp-gr-helper": "enabled",
        #        "ldp-gr-max-neighbor-reconnect-time": 120000,
        #        "ldp-gr-max-neighbor-recovery-time": 240000,
        #        "ldp-gr-reconnect-time": 60000,
        #        "ldp-gr-recovery-time": 160000,
        #        "ldp-gr-restart": "enabled",
        #        "ldp-gr-restarting": "false"
        #    }

        ldp_restart_value = out.q.get_values('ldp-gr-restart',0)

        if ldp_restart_value.lower() == expected_restart_state.lower():
            return True

        timeout.sleep()
    return False


def verify_ldp_session_status(
    device,
    address,
    expected_restart_state,
    helper_mode,
    max_time=60,
    check_interval=10,
):
    """Verifies ldp's restart state and helper mode

    Args:
        device (obj): device object
        address (str): Address to use in show command
        expected_restart_state (str): Expected state for the restart value in ldp
        helper_mode (str): helper mode state
        max_time (int, optional): Maximum timeout time. Default to 60
        check_interval (int, optional): Interval to check. Default to 10
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse("show ldp session {address} detail".format(address=address))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        #"ldp-session": {
        #    "ldp-connection-state": "Open",
        #    "ldp-graceful-restart-local": "disabled",
        #    "ldp-graceful-restart-remote": "disabled",
        #    "ldp-holdtime": "30",
        #    "ldp-keepalive-interval": "10",
        #    "ldp-keepalive-time": "3",
        #    "ldp-local-address": "59.128.2.250",
        #    "ldp-local-helper-mode": "enabled",
        #    "ldp-local-label-adv-mode": "Downstream unsolicited"...
        #}
        ldp_restart_value = out.q.get_values('ldp-graceful-restart-remote',0)
        ldp_helper_value = out.q.get_values('ldp-remote-helper-mode',0)

        if ldp_restart_value and ldp_restart_value.lower() != expected_restart_state.lower():
            timeout.sleep()
            continue

        if ldp_helper_value and ldp_helper_value.lower() != helper_mode.lower():
            timeout.sleep()
            continue

        return True
    
    return False