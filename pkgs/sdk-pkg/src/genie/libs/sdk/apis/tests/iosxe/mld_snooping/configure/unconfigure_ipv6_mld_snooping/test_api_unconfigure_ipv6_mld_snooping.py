import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.configure import (
    unconfigure_ipv6_mld_snooping,
)


class TestUnconfigureIpv6MldSnooping(TestCase):

    def test_unconfigure_ipv6_mld_snooping(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ipv6_mld_snooping(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with("no ipv6 mld snooping")


if __name__ == "__main__":
    unittest.main()
