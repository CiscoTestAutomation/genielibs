"""Common verification functions for device tracking"""

# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout
from genie.libs.parser.utils.common import Common as genie_common

log = logging.getLogger(__name__)


def verify_device_tracking_database(device, max_time=120,
                                    interval_time=5, **kwargs):
    '''Verify "show device-tracking database" output
        Args:
            device ('obj'): device object
            max_time('int', Optional): maximum time to wait, default 120s
            interval_time('int', Optional): how often to check, default 5s
            **kwargs (optional) :
                interface ('str'): interface name, e.g. GigabitEthernet0/0/0
                network_layer_address ('str'): network layer address, e.g.
                                               10.22.66.10
                link_layer_address ('str'): link layer address, e.g.
                                            7081.05ff.eb40
                vlan_id (int): VLAN ID, e.g. 10
                state ('str'): state, e.g. REACHABLE
        Returns:
            True/False
    '''
    def check_device_tracking_database(device, **kwargs):
        try:
            output = device.parse('show device-tracking database')
        except SchemaEmptyParserError:
            log.debug('No device-tracking database output found')
            return False

        output_list = list((output or {}).get('device', {}).values())
        if not output_list:
            log.debug(
                'No device entries found in device-tracking database output')
            return False

        kwargs = {k: (genie_common.convert_intf_name(v) \
                      if k == 'interface' else v) for k, v in kwargs.items()}
        for i in output_list:
            if 'interface' in i:
                i['interface'] = genie_common.convert_intf_name(i['interface'])
            if kwargs.items() <= i.items():
                return True
            else:
                continue
        else:
            log.debug(f'Verify device tracking database failed, '
                      f'expect {kwargs} in output: {output_list}')
            return False
    timeout = Timeout(max_time, interval_time)
    while timeout.iterate():
        if check_device_tracking_database(device, **kwargs) is True:
            return True
        else:
            timeout.sleep()
    log.debug(
        f'Verify device tracking database failed, expect {kwargs} in output')
    return False
