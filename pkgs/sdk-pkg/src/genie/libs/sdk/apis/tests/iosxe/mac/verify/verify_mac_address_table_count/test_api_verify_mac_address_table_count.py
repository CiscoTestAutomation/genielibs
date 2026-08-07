import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.verify import (
    verify_mac_address_table_count)


class TestVerifyMacAddressTableCount(unittest.TestCase):

    # parsed output of 'show mac address-table count'
    count = {
        'vlan': {
            '1': {
                'static_address_count': 1,
                'dynamic_address_count': 8,
                'total_mac_address': 9,
            },
        },
        'total_dynamic_address_count': 10,
        'total_static_address_count': 5,
        'total_mac_address_in_use': 15,
        'total_mac_address_space': 98294,
    }

    # parsed output of 'show mac address-table count vlan 100'
    count_vlan = {
        'Total_dynamic_address_count': 8,
        'Total_static_address_count': 1,
        'Total_mac_address_in_use': 9,
        'Total_mac_address_space': 65521,
    }

    def setUp(self):
        self.device = Mock()

    def test_verify_mac_address_table_count(self):
        self.device.api.get_mac_address_table_count.return_value = self.count
        self.assertTrue(
            verify_mac_address_table_count(
                self.device,
                min_dynamic_address_count=10,
                max_dynamic_address_count=10,
                min_total_mac_address_count=15,
                max_time=1, check_interval=1))

    def test_verify_mac_address_table_count_vlan(self):
        self.device.api.get_mac_address_table_count.return_value = \
            self.count_vlan
        self.assertTrue(
            verify_mac_address_table_count(
                self.device, vlan=100,
                min_dynamic_address_count=8,
                max_static_address_count=1,
                max_time=1, check_interval=1))

    def test_verify_mac_address_table_count_below_min(self):
        self.device.api.get_mac_address_table_count.return_value = self.count
        self.assertFalse(
            verify_mac_address_table_count(
                self.device,
                min_dynamic_address_count=20,
                max_time=1, check_interval=1))

    def test_verify_mac_address_table_count_above_max(self):
        self.device.api.get_mac_address_table_count.return_value = self.count
        self.assertFalse(
            verify_mac_address_table_count(
                self.device,
                max_dynamic_address_count=5,
                max_time=1, check_interval=1))

    def test_verify_mac_address_table_count_none(self):
        self.device.api.get_mac_address_table_count.return_value = None
        self.assertFalse(
            verify_mac_address_table_count(
                self.device,
                min_dynamic_address_count=1,
                max_time=1, check_interval=1))


if __name__ == '__main__':
    unittest.main()
