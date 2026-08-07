import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.get import (
    get_mld_snooping_address_count,
)


class TestGetMldSnoopingAddressCount(TestCase):

    def test_get_mld_snooping_address_count(self):
        device = Mock()
        parsed = {"total_number_of_groups": {"mld_groups_count": 551}}
        device.parse = Mock(return_value=parsed)

        result = get_mld_snooping_address_count(device)

        device.parse.assert_called_once_with(
            "show ipv6 mld snooping address count")
        self.assertEqual(result, parsed)

    def test_get_mld_snooping_address_count_empty(self):
        from genie.metaparser.util.exceptions import SchemaEmptyParserError
        device = Mock()
        device.parse = Mock(side_effect=SchemaEmptyParserError("empty"))

        result = get_mld_snooping_address_count(device)

        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
