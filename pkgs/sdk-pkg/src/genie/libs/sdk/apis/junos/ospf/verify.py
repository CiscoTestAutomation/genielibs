"""Common verification functions for OSPF"""

# Python
import logging

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
