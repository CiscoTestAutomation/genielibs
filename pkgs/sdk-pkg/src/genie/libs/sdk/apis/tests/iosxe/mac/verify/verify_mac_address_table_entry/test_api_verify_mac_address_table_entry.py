import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.verify import (
    verify_mac_address_table_entry)


class TestVerifyMacAddressTableEntry(unittest.TestCase):

    # parsed output of 'show mac address-table vlan 100'
    intf_table = {
        'mac_table': {
            'vlans': {
                '100': {
                    'vlan': 100,
                    'mac_addresses': {
                        'aaaa.bbbb.cccc': {
                            'mac_address': 'aaaa.bbbb.cccc',
                            'interfaces': {
                                'GigabitEthernet1/0/1': {
                                    'interface': 'GigabitEthernet1/0/1',
                                    'entry_type': 'static',
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    # parsed output of 'show mac address-table vlan 20' with drop entry
    drop_table = {
        'mac_table': {
            'vlans': {
                '20': {
                    'vlan': 20,
                    'mac_addresses': {
                        'aaaa.bbbb.cccc': {
                            'mac_address': 'aaaa.bbbb.cccc',
                            'drop': {
                                'drop': True,
                                'entry_type': 'static',
                            },
                        },
                    },
                },
            },
        },
    }

    def setUp(self):
        self.device = Mock()

    def test_verify_mac_address_table_entry(self):
        self.device.api.get_mac_address_table.return_value = self.intf_table
        self.assertTrue(
            verify_mac_address_table_entry(
                self.device, 'aaaa.bbbb.cccc', 100,
                interface='GigabitEthernet1/0/1', entry_type='static'))

    def test_verify_mac_address_table_entry_drop(self):
        self.device.api.get_mac_address_table.return_value = self.drop_table
        self.assertTrue(
            verify_mac_address_table_entry(
                self.device, 'aaaa.bbbb.cccc', 20,
                drop=True, entry_type='static'))

    def test_verify_mac_address_table_entry_not_found(self):
        self.device.api.get_mac_address_table.return_value = self.intf_table
        self.assertFalse(
            verify_mac_address_table_entry(
                self.device, 'dddd.eeee.ffff', 100))

    def test_verify_mac_address_table_entry_type_mismatch(self):
        self.device.api.get_mac_address_table.return_value = self.intf_table
        self.assertFalse(
            verify_mac_address_table_entry(
                self.device, 'aaaa.bbbb.cccc', 100,
                interface='GigabitEthernet1/0/1', entry_type='dynamic'))

    def test_verify_mac_address_table_entry_none(self):
        self.device.api.get_mac_address_table.return_value = None
        self.assertFalse(
            verify_mac_address_table_entry(
                self.device, 'aaaa.bbbb.cccc', 100))


if __name__ == '__main__':
    unittest.main()
