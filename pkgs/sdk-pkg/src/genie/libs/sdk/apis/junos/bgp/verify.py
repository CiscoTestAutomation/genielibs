"""Common verification functions for bgp"""

# Python
import re
import logging

# Genie
from genie.utils.dq import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)


def verify_bgp_peer_state(device, interface, expected_state,
                          max_time=60, check_interval=10):
    """
    Verify bgp peer state

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_state('str') : Expected peer state
        check_peer('boolean'): pass True if want to check peer address; default False
        max_time ('int', optional): Maximum time to keep checking. Default to 60
        check_interval ('int', optional): How often to check. Default to 10

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{
    #                                 'flap-count': '0',
    #                                 'peer-address': '20.0.0.3+63208',
    #                                 'peer-state': 'Established',
    #                                   .
    #                                   .
    #                                   .

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        peers_list = out.q.get_values("bgp-peer")

        for peer in peers_list:
            peer_interface = peer.get('peer-address')
            peer_state = peer.get("peer-state")

            # 20.0.0.3+63208
            if '+' in peer_interface:
                peer_interface = peer_interface.split('+')[0]

            # 20.0.0.2/24
            if '/' in interface:
                interface = interface.split('/')[0]

            if peer_interface == interface and peer_state == expected_state:
                return True

        timeout.sleep()
    return False


def verify_bgp_not_peer_state(device, interface, not_expected_state, max_time=60, check_interval=10):
    """
    Verify bgp peer state

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        not_expected_state('str') : Not expected peer state
        max_time ('int', optional): Maximum time to keep checking. Default to 60
        check_interval ('int', optional): How often to check. Default to 10

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{
    #                                 'flap-count': '0',
    #                                 'peer-address': '20.0.0.3+63208',
    #                                 'peer-state': 'Established',
    #                                   .
    #                                   .
    #                                   .

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        peers_list = out.q.get_values("bgp-peer")

        for peer in peers_list:
            peer_interface = peer.get('peer-address')
            peer_state = peer.get("peer-state")

            # 20.0.0.3+63208
            # 20.0.0.2/24
            if '+' in peer_interface:
                peer_interface = peer_interface.split('+')[0]
            elif '/' in peer_interface:
                peer_interface = peer_interface.split('/')[0]
            if '+' in interface:
                interface = interface.split('+')[0]
            elif '/' in interface:
                interface = interface.split('/')[0]

            if peer_interface == interface and peer_state != not_expected_state:
                return True

        timeout.sleep()
    return False


def verify_bgp_last_error(device, interface, expected_error, max_time=60, check_interval=10):
    """
    Verify bgp last error

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_error('str') : Expected last error
        max_time ('int', optional): Maximum time to keep checking. Default to 60
        check_interval ('int', optional): How often to check. Default to 10

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{
    #                                 'flap-count': '0',
    #                                 'peer-address': '20.0.0.3+63208',
    #                                 'last-error': 'None',
    #                                   .
    #                                   .
    #                                   .

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        peers_list = out.q.get_values("bgp-peer")

        for peer in peers_list:
            peer_interface = peer.get('peer-address')
            error_msg = peer.get("last-error")

            # 20.0.0.3+63208
            if '+' in peer_interface:
                peer_interface = peer_interface.split('+')[0]

            if peer_interface == interface and error_msg == expected_error:
                return True

        timeout.sleep()
    return False


def verify_bgp_error_message(device, interface, expected_message, expected_error_message, max_time=60, check_interval=10):
    """
    Verify bgp last error

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_message('str'): Expected message
        expected_error_message('str') : Expected error message
        max_time ('int', optional): Maximum time to keep checking. Default to 60
        check_interval ('int', optional): How often to check. Default to 10

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{
    #                                 "flap-count": '0',
    #                                 "peer-address": '20.0.0.3+63208',
    #                                 "peer-restart-flags-received": 'Notification',
    #                                 "bgp-error": [
    #                                 {
    #                                     "name": "Hold Timer Expired " "Error",
    #                                     "receive-count": "40",
    #                                     "send-count": "27",
    #                                 },
    #                                 {"name": "Cease", "receive-count": "0", "send-count": "16"},
    #                             ],
    #                                   .
    #                                   .
    #                                   .

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        peers_list = out.q.get_values("bgp-peer")

        for peer in peers_list:

            peer_interface = peer.get('peer-address')

            # 20.0.0.3+63208
            if '+' in peer_interface:
                peer_interface = peer_interface.split('+')[0]

            notification_message = Dq(peer).get_values(
                "peer-restart-flags-received", 0)

            error_message_dict = Dq(peer).get_values("bgp-error", 0)

            if len(notification_message) > 0 and error_message_dict:
                if peer_interface == interface and notification_message == expected_message and error_message_dict.get('name') == expected_error_message:
                    return True

        timeout.sleep()
    return False


def verify_bgp_holdtime(device, expected_holdtime, interface,
                        max_time=60, check_interval=10):
    """
    Verify bgp holdtimer with peer {interface}

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_holdtime('str'): Expected holdtime
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds
        check_interval ('int', optional): How often to check. Default to 10 seconds

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        filter_output = out.q.contains(
            'holdtime|peer-address', regex=True).reconstruct()

        # {'bgp-information': {
        #     'bgp-peer': [
        #         {'bgp-option-information': {
        #                 'holdtime': '30'},
        #          'peer-address': '20.0.0.3+179'},
        #         {'bgp-option-information': {
        #                 'holdtime': '10'},
        #          'peer-address': '2001:20::3+179'}]}}

        peer_list = filter_output.get('bgp-information').get('bgp-peer')

        for peer in peer_list:

            # 20.0.0.3+63208
            peer_address = peer.get('peer-address').split('+')[0]

            if peer_address == interface and\
                    Dq(peer).get_values('holdtime')[0] == str(expected_holdtime):
                return True

        timeout.sleep()
    return False


def verify_bgp_active_holdtime(device, expected_holdtime, interface,
                               max_time=60, check_interval=10):
    """
    Verify bgp active holdtimer with peer {interface}

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_holdtime('str'): Expected active holdtime
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds
        check_interval ('int', optional): How often to check. Default to 10 seconds

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        filter_output = out.q.contains(
            'active-holdtime|peer-address', regex=True).reconstruct()

        # {'bgp-information': {'bgp-peer': [{'peer-address': '20.0.0.3+179',
        #                                 'active-holdtime': '30'},
        #                                 {'peer-address': '2001:20::3+179',
        #                                 'active-holdtime': '60'}]}}

        peer_list = filter_output.get('bgp-information').get('bgp-peer')

        for peer in peer_list:

            peer_address = peer.get('peer-address').split('+')[0]

            if peer_address == interface and\
                    Dq(peer).get_values('active-holdtime', 0) == str(expected_holdtime):
                return True

        timeout.sleep()
    return False


def is_bgp_running(device, max_time=60, check_interval=10):
    """
    Verify if bgp is running

    Args:
        device('obj'): device to use
        max_time ('int', optional): Maximum time to keep checking. Default to 60
        check_interval ('int', optional): How often to check. Default to 10

    Returns:
        Boolean
    Raises:
        N/A
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer'; [], 'is-bgp-running': '\r\nBGP is not running'}}

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        is_bgp_running = out.q.get_values("is-bgp-running")

        if False in is_bgp_running:
            return True

        timeout.sleep()
    return False


def is_bgp_neighbor_authentication_key_configured(device, interface=None, max_time=60, check_interval=10):
    """
    Verify that all of bgp neighbors have Authentication key is configured

    Args:
        device('obj'): device to use
        interface('str'): peer interface. Default to None.
        max_time ('int', optional): Maximum time to keep checking. Default to 60
        check_interval ('int', optional): How often to check. Default to 10

    Returns:
        Boolean
    Raises:
        N/A
    """
    timeout = Timeout(max_time, check_interval)
    auth_key_not_configured = False

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{
    #                                 'flap-count': '0',
    #                                 'peer-address': '20.0.0.3+63208',
    #                                 'peer-state': 'Established',
    #                                  "bgp-option-information": {
    #                                           "address-families": "inet-unicast " "inet-labeled-unicast",
    #                                           "authentication-configured": True,

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        peers_list = out.q.get_values("bgp-peer")
        if interface:
            # 20.0.0.3+63208
            # 20.0.0.2/24
            if '+' in interface:
                interface = interface.split('+')[0]
            elif '/' in interface:
                interface = interface.split('/')[0]

        for peer in peers_list:
            # If interface is given, API checks authorization key is configured for given
            # the interface else it will check the authorization key for all peers.
            if interface:
                peer_interface = peer.get('peer-address', '')

                # 20.0.0.3+63208
                # 20.0.0.2/24
                if '+' in peer_interface:
                    peer_interface = peer_interface.split('+')[0]
                elif '/' in peer_interface:
                    peer_interface = peer_interface.split('/')[0]

                if peer_interface == interface and peer.get('bgp-option-information', {}).get(
                        'authentication-configured', False):
                    return True

            elif not peer.get('bgp-option-information', {}).get(
                    'authentication-configured', False):
                auth_key_not_configured = True
                break

        if not interface and not auth_key_not_configured:
            return True

        timeout.sleep()
    return False

def verify_bgp_all_neighbor_status(device, expected_state, max_time=60, check_interval=10):
    """
    Verify all bgp peer states

    Args:
        device('obj'): device to use
        expected_state('str') : Expected peer state
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds
        check_interval ('int', optional): How often to check. Default to 10 seconds

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{
    #                                 'flap-count': '0',
    #                                 'peer-address': '20.0.0.3+63208', 
    #                                 'peer-state': 'Established',
    #                                   .
    #                                   .
    #                                   .

  
    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        status_set = set(out.q.get_values('peer-state'))

        if len(status_set)==1 and expected_state in status_set:
            return True

        timeout.sleep()
    return False  


def verify_bgp_updown_time(device, given_seconds, max_time=60, check_interval=10):
    """
    Verify the up/down time of all neighbors is less than given_time

    Args:
        device('obj'): device to use
        given_seconds('int') : Given time in seconds
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds
        check_interval ('int', optional): How often to check. Default to 10 seconds

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp summary"

    while timeout.iterate():
        try:
            out = device.parse('show bgp summary')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # 'bgp-peer': [{'bgp-rib': [{'accepted-prefix-count': '0',
        #                             'active-prefix-count': '0',
        #                             'name': 'inet.0',
        #                             'received-prefix-count': '0',
        #                             'suppressed-prefix-count': '0'}],
        #             'elapsed-time': {'#text': '1:01'}, <-------------
        #             'flap-count': '1',
        
        # time_list: ['1:01', '57']
        time_list = out.q.get_values('#text')

        seconds_per_hour = 60*60
        seconds_per_day = 24*seconds_per_hour
        seconds_per_week = 7*seconds_per_day

        for t in time_list:

            # '1:01'
            p_min = re.compile(r'^\d+\:\d+$')
            if p_min.match(t):
                min_sec_list = t.split(':')
                t = int(min_sec_list[0])*60 + int(min_sec_list[1])

            # '11:11:11'
            p_hour = re.compile(r'^\d+\:\d+\:\d+$')
            if p_hour.match(t):
                hour_min_sec_list = t.split(':')
                t = int(hour_min_sec_list[0])*seconds_per_hour+\
                    int(hour_min_sec_list[1])*60+\
                    int(hour_min_sec_list[2])

            # "29w5d 22:42:36"
            p_day = re.compile(r'^(?P<week>\d+)w(?P<day>\d+)d\s+(?P<hour>\d+)\:(?P<minute>\d+)\:(?P<second>\d+)$')
            p_day_match = p_day.match(t)
            if p_day_match:
                group = p_day_match.groupdict()
                t = int(group['week'])*seconds_per_week+\
                    int(group['day'])*seconds_per_day+\
                    int(group['hour'])*seconds_per_hour+\
                    int(group['minute'])*60+\
                    int(group['second'])
            
            else:
                t = int(t)

            # compare current up/dwn time with given time
            if t > given_seconds:
                return False

        timeout.sleep()
    return True

def get_bgp_neighbor_prefixes_count(device, interface, max_time=60, check_interval=10):
    """
    Get bgp neighbor accepted, received or advertised prefixes count

    Args:
        device('obj'): device to use
        interface('str'): peer interface. Default to None.
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds.
        check_interval ('int', optional): How often to check. Default to 10 seconds.

    Returns:
        Boolean
    Raises:
        N/A
    """
    timeout = Timeout(max_time, check_interval)
    prefixes_count_dict = {}

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{
    #                                 "bgp-rib": [
    #                                         {
    #                                             "accepted-prefix-count": "684",
    #                                             "active-prefix-count": "682",
    #                                             "advertised-prefix-count": "0",
    #                                             "bgp-rib-state": "BGP restart " "is complete",
    #                                             "name": "inet.0",
    #                                             "received-prefix-count": "684",
    #                                             "rib-bit": "20000",
    #                                             "send-state": "in sync",
    #                                             "suppressed-prefix-count": "0",
    #                                         },

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        peers_list = out.q.get_values("bgp-peer")
        # 20.0.0.3+63208
        # 20.0.0.2/24
        if '+' in interface:
            interface = interface.split('+')[0]
        elif '/' in interface:
            interface = interface.split('/')[0]

        for peer in peers_list:
            peer_interface = peer.get('peer-address', '')

            # 20.0.0.3+63208
            # 20.0.0.2/24
            if '+' in peer_interface:
                peer_interface = peer_interface.split('+')[0]
            elif '/' in peer_interface:
                peer_interface = peer_interface.split('/')[0]

            if peer_interface == interface:
                bgp_rib_list = peer.get('bgp-rib', [])
                for bgp_rib in bgp_rib_list:
                    if bgp_rib.get('accepted-prefix-count', None):
                        prefixes_count_dict['accepted_prefix_count'] = int(bgp_rib.get('accepted-prefix-count'))
                    if bgp_rib.get('received-prefix-count', None):
                        prefixes_count_dict['received_prefix_count'] = int(bgp_rib.get('received-prefix-count'))
                    if bgp_rib.get('advertised-prefix-count', None):
                        prefixes_count_dict['advertised_prefix_count'] = int(bgp_rib.get('advertised-prefix-count'))
                return prefixes_count_dict

        timeout.sleep()
    return prefixes_count_dict
