import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.verify import (
    verify_mac_address_table_entry_learned)


class TestVerifyMacAddressTableEntryLearned(unittest.TestCase):

    def setUp(self):
        self.device = Mock()

    def test_verify_mac_address_table_entry_learned(self):
        self.device.api.verify_mac_address_table_entry.return_value = True
        self.assertTrue(
            verify_mac_address_table_entry_learned(
                self.device, 'aaaa.bbbb.cccc', 100,
                interface='GigabitEthernet1/0/1', entry_type='dynamic',
                max_time=1, check_interval=1))

    def test_verify_mac_address_table_entry_learned_not_exist(self):
        self.device.api.verify_mac_address_table_entry.return_value = False
        self.assertFalse(
            verify_mac_address_table_entry_learned(
                self.device, 'aaaa.bbbb.cccc', 100,
                interface='GigabitEthernet1/0/1', entry_type='dynamic',
                max_time=1, check_interval=1))


if __name__ == '__main__':
    unittest.main()
