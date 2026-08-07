import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.verify import (
    verify_mld_snooping_address_count,
)


# parsed output of 'show ipv6 mld snooping address count'
PARSED = {'total_number_of_groups': {'mld_groups_count': 551}}


class TestVerifyMldSnoopingAddressCount(unittest.TestCase):

    def test_within_range(self):
        device = Mock()
        device.api.get_mld_snooping_address_count = Mock(
            return_value=PARSED)

        result = verify_mld_snooping_address_count(
            device, min_count=100, max_count=600,
            max_time=1, check_interval=1)

        self.assertTrue(result)

    def test_below_min(self):
        device = Mock()
        device.api.get_mld_snooping_address_count = Mock(
            return_value=PARSED)

        result = verify_mld_snooping_address_count(
            device, min_count=600, max_count=900,
            max_time=1, check_interval=1)

        self.assertFalse(result)

    def test_above_max(self):
        device = Mock()
        device.api.get_mld_snooping_address_count = Mock(
            return_value=PARSED)

        result = verify_mld_snooping_address_count(
            device, min_count=100, max_count=300,
            max_time=1, check_interval=1)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
