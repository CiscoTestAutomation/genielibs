import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.lldp.verify import (
    verify_show_lldp_neighbors_detail)


SAMPLE_OUTPUT = {
    'interfaces': {
        'GigabitEthernet1/0/15': {
            'port_id': {
                'Gi1/0/1': {
                    'neighbors': {
                        'R5': {
                            'chassis_id': '843d.c6ff.f1b8',
                            'port_id': 'Gi1/0/1',
                            'port_description': 'GigabitEthernet1/0/1',
                            'system_name': 'R5',
                            'neighbor_id': 'R5',
                            'system_description': (
                                'Cisco IOS Software, C3750E Software'),
                            'time_remaining': 108,
                            'management_address': '10.9.1.1',
                            'vlan_id': '1',
                            'capabilities': {
                                'mac_bridge': {
                                    'system': True,
                                    'enabled': True,
                                    'name': 'mac_bridge',
                                },
                                'router': {
                                    'system': True,
                                    'enabled': True,
                                    'name': 'router',
                                },
                            },
                        }
                    }
                }
            }
        }
    }
}


class TestVerifyShowLldpNeighborsDetail(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_verify_show_lldp_neighbors_detail_match(self):
        self.device.api.get_lldp_neighbors_info.return_value = SAMPLE_OUTPUT
        self.assertTrue(verify_show_lldp_neighbors_detail(
            self.device, 'GigabitEthernet1/0/15',
            sys_name='R5',
            max_time=2, check_interval=1))

    def test_verify_show_lldp_neighbors_detail_not_found(self):
        self.device.api.get_lldp_neighbors_info.return_value = SAMPLE_OUTPUT
        self.assertFalse(verify_show_lldp_neighbors_detail(
            self.device, 'GigabitEthernet1/0/15',
            sys_name='no-such-host',
            max_time=2, check_interval=1))

    def test_verify_show_lldp_neighbors_detail_no_data(self):
        self.device.api.get_lldp_neighbors_info.return_value = None
        self.assertFalse(verify_show_lldp_neighbors_detail(
            self.device, 'GigabitEthernet1/0/15',
            sys_name='R5',
            max_time=2, check_interval=1))


if __name__ == '__main__':
    unittest.main()
