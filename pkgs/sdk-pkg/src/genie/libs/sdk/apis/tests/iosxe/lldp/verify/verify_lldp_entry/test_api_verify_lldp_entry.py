import unittest
from genie.libs.sdk.apis.iosxe.lldp.verify import verify_lldp_entry


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


class TestVerifyLldpEntry(unittest.TestCase):

    def test_verify_lldp_entry_none_output(self):
        self.assertFalse(
            verify_lldp_entry(None, 'GigabitEthernet1/0/15'))

    def test_verify_lldp_entry_empty_output(self):
        self.assertFalse(
            verify_lldp_entry({}, 'GigabitEthernet1/0/15'))

    def test_verify_lldp_entry_match(self):
        self.assertTrue(verify_lldp_entry(
            SAMPLE_OUTPUT,
            'GigabitEthernet1/0/15',
            port_id='Gi1/0/1',
            sys_name='R5',
            chassis_id='843d.c6ff.f1b8',
            sys_desc='Cisco IOS Software',
            port_desc='GigabitEthernet1/0/1',
            max_ttl=200, min_ttl=10,
            cap_system=['mac_bridge', 'router'],
            cap_enabled=['mac_bridge', 'router'],
            mgmt_addr='10.9.1.1',
            vlan_id='1'))

    def test_verify_lldp_entry_mismatch_port_id(self):
        self.assertFalse(verify_lldp_entry(
            SAMPLE_OUTPUT,
            'GigabitEthernet1/0/15',
            port_id='Gi9/9/9'))

    def test_verify_lldp_entry_unknown_intf(self):
        self.assertFalse(verify_lldp_entry(
            SAMPLE_OUTPUT,
            'GigabitEthernet9/9/9'))

    def test_verify_lldp_entry_capability_not_found(self):
        self.assertFalse(verify_lldp_entry(
            SAMPLE_OUTPUT,
            'GigabitEthernet1/0/15',
            cap_system=['telephone']))

    def test_verify_lldp_entry_ttl_below_min(self):
        self.assertFalse(verify_lldp_entry(
            SAMPLE_OUTPUT,
            'GigabitEthernet1/0/15',
            min_ttl=200))
