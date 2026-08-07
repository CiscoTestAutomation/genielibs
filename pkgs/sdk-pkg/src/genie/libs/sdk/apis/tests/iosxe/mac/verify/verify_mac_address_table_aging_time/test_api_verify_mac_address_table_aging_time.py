import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.verify import (
    verify_mac_address_table_aging_time)


class TestVerifyMacAddressTableAgingTime(unittest.TestCase):

    # parsed output of 'show mac address-table aging-time'
    aging_time = {'mac_aging_time': 300}

    def setUp(self):
        self.device = Mock()

    def test_verify_mac_address_table_aging_time(self):
        self.device.api.get_mac_address_table_aging_time.return_value = \
            self.aging_time
        self.assertTrue(
            verify_mac_address_table_aging_time(self.device, 300))

    def test_verify_mac_address_table_aging_time_mismatch(self):
        self.device.api.get_mac_address_table_aging_time.return_value = \
            self.aging_time
        self.assertFalse(
            verify_mac_address_table_aging_time(self.device, 100))

    def test_verify_mac_address_table_aging_time_none(self):
        self.device.api.get_mac_address_table_aging_time.return_value = None
        self.assertFalse(
            verify_mac_address_table_aging_time(self.device, 300))


if __name__ == '__main__':
    unittest.main()
