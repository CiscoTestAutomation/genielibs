import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.verify import (
    verify_mac_address_table_entry_flush)


class TestVerifyMacAddressTableEntryFlush(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_verify_mac_address_table_entry_flush(self):
        self.device.api.verify_mac_address_table_entry.return_value = False
        self.assertTrue(
            verify_mac_address_table_entry_flush(
                self.device, 'aaaa.bbbb.cccc', 100,
                interface='GigabitEthernet1/0/1',
                max_time=1, check_interval=1))

    def test_verify_mac_address_table_entry_flush_still_exist(self):
        self.device.api.verify_mac_address_table_entry.return_value = True
        self.assertFalse(
            verify_mac_address_table_entry_flush(
                self.device, 'aaaa.bbbb.cccc', 100,
                interface='GigabitEthernet1/0/1',
                max_time=1, check_interval=1))


if __name__ == '__main__':
    unittest.main()
