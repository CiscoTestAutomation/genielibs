import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.configure import (
    unconfigure_ipv6_mld_snooping_querier,
)


class TestUnconfigureIpv6MldSnoopingQuerier(TestCase):

    def test_unconfigure_ipv6_mld_snooping_querier(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ipv6_mld_snooping_querier(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "no ipv6 mld snooping querier"
        )


if __name__ == "__main__":
    unittest.main()
