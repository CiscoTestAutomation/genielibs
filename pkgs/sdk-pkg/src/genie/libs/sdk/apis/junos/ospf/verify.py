"""Common verification functions for OSPF"""

# Python
import logging
import re

# pyATS
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys

log = logging.getLogger(__name__)


def verify_ospf_interface_cost(device, interface, expected_cost, cost_type='ospf', instance=None,
                               area=None, max_time=60, check_interval=15):
    """ Verifies ospf cost on interface

        Args:
            device ('obj'): device to use
            interface ('str'): Interface to use
            cost_type ('str'): Cost type configured
            expected_cost ('int'): Expected configured cost
            instance ('str'): Instance to use
            area ('str'): Area to use
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    if 'ospf' in cost_type.lower():
        while timeout.iterate():
            try:
                out = device.parse('show ospf interface {interface} detail'.format(interface=interface))
            except SchemaEmptyParserError:
                log.info('Parser is empty')
                timeout.sleep()
                continue

            reqs = R([
                'instance',
                '{}'.format(instance if instance else 'master'),
                'areas',
                '{}'.format(area if area else '(.*)'),
                'interfaces',
                interface,
                'cost',
                '(?P<cost>.*)'
            ])

            found = find([out], reqs, filter_=False, all_keys=True)
            if found:
                keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={},
                                            source=found, all_keys=True)
                if 'cost' in keys[0] and int(expected_cost) == int(keys[0]['cost']):
                    return True

            timeout.sleep()
        return False
    elif 'te' in cost_type.lower():
        while timeout.iterate():
            try:
                out = device.parse('show interfaces {interface} terse'.format(interface=interface))
            except SchemaEmptyParserError:
                log.info('Parser is empty')
                timeout.sleep()
                continue

            reqs = R([
                interface,
                'protocol',
                'inet',
                '(.*)',
                'local',
                '(?P<local>.*)'
            ])

            found = find([out], reqs, filter_=False, all_keys=True)
            if found:
                keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={},
                                            source=found, all_keys=True)
                local_address = keys[0].get('local')

                try:
                    out = device.parse('show ted database extensive')
                except SchemaEmptyParserError:
                    log.info('Parser is empty')
                    timeout.sleep()
                    continue

                reqs = R([
                    'node',
                    '(.*)',
                    'protocol',
                    '(.*)',
                    'to',
                    '(.*)',
                    'local',
                    local_address.split('/')[0],
                    'remote',
                    '(.*)',
                    'metric',
                    '(?P<metric>.*)'
                ])
                found = find([out], reqs, filter_=False, all_keys=True)
                if found:
                    keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={},
                                                source=found, all_keys=True)
                    if 'metric' in keys[0] and int(expected_cost) == int(keys[0]['metric']):
                        return True

            timeout.sleep()
        return False

    log.info('This api does not support cost type {}'.format(cost_type))


def verify_ospf_neighbor_state(device, state, interface, ospf_name='ospf', max_time=60, check_interval=10):
    """ Verifies state of ospf

        Args:
            device ('obj'): device to use
            ospf_name ('str'): Expected to be either ospf or ospf3
            state ('str'): State of the interface
            interface ('str'): Name of interface
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse('show {} neighbor'.format(ospf_name))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        neighbors = output[ospf_name+'-neighbor-information'][ospf_name+'-neighbor']
        for neighbor in neighbors:
            if(neighbor['interface-name'] == interface and neighbor['ospf-neighbor-state'].lower() == state.lower() ):
                return True

        timeout.sleep()

    return False

def verify_no_ospf_neigbor_output(device, extensive=False, ospf_name='ospf', max_time=60, check_interval=10):
    """ Verifies state of ospf

        Args:
            device ('obj'): device to use
            ospf_name ('str'): Expected to be either ospf or ospf3
            extensive ('bool'): If ospf command is extensive
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        
        if extensive:
            output = device.execute('show {} neighbor extensive'.format(ospf_name))
        else:
            output = device.execute('show {} neighbor'.format(ospf_name))
        
        if not output:
            return True
            
        timeout.sleep()

    return False


def verify_neighbor_state_went_down(device, interface, realm, fail_reason, max_time=60, check_interval=10):
    """ Verifies state of ospf

        Args:
            device ('obj'): device to use
            interface ('str'): Interface that went down
            realm ('str'): ospf/ospf3 realm
            fail_reason ('str'): Reason state changed from full to down
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    regex_string1 = 'area +0.0.0.0\)) +state +'\
                    'changed +from +Full +to +Down +due +to +(?P<asdf>'
    regex_string2 = '[\s\S]+)$'
    temp = ('^(?P<ignored_portion>[\s\S]+)realm +(?P<interface>'
    '{realm} {interface} {regex_string1}{fail_reason}{regex_string2}'.format(
                        realm=realm,
                        interface = interface,
                        regex_string1 = regex_string1,
                        regex_string2 = regex_string2,
                        fail_reason = fail_reason
                    ))
    
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        output = device.execute('show log messages')
        for line in output.splitlines():
            line = line.strip()
            
            m = re.match(temp,line)
            if m:
                return True
        timeout.sleep()

    return False


def verify_default_route_ospf(device, route, expect_output, ip_type='ipv4', max_time=80, check_interval=10):
    """ Verifies state of ospf

        Args:
            device ('obj'): device to use
            ip_type ('str'): Either ipv4/ipv6
            route ('str'): ipv4/ipv6 default route
            expect_output ('bool'): Flag, either expecting output or no output 
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse('show route protocol ospf')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        route_tables = output['route-information']['route-table']
        if(ip_type == 'ipv4'):
            for routes in route_tables:
                if(routes['table-name'] == 'inet.0'):
                    default_route = routes['rt'][0]['rt-destination']
        else:
            for routes in route_tables:
                if(routes['table-name'] == 'inet6.0'):
                    default_route = routes['rt'][0]['rt-destination']

        if expect_output:
            if default_route == route:
                return True
        else:
            if default_route != route:
                return True
        timeout.sleep()

    return False
